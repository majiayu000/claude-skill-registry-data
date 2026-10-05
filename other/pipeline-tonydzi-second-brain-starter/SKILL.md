---
name: pipeline
description: >-
  Triage a lead pipeline and say who needs action today: replied means send the scheduling link,
  link sent 24h ago without a booking means nudge, awaiting reply means check inbound, going
  cold means follow up, booked means close out. Ranked and draft-first, so the owner edits
  before anything goes out. Triggers: "/pipeline", "work my leads", "who is stuck in the
  funnel".
license: MIT
---

# /pipeline — work the leads (today's actions)

> 🧒 **When reporting to a non-technical operator:** end with a child-simple "In plain words" recap in their language. NEVER inside lead messages.
> 📖 Operates under the `bible` skill — outreach codex `_Bible-Outreach-MOC`. Outbound = **send-direct (the operator 2026-06-16 — they edit the sent message after)**; NO mass auto-blast (pace + personalize per lead). Money / commitments / credentials → escalate.

## 🖥️ Dashboard first (the operator works visually)
`python "$IMPORTS_ROOT/build_pipeline_dashboard.py"` → open `$OBSIDIAN_VAULT/_Dashboards/Pipeline-Dashboard.html`: a kanban by stage (🔥 replied → ⏰ nudge → ⏳ booked → 👀 waiting → ✅ done) + ready drafts (click = copy). View only, it sends nothing. The text walkthrough below is for the actions themselves (send-direct, the operator edits after the fact).

## Step 1 — Load live pipeline state (deterministic, ~free)
Read `$IMPORTS_ROOT/tg_followups.json` (the watcher's live state). Each `pending[]` lead: `lead`, `chat_id`, `username`, `pitch_sent`, `calendly_sent`, `replied`, `booked`, `booking_confirmed`, + a `check` instruction. Plus `calendly_sent_at` (for the 24h nudge) and `booking_nudge_rule`.
Deeper history per lead: `04-Projects\crypto\Platinum-CRM\_Platinum-CRM-MOC.md` + its lead cards, or `/ask --leads "<name>"`.

## Step 2 — Classify each lead → TODAY's action (priority order)
1. 🔥 **Replied, Calendly not sent** (`replied` set, `calendly_sent:false`) → draft `calendly_text` to that chat. Warm NOW = top priority.
2. ⏰ **Calendly sent ≥24h, not booked** (`calendly_sent:true`, no `booking_confirmed`, `calendly_sent_at` >24h ago) → draft `booking_nudge_text` (leads forget to book — standing rule).
3. 👀 **Awaiting reply** (`pitch_sent:true`, no `replied`) → run the lead's `check`: read recent messages of `chat_id` (Telegram MCP; see `telegram-howto`) for a NEW inbound (sender ≠ Tony) after our pitch. If replied → it becomes case 1.
4. ❄️ **Going cold** (pitched long ago, no reply, no nudge) → propose ONE soft follow-up, or mark to drop.
5. ✅ **Booked/confirmed** → close out; suggest removing from `pending`. Never re-pitch.

## Step 3 — Output the worklist, then act on the operator's go
- Show a ranked table: **lead · state · proposed action · exact draft text**.
- Send each directly (the operator edits the sent message if something's off); NO mass auto-blast — pace + personalize per lead.
- After sending, **UPDATE `tg_followups.json`** (`calendly_sent`, `booking_confirmed`, `booking_nudge_sent`…) so state stays true.
- Refresh the lead's CRM card (telegram-lead-outreach capture step).
- End with 🧒 recap.

## Guardrails
- Voice = the operator's words **verbatim** (their rule); concise, no filler.
- Money / commitments / credentials → escalate, never autonomous.
- If `tg_followups.json` is empty/stale → say so; offer to rebuild from recent Telegram via telegram-lead-outreach ("find + capture").


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
