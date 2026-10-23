---
name: init
description: Initializes project AI-agent docs and workspace conventions. Use when
  generating agent rules docs, adding GitHub templates, or bootstrapping project rules.
---

# opencode Workspace Initialization

Profiles the project, authors the canonical tool-neutral `AGENTS.md` rules file (with a compatibility `@AGENTS.md`-importing `CLAUDE.md` shim and optional Claude-only notes), and optionally emits GitHub issue templates and git convention files — all flag-driven, non-destructive by default.

## Current Project Context

- **Profile detection** (complete `key=value` output, `project_root` first): !`~/.config/opencode/skills/init/scripts/profile-project.sh`

Context injection is deliberately one scoped helper call: no `pwd`, `ls | head`, `2>/dev/null`, or other shell pipeline/redirect. Some hosts reject compound pipelines as a whole even when each segment is allowed, and `head` truncated the profile (dropping keys such as `has_releasing_md`). Do not widen `allowed-tools` with `find`, `head`, `wc`, or `pwd`.

### Headless / permissions

- `allowed-tools` grants only the scoped `scripts/*.sh` helpers plus a few simple read/copy commands. Compound shell pipelines (`a | b`, `a && b`, redirection tricks) are **host-permission behavior**: this skill does not control them, and a caller allowlist that permits each segment may still reject the whole pipeline. Never rely on them.
- Every step below has a pipeline-free supported path: `profile-project.sh` (full profile), `count-source-files.sh` (capped count), `render-template.sh`, `migrate-rules.sh`, `rules-report.sh`. Run each as one command.
- All helpers require Python 3.11+ and fail up front with a readable message (no partial output) on an older `python3`.

## Arguments

| Flag                        | Meaning                                                                                       | Example                                     |
| --------------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------- |
| `--dry-run`                 | Preview every planned file; make no writes                                                    | `/init --dry-run`                       |
| `--docs-only`               | Skip MCP/agent selection; emit the rules files only                                           | `/init --docs-only`                     |
| `--templates`               | Also emit `.github/` issue forms, PR template, labels                                         | `/init --templates`                     |
| `--git`                     | Also emit `.gitignore`, `.gitmessage`, commitlint (JS/TS), and the lefthook bundle            | `/init --git`                           |
| `--vendor-neutral`          | Also emit `.ai/rules/project.md` pointer to `AGENTS.md`                                       | `/init --vendor-neutral`                |
| `--formatters`              | Also bootstrap lint/format via `formatters` (scripts, configs, aliases, docs)             | `/init --formatters`                    |
| `--release-model[=<model>]` | Run `release-model` without asking when `RELEASING.md` is missing                         | `/init --release-model=trunk-only`      |
| `--no-release-model`        | Never offer `release-model`                                                               | `/init --no-release-model`              |
| `--migrate-rules`           | Move an existing long `CLAUDE.md` into `AGENTS.md` (dry-run diff first)                       | `/init --migrate-rules`                 |
| `--allow-non-git`           | With `--migrate-rules`: permit non-git or git-ignored rules files (timestamped backups first) | `/init --migrate-rules --allow-non-git` |
| `--no-claude-md`            | Skip the `@AGENTS.md` `CLAUDE.md` shim (needs Claude Code 2.1.277+)                           | `/init --no-claude-md`                  |
| `--update`                  | Structured refresh of existing artifacts (merge/migrate, never clobber)                       | `/init --update`                        |
| `--force`                   | Overwrite existing files without prompting                                                    | `/init --force`                         |
| `--profile=<lang>`          | Override detected language (`rust`, `ts-node`, `python`, `go`, `mixed`, `empty`)              | `/init --profile=rust`                  |

Flags are composable. See `references/flag-reference.md` for the full matrix.

**Questions:** headless (no question tool or chat turn) defaults: class `clarify` (empty or unknown profile): print the questions and stop; class `confirm-destructive` (profile confirmation, conflicts, rules migration): behave as `--dry-run`, skip existing files, print diffs and the rerun, then stop. The release-model offer is skipped unless `--release-model` is passed. See `~/.config/opencode/shared/references/question-policy.md`.

