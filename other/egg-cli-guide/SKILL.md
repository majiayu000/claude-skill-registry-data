---
name: egg-cli-guide
description: CLI usage guide for the egg scaffolding tool. Use when an agent or user wants to hatch a template, needs the preview/apply/rollback/discard/transactions transaction flow, wants to manage templates (create/list/detail/install/validate/duplicate/move/delete/open), or wants to declare/pin/sync template sources reproducibly via an eggs.yml manifest (egg template sync/update).
---

# egg CLI Guide

egg is a template scaffolding tool with macro substitution and lifecycle hooks. It is agent-first: `egg hatch` defaults to a non-interactive transaction flow that emits JSON on stdout, so an agent can preview a change, inspect it, and only commit after approval.

```
egg <subcommand>
  template   Manage templates.
  hatch      Use a template to generate files with macro substitution.
  mcp        Start the MCP server for AI assistant integration.
```

## Template Locations

- **Global**: `~/.eggs/<TemplateName>/`
- **Project-local**: `./.eggs/<TemplateName>/`

Project-local templates take precedence over global ones of the same name: `detail`, `hatch`, and the MCP tools resolve custom `--template-search-paths` first, then project, then global. `egg template detail <name> --location <global|project>` (and the `location` argument of `egg_template_detail`) searches only that location. `egg template list` shows both entries (under `~/.eggs` and `./.eggs`, or with `location` set in JSON) when a project template shadows a global one.

## Agent Transaction Flow (egg hatch)

This is the flow to use by default. Every command below is non-interactive and emits JSON on stdout.

```sh
egg hatch preview <template> [--macro-name value ...] [--include <pathspec>] [--exclude <pathspec>] [--output <dir>] [--diff] [--allow-write <path> ...] [--allow-large-staging] [--no-sandbox --user-confirmed-no-sandbox]
egg hatch apply <applyToken> [--force] [--working-directory <dir>]
egg hatch rollback <rollbackId> [--force]
egg hatch discard <applyToken> [--force]
egg hatch transactions
```

The working directory should be a git repository — the staged change model
rides on git, and `.gitignore` scopes what counts as a change. In a fresh
directory, run `git init` first. A non-git directory is stageable with
explicit consent: `preview` refuses it with the resolved directory and its
measured file count, and `--allow-non-git-staging` (`allow_non_git_staging`
over MCP) proceeds — every file is then copied with no `.gitignore`
filtering, and script-generated artifacts appear as changes (the result
carries a `non_git_staging` warning). Prefer `git init`. Run from the repository root
unless you mean to scope everything to a subdirectory: staging and relative
`hatch.output` paths resolve against the current directory, and the preview
result carries a `subdirectory_of_repository` warning when they differ.

**Staging scope and cost.** `preview` clones the working directory twice
(workspace + reference). Only git-tracked files and untracked files not
covered by `.gitignore` are cloned (egg's own `.egg/` records are always
excluded, like git excludes `.git`), each as an APFS copy-on-write clone — so
the cost is per *file count*, not bytes. Above 20,000 files preview refuses
with a `stagingTooLarge` error naming the options: scope the clone to a
subdirectory with `--output <subdir>` (CLI) / `staging_root` (MCP), write
directly with `egg hatch direct <template> --no-staging` (no preview or
rollback), or pass `--allow-large-staging` / `allow_large_staging: true` to
proceed anyway. Prefer scoping; only bypass the guard when the user
understands the wait.

Every transaction moves through one state machine, recorded in
`.egg/transactions/<token>/metadata.json`. The `applyToken` and `rollbackId`
are always the same value:

```
preview ──apply──▶ applied ──rollback──▶ rolledBack ──apply──▶ applied (fresh bundle)
preview ──discard──▶ deleted
rolledBack ──discard──▶ deleted
applied ──discard --force──▶ deleted (records only; applied files stay)
```

