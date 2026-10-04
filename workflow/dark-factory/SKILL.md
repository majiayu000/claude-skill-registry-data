---
name: dark-factory
description: "Run the Dark Factory DOT pipeline runner against a goal. Slash command: /factory. Implements StrongDM's Attractor pattern as an external Python runner — .dot files are the versioned artifact, sealed holdouts live in a separate repo, every step is recorded to CXDB, and the Healer clusters failures into diagnoses. Use when you want the goal_harness idea executed as a reproducible external pipeline instead of in-Claude subagent dispatch."
---

# /factory — Dark Factory Pipeline Runner

## Purpose

Run a goal through the Dark Factory `.dot` pipeline runner at
`~/projects/dark-factory/`. The runner is the Python implementation of
StrongDM's Attractor pattern (cf. brynary/attractor, strongdm/attractor).

Versus `/h` / `/goal_harness`:

| Aspect | `/h` (goal_harness) | `/factory` (this skill) |
|--------|---------------------|-------------------------|
| Engine | Claude session dispatches subagents | **`dark-factory` binary** (uv install) |
| Artifact | Skill prose + tool calls | `.dot` graphviz file |
| Recording | Conversation transcript | SQLite CXDB row-per-step |
| Holdouts | Adversarial subagent reads diff | Sealed repo agent never sees |
| Reuse | Tied to this session | Replayable from `.dot` alone |
| Cost | High (multi-agent context) | Low (one CLI per node) |

Use `/factory` when you want the goal_harness idea as a reproducible external
pipeline; use `/h` when you want an interactive in-session loop.

## Entry points

| Command | Behavior |
|---------|----------|
| `/f` | Full loop, auto-routes PR-mode vs feature-mode (Step 0a below) |
| `/factory` | Alias for `/f`, identical behavior |
| `/f-pr` | Explicit PR-mode entry point (skips auto-route, always PR-mode) |
| `/fs` | Spec-generation entry point; runs `pipelines/slim/spec_gen.dot` or a binary-owned dynamic spec graph — run this first when the goal needs a spec |

This skill file is the single source of truth for the binary-first contract;
`.claude/commands/f.md` is the canonical command entry point, with `/factory`
and `/f-pr` as thin aliases so auto-detect behavior stays identical across
entry points.

**What "binary-first" bans**: an in-Claude prose-only workflow that claims a
factory run without a logged binary invocation is not a valid run — see
**Honesty rules** below. Every default run must preserve required default
nodes or their graph-level equivalents: plan/spec producer, independent
review, bounded fix loop, evidence gates, and exit summary. Dynamic graph
generation is valid only when the generated/selected DOT graph is saved or
echoed in the run evidence.

## Repos

- `~/projects/dark-factory/` — the runner (factory code; agent can see this)
- `~/projects/dark-factory-holdouts/` — sealed scenarios (agent must NEVER read)
- Pushed: `https://github.com/jleechanorg/dark-factory` + `dark-factory-holdouts`

## Available pipelines

| `.dot` file | Flow | When to use |
|-------------|------|-------------|
| **`pipelines/slim/two_node.dot`** ⭐ default | worker → fresh Codex reviewer → exit | **Default for `/f` and `/factory`** when no `--pipeline` is passed. The reviewer is a fresh fully tooled `codex exec --ephemeral --yolo` process; its response is copied to the worker on failure. |
| `pipelines/factory/hello.dot` | plan → implement → holdout → fix-loop → exit | Add a new feature with a holdout scenario |
| `pipelines/factory/gates.dot` | start → holdout → /es → /er → /code_standards → exit | Validate an already-implemented diff (Attractor-style 4-gate harness as `.dot`) |
| `pipelines/factory/pr_gates.dot` | start → holdout → /es → /er → /code_standards → exit | Validate an already-implemented in-flight PR diff (Holdout-always policy; requires `--feature <name>` for the holdout) |
| `pipelines/slim/minimal_feature.dot` | explore → plan → implement → test → review → holdout → gates → exit | Full production pipeline from scratch with a holdout |
| `pipelines/slim/minimal_pr.dot` | explore → plan → implement → test → review → holdout → gates → exit | Slim in-flight PR iteration loop with parameterized tests (Holdout-always policy; requires `--feature <name>` for the holdout) |

