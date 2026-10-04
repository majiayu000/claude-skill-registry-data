---
model_tier: medium
name: script-writing
description: "Use when adding or editing any script under `scripts/` — `--quiet`, `_lib/script_output`, silent Taskfile wiring, Iron-Law carve-outs; fires on 'add a check script for X'."
domain: process
workspaces:
  - agent-config-maintainer
packs:
  - meta
---

<!-- cloud_safe: degrade -->

# script-writing

## When to use

* Creating a new TypeScript script in `src/scripts/{name}.ts` (linters, checks, generators, measure tools — run via `./scripts-run src/scripts/{name}`)
* Editing an existing script that prints progress or success lines
* Wiring a script into `Taskfile.yml` or `taskfiles/*.yml`
* Reviewing a PR that adds scripts and asking "why does this still print on minimal?"

Do NOT use this skill when:

* The content is a one-off / archival under `scripts/ai_council/one_off_archive/` — those carry an `_one_off_` prefix and are exempt from the verbosity convention
* The content is a shell entrypoint with secret prompts (install-keys, release confirms) → see § 3 Iron-Law carve-outs
* The content is a `.mjs` / Node script under `scripts/cost/` — different runtime; convention covered in `agents/settings/contexts/cost-tracking.md`

## Script vs other writers — critical test

| Intent | Artifact |
|---|---|
| "Maintenance script the agent or CI runs" | **This skill** |
| "User types `/foo` to invoke" | `command-writing` |
| "Constraint the agent must always honor" | `rule-writing` |
| "Reference knowledge agents cite" | `guideline-writing` |

Scripts orchestrate file checks, generators, and validators. They are
neither user-invoked nor agent-routed — `task` and CI call them.

## Procedure

### 0. Run the Drafting Protocol

Creating or materially rewriting a script that joins the linter / check
family **must** go through Understand → Research → Draft from the
[`artifact-drafting-protocol`](../../rules/artifact-drafting-protocol.md) rule.

* **Understand** — what failure does this script catch that no existing
  check catches? Is it a one-off (then archive it) or evergreen?
* **Research** — `ls src/scripts/check_*.ts src/scripts/lint_*.ts`, grep for
  overlap, skim 1–2 peer scripts (e.g. `lint_handoffs.ts`,
  `check_md_language.ts`).
* **Draft** — propose name + one-line purpose first. Only fill the body
  after the shape is confirmed.

### 1. `--quiet` flag — argv check

Every `check_*.ts` / `lint_*.ts` script MUST accept `--quiet` so the
silent Taskfile layer (§ 4) can suppress success-only output.

**Canonical pattern (see e.g. `lint_handoffs.ts`):**

```ts
const QUIET = process.argv.slice(2).includes('--quiet');
// ...
if (!QUIET) {
    console.log('✅ All clean');
}
```

Failure output (`❌`, non-zero exit) is **never** gated — failures must
always print regardless of `--quiet`.

### 2. `_lib/script_output` helpers — preferred for new scripts

For anything richer than a single `✅`/`❌`, import the verbosity-aware
router instead of raw `print()`:

```ts
import { info, success, warn, error, flush_summary } from './_lib/script_output.js';

info('Loading manifest');          // drops on silent + minimal
success('Wrote 3 files');          // collected at minimal, printed at verbose
warn('Skipping stale entry');      // stderr unless silent
error('Manifest missing');         // stderr always

flush_summary('Done — 3 entries'); // one-line summary at minimal
```

Resolution order (first wins, cached for the process):

1. `AGENT_SCRIPT_VERBOSITY` env (`silent` / `minimal` / `verbose`)
2. `SCRIPT_OUTPUT_VERBOSE=1` alias (== `verbose`)
3. `.agent-settings.yml` → `verbosity.script_output`
4. Default `minimal`

The resolved level is exported back into `AGENT_SCRIPT_VERBOSITY` so
child processes inherit it. Tests reset via `reset_level()` from the
same module — see `tests/lib/script_output.test.ts`.

### 3. Iron-Law carve-outs — never silenced

The following surfaces **MUST** use plain `print()` and never the
helpers, so verbosity settings cannot suppress them:

* Release confirms — every task in `taskfiles/release.yml`
* Secret prompts — `install-anthropic-key`, `install-openai-key`,
  `setup-evals`, `install-hooks` interactive sections
* `runtime-e2e` and `test-triggers-live`
* CI orchestration sentinels — `_ci-start`, `_ci-end`, root `ci`
* Any prompt that asks the user for confirmation per
  [`non-destructive-by-default`](../../rules/non-destructive-by-default.md) — Hard Floor cannot be silenced

If unsure, check `src/scripts/ai_council/one_off_archive/2026-05/README.md`
for the archived carve-out inventory.

### 4. Taskfile wiring — `silent: true` + `{{.QUIET_FLAG}}`