- **`preview`** stages the template in an isolated clone and reports the proposed `changes`, any `warnings`, the `scriptOutput` of its lifecycle scripts, and an `applyToken`. Nothing is written to the working directory yet.
  - **`scriptOutput` is how a template author talks to you.** Lifecycle scripts run during `preview` (`apply` only copies the resulting files), so this is the only response that carries what they printed — a `post_hatch` step saying "now run `pnpm install`" reaches you here or nowhere. Read it before you report the preview as done. Each entry names its `phase` (`pre_hatch` or `post_hatch`), `index`, and `id` when the step declares one, plus `stdout`, `truncated`, and `skipped`. A step whose `if:` condition was false is reported with `skipped: true` and empty `stdout`, so "printed nothing" stays distinguishable from "never ran". Output past 64 KB per step is cut with `truncated: true`, keeping the leading bytes — where a deliberate message lives, ahead of any build noise. The `hatch` phase is pure file expansion and has no script steps, so it never appears. When a step exits non-zero the preview fails instead of returning a result, and that step's stdout is reported in the error message itself (there keeping the trailing bytes, where a failure's cause is).
  - `--include <pathspec>` forces a normally git-ignored path into the change set.
  - `--exclude <pathspec>` drops matching paths from the change set.
  - `--output <dir>` sets the directory the generated output targets. It is also the directory staging clones from and applies back into — use it to scope staging to a subdirectory of a large repository (the transaction records land under it). Follow the returned `nextCommands` verbatim: they carry the matching `--working-directory <dir>` that apply/rollback/discard need to find those records.
  - `--diff` includes each change's unified diff in the response (off by default).
  - `--allow-write <path>` (repeatable) consents to lifecycle-script writes on an external path the template declares in `config.yml`'s `sandbox.allowed_paths`. If a template declares such paths and none are consented, preview fails fast (before running anything) listing the expanded paths; show them to the user, ask for approval, and retry naming only the approved paths. Consenting to an undeclared path is an error. Writes to approved paths happen during preview and are not reverted by discard/rollback.
  - `--no-sandbox` disables the `sandbox-exec` guard around lifecycle scripts during preview only when paired with `--user-confirmed-no-sandbox` after explicit user approval. The command stays non-interactive and does not classify script contents. Prefer `--allow-write` for declared paths; reserve `--no-sandbox` for cases the sandbox cannot express.
  - **What the sandbox does and does not protect.** Lifecycle scripts run under `sandbox-exec` with writes confined to the staging clone, the declared-and-consented `allowed_paths`, and the temp directories (`/private/tmp`, `/private/var/folders`, plus the directory `TMPDIR` points to when it lives elsewhere, e.g. on an external volume — resolved to its real path, exactly that directory and not its parent; needed for scratch space and atomic writes); writes to the real working directory and everything else are denied. It is a *write* boundary, not a confidentiality boundary: scripts can **read any file the user can read and use the network**. Treat hatching a template like running its code — only hatch templates you trust, and remember that script side effects (network calls, temp-dir writes, consented external writes) happen at preview time and are not reverted by discard or rollback.
- **`apply <applyToken>`** writes the previewed changes to the real working directory and returns a `rollbackId`. Fails if the working directory drifted since the preview, unless `--force` is passed. Also re-applies a `rolledBack` transaction with the same token (a fresh rollback bundle replaces the consumed one; the result carries a `reapplied_after_rollback` warning).
- **`rollback <rollbackId>`** restores the pre-apply state and marks the transaction `rolledBack`, so it can be re-applied later. Fails if a file was hand-edited since the apply, unless `--force` is passed.
- **`discard <applyToken>`** deletes the transaction's records — the staged transaction and its rollback bundle — as a pair, from any state. Applied files in the working directory are never touched. Discarding an `applied` transaction requires `--force`, because deleting its bundle removes the only way to undo the apply; ask the user before forcing.
- **`transactions`** lists every record under `.egg/` as JSON: token, status (`preview`/`applied`/`rolledBack`, plus `corrupt` for unreadable metadata and `orphanedRollback` for bundles left by older egg versions), template name, and bundle presence. Pass `--size` (CLI) / `include_sizes: true` (MCP) to also compute each record's disk footprint (`sizeBytes`); it walks the full staged trees, so leave it off for routine status checks.