## Task

Execute the following phases in order. Phases are short — do not add narrative prose between steps.

### Phase 0 — Parse flags

Extract mode booleans from `$ARGUMENTS`:

- `DRY_RUN` — true if `--dry-run` present
- `DOCS_ONLY` — true if `--docs-only` present
- `TEMPLATES` — true if `--templates` present
- `GIT` — true if `--git` present
- `VENDOR_NEUTRAL` — true if `--vendor-neutral` present
- `FORMATTERS` — true if `--formatters` present
- `RELEASE_MODEL` — true if `--release-model` or `--release-model=<model>` present
- `RELEASE_MODEL_VALUE` — `<model>` from `--release-model=<model>`, else empty. Must be `trunk-only` or `release-branches`; any other value is an error before any phase runs.
- `NO_RELEASE_MODEL` — true if `--no-release-model` present. Combining it with `--release-model` is an error before any phase runs.
- `ALLOW_NON_GIT` — true if `--allow-non-git` present (only meaningful with `--migrate-rules`).
- `NO_CLAUDE_MD` — true if `--no-claude-md` present.
- `MIGRATE_RULES` — true if `--migrate-rules` present. Runs only the rules migration (Phase 5.7); combine with `--dry-run` for the preview without a prompt.
- `UPDATE` — true if `--update` present
- `FORCE` — true if `--force` present
- `PROFILE` — value of `--profile=<lang>` if provided, else empty

Defaults: all booleans off; no profile override. `--update` and `--force` are mutually reinforcing: `--update` controls merge/migrate behavior, `--force` controls conflict resolution. Without either, existing files are preserved with a diff-and-ask prompt.

### Phase 1 — Profile

1. Run `~/.config/opencode/skills/init/scripts/profile-project.sh` once, with no pipeline, `head`, or `2>/dev/null`, and parse the complete `key=value` output into variables (the Current Project Context above already holds the same output; re-run only after it changes). See `references/project-profile-heuristics.md` for the key list.
2. If `PROFILE` flag is set, override `primary_language` with that value.
3. If `is_empty=true` OR `primary_language=unknown`: ask the user conversationally for project name, purpose, and primary language. Set `project_name`, `project_purpose`, and `primary_language` from their answers.
4. If `UPDATE=false` AND at least two of `has_claude_md`, `has_agents_md`, `has_cursor_rules`, `has_issue_templates`, `has_gitmessage`, `has_gitignore` are true: warn the user "Existing doc/workflow files detected — consider re-running with `--update` for structured refresh, or `--force` to overwrite. Continuing with default skip-on-conflict behavior."
5. Surface the resolved profile summary to the user and wait for confirmation before writing anything — except when `DRY_RUN=true`, which proceeds directly to preview.

If `MIGRATE_RULES=true`, jump directly to Phase 5.7 after profiling; skip all other rendering, release-model, and formatter phases. Migration ignores `--force`.

### Phase 2 — Optional deep analysis

Skip this phase when `DOCS_ONLY=true`.

Otherwise, estimate source file count with the single scoped helper (no pipeline; walk errors stay visible, output is capped at 51 files):

```bash
~/.config/opencode/skills/init/scripts/count-source-files.sh --repo .
```

It prints `count=<n>`, `capped=true|false`, `cap=50`. If `capped=true` (i.e., >50 files), dispatch `@codebase-research-analyst` with a prompt requesting:

- Key architectural patterns and conventions to encode in `AGENTS.md`
- Critical commands (test, lint, build, deploy) to embed
- Project-specific MUST/MUST NOT rules worth adding

Feed the agent's output into the `AGENTS.md` rendering in Phase 3 (conventions and commands only; keep the file well under 100 lines).

### Phase 3 — Render templates

