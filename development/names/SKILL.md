---
name: names
description: Refactor code by renaming variables, methods, classes, and concepts for clearer intent. Use when asked to improve names, clarify naming, perform a naming pass, or run `/refactor:names`.
metadata:
  legacy-name: refactor:names
---

# Rename Refactor

Ask the user for the file or directory to refactor. Support multiple files if a directory is provided.

## Process

Work through these steps in order, making a separate commit for each rename:

1. **Rename local variables**
   - Replace generic names (data, temp, obj, etc.) with domain-specific terms
   - Make names describe behavior and domain purpose
   - Follow language conventions (camelCase, snake_case, etc.)

2. **Rename private methods/fields**
   - Improve clarity and reveal intent
   - Ensure consistency across related names
   - Use behavior-focused names

3. **Rename public methods/fields**
   - Same as private, but broader impact
   - Ensure all references updated throughout codebase

4. **Rename classes/types**
   - Highest impact, most careful
   - Domain-driven names that reveal purpose

After EACH rename:
- Run tests automatically
- If tests fail, revert the change immediately
- Commit using: `. r rename <old> to <new>`

## Guidelines

- DO NOT CHANGE ANY BEHAVIOR - only improve names
- Use IDE rename refactoring when possible (compile-error driven)
- Ensure all references updated throughout codebase

## Output

- If no names to improve, report "No names to improve"
- Otherwise provide brief summary (e.g., "Renamed 7 variables, 3 methods, 1 class")

## Commit Format

Use Arlo's Commit Notation (ACN):
- `. r rename getData to fetchStockPrices`
- `. r rename userObj to investorProfile`