Run `egg template detail <name>` before `preview` to learn exactly which macro flags a template needs.

### Recommended agent sequence

1. `egg template detail <name>` to read required macros.
2. `egg hatch preview <name> --macro-name value ...` to produce an `applyToken` and a change list.
3. Inspect `changes`, `warnings`, and `scriptOutput` in the JSON response. Relay anything the lifecycle scripts printed for the user — it is the template author's message and it appears nowhere else.
4. `egg hatch apply <applyToken>` once the plan looks correct.
5. `egg hatch rollback <rollbackId>` if something needs to be undone — and `egg hatch apply <applyToken>` again if the rollback should itself be undone.
6. Once the user accepts the applied result and no undo is needed anymore, clean up with `egg hatch discard <applyToken> --force` (ask the user first — this deletes the rollback bundle). Run `egg hatch transactions` periodically to find leftovers, including `orphanedRollback` entries from older egg versions, and discard them.

Macro flags follow kebab-case derived from the macro's config name (for example a macro named `ProjectName` becomes `--project-name`).

## Human and Inline Flow (egg hatch)

```sh
egg hatch                        # interactive: prompts for template and macros
egg hatch direct MyTemplate ...  # applies inline, no preview/apply/token step
```

Two things vary independently here, and conflating them is a common mistake: **how macro values are collected** (interactive prompts when a value is missing, vs. resolved from the flags you pass) and **how changes reach disk** (staged/transactional vs. direct write). `egg hatch direct <Template> --macro value ...` with every required flag supplied is *not* interactive — it runs unattended and just skips the preview/apply token step. Interactivity is only the fallback UI for missing values, not a "human mode."

`egg hatch` with no subcommand drops straight into an interactive prompt (pick a template, answer for each macro). `egg hatch direct` accepts the same macro flags as `preview`/`apply` combined, plus:

| Flag | Description |
| --- | --- |
| `--no-staging` | Apply directly, skipping the preview/rollback staging step. |
| `--override-conflicts` | Overwrite existing files without prompting. |
| `--no-sandbox` | Disable the `sandbox-exec` guard around lifecycle scripts. |
| `--apply-changes` | Skip the confirmation prompt and apply immediately. |
| `--staging-root <dir>` | Use a different staging root (when output targets another directory). |
| `--picker <list\|text>` | Interactive template picker style. |

Prefer `egg hatch direct` only for one-shot human use where a preview/rollback pair isn't needed. Agents should default to the transaction flow above.

## Managing Templates (egg template)

| Command | What it does |
| --- | --- |
| `egg template create --name <n> --description <d> --location <global\|project>` | Scaffold a new template's `config.yml`. |
| `egg template install <git-url\|path> [--branch/--tag/--revision] [--template ...] [--global] [--force]` | Install templates from a Git repo or a local directory. |
| `egg template sync [--global\|--project] [--dry-run]` | Install everything declared in `eggs.yml` (global: `$XDG_CONFIG_HOME/egg/eggs.yml`, project: `./eggs.yml`), honoring `eggs-lock.yml` pins like `Package.resolved`. |
| `egg template update [--global\|--project] [--dry-run]` | Re-resolve `from:` ranges and `branch:` entries to the latest eligible and rewrite `eggs-lock.yml`. |
| `egg template list [--location <global\|project>] [--hide-description]` | List available templates. |
| `egg template detail <name> [--location <global\|project>]` | Show macros, types, defaults, and an example command. `--location` restricts the search to one location. |
| `egg template validate <path>` | Validate a template's `config.yml`. |
| `egg template duplicate <name> --name <new> --description <d>` | Copy a template under a new name. |
| `egg template move <name> --to <global\|project> [--force]` | Move a template between locations. |
| `egg template delete <name> [--force]` | Delete a template. |
| `egg template open <name>` | Reveal a template's directory in Finder. |

