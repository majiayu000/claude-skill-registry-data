---
name: mining-session-patterns
description: Extract actionable patterns from Claude Code session JSONL files. Surfaces error→fix sequences, tool failure rates, and cost-per-story signals for compound learning.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Glob, Grep, Write
  argument-hint: "[time-range] [output-path]"
  context: fork
  stability: development
---

# Session Pattern Mining

**Target**: $ARGUMENTS

Mines Claude Code session transcripts for recurring patterns that feed
compound learning. Converts raw session data into actionable improvements.

## Arguments

| Position | Name | Required | Default | Description |
|----------|------|----------|---------|-------------|
| 1 | `time-range` | no | `7d` | Period to scan. E.g. `7d`, `30d`, `this-week`. |
| 2 | `output-path` | no | `docs/patterns/session-patterns.md` | Where to write findings. |

**Examples:**

```text
/mining-session-patterns                    # Last 7 days, default output
/mining-session-patterns 30d                # Last 30 days
/mining-session-patterns 7d ./patterns.md   # Custom output path
```

## Data Source

```text
~/.claude/projects/*/*.jsonl    # Session transcripts
```

**Critical**: Never bulk-read full `.jsonl` files. Use sampling strategy below
to respect context budget.

## Workflow

1. **Discover session files** — Glob `~/.claude/projects/*/*.jsonl`. Filter by
   mtime within `time-range`. Select up to **10 files**, preferring recent.

2. **Sample each file** — Read **first 20 lines** + **last 20 lines** per file.
   This captures session setup (tools, config) and final outcomes (errors,
   completions). Skip files smaller than 5 lines.

3. **Extract patterns** from sampled lines:

   - **Error-fix sequences**: Tool call with error response followed by a
     successful retry or different approach. Look for `type: "tool_error"` or
     error messages in tool results, then the next tool call on the same target.
   - **Tool failure rates**: Count tool calls and failures per tool type
     (Bash, Edit, Read, Grep, Glob, Write). A failure is any tool result
     containing error indicators.
   - **Cost signals**: Estimate token usage per session from message counts
     and approximate message sizes. Map to task complexity (small/medium/large)
     based on message count thresholds: <20 small, 20-80 medium, >80 large.

4. **Format findings** — Structure as tables per Output Format below.
   Every row must suggest a concrete improvement or be omitted.

5. **Write output** — Write to `output-path`. Create parent directories
   if needed.

## Output Format

```markdown
# Session Patterns — <start-date> to <end-date>

## Error-Fix Sequences
| Error Pattern | Recovery Strategy | Frequency | Candidate Learning |
|---------------|-------------------|-----------|-------------------|
| <tool>: <error summary> | <what worked> | N occurrences | <rule or skill suggestion> |

## Tool Failure Rates
| Tool | Calls | Failures | Rate | Common Cause |
|------|-------|----------|------|--------------|
| Bash | N | N | N% | <top failure reason> |

## Cost Signals
| Session | Messages | Est. Tokens | Task Complexity |
|---------|----------|-------------|-----------------|
| <uuid-short> | N | ~Nk | small/medium/large |

## Recommended Actions
- <Concrete improvement derived from patterns above>
```

## Quality Check

- Every table row is **actionable** — suggests a specific improvement
- Findings trace to specific session files (cite UUID prefix)
- Output stays under ~100 lines — summarize, don't dump
- Correct > Complete > Minimal (ACE-FCA)
- If no meaningful patterns found, say so explicitly rather than padding

## Common Pitfalls

- **Reading full transcripts**: Sample only. First 20 + last 20 lines.
- **Max 10 files**: Don't exceed. Prefer recent files over completeness.
- **False patterns**: 1-2 occurrences are anecdotes, not patterns. Minimum 3
  occurrences before reporting as a pattern.
- **Data dumps**: Interpret the data. Raw counts without analysis are noise.