| `pipelines/factory/level5_feature.dot` | full reference pipeline | Full Level-5 reference pipeline with hard-tier gates wired in |
| **dynamic DOT via binary** | binary-owned graph builder | A static graph can't express the needed phase/fanout; the binary saves/echoes the generated graph in run evidence |
| **no pipeline** | — | When no available pipeline fits the inspected PR, follow canonical **Honesty rules** below: report the limitation and return to the parent for authorized work; do not force an inapplicable holdout pipeline |

You can also write your own `.dot` and pass it via `--pipeline`.

### How to invoke this skill

The user types `/f $ARGUMENTS` (or `/factory $ARGUMENTS`). Parse the
arguments and run the steps below. When `--pipeline` is omitted, `/f` and
`/factory` default to `two_node` (`pipelines/slim/two_node.dot`). Non-default
pipelines require explicit opt-in via `--pipeline <name>`.

### Step 0a — Auto-route PR-mode vs feature-mode (applies to `/f` and `/factory`; `/f-pr` skips this and forces PR-mode)

Run once before dispatch:

```bash
gh pr list --head "$(git rev-parse --abbrev-ref HEAD)" \
  --json number,title,state,isDraft,additions,deletions,changedFiles,baseRefName,headRefName,labels
echo "$ARGUMENTS"
```

Reasoning (LLM, not rules):
- **No open PR** → feature-mode (new work).
- **Open PR exists** AND goal relates to it → PR-mode (drive the existing PR to green).
- **Open PR exists** AND goal is unrelated → **ask the user** which mode they meant. Do not silently route.

### `/f-pr` — explicit PR-mode entry point

`/f-pr` skips Step 0a and always runs PR-mode. Use the LLM to **read the
PR's actual context and pick the right pipeline** — this is a reasoning
task, not a deterministic rule table (no `if is_draft then X`, no
`if labels contains 'bug' then bug_fix.dot`, no keyword-routing).

1. **Resolve the PR number**: from `$ARGUMENTS` if present, else
   `gh pr list --head "$(git rev-parse --abbrev-ref HEAD)" --json number --jq '.[0].number'`,
   else ask the user.
2. **Read PR context as facts, not routing rules**:
   ```bash
   gh pr view <N> --json number,title,state,isDraft,additions,deletions,changedFiles,baseRefName,headRefName,body,files,labels
   gh pr view <N> --json statusCheckRollup
   gh pr diff <N> --name-only
   gh pr view <N> --comments   # optional
   ls specs/ roadmap*/ docs/design/ 2>/dev/null   # optional
   ```
3. **Reason about**: what kind of work this is (new feature / bug fix /
   refactor / docs / test-only / infra — from diff+body+files, never
   pre-bucketed by label alone); whether a spec already covers the
   change (if so, `/fs` is skippable; if needed, report the prerequisite
   and carry out its already-authorized preparation or return it to the
   parent task under active repository role and execution constraints.
   Do not force a pipeline run before it is ready); holdout
   eligibility (pass `--feature <name>` only if
   `~/projects/dark-factory-holdouts/holdouts/<feature>/` actually
   exists — never invent one); and what evidence mix (`/es` + `/er` +
   `/code_standards` minimum, `holdout_eval` for behavior-grade) the
   pipeline needs to deliver without over-running.
4. Execute only after needed preparation is complete and a pipeline
   actually fits: pick the pipeline from **Available pipelines** above
   using that reasoning, pick the backend (`echo` for wiring smoke;
   `claude` unless the PR's reviewer queue or `gate_er` priority queue
   says otherwise), then construct, show, and run the command — same
   shape as Step 0c below but `cd` into the PR's target repo, not
   `dark-factory`.