Every Taskfile task that wraps a `--quiet`-aware script MUST set
`silent: true` and pass `{{.QUIET_FLAG}}` to the script:

```yaml
# Per-task in taskfiles/*.yml:
tasks:
  lint-handoffs:
    silent: true
    cmd: ./scripts-run src/scripts/lint_handoffs {{.QUIET_FLAG}}
```

The `QUIET_FLAG` var is defined once at the root of `Taskfile.yml`
and resolves to `""` only when `AGENT_SCRIPT_VERBOSITY=verbose`:

```yaml
# Root Taskfile.yml — already in place, do not duplicate:
vars:
  QUIET_FLAG:
    sh: '[ "$AGENT_SCRIPT_VERBOSITY" = "verbose" ] && echo "" || echo "--quiet"'
```

Carve-out tasks (release, install secrets, CI orchestration — see § 3)
do **not** add `silent: true` and do **not** use `{{.QUIET_FLAG}}`.

### 5. Validate

* Run `./scripts-run src/scripts/skill_linter src/skills/script-writing/SKILL.md` → 0 FAIL
* Run `./scripts-run src/scripts/{your-script} --quiet` and the verbose path — exit code 0 on clean, non-zero on failure regardless of flag
* If the script uses `_lib/script_output`, add a test under `tests/` patterned on `tests/lib/script_output.test.ts` — assert `silent` / `minimal` / `verbose` behave per § 2
* Run the full CI pipeline locally (see `Taskfile.yml` in this repo for the script list) — must exit 0 except for tolerated warnings

## Output format

1. Script file at `src/scripts/{name}.ts` with `--quiet` accepted
2. Taskfile wiring with `silent: true` + `{{.QUIET_FLAG}}` (unless carve-out)
3. Test under `tests/` if `_lib/script_output` is used
4. Linter output showing 0 FAIL

## Gotchas

* Forgetting `--quiet` — the silent Taskfile layer wraps the script and the call fails with `unrecognized arguments: --quiet`
* Gating `❌` failures behind `--quiet` — failures must always print
* Using raw `print()` for progress lines — drops on `minimal`, no inheritance
* Adding `silent: true` to a release / install-keys task — bypasses the Hard Floor confirmation
* Editing `Taskfile.yml`'s `QUIET_FLAG` var — single source of truth, do not duplicate
* Forgetting that `import … from './_lib/script_output.js'` resolves relative to the script's own directory — copy the import path from a peer under `src/scripts/`

## Frugality Standards

Apply the [Frugality Charter](../../contexts/contracts/frugality-charter.md)
to every script you author. Phase 10 of the charter (settings hooks
row — `verbosity.script_output` / `verbosity.taskfile_command_echo`)
is what this skill exists to teach.

**Examples in this artifact:**
- Per the charter's default-terse rule, success lines are gated behind
  `--quiet` so the only thing visible at `minimal` is the end-of-run
  summary or a failure.
- Per the post-action summary suppression, scripts with multi-step
  output collect via `success()` and emit one `flush_summary()` line.
- Per the cheap-question check, scripts never prompt unless they hit
  a Hard Floor surface (§ 3 carve-outs).

**Pre-save self-check:**
1. Does every `print("✅ ...")` line sit behind `--quiet` / the helper?
2. Does the script add `silent: true` + `{{.QUIET_FLAG}}` to its
   Taskfile entry (unless a carve-out)?
3. Are failure lines (`❌`, exit non-zero) **never** gated by quiet?
4. Are Iron-Law surfaces using plain `print()` and not the helper?

## Do NOT

* Do NOT gate `❌` / failure output behind `--quiet`
* Do NOT use `_lib/script_output` for release confirms or secret prompts
* Do NOT add `silent: true` to carve-out tasks
* Do NOT hardcode `print()` for progress in new scripts — use `info()`
* Do NOT skip the Taskfile wiring — without it the verbosity gates leak
* Do NOT edit `dist/agent-src/`, `.augment/`, or `.claude/` projections

## Cloud Behavior

On cloud surfaces (Claude.ai Web, Skills API) the package's `task`
runner and `_lib/script_output` are not reachable. The skill still
applies — with prose-only validation:

* Emit the full script + Taskfile snippet as copyable Markdown blocks. Do not attempt to write to disk.
* Self-check: `--quiet` accepted, failures never gated, success lines gated, helper imports look syntactically right.
* Tell the user to save under `src/scripts/{name}.ts`, wire the Taskfile entry, and run `task lint-skills && task ci` locally before committing.
* Skip every reference to running the linter or `task` commands yourself — they only run on the user's machine.

## Examples

Good description (trigger-shaped, names domain + symptoms):

> "Use when adding or editing any script under `scripts/` — `--quiet` flag, `_lib/script_output` helpers, silent Taskfile wiring, Iron-Law carve-outs — even when you just say 'add a check script for X'."

Bad description (vague, no trigger):

> "Script conventions"
