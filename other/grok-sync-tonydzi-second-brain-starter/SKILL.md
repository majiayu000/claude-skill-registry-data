---
name: grok-sync
description: "Pull Anton's Grok (grok.com / SuperGrok) conversation history into the Obsidian vault from an official Grok data export (prod-grok-backend.json). Trigger on “/grok-sync“, “синкани grok“, “подтяни grok“, “забери чаты из grok“, “обнови grok“, “sync grok“, “что нового в grok в волт“"
version: 1.0.0
---

OBJECTIVE: Fold a Grok data export into the vault (one note per conversation + SQLite), idempotently. Reply to Anton in Russian; end with a 🧒 «Простыми словами» recap ([[eli5-always]]).

## Why this shape (read before "fixing") — canon DR26-07-15-HUB-01
Grok has NO streaming/history API (the xAI API at api.x.ai is new-generations-only). The SANCTIONED rail is the on-demand bulk export → this skill parses that export; the "recurring" part is a **weekly actor**: trigger export → email link → download ZIP → parse (same family as [[takeout-pull]]). Incrementality is LOCAL (conversation_id + content_hash) because Grok re-exports the FULL archive each time.
⚠️ **AUP (2026-06-26)**: xAI forbids automated access → the reverse cookie rail (`/rest/app-chat/*`) stays **OFF by default**; only turn it on by Anton's explicit decision. This skill only ever parses an export you were given — no network.

## Step 0 — Get the export (human gate, then a weekly actor)
If no fresh Grok export is on disk:
- grok.com → **Settings → Data Controls → Export Data** (or `accounts.x.ai/data`) → email with a download link → **ZIP** under `ttl/30d/export_data/<uuid>/` containing **`prod-grok-backend.json`** (+ `prod-mc-asset-server/` for media).
- Interactive X/Grok login / 2FA = HARD-STOP → escalate to Anton (never enter credentials). Download of his OWN export = pre-authorized (drive his logged-in Chrome).
- The download link is time-limited — pull it inside the window (the [[takeout-pull]] actor pattern: detect the "ready" mail, download in time).
- ⚠️ X data archive ≠ grok.com history (separate stores, confirmed by [аккаунт] 2026-07-15) — do NOT use the X archive as the rail.

## Step 1 — Import (idempotent, stdlib, 0 tokens)
Point the importer at the extracted `prod-grok-backend.json`:
```
python "$HOME/Obsidian/_imports/grok/grok_lib.py" import "<path-to-prod-grok-backend.json>"
```
It: normalizes wrappers (`conversation` + `responses[]`, mixed ISO/BSON times, human→user) → upserts into `grok_conversations.db` (keyed by conversation_id; re-writes only when content_hash changed) → writes ONE note per conversation under `01-Conversations/Grok/conversations/` (thinking traces in `<details>`) → writes `_freshness.json`.

Prints: `grok import: +N new / M updated / K unchanged | notes: W written | DB total T | newest DAY (stale Dd)`.

## Step 2 — Verify on FIRST real export (⚠ field-names + completeness)
The parser is verified on a synthetic fixture matching the DR-documented schema (`_test_grok.py`, 18/18). On the **first real export**, spot-check a written note against `prod-grok-backend.json`: confirm turns alternate user/assistant, thinking traces landed, BSON timestamps decoded. If field names differ, adjust `normalize_grok()` in `grok_lib.py` (single source), NOT this skill. Reference parser to cross-check: `Owlock/easy-grok-chat-exporter`.
⚠️ **Completeness canary** (DR risk): some exports may truncate — compare turn-count of a few known live conversations (UI) vs the export; systematic shortfall → escalate.

## Step 3 — Reindex + report
- `python "$HOME/Obsidian/_imports/brain_embed_update.py"` if RAG is available on this node ([машина флота] = follower — may defer to hub nightly; don't force an ML stack onto the laptop).
- Report new/updated notes, newest day, freshness. End with 🧒 recap.

## Boundaries / constraints
- AK-47: single SKILL.md + `grok_lib.py` (stdlib). No server/service. No network (parses a file).
- Idempotent: writes only under `01-Conversations/Grok/conversations/` (files it owns); never clobbers concept-enriched notes elsewhere.
- Test gate: after any change to `grok_lib.py`, run `python _imports/grok/_test_grok.py` (must stay ✅ ALL PASS) before "done" ([[test-after-build-skill]]).
- No secrets: file-based export, nothing to leak. Do NOT enable the cookie rail without Anton's explicit decision (AUP).

## Relation (do not duplicate)
- Acquisition of the export = a weekly actor on the [[takeout-pull]] pattern (detect ready mail, download). This skill only PARSES what landed.
- Siblings: [[chatgpt-sync]], [[gemini-sync]], [[claudeai-sync]], [[whatsapp-sync]].
- Full architecture + build order: [[insight-DR-DR26-07-15-HUB-01-grok-gemini-export-architecture]].


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
