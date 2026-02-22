---
name: claude-session-tools
description: This skill should be used when the user asks to "find Claude sessions", "explore session history", "search Claude sessions", "analyze session", "list sessions", "extract session content", "export Claude sessions", "find tool usage in sessions", "session timeline", mentions "Claude Code session.jsonl files", or needs to explore, search, analyze, or export Claude Code session histories stored in ~/.claude/projects/.
version: "2.0.0"

# VISIBILITY & TRIGGERING
user-invocable: true
disable-model-invocation: false

# EXECUTION CONTEXT - Tools this skill can use
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# Claude Session Tools

General-purpose tool for exploring, searching, analyzing, and exporting Claude Code session histories stored in `~/.claude/projects/`.

**Usage:**
- `/ar:claude-session-tools` - Show full guide
- `/ar:claude-session-tools list <PROJECT>` - List all sessions for a project
- `/ar:claude-session-tools search <PATTERN>` - Search sessions for pattern
- `/ar:claude-session-tools extract <PROJECT> <SESSION-ID> <TYPE>` - Extract specific content
- `/ar:claude-session-tools analyze <PROJECT> <SESSION-ID>` - Analyze session structure
- `/ar:claude-session-tools timeline <PROJECT> <SESSION-ID>` - Show chronological timeline
- `/ar:claude-session-tools cross-ref <PROJECT> <SESSION-ID> <FILE>` - Cross-reference with file
- `/ar:claude-session-tools find-tool <TOOL> <PATTERN>` - Find specific tool usage
- `/ar:claude-session-tools corrections [PROJECT]` - Find user correction patterns
- `/ar:claude-session-tools find-commands <PATTERN> [CONTEXT]` - Search for command patterns
- `/ar:claude-session-tools planning-usage` - Analyze planning command usage
- `/ar:claude-session-tools export <PROJECT> <SESSION-ID> [OUTPUT]` - Export session to markdown
- `/ar:claude-session-tools export-recent [DAYS] [OUTPUT]` - Export recent sessions to single file

## Arguments

This command accepts arguments for automated operations:

```
$ARGUMENTS
```

## Operations

### Session Discovery

**`list <PROJECT>`**
Show all sessions for a project with metadata.

```
/ar:claude-session-tools list repomix
```

### Content Extraction

**`extract <PROJECT> <SESSION-ID> <TYPE>`**
Extract specific content type from a session.

Types: `pbcopy`, `bash-output`, `user-prompts`, `assistant-responses`, `tool-usage`, `all`

```
/ar:claude-session-tools extract repomix 6ab3b336 user-prompts
/ar:claude-session-tools extract repomix 6ab3b336 pbcopy
```

### Analysis Operations

**`search <PATTERN>`**
Find pattern across all sessions and projects.

```
/ar:claude-session-tools search "your-pattern"
/ar:claude-session-tools search "function-name"
```

**`analyze <PROJECT> <SESSION-ID>`**
Show session structure and statistics.

```
/ar:claude-session-tools analyze repomix 6ab3b336
```

**`timeline <PROJECT> <SESSION-ID>`**
Show chronological timeline of events in a session.

```
/ar:claude-session-tools timeline repomix 6ab3b336
```

### Advanced Analysis

**`find-tool <TOOL> [PATTERN]`**
Find usage of specific tools (Read, Edit, Bash, Grep, etc.).

```
/ar:claude-session-tools find-tool Bash "grep"
/ar:claude-session-tools find-tool Edit
/ar:claude-session-tools find-tool Read "gitLogHandle"
```

**`corrections [PROJECT]`**
Find user correction patterns across sessions.

Categories: `regression`, `skip_step`, `misunderstanding`, `incomplete`
Detects patterns like "you forgot", "wrong", "actually", "nono", etc.

```
/ar:claude-session-tools corrections
/ar:claude-session-tools corrections repomix
```

**`find-commands <PATTERN> [CONTEXT]`**
Search for command patterns with context.
Context: Number of following messages to include (default: 5)

```
/ar:claude-session-tools find-commands "git commit"
/ar:claude-session-tools find-commands "/ar:plan" 3
```