All `template` subcommands accept `--json` to emit machine-readable JSON on stdout instead of the human-readable tables and status lines — agents should always pass it rather than parsing prose. `--json` implies direct mode: every value the command needs must be supplied as a flag (e.g. `detail <name> --json`, `create --name n --description d --location project --json`).

Interactive fallbacks require a TTY. When stdin is not a TTY (agents, CI) and a command would prompt, egg fails fast with the prompt's question and the flags to pass instead of hanging — so a missing argument surfaces as an immediate error, never a stuck process.

All `template` subcommands support an interactive mode when arguments are omitted, and accept `--project-directory`/`--template-search-paths` to look beyond the current directory.

## Declaring Templates (eggs.yml)

Use this instead of `egg template install` when the user wants templates to
be *reproducible* — reinstalled the same way on another machine, pinned to a
version, or tracked in dotfiles — rather than fetched once. Trigger phrases:
"add this template repo to my setup", "pin this template to a version",
"sync my templates", "manage templates in dotfiles", "keep templates up to
date across machines".

An `eggs.yml` manifest declares template sources; `egg template sync`
resolves and installs them, recording the exact result in `eggs-lock.yml`
next to the manifest. Two independent scopes, never merged:

| Scope | Manifest path | Installs to |
| --- | --- | --- |
| Global | `$XDG_CONFIG_HOME/egg/eggs.yml` (default `~/.config/egg/eggs.yml`) | `~/.eggs/` |
| Project | `<project>/eggs.yml` | `<project>/.eggs/` |

### Writing eggs.yml

```yaml
eggs:
  - url: owner/repo                # GitHub shorthand -> https://github.com/owner/repo.git
    from: "1.0.0"                  # SwiftPM-style upToNextMajor range: highest tag in [1.0.0, 2.0.0)
    only: [SwiftCLI, SwiftLibrary] # optional; install only these template names (or use `exclude:`)
  - url: git@github.com:owner/private-templates.git
    branch: main                   # follow a branch; sync installs the locked SHA, update moves to the tip
  - url: https://github.com/owner/repo.git
    exact: "1.2.0"                 # single version, matches "1.2.0" or "v1.2.0"
  - url: https://github.com/owner/repo2.git
    revision: 6c0f1a2b9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a
  - url: ./local-templates          # local path: no version key allowed, never locked
```

Each git entry (every `url` that isn't a bare local path) takes **exactly
one** of `from:` / `exact:` / `branch:` / `revision:`. Prefer `from:` when
the user wants to track new releases automatically; use `exact:` or
`revision:` when they want a fixed pin; use `branch:` only when they
explicitly want floating/unreleased content.

### Workflow for an agent asked to add a template source

1. Ask (or infer from context) which scope: personal/dotfiles setup →
   global; this specific project → project.
2. Read or create the manifest at the scope's path above (`cat` it first —
   append to `eggs:` rather than overwriting an existing manifest).
3. Add an entry. Default to `from:` with the source repo's latest release
   tag as the lower bound unless the user asks for a branch or exact pin.
4. Run `egg template sync --global` or `--project --json` and inspect the
   result: `entries[].failed` names any source that didn't resolve or
   install, with the underlying git error.
5. Report what was installed (`entries[].installed`) and the resolved
   version (`entries[].resolvedVersion`).

To move existing pins forward, run `egg template update` instead of
hand-editing `eggs-lock.yml` — never edit the lockfile directly, it is
regenerated on every sync/update.

### `install --global` auto-registers into the manifest