5. Report the outcome: when a pipeline ran, report the verdict per
   **Output contract** below; otherwise report the unmet prerequisite or
   no-fitting-pipeline limitation and return to the parent task with no
   fabricated run ID, exit code, or review verdict, preserving authorized
   parent continuation.

`/f-pr` honesty rules (in addition to the shared ones under **Honesty
rules**): the `gate_er` priority queue (`codex > minimax > agy >
claude-sonnet`) still resolves the reviewer even when `--backend claude`
was passed for the run itself — passing `--backend claude` does not mean
`gate_er` uses claude by default.

### Step 0b — Auto-detect CLI backend

When the user invokes Claude via a `~/.bashrc` wrapper (`claudem`, `clauded`,
`codex`, `agy`), bash exports a `BASH_FUNC_<wrapper>%%` env var. Read these to
pick the right `--backend` flag so the LLM that runs the audit is the same
one the user picked from their shell. `%%` in the var name breaks
`${BASH_FUNC_X%%:-default}` and `${!key}` expansion, so use `printenv`:

```bash
detect_cli_backend() {
  local key parent_comm ppid
  for key in 'BASH_FUNC_claudem%%' 'BASH_FUNC_clauded%%' 'BASH_FUNC_agy%%' 'BASH_FUNC_codex%%' 'BASH_FUNC_claude%%'; do
    if [ -n "$(printenv "$key" 2>/dev/null)" ]; then
      case "$key" in
        *claudem%%) echo "minimax"; return ;;
        *clauded%%) echo "claude";  return ;;
        *agy%%)     echo "agy";     return ;;
        *codex%%)   echo "codex";   return ;;
        *claude%%)  echo "claude";  return ;;
      esac
    fi
  done
  case "${ANTHROPIC_BASE_URL:-}" in
    *api.minimax.io*) echo "minimax"; return ;;
    *anthropic.com*)  echo "claude";  return ;;
    *openai.com*)     echo "codex";   return ;;
  esac
  ppid="${PPID:-}"
  if [ -n "$ppid" ]; then
    parent_comm="$(ps -o comm= -p "$ppid" 2>/dev/null | tr -d ' ')"
    case "$parent_comm" in
      *claude*|*claudem*) echo "claude"; return ;;
      *codex*)            echo "codex";  return ;;
      *agy*|*antigrav*)   echo "agy";    return ;;
    esac
  fi
  echo "claude"
}
DETECTED_BACKEND="$(detect_cli_backend)"
```

Override precedence (highest to lowest): explicit `--backend <x>` flag >
`BASH_FUNC_*` wrapper signal > `ANTHROPIC_BASE_URL` > parent process name >
hardcoded default (`claude`). Always echo the detected backend + source in
the proof block (see **Output contract**). If `--backend` was passed
explicitly, note the override rather than the raw detection.

### Step 0c — Pipeline selection

When `--pipeline` is omitted, the runner dispatches `pipelines/slim/two_node.dot` by default. To opt into a non-default pipeline (such as `gates`, `minimal_feature`, `review_slim`, etc.), pass explicit `--pipeline <name>`.

### Short-name expansion

When `--pipeline` is a short name (no `/` or `.dot`), expand under
`$DARK_FACTORY_HOME`:

| Short name | Path |
|------------|------|
| `two_node` | `pipelines/slim/two_node.dot` |
| `gates` | `pipelines/factory/gates.dot` |
| `hello` | `pipelines/factory/hello.dot` |
| `pr_gates` | `pipelines/factory/pr_gates.dot` |
| `minimal_feature` | `pipelines/slim/minimal_feature.dot` |
| `minimal_pr` | `pipelines/slim/minimal_pr.dot` |
| `review_slim` | `benchmarks/attractor-spec-review/pipelines/review_slim.dot` |
| `review_full` | `benchmarks/attractor-spec-review/pipelines/review_full.dot` |
| `spec_gen` | `pipelines/slim/spec_gen.dot` |
| `bug_fix` | `pipelines/bug_fix.dot` |
| `level5_feature` | `pipelines/factory/level5_feature.dot` |

