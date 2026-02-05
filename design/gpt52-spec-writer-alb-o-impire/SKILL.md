---
name: gpt5.2-spec-writer
description: Guide for writing effective prompt specifications (specs) for the GPT-5.2 Codex agent. Use when the user asks to "write a prompt spec", "create a system prompt for GPT-5.2", "design a spec for an agent", or "how to prompt GPT-5.2".
---

# GPT-5.2 Spec Writer

Guide for writing prompt specifications tailored for GPT-5.2. The model excels at structured reasoning and instruction following but benefits from explicit constraints on verbosity and scope.

## How to Write a Spec

A spec is a markdown document defining persona, constraints, architecture, and operational rules for an agent.

1. Start with [references/spec-template.md](references/spec-template.md)
1. Fill in project-specific sections (directive, architecture, conventions)
1. Verify coverage: task structure, verbosity/scope constraints, tool usage guidance, context handling for large inputs

## Key Patterns

### Explicit Task Roadmaps with Checkboxes

Every spec should include an objective, actionable sequence of tasks using **markdown checkboxes** (`- [ ]`). GPT-5.2 performs best with concrete work items and clear completion criteria, not abstract guidance.

- Use `- [ ]` checkboxes for all tasks—GPT-5.2 tracks and checks them off as work completes
- Numbered phases with measurable objectives
- Specific file paths and function names
- Concrete steps: Read X -> Edit Y -> Run Z
- Completion criteria for each task

Example:
```markdown
- [ ] 1.1 Fix null check in `parse_config()` at line 42
- [ ] 1.2 Add error handling to `load_settings()`
- [ ] 1.3 Run tests and verify all pass
```

Avoid vague instructions like "improve the code". Be specific: "Fix the null check in parse_config() at line 42".

### XML Constraint Blocks

Use XML tags to define distinct rule sets:

- `<mandatory_execution_requirements>` - execution loop (Read -> Edit -> Verify)
- `<verbosity_and_scope_constraints>` - output size and scope control
- `<design_freedom>` - when new patterns/refactors are acceptable

### Chain of Verification

Instruct the model to verify its work: Edit -> Build/check -> Fix -> Report only when complete.

### Tool Usage

- Encourage parallel tool use for batch operations (e.g. reading multiple files)
- Require verification after edits (run build, run tests)

### Context Management

For large inputs (>10k tokens), use `<long_context_handling>` to instruct the model to outline key sections, restate constraints, and anchor claims to specific locations.

## References

- [Spec Template](references/spec-template.md)
- [GPT-5.2 Model Guide](references/gpt5.2-model.md)
