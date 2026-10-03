---
name: ate
description: "ATE (Automated Testing Environment): drive long-running (2-3hr+) unattended variation-test suites against the Aider, OpenRouter, and GLM 5.2 pipeline using a local Gemma model in LM Studio as the worker, with periodic frontier-model check-ins for drift control, ending in a single triaged GitHub issue. Use this whenever the user wants to \"run variation tests overnight/for hours\", \"debug a bunch of small Aider bugs\", \"test Aider flag combinations\", \"fuzz the Aider harness\", mentions LM Studio + Gemma as a local test driver, wants test failures rolled up into one GH issue triaged by severity, or invokes ATE by name. Also trigger if the user asks to set up a check-in loop between a local model and a frontier model for a long-running task."
---

# ATE — Automated Testing Environment (generic bounded-variation matrix runner)

The skill interface lives here; its implementation is bundled under
[`utils/ate/`](https://github.com/HiQS-Labs/XYZ-forge/blob/development/utils/ate).

ATE walks a declared grid of command variations unattended for hours, logs every result as
structured JSON, and a frontier model (you, Claude) checks in every ~5 minutes to catch
drift/looping. The full cycle — run, capture, document, file — is chained end to end: when the
run ends (time limit, abort, or safety cap), `run_variations.py` automatically hands off to
`compile_issue.py`, which opens **one** GitHub issue titled
`ATE - [test-name] yyyy-mm-dd` containing every finding from that run as a single
checklist, ranked by severity (critical first). No manual second step required
as long as `--gh-repo` was passed.

## Architecture (linear)

1. **Gemma (LM Studio, local)** — worker. Cycles through the variation grid
   (repeating from the top once it reaches the end), runs
   `aider --model openrouter/z-ai/glm-5.2 ...` as a subprocess, classifies the result.
2. **error_log.jsonl** — the single source of truth. Append-only. Every variation
   writes one line here regardless of pass/fail.
3. **control.json** — the only channel Claude writes to. Gemma polls it before each
   iteration. `{"action": "continue"}` / `{"action": "abort", "reason": "..."}`.
   `run_variations.py` resets this to `continue` at the start of every run, so a
   stale abort from a previous run in the same directory can't kill a fresh one.
4. **Claude (you)** — supervisor. Every ~5 min, run `checkin.py`, read the summary,
   decide continue/abort, write `control.json` if aborting.
5. **compile_issue.py** — chained automatically: `run_variations.py` calls it the
   moment the run stops (time limit, abort, or safety cap), passing `--gh-repo`
   through. It groups `error_log.jsonl` by severity/signature into one unified,
   severity-ranked checklist and opens a single GitHub issue titled
   `ATE - [test-name] yyyy-mm-dd` via `gh issue create`. Can still be run standalone
   for a manual rollup (e.g. after a crash that killed `run_variations.py` before
   it could chain).

## Quick start (do this first)

```bash
# 1. Install
bash utils/ate/install.sh           # copies the interface + implementation to ~/.claude/skills/

# 2. In LM Studio: load a Gemma 4 model (31B Dense recommended), start the
#    Local Server (Developer tab -> Start Server). Default: http://localhost:1234/v1
#    Note the exact model identifier shown in LM Studio's server log/model list.

# 3. Set OpenRouter key for the Aider side of the pipeline being tested
export OPENROUTER_API_KEY="sk-or-v1-..."

# 4. Point run_variations.py at a scratch git repo (never your real repo).
#    error_log.jsonl and control.json land in this directory by default —
#    run checkin.py from here too, or pass --log/--control explicitly.
cd ~/scratch/aider-test-repo && git init -q

# 5. Kick off the run (defaults to 3 hours, edit variations.yaml first).
#    --gh-repo is what turns on the automatic issue filing at the end — omit it
#    to just get error_log.jsonl with no GitHub side effect. Requires
#    `gh auth status` to already be logged in.
python3 ~/.claude/skills/ate/scripts/run_variations.py \
  --repo . \
  --variations ~/.claude/skills/ate/variations.example.yaml \
  --lmstudio-model "gemma-4-31b-instruct" \
  --gh-repo OWNER/REPO \
  --test-name "aider-flag-fuzz" \
  --minutes 180 &
```

Then, on your (Claude's) side, every ~5 minutes:

```bash
python3 ~/.claude/skills/ate/scripts/checkin.py --tail 20
```

Read the printed summary. If it looks healthy, do nothing (Gemma keeps polling
`control.json`, sees no abort, continues). If you see drift (see "What counts as
drift" below), abort the run — `checkin.py --abort "reason"` does this for you in
one call. There is no "redirect" action; the only control signals are `continue`
and `abort`.

When the run ends (time limit, abort, or the iteration safety cap of 20 full
passes over the grid — see "Notes / gotchas"), `run_variations.py` automatically
chains into `compile_issue.py` and opens one GitHub issue titled
`ATE - [aider-flag-fuzz] 2026-07-09` (using today's date and the `--test-name`
you passed, or the `variations.yaml` filename's stem if you didn't pass one) with
every finding from the run as a single severity-ranked checklist. Nothing further
to run by hand. If you need the standalone/manual form (e.g. `run_variations.py`
itself crashed before it could chain, or `--gh-repo` was omitted):

```bash
python3 ~/.claude/skills/ate/scripts/compile_issue.py \
  --log error_log.jsonl --repo OWNER/REPO --test-name "aider-flag-fuzz"
```

## Exit codes (#142)

Both scripts in the filing chain exit with a contract a wrapper, CI job, or supervising agent
can branch on. Before #142 every terminal state exited 0 — including a failed `gh issue create`
— so a multi-hour run's final step could fail invisibly.

| Code | Meaning |
|---|---|
| `0` | Issue filed, or `--dry-run` body rendered. |
| `3` | No records in the log — nothing to file. Distinct from filed so callers can tell "done its job" from "did nothing". |
| `1` | `gh issue create` failed. `issue_body.md` is preserved in the working directory for manual filing. |
| `2` | `run_variations.py` only: repo guard refused the run (`--repo` is the harness itself, or carries a remote without `--allow-destructive-reset`). |

`run_variations.py` propagates `compile_issue.py`'s code when `--gh-repo` is set: the run's exit
code IS the filing outcome. Supervisors: treat `0` and `3` as healthy ends, `1`/`2` as needing
attention, and abort-drift separately via `checkin.py`. The `gh issue create` call is capped at
120s (`ATE_GH_TIMEOUT_S` overrides); a hang, a missing `gh`, or a launch failure all land in
exit `1` with `issue_body.md` preserved — no traceback, no indefinite hold on the run's completion.

## Targets beyond Aider (#141 Phase 5)

The engine is target-agnostic: any grid with a `command_template` (argv-list form — values are
substituted per-token, never through a shell string) runs against any CLI. Aider is one preset,
not the subject.

- **Classifier oracle decoupling (`expects_edits`)** — the stock Aider grid expects the tree to
  change, so exit-0-with-no-edit classifies `fail/no_edit`. A grid that only probes (usage
  surfaces, read-only diagnostics) declares `expects_edits: false`, and exit-0-no-edit is a
  PASS. The #146 Gemma soak recorded 17 false HIGH `no_edit` verdicts before this key existed —
  do not run a non-edit grid without it.
- **Rollup labels are neutral by default** — `bug`, nothing else. The Aider preset opts back in
  via `issue_labels: [bug, aider-pipeline]` in its grid; any grid or `--issue-label` overrides.
  A turn-shim soak must never file Aider-labelled issues.
- **Declared non-Aider grids shipped here:** `variations.tool-density.yaml` /
  `variations.tool-calling.yaml` (script_runner benchmarks) and `variations.turn-shims.yaml`
  (turn-shim CLI-contract usage soak — read its header for the safe execution profile before
  wiring it to a runner; it is diagnostic, `expects_edits: false`, and must run against stubs or
  a disposable clone if extended past the usage surface).

## What counts as drift (abort triggers)

- 3+ consecutive iterations with the **same** `likely_cause` signature — Gemma is
  stuck re-testing the same bug instead of moving to the next variation
- Gemma marks something `pass` but the raw Aider stdout/stderr in the same record
  contains a traceback or non-zero exit code — classification is unreliable, stop
  and inspect
- No new lines appended to `error_log.jsonl` for 2+ check-in cycles — the worker
  has hung (check the LM Studio server and the `aider` subprocess). `checkin.py`
  has no memory of previous invocations, so use its printed
  `log_last_modified_seconds_ago` field and compare it against what you saw last
  check-in rather than relying on the tool to flag this automatically.
- Wall-clock time on a single variation exceeds `--per-variation-timeout` (default
  180s) — treat as a hang, not a slow test; `run_variations.py` kills it and logs
  it as `severity: high, category: timeout` automatically

## variations.yaml format

Grid of Aider flags to combine (see `variations.example.yaml`). Each combination
becomes one subprocess call. Keep the task `message` short and deterministic (a
fixed small task like "add a docstring to foo()") so failures are attributable to
the *pipeline* (Aider/OpenRouter/GLM plumbing), not to task ambiguity.

```yaml
model: openrouter/z-ai/glm-5.2
edit_formats: [diff, whole, udiff]
map_tokens: [0, 1024, 4096]
auto_commits: [true, false]
message: "Add a one-line docstring to the function `foo` in sample.py"
per_variation_timeout_seconds: 180
```

## Severity rubric (used by compile_issue.py to rank the unified checklist)

| Severity | Definition |
|---|---|
| critical | Aider process crashes, non-zero exit with traceback, or corrupts the git working tree |
| high | Wrong/no edit applied, OpenRouter auth or routing failure, timeout/hang |
| medium | Edit applied but malformed (bad diff format, partial file write) |
| low | Cosmetic — extra output noise, formatting drift, slow-but-succeeded |

## Files in this skill

- `scripts/run_variations.py` — the Gemma-driven worker loop (long-running); chains
  into `compile_issue.py` automatically when it stops, if `--gh-repo` was passed
- `scripts/checkin.py` — Claude-side supervisor: summarize + optionally abort
- `scripts/compile_issue.py` — rolls up `error_log.jsonl` into one GH issue titled
  `ATE - [test-name] yyyy-mm-dd`; runs standalone too, for a manual rollup
- `variations.example.yaml` — starter grid, copy and edit per pipeline under test
- [`utils/ate/install.sh`](https://github.com/HiQS-Labs/XYZ-forge/blob/development/utils/ate/install.sh) — copies the interface and implementation to `~/.claude/skills/`

## Notes / gotchas

- LM Studio's OpenAI-compatible endpoint ignores auth — no API key needed locally,
  but you must pass the exact model name LM Studio reports (`/v1/models` will list it).
- Aider's OpenRouter model string needs the `openrouter/` prefix on top of the
  OpenRouter slug itself: `openrouter/z-ai/glm-5.2` — the bare slug alone will fail.
- Gemma 4's training cutoff is Jan 2025 — if Aider's CLI flags have changed since,
  Gemma may generate stale flag names. `run_variations.py` only ever calls flags
  from `variations.yaml` (never lets Gemma invent flags), which sidesteps this.
- **Run everything against a disposable scratch repo.** `run_variations.py` does a
  destructive `git reset --hard` + `git clean -fdx` before *every* variation (so each
  variation starts from the same pristine state and results are comparable across the
  grid). This permanently deletes uncommitted and ignored files in `--repo`. Two guards
  refuse the obvious footguns before anything runs (GH-195): it hard-refuses `--repo`
  pointed at the harness clone itself, and refuses a `--repo` that has a git remote (i.e.
  looks like a real checkout) unless you pass `--allow-destructive-reset`. A fresh
  `git init` scratch repo has no remote, so the Quick start above needs no extra flag —
  and a `git init` with no commits yet no longer crashes (the script auto-creates a base
  commit to rewind to).
- The grid is cycled, not walked once — `run_variations.py` loops back to the
  start after the last combination and only stops on the time budget, an abort,
  or an iteration safety cap of `len(combos) * 20` (a backstop against a runaway
  `--minutes` value).