### Default graph when `--pipeline` is omitted

When the user invokes `/f` or `/factory` with no `--pipeline` flag, the
runner dispatches `pipelines/slim/two_node.dot` by default — exactly two
productive nodes (a generic `worker` codergen + a `cold_reviewer`
`type="codergen"` verdict gate), plus a bounded fix loop. The cold reviewer
runs as a fresh fully tooled Codex process in the worker's target worktree;
the engine copies its exact response back into the worker prompt on failure.

To opt into a richer pipeline, pass an explicit `--pipeline <name>`. To
roll your own (e.g. a custom slim or feature shape), pass
`--pipeline /absolute/path/to/your.dot`. Custom dot graphs always win
over the default — there is no scenario where `/f` will silently fall
through to a heavyweight pipeline.

The default is the user's standing rule (set 2026-08-02): **slim two-node
is the default; custom graphs are explicit opt-in.** This applies to all
`/f` invocations across this repo.

### Arg parsing

Honor these flags inside `$ARGUMENTS`:

- `--pipeline <name>` — short name (`two_node`, `gates`, `hello`, `pr_gates`,
  `minimal_pr`, `minimal_feature`, `review_slim`, `review_full`) or path to a
  `.dot`. If omitted, the runner dispatches the slim two-node default graph
  (`pipelines/slim/two_node.dot`) — a generic worker + fresh, fully tooled
  Codex reviewer — for every `/f` and `/factory` invocation. To opt into the
  heavyweight pipelines (gates / minimal_feature / etc.) pass an explicit
  `--pipeline <name>`. The previous "auto-select from the goal" behavior is
  retired; the slim two-node shape is the new default across the board.
- `--feature <name>` — holdout feature. Required when the pipeline includes a
  `holdout_eval` node, but never default it blindly: pass it only after
  confirming `~/projects/dark-factory-holdouts/holdouts/<name>/` actually
  exists (`hello` is a real, feature-agnostic holdout and a reasonable choice
  when the goal has no more specific holdout, but confirm the directory
  exists before passing it rather than defaulting unconditionally — see
  Honesty rules below on not inventing `--feature` values)
- `--backend echo|claude|codex|ao|agy` — default `claude`. Use `echo` for cost-free
  dry-runs that verify wiring without LLM calls.
- `--max-steps <N>` — default 100
- `--cxdb <path>` — default `~/.dark-factory/cxdb.sqlite` (shared across runs
  so the Healer can cluster across history)
- `--state KEY=VALUE` — pre-seed context variables; repeatable. Extremely useful for setting parameterized test commands (e.g. `--state slim.test_command="pytest tests/..."`) during PR iteration loops.

Whatever is left after flag parsing is the **goal description**.

### Steps

Before Steps 1–2, define this resolver. It preserves an explicit
`DARK_FACTORY_HOME`; otherwise it resolves the `dark-factory` binary selected
from `PATH`, follows symlinks, derives its repository root, and exports that
same source for pipeline and prompt resolution:

```bash
resolve_dark_factory_home() {
  if [ -z "${DARK_FACTORY_HOME:-}" ]; then
    DARK_FACTORY_BIN="$(command -v dark-factory 2>/dev/null)" || {
      echo "ERROR: dark-factory is not on PATH; run ./install.sh first"
      return 1
    }
    DARK_FACTORY_BIN="$(python3 -c 'import os, sys; print(os.path.realpath(sys.argv[1]))' "$DARK_FACTORY_BIN")" || {
      echo "ERROR: unable to resolve the installed dark-factory binary"
      return 1
    }
    DARK_FACTORY_HOME="$(cd "$(dirname "$DARK_FACTORY_BIN")/.." && pwd -P)" || return 1
  fi
  export DARK_FACTORY_HOME
}
```

