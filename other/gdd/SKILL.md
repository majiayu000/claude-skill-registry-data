---
name: gdd
description: >-
  Take a written repo goal through fresh authoring stages, PR review, operator-run gates and authorized merge, or
  resume from a saved stage ledger. Hand a bounded patch or review to a CLI agent with a written brief and isolated
  checkout; compare independent coding assistants in separate worktrees and check changes before integration.
metadata:
  revision: "35"
  areas: "software-development,work-management"
  targets: "runtime-agnostic"
  summary: "deliver a goal through staged authoring, gates and authorized merge, or verify one isolated CLI handoff without shipping"
  summary_zh: "用分阶段产出、门禁和授权合并交付目标，或单次委派给隔离的 CLI 并独立验收，不发布"
  kind: "controller"
  consumes: "goal-contract"
  produces: "chain-plan"
---

# Goal-driven delivery

In full delivery, an agent authors one written increment and the operator verifies and lands it.
**Done** is merged and the next goal branched from the merged head, not merely an open PR.

## When to Use

- "Start the next goal", "run the goal-driven flow", "finish this the usual way".
- 中文同义说法同样触发：`开始下一个 goal`、`推进 goal driven 流程`、`按老流程把这个做完`。
- Any multi-hour repo increment: a feature, a research-feasibility study, a migration, a docs
  rewrite — anything with a written completion contract and machine-checkable gates.
- A repo where the operator delegates end to end, including the merge.

Not for: one-line fixes, exploratory poking with no acceptance criteria, or work whose result no
machine can check.

## Lightweight delegation

For a bounded coding CLI handoff, read [lightweight delegation](references/lightweight-delegation.md).
Require a written brief, isolated Git worktree, explicit CLI and stop authority, and independent
acceptance. Stop on unsafe or out-of-scope work. No ledger, commit, push, PR, merge gate or merge.
The stages below apply only to full delivery.

## Stage order — fixed

```
contract → implement → verify → [simplify-report → apply] → code-review-report → fix
        → gates → PR → babysit → merge → reset
```

A dispatched two-phase step must close; simplify/apply is the one conditional pass (phase 3), review always
runs. Caps: `implement` 2 recovery attempts, `simplify` 2 rounds, `review→fix` 2 rounds. On a third round,
stop and report — do not burn budget in silence.

## Roles — authoring vs inspection

- **The agent authors**: product code, tests, docs, evidence records, applying simplify/review fixes,
  re-running measurements. Dispatch it; never type it yourself, not even a two-line fix.
- **The operator inspects**: reading diffs, running gates read-only, grading findings, deciding to
  merge, and the mechanical git work (commit, push, PR, merge, cleanup).
- Why: a hand-edit from the wrong surface is an unaccounted write — the diff can no longer be
  attributed to the agent that owns the code, and the next review cannot reason about it.

## Phase table — route, then read the detail

| Phase | Produces | Rules that must not be missed | Detail |
|---|---|---|---|
| 0 contract | a dispatchable goal contract | all six clauses: observable pass condition, judging artifact, failure control, out of scope, evidence plan, mergeable alone; one goal ≈ one run ≈ one PR; fix the contract, never dispatch and hope | [`references/phases/00-contract.md`](references/phases/00-contract.md) |
| 1 branch + dispatch | baseline snapshot and one implementation run | branch from `origin/main` and report the base SHA; report pre-existing dirty paths; settle the run plan once with `gdd.py setup` (ask the owner once, only for missing fields; never re-ask mid-run); `gdd.py stage` renders prompt, run name and ledger row from one template and refuses past a per-stage round cap or the plan's token cap, counting every dispatched run's launcher-reported usage (unknown when unreported) | [`references/phases/01-branch-dispatch.md`](references/phases/01-branch-dispatch.md) |
| 2 verify | gate evidence and a clause→test map | exit 0 means the process ended, not the phase finished; re-run gates on the FINAL tree; a proof test must fail when the feature is deleted; a weak proof test is its own increment | [`references/phases/02-verify.md`](references/phases/02-verify.md) |
| 3 simplify → apply | accepted fixes, or a recorded skip | conditional: skip a documentation-only, mechanical, or sub-threshold diff and record the reason in the ledger; report only, never silent apply; name rejected numbers in the apply prompt; a dead-code finding needs mechanical evidence; re-derive changed counts from the tree | [`references/phases/03-simplify-apply.md`](references/phases/03-simplify-apply.md) |
| 4 review → fix | per-finding fixes | run `gdd.py commit --no-push` before the next stage; reproduce every finding; classify regression vs pre-existing; a third same-class dispatch changes the mechanism | [`references/phases/04-review-fix.md`](references/phases/04-review-fix.md) |
| 5 commit → gates → PR | a sealed increment and its PR | run `gdd.py commit` to check the base and overlap, seal the index, verify the exact shipping SHA, run gates and push; re-derive every number on the final tree | [`references/phases/05-gates-pr.md`](references/phases/05-gates-pr.md) |
| 6 merge | a merge verdict, then the next branch | `--verified-head` is the SHA the gates ran on; bot marker `status: completed` with `commit_sha` matching the SAME head; no merge without the script's verdict | [`references/phases/06-merge.md`](references/phases/06-merge.md) |
| 7 ledger | one ledger row per stage | the operator writes it, never the agent; resume with `show` + `git status` + `git log origin/main..HEAD`; mid-flight status comes from live state | [`references/phases/07-ledger.md`](references/phases/07-ledger.md) |
| 8 reset | a fresh base for the next goal | fresh run, never a resumed session; delete merged branches; fork from freshly fetched `origin/main`; report the base SHA | [`references/phases/07-ledger.md`](references/phases/07-ledger.md) |

