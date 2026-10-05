---
name: alpha-review
description: >-
  Open the alpha review screen to mark judge keepers as gold or miss, read per-miner precision,
  and print the eval state. Use when tuning a miner's accuracy. Thin launcher over the existing
  harvest engine and local review server. Triggers: "/alpha-review", "alpha screen", "open the
  review screen".
license: MIT
---

# /alpha-review — the alpha selection screen in one command

The engine is already built (2026-06-18/20). This skill is launch + summary; it duplicates nothing.

## Steps

1. **Is the server alive?** `netstat -ano | findstr :8772` (PowerShell) / `netstat -ano | grep :8772` (bash).
   - Listening → jump to step 3.
2. **Start it** (a fresh harvest runs inside):
   ```
   cd /e/Obsidian/_imports/alpha && PYTHONIOENCODING=utf-8 python alpha_review_server.py --no-browser
   ```
   in the background (`run_in_background`). Manual alternative for the operator: double-click `$IMPORTS_ROOT/alpha/alpha-review.cmd`.
3. **Hand over the link**: http://127.0.0.1:8772 — open in a browser (local only, nothing leaves the machine).
4. **Eval summary** (0 LLM tokens):
   ```
   PYTHONIOENCODING=utf-8 python $IMPORTS_ROOT/alpha/alpha_tune.py
   ```
   Show the operator: how much is labelled / per-miner precision / what to label first (uncertainty sampling: PARTIAL first). At >=8 labels per miner, tune names a concrete detector fix.
5. **Remind them of the loop**: labels -> `alpha_tune.py` -> adjust the detector threshold/filter -> re-harvest -> re-label. Cards carry a batch badge (🆕 = fresh nightly batch).

## Pitfalls
- The DB is a cumulative INBOX of every nightly batch (not just the latest judged file) — "extra" items are not junk, they are an unlabelled backlog. Do not "fix" it.
- An empty screen is not the same as no data: first check that the harvest actually ran (`alpha_harvest.py` prints counters) and that you are looking at the right drive (E:, not C:).
- 🔒 Community-sourced cards are HIGH sensitivity: never screenshot the screen outside, and approach contacts value-first only (standing rule for elite crypto communities: zero cold DMs, value first).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
