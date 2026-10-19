---
name: watch-and-monitor-with-poller
description: Use when monitoring Crewrift evaluations, rounds, or rankings across turns with a persistent poller.
---

# Watch and monitor with a poller

The crewrift watch loops (crux-battery polling, "re-sweep every new round", "tell me when daveey hits
#1 in Wood") all share one failure mode and one fix. Read this before you launch any standing watch.

## The rule (and the one exception)

- **Multi-cycle / long-lived poll → use the `Monitor` tool**, arming it with the poller command
  directly. Monitor is harness-managed: it streams the poller's stdout back as events and keeps the
  command alive for the whole session. Each printed line becomes a notification.
- **A bare `bash run_in_background` with an in-shell `for ...; do <work>; sleep 900; done` DIES after
  the first cycle.** The harness keeps a launched *command* alive, but a long in-shell `sleep` inside a
  detached wrapper script gets reaped before the next iteration. Observed twice: the crux-scout poller
  (`tmp/crux/scout/poll_scout.py`) and a recon-sweep `watch_loop.sh` both logged cycle 1, hit the
  `sleep`, and vanished from `ps` with a 0-byte output file — arms completed server-side but no verdicts
  were harvested and no error surfaced. (session-derived, unverified)
- **Exception — a single "tell me when X finishes" wait** that exits in seconds is fine as
  `bash run_in_background` with `until grep -q DONE <log>; do sleep 30; done`. The reaping only bites
  the long-lived *multi-cycle* loop, not a short wait that terminates on its own. (session-derived,
  unverified)

## Reference tool

`universal/tools/monitor.py` is the canonical poller shape: a `while True:` loop that snapshots the
Observatory league/leaderboard via `httpx`, prints a line **only on a meaningful change**, and
`time.sleep(900)` between cycles. It is the thing you arm `Monitor` with. Copy its structure for a new
watch; only the snapshot body and the change-detection differ.

## Recipe: launch a standing watch

### 1. Write a poller that is idempotent and emits one line per genuinely-new event

The poller must (a) hold its own "already seen" state and (b) print only on change, so every Monitor
event is real signal and not a per-tick repeat.

For a league/leaderboard watch, the snapshot is an authenticated Observatory call. The auth + base-URL
pattern (from `monitor.py`):

```python
import time, json, sys, httpx
from softmax.auth import get_api_server, load_current_cogames_token

def snapshot():
    server = get_api_server()
    token = load_current_cogames_token(api_server=server)
    H = {"X-Auth-Token": token}
    base = f"{server.rstrip('/')}/observatory"
    # GET /v2/division-leaderboards/{DV}  -> rows under "entries"/"rows"/"results"
    # GET /v2/rounds?league_id=...&limit=30 , then GET /v2/rounds/{id} for results
    ...
    return state

def main():
    prev = None
    while True:
        try:
            cur = snapshot()
            if cur != prev:        # gate: only print on change
                print(f"... {cur} ...", flush=True)
            prev = cur
        except Exception as e:     # noqa: BLE001 — deliberate poll-error guard, see below
            sys.stderr.write(f"poll error: {e}\n")
        time.sleep(900)           # 15-min cadence for league rank; tighten for a battery

if __name__ == "__main__":
    main()
```

Constants you will need (from `monitor.py`, current as of 2026-06-12 — re-verify the ids if the league
rolled):
- Wood league id: `league_605ff338-0a2e-4e62-aeda-559df9a9198f`
- Wood division id: `div_c2be3343-f046-4c21-8674-267b5797a059`

For a **crux/experience-request battery** the snapshot is instead
`GET /v2/experience-requests/{xid}` per arm, checking episode statuses; gate the print on the NEW-count
(emit only when an arm reaches a terminal `completed`/`failed` status you have not yet reported). Keep a
seen-set on disk (e.g. `tmp/crux/recon/seen_rounds.json`) so a re-run does not re-announce old events.
(session-derived, unverified)

The **one allowed `try/except`** is the poll-error guard around the snapshot: a transient API hiccup
must not kill a multi-hour watch. This is the single deliberate exception to "let it crash" — keep it
narrow (wrap only the network call, log to stderr, continue the loop). Do not wrap anything else.

For the stdout filter when arming Monitor, use a grep that surfaces both verdicts and crashes, e.g.
`grep -E "TEST |BATTERY DONE|Traceback|Error|rank=|NEW "`. (session-derived, unverified)

### 2. Validate the poller runs before arming Monitor

The harness `_harness` / poller code runs with **unittest, not pytest** (pytest is not a project
dependency). If you wrote or touched a `_harness` test for the poller, run it with:

```bash
uv run python -m unittest discover -s _harness -p "test_*.py"
# or, for a single module (imports siblings, so it needs _harness on sys.path):
PYTHONPATH=_harness uv run python -m unittest <bare_module_name>
```

Do a one-shot smoke of the poller itself (let it print one cycle, then Ctrl-C) to confirm auth resolves
and the snapshot parses — before committing it to a long Monitor run.

### 3. Arm Monitor with the poller as its command

Use the `Monitor` tool (search its schema with ToolSearch `select:Monitor` if it is not yet loaded).
Arm it with the poller invocation as the command and the grep filter above, with an until/while
condition matching your terminal signal (e.g. until the battery prints `BATTERY DONE`, or run open-ended
for a rank watch). Monitor streams each printed line back to you as an event and survives the session.

## Gotchas

- **Do NOT poll a long watch with `Bash` `run_in_background` + foreground `sleep`.** It is reaped after
  cycle 1, silently. This is the whole reason this skill exists. (session-derived, unverified)
- **If the Monitor goes quiet longer than ~20 min, sanity-check the arms directly.** For a battery, hit
  `GET /v2/experience-requests/{xid}` and read episode statuses; the arms may have reached terminal
  server-side while the poller exited early. The poller writes `*_results.json` incrementally, so if it
  did exit you can re-run it once arms are terminal and harvest verdicts from disk. (session-derived,
  unverified)
- **Re-verify league/division/policy ids and live roster right before launch.** The league rolls policy
  versions and may roll league/division ids mid-session; a hardcoded id from a prior run can be stale.
- **Dashboard staleness is a separate trap, not a poller problem.** If you are *also* watching the local
  `_harness/dashboard.py` dev server (port 8765) and it shows missing/stale runs: the run index
  (`league_runs.json`) is **per-checkout** — an instance launched from an old worktree knows nothing
  about runs submitted elsewhere. Check which checkout the live instance was launched from, kill stale
  instances (including another agent's port-squatter), and restart from the current checkout. The
  single-file HTML/JS is rendered once at server boot (render.py), so any frontend change needs a server
  restart before the browser reflects it. (session-derived, unverified)

## Success check

- The Monitor is running and has emitted at least one event (or you have confirmed via a one-shot smoke
  that the poller prints and the auth resolves).
- Each emitted line corresponds to a genuinely-new occurrence, not a per-tick repeat (the change gate
  works).
- The watch is still alive after the first cadence interval has elapsed — i.e. it did NOT die after
  cycle 1 (the symptom of the run_in_background+sleep failure mode you are avoiding).
- When the terminal condition fires (battery `completed`, rank reached), you can cross-check it against a
  direct `GET /v2/experience-requests/{xid}` or `GET /v2/division-leaderboards/{DV}` and the numbers
  agree.
