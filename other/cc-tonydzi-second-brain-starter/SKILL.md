---
name: cc
description: >-
  Print a ready-made /compact line in a canonical handoff format, so the operator pastes it as
  the next message and shrinks working memory without losing the thread. Use at the end of a
  long session. Triggers: "/cc", "compact", "finish via compact".
license: MIT
---

# /cc — compact in one keystroke

**The pain:** a bare `/compact` does NOT read our format (measured: 0 out of 354 — everything fell
back to the default, #14160). The ONLY thing that works is pasting an inline block right after
`/compact`. The operator used to fetch that block by hand. Now `/cc` assembles it itself, already
enriched with this session, and hands over a ready-to-paste line.

**What this is NOT:** it is not `/retro`. Retro = the full end of a session (inventory of what was
built → routing rules to their homes → and only then the compact handoff). `/cc` is only the
compact handoff itself, lightweight, with no inventory: for when the operator just wants to shrink
the window at a task boundary rather than close the session.

## What to do when invoked

1. **Read the canonical template** — the single source of the format (never invent headings):
   ```bash
   cat "$HOME/.claude/compact-prompt.md"   # on Windows: %USERPROFILE%\.claude\compact-prompt.md
   ```
   The skeleton = 7 headings: DECISIONS · TODO · NOW · PATHS AND VALUES · COUNTERS · OPEN · TOOLS AND CONTRACTS.

2. **Enrich the block with the CURRENT session** — never hand over an empty template. Walk the 7
   headings and fill each one with the real, verbatim content of this chat (decisions + why, the
   active error under NOW, exact paths/values/IDs, self-check counters + `/tt` status ✅ vs not
   verified, what broke under OPEN). Rationales are the first thing to evaporate — preserve those
   first.

3. **Emit the READY line** — it starts with `/compact `, followed by the enriched block, all inside
   a single ```code``` block so the operator can copy it whole and paste it as the next message.
   Plus one line above it: "➤ Copy everything in the block below and paste it as your next message."

4. **🧒 In plain words** ([[eli5-always]]): "I'm packing our memory into a short note so nothing gets
   lost when the context is squeezed. Copy it and paste it."

## Boundaries
- The folder name is `cc`, so `/cc` works natively; "compact" and similar words are text triggers for the same skill. Case does not matter ([[commands-case-insensitive]]).
- The skill does NOT run the compact itself (that is a built-in command) and it sends/edits nothing — it only assembles text.
- When to fire it: at a task boundary around 60% of the window; don't wait for the auto-compact at 95% (that loses more).
- Don't confuse: `/tt` = test what was built · `/rr` = full retro · `/cc` = quick compact handoff · `/1` = resurrection after a crash.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
