---
name: methods
description: Refactor long methods or large code blocks by extracting small, focused helper methods with clear names and narrow responsibilities. Use when asked to extract methods or run `/refactor:methods`.
metadata:
  legacy-name: refactor:methods
---

# Extract Methods Refactor

Ask the user for the file or directory to refactor. Support multiple files if a directory is provided.

## Process

Work through these steps in order, making a separate commit for each extraction:

1. **Extract simple helper methods**
   - Calculations, formatting, simple logic
   - Single responsibility, behavior-focused names
   - Pass necessary parameters rather than sharing state

2. **Extract complex logic blocks**
   - Validation, transformations, data processing
   - Well-named methods that reveal intent
   - Apply proper access modifiers (private for helpers)

3. **Extract control flow sections**
   - Only when it improves readability
   - Avoid over-extraction that hurts clarity

After EACH extraction:
- Run tests automatically
- If tests fail, revert the change immediately
- If tests pass and using IDE refactoring tool, commit: `. r <description>`
- If tests pass but manual refactoring, commit: `^ r <description>`

## Guidelines

- Extract pragmatically to improve code organization
- Name methods based on behavior not implementation
- Ensure each method ≤ 25 lines
- Preserve original functionality exactly

## Output

- If no methods to extract, report "No methods to extract"
- Otherwise provide brief summary (e.g., "Extracted 5 methods from 3 large blocks")

## Commit Format

Use Arlo's Commit Notation (ACN):
- `. r extract validateUserCredentials method` - IDE refactoring
- `^ r extract transformRawStockData method` - Manual refactoring
