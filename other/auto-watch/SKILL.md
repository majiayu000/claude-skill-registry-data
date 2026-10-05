---
name: auto-watch
description: >
  Render the live auto agent tree — driver → work step → do_step fan-out agent —
  with each node's age against its stall threshold and its attempt count, then
  overlay live-agent status from the harness. Use when the driver or operator
  wants to SEE what a run has dispatched, what is nested under a fan-out step, and
  which node is wedged or over-age vs the stall threshold — "watch the tree",
  "show the agent tree", "what's dispatched", "is anything hung". Structure comes
  from the run-record via lib/watch_tree.py; liveness comes from the TaskList/Monitor
  task tools. It renders a view — it does NOT reap, retry, or escalate (that is
  the driver's supervision policy in skills/auto/SKILL.md §4).
---

# auto-watch (the agent-tree watch view)

A legible, at-a-glance picture of a live auto run's agent tree: the driver, the
work steps it dispatched, and the `do_step` fan-out agents nested under their
producer parents — each annotated with how long it has been in flight against its
stall threshold and which attempt it is on. Its purpose is supervision *legibility*
(R6, AE5): surface a wedged or dead node — top-level or nested — as a distinct,
over-age node so the driver's reap→retry→escalate policy (`skills/auto/SKILL.md`
§4) has something to act on.

Two halves, deliberately split (KTD5):

- **Structure + age — from the run-record, deterministic.** `lib/watch_tree.py`
  reads the run's run-record and renders the tree: declaration order, `do_step`
  children nested under the parent they depend on, dispatched nodes annotated
  `age=Ns/Ts` with an `OVER-AGE` flag past threshold and `attempt=K`. Pure and
  byte-deterministic (`now` is passed in), so the same run-record always renders the
  same tree.
- **Liveness — from the task tools, model-side.** Nested `do_step` agents carry
  their OWN `session_id` and are not reachable by the run-record alone, so overlay
  their live process status from `TaskList` / `Monitor`, mapping each task back
  to its step id.

## Render the tree

Resolve the run's repo + run-id (the driving session's run-record), read the run-record,
and render it with the current time as a pinned ISO-8601 `now`:

```
python3 - "$RUN_ID" <<'PY'
import sys, os, datetime
sys.path.insert(0, os.path.join(os.environ["CLAUDE_PLUGIN_ROOT"], "lib"))
from _bootstrap import load_run_record, load_lib_module
run_record = load_run_record()
watch_tree = load_lib_module("watch_tree")
run_id = sys.argv[1]
repo = os.environ.get("CLAUDE_AUTO_REPO") or os.getcwd()
led = run_record.read_run_record(repo, run_id)
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
print(watch_tree.render_agent_tree(led, now))
PY
```

`render_agent_tree(run_record, now)` returns a multi-line string:

```
agent-tree: <run-id>

  • plan  [verdict-returned]
    • build-clarity  [dispatched age=3600s/600s OVER-AGE attempt=2]
    • build-perf  [dispatched age=60s/600s attempt=1]
  • compare  [pending]
```

`now` is passed IN — never let the renderer read the clock. That keeps the view
pure so a fixed run-record renders identically for the same instant (the property its
determinism test pins). A run with nothing dispatched renders the empty-tree
sentinel (`(no dispatched steps)`) — there is no live agent to watch yet.

## Overlay live-agent status

The run-record shows what the run BELIEVES is dispatched; the task tools show what is
actually alive. Overlay them so a node the run-record still calls `dispatched` but
whose agent has died (or wedged) is visible:

1. Call **`TaskList`** for the run's dispatched agents. Nested `do_step` agents
   carry their own `session_id`, so map each task back to its step id (by the
   step id baked into the dispatch, per `skills/auto/SKILL.md` §4 / KTD-5).
2. For a node the run-record calls `dispatched` but that has no live task — or one
   `TaskList`/`Monitor` reports finished/dead — call it out next to the run-record
   node: the two disagree, which is exactly the alive-but-wedged / silently-dead
   signal the watch view exists to surface.
3. A node flagged `OVER-AGE` by the renderer is past its stall threshold — the
   timeout-watchdog case — regardless of what the task tools say.

See `references/live-overlay.md` for the run-record-state ↔ task-liveness mapping.

## What this skill does NOT do

- It does not reap, retry, or escalate. It renders a view; the driver acts on it
  via the supervision policy in `skills/auto/SKILL.md` §4 (reap the live agent,
  `auto-resume.py retry`, and pause-escalate at attempt N=2). Keeping watch
  read-only is deliberate — one place decides, one place shows.
- It does not mutate the run-record — no write path, no `now` from the clock inside
  the renderer.
- It does not re-derive the exit predicate or the stall threshold; it reads the
  per-step `stall_threshold_seconds` the run-record already carries (default 600).
