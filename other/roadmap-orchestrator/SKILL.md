---
name: roadmap-orchestrator
description: One bounded roadmap-advance tick — dispatch ready packages, dual-gate PRs (CI + serialized local hardware test), auto-merge, write the daily standup. Cron-driven via Windows Task Scheduler (opencode run).
invocation: /roadmap-orchestrator
---

# /roadmap-orchestrator [--dry-run]

Implements `.astroray_plan/docs/2026-05-16-roadmap-orchestrator-design.md`. One
invocation = one bounded tick. Recurrence comes from a `/schedule` cron routine,
never from looping in-session.

## Step 0 — Guards
1. `cd` to the canonical repo path; `git rev-parse --show-toplevel` to confirm.
2. `git fetch origin`; confirm on `main`, up to date.
3. Stale-`.pyd` scan (reuse `pkg-ship` Step 0 PowerShell scan). Abort tick on shadow `.pyd`.
4. Acquire the tick lock: `acquire_lock(".astroray_plan/.orchestrator.lock", 1500)` returns `True` if the lock was acquired (proceed) or `False` if a live (non-stale) lock is already held by a running tick. **If it returns `False`, exit now** — do not run an overlapping tick. On `--dry-run`, skip lock acquisition entirely.

## Step 1 — Compute the tick plan (decision engine)
Determine `eligible_packages`: from `NEXT_STAGE_REPORT.md` §2, the ready packages
(not research-only, deps merged, no open PR, no active worktree, dispatchable Track) —
this is exactly `dispatch-next`'s eligibility logic; reuse it. **Also exclude any
package already recorded in `ledger.get("impl_dispatches", {})` with a non-terminal
outcome (e.g. `"dispatched"`) — those are already in flight; do NOT re-dispatch them.**
Count `in_flight` (active worktrees + running implementer agents).

Run:
```
python -m roadmap_orchestrator.cli \
  --ledger .astroray_plan/.orchestrator-state.json \
  --next-stage-report .astroray_plan/docs/NEXT_STAGE_REPORT.md \
  --eligible <comma-joined eligible_packages> --in-flight <n> \
  [--dry-run]   (pass --gpu-lock-free only if the GPU lock is free)
```
GPU-lock-free is decided via `lock_status(.astroray_plan/.orchestrator.gpu.lock, 5400)`.
Parse the JSON: `plan.dispatch`, `plan.fixers`, `plan.hw_dispatch`, `plan.merges`,
`plan.hw_failed`, `standup_md`.

**If `--dry-run`:** print the plan + `standup_md`, do nothing else, exit. (No lock,
no spawn, no merge, no build, no file write.)

Note: `cli.py` always emits the plan JSON and performs **no** side effects itself; the `--dry-run` flag is only echoed back as `dry_run: true` in the JSON and is the SKILL's own signal to stop after printing. All side effects (Step 2/3) are performed by this SKILL, never by the CLI.

## Step 2 — Execute side effects (live only)
In this order, respecting caps already applied by the engine:

1. **Dispatch** each pkg in `plan.dispatch` via `dispatch-next` routing
   (`package-implementer` in its own fresh worktree; Codex is supported again
   (2026-09-05) as a CLI second-opinion reviewer (Terra/Luna via `codex exec`),
   never as an implementer or orchestrator, so legacy Track-E / Codex-paste-ready
   specs remain inert and route here too) with the
   NEXT_STAGE_REPORT §3 drop-in prompt verbatim. **Record the dispatch BEFORE
   spawning:** `ledger.setdefault("impl_dispatches", {})[<pkg>] = {"outcome":
   "dispatched", "ts": <now>}` then `save_ledger(...)` — this is what stops the
   next tick from re-dispatching the same package. **If an isolated worktree cannot
   be created, abort that dispatch** (and set the entry outcome to
   `"escalated:worktree"` so it surfaces in the standup) — never fall back to `main`
   (memory `parallel_agent_worktree_contamination`). After spawning, re-check
   `git rev-parse main` == Step-0 value; if it moved, halt dispatch and write a
   `CONTAMINATION` Action item.
