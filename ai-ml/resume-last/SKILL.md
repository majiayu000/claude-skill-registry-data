---
name: resume-last
description: >-
  Collect the last human session, or a specific one by id, into a seed on the clipboard, so a
  new session continues where the old one broke off, including after a crash or on a machine
  where native resume does not work. Triggers: "/resume-last", "/resume", "continue the last
  session".
license: MIT
---

# /resume-last — pick up the previous chat in one move

**The pain:** a session crashed or got lost in the interface → you used to have to dig through the
catalog, find it and copy it by hand. The native `claude --resume` does **not** work for a foreign or
cross-machine session (since v2.1.9 Claude rejects a "foreign" session). So the reliable way is to start a
NEW session pre-loaded with the full history of the old one.

## What it does

1. Finds your **latest human** session (service/robot ones are filtered out by the
   `session_author` classifier) — or takes a specific `cliSessionId` if you pass one.
2. Builds the seed: the whole history + "continue from here", and puts it on the **clipboard**
   (plus a file `_Dashboards/sessions-md/_continue/<cli>.seed.md`).
3. You open a **New session** and press **Ctrl+V** — the conversation continues.

## How to run

The latest session on this machine:
```
python "$IMPORTS_ROOT/claude_sessions/continue_session.py" --last
```
A specific session (id from `Sessions-Catalog.html` or from the `/resume-last` header):
```
python "$IMPORTS_ROOT/claude_sessions/continue_session.py" <cliSessionId>
```

(On Macs: `python3`, and for a non-standard vault path set env `CLAUDE_VAULT_ROOT=<...>`.)

## What to tell the operator

- Say WHICH session was picked up (title + date + cli) and that the seed is already on the clipboard.
- Give exactly one instruction: **"Open a New session and press Ctrl+V — you will continue where you left off."**
- If `clipboard: FAILED` — say the seed is in the file `<cli>.seed.md`, open it and copy manually.
- If the operator can already see the wanted session in Recents on the same machine — remind them the
  native `claude --resume <cli>` works there too (faster, no pasting).

## Boundaries

- READ-only against the vault/sessions: it only READS transcripts and writes the seed file + clipboard.
  It sends nothing and changes nothing in live data.
- It is the twin of the SessionStart hook `session_resume_hook` (that one SHOWS the previous session at
  startup; this one PICKS IT UP with a single command).


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
