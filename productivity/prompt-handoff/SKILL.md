---
name: prompt-handoff
description: convert a sensemaking artifact into a ready-to-copy prompt for the next specialized skill. use to ensure context is preserved across skill transitions.
---
# prompt-handoff

Produces a **Prompt Handoff** to ensure that the judgment reached in sensemaking is successfully transmitted to the next specialized skill (e.g., `to-prd`, `tdd`).

## Workflow
1. **Intake**: Review the latest sensemaking artifact (Problem Frame, Brief, or Plan).
2. **Target Selection**: Identify the next specialized skill in the registry.
3. **Context Preservation**: Extract the most critical constraints, goals, and evidence.
4. **Task Formulation**: Write a clear, actionable task statement.
5. **Constraint Mapping**: List all "must-haves" and "must-nots."
6. **Stop Condition**: Define exactly when the next skill should stop for review.

## Output Format
Every response must follow the [Prompt Handoff](references/prompt-handoff-template.md) structure.

## Boundary Rule
Do not execute the prompt yourself. Your job is to package the context for the user to copy/paste or for the orchestrator to pass.

## References
- [Prompt Handoff Template](references/prompt-handoff-template.md)