**`planning-usage`**
Analyze planning command usage across all sessions.
Shows frequency by command and by project.

```
/ar:claude-session-tools planning-usage
```

### Cross-Reference

**`cross-ref <PROJECT> <SESSION-ID> <FILE>`**
Cross-reference session changes with file to verify what was applied.

```
/ar:claude-session-tools cross-ref repomix 6ab3b336 PR-DESCRIPTION.md
```

### Export Operations

**`export <PROJECT> <SESSION-ID> [OUTPUT]`**
Export single session to markdown file.

Output includes:
- Session metadata (date, git branch, working directory)
- All user messages (filtered, cleaned)
- Compact session summary if available

```
/ar:claude-session-tools export repomix 6ab3b336 session.md
/ar:claude-session-tools export repomix 6ab3b336 output.md
```

**`export-recent [DAYS] [OUTPUT]`**
Export all sessions from last N days to single markdown file.

```
/ar:claude-session-tools export-recent 7 weekly_sessions.md
/ar:claude-session-tools export-recent 2 recent.md
```

## Command Aliases

For faster typing, these commands have short aliases:

| Full Command | Short Alias |
|--------------|-------------|
| `find-tool` | `ft` |
| `find-commands` | `fc` |
| `planning-usage` | `pu` |
| `export-recent` | `er` |

```
/ar:claude-session-tools ft Bash "grep"
/ar:claude-session-tools fc "git commit"
/ar:claude-session-tools pu
/ar:claude-session-tools er 7 weekly.md
```

## CLI Parameter Overrides

All configuration values can be overridden via CLI flags following typer/click patterns:

**Environment variable:** `SESSION_TOOLS_PREVIEW_LIMIT`
**CLI flag:** `--preview-limit N`
**Priority:** CLI flag > Environment variable > Default

```
# Override preview limit via CLI
/ar:claude-session-tools search "pattern" --preview-limit 200

# Override projects directory
/ar:claude-session-tools list myproject --projects-dir /custom/path/to/projects

# Override result limits
/ar:claude-session-tools corrections --max-results-per-project 5 --max-results-total 20
```

**Available CLI parameters:**
- `--projects-dir <PATH>` - Override CLAUDE_PROJECTS_DIR
- `--preview-limit <N>` - Override SESSION_TOOLS_PREVIEW_LIMIT
- `--context-limit <N>` - Override SESSION_TOOLS_CONTEXT_LIMIT
- `--display-limit <N>` - Override SESSION_TOOLS_DISPLAY_LIMIT
- `--extract-limit <N>` - Override SESSION_TOOLS_EXTRACT_LIMIT
- `--tool-content-limit <N>` - Override SESSION_TOOLS_TOOL_CONTENT_LIMIT
- `--max-results <N>` - Override SESSION_TOOLS_MAX_RESULTS (per project)
- `--max-results-total <N>` - Override SESSION_TOOLS_MAX_RESULTS_TOTAL

## Multi-Layer Verification Strategy

When verifying that changes were applied correctly:

### Layer 1: Content Classification
Identify all content types being modified:
- Tool outputs (Bash, Edit, Read results)
- User prompts and discussions
- Assistant responses and reasoning
- Code snippets and examples
- Structured data (tables, lists, configurations)

### Layer 2: Temporal Ordering
Track chronological sequence of events:
1. Extract all events with timestamps
2. Group by content type
3. Identify iterations and refinements
4. Note which version was finalized

### Layer 3: Change Detection
Look for specific patterns of change:
- **Content reordering** (items moved, sections rearranged)
- **Introductions** (headers, context lines added)
- **Format changes** (table structure, layout updates)
- **Terminology shifts** (new terms introduced, old ones removed)

### Layer 4: File Cross-Reference
Compare current files against session changes:
1. Extract all content from session
2. Compare against current file version
3. Identify which changes were applied
4. Flag any missing or incomplete updates

### Layer 5: Pattern Matching
Use distinctive markers to find specific changes:
- Search for unique phrases
- Look for section headers that changed
- Find example commands
- Identify table column changes

## Common Search Patterns

### Find all code discussions
```
/ar:claude-session-tools search "function"
/ar:claude-session-tools search "class"
/ar:claude-session-tools search "interface"
```

