---
name: handover
description: Use when starting a session (resume previous work) or ending a session (create handover for next). Automatically detects mode based on conversation state. Cascades through completed handovers via Haiku subagents until finding incomplete work.
---

# Handover Skill

Context-aware handover management: resume previous work or create a handover for the next session.

## Mode Detection

Determine mode based on conversation state:

| Conversation State | Mode | Action |
|-------------------|------|--------|
| Empty or minimal (just `/handover`) | **Process** | Read `reference/process-mode.md` |
| Progress has been made | **Create** | Read `reference/create-mode.md` |

## Process Mode

Resume from latest incomplete handover. Uses Haiku subagents to cascade through completed handovers.

**Critical**: Process mode handles ONE handover per session. After finding incomplete work, STOP cascading and begin implementation.

**See**:
- `reference/process-mode.md` - Cascade workflow and Haiku subagent prompt
- `reference/human-decision-workflow.md` - **MANDATORY** when handover requires human decisions with subagent recommendations (counter-recommend, executive summaries)

## Create Mode

Generate handover from conversation for the next session.

**Arguments:**
- `file` - Write to file only, suppress chat output
- `chat` - Output to chat only, skip file creation
- (none) - Both file and chat (default)

**See**: `reference/create-mode.md` for full workflow including:
- Pre-creation analysis (task separation, dependencies)
- Dependency blocking instructions
- Output format template
- File numbering rules