2. **Fixers** — for each `plan.fixers` (each is `{"pr": n, "kind": "rebase"|"ci"}`): `kind=="rebase"` → rebase-fixer on that PR's branch worktree (rebase `origin/main`, push); `kind=="ci"` → `gate-failure-reviewer` (which now produces a root-cause analysis + routes a fresh `package-implementer` to draft a fix + requires a different-model sign-off on the proposed fix before push — see `gate-failure-reviewer.md` § Deliverables). The fixer is **not pushed for re-gate** without a recorded `indep_review:SIGN-OFF`; a `BLOCK` verdict halts the push and writes an Action item to the standup. Then `record_action(ledger, <pr number>, "rebase_dispatched"|"ci_dispatched"|"indep_review:SIGN-OFF"|"indep_review:BLOCK")` (signature: `state.record_action(ledger, number, action)`).
3. **Hardware gate (strictly serialized, asynchronous across ticks — design spec §2a).** `plan.hw_dispatch` is either `null` or a single **PR number** (int), not a dict.
   a. **Read back a finished result first.** Check `lock_status(".astroray_plan/.orchestrator.gpu.lock", 5400)`. If the GPU lock is held and its dispatched `hardware-verifier` job for that PR has finished, call `record_hw_result(ledger, <pr number>, <head_sha>, "PASS"|"FAIL", <numbers>, <artifact path>)` (signature: `state.record_hw_result(ledger, number, head_sha, result, numbers, artifact)`), then `release_lock(".astroray_plan/.orchestrator.gpu.lock")`.
   b. **Dispatch a new job only if the slot is free.** If `plan.hw_dispatch` is not `null` AND the GPU lock is free: look up that PR's `headRefOid` and `headRefName` from `gh pr view <plan.hw_dispatch> --json headRefOid,headRefName`; resolve the PR's worktree path (`.claude/worktrees/<pkg>` from the branch name, verified via `git worktree list`); `acquire_lock(".astroray_plan/.orchestrator.gpu.lock", 5400, meta={"sha": <headRefOid>})`; if acquired, dispatch the local hardware build+test via the `verify` skill / `hardware-verifier` on that PR's branch worktree, passing the worktree path + `headRefOid` + PR number + spec path + newest binding **as a background job — do NOT block the rest of this tick waiting for it** (a CUDA build+render runs far longer than the 10-min tick cadence; its result is read back by a later tick via step (a)). The HW build runs the PR's own worktree at its head SHA via the vcvars-bootstrapping wrapper; never `main`; Step-0 stale-`.pyd` hygiene and single-CUDA-job serialization are unchanged. **Exactly one GPU/CUDA job ever** — never start a second while this lock is held (memory `cuda_verifier_concurrency`). Never auto-run the full closeout sweep.
4. **Merges** — for each `plan.merges`: **if the PR's package is non-HW-gated** (Track A addon/orchestrator/engine plumbing / docs-with-code — no HW/render acceptance gate), dispatch one independent different-model pre-merge code review of the PR diff against the package spec's acceptance criteria **before** invoking `pr-reviewer`. Verdict is `SIGN-OFF` or `BLOCK`:
   - `SIGN-OFF` → proceed to `pr-reviewer` (which still runs its full checklist; the independent review is additive).
   - `BLOCK` → do **not** invoke `pr-reviewer`; write a standup Action item (PR number, the integration/logic gap named by the reviewer) and route a `gate-failure-reviewer` / fresh-implementer pass. The PR is not merged this tick.
   
   **If the PR's package is HW/render-gated** (has a HW/render acceptance gate in its spec — the empirical RTX visual gate is its real backstop), **skip** the independent review and proceed directly to `pr-reviewer` exactly as today. The `pr-reviewer` agent's checklist self-escalates and STOPS on gate/license problems. It only auto-merges a PR that is `mergeable` + CI all-pass; the engine already confirmed hardware `PASS` bound to the current head SHA.
   
   **Pure-docs PRs** (diff touches only `*.md` and `.astroray_plan/`): the existing `pr-reviewer` doc-only fast path is preserved; no independent review is dispatched (keeps the gate minimal).
5. **HW-failed / Action items** — for each `plan.hw_failed`: dispatch `gate-failure-reviewer` on the local failure artifacts (which now produces a root-cause analysis + routes a fresh `package-implementer` to draft a fix + requires a different-model sign-off on the proposed fix before push — see Step 2.2 and `gate-failure-reviewer.md` § Deliverables). A HW `FAIL` is never overridden automatically; the fix is **not pushed for re-gate** without a recorded `indep_review:SIGN-OFF`. Then `record_action(ledger, <pr number>, "gate_review_dispatched")` to debounce re-dispatch (memory `orchestrator-hw-failed-no-debounce`).

## Step 3 — Standup + close out
1. `finalize_previous(.astroray_plan/docs/standup, <today>)`.
2. `upsert_standup(.astroray_plan/docs/standup, <today>, plan, gpu_holder, hw_queue, ledger)` (pass ledger to surface independent-review verdicts in standup).
3. `expire_closed(ledger, open_numbers)` where `open_numbers` is a Python `set` of int PR numbers from the `gh pr list`; then `save_ledger(".astroray_plan/.orchestrator-state.json", ledger)`.
4. `release_lock(.astroray_plan/.orchestrator.lock)` (also release on every abort path).