### Find specific operations
```
/ar:claude-session-tools search "git commit"
/ar:claude-session-tools search "npm run"
/ar:claude-session-tools search "pytest"
```

### Find all tool usage
```
/ar:claude-session-tools find-tool Bash
/ar:claude-session-tools find-tool Edit
/ar:claude-session-tools find-tool Read
/ar:claude-session-tools find-tool Grep
```

### Find discussion topics
```
/ar:claude-session-tools search "error"
/ar:claude-session-tools search "refactor"
/ar:claude-session-tools search "optimization"
```

## Session File Structure

Sessions are stored as `.jsonl` files (JSON Lines format) at:
```
~/.claude/projects/<ENCODED-PATH>/
  ├── <SESSION-ID>.jsonl
  ├── agent-<ID>.jsonl
  └── ...
```

The `<ENCODED-PATH>` is the project directory path with `/` replaced by `-`:
- macOS: `/Users/<user>/project` → `-Users-<user>-project`
- Linux: `/home/<user>/project` → `-home-<user>-project`
- Windows: `C:\Users\<user>\project` → `C--Users-<user>-project`

Each line is a complete JSON object:

```json
{
  "type": "user|assistant|system",
  "timestamp": "2025-11-25T20:30:15.744Z",
  "message": {
    "content": [
      {
        "type": "text|tool_use|tool_result",
        "text": "...",
        "name": "ToolName",
        "input": { /* tool input */ },
        "content": "..."
      }
    ]
  }
}
```

### Common Tool Types

- **Bash**: Shell command execution
- **Read**: File content reading
- **Edit**: File modification
- **Write**: New file creation
- **Grep**: Pattern searching in files
- **Glob**: File pattern matching
- **TodoWrite**: Task list management
- **Task**: Launch specialized agents

## Exploration Workflow

### 1. List and understand available sessions
```
/ar:claude-session-tools list myproject
```
Identify which session contains the work you want to verify.

### 2. Extract relevant content
```
/ar:claude-session-tools extract myproject SESSION_ID user-prompts
/ar:claude-session-tools extract myproject SESSION_ID pbcopy
```
See what was asked/discussed and what was copied to clipboard.

### 3. Analyze changes
```
/ar:claude-session-tools analyze myproject SESSION_ID
```
Understand scale and scope of changes.

### 4. Cross-reference with files
```
/ar:claude-session-tools cross-ref myproject SESSION_ID path/to/file.md
```
Verify all changes were applied.

### 5. Deep dive into specifics
```
/ar:claude-session-tools find-tool Edit "filename"
/ar:claude-session-tools search "specific-phrase"
```
See all edits to specific file or find when something was discussed.

## Tips and Best Practices

1. **Always extract complete content** - Don't rely on truncated previews
2. **Use timestamps to verify order** - Chronological sequence matters
3. **Cross-reference multiple sources** - Compare tool outputs with file results
4. **Search broadly first** - Find all mentions before deep dive
5. **Classify by content type** - Group similar changes together
6. **Document your findings** - Create a change log as you verify
7. **Look for approval markers** - Find where changes were confirmed as final
8. **Check tool outputs** - Verify tools returned what was expected
9. **Track iterations** - Note how ideas evolved and improved
10. **Note dependencies** - Understand what depended on what

## Verification Checklist

When verifying changes were applied:

- [ ] List all sessions with relevant work
- [ ] Extract all content from each session (user prompts, responses, tool outputs)
- [ ] Classify each piece of content by type
- [ ] Identify the final/authoritative version of each change
- [ ] Compare against current file state
- [ ] Note any iterations or alternatives discussed
- [ ] Mark which changes were applied
- [ ] Flag any missing or incomplete updates
- [ ] Document the verification process
- [ ] Create summary of what changed and why

## Export for Documentation

### Single Session Export

Export a complete session for documentation:

```
/ar:claude-session-tools export myproject SESSION_ID documentation/session-analysis.md
```

### Bulk Export

Export recent sessions for comprehensive context:

```
/ar:claude-session-tools export-recent 7 documentation/weekly-work.md
```

### Integration with Notes

Append session history to project notes:

