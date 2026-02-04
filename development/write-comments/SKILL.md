---
name: write-comments
description: Writes explanatory comments to code to improve readability for developers and AI systems. Use when documenting code or improving code comprehension.
---

# Write Comments to Code

Your primary objective is to clarify the code's **purpose and intent** for a new developer. If the code is self-evident, do not add a comment.

## Process

1. Analyze the code to understand its structure and functionality
2. Identify key components, functions, loops, conditionals, and any complex logic
3. Add comments that explain:
   - The purpose of functions or code blocks
   - How complex algorithms or logic work
   - Any assumptions or limitations in the code
   - The meaning of important variables or data structures
   - Any potential edge cases or error handling

## Formatting

- Every comment must start with a capital letter and end with a period.
- Multi-line docblocks (`/** ... */`) must have the `/**` and `*/` on their own, separate lines.

## Content and Placement

- Docblocks (`/** ... */`): Use for all exported members (functions, types, hooks, constants) and complex internal logic. Explain what the item is for.
- Single-line (`//`): Use for brief, inline explanations of non-obvious implementation details or to label logical sections within a function.
- Focus on the "why" and "how" rather than just the "what".
- Preserve the original code's formatting and structure.
- Do not change the code's functionality.

## Deletion Mandates

- DELETE any comment that merely restates what the code does (e.g., `// Increment counter`).
- DELETE all commented-out code blocks. Use version control for history.
