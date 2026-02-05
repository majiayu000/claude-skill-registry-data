---
name: prompt-generator
description: Generate implementation prompts for phase-based project execution using an orchestration pattern. Use when users request prompts for implementing project phases, need orchestration prompts for multi-step implementations, ask for "/prompt", "generate prompt", "create implementation prompt", or want to create structured implementation instructions for subagent delegation. Outputs the prompt to chat and saves to docs/prompts folder.
---

# Prompt Generator

Generate structured implementation prompts for phase-based project execution using an orchestrator/subagent pattern.

## Quick Start

When triggered, gather these inputs from the user:

| Variable | Description | Example |
|----------|-------------|---------|
| `PHASE_NUMBER` | Phase identifier | "1", "2", "3" |
| `PHASE_NAME` | Descriptive phase name | "Foundation", "Data Pipeline" |
| `PHASE_DOC_PATH` | Path to phase plan document | `/project/docs/plans/01-foundation.md` |
| `PROJECT_ROOT` | Project root directory | `/home/user/myproject` |
| `GENERAL_PLAN_PATH` | Path to general plan (optional) | `/project/docs/plans/00-general-plan.md` |

## Workflow

### 1. Gather User Input

Ask the user for required variables. If context provides these values, confirm them:

```
To generate the implementation prompt, I need:
1. Phase number (e.g., 1, 2, 3)
2. Phase name (e.g., "Foundation", "Data Pipeline")
3. Path to the phase document
4. Project root directory
5. Path to general plan (optional)
```

### 2. Generate the Prompt

Read the template from `references/implementation-prompt-template.md` and substitute all `{PLACEHOLDER}` values with user-provided inputs.

### 3. Output and Save

1. **Display**: Output the complete generated prompt in the chat
2. **Save**: Use `scripts/save_prompt.py` to save to `<PROJECT_ROOT>/docs/prompts/`

```bash
echo "<generated_prompt>" | python scripts/save_prompt.py <project_root> <phase_number> <phase_name>
```

The file is saved as: `docs/prompts/phase-<N>-<name>.md`

## Template Features

The generated prompt includes:

- **Orchestration requirements**: Main session coordinates, subagents implement
- **Delegation patterns**: File creation, testing, infrastructure, integration
- **Progress tracking**: TodoWrite integration for task management
- **Validation workflow**: Group validation and final success criteria checks
- **Error handling**: Failure analysis, rollback procedures, escalation guidance
- **Handoff preparation**: Documentation for next phase transition

### Subagent Patterns Reference

| Task Type | Pattern | Concurrency |
|-----------|---------|-------------|
| File creation (independent) | Parallel | High (5-7) |
| File creation (dependent) | Sequential | Low (1-2) |
| Testing/Validation | Per test suite | Medium (3-5) |
| Docker/Infrastructure | Per service | Medium (3-4) |
| Integration | Per integration point | Low (2-3) |

## Output Format

The generated prompt follows this structure:

```markdown
Implement Phase {N}: {Name} of the trading platform...

IMPORTANT ORCHESTRATION REQUIREMENTS:
1. This is an ORCHESTRATION SESSION...
2. Use the implement-plan skill...
3. Spawn SUBAGENTS for all implementation...
4. Track progress using TodoWrite...
5. Coordinate subagents and validate...

## Implementation Strategy
[Phase overview, orchestration workflow, delegation patterns]

## Error Handling
[Failure analysis, rollback, escalation]

## Success Criteria Validation
[Automated and manual checks]

## Handoff to Next Phase
[Completion documentation, context prep, clean state]
```

## Resources

### references/
- `implementation-prompt-template.md`: Full prompt template with all placeholders and patterns

### scripts/
- `save_prompt.py`: Saves generated prompts to `docs/prompts/` with metadata header
