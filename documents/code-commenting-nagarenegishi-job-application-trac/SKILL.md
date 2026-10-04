---
name: code-commenting
description: >
  Apply whenever writing or editing code in any language, even if comments are
  not explicitly requested. Enforces comment and documentation discipline:
  concise file headers, function docs in the language's native format, inline
  comments for non-obvious logic, and protection of existing comments. Not
  required during suggestion-only or discussion when no file is written.
---

# Code Commenting

Governs comments and documentation only. Does not change how the code itself is written.

## Documentation format

Use the language's native doc-comment convention. Examples:
- C# → XML doc (`///`)
- Java → Javadoc (`/** */`)
- Python → docstrings
- JavaScript / TypeScript → JSDoc / TSDoc
- Go → doc comments (`// Name ...`)
- Rust → `///`

For any other language, follow that language's accepted documentation standard.

## File header

Add a concise header at the top of every file stating what the file is in general, in one or two lines. No implementation detail; detail belongs to the functions.

## Function comments

Document every function with a comment describing what it does, not how.
Skip functions that are trivial, self-evident, or not conventionally documented (getters, setters, one-liners whose name already says everything).

## Inline comments

Add inline comments only where logic is complex or a decision is non-obvious: anything a later reader needs to follow the code. Explain the reason or key point, not the mechanics.

## Style

- Concise but meaningful. Write for a human reader in natural language.
- No filler, no line-by-line narration, no AI-tell phrasing.
- Never add a comment that only states the obvious or adds nothing.

## Existing comments (protected)

- Do not modify, rewrite, or delete existing comments while coding.
- Adding new comments is allowed freely.
- To change or remove an existing comment, including obvious or no-value ones, ask permission first.
