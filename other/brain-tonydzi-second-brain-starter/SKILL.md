---
name: brain
description: >-
  Health-check the second brain so failures are not silent: is the local search server alive, is
  the RAG index fresh, is the session-memory ledger filling, did the nightly distillation run.
  Read-only, with a green/red verdict per component. Triggers: "/brain", "/memory", "is the
  reindex alive".
license: MIT
---

# /brain — second-brain health at one glance

> 🧒 When reporting to a non-technical operator, end with a short plain-words recap (rule `eli5-always`).

Catches SILENT breakage of the memory/RAG stack (the things that kept breaking month after month: the reindex, the local search server, the memory pilot). Read-only, 0 tokens.

## What it does (one script)
`python $IMPORTS_ROOT/brain_health.py`

Checks 5 things and colors them 🟢/🟡/🔴:
1. **Search server** on its local port — alive or not (if it's down, auto-recall silently disappears); also shows whether the graph-assisted mode is on.
2. **Index** `_brain_e5.npy` — how fresh (🟡 if the reindex lags >48h).
3. **TurnState ledger** — how many turns recorded (memory Phase 1), when the last one was.
4. **Nightly distillation** — candidates in quarantine + when the last run happened.
5. **A/B direct-vs-graph recall** — how many runs + the operator's verdicts (👍/👎).

Writes a dashboard `$OBSIDIAN_VAULT/_Dashboards/Brain-Health.html` (the operator reads with their eyes, [[prefer-visual-dashboards]]). Exit code 0/1/2 = ok/warn/red (for scripts).

## When to fix (on 🔴/🟡)
- **🔴 search server down** → run the restart script (as admin, see [[always-on-memory-pilot]]); or reboot (the at-logon task brings it up).
- **🟡 index lagging** → `gpu_check.py [--kill]`, then `brain_embed_update.py [--wait-gpu 10]` ([[reindex-routine]]).
- **🟡 ledger empty** → fine if memory Phase 1 was just enabled (it fills from the next sessions on).

## What it does NOT do
It doesn't fix anything and doesn't write to the vault. It's a diagnostic. Fixing is a separate explicit step (the "read before you fix" rule, [[verify-existing-before-proposing]]).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
