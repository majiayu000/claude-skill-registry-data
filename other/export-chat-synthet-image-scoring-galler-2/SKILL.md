---
name: export-chat
description: Use when the user types /export or /export-chat, or asks to export, save, dump, copy, or share the current chat, conversation, or agent transcript as a file or to the clipboard. Mimics Claude Code's /export for Cursor by rendering the Cursor agent transcript (user/assistant text plus full tool-call inputs) to Markdown. Also use to export an earlier Cursor chat by id.
capability: "Export a Cursor agent chat transcript to a Markdown file or the clipboard, like Claude Code /export."
side_effect_level: local_write
approval_required: false
requires_tools: "python (stdlib only); clip / pbcopy / wl-copy / xclip / xsel for --clipboard"
output_schema: "Path of the written Markdown file (or clipboard tool used) plus message/tool-call counts; --json for a summary object"
risk_class: low
---

# Export chat (Cursor `/export`)

Renders the Cursor agent transcript at
`~/.cursor/projects/<workspace-slug>/agent-transcripts/<uuid>/<uuid>.jsonl` to Markdown. The
newest transcript for the workspace is the current chat. Run the script from the workspace root.
The script lives next to this file, so use `.cursor/skills/export-chat/scripts/export_chat.py` in
this repo or `~/.cursor/skills/export-chat/scripts/export_chat.py` for the user-level install.

## Invoke

```bash
# /export            -> timestamped .md in cwd (YYYY-MM-DD-HHMMSS-<first-prompt>.md)
python .cursor/skills/export-chat/scripts/export_chat.py --json

# /export <file>     -> write to that path
python .cursor/skills/export-chat/scripts/export_chat.py notes/chat.md --json

# Copy to clipboard instead of writing a file
python .cursor/skills/export-chat/scripts/export_chat.py --clipboard --json

# Export an earlier chat: list, then pass the id (prefix ok) or a .jsonl path
python .cursor/skills/export-chat/scripts/export_chat.py --list
python .cursor/skills/export-chat/scripts/export_chat.py --transcript 29467281 --json
```

Other flags: `--workspace <path>` (default cwd) and `--raw`, which keeps injected wrapper tags such as
`<system_reminder>` in user messages. By default only the `<user_query>` text is kept.

## LLM judgment slots

- Use the filename or destination the user gave after `/export`. If they gave none, use the default.
  If they said "clipboard", pass `--clipboard`.
- Report the output path and counts from the JSON result in one sentence.

## Limits

- Cursor transcripts store tool *inputs*, not tool results, so results are not in the export.
- The reply that runs the export is not in the transcript yet, so it is not exported.

## Safety

- The export contains everything pasted into the chat, including any secrets. Do not write it
  into a tracked path without telling the user. Do not commit it, and do not send it to an
  external service without explicit approval.

Resolve helper paths from this skill directory. Run project commands from the target workspace.