## Before you dispatch, and before you believe a run

Two references decide most failures. Read
[`references/cross-platform-increments.md`](references/cross-platform-increments.md) before writing a
verification plan for a repo that ships on more than one OS — a green local run is not evidence there.
Read [`references/run-failure-modes.md`](references/run-failure-modes.md) before adding a selftest case or
believing a run's report of itself: a test can kill the process under test, a stubbed test can pass for
the wrong reason, and an exit code can disagree with the artifact it produced.

## Stop conditions — when to stop and ask

- Red line touched: destructive/irreversible action, production, credentials, public release, or
  anything affecting a third party. Report impact + rollback + the exact action, then wait.
- Scope drift or write overlap: a non-empty `overlapping_paths`, sealed-scope drift after commit, or
  work outside the contract stops the loop; the operator decides which writer owns the path.
- Two attempts in one stage with no convergence (`BLOCKED:no_progress`): stop, keep the evidence,
  present the choice (different model / narrower contract / abandon).
- Unfair evidence: a "faster/cheaper" claim that does not survive
  [`references/evidence-fairness.md`](references/evidence-fairness.md) is not accepted as an outcome.
- The contract itself is wrong (ambiguous or contradictory requirements discovered mid-flight): stop,
  amend it, then continue. Never ask an agent to satisfy an impossible clause.

## Configuration

| Variable | Resolves | Default |
|---|---|---|
| `GDD_STATE_FILE` | ledger path | `${XDG_STATE_HOME:-$HOME/.local/state}/gdd/ledger.tsv` |
| `GDD_TASK_ROOT` | task/state root | `${XDG_STATE_HOME:-$HOME/.local/state}/gdd/tasks` |
| `GDD_RUN_ROOT` | launcher run root | `${XDG_STATE_HOME:-$HOME/.local/state}/gdd/runs` |
| `GDD_SKILLS_ROOT` | override the headless runner's route discovery root | lexical sibling skills root |
| `GDD_LAUNCHER`, `GDD_AGENT` | explicit launcher selection (custom launchers must accept `--schema`); install the selected headless route skill next to `gdd` | bundled `scripts/agent_run.py`, agent `omp` (`gdd-route-omp`); opt in to native Paseo with `scripts/adapters/paseo-run.py` |
| `GDD_RUN_DETACH` | detach mode: `auto`, `systemd`, `launchd`, `setsid`, `windows`, or environment-only `tmux` / `herdr` | `auto` (Linux user unit, macOS LaunchAgent, POSIX double fork, or native Windows) |
| `GDD_TEMPLATES` | stage-template root | the bundled `references/stage-templates` |
| `GDD_GOAL_GLOB` | goal-contract glob | `docs/goals/*<goal>*.md` |
| `GDD_GATES` | JSON array of gate commands for `gdd.py commit`, overridden by repeated `--gate`. Use POSIX quoting and forward slashes on every OS. Commands run in the repo root without a shell except for Windows batch shims. Quote the array as a scalar in the config file; stage prompts still accept a legacy plain-text environment value. | none (push refused without gates) |
| `GDD_RUN_PLAN_DEFAULTS` | JSON run-plan defaults that `gdd.py setup` merges under `--plan-file` ([phase 1](references/phases/01-branch-dispatch.md#run-plan)); per-stage round caps default to **2x**, `token_cap` to none; `--over-budget` overrides one dispatch | none |
| `GDD_WORKTREE_SCOPE` | `worktree-scope.py` path | `../delegated-work-acceptance/scripts/worktree-scope.py` |

`gdd.py` resolves these keys through `scripts/skill_config.py`; lookup order and the config path are in [references/configuration.md](references/configuration.md).
Run bundled scripts with `uv run <path>`. Only if a script command fails (for example `uv` is not
found), read [references/troubleshooting.md](references/troubleshooting.md).

Read [`references/transport.md`](references/transport.md) before selecting or dispatching a launcher:
it covers installed headless routes, native Paseo, artifact polling, and platform-specific evidence.
Native stages are Paseo agents and require a reachable daemon; never substitute routes by reachability.
Missing state/agents and an unreachable daemon are unknown, never success; headless evidence is not native evidence.