1. **Verify binary install**. The factory runs via the **`dark-factory` binary**
   (not `python -m runner` from source). If missing, report the unmet prerequisite
   and inspect the existing installation before cloning or reinstalling. Complete
   setup within the current authorized scope and repository execution rules, or
   return the limitation to the parent for other authorized work. Ask only for
   missing authority or access; an unavailable binary is not a completed run.
   The following check runs as a tool command; its failure ends that command,
   then the parent follows the prerequisite guidance above:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   resolve_dark_factory_home || exit 1
   command -v dark-factory || exit 1
   dark-factory --help || exit 1
   test -x "$DARK_FACTORY_HOME/bin/dark-factory" || {
     echo "ERROR: run $DARK_FACTORY_HOME/install.sh first"
     exit 1
   }
   ```

2. **Environment**:
   ```bash
   resolve_dark_factory_home || exit 1
   export DARK_FACTORY_HOLDOUTS="${DARK_FACTORY_HOLDOUTS:-$HOME/projects/dark-factory-holdouts}"
   export PATH="$HOME/.local/bin:$PATH"
   ```

3. **Run the pipeline** from the **target repo** (implementation workdir = cwd).
   Pipelines and prompts resolve from `$DARK_FACTORY_HOME`; code changes land in cwd:
   ```bash
   cd "<TARGET_REPO>"   # e.g. the product repo being built
   dark-factory \
     --pipeline pipelines/<PATH_TO_DOT>.dot \
     --goal "<GOAL>" \
     --backend <BACKEND> \
     --feature <FEATURE> \
     --cxdb <CXDB_PATH> \
     --state <KEY>=<VALUE>
   ```

4. **Surface the verdict**. The last line of stdout is a JSON summary with
   `final_outcome`, `pipeline`, `goal`, `steps`, `trace`. Report:
   - Pipeline name + final outcome
   - Per-node trace (one line each: `node  outcome  preview`)
   - Exit code of the runner

5. **Run the Healer** (only if `final_outcome != "success"`):
   ```bash
   df-healer --cxdb <CXDB_PATH>
   ```
   Render the resulting markdown table inline. Each row is a failure cluster
   with a prescription template the user can act on.

6. **Sealed holdouts reminder**. If the run included a `holdout_eval` node,
   remind the user that you (and any subagent) did NOT see the scenarios at
   `~/projects/dark-factory-holdouts/holdouts/<feature>/` — only the
   PASS/FAIL verdict per scenario name leaked back.

## Reviewer calibration (default on)

`--reviewer-calibration=true` is the default for every real `/f`/`/factory`
run. Treat the flag as present unless the user explicitly passes
`--reviewer-calibration=false`.

Calibration routes the Codex backend through the binary-owned controller
command:

```bash
dark-factory review \
  --workdir <repo> \
  --base-sha <full-40-hex-sha> \
  --head-sha <full-40-hex-sha> \
  --task-file <path> \
  --output-dir <dir> \
  --backend codex
```

`dark-factory review` owns the static prompt, canonical envelope, backend
dispatch, response validation, and `controller-receipt.json`. Controller v1
accepts only Codex through its tool-free JSONL transport. A valid PASS requires
non-empty `evidence_checked` and `commands_executed: []`; the
`ReviewTransportReceipt` and controller terminal receipt bind the prompt,
envelope, response, reviewed revision/tree, and evidence manifest. Do not
author reviewer instructions, do not inline prompts, do not pass vendor CLI
flags. The controller binds `prompt SHA-256`, `envelope SHA-256`, `task
SHA-256`, `diff SHA-256`, `changed-files SHA-256`, and
`evidence-manifest SHA-256` in the controller receipt so calibration lanes can
hash the receipt itself for provenance.

Each accepted lane must expose a controller receipt digest containing
the prompt SHA-256, envelope SHA-256, task SHA-256, diff SHA-256,
changed-files SHA-256, evidence-manifest SHA-256, head SHA, base SHA,
and the response's own response SHA-256 digest. Hashing the
`controller-receipt.json` file itself gives a stable SHA-256 digest for
the controller receipt.

`prompt.txt` is a binary-emitted audit capture, not an authority file.
The static authority lives in `prompts/catalog/controller_cold_review_v1.md`
and is bound by its SHA-256 of the controller receipt.

```text
evidence/<run-id>/reviewer-calibration/
  <backend>/
    controller-receipt.json
    envelope.json
    prompt.txt
    reviewer.output.md
    findings.json
  comparison.json
  adjudication.md
