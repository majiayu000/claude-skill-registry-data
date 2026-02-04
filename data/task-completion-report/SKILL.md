---
name: task-completion-report
description: Generate a detailed task completion report for any milestone spec, showing overall completion percentage, per-phase breakdown with progress bars, and status indicators. Invoked when user asks for progress tracking, phase summaries, completion reports, or needs to assess work status before PR/merge.
allowed-tools: Read, Bash
---

# Task Completion Report Generator

## Purpose

This skill generates a detailed, formatted task completion report by analyzing any milestone spec's `tasks.md` file. It provides:

- **Overall completion percentage** across all phases
- **Per-phase breakdown** with visual progress bars
- **Status indicators** (✅ Complete, 🟢 Near Complete, 🔄 In Progress, 🟡 Started, 📋 Pending)
- **Phase details** showing completed vs total tasks per phase

## When to Use This Skill

Claude should invoke this skill when:
- User asks: "What's our progress on [phase/milestone]?"
- User requests: "Generate a completion report"
- User needs: "Phase summary", "Task status", "Are we done with milestone 2?"
- User checking: "What percentage of core mechanics is complete?"
- Context mentions: progress tracking, status check, release readiness, quality metrics

## How the Skill Works

The skill uses a pre-built Python script (`scripts/task-completion-report.py`) that:
1. Parses the tasks.md file for the specified milestone
2. Detects all phase headers (Phase 1-5, Phase 4a-h, etc.)
3. Counts completed tasks (marked with ✅) vs incomplete tasks (marked with [ ])
4. Calculates completion percentages per phase
5. Generates visual progress bars and status indicators
6. Outputs a beautifully formatted report

## Instructions for Claude

When you receive a request for task completion or phase progress:

### Step 1: Determine Which Milestone to Report On

- If user specifies a milestone or spec name, use that (e.g., "001-core-mechanics", "002-visual-prototype")
- Otherwise, default to "specs/001-core-mechanics/tasks.md" (current primary milestone)
- Check git branch context if needed to determine relevant milestone

### Step 2: Run the Report Script

Execute one of these bash commands:

**Using npm script (recommended):**
```bash
pnpm report:tasks:001          # Core Mechanics (Milestone 2)
pnpm report:tasks:002          # Visual Prototype (Milestone 1)
pnpm report:tasks              # Default
```

**Using Python directly:**
```bash
python3 scripts/task-completion-report.py specs/001-core-mechanics/tasks.md
python3 scripts/task-completion-report.py specs/002-visual-prototype/tasks.md
```

### Step 3: Present Results to User

Format your response like this:

```markdown
# Task Completion Report: [Milestone Name]

[Output from script - full report with progress bars]

## Analysis & Insights

- **Overall Status**: [Summary of overall progress]
- **Bottlenecks**: [Any phases with low completion]
- **Near Complete**: [Phases almost finished]
- **Next Steps**: [What should be tackled next]
```

### Step 4: Provide Context

Add brief analysis based on the report:
- Which phases are blocking others?
- What's left to complete the milestone?
- Are there critical gaps or risks?
- Recommendations for next work items

## Key Files & Paths

- **Report Script**: `scripts/task-completion-report.py` (main implementation)
- **Bash Wrapper**: `scripts/task-completion-report.sh` (alternative execution)
- **Tasks Files**: `specs/{milestone}/tasks.md` (data source)
- **Documentation**: `scripts/README.md` (full documentation)
- **Config**: `package.json` (npm scripts)

## Example Outputs

### Example 1: User asks for current progress
**User**: "How much of core mechanics have we done?"

**Skill Action**: Runs `pnpm report:tasks:001`

**Output**:
```
OVERALL: 113/136 tasks completed (83.1%)

Phase 1: Setup
  4/4 tasks  [████████████████████████████████████████]  ✅ COMPLETE (100%)

Phase 4e-Advanced
  0/7 tasks  [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]  📋 PENDING (0%)
```

### Example 2: User needs release readiness check
**User**: "Is milestone 2 ready to merge?"

**Skill Action**: Analyzes phase completion, identifies blockers

**Response**: Shows completion report + highlights critical incomplete phases + recommends next actions

## Status Indicator Guide

| Emoji | Status | What It Means |
|-------|--------|--------------|
| ✅ | COMPLETE | 100% - All tasks done, ready for review |
| 🟢 | NEAR COMPLETE | 75-99% - Almost done, final polish |
| 🔄 | IN PROGRESS | 50-74% - On track, solid progress |
| 🟡 | IN PROGRESS | 1-49% - Started, early stages |
| 📋 | PENDING | 0% - Not started yet |

## Notes

- The script is zero-dependency (uses only Python stdlib)
- Reports can be generated for any milestone spec
- All phase detection is automatic
- Progress bars are visual and easy to scan
- Perfect for status checks before PRs or releases

## Related Files

- `specs/001-core-mechanics/tasks.md` - Primary milestone tasks
- `specs/002-visual-prototype/tasks.md` - Alternative milestone tasks
- `docs/IMPLEMENTATION_STATUS.md` - Detailed implementation notes
- `.claude/CLAUDE.md` - Project context and standards

---

**Created**: November 23, 2025
**Last Updated**: Current session
**Status**: Ready for production use
