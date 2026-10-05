---
name: rr
description: >-
  Alias for the retro skill: identical behavior, shorter to type. On any trigger, run the retro
  skill, which holds the single copy of the logic. Triggers: "/rr", "rr", "retro".
license: MIT
---

# /rr — alias for /retro

**What it is:** just a short hotkey. `/rr` = `/retro`, letter-for-letter the same thing.
Typing `rr` is faster than `retro`. There is NO separate logic here and there must never be any.

**What to do on trigger:** immediately invoke the `retro` skill via the Skill tool and follow it as usual.
Do not copy the retro steps here — the single source is the `retro` skill (the "one source, no duplicates" rule; simplicity-first).

**The double-letter alias family** (one logic per pair):
- `/tt` == `/test` — test what was just built
- `/rr` == `/retro` — end-of-session retrospective
- `/cc` — print a ready-made `/compact` line for this session
- `/1` == `/!` — resurrect after a crash

**Boundaries:** the folder name is `rr`, so `/rr` works natively; wrong-keyboard-layout variants are
text triggers — on recognizing them, run this same skill. Case-insensitive ([[commands-case-insensitive]]).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
