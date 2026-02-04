---
name: writing-commit-messages
description: Use when writing or improving messages for Git commits, or when asked to generate a commit message or pull request description.
---

# Writing commit messages

## Instructions

Commit messages MUST follow the following format:

```
<subject>

<body>
```

### `<subject>`

This is in one of the following formats:

```
<summary>
<scope>: <summary>
<kind>(<scope>): <summary>
```

Where:

- `<kind>` is the type of change being made.
  It is one of: feat, fix, docs, style, refactor, test, chore.
- `<scope>` identifies the area of the codebase affected.
  This is the name of a module, component, feature, or project.
- `<summary>` is a concise summary of the changes made in the commit.
- `<summary>` MUST use the imperative mood.
  For example, use "Add feature" instead of "Added feature" or "Adds feature".

`<subject>` SHOULD be fewer than 50 characters, and MUST be fewer than 72.
If the subject would exceed 72 characters, omit the `<kind>`.
If it still exceeds 72 characters, omit the `<scope>`.
If it still exceeds 72 characters, rethink the `<summary>` to shorten it.

### `<body>`

- Add a detailed description of the changes made in the commit.
- DO NOT use itemized lists just to enumerate changes made in the commit.
  Anything that is obvious from looking at the diff
  MUST NOT be included in the commit message.
- NEVER use an empty body.
  There MUST ALWAYS be a body to the commit message.
- Commit message body MUST NOT have lines longer than 72 characters.
- Apply semantic line breaks formatting.
- Treat commit messages as Markdown documents:
  - Use backticks for inline code (function names, variables, file paths)
  - Use other Markdown formatting (bold, lists, etc.) judiciously
  - Maintain semantic line breaks
- Use objective, factual tone:
  - Avoid subjective embellishments like "critical issue", "serious problem"
  - Focus on what the code does and why, not value judgments
- **Attribution**:
  If the bot wrote any code that is part of the commit,
  attribute the bot as a co-author in the commit message.

  ```
  Co-Authored-By: Claude <noreply@anthropic.com>
  // or
  Co-Authored-By: Amp <amp@ampcode.com>
  ```

  Exception:
  If the bot *only* wrote the commit message,
  and was not involved in writing any code,
  do NOT include a co-authorship trailer.

## Formatting

The `<subject>` SHOULD be fewer than 50 characters,
and MUST be fewer than 72 characters.

The `<body>` MUST NOT have lines longer than 72 characters.

Commit messages MUST ALWAYS be formatted with semantic line breaks.

## Providing feedback on commit messages

When reviewing or providing feedback on commit messages:

- Organize feedback using Markdown headings (##, ###)
  when there are multiple distinct issues or sections
- Use fenced code blocks (```) when:
  - Providing examples of problematic code
  - Showing diffs or comparisons
  - Demonstrating technical examples
- Apply the same factual tone guidelines as commit messages themselves

## Common mistakes

### Not using semantic line breaks

NEVER write commit messages without semantic line breaks.

**Solution**:
Apply semantic line breaks formatting to commit messages.

### Using itemized lists of changes in the commit

DO NOT just enumerate the changes in the commit message.

**Why**:
Any information that is obvious from looking at the `git diff`
does not need to be present in the commit message.

**Solution**:
Focus on *why* the changes were made,
not *what* changes were made.

### Using single-line commit messages

NEVER use single-line commit messages.

**Solution**:
There MUST ALWAYS be a body to the commit message.

## Important: This skill only writes the message

This skill provides guidance on how to format commit messages.
After using this skill to craft a commit message,
you must invoke the `committing` skill
to actually perform the commit operation.

**NEVER use `git commit` directly.**
Always use `Skill(committing)` after writing the commit message.
