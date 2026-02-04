---
name: session-analyzer
description: Discovers and lists Claude Code session transcripts from .claude/logs/ for analysis. Use when the user wants to find available sessions, view session timelines, identify which sessions to analyze for workflow improvements, or understand session history. Triggers when user mentions "what sessions do I have", "analyze my workflow", "show my recent sessions", "find transcripts from [date]", or similar session discovery requests.
---

# Session Analyzer Skill

Discovers and analyzes Claude Code session transcripts from `.claude/logs/` directory to help users understand their development workflow and identify optimization opportunities.

## When to Use This Skill

Claude should invoke this skill when the user:
- Wants to see available Claude Code sessions
- Asks about recent development sessions or workflow history
- Mentions analyzing workflow patterns or efficiency
- Needs to find transcripts from a specific date
- Wants to understand subagent usage across sessions
- Requests session discovery or listing

## Current Status

**Implemented Features:**
- ✅ Auto-discovery of session logs from `.claude/logs/`
- ✅ Date-based session listing and filtering
- ✅ Session grouping (main + subagent transcripts)
- ✅ Timeline display with start times
- ✅ Colored terminal output
- ✅ Date validation and formatting

**Planned Features** (not yet implemented):
- 🚧 Transcript parsing and correlation
- 🚧 Workflow analysis (task decomposition, handoffs, bottlenecks)
- 🚧 Metrics extraction (duration, success rate, tool usage)
- 🚧 Subagent orchestration evaluation
- 🚧 Code quality assessment
- 🚧 Recommendation generation
- 🚧 Report export (markdown format)

## Key Capabilities

### Session Discovery
- Automatically scans `.claude/logs/` directory for session transcripts
- Identifies and groups related main and subagent transcripts
- Sorts sessions chronologically (newest first)
- Displays human-readable date formatting

### Session Information
For each session, displays:
- **Session ID**: Short identifier (first 8 chars of UUID)
- **Start Time**: Precise timestamp (HH:MM:SS)
- **Main Transcript**: Filename of primary session
- **Subagent Count**: Number of related subagent transcripts

### Date Filtering
- Filter sessions by specific date (YYYYMMDD format)
- View all sessions from a particular day
- Navigate through session history by date

## Usage Examples

### List All Available Sessions
```bash
# Shows all dates with available sessions
node .claude/skills/session-analyzer/analyze-session.js
```

Output:
```
Available Claude Code session logs:

  1. October 17, 2025 (20251017)
  2. October 12, 2025 (20251012)
  3. October 7, 2025 (20251007)

Run with date to analyze:
  node analyze-session.js 20251017
```

### List Sessions for Specific Date
```bash
# Shows all sessions from October 17, 2025
node .claude/skills/session-analyzer/analyze-session.js 20251017
```

Output:
```
Sessions for October 17, 2025:

  1. Session abc123de
     Time: 14:32:15
     Main: transcript_abc123de_20251017_143215.json
     Subagents: 8

  2. Session def456gh
     Time: 09:15:42
     Main: transcript_def456gh_20251017_091542.json
     Subagents: 3

Run with session ID to analyze:
  node analyze-session.js 20251017 abc123de
```

### Analyze Specific Session
```bash
# Analyzes session abc123de from October 17, 2025
node .claude/skills/session-analyzer/analyze-session.js 20251017 abc123de
```

Output (current implementation shows basic info, detailed analysis coming):
```
Analyzing session: abc123de
Date: October 17, 2025
Main transcript: transcript_abc123de_20251017_143215.json
Subagent transcripts: 8

Subagent transcripts:
  - transcript_subagent_backend_abc123de_20251017_143220.json
  - transcript_subagent_frontend_abc123de_20251017_143245.json
  ...

Analysis complete! (Implementation pending)

Next steps:
  - Add transcript parsing logic
  - Implement workflow analysis
  - Generate metrics and recommendations
```

## Transcript File Patterns

The script recognizes these filename patterns:
- **Main transcripts**: `transcript_<sessionId>_<YYYYMMDD>_<HHMMSS>.json`
- **Subagent transcripts**: `transcript_subagent_<sessionId>_<YYYYMMDD>_<HHMMSS>.json`

Session grouping is based on the session ID portion of the filename.

## Common Use Cases

1. **Session Discovery**: "What sessions do I have from this week?"
   - Use without arguments to list all dates
   - Then specify date to see sessions

2. **Recent Activity Review**: "Show me today's Claude sessions"
   - Use with today's date in YYYYMMDD format

3. **Workflow Analysis Prep**: "Find the session where I built the API"
   - List sessions by date, identify by timestamp

4. **Subagent Usage Tracking**: "How many subagents did I use yesterday?"
   - View session list with subagent counts

## Tips for Claude

- Default logs directory is `.claude/logs/` in the current project
- Date format must be YYYYMMDD (e.g., 20251017)
- Session IDs are displayed as short 8-character identifiers (first part of UUID)
- When user asks about "recent sessions", show the most recent date's sessions
- Suggest running the transcript-condenser skill on specific sessions for detailed analysis
- If logs directory doesn't exist, inform user that logging may not be enabled

## Command Reference

```
node .claude/skills/session-analyzer/analyze-session.js [date] [sessionId]

Arguments:
  date       (optional) Session date in YYYYMMDD format (e.g., 20251017)
  sessionId  (optional) Short session ID to analyze (requires date)

Options:
  --help, -h  Show help message

Examples:
  node analyze-session.js                  # List all available session dates
  node analyze-session.js 20251017         # List sessions from Oct 17, 2025
  node analyze-session.js 20251017 abc123  # Analyze specific session
```

## Integration with Other Skills

**Workflow recommendation**: After discovering sessions with this skill, use the **transcript-condenser** skill to generate detailed reports:

```bash
# 1. Find sessions
node .claude/skills/session-analyzer/analyze-session.js 20251017

# 2. Condense specific session
node .claude/skills/transcript-condenser/condense-transcript.js \
  .claude/logs/20251017/transcript_abc123de_20251017_143215.json \
  --output=session-report.md
```

## Development Roadmap

Future enhancements will add:
1. **Transcript Parsing**: Load and parse JSON session data
2. **Correlation Engine**: Link subagent transcripts to main session events
3. **Workflow Metrics**: Calculate efficiency metrics, tool usage patterns
4. **Bottleneck Detection**: Identify slow operations and optimization opportunities
5. **Quality Scoring**: Evaluate code quality and testing coverage
6. **Actionable Recommendations**: Generate specific improvement suggestions
7. **Report Generation**: Export findings as markdown reports

## Requirements

- Node.js 18.0.0 or higher
- No external dependencies (uses built-in Node.js modules only)
- Requires `.claude/logs/` directory with session transcripts
