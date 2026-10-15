---
name: deslop
description: Remove AI-generated code slop -- verbose comments, unnecessary abstractions, over-engineering.
version: 0.1.0
execution-mode: remedial
argument-hint: <file or directory to clean>
category: dev-tools
status: candidate
---
# Deslop

Strip AI-generated cruft from code. AI assistants tend to produce recognizable patterns of unnecessary verbosity.

## What to Remove

### Comments
- Comments that restate the code: `# Increment counter` above `counter += 1`
- Section banners that add no information: `# ===== MAIN LOGIC =====`
- Docstrings on obvious methods: `"""Get the name."""` on `def get_name(self)`
- `TODO`-style comments with no context: `# TODO: improve this`

### Abstractions
- Single-use helper functions that could be inline
- Wrapper classes around a single method
- Config objects for 2-3 settings that could be parameters
- Factory patterns when direct instantiation works

### Patterns
- Try/except that catches Exception and re-raises
- Logging at every entry/exit point
- Type annotations on obvious literals: `x: int = 0`
- Unnecessary `else` after `return`/`raise`/`continue`
- Default parameter values that are never overridden

### Naming
- Overly verbose names: `process_and_validate_user_input_data` -> `validate_input`
- Hungarian notation: `str_name`, `list_items`
- Redundant prefixes: `user_name` in a `User` class -> just `name`

## Execution

1. Read the target file(s)
2. Identify slop patterns (list them with line numbers)
3. Show the user what you'd remove and why
4. Apply changes only after approval
5. Run tests to verify nothing broke

## Rules
- Never remove comments that explain WHY (only remove WHAT comments)
- Never remove error handling that catches specific exceptions
- Never simplify code that has a non-obvious reason for its complexity
- If unsure, leave it and flag it as "possible slop, needs human judgment"
- Three similar lines of code is better than a premature abstraction
