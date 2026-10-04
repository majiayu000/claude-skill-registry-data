---
name: codex-exploration-loop
description: Use when Codex should explore a fuzzy, underspecified, or stubborn problem through bounded rounds rather than finish a known implementation. Triggers include time-boxed or round-count exploration, "try several directions", "keep attacking this unclear issue", surprising-design search, sandboxed brute-force investigation, branch exploration with subagents, or evidence-seeking loops inspired by Tree of Thoughts, Reflexion, or Voyager. Do not use for straightforward implementation, final cleanup, review-only tasks, credential setup, or high-risk external actions.
---

# Codex Exploration Loop

Run a bounded exploration loop for fuzzy work. The goal is leads, evidence, and a next decision, not pretending the problem is complete.

## Quick Start

1. Restate the fuzzy target as `question`.
2. Choose defaults when the user did not specify them:
   - `mode`: `standard`
   - `max_rounds`: `6`
   - `round_timebox_minutes`: `10`
   - `workspace`: current repo
   - `max_rounds` counts branch probe records, not fanout layers.
3. Gate risky actions:
   - Allowed by default: read/search, scratch edits, public network, local tests, local skills.
   - Ask first: destructive edits, paid/authenticated calls, credentials, commit/push, merge, production systems.
4. Initialize a run directory with `scripts/explore_ledger.py init`.
5. Choose the next frontier action; do not pre-plan all remaining rounds as fanout:
   - continue one active branch for one concrete probe;
   - fan out one selected branch when breadth is needed;
   - resume a strong parked branch when the newest fanout layer is low-yield;
   - run a critic checkpoint when the loop is about to over-commit to a weakly verified lead;
   - prune, pivot, promote, or stop.
6. For a single-branch round:
   - select a branch from `frontier.json`;
   - write `start-round`;
   - run one concrete probe;
   - write `finish-round` with evidence, score, reflection, and decision.
   - For scripted branch workers, use `prepare-worker`, run the generated `codex-exec.ps1`, then `finish-worker`.
7. For a Tree-of-Thoughts fanout layer:
   - create 3-5 candidate branches with `fanout`;
   - create per-branch Git worktrees with `prepare-worktree` before edit-heavy sibling probes;
   - explore them in parallel with native subagents or `codex exec` workers when authorized;
   - count each sibling probe as one round record;
   - import each branch result;
   - run `critic-checkpoint --after-beam` when one high-promise/low-evidence branch is about to dominate;
   - run `beam-select` to keep the best branches plus optional diversity.
8. After beam selection, deepen or split only the retained branches. If all new children are weak, run `next-frontier --include-parked` and resume the best earlier parked branch instead of forcing another probe into weak children. Do not restart every remaining round as another same-layer fanout.
9. Before `promote`, run a critic checkpoint or `codex-adversarial-qa` unless the user explicitly asked for a lightweight scout.
10. Stop when the round budget is used, a lead is promoted, all branches are blocked/pruned/parked, or the user redirects.
11. End with best leads, dead ends, parked branches, artifacts, and the recommended next lane.

## Modes

Scout:

- 3 rounds, 5 minutes each.
- Prefer read-only probes.
- No subagents unless the user explicitly asks.

Standard:

- 6 rounds, 10 minutes each.
- Use a scratch worktree for edit-heavy probes.
- Public network, local commands, local skills, and one independent branch worker are allowed when useful.
- If the user asks for breadth or ToT-style exploration, use fanout width 3 and beam width 2.

Bull:

- 10 rounds, 15 minutes each.
- Scratch worktree required for edits.
- Bounded subagents and branch fanout are expected at real expansion points when the problem has independent hypotheses.
- Default ToT settings: fanout width 4, beam width 2, diversity branch 1.
- Keep explicit gates for paid, authenticated, destructive, commit/push, and merge actions.

## Tree-of-Thoughts Fanout

Use ToT fanout when the user wants parallel exploration, there are several plausible hypotheses, or single-branch probing is likely to tunnel too early.

Round/layer relationship:

- A `run` contains one frontier and many round records.
- A `round` is one concrete probe on one branch.
- A `fanout layer` is an expand-collect-select event that creates sibling branches and usually consumes multiple round records, one per sibling probe.
- A `generation` is the sibling set created by one fanout layer.
- `max_rounds = 8` means up to eight branch probes total; it does not mean eight separate same-layer fanouts.

Layer cycle:

1. `expand`: write several branch hypotheses and probes.
2. `parallel probe`: dispatch independent branches through native subagents or schema-backed `codex exec` workers.
3. `evaluate`: import each branch result as a normal round record.
4. `beam select`: keep top-scoring branches and optionally one high-novelty diversity branch.
5. `critic checkpoint`: when selection would collapse too early, attack the lead and require a falsification or verification probe.
6. `iterate`: continue a retained branch, split a retained branch, compare retained branches, promote a lead, or stop.
7. `fallback`: if the latest sibling layer is low-yield, resume the best earlier parked branch from the global frontier.

Avoid this anti-pattern:

- Do not say "I will set 8 rounds and keep every round as same-layer parallel probing."
- Do not create fresh unrelated sibling sets after every round.
- Do not fan out again before the previous sibling layer has been collected and selected.
- Do not spend extra rounds on a weak newest layer just because it is newest; use the global frontier.

Use native subagents only when the user explicitly authorized subagents, parallel agents, delegation, or this skill's ToT fanout. The lead agent still owns context reading, branch prompts, scoring integration, and final recommendations.

## Round Discipline

Every round must produce a decision:

- `continue`: same branch deserves one more probe.
- `pivot`: same problem, different hypothesis.
- `branch`: split a promising alternative.
- `prune`: stop spending budget on this branch.
- `promote`: convert the lead into a completion/review task.
- `stop`: budget done or no useful next probe.

Reflection must be delta-oriented: say what changed, what failed, and what to try next. It is not enough to write a thoughtful paragraph; the reflection must either change `next_probe`, justify the score, or explain why the branch decision is still valid.

## Critic Checkpoints

Use critic checkpoints to prevent premature convergence on problems that need more thought, evidence, or verification. This is inspired by Tree-of-Thoughts self-evaluation/backtracking, Reflexion-style memory, Self-Refine feedback loops, LATS-style value updates with external feedback, and process supervision. Do not treat intrinsic self-correction as reliable by itself; require evidence, tests, counterexamples, source checks, or a concrete falsification probe.

Trigger a checkpoint when any of these are true:

- a branch is about to `promote`;
- the top branch has high `promise` but low `evidence`;
- the same branch receives two `continue` decisions without evidence gain;
- `beam-select` would leave only one plausible active lead while parked alternatives remain;
- two retained branches are close in score but imply different next actions;
- the user asked for deeper thinking, verification, red-team review, or avoiding early convergence.

A critic checkpoint must answer:

- what assumption makes the current lead fragile;
- what evidence would falsify or materially weaken it;
- which parked or challenger branch deserves comparison;
- whether to lower `promise`/`evidence`, raise `risk`, or add an `exploration_bonus` to a neglected challenger;
- the next concrete verification probe.

The checkpoint output must become a normal logged probe or controller event. Prefer a normal `finish-round` record when the critic runs tools, reads sources, or changes scores. Use `critic-checkpoint` only as a deterministic helper that recommends and optionally records that a critic round is needed. A checkpoint may lead to `continue`, `pivot`, `branch`, `prune`, or `promote`; do not introduce a new decision enum.

## Official Codex First

Use Codex mechanisms before custom harness code:

- AGENTS.md for repo policy.
- Codex skills for reusable workflows.
- Permission profiles, sandbox modes, and approval policy for boundaries.
- Codex app worktrees or Git worktrees for isolation.
- Native subagents for bounded independent branch scouts.
- MCP/connectors/web search for external tools.
- `codex exec` plus `schemas/round-result.schema.json` for scripted round workers.
- `run-plan` for v2.0 local runner orchestration over multiple bounded rounds.
- Codex automations or SDK/app-server only when the runner must be scheduled, resumed, or embedded outside the current Codex turn.

Do not rebuild Codex's model/tool loop, subagent pool, approval system, sandbox, or scheduler inside this skill.

## Resource Routing

Read only what is needed:

- `references/ledger-schema.md`: ledger files, JSON shapes, scoring, and recovery.
- `references/worktree-isolation.md`: scratch worktree and path-safety rules.
- `references/branch-operators.md`: branch decisions, scoring, and local-skill operators.
- `references/tot-fanout.md`: Tree-of-Thoughts fanout, subagent branch prompts, beam select, and safety rules.
- `references/official-codex-mechanisms.md`: when to use Codex skills, subagents, `codex exec`, automations, SDK, and MCP.
- `references/codex-exec-round-workers.md`: how to run schema-backed non-interactive branch workers.
- `references/automation-and-sdk-runner.md`: v2 guidance for recurring or programmatic runs.
- `references/runner-layer.md`: v2.0 runner plan, retry, and handoff contract.
- `prompts/lead-controller.prompt.md`: reusable lead-agent prompt skeleton.
- `prompts/round-worker.prompt.md`: reusable branch-worker prompt skeleton.
- `schemas/round-result.schema.json`: output schema for round records.
- `schemas/runner-plan.schema.json`: optional schema for runner plans.
- `scripts/explore_ledger.py`: deterministic run-dir, ledger, frontier, and digest helper.