Load each applicable `.tmpl` file from `~/.config/opencode/skills/init/templates/`. Substitute all `{{PLACEHOLDER}}` variables using profile values from Phase 1 (and Phase 2 if run). For language-conditional blocks (`{{#IF_RUST}}...{{/IF_RUST}}` etc.), include only the block matching `primary_language`. Leave `{{#IF_RELEASE_MODEL}}...{{/IF_RELEASE_MODEL}}` blocks (in `AGENTS.md.tmpl` and `github/labels.md.tmpl`) unresolved — Phase 5 (dry run) or Phase 5.5 resolves them. Render all files in memory — do NOT write yet. `scripts/render-template.sh --template <bundled-template> [--profile -]` (profile on stdin; needs Bash 3.2+ and Python 3) renders a template without writing (a thin wrapper over `scripts/render-template.py`). It only reads templates under the skill's own `templates/` directory. A command that `profile-project.sh` reports as `unknown` renders as `# not detected` inside fenced shell blocks, and any template that would put it into YAML (`run:`) or a checklist guards it with `IF_*_CMD` / `IF_NO_*_CMD` blocks instead (lefthook `pre-push` is omitted, with a comment, when no test command is detected). If `profile-project.sh` warns that `jq` is missing, say so in the Phase 1 summary: JS/TS commands could not be detected and will render as `# not detected`. Mixed-language profiles keep the language blocks of every component language in `secondary_languages`.

Rendering map:

| Condition                                                      | Source template                              | Target path                                  |
| -------------------------------------------------------------- | -------------------------------------------- | -------------------------------------------- |
| Always                                                         | `AGENTS.md.tmpl`                             | `AGENTS.md` (canonical, ≤80 template lines)  |
| Unless `NO_CLAUDE_MD=true` (see below)                         | `CLAUDE.md.tmpl`                             | `CLAUDE.md` (`@AGENTS.md` + short section)   |
| Path-scoped rules exist (see below)                            | `cursor-rule.mdc.tmpl`                       | `.cursor/rules/<scope>.mdc`                  |
| `VENDOR_NEUTRAL=true`                                          | `ai-rule.md.tmpl`                            | `.ai/rules/project.md` (pointer)             |
| `TEMPLATES=true`                                               | `github/bug_report.yml.tmpl`                 | `.github/ISSUE_TEMPLATE/bug_report.yml`      |
| `TEMPLATES=true`                                               | `github/feature_request.yml.tmpl`            | `.github/ISSUE_TEMPLATE/feature_request.yml` |
| `TEMPLATES=true`                                               | `github/docs_request.yml.tmpl`               | `.github/ISSUE_TEMPLATE/docs_request.yml`    |
| `TEMPLATES=true`                                               | `github/config.yml.tmpl`                     | `.github/ISSUE_TEMPLATE/config.yml`          |
| `TEMPLATES=true`                                               | `github/pull_request_template.md.tmpl`       | `.github/pull_request_template.md`           |
| `TEMPLATES=true`                                               | `github/labels.md.tmpl`                      | `.github/labels.md`                          |
| `TEMPLATES=true`                                               | `github/copilot-instructions.md.tmpl`        | `.github/copilot-instructions.md`            |
| `TEMPLATES=true`                                               | `github/workflows/pr-title.yml.tmpl`         | `.github/workflows/pr-title.yml`             |
| `TEMPLATES=true`                                               | `github/workflows/pr-title-autofix.yml.tmpl` | `.github/workflows/pr-title-autofix.yml`     |
| `GIT=true`                                                     | `git/gitignore.tmpl`                         | `.gitignore`                                 |
| `GIT=true`                                                     | `git/gitmessage.tmpl`                        | `.gitmessage`                                |
| `GIT=true`                                                     | `git/lefthook.yml.tmpl`                      | `lefthook.yml`                               |
| `GIT=true`                                                     | `git/install-lefthook.sh.tmpl`               | `scripts/install-lefthook.sh`                |
| `GIT=true`                                                     | `git/lefthook-usage.md.tmpl`                 | `docs/lefthook-usage.md`                     |
| `GIT=true` AND `primary_language` in `{typescript,javascript}` | `git/commitlint.config.cjs.tmpl`             | `commitlint.config.cjs`                      |