`egg template install <git-url> --global` also upserts an entry for that
repo into the global `eggs.yml` (creating it if needed) and pins the result
in `eggs-lock.yml`, so a one-shot global install is picked up by future
`egg template sync --global` / `update --global` runs without any manual
manifest editing. The requirement written depends on what was passed:

| Flag | Requirement written |
| --- | --- |
| `--tag <name>`, parses as SemVer | `exact: <version>` |
| `--tag <name>`, not SemVer | `revision: <resolved-SHA>` |
| `--branch <name>` | `branch: <name>` |
| `--revision <sha>` | `revision: <sha>` |
| none (default branch) | `revision: <resolved-SHA>` |

Re-running `install --global` against an already-declared URL replaces that
entry's requirement rather than duplicating it, and preserves the existing
`only:`/`exclude:` filter unless the new install passed `--template`/
`--exclude` explicitly. `--project` and local-path installs never touch any
manifest. If registration fails after templates already installed (e.g. a
permission error), the install still succeeds — a warning is printed instead
of failing the command.

Full reference (field table, `from:` semantics, lock format,
troubleshooting): `egg template sync --help` / `egg template
update --help`, or egg's published API documentation.

## MCP Integration

`egg mcp` starts a Model Context Protocol server that mirrors the CLI transaction flow (`egg_template_detail`, `egg_hatch_preview`, `egg_hatch_apply`, `egg_hatch_rollback`, `egg_hatch_discard`, `egg_hatch_transactions`). Manifest workflows are available as `egg_template_sync` and `egg_template_update` (arguments: `scope`, `dry_run`, `project_directory`), returning the same JSON as the CLI's `--json` flag. There is no one-shot hatch tool over MCP — every hatch goes through `egg_hatch_preview` then `egg_hatch_apply`, so a caller always inspects the change set before anything is written. `egg_hatch_discard` takes a `force` boolean that is required when discarding an `applied` transaction — ask the user before setting it, since it deletes the rollback bundle and the apply can no longer be undone. Macro keys over MCP must use the exact config names (e.g. `___MODULE_NAME___`), not the kebab-case CLI flags. To disable sandboxing for `egg_hatch_preview`, first ask the user whether to run lifecycle scripts without sandbox protection. Do not classify script contents yourself; after explicit user approval, pass both `disable_sandbox: true` and `user_confirmed_no_sandbox: true`. When a template declares `sandbox.allowed_paths` and `egg_hatch_preview` fails with `SANDBOX EXTENDED WRITE ACCESS REQUIRED`, show the listed paths to the user, ask for approval, and retry with `allowed_write_paths` containing only the approved paths — never approve paths yourself.

## Troubleshooting

### "Template not found"
1. Check the template exists: `egg template list`.
2. Verify the location: `~/.eggs/` (global) or `./.eggs/` (project-local).
3. Use `--template-search-paths` for custom locations.

### "Macro X is required"
Run `egg template detail <name>` to see every required macro, then pass each as `--macro-name value` on `preview` or `direct`.

### `apply` fails with a drift error
The working directory changed since `preview` was run. Re-run `preview` to get a fresh `applyToken`, or pass `--force` to `apply` if the drift is expected.

### `apply` fails with "cannot be applied because its status is 'applied'"
The transaction is already applied. To redo it, roll it back first (`egg hatch rollback <token>`), then apply again. Only `preview` and `rolledBack` transactions can be applied.

### `discard` refuses with "deletes its rollback bundle"
The transaction is `applied`, so discarding removes the only way to undo it. To undo the changes instead, run `egg hatch rollback <token>` first. To delete the records and keep the applied files, ask the user, then re-run with `--force`.

### Lifecycle script errors
- Check script permissions.
- `SANDBOX EXTENDED WRITE ACCESS REQUIRED`: the template declares external write paths. Ask the user, then retry with `--allow-write <path>` for each approved path.
- Use `--no-sandbox` if the sandbox blocks a legitimate operation no declared path covers.
- Review the script's stdout/stderr in the response for details.