## Minimal Commands

Initialize:

```powershell
python <skill-dir>\scripts\explore_ledger.py init `
  --root <workspace> `
  --root-label <public-or-short-label> `
  --slug <slug> `
  --question "<question>" `
  --max-rounds 6 `
  --round-timebox-minutes 10 `
  --mode standard
```

Start and finish a round:

```powershell
python <skill-dir>\scripts\explore_ledger.py start-round --run-dir <run-dir> --round 1 --branch-id b001 --timebox-minutes 10
python <skill-dir>\scripts\explore_ledger.py finish-round --run-dir <run-dir> --record-json <round-result.json>
```

Create and select a ToT fanout layer:

```powershell
python <skill-dir>\scripts\explore_ledger.py fanout `
  --run-dir <run-dir> `
  --parent-branch b001 `
  --candidate "Hypothesis A ||| Probe A" `
  --candidate "Hypothesis B ||| Probe B" `
  --candidate "Hypothesis C ||| Probe C" `
  --beam-width 2

python <skill-dir>\scripts\explore_ledger.py beam-select `
  --run-dir <run-dir> `
  --layer-id l001 `
  --beam-width 2 `
  --diversity-count 1
```

Summarize:

```powershell
python <skill-dir>\scripts\explore_ledger.py critic-checkpoint --run-dir <run-dir> --record
python <skill-dir>\scripts\explore_ledger.py next-frontier --run-dir <run-dir> --include-parked
python <skill-dir>\scripts\explore_ledger.py frontier --run-dir <run-dir>
python <skill-dir>\scripts\explore_ledger.py digest --run-dir <run-dir>
```

Prepare a v1.5 schema-backed `codex exec` worker:

```powershell
python <skill-dir>\scripts\explore_ledger.py prepare-worktree `
  --run-dir <run-dir> `
  --branch-id b001 `
  --repo-root <git-repo>

python <skill-dir>\scripts\explore_ledger.py prepare-worker `
  --run-dir <run-dir> `
  --round 2 `
  --branch-id b001 `
  --probe "Run the smallest useful probe for this branch." `
  --portable

& <run-dir>\artifacts\b001-round-002.codex-exec.ps1

python <skill-dir>\scripts\explore_ledger.py finish-worker `
  --run-dir <run-dir> `
  --worker-output <run-dir>\artifacts\b001-round-002.result.json
```

When `--workspace` is omitted, `prepare-worker` uses the active worktree recorded for that branch, then falls back to `scratch_worktree`, then the run root.

Use `--portable` for public or shared experiment artifacts; it copies the schema beside the worker files and avoids local absolute paths in the worker manifest.

Retire an isolated branch worktree after the lead has been promoted or abandoned:

```powershell
python <skill-dir>\scripts\explore_ledger.py promote-worktree --run-dir <run-dir> --branch-id b001
python <skill-dir>\scripts\explore_ledger.py retire-worktree --run-dir <run-dir> --branch-id b001
```

Run a v2.0 plan:

```powershell
python <skill-dir>\scripts\explore_ledger.py write-plan --run-dir <run-dir>

python <skill-dir>\scripts\explore_ledger.py run-plan `
  --run-dir <run-dir> `
  --plan <run-dir>\runner-plan.json `
  --max-rounds 3 `
  --digest
```

Runner modes:

- `mock`: deterministic schema-valid smoke, no model call.
- `replay`: import a pre-existing worker output.
- `external`: execute the generated `codex-exec.ps1` worker and import its result.

Use `mock` or `replay` for CI-like verification. Use `external` only when live Codex execution is acceptable and the workspace is isolated.

## Output

Final response:

```text
Exploration complete
- Budget used:
- Run dir:
- Scratch worktree:

Best leads
1. ...

Dead ends
- ...

Artifacts
- ...

Recommended next lane
- completion-loop / adversarial-qa / continue-exploration / human decision

Not done
- ...
```