**Rules-file shape**: `AGENTS.md` is the single canonical rules file (detected commands, project conventions, MUST / MUST NOT, a one-line Conventional Commits rule, links) — no commit-types table, no stack table, no generic SHOULDs. `CLAUDE.md` is always rendered as the `@AGENTS.md` shim (plus a short `## Claude-only notes` section, ≤15 lines total, when Phase 2 or the user supplied Claude-specific content), because Claude Code reads `CLAUDE.md`, not `AGENTS.md`, in versions before 2.1.277; newer versions fall back to `AGENTS.md` when no `CLAUDE.md` exists, so omitting the shim is version-dependent. Skip the shim only with `--no-claude-md` or an explicit user choice, and then state the 2.1.277+ requirement in the Phase 7 report. Emit `.cursor/rules/*.mdc` only for path-scoped rules (`alwaysApply: false`, real `globs`); recent Cursor versions read a root `AGENTS.md` when available (verify for your version), so never emit an always-apply copy of the project rules; offer `--vendor-neutral` or a path-scoped rule if the user's Cursor does not. `copilot-instructions.md` points at `AGENTS.md` but does not rely on Copilot following the link: it also carries the detected commands and three repo-neutral essentials (no secrets, Conventional Commits, issue link).

**Language-block selection**: for every template except `gitignore.tmpl`, include only the block matching `primary_language`. For `gitignore.tmpl`, include every block whose language appears in `primary_language` or `secondary_languages` (comma-separated) so mixed-stack repos get every applicable section. For `gitignore.tmpl`, `javascript` is treated as `typescript` for `{{#IF_TS}}` activation; `terraform` activates `{{#IF_TERRAFORM}}`.

Fill `PROJECT_CONVENTIONS` with verified project-specific architecture/naming constraints from existing docs, Phase 2, or the user; if none are known, use "No additional project-specific conventions detected." Never stamp generic language conventions or assumed tools. Use `--keep IF_CLAUDE_ONLY --set CLAUDE_ONLY_NOTES=...` for the optional Claude-only notes.

See `references/template-library.md` for placeholder definitions.

### Phase 4 — MCP/agent selection

Skip this phase when `DOCS_ONLY=true`.

Run the catalog generators:

```bash
~/.config/opencode/skills/init/scripts/generate-mcp-catalog.sh
~/.config/opencode/skills/init/scripts/generate-agent-catalog.sh
```

Present all available options as checkboxes organized by category. Pre-check items that align with the detected profile (language, infrastructure, workflow). Let the user freely adjust the selection before proceeding.

### Phase 5 — Dry-run check

If `DRY_RUN=true`:

- Print a listing of every planned file with a preview snippet (first ~15 lines each). Resolve `IF_RELEASE_MODEL` blocks as kept when `has_releasing_md=true` or `RELEASE_MODEL=true`, else drop them.
- Print planned rules-file line counts (see Phase 7) so oversize output is visible before any write.
- Show the planned `.mcp.json` content.
- List agent files that would be copied.
- Print the release-model step Phase 5.5 would take: "skip (RELEASING.md exists)", "skip (--no-release-model)", "would run `release-model` [--model <value> --yes]", or "would offer `release-model`".
- STOP — make no writes.

### Phase 5.5 — Release model

