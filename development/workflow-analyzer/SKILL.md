---
name: workflow-analyzer
description: Analyzes Claude Code session history to identify repeated workflows and suggest slash commands to automate them
invocation: Ask Claude to "analyze my workflows" or "find repeated patterns in my Claude Code usage"
---

# Workflow Analyzer Skill

## Purpose

This skill analyzes your Claude Code usage patterns by examining session transcripts to identify workflows you repeat frequently. It suggests specific slash commands you could create to automate these patterns, complete with time savings estimates and implementation priorities.

## When to Use

Use this skill when you want to:
- Identify repeated workflows in your Claude Code sessions
- Discover automation opportunities
- Get specific recommendations for slash commands to create
- Understand your development patterns and time investment
- Optimize your Claude Code workflow efficiency

## How It Works

This skill includes a pre-built Python analysis script that:
1. Parses session JSONL files from `~/.claude/projects/*/`
2. Identifies repeated patterns in user requests across sessions
3. Detects common workflows (git operations, documentation updates, testing cycles, etc.)
4. Generates a comprehensive report with automation recommendations

## Parameters

- **days** (optional): Number of days to analyze, defaults to 30
  - Examples: "analyze my workflows from the last 7 days", "analyze my workflows from the last 60 days"

## Analysis Criteria

The skill considers a pattern significant if it:
- Appears 3+ times in the analyzed period
- Has consistent structure across occurrences
- Represents meaningful time investment
- Could be automated as a single slash command

## Patterns Detected

The skill identifies these common workflow patterns:

1. **Git workflows**: add/commit/push sequences, branch operations, PR creation
2. **Version/publish sequences**: version bumps, plugin/marketplace updates, releases
3. **Documentation updates**: README changes, consistency checks, sync operations
4. **Implementation cycles**: plan → build → test patterns, phase-based development
5. **Test/fix cycles**: test execution, error fixing, validation loops

## Usage Instructions

When the user requests workflow analysis:

1. **Calculate date range**:
   - Use the `days` parameter if provided, otherwise default to 30
   - Calculate cutoff timestamp: `date -v-{days}d +%s` (macOS) or `date -d "{days} days ago" +%s` (Linux)

2. **Locate session files**:
   ```bash
   find ~/.claude/projects -name "*.jsonl" -type f -mtime -{days} 2>/dev/null
   ```

3. **Run analysis and generate report**:
   ```bash
   find ~/.claude/projects -name "*.jsonl" -type f -mtime -{days} 2>/dev/null | \
     python3 <skill-path>/scripts/workflow_analyzer.py
   ```

4. **Present findings**:
   - Display the complete markdown report to the user
   - Highlight top 3 automation opportunities
   - Include specific time savings estimates
   - Provide concrete next steps

## Report Deliverables

The generated report includes:

### Analysis Summary
- Time period analyzed (date range)
- Number of sessions reviewed
- Number of user prompts examined
- Total patterns detected

### High-Priority Patterns (ranked by impact)
For each pattern:
- Pattern name and description
- Frequency of occurrence
- Example user request sequences (actual prompts from sessions)
- Suggested command name (verb-noun format)
- Estimated time per occurrence and total time spent
- Potential time savings with automation

### Project-Specific Insights
- Which projects show the most repeated workflows
- Project-specific automation opportunities
- Activity distribution across projects

### Recommendations
- Which commands to create first (ranked by ROI)
- Estimated time savings for top suggestions
- Implementation complexity assessment
- Next steps for the user

## Privacy

- All analysis is performed **locally only**
- No data is sent to external services
- Session transcripts never leave the user's machine
- All processing happens in-memory with no temporary files created

## Success Criteria

This skill is successful if it:
- Accurately identifies patterns the user actually repeats
- Provides specific, actionable automation suggestions
- Shows clear time savings estimates
- Presents findings in a scannable, useful format
- Completes in reasonable time (< 2 minutes for 30 days of data)

## Example Invocations

- "Analyze my workflows"
- "What workflows am I repeating in Claude Code?"
- "Analyze my workflows from the last 60 days"
- "Find automation opportunities in my Claude Code usage"
- "Show me what I'm doing repeatedly"

## Notes

- The skill focuses on user prompts, not system messages or command outputs
- Patterns must appear 3+ times to be considered significant
- Time estimates are based on typical workflow execution times
- Suggested command names follow verb-noun convention (e.g., `/ship-git`, `/publish-plugin`)
