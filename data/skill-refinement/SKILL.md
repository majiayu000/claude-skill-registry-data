---
name: skill-refinement
description: |
  Feedback-driven skill improvement through tool outcome analysis. Collects execution
  data and surfaces insights for skill refinement. Use this skill when you want to:
  - Understand how skills are performing ("show skill feedback", "how are skills doing")
  - Get insights on skill effectiveness ("skill insights", "what skills need improvement")
  - Identify skills that need improvement ("which skills have errors")
  - Analyze tool usage patterns ("what tools are failing", "error hotspots")
  - Set up feedback collection ("enable feedback", "setup feedback tracking")
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Feedback-Driven Skill Refinement

Collects PostToolUse feedback, attributes outcomes to skills semantically, and surfaces actionable insights for improving skills.

## Quick Start

```bash
# Set up feedback collection (one time)
voyager feedback setup

# Use Claude Code normally - feedback is collected automatically

# View insights
voyager feedback insights

# View insights for a specific skill
voyager feedback insights --skill session-brain --errors
```

## CLIs

### `feedback-setup` / `voyager feedback setup`

Initialize feedback collection by:
1. Creating the feedback database at `.claude/voyager/feedback.db`
2. Installing a PostToolUse hook at `.claude/hooks/post_tool_use_feedback.py`
3. Updating `.claude/settings.local.json` with hook configuration

Options:
- `--dry-run` / `-n`: Show what would be done without making changes
- `--reset`: Delete existing feedback data and start fresh
- `--db PATH`: Use a custom database path

### `skill-insights` / `voyager feedback insights`

Analyze collected feedback and generate improvement recommendations.

Options:
- `--skill SKILL` / `-s SKILL`: Filter insights for a specific skill
- `--errors` / `-e`: Show common errors
- `--json`: Output results as JSON
- `--db PATH`: Use a custom database path

## How Skill Attribution Works

The system uses a **cascade of strategies** to attribute tool executions to skills without hardcoded mappings:

1. **Transcript Context** (most accurate)
   - Checks if Claude read a SKILL.md file in this session
   - If yes, attributes subsequent tool uses to that skill

2. **Learned Associations** (fast)
   - Looks up similar tool+context patterns from past sessions
   - Improves over time as more feedback is collected

3. **ColBERT Index Query** (semantic, if available)
   - Queries the skill retrieval index with tool context
   - Works when `find-skill` command is available

4. **LLM Inference** (comprehensive, disabled by default in hooks)
   - Asks an LLM to identify the skill from context
   - Slowest but most comprehensive fallback

## Storage

- **Feedback Database**: `.claude/voyager/feedback.db` (SQLite)
- **Hook Script**: `.claude/hooks/post_tool_use_feedback.py`

### Database Schema

**tool_executions**: Per-tool execution logs
- session_id, tool_name, tool_input, tool_response
- success, error_message, duration_ms
- skill_used (attributed skill)
- timestamp

**session_summaries**: Per-session aggregates
- tools_used, skills_detected
- total/successful/failed calls
- task_completed, completion_feedback

**learned_associations**: Tool context → skill mappings
- context_key (tool|extension|command)
- skill_id, confidence, hit_count

## Insights Output

The insights command shows:

1. **Summary**: Total executions, sessions, skills detected
2. **Skill Performance**: Success rate and error counts per skill
3. **Tool Usage**: Which tools are used most, failure rates
4. **Common Errors**: Recurring error patterns
5. **Recommendations**: Actionable suggestions like:
   - "Low success rate - update SKILL.md with better guidance"
   - "Recurring error (5x): file not found..."
   - "Low usage - add more trigger phrases"

## Workflow for Improving Skills

1. Run `voyager feedback insights --errors` to see problem areas
2. Check specific skill with `voyager feedback insights --skill NAME`
3. Review the recommendations
4. Update SKILL.md or reference.md based on observed failures
5. Re-run insights periodically to track improvement

## See Also

- `reference.md` - Technical reference for implementation details
- `skills/skill-retrieval/` - Skill indexing for semantic attribution
- `skills/skill-factory/` - Creating new skills from observed patterns
