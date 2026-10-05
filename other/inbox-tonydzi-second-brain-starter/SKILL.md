---
name: inbox
description: >-
  Read this machine's cross-machine mailbox, the messages another computer's agent left here
  over a file-synced bus folder, and send messages back the same way. A session-start hook shows
  new mail automatically; this is the on-demand mid-session re-check. Triggers: "/inbox", "check
  inbox", "messages from the other machine".
license: MIT
---

# /inbox — mail between my own machines

The "Claude on one machine → Claude on another" channel, over the synced `_machine-bus` folder (Syncthing, ~10s). It removes the human courier. Copy-paste by hand is an EMERGENCY channel only.

## Check what arrived for me (the main use)
```bash
python "$USERPROFILE/.claude/scripts/machine_bus.py" read
```
Shows only what is NEW for THIS machine (matched by hostname) and marks it read. Then report to the operator what came in and act on it if needed.
- At session start the `SessionStart` hook already does this automatically — `/inbox` is for when the operator says "check the inbox" mid-session (e.g. something new arrived over sync).
- Re-check without marking as read: `... read --peek`.

## Send a message to Claude on ANOTHER machine
1. List the available mailboxes:
   ```bash
   python "$USERPROFILE/.claude/scripts/machine_bus.py" list
   ```
2. Send:
   ```bash
   python "$USERPROFILE/.claude/scripts/machine_bus.py" send <RECIPIENT-HOSTNAME> "message text"
   ```
   The message must be self-contained (Claude on that machine has none of this session's context — include the goal, the steps, the paths, the values). It arrives in ~10s and surfaces for the recipient at session start or via `/inbox`.

## Which channel when
- **The automatic mailbox (this skill + the hook)** — the norm for everything cross-machine.
- **A human courier (copy-paste)** — ONLY if sync is down, the machines are off the shared network, or it is extremely urgent.

## Boundaries
- Do not put secrets in the mailbox if third parties could see the file (across the owner's own machines it is fine).
- "Fresher beats older": edit conflicts are resolved by the operator (Syncthing leaves `*.sync-conflict-*` files).
- Delivery is not instant: Claude is not a daemon; the letter waits until a session opens on that machine (or a routine fires).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