```

Do not claim delegated subagents underperformed raw Codex unless the same
envelope and prompt were reviewed at the same SHA and raw Codex found a
later-confirmed blocker the delegated reviewer missed. If calibration is
disabled, the final response must say `Reviewer calibration: disabled` and
give the explicit reason.

The `gate_er` priority queue is `codex > minimax > agy > claude-sonnet` by
default; passing `--backend claude` for the run itself does not change how
`gate_er` resolves its reviewer.

## Output contract

When a pipeline ran, end the `/f`/`/factory` invocation with this proof block
(missing any required line means the run is unproven and must be reported as
such). When no pipeline ran because a prerequisite was unmet or no applicable
pipeline fits, report the unmet prerequisite or no-fitting-pipeline limitation
and return to the parent task without fabricated run metadata (no fabricated
run ID, exit code, or review verdict), preserving authorized parent
continuation.

For executed pipeline runs, provide this proof block:

```bash
# CLI backend: <detected-or-override> (source: <BASH_FUNC_X%%|explicit --backend|default>)
# Literal command run:
cd /Users/jleechan/projects/<target-repo>
DARK_FACTORY_HOLDOUTS=~/projects/dark-factory-holdouts \
PATH="$HOME/.local/bin:$PATH" \
dark-factory \
  --pipeline <chosen-or-generated-dot> \
  --goal "<echo of $ARGUMENTS>" \
  --backend <backend> \
  --feature <feature-if-any> \
  --cxdb ~/.dark-factory/cxdb.sqlite
