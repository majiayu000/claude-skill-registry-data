---
name: power-init
description: Use when a repository has no PWDEV Power workspace yet, when resuming one, when the codebase map needs refreshing, or when the setup should be checked
---

# Initialize a Power Workspace

Never read a secret, and never edit configuration outside the repository — print the command and
let the human run it. Read [artifacts](../../references/artifacts.md) before writing `config.json`
or `state.md` (Step 4), [context](../../references/context.md) before mapping (Step 5),
[runtime](../../references/runtime.md) before dispatching the mapper, and
[safety](../../references/safety.md) before touching `.gitignore` or anything outside
`.planning/power/`.

## Routes

| Route | Meaning |
|---|---|
| no argument | initialize, or report and resume if already initialized |
| `--map` | re-map the codebase; do not touch configuration |
| `--check` | report the runtime surface and map staleness only; write nothing |

## Step 1 — Detect before you ask

Never ask the human something the repository already answers.

1. Is `.planning/power/config.json` present? If yes, this is a resume: read it, read `state.md`,
   report the active feature and the exact next valid action. Do not re-initialize and do not
   overwrite an existing config. Offer `--map` if the map is stale (Step 5).
2. Is this a Git repository with a named branch? If not, say so and stop — every later phase binds
   to a branch.
3. Greenfield or brownfield? Brownfield is anything with source files already committed.
4. Detect the stack from manifests, not from folder names: `package.json`, `pyproject.toml`,
   `go.mod`, `Cargo.toml`, `composer.json`, `pom.xml`, `Gemfile`. Read the actual test and lint
   commands out of them.

## Step 2 — Runtime surface

Report what is available, one line each. Do not install anything, and do not edit any
configuration outside the repository.

| Check | Command | If missing |
|---|---|---|
| Runtime | your own tool surface | — |
| cmux binary and socket | source `../../scripts/cmux-common.sh` and call `power_cmux_require` | fleet is unavailable; everything else works |
| Hermes CLI | `hermes --version` | the Kanban bridge is unavailable |
| cmux↔Hermes hooks | `cmux hooks hermes-agent` | print `cmux hooks hermes-agent install` and let the human run it |
| `jq`, `sqlite3` | `command -v` | audit stays off; note it |

Missing tools are facts to report, not errors to fix. Only the fleet requires cmux.

**Do not probe for cmux with `command -v cmux`.** On macOS the CLI lives inside the app bundle
and is usually not on `PATH`, so that check reports "not installed" for a cmux that is running
fine. `power_cmux_require` resolves the binary the same way the fleet does, and it distinguishes
"not running" from "running but refusing this process".

## Step 3 — Ask what cannot be detected

At most one round, at most three questions, one at a time:

1. Language for conversation and artifacts (default: the repository's existing language).
2. Model profile: `economy`, `balanced`, `performance` (default: `balanced`).
3. Audit trail on? (default: off).

## Step 4 — Write the workspace

Create `.planning/power/` with `config.json` and `state.md` exactly as
[artifacts](../../references/artifacts.md) specifies. If audit was enabled, create the database
file — the audit scripts refuse to write into a database that does not exist, so creating it is
the act that turns auditing on.

Add these to the repository's `.gitignore` if one exists — none of them is a contract:

- `.planning/power/audit/` and `.planning/power/fleet-logs/` — logs
- `.planning/power/fleet-results/` — raw provider bytes
- `.planning/power/features/*/review-*.diff` — review packages
- `.planning/power/fleet/` and `.planning/power/fleet-status.json` — live fleet state, which
  records absolute worktree paths, a cmux workspace id and host ports, and is therefore true for
  exactly one machine

Everything else under `.planning/power/` is a contract and belongs in version control.

**Check whether `.planning` is already ignored wholesale**, which is a common default. If it is,
carve `.planning/power/` back out:

```gitignore
.planning/*
!.planning/power/
.planning/power/audit/
.planning/power/fleet/
.planning/power/fleet-status.json
.planning/power/fleet-logs/
.planning/power/fleet-results/
.planning/power/features/*/review-*.diff
```

An ignored contract directory is not a cosmetic problem: the fleet decides whether a stage did
any work by asking git whether the feature directory is dirty, and git never says that of an
ignored path. Left alone, the plan stage — whose only output is `plan.md` — is refused as work
nobody did, and `fleet-up` now declines to launch rather than let that happen mid-run.

## Step 5 — Map the codebase

**Greenfield repositories skip this.** There is nothing to observe yet, and a map of an empty
directory is noise that later phases will read as fact. Say you skipped it and why.

For brownfield, dispatch the packaged `mapper` subagent — see [runtime](../../references/runtime.md)
for how, in your runtime. Give it the repository root, the language, and the output contract. It
writes four files and returns at most ten lines; do not paste its files into your context.

Where no subagent mechanism exists, map inline, and keep it to exactly what the four documents
need rather than exploring for its own sake.

**Produces:** `.planning/power/context/{project,stack,domain,pitfalls}.md`

### Staleness

`project.md` records the commit it was mapped at. On resume, compare it to `HEAD`: same commit,
or only `.planning/` changed, means current; a changed stack, manifest, or top-level directory
means stale — say so and offer `--map`. Never remap silently, and when the map and the code
disagree, the code is right ([context](../../references/context.md) §Staleness).

## Step 6 — Governance file, only if asked

Offer to generate the governance file your runtime reads — the instructions file named in your
runtime's tool mapping — from `templates/CLAUDE.template.md`, filled with what the map found. If
one already exists, show what you would change and ask before touching it. Never silently
overwrite a governance file.

The file is named indirectly here on purpose: Hermes drops any skill whose body contains those
two filenames literally, silently and without an error, so naming them would make this whole
skill invisible on that runtime. See the note in [runtime](../../references/runtime.md).

## Report

State the workspace path, the detected stack with its real test and lint commands, the runtime
surface with anything missing, whether the map was written, skipped or refreshed, and the next
action: `product` for a new product, `plan` for a feature, `quick` for a small change.
