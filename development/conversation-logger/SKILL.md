---
name: conversation-logger
description: This skill should be used when users need to save, search, or retrieve Claude Code conversation transcripts. Use this skill when users ask to save the current conversation, search through past conversations for context, or retrieve information from previous sessions. Also use when appropriate to proactively save important conversations at natural breakpoints (e.g., after completing a major feature, fixing a critical bug, or when the user indicates they're done with a session).
---

# Conversation Logger

## Overview

This skill enables systematic saving, searching, and retrieving of Claude Code conversation transcripts. It converts raw JSONL transcripts into readable markdown format and provides search capabilities across all saved conversations.

## When to Use This Skill

Use this skill when:
- User explicitly asks to save the current conversation
- User wants to search through past conversations for context or information
- User asks about previous sessions or work done in earlier conversations
- Proactively saving important conversations at natural breakpoints (completed features, major bug fixes, end of work session)
- User needs to find when a specific topic, command, or issue was discussed

## Core Capabilities

### 1. Save Current Conversation

To save the current conversation, use the `save-conversation.sh` script with the transcript path and optional session ID.

**Script location:** `scripts/save-conversation.sh`

**Usage:**
```bash
bash scripts/save-conversation.sh <transcript-path> [session-id]
```

**Important:** The transcript path is typically available as an environment variable or in the session context. Common locations:
- `$CLAUDE_TRANSCRIPT_PATH` (if set)
- `~/.claude/sessions/<session-id>/transcript.jsonl`
- Check the current session directory for transcript files

**What it does:**
- Copies the JSONL transcript to `~/.claude/conversation-logs/`
- Converts the transcript to readable markdown format
- Creates session metadata file
- Creates symlinks to the latest conversation for easy access

**Output files created:**
- `conversation_YYYY-MM-DD_HH-MM-SS.jsonl` - Raw transcript
- `conversation_YYYY-MM-DD_HH-MM-SS.md` - Human-readable markdown
- `session_YYYY-MM-DD_HH-MM-SS.json` - Session metadata
- `conversation_latest.jsonl` and `conversation_latest.md` - Symlinks to most recent

**Example workflow:**
When a user says "save this conversation" or "log our work", first locate the transcript path, then execute the save script.

### 2. Search Through Saved Conversations

To search through saved conversations for specific terms or topics, use the `search-conversations.sh` script.

**Script location:** `scripts/search-conversations.sh`

**Usage:**
```bash
# Search for a term
bash scripts/search-conversations.sh "search-term"

# Search with more context lines
bash scripts/search-conversations.sh "search-term" --context 5

# List all saved conversations
bash scripts/search-conversations.sh --list

# Show recent conversations
bash scripts/search-conversations.sh --recent 5
```

**Common search scenarios:**

**Finding when a topic was discussed:**
```bash
bash scripts/search-conversations.sh "docker configuration"
```

**Finding command usage:**
```bash
bash scripts/search-conversations.sh "git commit" --context 10
```

**Browsing recent work:**
```bash
bash scripts/search-conversations.sh --recent 3
```

**Example workflow:**
When a user asks "when did we work on the authentication bug?" or "find conversations about database migrations", use the search script to locate relevant conversations, then read the full conversation file if needed.

### 3. Retrieve Full Conversations

To read a complete saved conversation, access the markdown files directly in `~/.claude/conversation-logs/`.

**Typical workflow:**
1. Use search to find relevant conversations
2. Note the timestamp from search results
3. Read the full markdown file: `~/.claude/conversation-logs/conversation_YYYY-MM-DD_HH-MM-SS.md`

**Quick access to latest:**
```bash
cat ~/.claude/conversation-logs/conversation_latest.md
```

## Conversation Format

Saved conversations are stored in two formats:

**JSONL (Raw):** Complete conversation data including all API messages, tool calls, and metadata. Used by the parser and for programmatic access.

**Markdown (Readable):** Human-friendly format with:
- Clear USER/ASSISTANT sections
- Tool usage summary (shows tool name and key parameters)
- Filtered system messages and noise
- Timestamps and session IDs

## Proactive Usage Guidelines

Consider saving conversations proactively when:
- A complex feature or bug fix is completed
- User indicates they're wrapping up (phrases like "that's all for now", "thanks, I'm done")
- A significant amount of work has been accomplished in the session
- User switches context significantly (new project, different task domain)

**Important:** Always ask first before saving proactively. Example: "This looks like a good stopping point. Would you like me to save this conversation for future reference?"

## Requirements

**System dependencies:**
- `python3` - Required for parsing JSONL to markdown
- `bash` - For running the scripts
- `jq` - Optional, for working with JSON metadata

**Installation check:**
```bash
command -v python3 && echo "✓ Python installed" || echo "✗ Python required"
```

## Troubleshooting

**Cannot find transcript path:**
- Check session directory: `ls -la ~/.claude/sessions/`
- Look for environment variables: `env | grep CLAUDE`
- Ask user for the transcript location

**Parser fails:**
- Verify python3 is installed and accessible
- Check that the JSONL file is valid (not corrupted)
- Fallback: Save only the JSONL file, skip markdown conversion

**Search finds nothing:**
- Verify conversations exist: `ls ~/.claude/conversation-logs/`
- Check that search term is spelled correctly
- Try broader search terms or use `--list` to see available conversations

## Resources

### scripts/

- **save-conversation.sh** - Main script to save and parse conversations
- **search-conversations.sh** - Search utility for finding past conversations
- **parse-conversation.py** - Python parser that converts JSONL to markdown

All scripts are executable and can be run directly from the skill directory.
