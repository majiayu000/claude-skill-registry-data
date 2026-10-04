---
name: nlm-skill
description: >-
  Expert guide for the NotebookLM CLI (nlm) and MCP server. Covers
  authentication, notebook management, source addition (URLs, YouTube, text,
  Drive, files), content generation (audio, video, report, quiz, flashcards,
  mind map, slides, infographic, data table), research, artifact management,
  and automation workflows. Progressive disclosure: body carries critical
  rules + decision tree + phase workflow; full command reference in
  references/.
  Triggers on "nlm", "notebooklm", "notebook lm", "podcast generation",
  "audio overview", or any NotebookLM automation task.
user-invocable: true
disable-model-invocation: false
version: "0.7.0"
author: "Ali Farahat"
tags: ["nlm", "notebooklm", "cli", "mcp", "ai-automation"]
when_to_use: |
  USE WHEN:
  - User invokes /nlm-skill or asks about NotebookLM.
  - User mentions `nlm`, NotebookLM, or "notebook lm".
  - User wants to create/manage notebooks or add sources (URLs, YouTube,
    text, Drive, files).
  - User wants to generate content (audio podcast, video, report, quiz,
    flashcards, mind map, slides, infographic, data table).
  - User wants to research/discover new sources, or chat with notebook
    sources.
  - User wants to automate NotebookLM workflows.

  DO NOT USE WHEN:
  - User wants a podcast about arbitrary content not in NotebookLM (use a
    general audio skill).
  - User needs Google Drive file management outside NotebookLM context.
---

# NotebookLM CLI & MCP Expert

> **Leading words:** nlm, NotebookLM, audio overview, studio artifacts,
> progressive disclosure, phase separation, confirm-required, capture IDs,
> alias shortcuts, no REPL.

This skill provides comprehensive guidance for using NotebookLM via both the
`nlm` CLI and MCP tools. The body carries the critical rules, the tool
detection decision tree, and the 3-phase workflow. Depth lives in
`references/` behind context pointers.

## Tool Detection (CRITICAL — read first)

**ALWAYS check which tools are available before proceeding:**

1. **Check for MCP tools:** Look for tools starting with `mcp__notebooklm-mcp__*`.
2. **If BOTH MCP tools AND CLI are available:** ASK the user which they prefer.
3. **If only MCP tools are available:** Use them directly (see
   [references/mcp_tools.md](references/mcp_tools.md)).
4. **If only CLI is available:** Use `nlm` CLI commands via Bash (see
   [references/command_reference.md](references/command_reference.md)).

```
has_mcp_tools = check_available_tools()  # mcp__notebooklm-mcp__*
has_cli = check_bash_available()         # Can run nlm commands

if has_mcp_tools and has_cli:
    user_preference = ask_user()
else if has_mcp_tools:
    use_mcp_tools()
else:
    use_cli()
```

## Critical Rules (read first)

1. **Always authenticate first:** Run `nlm login` before any operations.
2. **Sessions expire in ~20 minutes:** Re-run `nlm login` if commands start
   failing with auth errors.
3. **⚠️ ALWAYS ASK USER BEFORE DELETE:** Deletions are irreversible. Show
   what will be deleted and warn about permanent data loss.
4. **`--confirm` is REQUIRED:** All generation and delete commands need
   `--confirm` / `-y` (CLI) or `confirm=True` (MCP).
5. **Research requires `--notebook-id`:** The flag is mandatory, not
   positional.
6. **Capture IDs from output:** Create/start commands return IDs needed for
   subsequent operations.
7. **Use aliases:** `nlm alias set <name> <uuid>` simplifies long UUIDs.
8. **Check aliases before creating:** `nlm alias list` first to avoid name
   conflicts.
9. **DO NOT launch REPL:** Never `nlm chat start` — it opens an interactive
   REPL that AI tools cannot control. Use `nlm notebook query` for one-shot
   Q&A.
10. **Output format:** Default (no flags) = compact + token-efficient.
    `--quiet` captures IDs for piping. `--json` only when parsing fields.
11. **Use `--help` when unsure:** `nlm <command> --help` shows options.

## Phase 1 — Authenticate

```
- [ ] nlm login (launches browser, extracts cookies — primary method)
- [ ] nlm login --check (validate current session)
- [ ] If multi-account: nlm login --profile <name>; nlm login switch <name>
- [ ] If MCP only and auth fails: mcp__notebooklm-mcp__refresh_auth()
```

🛑 **Checkpoint:** Confirm authentication is valid before any other
operation. Re-authenticate if session > 20 minutes old.

## Phase 2 — Operate

```
- [ ] List/find notebook: nlm notebook list, or use an alias.
- [ ] Add sources: --url (web/YouTube), --text, --drive <doc-id>,
      --file "/path" --wait.
- [ ] Research new sources: nlm research start "query" --notebook-id <id>
      (--mode fast|deep, --source web|drive).
- [ ] Poll research: nlm research status <id> --max-wait 300.
- [ ] Import: nlm research import <id> <task-id> [--indices ...] [--cited-only].
- [ ] Manage aliases: nlm alias set|get|list|delete.
- [ ] Query sources: nlm notebook query <id> "question" (--source-ids to scope).
```

Pull [references/command_reference.md](references/command_reference.md) for
full CLI command signatures and options.

## Phase 3 — Generate

```
- [ ] Pick artifact: audio | video | report | quiz | flashcards | mindmap |
      slides | infographic | data-table.
- [ ] ALWAYS require --confirm (CLI) or confirm=True (MCP).
- [ ] Poll status: nlm studio status <nb-id>.
- [ ] Download: nlm download audio|video|report|slide-deck|quiz <nb-id>
      --output <path>.
- [ ] Export to Docs/Sheets: nlm export docs|sheets <nb-id> <artifact-id>
      --title "...".
- [ ] Delete artifact: nlm studio delete <nb-id> <artifact-id> --confirm
      (ASK USER FIRST).
```

Pull [references/command_reference.md](references/command_reference.md) for
artifact-specific flags (formats, lengths, styles, orientations).

## Reference Index

| File | Use it for |
|---|---|
| [references/command_reference.md](references/command_reference.md) | Full CLI command signatures + all options for every `nlm` command |
| [references/mcp_tools.md](references/mcp_tools.md) | Full MCP tool reference — every `mcp__notebooklm-mcp__*` tool with parameters |
| [references/workflows.md](references/workflows.md) | End-to-end workflow sequences (research → podcast, study materials, Drive sync, batch + cross-notebook) |
| [references/troubleshooting.md](references/troubleshooting.md) | Detailed error recovery — every error, cause, and solution |

## Quick Reference

```bash
nlm --help              # List all commands
nlm <command> --help    # Help for specific command
nlm --ai                # Full AI-optimized documentation
nlm --version           # Check installed version
```

## Rate Limiting

Wait between operations to avoid rate limits:
- Source operations: 2 seconds
- Content generation: 5 seconds
- Research operations: 2 seconds
- Query operations: 2 seconds
