---
name: suggest_skill
description: 現在の状況やタスクに合わせて、今使うべきおススメのスキルを提案する
---

# Suggest Skill

Analyze the current work status, recent command execution results, or user intent to suggest the optimal agent skill from those available.

## Procedure

1.  **Understand Context**:
    *   Check recently executed commands (e.g., test failures, build errors).
    *   Check the current file editing status (e.g., source code changes, documentation updates).

2.  **Select Skill**:
    *   Propose several appropriate next actions from all skills defined in the `list_skills` skill.
    *   Example: Suggest `wrap_up` immediately after tests pass.

3.  **Present Rationale**:
    *   Briefly explain why the skill is recommended and what its benefits are.
