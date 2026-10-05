---
name: community-alpha
description: >-
  Run one full mining pass over an imported community-chat corpus: deterministic detector, LLM
  judge, harvest, review screen. Works on any imported corpus through a per-source config and is
  safe to re-run, being idempotent by message id. Triggers: "/community-alpha <source> [month]",
  "mine alpha from <community>".
license: MIT
---

# /community-alpha <source> [month] — one community-alpha run

Example: `/community-alpha sostav 2026-06`. No month given → the previous full month.

## Steps

1. **Is there a detector?** `$IMPORTS_ROOT/<source>\<source>_alpha.py` (today: `lobster`, `sostav`).
   - No → this is a NEW corpus: offer the operator a one-off adapter built to the existing pattern (schema from their SQLite + language keys + intro/banter penalty + topic weights; template = `sostav_alpha.py`). Do not build it without an explicit "+".
2. **Run the detector** (0 tokens):
   ```
   cd /e/Obsidian/_imports/<source> && PYTHONIOENCODING=utf-8 python <source>_alpha.py \
     --since <YYYY-MM-01> --until <the 1st of the next month> --top 35 --tag <YYYY-MM>
   ```
   → `$IMPORTS_ROOT/alpha/candidates/<source>-<tag>-report.md`. Show the scanned→shortlisted counter.
3. **Judge** (me, with the session model): I read ONLY the report (~35 candidates, never the corpus — token economy) and give a verdict ✅ ALPHA / 🟡 WATCH / 🗑 NOISE with a reason for each → write `$IMPORTS_ROOT/alpha/candidates/<source>-judged-latest.md` (format: `## ✅ ALPHA` / `## 🟡 WATCH` / `## 🗑 NOISE (DROP)`, inside it `### #N — title` + Verdict + Reason — the harvest parser already understands this).
4. **Is the miner registered?** `MINERS` in `$IMPORTS_ROOT/alpha/alpha_harvest.py`. No → add the row `("<source>", "<source>-judged-latest.md", "<home-note>")`. ⚠️ A parallel fleet edits this file too — re-read it immediately before editing (verify-existing), and keep the edit strictly additive. Optional: a label in the server's `MINER_LABEL`/`ORDER` (it does not crash without one — there is a fallback).
5. **Harvest + screen**: `python $IMPORTS_ROOT/alpha/alpha_harvest.py` (counters!) → `/alpha-review`. The new batch is visible by the 🆕 badge.

## Boundaries
- 🔒 Private communities (sostav and the like) are HIGH sensitivity: the layer stays strictly local, nothing goes outside; people surfaced by a find are approached value-first / warm intro only (zero cold DMs). Risk signals are DATA, not "opportunities".
- Judge honestly: reference cards, intro blurbs and restatements are 🗑 — never stretch a ✅ to pad the counter.
- This skill writes nothing into the vault; moving gold into home notes is a separate step behind the Tier-2 gate (the "→ to home" queue on the screen).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
