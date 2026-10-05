---
name: last30days
description: >-
  Report what is genuinely new in the last 30 days on a topic, by slicing locally collected
  nightly channel databases with no live crawling. Run it before a strategic decision, as the
  fresh-signal feed for the gap phase. Triggers: "/last30days <topic>", "trendwatch <topic>",
  "what changed last 30 days on X".
license: MIT
---

# /last30days — what's new on topic X over the last 30 days

> 🧒 End the reply to the operator with a short "In plain words" recap (memory `eli5-always`).

A fast **trend-watch BEFORE strategy**: before planning or launching a Deep Research, take a 10-second slice of "what actually moved on this topic in the last 30 days". This is the **entry into the GAP phase of the Alpha Protocol** (`/alfa`): recall knows the operator's past, `/last30days` adds fresh signal from outside → together they outline the hole a DR has to fill.

Three-layer design ([[skill-design-three-layer]]): a thin skill (UX) → a deterministic engine (0 tokens) → an existing store (8 channel databases). The cost ladder [[vault-data-architecture]]: a SQL slice answers cheaply, the LLM only synthesizes the top hits.

## Steps

**0. RECALL (don't duplicate).** Is there already a fresh slice on this topic? Check `$IMPORTS_ROOT/alpha\candidates\_last30days-<topicslug>.md` plus memory/the vault (`/ask <topic>`). If the slice is fresh (from today) — reuse it, don't re-run.

**1. Deterministic slice (0 tokens, 0 network).** Expand the topic into synonyms in both languages you collect in (the model judges what matters): e.g. the topic "sub-agents" → `mcp, sub-agent, subagent, agent, orchestr, swarm`.
```
set PYTHONIOENCODING=utf-8
python $IMPORTS_ROOT/watchers\last30days.py --topic "<term1, term2, …>" --days 30 --top 25 --json
```
→ slices the 8 channel databases (`_imports\alpha\<slug>\<slug>.db`, refreshed nightly) by window × keys, scores through `mine_channel.score`, dedups, writes the digest `_imports\alpha\candidates\_last30days-<topicslug>.md` and prints the top as JSON. **It does not re-scrape** — the databases are updated by the nightly `watch_run.py`. Need a guarantee of freshness right now → add `--refresh` (goes to the network on the subscription session). Empty result → widen the synonyms / raise `--days`.

**2. (optional) Outside freshness — WebSearch.** If the topic reaches beyond the operator's Telegram channels (market/releases/competitors) — 1-2 `WebSearch` queries over the same keys, windowed to the last 30 days. It complements the channel slice, it does not replace it. Skip it for narrowly internal topics.

**3. Synthesis (LLM, top hits only — Sonnet).** Grunt work → Sonnet ([[model-routing-sonnet-grunt]]; subagent `model:'sonnet'`). Read ONLY the digest file + the WebSearch results, dedup semantically (cross-channel reposts of the same item), and assemble a **tight** digest by theme:
- **🆕 What's new** — concrete releases/tools/deals/techniques within the window (with a link and a date).
- **🔀 What changed** — a shift in consensus or direction versus what the operator already knew (compare against recall).
- **👀 What to watch** — early signals, not yet mainstream.
Each item is one line + a link. No filler. Mark confidence where it matters.

**4. Feed it into strategy.** Hand the digest to the GAP phase of `/alfa` (or straight into a Decision Memo / DR prompt as "fresh 30-day context"). A valuable slice is worth keeping → a vault note via [[obsidian-ingest]] (provenance: the channel databases + the window dates).

## Boundaries
Read-only and **PRIVATE** (Second-Brain layer) — the engine only reads the databases and writes a digest file; nothing goes outward. The scoring is a mechanical detector (engagement + keywords), not "smart" — the smart filtering is step 3. Freshness comes from the nightly `watch_run.py`; suspect it's stale → `--refresh`. Topic outside those 8 channels → lean on step 2 (WebSearch), don't invent.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
