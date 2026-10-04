---
name: marshal-benchmark
description: >
  Compare AI coding strategies on a real task with Marshal: run the same goal through several
  configured clients (e.g. a premium model vs a cheaper one) and get a measured cost/latency/outcome
  comparison. Use when you want evidence for which provider/model to route a kind of work to, or to
  prove what a cheaper strategy actually saved. Honest by construction - it measures, it never guesses.
---

# Benchmarking routing strategies

Marshal's differentiator is **proving** what a routing choice costs, with measured numbers - not a
fixed % claim. A *strategy* is a configured client (a backend + model + permission combo). This
playbook runs one goal through N strategies and compares them.

## Run it
1. `list_clients` - pick the strategies (client names) to compare, e.g. a premium worker vs a cheap
   one, both capable of the task.
2. `benchmark(goal, clients, task_id?, max_concurrency?)` - runs the **same goal** through each client
   in parallel (each in its own worktree), then returns a comparison:
   - `strategies[]` - per client: `status`, `cost_usd`, `source`, `duration_ms`, tokens, `run_id`.
   - `cheapest` / `fastest` - the winning client, but **only among strategies that succeeded and have
     a known cost**. A strategy whose cost is `unavailable` never wins "cheapest."
3. `report(task_id)` re-derives the same comparison later from the ledger (read-only) - reproducible
   and auditable.

> **Multi-workspace:** `benchmark` and `report` are scoped to one workspace, and `task_id`s are
> per-workspace. If you benchmark with `workspace=<name>`, pass the **same** `workspace` to
> `report(task_id, workspace=<name>)` - otherwise it reads the wrong repo's ledger and finds nothing.

## Read it honestly
- Check `source` on each row. `native` = the backend reported the cost; `admin-api` = the **real**
  charge read back from a provider usage API (e.g. EastRouter); `unavailable` = unknown (e.g. Cursor
  without the Admin API, or a token-only Codex run). Never read an `unavailable` `$0` as free.
- The benchmark measures cost, latency, and outcome **status** - not correctness. A cheapest strategy
  can still produce worse code. Review the diffs (`collect_run`) before drawing conclusions.
- `empty` / `failed` / `verify_failed` strategies still cost tokens; they appear in per-run cost but
  are excluded from `cheapest` / `fastest`.

## What to do with the result
- Route future work of this kind to the strategy with the best cost/quality trade-off (the cheapest
  one that also produces correct diffs).
- To keep a strategy's output, `integrate` its `run_id` (see **marshal-orchestrate**).
- The historical record of what each strategy cost - derived on read, never a stored guess - is the
  defensible asset. Build it up over real tasks rather than promising a universal savings number.
