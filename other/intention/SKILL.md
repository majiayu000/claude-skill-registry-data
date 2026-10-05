---
name: intention
description: >-
  Mine the day's sessions for the owner's intentions, cluster them into distinct ones, store
  them, and write two or three detailed posts with an explicit ask per channel, plus a loop
  tracking who answered. Drafts only. Triggers: "/intention", "mine today's intentions",
  "intention posts".
license: MIT
---

INTENTION_LANE_RUN

# /intention — the day's intentions → intention posts (draft-first)

GOAL: turn the owner's INTENTIONS of today (every pain / "how do I do X" question / "I need someone who…" from the day's sessions) into 2-3+ honest intention posts with an explicit ASK, so the audience returns ALPHA (a solution, a warm intro, a warning, a co-author). Draft-first: nothing is published, the drafts go to the owner over Telegram.

## Paths and engine
- Miner + store: `python $IMPORTS_ROOT/content-factory/intention/intention_mine.py <cmd>` (0 tokens).
- Store: `intentions.db` (never loses anything; deduped by content hash).
- Candidates: `candidates\cand-<DAY>.md`. Drafts: `drafts\intentions-<DAY>.md`.
- Decision/canon: `$OBSIDIAN_VAULT/02-Decisions/decision-intention-lane-content-factory-2026-07-02.md`.
- Telegram Saved Messages (the primary work account): numeric chat_id `<YOUR_CHAT_ID>` (NOT "me", no parse_mode).
- ⚠️ DELIVERY FALLBACK (when the Telegram MCP is unavailable/connecting — it drops out routinely): the Telethon rail, MCP-independent. Text: `TG_BUS_GROUP=<YOUR_CHAT_ID> python $USERPROFILE/.claude/scripts/tg_bus_send.py --raw "…"`; file: `… --raw --file "<path>" "<caption>"`. Verified 2026-07-02.

## Channel rules (from Deep Research 2026-07-02) — IMPORTANT
- Channels for alpha-seeking ask posts: **Telegram** (RU) · **X** (EN, #buildinpublic) · **Indie Hackers** (EN) · **Ask HN** (EN, "Ask HN:"). Optional: LinkedIn (business tone).
- ⛔ **Do NOT post asks on long-form article platforms or in the Facebook body** — the ask format does not work there (an article platform is for articles, not quick answers). Those platforms are separately the channel for longreads/dev-logs, not intentions.
- The platform decides the language: Telegram=RU, X/IH/HN=EN. No forced bilingual output.

## The intention-post format (established)
Context (what I'm doing) → what failed / what I realised → **an explicit, concrete ask** at the end. Honest, vulnerable tone, no marketing gloss. A concrete request ("do I pick A or B?", "I need an expert on X, who has done it?") beats a vague one. **Describe IN DETAIL how the owner got here and why** (his own rule). Length: X = teaser (240-370), Telegram/IH = medium, Ask HN = "Ask HN: <question>" + a paragraph.
5 templates (need an expert / A-vs-B choice / hit a wall / realised I was wrong / general poll) — in the decision memo §A4 / the DR.

## PRIVACY (hard)
No real names / @handles of third parties, no exact amounts (revenue/rounds/other people's deals), no secrets or paths with personal ids. Generalise ("a large lead", "$X"). Privacy beats completeness.

## MODEL
The post is the owner's authorial voice → written by the **top-tier model**. If the current run is NOT on it — delegate THE WRITING ITSELF to a subagent with `model:'opus'` (Agent tool), passing it the candidates + the format + the privacy rules. Clustering / candidate selection can run on a cheap model.

## STEPS
1. DAY = today's local date YYYY-MM-DD (print ASCII only).
2. Mining: `intention_mine.py mine <DAY>`. Read the summary (CANDIDATES) and the file `candidates\cand-<DAY>.md`.
3. If CANDIDATES == 0: do not invent anything. Tell the owner over Telegram "📭 <DAY>: no intentions mined today" and finish.
4. CLUSTERING (the judge): assemble DISTINCT intentions out of the raw candidates (one pain = one intention; merge repeats of the same topic). For each: a short title · pain (the pain/question) · journey (how he got here + why, in detail) · ask (the explicit request). Discard pure noise (non-intentions, housekeeping).
5. Store: for every distinct intention — `intention_mine.py add --day <DAY> --title "…" --pain "…" --journey "…" --ask "…" --sessions "sid1,sid2"`. Dedup will drop the ones already stored (that is fine — we don't post twice).
6. SELECTION for posting: take the 2-3 most alpha-worthy intentions OF TODAY (a strong concrete ask, freshness). More if the day was rich.
7. WRITING (top model): for each selected intention, write posts for the suitable channels (Telegram-RU + X-EN at minimum; add IH/Ask HN where the ask fits). Format + privacy as above. Vary the type (request / choice / realised-I-was-wrong).
8. Save every draft into `drafts\intentions-<DAY>.md` (UTF-8, no BOM; APPEND ONLY, never overwrite someone else's edits — if the file exists, append a section stamped with the run time). Mark the intentions: `intention_mine.py mark --id N --status drafted`.
9. Send to Telegram (chat_id `<YOUR_CHAT_ID>`, no parse_mode) a header "🎯 Intention drafts for <DAY> (edit and post them yourself):" + per intention a block "— <title> —" and the per-channel versions. Longer than ~4000 → split on paragraph boundaries into "Part N/M".
10. Report to the owner: how many intentions were mined / stored / drafted, which channels, what was deferred. Finish with "what's next".

## The bridge into an episode (intention → longread/dev-log on GitHub)
A strong intention is worth expanding into a "reality show episode": `intention_mine.py episode --id <N>` creates an episode bundle (9 drafts across the tiers of §7.2, including the longread tier — the article platform here is the LONGREAD channel, not an ask channel) + `intention-seed.md` carrying the context (pain/journey/ask) for the writer. Then write the drafts (voice = top model) in `episodes/<slug>/`, then `python episode_adapter.py check --slug <slug>`. The intention is marked `status=episode`. This is the seam with `/episode` — don't duplicate it, call it.

## The alpha loop (as responses arrive)
The owner says "<who> replied to the post about X" → `intention_mine.py respond --id <N> --who "<name/@>" --channel <channel> --note "<gist>"`. Check the queue: `responders --pending`. Promotion into the CRM (`leads.db`) is a separate verifiable step through the normal lead flow (never write into the production CRM blind).

## Boundaries
Draft-first is HARD — nothing goes outbound without the owner's explicit "publish". Don't post asks on article platforms. AK-47: don't spawn platforms beyond the decided set. Tier-2 (outbound/money) is not waived.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
