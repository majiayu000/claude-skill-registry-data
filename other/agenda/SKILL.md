---
name: agenda
description: >-
  Show the operator's day: today's calendar plus what needs them personally (leads due, people
  awaiting a reply, deadlines), pulled from Calendar and Telegram and ranked. Read-only: sends
  and commits nothing. Triggers: "/agenda", "what's on today", "my agenda".
license: MIT
---

# /agenda — today at a glance

> 🧒 When reporting to Anton end with a child-simple "In plain words" recap. (memory `eli5-always`)

A fast, read-only "what does my day look like" — the manual counterpart of the scheduled `Tg calendar agenda` task (same intent, fired by hand). It assembles, it does NOT act (sending/booking lives in /pipeline + /intro).

## Assemble (read-only)
1. **Calendar** — `mcp__a63ab772-..._list_events` for today across Anton's calendars (`list_calendars` first if unsure). If that tool id is stale (connector reconnected), load it via ToolSearch query "calendar list events" like the `tg-calendar-agenda` twin does. His reminders live in **`owner.calendar@example.com`**, times in **Europe/Lisbon** (he lives there mostly — [[remind-anton-via-calendar]]). List meetings/reminders with times.
2. **Needs HIM personally** — the rare things only Anton can clear: leads due today (read `$IMPORTS_ROOT/tg_followups.json` + Platinum CRM, or call /pipeline's triage logic), a real human awaiting his reply, a money/legal deadline. He doesn't read email → surface only the email items that need HIM ([[anton-doesnt-read-email]]); no digest walls.
3. **Today's one commitment** — if /coach logged an evening "tomorrow's one commitment" in `04-Coach/`, echo it.

## Rank & present
Top of the list = time-bound + needs-Anton (a meeting in 2h, a lead going cold). Then fixed calendar blocks. Then nice-to-have. Keep it tight — this is a glance, not a report. Offer the obvious next action ("work the leads → /pipeline", "a meeting with no agenda → /intro").

## Safety
Read-only. Never send a message, book, or commit from here — hand off to /pipeline, /intro, or ask.

## Output
A short ranked agenda (≤~8 lines): ⏰ time-bound first, then context. Then 🧒 recap. Visual option: the Life-OS / Coach dashboards already render the day by eye ([[prefer-visual-dashboards]]).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