Decide whether to create `RELEASING.md` (the project's branching and release rules — see `~/.config/opencode/shared/references/branching-model.md`), then resolve the `IF_RELEASE_MODEL` blocks.

1. **Choose the action** (first match wins):
   - `has_releasing_md=true` → skip. The project already has a release model; init reads only its presence (`/release-model --audit` validates it).
   - `NO_RELEASE_MODEL=true` → skip.
   - `RELEASE_MODEL=true` → run without asking.
   - `DOCS_ONLY=true` (and no `--release-model`) → skip; `--docs-only` stays limited to the rules files.
   - Otherwise → ask: "This project has no `RELEASING.md`. Run `release-model` to choose a branching and release model (trunk-only or release branches) and write one?" Default: yes. A missing `RELEASING.md` never blocks init — "no" continues normally.
2. **Run** the `release-model` skill when chosen. With `RELEASE_MODEL_VALUE` set, pass `--model <value> --yes`: the model was decided upstream (for example by `blueprint`), so the proposal is accepted without questions. Otherwise run it without arguments so it can propose a model from the repo's signals and confirm with the user.
3. **Resolve** every `IF_RELEASE_MODEL` block rendered in Phase 3: keep the block contents when `RELEASING.md` now exists at the project root, else drop the block. This covers "exists already" and "created in this run", and drops the pointer if `release-model` was declined or failed.
4. If `release-model` errors, record the failure for the Phase 7 summary and continue — do not abort init.

### Phase 5.7 — Rules migration (when `MIGRATE_RULES=true`)

Runs instead of Phases 2–6.5 (profile only), for repos that already have a long `CLAUDE.md`. Never silently rewrites it.

1. Run `~/.config/opencode/skills/init/scripts/migrate-rules.sh --repo . --dry-run` (a Bash 3.2 entrypoint for `scripts/migrate-rules.py`, which shares the `@AGENTS.md` import parser in `_shared/scripts/rules_pointer.py` (via `scripts/rules_file_lib.py`) with release-model's `pointer-targets.sh`) and show the full output: the move diff for `AGENTS.md` and `CLAUDE.md`, new line counts, and the **content-loss list** (the full text of any replaced legacy pointer `AGENTS.md`, sections skipped as duplicates, and merge conflicts). Nothing is written.
2. With `DRY_RUN=true`, stop here.
3. Otherwise ask once: "Apply this migration?" The script refuses outside the git root, over uncommitted changes, or for git-ignored/symlinked rules files; `--allow-non-git` is the explicit opt-in for those cases. Every apply first copies both files to a timestamped backup directory (printed in the output) and writes via temp file + atomic rename, restoring from the backup if the pair cannot be completed. Routing is heading-based and shown per section: only exact Claude runtime headings stay in `CLAUDE.md`; everything else moves to `AGENTS.md`, and headings that merely mention Claude are routed to `AGENTS.md` and listed as ambiguous for review. On yes, run the same command with `--yes` instead of `--dry-run`. On no, stop; nothing changed.
4. Content moves to `AGENTS.md`; only exact Claude runtime headings remain after `@AGENTS.md`. Nothing is deleted (a replaced legacy pointer's full text is printed), ambiguous headings are reported, and no duplicate H1/headings are created. Report the new line counts per Phase 7.

### Phase 6 — Apply

For each rendered file from Phase 3, apply the resolution rule below. Never silently clobber user content.

**Target does not exist** → write the rendered file.

**Existing rules safeguard (before all resolution rules)** → never rewrite an existing non-importing `CLAUDE.md` or a legacy pointer `AGENTS.md`, even with `--force`; offer `--migrate-rules`. Skip rendering new rules files that would conflict with that existing canonical layout.

**Target exists AND `FORCE=true`** → overwrite other artifacts and log the path.

**Target exists AND `UPDATE=true`** → structured refresh per artifact type:

| Artifact                                                  | Update behavior                                                                                                                                                                                           |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AGENTS.md` (canonical or custom)                         | Parse existing `##`-level headings. Append only the template sections that are missing; preserve existing content verbatim. Report the appended section list.                                             |
| `AGENTS.md` (legacy pointer, `agents_md_is_pointer=true`) | Offer `--migrate-rules` (the pointer names `CLAUDE.md`, so the real rules are there). Without it, leave the file untouched.                                                                               |
| `CLAUDE.md` (already `@AGENTS.md`)                        | Leave untouched.                                                                                                                                                                                          |
| `CLAUDE.md` (long, no `@AGENTS.md`)                       | Never rewrite. Print the line count and offer `--migrate-rules` (dry-run diff first). Without it, leave the file and `AGENTS.md` as they are.                                                             |
| `.cursor/rules/<scope>.mdc`                               | Overwrite body content; preserve any non-standard frontmatter keys the user added beyond `description`, `globs`, `alwaysApply`.                                                                           |
| `.cursor/rules/project.mdc` (legacy always-apply copy)    | Leave as is; advise removing it once `AGENTS.md` is canonical (Cursor reads `AGENTS.md` when available; verify your version).                                                                             |
| `.cursorrules` (legacy, `has_legacy_cursorrules=true`)    | Offer `--migrate-rules`-style review: show its content, fold project-specific lines into `AGENTS.md`, and advise deleting `.cursorrules` (do not delete automatically).                                   |
| `.ai/rules/project.md`                                    | Overwrite the pointer body.                                                                                                                                                                               |
| `.github/ISSUE_TEMPLATE/*.yml`                            | Per template: if missing → create; if present → show diff and default to skip (issue forms are often customized). `--update --force` overwrites.                                                          |
| `.github/pull_request_template.md`                        | Show diff; default skip. `--update --force` overwrites.                                                                                                                                                   |
| `.github/labels.md`                                       | Always overwrite (reference doc, safe to refresh).                                                                                                                                                        |
| `.github/copilot-instructions.md`                         | Show diff; default skip (users customise agent-facing rules). `--update --force` overwrites.                                                                                                              |
| `.github/workflows/pr-title.yml`                          | Show diff; default skip (users may customise the Conventional Commits type list or branch filters). `--update --force` overwrites.                                                                        |
| `.github/workflows/pr-title-autofix.yml`                  | Show diff; default skip (users may tune the placeholder regex, the type-normalization pass, or the draft-toggle behaviour). `--update --force` overwrites.                                                |
| `.gitignore`                                              | Show diff; default skip (users curate this file heavily). `--update --force` overwrites. When `has_gitignore=true` at Phase 1, warn the user the file already exists.                                     |
| `.gitmessage`                                             | Show diff; default skip. `--update --force` overwrites (usually safe — it is a reference template).                                                                                                       |
| `commitlint.config.cjs`                                   | If present → show diff and default skip with a warning ("commitlint rules are often project-customized"). `--update --force` overwrites.                                                                  |
| `lefthook.yml`                                            | Show diff; default skip (users often extend the config with project-specific commands). `--update --force` overwrites. When `has_lefthook_config=true` at Phase 1, warn the user the file already exists. |
| `scripts/install-lefthook.sh`                             | Always overwrite (managed bootstrap tooling; tracks upstream improvements).                                                                                                                               |
| `docs/lefthook-usage.md`                                  | Always overwrite (managed reference doc).                                                                                                                                                                 |

**Target exists AND `UPDATE=false` AND `FORCE=false`** → show a unified diff, then prompt the user with three choices: overwrite, merge (only meaningful for `AGENTS.md`), or skip. Default choice: skip.

Then apply MCP/agent selections from Phase 4 (skipped when `DOCS_ONLY=true`):

```bash
${HOME}/.config/opencode/mcp-library/generate-mcp-config.sh <selected-mcps>
```

Create `.claude/agents/` if needed; copy selected agent files from `${HOME}/.config/opencode/agents/`.

### Phase 6.5 — Formatter bootstrap (when `FORMATTERS=true`)

When `FORMATTERS=true`, invoke the `formatters` skill to bootstrap the lint/format environment. Pass through `--dry-run` and `--force`; let the skill handle its own flag defaults for everything else (stack detection, sync vs copy, aliases, docs). Do NOT duplicate formatter logic here — the formatters skill owns every decision about scripts, tool configs, aliases, and docs.

If `DRY_RUN=true`, invoke `formatters --dry-run` and merge its preview output into the Phase 7 summary. Otherwise invoke `formatters` normally.

If the formatters skill exits with an error, record the failure in the Phase 7 summary and continue — do not let a formatter error abort the overall init run.

### Phase 7 — Summary report

Produce a summary using `~/.config/opencode/skills/init/templates/workspace-report.md` as the base. Extend it with these sections appended after the existing MCP/agents tables:

**Docs emitted** — list each path written, or "skipped: user chose keep". State explicitly when the user opted out of the CLAUDE.md shim (requires Claude Code 2.1.277+ for native AGENTS.md fallback).

**Rules files** — one line per rules file that exists after the run (`AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, `.cursor/rules/*.mdc`) with its line count, e.g. `AGENTS.md: 31 lines`. Mark any file over 200 lines `⚠ over 200 lines — long rules files lose adherence; trim or run --migrate-rules`. Run `~/.config/opencode/skills/init/scripts/rules-report.sh` to produce these lines; do not estimate.

**GitHub templates emitted** — list each `.github/` path written (omit section if `TEMPLATES=false`).

**Git conventions emitted** — list each git artifact path written (omit section if `GIT=false`).

**Release model** — the Phase 5.5 outcome: `RELEASING.md` created (with the chosen model), already present, skipped (and why), declined, or failed (with the error).

**Next steps** — suggest:

- `git config commit.template .gitmessage` (if `GIT=true`)
- Review the generated `.gitignore` — confirm language sections match the stack and add project-specific entries (secrets files, generated assets, local scratch dirs). Rust libraries should un-comment the `Cargo.lock` ignore line (if `GIT=true`).
- `bash scripts/install-lefthook.sh` to install the `lefthook` binary and activate the hooks defined in `lefthook.yml` (if `GIT=true`). Re-runnable on every checkout; safe to rerun.
- For JS/TS projects: run `{{PACKAGE_MANAGER}} install` (devDependencies `@commitlint/cli` + `@commitlint/config-conventional` must be installed for the `commit-msg` hook to work).
- Review `.github/labels.md` and run the `gh label create` commands listed there (if `TEMPLATES=true`). Under the release-branches model, create one `backport:X.Y` label per maintenance branch.
- Review `RELEASING.md` and commit it with the rest of the init output (if Phase 5.5 created it). If the offer was declined, `/release-model` can create it later.
- Review `.github/copilot-instructions.md` — it is a short pointer to `AGENTS.md` plus the detected commands; keep it that way (if `TEMPLATES=true`).
- Enable the PR title check as a required status: **Settings → Branches → Branch protection rules**, add `Validate Conventional Commit PR title` (the job name from `.github/workflows/pr-title.yml`) to the required checks. Without this, the workflow runs but isn't enforced (if `TEMPLATES=true`).
- `.github/workflows/pr-title-autofix.yml` runs alongside the validator and (1) strips placeholder prefixes (`[WIP]`, `Draft:`, `Initial plan`) from PR titles server-side, then (2) normalizes a leading Conventional Commit type that was written without a colon or with capitalization (e.g. `Refactor X` → `refactor: X`, `Feat(auth): X` → `feat(auth): X`). Runs because GitHub Copilot's coding-agent token often lacks `pull_requests:write` and cannot self-correct. Do **not** add this workflow to required checks — it is an auto-correcting side effect, not a gate (if `TEMPLATES=true`).
- Open `AGENTS.md` to review and refine the generated project rules (it is the canonical file; add only what is specific to this project).
- If `has_legacy_cursorrules=true`: fold any project-specific lines of `.cursorrules` into `AGENTS.md`, then delete it (init never deletes it).

## Important Notes

- Default behavior never destroys existing files; always diff-and-ask before overwriting.
- `--update` enables structured merge/migrate semantics and is the recommended flag when re-running `init` in a project that already has docs/templates.
- `--force` is opt-in and always logs every path it overwrote. `--update --force` applies merge semantics but overwrites on conflict instead of skipping.
- No new agents are registered. `codebase-research-analyst` is called only once, conditionally, for large existing repos (>50 source files) when `--docs-only` is not set.
- The MCP and agent selection flow is preserved unchanged behind `--docs-only`.
- A missing `RELEASING.md` never blocks init. Phase 5.5 only offers `release-model`; `--release-model` runs it and `--no-release-model` silences the offer.
- For the full flag matrix with composability examples, see `references/flag-reference.md`.
- Read `references/conventional-commits.md` only when the user asks for the full commit-type reference; the generated `AGENTS.md` carries a one-line rule, not the types table. Read `references/label-taxonomy.md` when rendering
  `.github/labels.md` (`--templates`).