```
echo "" >> notes/investigation.md
echo "## Claude Session History" >> notes/investigation.md
/ar:claude-session-tools export myproject SESSION_ID - >> notes/investigation.md
```

## Migration from Legacy Skills

This unified skill replaces two legacy skills:

### From claude-code-session-explorer

| Old Command | New Command | Notes |
|-------------|-------------|-------|
| `/ar:claude-code-session-explorer list` | `/ar:claude-session-tools list` | Same syntax |
| `/ar:claude-code-session-explorer search` | `/ar:claude-session-tools search` | Same syntax |
| `/ar:claude-code-session-explorer extract` | `/ar:claude-session-tools extract` | Same syntax |
| `/ar:claude-code-session-explorer analyze` | `/ar:claude-session-tools analyze` | Same syntax |
| `/ar:claude-code-session-explorer timeline` | `/ar:claude-session-tools timeline` | Same syntax |
| `/ar:claude-code-session-explorer find-tool` | `/ar:claude-session-tools find-tool` or `ft` | Same syntax |
| `/ar:claude-code-session-explorer corrections` | `/ar:claude-session-tools corrections` | Same syntax |
| `/ar:claude-code-session-explorer find-commands` | `/ar:claude-session-tools find-commands` or `fc` | Same syntax |
| `/ar:claude-code-session-explorer planning-usage` | `/ar:claude-session-tools planning-usage` or `pu` | Same syntax |
| `/ar:claude-code-session-explorer cross-ref` | `/ar:claude-session-tools cross-ref` | Same syntax |

### From export-claude-sessions

| Old Command | New Command | Notes |
|-------------|-------------|-------|
| `./export_claude_session.sh <id> <output>` | `/ar:claude-session-tools export <project> <id> <output>` | Now requires project argument |
| `./export_recent_claude_sessions.sh <days> <output>` | `/ar:claude-session-tools export-recent <days> <output>` | Same syntax |

All functionality from both legacy skills is preserved in the unified skill.

## Advanced Usage

### Finding Related Sessions
```
/ar:claude-session-tools search "PR-DESCRIPTION"
```
Finds all sessions that worked on this file.

### Tracking Evolution of Ideas
```
/ar:claude-session-tools timeline myproject SESSION_ID
```
Shows how discussion evolved chronologically.

### Comparing Multiple Sessions
```
/ar:claude-session-tools list myproject
```
List all, then compare specific ones.

### Understanding Decision Points
```
/ar:claude-session-tools search "should we"
/ar:claude-session-tools search "what about"
```
Find where decisions were made.

## Configuration

### Environment Variables

All limits and settings can be configured via environment variables:

```bash
# Display limits
export SESSION_TOOLS_PREVIEW_LIMIT=100
export SESSION_TOOLS_CONTEXT_LIMIT=500
export SESSION_TOOLS_DISPLAY_LIMIT=150
export SESSION_TOOLS_EXTRACT_LIMIT=300
export SESSION_TOOLS_TOOL_CONTENT_LIMIT=200

# Session discovery
export CLAUDE_PROJECTS_DIR=~/.claude/projects

# Content filtering
export SESSION_TOOLS_SYSTEM_PATTERNS='[Request interrupted,<task-notification>,<system-reminder>'

# Result limits
export SESSION_TOOLS_MAX_RESULTS=3
export SESSION_TOOLS_MAX_RESULTS_TOTAL=10

# Export defaults
export SESSION_TOOLS_EXPORT_TEMPLATE='session_{session_id}.md'
export SESSION_TOOLS_RECENT_TEMPLATE='recent_sessions.md'

# Pattern customization
export SESSION_TOOLS_CORRECTION_PATTERNS='you deleted,you forgot,wrong,mistake'
export SESSION_TOOLS_PLANNING_COMMANDS='/ar:plannew,/ar:planrefine,/ar:planupdate,/ar:planprocess'
```

## Customization

You can use custom instructions with `/ar:claude-session-tools` to:
- Create verification reports for specific projects
- Build change logs
- Track evolution of features
- Document decision-making processes
- Generate session summaries
- Compare different approaches
- Analyze patterns in your workflow

Simply provide your custom instruction after invoking the command!
