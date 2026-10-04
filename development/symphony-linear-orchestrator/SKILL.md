---
name: symphony-linear-orchestrator
description: Bootstrap self-improving Symphony + Linear orchestration for a software repository. Use when Codex needs to inspect a repo, review or generate repo-local guidance, shape Linear issues, render a Symphony workflow, launch a high-leverage first execution wave, or run an orchestrator-led review, recovery, and learnings loop that makes future runs better.
---

# Symphony + Linear Orchestrator

Use this skill to onboard a repository for Symphony workers coordinated by an orchestrator and tracked in Linear.

## Roles

- The orchestrator inspects the repo, plans work, runs setup, and reviews results.
- Symphony dispatches workers.
- Workers execute bounded issues.
- Linear stores issue planning, dependencies, and review state.

## Required workflow

1. Inspect the target repo, current `AGENTS.md`, and any security or privacy constraints that workers must respect.
2. Run `scripts/doctor.py` to confirm the local toolchain and auth state.
3. Run `scripts/bootstrap.py` to render onboarding artifacts into the target repo's `.orchestration/` directory. Choose a lane deliberately, keep the first run conservative, and set workspace assertions that would catch a bad checkout quickly.
4. Merge the generated `AGENTS_ADDITIONS.md` content into the target repo manually. Do not let the script edit `AGENTS.md` for you.
5. Create Linear issues using the contract in `references/linear-contract.md` or render them from structured JSON with `scripts/issue_schema.py`.
6. Run `scripts/preflight.py` before starting any real run, then dispatch the wave: run your built Symphony binary against the rendered `.orchestration/<name>.WORKFLOW.md` (e.g. `symphony .orchestration/wave1.WORKFLOW.md --logs-root .orchestration/logs/wave1`; see the README quickstart and https://github.com/openai/symphony for build + exact flags). Symphony spawns one worker per active Linear issue.
7. Start with `max_concurrent_agents: 1` by default. Raise concurrency only after the repo baseline, issue boundaries, and review loop are proven.
8. When multiple workflows share one Linear project, use explicit routing labels such as `sym:small`, `sym:medium`, `sym:large`, and `sym:content`.
9. Keep the workflow's `campaign` metadata aligned with the worker prompt: the default mode is `orchestrator-review`, workers move completed issues to `In Review`, and the orchestrator integrates before moving issues to `Done`.
10. Treat `In Review` as the orchestrator gate. Review worker output, integrate the result, then move the issue to `Done`.
11. After each execution wave, update `.orchestration/RUNBOOK.md` and `.orchestration/LEARNINGS.md`, then promote stable learnings into `AGENTS.md`, the issue template, or workflow defaults.
12. Use the optional Release Manager lane only after workers reliably attach PR URLs and mark issues with `release:ready`. Keep it single-writer (`max_concurrent_agents: 1`) and dry-run it before using `--apply`. For high-volume parallel merges, verify a GitHub merge queue is enabled first (`scripts/release_manager.py --check-merge-queue`) so a burst of PRs batches instead of serializing, and re-run the lane to drain and finalize -- or render the scheduled GitHub Action sample (`bootstrap.py --with-release-manager`) to run that drain loop hands-off. See `references/release-manager-lane.md`.
13. For autonomous, goal-directed running (deciding the next wave from a goal, not just executing one wave), use the optional goal loop. Render it with `bootstrap.py --with-goal-loop`, init the budget ledger with `scripts/goal_state.py --init`, and have an orchestrator agent run the per-lap prompt (`.orchestration/goal-loop.PROMPT.md`). Every lap consults `scripts/goal_state.py`, which returns `continue`/`done`/`stuck` from real Linear state plus hard budget caps -- obey `stuck` and never code around it. Default posture is gated (the orchestrator reviews `In Review` and owns the merge); it flips to auto (via the Release Manager lane) or a per-label mix. See `references/autonomous-goal-loop.md` and `references/planner-lane.md`.

## Safety defaults

- Keep most work in `Backlog`.
- Activate only the first execution wave. Fill worker slots only after the workflow, issue contract, and review loop are behaving predictably.
- Do not auto-merge.
- Do not default to snapshot promotion or automatic PR creation.
- If enabling autonomous deploys, route them through the Release Manager lane; normal workers must not push, rebase, merge, or deploy `main`.
- Treat the autonomous goal loop as opt-in and capped. The budget ledger's caps (`max_laps`, `max_dispatched`, `max_planner_depth`, `max_wall_clock_minutes`) are hard stops, and a `stuck` verdict from `scripts/goal_state.py` always stops the loop and escalates to a human -- never override it. Do not enable auto-merge in the loop without real validation gates (required status checks or a merge queue) on the base branch. Keep planner recursion shallow.
- Do not introduce machine-specific background services into the target repo.
- Do not inherit the whole shell environment by default. Use an explicit Codex environment allowlist and add variables only when the workflow requires them.
- Do not put secrets, credentials, tokens, session cookies, personal data, or raw customer payloads into Linear issue bodies, workflow files, learnings, or worker comments.
- Treat anyone who can create or edit routed Linear issues as part of the trusted execution boundary.
- Prefer bootstrap assertions and no-progress guardrails over relying on operator intuition after a run has already gone wrong.
- Integrate validated worker output quickly so the dependency chain keeps moving.
- Do not leave repeated lessons trapped in chat or issue comments. Promote durable learnings into repo guidance.

## Reference map

- Read `references/orchestrator-model.md` when you need the operating model and role boundaries.
- Read `references/linear-contract.md` before writing issue bodies or dependency chains.
- Read `references/symphony-workflow.md` before rendering or editing a workflow.
- Read `references/release-manager-lane.md` before enabling autonomous PR merge/deploy flow.
- Read `references/autonomous-goal-loop.md` before running the goal loop for autonomous, goal-directed work; it covers the convergence/budget spine, the three layers, and the safety requirements.
- Read `references/planner-lane.md` before dispatching planners that shape the next wave; it covers the recursion fences.
- Read `references/repo-onboarding.md` when reviewing the target repo's `AGENTS.md` and local guidance.
- Read `references/recovery-playbook.md` when a worker stalls, clones the wrong branch, or drifts from validation.
- Read `references/self-improvement-loop.md` after each run when you need to convert operator observations into durable runbooks, learnings, and better defaults.
- Read `references/example-prompts.md` when you want prompt patterns for Codex or Claude Code.
