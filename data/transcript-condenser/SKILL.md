---
name: transcript-condenser
description: Condenses Claude Code session transcripts into readable summaries by filtering metadata, system notifications, and command artifacts. Use when the user wants to review, analyze, or understand what happened in a Claude Code session, view tool usage patterns, or export session data. Triggers when user mentions "analyze session", "review transcript", "condense logs", "what tools did I use", or similar workflow analysis requests.
---

# Transcript Condenser Skill

Condenses verbose Claude Code session transcripts from `.claude/logs/` into human-readable summaries.

## When to Use This Skill

Claude should invoke this skill when the user:
- Wants to review what happened in a Claude Code session
- Asks about tool usage patterns or statistics
- Mentions analyzing transcripts or logs
- Wants to understand workflow from a past session
- Requests session summaries or reports
- Needs to export session data for analysis

## Key Capabilities

### Output Formats
- **Markdown** (default): Human-readable timeline with session metadata and summary statistics
- **JSON**: Machine-parseable format for automated analysis or integration

### Verbosity Levels
- **Minimal**: Condensed view showing only key events and outcomes
- **Standard** (default): Balanced detail with truncated long messages
- **Detailed**: Full content including all tool parameters and complete messages

### Filtering Options
- **Tool-only view**: Show only assistant messages that used tools
- **Subagent-only view**: Show only subagent invocations and interactions
- **System message stripping**: Remove system notifications (enabled by default)

### Batch Processing
- Process entire directories of transcripts
- Automatically generate output files with consistent naming
- Progress reporting for multiple files

## Usage Examples

### Basic Usage
```bash
# Condense a single transcript to markdown (stdout)
node .claude/skills/transcript-condenser/condense-transcript.js <transcript-file>

# Save condensed version to file
node .claude/skills/transcript-condenser/condense-transcript.js <transcript-file> --output=summary.md
```

### Format Options
```bash
# Output as JSON for automated analysis
node .claude/skills/transcript-condenser/condense-transcript.js <transcript-file> --format=json --output=session.json
```

### Verbosity Control
```bash
# Minimal output (quick overview)
node .claude/skills/transcript-condenser/condense-transcript.js <transcript-file> --verbosity=minimal

# Detailed output (full content)
node .claude/skills/transcript-condenser/condense-transcript.js <transcript-file> --verbosity=detailed
```

### Filtered Views
```bash
# Show only tool usage
node .claude/skills/transcript-condenser/condense-transcript.js <transcript-file> --only-tools

# Show only subagent interactions
node .claude/skills/transcript-condenser/condense-transcript.js <transcript-file> --only-subagents
```

### Batch Processing
```bash
# Process all transcripts in a directory
node .claude/skills/transcript-condenser/condense-transcript.js logs/20251017/ --output-dir=condensed/

# Batch process with specific format
node .claude/skills/transcript-condenser/condense-transcript.js logs/20251017/ --output-dir=condensed/ --format=json
```

## Output Structure

### Markdown Format
The markdown output includes:
1. **Session Metadata**: ID, date, branch, duration, working directory, version
2. **Timeline**: Chronological event list with timestamps (relative to session start)
3. **Summary Statistics**: Tool usage counts, subagent calls, files modified, errors/warnings

### JSON Format
The JSON output provides structured data:
```json
{
  "session": {
    "id": "abc123",
    "date": "2025-10-17",
    "branch": "main",
    "duration": "5m 23s",
    ...
  },
  "timeline": [
    {
      "time": "00:00:15",
      "type": "user",
      "content": "...",
      ...
    }
  ],
  "summary": {
    "toolsUsed": { "Read": 3, "Write": 2 },
    "filesModified": 3,
    ...
  }
}
```

## Automatic Filtering

The script automatically removes noise:
- Meta messages (`isMeta: true`)
- Hook notifications
- Command clear messages
- Empty stdout
- System reminders (can be disabled with `--no-system`)

## Common Use Cases

1. **Quick Session Review**: "What did I do in my last session?"
   - Use minimal verbosity for fast overview

2. **Tool Usage Analysis**: "Which tools did I use most?"
   - Use `--only-tools` flag

3. **Subagent Tracking**: "How many times did I call the backend-architect?"
   - Use `--only-subagents` flag

4. **Batch Reporting**: "Generate reports for all sessions this week"
   - Use batch processing with output directory

5. **Data Export**: "Export session data for analysis"
   - Use JSON format for programmatic access

## Tips for Claude

- Locate transcript files in `.claude/logs/YYYYMMDD/` directories
- Transcript filenames follow pattern: `transcript_[subagent_]<sessionId>_<date>_<time>.json`
- Suggest appropriate verbosity level based on user's request:
  - "Quick look" → minimal
  - "Detailed analysis" → detailed
  - General review → standard (default)
- For batch processing, create output directory if it doesn't exist
- Always show the output file path when saving to a file

## Command Reference

```
node .claude/skills/transcript-condenser/condense-transcript.js <input> [options]

Arguments:
  input                 Path to transcript file or directory

Options:
  --format=<type>       Output format: "markdown" (default) or "json"
  --output=<file>       Output file (default: stdout)
  --output-dir=<dir>    Output directory for batch processing
  --verbosity=<level>   Level: "minimal", "standard" (default), "detailed"
  --only-tools          Show only tool usage
  --only-subagents      Show only subagent interactions
  --no-system           Strip all system messages
  --include-usage       Include token usage statistics
  --help, -h            Show help message
```

## Requirements

- Node.js 18.0.0 or higher
- No external dependencies (uses built-in Node.js modules only)
