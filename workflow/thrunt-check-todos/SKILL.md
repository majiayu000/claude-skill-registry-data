---
name: thrunt-check-todos
description: List pending todos and select one to work on
argument-hint: "[area filter]"
allowed-tools: Read, Write, Bash, AskUserQuestion
---


<objective>
List all pending todos, allow selection, load full context for the selected todo, and route to appropriate action.

Routes to the check-todos workflow which handles:
- Todo counting and listing with area filtering
- Interactive selection with full context loading
- Huntmap correlation checking
- Action routing (work now, add to phase, brainstorm, create phase)
- STATE.md updates and git commits
</objective>

<execution_context>
@.github/thrunt-god/workflows/check-todos.md
</execution_context>

<context>
Arguments: $ARGUMENTS (optional area filter)

Todo state and huntmap correlation are loaded in-workflow using `init todos` and targeted reads.
</context>

<process>
**Follow the check-todos workflow** from `@.github/thrunt-god/workflows/check-todos.md`.

The workflow handles all logic including:
1. Todo existence checking
2. Area filtering
3. Interactive listing and selection
4. Full context loading with file summaries
5. Huntmap correlation checking
6. Action offering and execution
7. STATE.md updates
8. Git commits
</process>
