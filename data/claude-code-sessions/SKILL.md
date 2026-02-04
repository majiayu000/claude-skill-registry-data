---
name: claude-code-sessions
description: Use when user says "resume session", "what did I work on", or "find conversation about [topic]". Automatically searches, resumes, and analyzes Claude Code sessions. Handles session discovery, content search, and automatic session restoration from any directory.
---

# Claude Code Sessions Skill

Comprehensive session management for Claude Code - search, analyze, and resume conversations from any directory.

## When to Use This Skill

Use this skill when:
- Search sessions by content or keywords
- List all available sessions across projects
- Analyze session history and patterns
- Find sessions created in different directories
- Get session metadata and statistics

## Quick Start Checklist

When user wants to resume or find sessions:

```markdown
[ ] 1. Identify request type: resume by ID, search by text, or list recent
[ ] 2. If resume by ID: use 21_universal_session_resume.py with session ID
[ ] 3. If search by text: use --text flag with search keywords
[ ] 4. If list recent: use 22_list_all_sessions.py with --days filter
[ ] 5. Verify correct working directory from session metadata
[ ] 6. Launch Claude Code with proper context
```

**5-Second Decision Tree:**
- User mentions session ID? → Resume with 21_universal_session_resume.py
- User describes topic/content? → Search with --text flag
- User asks "what did I work on"? → List with 22_list_all_sessions.py

## Practical Workflow

**BEFORE attempting to resume/search:**

1. **Determine intent** (resume specific vs search vs browse recent)
2. **Choose command** based on intent:
   - Known ID → `python 21_universal_session_resume.py [ID]`
   - Topic search → `python 21_universal_session_resume.py --text "keyword"`
   - Recent work → `python 22_list_all_sessions.py --days 7`
3. **Execute command** and verify session found
4. **Resume automatically** (script handles directory switching)

**Example rapid application:**
```
User: "Resume my dashboard work from yesterday"

Agent thinks:
- Text search needed ("dashboard")
- Recent timeframe (yesterday)
- Use: python 21_universal_session_resume.py --text "dashboard" --all
- Filter results by date, pick most recent
```

## Core Capabilities

### 1. Universal Session Resume

Resume any session from any directory - automatically handles path resolution and project switching.

**CLI Usage:**
```bash
# Resume by session ID (default mode)
python data_sources/claude_code/21_universal_session_resume.py c080fd31-1fea-44e2

# Resume by ID (full UUID)
python data_sources/claude_code/21_universal_session_resume.py c080fd31-1fea-44e2-8690-c58ad0f4a829

# Search by text content (requires --text flag)
python data_sources/claude_code/21_universal_session_resume.py --text "dashboard implementation"

# Resume latest session
python data_sources/claude_code/21_universal_session_resume.py --last

# Preview command without executing
python data_sources/claude_code/21_universal_session_resume.py --dry-run c080fd31

# Show all matching sessions
python data_sources/claude_code/21_universal_session_resume.py --text "dashboard" --all
```

**Shell Alias (if configured):**
```bash
# After source ~/.zshrc
rc c080fd31-1fea-44e2                 # By ID (default)
rc --text "dashboard"                  # By text search
rc --last                              # Latest session
rc --dry-run c080fd31                  # Preview only
```

**How It Works:**
1. Scans all projects in `~/.claude/projects/`
2. Finds session regardless of creation directory
3. Determines correct working directory from session metadata
4. Automatically switches to project folder
5. Launches Claude Code with correct session context

**Parameters:**
- `session_input` (positional): Session ID (default) or search text (with --text)
- `--text`, `-t`: Treat input as text search instead of session ID
- `--last`: Find most recent session across all projects
- `--dry-run`: Show resume command without executing
- `--all`: Show all matching sessions, not just first

### 2. List All Sessions

View all Claude Code sessions grouped by project with statistics.

**CLI Usage:**
```bash
# List all sessions
python data_sources/claude_code/22_list_all_sessions.py

# Show detailed information
python data_sources/claude_code/22_list_all_sessions.py --detailed

# Filter by project path
python data_sources/claude_code/22_list_all_sessions.py --project chrome-extension-tcs

# Show only recent sessions (last 7 days)
python data_sources/claude_code/22_list_all_sessions.py --days 7
```

