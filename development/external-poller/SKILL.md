---
name: evi-external-poller
description: Use when an agent must react to external events (mentions, emails, webhooks) without burning turns polling — a design pattern for out-of-turn polling that wakes the agent only on a hit.
---

# External poller

A pattern, not a script. To make an agent react to an external source (X
mentions, new emails, a webhook queue) without spending a model turn on every
empty poll, move the polling **outside** the agent's turns and wake the agent
only when there is something to handle.

## What it guarantees

The expensive resource — model turns / context — is spent only on real events.
Polling runs on a cheap supervisor timer; the agent stays idle until a hit
produces work, then is woken exactly once per batch of hits, with a bound on
re-pokes and a quiet window at night.

## How it works (the pattern)

```
[supervisor timer: launchd / systemd, every N min]
        │
        ▼
[poller script]  ── checks the external source (no model involved)
        │
        ├── nothing new → exit quietly
        │
        └── hit(s):
              ① write the payload to a pending file  (e.g. tasks/pending-mentions.json)
              ② self-poke the REPL  (tmux send-keys: text, sleep 1.5s, Enter — separate calls)
              ③ record poke time + attempt count in a state file
        │
        ▼
[agent wakes] → reads the pending file → handles items → deletes/empties it
```

Four design points that keep it honest:

- **Pending-consumption check.** Before re-poking, the script checks whether the
  pending file was consumed (emptied/deleted by the agent). If it still has
  content, the previous poke did not land — re-poke. If it is gone, the agent
  handled it — do nothing. The pending file *is* the start marker.
- **Re-poke cap.** Bound re-pokes (e.g. `MAX_REPOKE=3`). A poke during an active
  turn loses its Enter (the same send-keys lesson as burn/cron); re-poke a few
  times, then give up and let the next scheduled cycle or the morning brief
  surface the backlog. Never re-poke unbounded.
- **Night skip.** Gate firing on local hours (e.g. skip 23:00–07:00) so the
  agent is not woken — and the owner not pinged — overnight. Hits that arrive in
  the quiet window stay in the pending file and are handled at the next allowed
  cycle.
- **Idempotent payloads.** Dedupe on a stable id (mention id, message id) so the
  same event is never enqueued twice across overlapping polls.

## Implement in your project

There is no canned poller script in the kit — the source you poll is yours. Build
it by copying the mechanics of the closest sibling,
[`../../scripts/burn-watcher.sh`](../../scripts/burn-watcher.sh),
which already demonstrates: a supervised timer, a `poke()` with a 10-second
watchdog, separate text/Enter send-keys, a JSON state file, and a start-marker
re-poke loop. Replace its rate-window check with your source check, and replace
its `/burn` poke with a poke that tells the agent to read your pending file.

Supervise it like burn mode (see
[`../../launchd/com.example.burn-watcher.plist`](../../launchd/com.example.burn-watcher.plist)
for the plist shape).

## Adaptation points

- **Source:** any pollable API or local queue. Keep the network/IO work in the
  script, out of the model.
- **Wake transport:** tmux self-poke on Claude Code; on another harness use its
  equivalent "start a turn" trigger. The pending-file + state-file contract is
  transport-independent.
- **Push instead of poll:** if your source supports webhooks, the webhook handler
  replaces steps before ①; steps ①–③ (pending file + bounded self-poke + night
  skip) stay identical.

## Verify

1. Dry-run the poller with a forced hit → a pending file appears and a poke is
   sent once.
2. Leave the pending file in place → the next run re-pokes, up to the cap, then
   stops.
3. Consume (delete) the pending file → the next run does not re-poke.

## Rollback

Unload the supervisor timer; delete the pending and state files.
