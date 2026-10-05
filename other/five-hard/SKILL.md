---
name: five-hard
description: >-
  Have the second brain ask the owner five hard questions about their own long-held beliefs and
  codex entries that have not been revisited, so assumptions stop fossilizing. Monthly or on
  demand. Triggers: "/five-hard", "challenge my beliefs", "pressure-test my views".
license: MIT
---

# /five-hard — five hard questions

> 🧒 When reporting to a non-technical operator, end with a child-simple "In plain words" recap in their language.

**Why:** the identity layer (`belief-*` + `concept-bible-*`, ~24 notes) is "how I think".
That gets dangerous once part of it is wrong and nobody has checked. Here the brain itself starts the pressure-test.

## Run
`python "$IMPORTS_ROOT/five_hard_pick.py"` -> the 5 most stagnant notes (oldest mtime)
-> `$IMPORTS_ROOT/_five_hard_pick.json`. Override: env `FIVE_HARD_N=7`.

## The questions (top-model quality — identity synthesis, not grunt work)
Read each note IN FULL and give ONE hard question per note:
```
N. **[<stem>]** — <the owner's thesis in your own words>
   Question: <sharp, Socratic, capable of forcing a rethink>
   Why it is hard: <which counter-fact or trend could flip it>
```
Style: Socratic — not "you are wrong" but "what makes you sure today?"; lean on CONCRETE recent
signals; `epistemic-neutrality`; aim at the UNTESTED edge (the "tension / nuance" section),
not at the part already reflected on. "The rule still stands" is a valid answer (`bible-as-prompt`).

## Recording the answer (long memory; backup-first: vault_backup.py)
-> `$OBSIDIAN_VAULT/04-Coach/_Five-Hard/five-hard-YYYY-MM-DD.md`
Frontmatter: title, date, `type: five-hard`, `source: claude-session`,
`tags: [five-hard, coach, identity-layer]`. Body: the questions + the owner's answers verbatim;
if they changed position, propose a diff to the belief/bible note with `supersedes:` (via `/intake`). NO 🧒 block inside the note.

## Scheduled twin
Cron `five-hard-monthly`: 1st of the month, 05:25 local time (the briefing window, `routines-run-at-night`).
Picker -> questions (top-model subagent) -> **the fleet log chat** via `python $USERPROFILE/.claude/scripts/bus_ping.py --post "..."`
(canon: alerts go to the fleet log chat, never to Saved Messages) + "answer by voice or text, I will file it into the vault".
The manual twin is this skill; the single source of truth is the picker.

## Related
[[self-bible-identity-layer]] · [[bible-as-prompt]] · [[epistemic-neutrality]] · /coach (daily) vs
/five-hard (monthly). Active-brain map A-E: item B. ⚠️ Restored 2026-07-04 after the 2026-06-24 migration wipe.



<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
