---
name: parallel-dispatch
description: Fires independent tasks in waves with a concurrency ceiling + sequential fallback on rate limit
---

> **Auto-Trigger:** When there are 2+ independent tasks (disjoint paths/domains) that can run in parallel
> **Keywords:** "parallel", "fan-out", "in parallel", "several at once", "dispatch", "waves", "batches"
> **Priority:** HIGH
> **Tools:** Task/Agent, Bash, Read

# parallel-dispatch — fan-out with a ceiling and a fallback

Generalizes `dispatching-parallel-agents` in a **portable, config-driven** way. Resolves the lesson "waves of ≤3 win where 8-16 blow up (server rate limit)".

## Contract

**INPUT:** list of independent tasks (disjoint scope); `concurrency.max_agents`/`concurrency.fallback` from `operator-profile.yaml`.

**OUTPUT:** the tasks' results, verified on disk (not the agent's "done" message); waves closed at a barrier.

**EXIT CODES** (from `${CLAUDE_PLUGIN_ROOT}/_lib/concurrency.py`, invoked in step 2 to read the ceiling):

| Exit | Meaning |
|---|---|
| 0 | ceiling/wave_size/fallback printed successfully (always — degrades to defaults without a profile) |

**STATE IT TOUCHES:**

| Resource | Reads/Writes | Purpose |
|---|---|---|
| `operator-profile.yaml` (`concurrency.*`) | Reads | ceiling, wave_size, fallback |
| stderr of the dispatched agents | Reads | detect rate limit (`is_rate_limited`) |
| each task's output on disk | Reads | real verification (step 6) |

## Process
1. **Confirm independence.** Only parallelize tasks with **disjoint scope** (paths/domains that do not overlap). If there is a sequential dependency or shared state, do NOT parallelize.
2. **Read the ceiling.** `python ${CLAUDE_PLUGIN_ROOT}/_lib/concurrency.py` prints `max_agents`/`wave_size`/`fallback` from `operator-profile.yaml` (default max_agents=3). Never exceed the ceiling.
3. **Group into waves** of size ≤ ceiling. Dispatch one wave, **only open the next when the previous one has closed** (barrier).
4. **Each task carries a contract:** objective + scope + **constraint not to touch files outside its scope** + return format.
5. **Fallback on rate limit.** If `is_rate_limited(stderr)` (matches "429"/"rate limit"/"quota"/"overloaded"), degrade according to `concurrency.fallback` in the profile — default `sequential-local`: finish the remaining tasks **sequentially and locally** (bash/directly), immune to the server's rate limit.
6. **Verify the return.** A delegated agent's "done" lies — confirm on disk/at the source (see `adversarial-refuter` / `delegate-with-handback`).

## When NOT to Activate
- Single task, or tasks with a sequential dependency / shared state.
- When the coordination cost exceeds the gain (2 trivial tasks).
- When the environment has no 2nd executor available.
- Just 1 delegation, with an individual handback → use `delegate-with-handback` (this skill is fan-out of N; that one is 1-to-1).

## Executed examples

```console
$ python ${CLAUDE_PLUGIN_ROOT}/_lib/concurrency.py
max_agents=3 wave_size=3 fallback=sequential-local signals=['429', 'rate limit', 'quota', 'overloaded']
```
<!-- executed: 2026-10-30 · exit=0 -->

```console
$ python ${CLAUDE_PLUGIN_ROOT}/_lib/concurrency.py --self-test
self-test OK
```
<!-- executed: 2026-10-30 · exit=0 -->

```console
$ python ${CLAUDE_PLUGIN_ROOT}/scripts/done_gate.py "python -m pytest -q"
  [FAIL] (exit 5) python -m pytest -q
        ^ no tests ran in 0.02s

DONE-GATE: NOT-DONE (0/1 criteria)
  no pending-work declaration. If this is PARTIAL, declare what is missing
  (--declare-partial "..."); if it is a FAILURE, fix it. Silence is not a state.
```
<!-- executed: 2026-09-24 · exit=1 -->
(step 6 — "a delegated agent's done lies": the gate confirms on disk and rejects when the criterion does not match.)

## Proof

```bash
python ${CLAUDE_PLUGIN_ROOT}/_lib/concurrency.py --self-test
```
