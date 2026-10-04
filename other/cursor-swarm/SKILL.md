---
name: cursor-swarm
description: "Fan out N parallel workers, drain them, and return one report. Use for /swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration."
---

## Codex adaptation

Open a visible four-phase todolist or Markdown checklist before launch: Frame, Fan out, Aggregate, Report. State the done predicate and output; choose partition, race, or mixed shape; declare the selection rule for a race; set total N, worker models, and separate writable outputs. Launch all N bounded native workers in parallel. Default to Work cloud only when its native worker route is available and the operator has authorized that destination. Use local workers when they need access to the user's computer. Otherwise report cloud unavailable without substituting local work. Each brief stands alone and requires PASS, ISSUES, or BLOCKED with evidence. Drain terminal results and return one compact aggregate with every required slice, issues, and explicit gaps or dropouts. A sequential fallback is not fan-out proof. The read-only two-slice local case and prior blocked worker outcome are in reports/pstack-swarm-four-phase-20260914.md and reports/pstack-thermos-swarm-real-20260914.md. Automatic selection and Work cloud parity remain unobserved.

# Swarm

Fan out N parallel native workers. Work cloud is the default only when its native worker route is available and authorized. Use local workers when they need the user's computer; never silently substitute local workers for unavailable cloud workers. They may cover separate slices, race the same brief, or mix both. The parent waits, aggregates, and returns one report.

## Start

Open a visible native todolist or Markdown checklist with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Set N from the user or derive it from the shape. N is total workers, not the cloud concurrency limit.
4. Pick the worker model and effort from the standing `model-capability-router` and the target channel's advertised inventory. Preserve an explicit operator selection. For a model race, name each arm's model and effort up front; do not invent unavailable Cursor slugs.
5. Give each worker its own writable output when it writes. When workers verify or measure commits, each brief names the exact SHAs. A measurement brief also names the method (sample count, what one sample is, order). The worker records both in its result.

## Phase B: Fan out

Launch all N bounded native workers in parallel with the selected model/effort and standalone briefs. Default to Work cloud only when its native worker route is available and authorized. Use local native subagents when the workers need access to the user's computer; otherwise report cloud unavailable rather than substituting local work.

When a worker must start from a non-default pushed branch, give the exact verified branch/ref in its brief and use a native branch-start option only if that worker channel documents one. Do not invent `cloud_base_branch` support.

Every brief stands alone. Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence. A worker that can prove a defect reports `ISSUES` and lists every issue it can prove, not only the first.

If a worker drops out, proceed with N-1 and note it.

## Phase C: Aggregate

Read the terminal results. Drop a result that does not record the SHAs and method its brief names, and rerun that worker once. After a second miss, record a gap. A gap does not count as a pass. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

Keep a compact result table, one-line evidenced issues, and explicit gaps or dropouts.

## Phase D: Report

Return one consolidated in-chat report with the table, issue one-liners, gaps or dropouts, and the race rule when used.
