---
name: share-session
description: Convert and share Claude Code conversation sessions as readable markdown files. Use when user wants to share a session transcript, export conversation history, or create a shareable markdown document from a Claude Code session. Triggered by requests like "share this session", "export conversation", "convert session to markdown".
---

# Share Session

## Overview

Convert Claude Code sessions into readable markdown format for easy sharing. This skill finds sessions by fuzzy matching todo items and generates well-formatted markdown documents.
If this is loaded by user's explicit request but no comments there, just execute followings.

## Workflow

### Step 1: CRITICAL - Create Todo for Session Identification

**MANDATORY**: You MUST use TodoWrite tool to create a todo item that describes **what this session is about**.

**IMPORTANT**: You do NOT need to know the session ID. Describe the session content instead.

**CORRECT Usage:**
```python
TodoWrite(todos=[{
    "content": "share this session about ccusage integration and time tracking",
    "status": "in_progress",
    "activeForm": "Sharing session"
}])
```

**Good Examples (describe session topic):**
- ✅ "share this session about ccusage integration"
- ✅ "export conversation on implementing time tracking"
- ✅ "share current session with share-session improvements"

**Bad Examples (using session ID directly):**
- ❌ "get session id of 62d3a2b2-102c-43d3-8414-0a30d7a5e5e0" (you don't know session ID yet!)
- ❌ "export 62d3a2b2" (session ID unknown)

**How it works:**
1. You create todo with **session description**
2. Claude Code saves todo as: `~/.claude/todos/{SESSION-ID}.json`
3. Script searches todo **content** using fuzzy matching (60% threshold)
4. Script extracts SESSION-ID from the matching todo **filename**
5. Script uses that SESSION-ID to find transcript

**Why this is required:**
- Without a todo, the script has no way to identify which session to export
- The todo file name is the ONLY place where session ID is stored
- Fuzzy matching allows flexible queries ("share this session" matches multiple variations)

**Common mistakes:**
- ❌ Forgetting to call TodoWrite before running the script
- ❌ Using session ID in todo content (you don't know it yet!)
- ❌ Query in Step 2 doesn't match todo content at all

### Step 2: Run share_session.py

**IMPORTANT**: Always use the ABSOLUTE path to the script:

```bash
uv run --script /Users/yeongyu/local-workspaces/advanced-claude-code/claude-code-plugins/cc-plus/skills/share-session/scripts/share_session.py "your search query"
```

**The search query should match your todo content from Step 1.**

The script automatically:
- Searches todos using fuzzy matching (60% threshold)
- Locates transcript at `~/.claude/projects/*/{session-id}.jsonl`
- Merges pre-compact backups if they exist
- **Fetches accurate cost/token data from ccusage** (NOT LiteLLM)
- Converts to markdown with full statistics
- **Truncates before /share command** (excludes the share request itself)
- Saves to `/tmp/claude-code-sessions/{session-id}-{timestamp}.md`
- Copies the file path to clipboard
- Displays success message with cost breakdown

### Step 3: Output

The script displays:
```
✅ Markdown saved to:
/tmp/claude-code-sessions/{session-id}-{timestamp}.md

💰 Total Session Cost: $X.XXXXXX

📋 The path has been copied to your clipboard.
```

## Generated Markdown Format

The script generates comprehensive markdown with:

**Session Metadata:**
- 📊 Session ID, generation timestamp, message count
- 🔄 Models used (from ccusage data)

**Content:**
- 💬 User messages with timestamps (meta messages filtered)
- 🤖 Assistant responses with timestamps
- 🧠 Thinking process (when available, shown as nested quotes)
- 🔧 Tool usage details (collapsed in `<details>` tags)
- 🚀 Subagent calls (Task tool usage)

**Cost & Token Statistics (from ccusage):**
- 💰 Total session cost (accurate calculation from ccusage)
- 📊 Token breakdown:
  - Input tokens
  - Output tokens
  - Cache creation tokens
  - Cache read tokens
  - Total tokens
- 🎯 Cache hit rate percentage
- 📉 Average cost per message

**Session Timeline (NEW):**
- ⏱️ **Total Session Time**: First message → Last message
- 🟢 **LLM Active Time**: User question → Last assistant response (per turn)
- 🟡 **LLM Idle Time**: Last assistant → Next user question
- 📊 **LLM Utilization**: (Active Time / Total Time) × 100%

**Special Features:**
- 📦 Compact markers shown for merged pre-compact backups
- 🔪 Auto-truncates before `/share` command (excludes the export request itself)
- 🔄 Multi-model support (tracks different models per message)

## Script

### share_session.py

**The only script you need.** Does everything from search to markdown generation.

**Usage:**
```bash
uv run --script /Users/yeongyu/local-workspaces/advanced-claude-code/claude-code-plugins/cc-plus/skills/share-session/scripts/share_session.py <query>
```

**Dependencies (auto-installed by uv):**
- `orjson`: Fast JSON parsing
- `thefuzz`: Fuzzy string matching for todo search
- `rich`: Terminal formatting and progress display

**Complete features:**
- ✅ Fuzzy search through todo files (60% threshold)
- ✅ Automatic pre-compact backup merging
- ✅ **Accurate cost/token data from ccusage** (via `bunx --bun ccusage session -i`)
- ✅ **Turn-based time tracking**:
  - LLM Active Time (user → last assistant per turn)
  - LLM Idle Time (last assistant → next user)
  - Utilization percentage
- ✅ Auto-truncation before `/share` command
- ✅ Multi-model session support (from ccusage data)
- ✅ Clipboard integration (macOS `pbcopy`)
- ✅ Rich terminal output with colored progress
- ✅ TypedDict-based type safety

**Output:** File path (stdout) + clipboard

**Exit codes:**
- 0: Success
- 1: Session not found or conversion failed

**Performance:**
- Typical execution: 2-5 seconds
- Timeout: 30 seconds (for ccusage call)

## Error Handling

**No session found:**
- ❌ **Cause**: Todo item not created or query doesn't match
- ✅ **Solution**:
  1. Verify you called `TodoWrite` in Step 1
  2. Check query matches todo content (60% fuzzy threshold)
  3. Try exact session ID if known

**Transcript not found:**
- ❌ **Cause**: Session ID extracted but transcript missing
- ✅ **Solution**:
  1. Confirm session ID is correct
  2. Check `~/.claude/projects/` directory exists
  3. Look for `{session-id}.jsonl` file
  4. Check pre-compact backups at `~/.claude/pre-compact-session-histories/`

**ccusage data fetch failed:**
- ⚠️ **Symptom**: "Could not fetch session usage data from ccusage"
- ❌ **Possible causes**:
  1. `ccusage` command not available (check `bunx --bun ccusage --version`)
  2. Session ID not found in ccusage database
  3. JSON parsing error from ccusage output
- ✅ **Impact**: Markdown still generated but without cost/token statistics
- ✅ **Fallback**: Warning message displayed, conversion continues

**Conversion failed:**
- ❌ **Cause**: JSONL parsing or markdown generation error
- ✅ **Solution**:
  1. Check transcript file is valid JSONL (each line = valid JSON)
  2. Review error message from stderr
  3. Check for corrupted transcript data

**Clipboard copy failed:**
- ⚠️ **Symptom**: "Warning: Could not copy to clipboard"
- ❌ **Cause**: `pbcopy` command failed (macOS only)
- ✅ **Impact**: Non-critical - file path still shown in stdout
- ✅ **Workaround**: Manually copy the displayed path

## Troubleshooting

**Script says "No session found" even though todo exists:**
```bash
# Check if todo file exists
ls -la ~/.claude/todos/ | grep $(date +%Y-%m-%d)

# Verify todo content
cat ~/.claude/todos/{session-id}*.json | jq .
```

**Want to export specific session by ID:**
```bash
# Create todo with exact session ID
TodoWrite(todos=[{"content": "export {exact-session-id}", "status": "in_progress", "activeForm": "Exporting"}])

# Then run with session ID
uv run --script ... "{exact-session-id}"
```

**ccusage returns wrong data:**
- Verify ccusage version: `bunx --bun ccusage --version`
- Test ccusage directly: `bunx --bun ccusage session -i {session-id} --json`
- Check if session exists: `bunx --bun ccusage session`
