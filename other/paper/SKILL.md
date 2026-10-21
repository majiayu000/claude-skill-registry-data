---
name: paper
description: Paper design canvas work, done by scripts. Use to capture a website or user flow into Paper as editable frames, copy or move frames between Paper files, organise a page into labelled groups, or read and bulk-edit a canvas cheaply.
---

The scripts in `~/.claude/skills/paper` talk to Paper desktop's local MCP endpoint (`PAPER_MCP`, default `http://127.0.0.1:29979/mcp`) and drive a headless Chrome of their own over the DevTools Protocol: each command starts it with a temporary profile and no window, and removes it when it ends. `PAPER_CDP` names another browser instead; Synth's port 9300 is refused, because driving it crashes Synth. Markup and screenshots travel script → Paper, never through your context: every command prints one line per frame.

## Branches

- Capture a site, app or flow into Paper → [`SNAPSHOT.md`](SNAPSHOT.md)
- Copy or move frames between Paper files → [`TRANSFER.md`](TRANSFER.md)
- Name frames and arrange a page into groups → [`LAYOUT.md`](LAYOUT.md)
- Read, find, bulk-edit or verify a canvas → [`CANVAS.md`](CANVAS.md)
- List how a built page differs from its frame → [`FIDELITY.md`](FIDELITY.md)
- A frame renders wrong, or you are about to change a script → [`CHANGELOG.md`](CHANGELOG.md)

## Rules for every branch

- **Target**: write to the file and pages the user named. `node canvas.mjs boards` lists the open file's pages; `node snap.mjs mcp create_page '{"fileId":"…","name":"…"}'` makes one when asked.
- **Size warning**: every script stops when Paper answers "file is too large", because further writes can lose data. The warning can be stale after deletions: ask the user to reconnect the Paper MCP, re-check with one read (`canvas.mjs boards`), and report if it is still there.
- **Own data only**: change what this run created. On data someone else owns, open only states that change nothing; a bin, Remove, Cancel, Pay or Confirm control can act at once, so capture those states from data the run created, or leave them out and say so.
- **Placeholders**: swap real names, emails and phone numbers in a form for placeholders before capturing it, and restore them after.
- **Working indicators**: the scripts release their own. After editing layers by hand through the Paper MCP, call `finish_working_on_nodes`.
- **Paper's guide**: load `get_guide` when you edit layers by hand through the Paper MCP; the scripts carry what they need.

Done when the user's page holds the frames, `canvas.mjs verify` or a screenshot has checked them, and your report lists what was captured, what failed and why.
