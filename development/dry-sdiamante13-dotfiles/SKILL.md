---
name: dry
description: Refactor duplicated code by extracting helpers, shared abstractions, or clearer reusable structure. Use when asked to apply DRY, remove duplication, consolidate repeated logic, or run `/refactor:dry`.
metadata:
  legacy-name: refactor:dry
---

# DRY Refactor

Ask the user for the file or directory to refactor. Support multiple files if a directory is provided.

## Process

Work through these steps in order, making a separate commit for each extraction:

1. **Extract simple helper methods** (strings, calculations, parsing)
   - Identify duplicated logic
   - Extract to focused method with clear name
   - Remove duplicated code immediately after extraction
   - Commit the extraction

2. **Extract complex methods with parameters**
   - Find similar code blocks with variations
   - Extract with parameters to handle variations
   - Remove duplicated code immediately after extraction
   - Commit the extraction

3. **Apply design patterns when beneficial**
   - Template Method, Strategy, etc. for structural duplication
   - Only when it improves readability/maintainability
   - Avoid over-engineering or premature abstraction
   - Remove duplicated code immediately after extraction
   - Commit the extraction

After EACH extraction:
- Run tests automatically
- If tests fail, revert the change immediately
- If tests pass and using IDE refactoring tool, commit: `. r <description>`
- If tests pass but manual refactoring, commit: `^ r <description>`
- Remove the now-duplicated code in the same commit

## Output

- If no duplication found, report "No duplication found"
- Otherwise provide brief summary at end (e.g., "Extracted 4 methods, removed 3 duplicated blocks")

## Commit Format

Use Arlo's Commit Notation (ACN):
- `. r extract saveToDatabase method` - IDE refactoring or provably safe
- `^ r extract validation logic` - Manual refactoring validated by tests