## Step 3 — Standup + close out
1. **Safe merged-worktree auto-GC (live path only; never under `--dry-run`).**
   Call `gc_merged_worktrees(".claude/worktrees", ledger)` (signature: `state.gc_merged_worktrees(worktrees_dir, ledger) -> dict`).
   Returns `{"removed": [...], "escalations": [...]}`.
   This safely removes worktrees + branches for PRs that are (a) MERGED on GitHub, (b) content in `origin/main` (squash-aware), (c) zero uncommitted/unpushed changes.
   Anything not provably safe is escalated, never force-deleted. Design: pkg97 § Phase 1.
2. `finalize_previous(.astroray_plan/docs/standup, <today>)`.
3. `upsert_standup(.astroray_plan/docs/standup, <today>, plan, gpu_holder, hw_queue, merged_today, gc_report, ledger)` where `merged_today` is the list of PR numbers merged today (from `_get_merged_today()`) and `gc_report` is the GC report from step 1.
4. `expire_closed(ledger, open_numbers)` where `open_numbers` is a Python `set` of int PR numbers from the `gh pr list`; then `save_ledger(".astroray_plan/.orchestrator-state.json", ledger)`.
5. `release_lock(.astroray_plan/.orchestrator.lock)` (also release on every abort path).

## Model routing (authority lives in agent frontmatter, not this body)

Per-agent model assignments live in the agent frontmatter — `.opencode/agents/*.md`
(opencode, primary) and `.claude/agents/*.md` (Claude Code, fallback) — plus the
delegate tiers in `.claude/skills/delegate/config/tiers.json`. **Never hardcode a
model id here.** The tick's own session runs on a cheap open-weight model; every
judgment-heavy step below carries its own agent + model via its frontmatter.

**Independent sign-off (Steps 2.2, 2.4, 2.5):** the independent review of implementer
output MUST be produced by a different lineage than the drafter. Dispatch the `sign-off`
agent (which runs `claude -p` — Claude Code, a different provider than the open-weight
drafter) with an adversarial prompt. The verdict is `SIGN-OFF` or `BLOCK`. Failing to
dispatch the `sign-off` agent silently defeats the rule. BLOCK halts the push (see
`gate-failure-reviewer.md`).

**Outside-eye pre-pass (cheap, additive, non-authoritative):** before the sign-off at each
of the three sites, run
`python .claude/skills/delegate/scripts/delegate.py --tier verify --agent critic
--prompt "..."` on the same diff/spec. Its findings are LEADS, never a verdict — fold
them into the `sign-off` prompt (e.g. "a cheap first pass flagged: <findings>; weigh and
verify before your SIGN-OFF/BLOCK"). The critic pass never itself produces SIGN-OFF/BLOCK
and never blocks a merge on its own; if opencode/the model is unavailable, skip it
silently and proceed straight to the `sign-off` review — it's a bonus signal, not a
dependency.

## Safety rails (non-negotiable — see design spec §5)
- One tick at a time (tick lock); one CUDA job at a time (GPU lock).
- Per-package isolated worktree or abort — never `main`. `main` mutated only by `pr-reviewer`.
- The HW build runs the PR's own worktree at its head SHA via the vcvars-bootstrapping wrapper; never `main`; Step-0 stale-`.pyd` hygiene and single-CUDA-job serialization are unchanged.
- Implementer cap 2 / fixer cap 1 (enforced in the engine).
- Auto-merge requires BOTH CI all-pass AND head-SHA-bound hardware `PASS`. A HW `FAIL` blocks merge + escalates.
- **A gate-failure fix (CI or HW) is never pushed for re-gate without a recorded different-model SIGN-OFF; BLOCK halts the push.** (pkg98)
- **Non-HW-gated packages get one independent different-model pre-merge code review before `pr-reviewer`; HW-gated packages skip it** (the empirical HW visual gate already covers them). (pkg98)
- `--dry-run` = zero side effects.
- **Worktree/branch GC is merged-only, never force-delete on doubt.** Only PRs with `state == "MERGED"` AND content in `origin/main` (squash-aware) AND clean worktree are removed. No staleness/age heuristic. Escalate all ambiguous cases as Action items (pkg97 § Phase 1 hard invariant).

## Recurrence (Windows Task Scheduler, not /schedule)

opencode has no built-in cron. Recurrence is a Windows Task Scheduler task
(`Astroray-RoadmapOrchestrator`) that runs `scripts/orchestrator_tick.ps1 -Driver opencode`
every 10 minutes, which pins the environment + PATH and invokes
`opencode run -m opencode-go/deepseek-v4-pro "Run the roadmap-orchestrator skill —
one bounded tick."`. The tick lock makes exact firing time immaterial.

**Pause/stop:** `schtasks /change /tn Astroray-RoadmapOrchestrator /disable` (or
`/enable`). Disable it during `team-overnight` runs to avoid a second driver.

The standup is updated every tick and finalized on day rollover, so no separate daily
cron is needed.
