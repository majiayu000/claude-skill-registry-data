---
name: plan-review-loop
description: Run a review loop on an implementation plan — author or locate the plan, get an independent multi-lane review (zero-context executability, grounding against the repo and source spec, task structure), then address findings with judgment. Use when a plan is written and needs adversarial review before execution, or when asked to "review the plan", "check this plan", or "plan review loop". Supports superpowers plans (docs/superpowers/plans/), planning-with-files task_plan.md, and any other plan format; the source spec is reviewed transitively via the traceability lane. For code review loops, see the review-loop plugin.
user-invocable: true
argument-hint: "<plan path | task to plan | cancel>"
metadata:
  version: "1.0.0"
---

# Plan Review Loop

Adversarial review loop for implementation plans, modeled on the review-loop plugin's implement → independent review → address cycle, but targeting **plans** instead of code. A plan defect costs an hour of review now or a day of wrong implementation later.

**Core principle:** A plan is only as good as its worst instruction executed by someone with zero context. Reviewers must never have seen the planning conversation — fresh context is the independence guarantee.

## Lifecycle

```
setup → locate-or-author → independent review → address with judgment → [confirm] → cleanup
```

State lives in `.claude/plan-review-loop.local.md`. Reviews are written to `reviews/plan-review-<id>.md`. On any tooling error, fail open: report the problem and continue without the loop rather than trapping the user.

**Enforcement:** the inkstone stop hook (`hooks/stop-hook.sh`) will not let the session stop while this loop's state file says the review is incomplete, findings are undispositioned, or a required confirmation round is pending. Keep the state file's `phase:` accurate as you progress — it is the contract with the hook.

**Coexistence with the original review-loop plugin:** the setup block below refuses to start while a code review loop (`.claude/review-loop.local.md`) is active, and the stop hook defers entirely to that plugin whenever its state file exists. Run doc loops and code loops sequentially, never concurrently.

## Phase 0 — Setup

If the argument is `cancel`: read `.claude/plan-review-loop.local.md` if it exists, report its phase and review id, delete it, and stop (note that any existing `reviews/plan-review-<id>.md` survives cancellation). If absent, report "No active plan review loop."

Otherwise run this setup command verbatim:

```bash
set -e && mkdir -p .claude reviews && if [ -f .claude/review-loop.local.md ]; then echo "Error: the original review-loop is active. Finish it or run /review-loop:cancel-review first." && exit 1; fi && if [ -f .claude/plan-review-loop.local.md ]; then echo "Error: a plan review loop is already active. Run plan-review-loop with argument cancel first." && exit 1; fi && REVIEW_ID="$(date +%Y%m%d-%H%M%S)-$(openssl rand -hex 3 2>/dev/null || head -c 3 /dev/urandom | od -An -tx1 | tr -d ' \n')" && cat > .claude/plan-review-loop.local.md << STATE_EOF
---
active: true
phase: locate
review_id: ${REVIEW_ID}
started_at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
target: (pending)
spec: (pending)
---

$ARGUMENTS
STATE_EOF
echo "Plan Review Loop activated (ID: ${REVIEW_ID})"
```

Update `phase:`, `target:`, and `spec:` in the state file as the loop progresses. If the session is interrupted and resumed, read this file to pick up where the loop left off.

## Phase 1 — Locate or Author

**If the argument is a file path:** that's the target plan. Read it fully.

**If the argument names an existing plan loosely** ("the migration plan"): search these locations, newest first:

- `docs/superpowers/plans/*.md` (superpowers writing-plans output)
- `docs/plans/`, `plans/`, `docs/planning/`
- `task_plan.md` at repo root (planning-with-files)
- `.kiro/specs/*/tasks.md`
- `PLAN.md`, `IMPLEMENTATION.md` at repo root or under `docs/`

**If the argument is a task with no existing plan:** author one first — follow the project's planning convention if one exists (for superpowers projects, the writing-plans structure: header with Goal/Architecture/Global Constraints, bite-sized tasks with exact Files/Interfaces/steps/commands), save it to the conventional location (default `docs/superpowers/plans/YYYY-MM-DD-<feature>.md`), then enter review. Write it as if it were final.

