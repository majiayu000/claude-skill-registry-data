---
name: watch-channel
description: >-
  Put a nightly watcher on any Telegram channel or chat in one command: register the channel and
  a single nightly job doing an incremental zero-token fetch plus the shared detector, producing
  a private shortlist report. Triggers: "/watch-channel <@channel|id>", "watch this channel",
  "monitor <channel> nightly".
license: MIT
---

# /watch-channel - put a nightly watcher on a channel with one command

> 🧒 End the report to a non-technical owner with a simple "In plain words" recap (memory `eli5-always`).

This is the "turn `/mine-channel` into a nightly routine" button (its Step 5, "should this become a routine?"). One parametric runner + a registry + ONE nightly job on the hub - we do NOT write a new engine per channel. Cost ladder [[vault-data-architecture]]: the incremental detector (0 tokens) at night → the LLM judge ONLY on demand (`/alpha-judge`), NEVER in cron.

Boundary vs neighbors: **`/mine-channel`** = a one-off mine (full scrape + judge + vault). **`/watch-channel`** = put it on nightly autopilot (incremental + detector → a private report; the judge stays manual). **`/chat`** = find the channel id.

## Steps

**0. RECALL (don't duplicate).** Is the channel already watched? Read `$IMPORTS_ROOT/watchers/watchers.json` - if the slug is there and `active:true`, it already works (tell the owner, don't spawn a second one). Legacy per-community watchers have their own engines and do NOT go through this registry.

**1. Resolve the channel → id + slug.** A username (`@prompt_design`) or a numeric id. Don't know the id - `/chat <name>` or `mcp__telegram__search_dialogs`. Pick a short latin **slug** (it doubles as the folder `_imports\alpha\<slug>`).

**2. Confirmation fork (show BEFORE→AFTER, wait for `+`).** Ask/confirm 3 things, because there are non-trivial choices here (this is not a "blind yes", [[informed-consent-explain-why]]):
- **the account session** - which Telegram account we read as (that account must be subscribed / have access to the channel). Default `TELEGRAM_SESSION_STRING_WORK_ACCT_A`. ⚠️ **AuthKey invariant** ([[deterministic-script-gotchas]]): the watchers' session must NOT be used simultaneously by a live MCP from another IP - Telegram will invalidate the key. All watchers run **sequentially on the HUB under one session** - that is safe; but if the chosen account is the one holding a live listener, pick a dedicated `..._WATCH` session instead.
- **sensitivity** - a closed/delicate channel → `sensitivity:"private"` (anti-leak on the OUTPUT side - the report never goes outbound/public, [[telegram-safety]]).
- **window/top** - `window_days` (default 3), `top` (default 25).

**3. Register it.** Append an object to `watchers.json → watchers[]` (fields are described in the file's `_fields`), `active:true`. That is all the "code" a new channel needs - you do NOT create a new scheduler task (one shared task runs the whole registry).

**4. Create/verify the nightly task - ON THE HUB** ([[hub-master-machine]], [[desktop-max-laptop-min]]; night window [[routines-run-at-night]]). All automatic Telegram jobs are consolidated on the always-on hub. If `WatchChannelsNightly` does not exist yet - create it there (via a `_machine-bus` task to the hub, [[machine-bus-telegram-rail]]):
- command: `watch_run.cmd` → `python $IMPORTS_ROOT/watchers/watch_run.py` (PYTHONUTF8=1, PYTHONIOENCODING=utf-8, log in `_watch_run_log.txt`);
- a slot inside the night window, **spaced apart** from the other nightly miners (03:30 / 04:15 / voice) - e.g. **04:45**;
- `_imports` is NOT synced → stage the engine into `_machine-bus\_transit\_imports-engines\watchers\` and ask the hub to copy it.
If the task already exists - the registry simply got updated, and the new channel is picked up the next night.

**5. Prove it (`/tt`) while the session is alive.** One-off run of a single channel: `python $IMPORTS_ROOT/watchers/watch_run.py <slug>` → check that `_imports\alpha\candidates\<slug>-report.md` appeared and the counter says `+N new`. A repeat run = `+0` (idempotent). ⚠️ Check the report's CONTENT too, not just the counters: it must contain clickable `t.me/...` links (for that the registry entry needs the `username` field - without it detect() only gets a numeric id and writes no links; this pitfall was caught 2026-07-04). On a laptop with a dead/foreign session skip the live test - the first run happens on the hub.

## Management
- **list:** read `watchers.json` (or `/arch`).
- **remove/pause:** `active:false` (don't delete - the history and the db stay).
- **reports:** `_imports\alpha\candidates\<slug>-report.md` (overwritten nightly, the latest one is the fresh one). Want it in the vault - run `/alpha-judge` or Step 4 of `/mine-channel` (judge → atomic notes + concept links).

## Boundaries
READING the channel only, never send anything into it. The detector is generic (KW/PROMO/BANTER in `mine_channel.py`); per-channel tuning happens there too. Sensitive channels → `#private`, never outbound. The judge (LLM) - ON DEMAND ONLY, never in the nightly cron (token economy).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