**Output Format:**
```
📊 Summary:
  Total projects: 5
  Total sessions: 127
  Total size: 45.32 MB

📁 Projects and Sessions:

📂 ~/project
   Sessions: 89 | Size: 32.15 MB
   Period: 2024-10-01 to 2025-01-15
   • c080fd31... (2h ago) - dashboard implementation with DataTables...
   • b2435f08... (1d ago) - fix session resume script...
   • a7f3e290... (3d ago) - Notion integration analysis...
   ... and 86 more sessions
```

**Parameters:**
- `--detailed`: Show full information for each session (first 10 per project)
- `--project`: Filter by project path (substring match)
- `--days`: Show only sessions modified in last N days

### 3. Session Search with Grep

Fast content search across all sessions using grep.

**CLI Usage:**
```bash
# Search for keyword in all sessions
grep -i "dashboard" ~/.claude/projects/-Users-*/*.jsonl

# List files containing keyword
grep -l "search_term" ~/.claude/projects/-Users-*/*.jsonl

# Search with context (2 lines before/after)
grep -C 2 "error message" ~/.claude/projects/-Users-*/*.jsonl

# Search in specific project
grep -i "dashboard" ~/.claude/projects/-Users-username-projects-project/*.jsonl
```

**Why Grep:**
- 10-100x faster than custom search tools
- Works with any content
- Simple and reliable
- Standard Unix tool

## Session Storage Structure

### Storage Location
```
~/.claude/projects/
├── -Users-Kravtsovd-projects/
│   └── b2435f08-65e2-4b88-91c6-79f3a93ced9a.jsonl
├── -Users-username-projects-project/
│   └── c080fd31-1fea-44e2-8690-c58ad0f4a829.jsonl
└── -Users-username-projects-ai-dashboards/
    └── a7f3e290-4b3c-11ef-8901-234567890abc.jsonl
```

**Directory Naming:**
- Claude Code creates unique folder for each working directory
- Path format: `-` separated segments
- Example: `~/projects` → `-Users-Kravtsovd-projects`

### Session File Format (JSONL)

Each line is a JSON object representing a message or event:

```jsonl
{"type":"system","cwd":"~/project","timestamp":"2025-01-15T10:30:00Z"}
{"type":"user","message":{"content":"implement dashboard"},"timestamp":"2025-01-15T10:30:15Z"}
{"type":"assistant","message":{"content":"I'll help..."},"timestamp":"2025-01-15T10:30:20Z"}
```

**Message Types:**
- `system`: Session metadata, cwd, environment
- `user`: User input and prompts
- `assistant`: Claude responses
- `tool_use`: Tool invocations and results

## Python API

### Session Resume

```python
from data_sources.claude_code.session_manager import ClaudeSessionManager

# Initialize manager
manager = ClaudeSessionManager()

# Resume by ID
manager.resume_session(session_id="c080fd31-1fea-44e2-8690-c58ad0f4a829")

# Resume latest
manager.resume_latest()

# Search and resume
sessions = manager.search_sessions(text="dashboard")
if sessions:
    manager.resume_session(session_id=sessions[0]['session_id'])
```

### Session Search

```python
from data_sources.claude_code.session_scanner import SessionScanner

scanner = SessionScanner()

# Search by text
results = scanner.search(
    text="dashboard implementation",
    limit=10
)

# Search by date range
results = scanner.search(
    date_from="2025-01-01",
    date_to="2025-01-15"
)

# Get all sessions
all_sessions = scanner.list_all_sessions()

# Get project sessions
project_sessions = scanner.get_project_sessions(
    project_path="~/project"
)
```

## Practical Examples

### Example 1: Resume Recent Dashboard Work

**User:** "Resume my last session about dashboard implementation"

**Agent Action:**
```bash
# Search for dashboard sessions
python data_sources/claude_code/21_universal_session_resume.py --text "dashboard implementation"

# Output:
✅ Found session!
  Session ID: c080fd31-1fea-44e2-8690-c58ad0f4a829
  Created in: ~/project
  Modified: 2025-01-15 10:30:00
  Size: 2.45 MB
  Content: implement dashboard with DataTables and real-time updates...

🚀 Resuming session...
  📁 Directory: ~/project
  🔄 Launching Claude Code...
```