# Run ID: <id>
# CXDB SHA: <sha>
# Final outcome: <success|failure|exhausted|error>
# Exit code: <integer>
# Wall-clock: <duration>
# Logs: <path>
# Evidence envelope: <path>
# Reviewer calibration: <enabled|disabled> <artifact-path-or-reason>
```

Plus the per-node trace and, on failure, the Healer report.

## Adding a new feature

To add a new sealed-holdout feature `foo`:

1. Write `~/projects/dark-factory/specs/foo.md` (agent-visible).
2. Write `~/projects/dark-factory/prompts/foo/{plan,implement,fix}.md`.
3. Write `~/projects/dark-factory-holdouts/holdouts/foo/scenarios.yaml`
   in the sealed repo (the implementing agent must never read this).
4. Either reuse `pipelines/factory/hello.dot` (which is feature-agnostic) by
   passing `--feature foo`, or write `pipelines/factory/foo.dot` with custom
   nodes.

## Review Verdict Interpretation Contract (Zero Inversion)

- `status: "valid"` / `backend_returncode: 0`: Indicates only that the reviewer CLI/transport executed cleanly and emitted valid JSON matching the schema. It does **NOT** indicate that the code passed.
- `verdict: "fail"` / `exit_code: 2`: Indicates the independent review **REJECTED** the change.
- `verdict: "pass"` / `exit_code: 0`: Indicates the review **ACCEPTED** the change.
- **NEVER** treat `status: "valid"` or a successful LLM invocation as a passing verdict when `verdict == "fail"`.

### Review Result Surface Requirements

Whenever `dark-factory review` completes, the agent MUST immediately report:
- **If `verdict: fail` (exit code 2)**:
  1. `VERDICT: REJECTED (FAIL)`
  2. The exact reviewed `HEAD_SHA` and `BASE_SHA`.
  3. List of all failing Criteria Gates (`C0`–`C7`) and Evidence Gates (`E0`–`E14`).
  4. Full verbatim list of Critical, High, and Blocker findings from `reviewer.output.md`.
  5. Explicit statement that the PR is NOT `/ready` and CANNOT be merged.
- **If `verdict: pass` (exit code 0)**:
  1. `VERDICT: ACCEPTED (PASS)`
  2. The exact reviewed `HEAD_SHA` and `controller-receipt.json` digest.

### Loop Exhaustion Invariant

- Reaching the maximum cycle budget (e.g., 3/3 cycles) without achieving `verdict: pass` constitutes a **FAILED RUN**.
- The agent MUST report `STATUS: REVIEW FAILED / EXHAUSTED AFTER N CYCLES` and
  end that factory invocation and return its failure evidence to the parent task.
  The parent continues authorized work within the mission deadline and the
  active repository's role and execution rules. Where coding must run through
  auto-factory, route repairs through a fresh or adjusted factory run.
  An invocation's cycle budget is not a mission stop.
- An agent must **NEVER** summarize cycle exhaustion as "addressed findings", "all gates passing", or "/ready".

## Honesty rules

- Always tell the user the **actual command** you ran (`dark-factory ...` or `df-healer ...`). No paraphrasing.
- Always quote the **runner's exit code** and **actual review verdict** (`pass` / `fail`) verbatim.
- Never rewrite or summarize a failed review (`verdict: fail`, exit code 2) as a success, pass, or confirmation.
- Never claim a PR is `/ready`, `/green`, or "All gates passing" when the review verdict is `fail` or when CI checks are pending/failing.
- Never claim a holdout passed if you read the scenarios — that breaks the
  adversarial guarantee. If you read `~/projects/dark-factory-holdouts/`,
  declare the run **invalid** and rerun the pipeline.
- If `--backend echo` was used, label the run as a wiring smoke, not a real
  validation.
- Reviewer calibration is default-on. If `--reviewer-calibration=false` is
  passed, quote the explicit opt-out reason and do not imply raw-Codex-vs-
  subagent quality was measured.
- Do not claim a factory run based on an in-Claude workflow, `Skill()` call,
  or prose summary. The only valid proof is an actual `dark-factory` binary
  invocation plus the proof block above.
- If `/fs` is needed first, follow `/f-pr` item 3: report the prerequisite and
  carry out its already-authorized preparation or return it to the parent task
  under active repository role and execution constraints. Ask only for missing
  authority; do not silently fall through to `gates.dot` and pretend the PR is green.
- If no pipeline fits (e.g. docs-only PR), report that limitation and return to
  the parent task for authorized diagnosis or preparation. A materially different
  requested method needs authorization; do not silently substitute a
  holdout-bearing pipeline.
- Do not invent `--feature` values. If there's no holdout directory at
  `~/projects/dark-factory-holdouts/holdouts/<feature>/`, don't pass `--feature`.
- When the goal is unrelated to the open PR (Step 0a), **ask the user** which
  mode they meant. Do not silently route to PR-mode for unrelated work.
- When the fix loop exhausts (3 attempts), surface its failure diagnosis and
  return control to the parent as above. Preserve the failed verdict; never
  auto-merge or retry an unchanged failing approach merely to get a pass.

## Known limits

- The `claude` backend shells out to `claude --print
  --dangerously-skip-permissions` — each node is a fresh non-interactive
  session. Long agentic loops should use `/h` instead.
- `_parse_verdict` falls back to scanning the tail for a standalone PASS/FAIL
  token; if the gate command emits a debug line with just "PASS" the runner
  will trust it. For high-stakes gates require explicit `VERDICT:` markers.
- CXDB is per-process — don't share one across threads.