**Find the source spec.** A plan usually implements a spec or requirements doc (check the plan's own references, `docs/superpowers/specs/`, or ask the user). Record both paths in the state file. If no spec exists, note that in the state file — Lane 2 reviews grounding against the codebase only, and the missing spec itself becomes a finding candidate.

Set `phase: review`.

## Phase 2 — Independent Review

Pick a reviewer backend, in order of preference:

1. **Codex CLI** (if `command -v codex` succeeds): first ensure multi-agent is enabled by running this bootstrap verbatim (idempotent; identical to the original review-loop's):

   ```bash
   CODEX_CONFIG="${HOME}/.codex/config.toml" && if [ ! -f "$CODEX_CONFIG" ]; then mkdir -p "${HOME}/.codex" && printf '[features]\nmulti_agent = true\n' > "$CODEX_CONFIG" && echo "Created ~/.codex/config.toml with multi_agent enabled"; elif ! grep -qE '^\s*multi_agent\s*=\s*true' "$CODEX_CONFIG"; then if grep -qE '^\[features\]' "$CODEX_CONFIG"; then if [ "$(uname)" = "Darwin" ]; then sed -i '' '/^\[features\]/a\'$'\n''multi_agent = true' "$CODEX_CONFIG"; else sed -i '/^\[features\]/a multi_agent = true' "$CODEX_CONFIG"; fi; else printf '\n[features]\nmulti_agent = true\n' >> "$CODEX_CONFIG"; fi && echo "Enabled multi_agent in ~/.codex/config.toml"; else echo "Codex multi-agent: already enabled"; fi
   ```

   Then run `codex exec` non-interactively with the review prompt (one agent per lane, run in parallel, then consolidate), instructing it to write the consolidated review to `reviews/plan-review-<id>.md`. Cross-model independence, matching the original review-loop.

   **A hung Codex never exits — never wait on exit alone.** Codex can block on startup (auth refresh, dead network call) and burn an hour producing nothing. Three mandatory rules:

   - **Redirect, never pipe.** Launch in the background with output to a file — pipes (`| tail`, `| head`) buffer until exit and make a dead process indistinguishable from a working one:

     ```bash
     touch .claude/plan-review-codex-launch && codex exec <flags> "<prompt>" > .claude/plan-review-codex-run.log 2>&1 &
     ```

   - **Liveness probe at ~90s.** A healthy Codex writes a rollout file within seconds of starting a session. About 90 seconds after launch, check:

     ```bash
     find "$HOME/.codex/sessions/$(date +%Y/%m/%d)" -name 'rollout-*.jsonl' -newer .claude/plan-review-codex-launch 2>/dev/null | head -1
     ```

     No rollout file → the run is dead on arrival. Kill the process, log `backend=codex DEAD (no rollout within 90s)`, and fall back to backend 2 immediately.

   - **Watchdog.** Hard cap ~15 minutes total; also treat "run log unchanged for 5 consecutive minutes" as a hang (poll while waiting — do not idle to a stop). On either trigger, or if Codex exits without producing the review file: kill the process, log the failure, fall back to backend 2.
2. **Context-blind subagents** (fallback, always available): dispatch **three parallel subagents**, one per review lane. Each subagent's prompt must contain ONLY: the plan path, the source spec path (Lane 2), the repo root, its lane's criteria from `plan-review-dimensions.md`, and the finding format. Never include your planning reasoning or conversation history. Consolidate their findings yourself: deduplicate (keep the most detailed duplicate), sort by severity, write `reviews/plan-review-<id>.md`.

**The three review lanes** (full criteria in `plan-review-dimensions.md` — read it before dispatching):

1. **Zero-Context Executability** — role-play an engineer with no codebase knowledge executing the plan literally; flag every point where they'd have to guess
2. **Grounding & Traceability** — verify every referenced path/API/command against the actual repo; verify the plan covers its source spec completely and invents nothing beyond it
3. **Structure & Risk** — task granularity and ordering, dependency correctness, per-task verification, missing failure/rollback handling

**Finding format** (same shape as review-loop code findings):

```
- **[severity: critical|high|medium|low] [lane]** <task/step or line reference>
  <description of the problem>
  Suggested fix: <concrete, actionable rewrite or addition>
```

The review file ends with a summary: total findings, breakdown by severity, lanes run, and an overall verdict (`ready to execute` / `needs revision` / `re-plan against spec`).

Set `phase: addressing`.

## Phase 3 — Address With Judgment

Read the review file carefully. For each finding, **independently decide if you agree** — do not blindly accept every suggestion:

- **Agree** → revise the plan document directly.
- **Disagree** → do not change the plan; record why.
- Findings that change scope or contradict the spec's intent → surface to the user rather than deciding unilaterally.

Work critical and high severity first. **Before appending the disposition log**, decide whether a confirmation round is owed: if any critical finding is being FIXED, set `phase: confirm` in the state file first, so the stop hook knows the loop is not done at disposition time. If no critical finding was fixed, leave the phase at `addressing` (the hook treats disposition-in-addressing as completion). Then append the disposition log to the bottom of the review file:

```
## Disposition (<UTC timestamp>)
- Finding 1: FIXED — <one line on the change>
- Finding 2: SKIPPED — <one line on why>
- Finding 3: ESCALATED to user — <the question>
```

## Phase 4 — Confirm (conditional)

If any **critical** finding was fixed (i.e., the state file now says `phase: confirm`), run exactly one confirmation round: re-dispatch **one** fresh context-blind reviewer with the revised plan and the prior review file, asking only "are the critical findings resolved, and did the revisions introduce new problems?" The same backend rules apply, including the Codex liveness probe and watchdog — on backend failure, fall back to a subagent rather than skipping confirmation. Append its verdict to the review file as a `## Confirmation` section (the stop hook looks for this exact heading before allowing exit from the confirm phase). Do not loop beyond this single round.

## Phase 5 — Cleanup

Delete `.claude/plan-review-loop.local.md`. Report to the user: plan path, review file path, findings fixed/skipped/escalated, and the final verdict. If the verdict is `ready to execute`, suggest the appropriate execution route (e.g., superpowers:executing-plans or superpowers:subagent-driven-development for superpowers plans).

## Rules

- Keep the state file's `phase:` truthful at every transition — the stop hook enforces the loop through it (`locate`/`review` → review file required; `addressing` → disposition required; `confirm` → `## Confirmation` required) and fails open (abandons the loop) after repeated blocks with no progress
- Never pipe a reviewer process's output; redirect to a file and poll for growth — a pipe hides the difference between working and dead
- Log notable events (backend chosen, fallbacks, phase transitions, watchdog kills) to `.claude/plan-review-loop.log` as timestamped lines, matching the hook's format
- Complete the plan fully before entering review — no stopping mid-draft to "let the review catch it"
- Reviewers never see planning context; dispatch prompts are built from the documents and the dimensions file only
- Never fabricate findings or a review file — if the backend fails, say so and fall back
- The plan document is the single source of truth; all accepted fixes land in the plan itself, not in the review file