### Example 2: Find All Sessions About Notion

**User:** "Show me all conversations about Notion integration"

**Agent Action:**
```bash
# Search with --all flag
python data_sources/claude_code/21_universal_session_resume.py --text "notion" --all

# Or use grep for faster search
grep -l "notion" ~/.claude/projects/-Users-*/*.jsonl
```

### Example 3: List Recent Work

**User:** "What did I work on this week?"

**Agent Action:**
```bash
python data_sources/claude_code/22_list_all_sessions.py --days 7 --detailed
```

### Example 4: Resume from Different Directory

**User:** "Resume session c080fd31 but I'm in wrong folder"

**Agent Action:**
```bash
# No problem - script handles it automatically
python data_sources/claude_code/21_universal_session_resume.py c080fd31

# Script will:
# 1. Find session in ~/.claude/projects/
# 2. Detect original working directory
# 3. cd to correct directory
# 4. Launch Claude Code with session
```

## Troubleshooting

### Session Not Found

**Problem:** `❌ No sessions found`

**Solutions:**
1. Check session ID is correct: `python data_sources/claude_code/22_list_all_sessions.py`
2. Try partial ID (first 8 characters): `rc c080fd31`
3. Search by content: `rc --text "keyword"`
4. Use `--last` for most recent: `rc --last`

### Wrong Directory

**Problem:** Session opens in wrong project folder

**Solution:** Script automatically handles this - finds correct directory from session metadata

**If still wrong:**
```bash
# Check session metadata
grep "cwd" ~/.claude/projects/-Users-*/{session_id}.jsonl

# Verify project path
python data_sources/claude_code/22_list_all_sessions.py --detailed
```

### Duplicate Sessions

**Problem:** Multiple sessions for same project

**Cause:** Claude Code creates separate folder for each unique working directory

**Solution:**
```bash
# Find duplicates
python data_sources/claude_code/22_list_all_sessions.py --detailed

# Search across all
grep -l "keyword" ~/.claude/projects/-Users-*/*.jsonl
```

## Shell Configuration (Optional)

Add to `~/.zshrc` for quick access:

```bash
# Claude Code session resume
rc() {
    python ~/project/data_sources/claude_code/21_universal_session_resume.py "$@"
}

# List sessions
rc-list() {
    python ~/project/data_sources/claude_code/22_list_all_sessions.py "$@"
}

# Quick last session
rc-last() {
    rc --last
}

# Search sessions
rc-find() {
    rc --text "$1" --all
}
```

**Usage after `source ~/.zshrc`:**
```bash
rc c080fd31                    # Resume by ID
rc --text "dashboard"          # Search by text
rc-list                        # List all
rc-last                        # Resume latest
rc-find "notion"              # Find by keyword
```

## Related Files

**Core Scripts:**
- `data_sources/claude_code/21_universal_session_resume.py` - Universal resume
- `data_sources/claude_code/22_list_all_sessions.py` - Session listing
- `data_sources/claude_code/20_find_current_session.py` - Session search

**Documentation:**
- `data_sources/claude_code/16_CLAUDE_SESSION_MANAGEMENT.md` - Session management guide
- `data_sources/claude_code/00_session_id_detection_guide.md` - Session ID detection
- `data_sources/claude_code/CLAUDE.md` - Progress summary

**Python Modules:**
- `data_sources/claude_code/claude_code_client.py` - API client
- `data_sources/claude_code/session_manager.py` - Session manager (if exists)

## Best Practices

1. **Use grep for speed** - Simple keyword search is fastest
2. **Partial IDs work** - First 8 characters usually unique: `rc c080fd31`
3. **Text search is fuzzy** - Searches first 20 messages
4. **--dry-run to preview** - Check command before executing
5. **--all for exploration** - See all matches, not just first
6. **Use --last daily** - Quick access to recent work

## Version

v1.0 (2025-01-15)

## Author

Daniel Kravtsov (daniel@improvado.io)
