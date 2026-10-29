---
name: markdown-document-formatter
description: "Use when you need to clean up messy Markdown, fix heading structure, or polish a Markdown document for review."
argument-hint: [file.md]
allowed-tools: Read, Write, Glob
---

## Purpose

Read a messy or poorly formatted Markdown file and produce a clean, well-structured version without changing content or meaning.

## Inputs

- A file path to a `.md` file, or raw Markdown text pasted directly.
- No external systems or credentials.

If `$ARGUMENTS` resolves to an existing file path, read that file. If `$ARGUMENTS` is
plain text rather than a path, treat it as the pasted Markdown content directly. If
`$ARGUMENTS` is empty, ask via `AskUserQuestion` how to provide it: **Paste the Markdown
text** / **Provide a file path**. Then request the actual content per their choice as free
text -- the document content itself has no finite menu.

## Steps

1. Read the Markdown content (from file or pasted text).
2. Analyze for formatting issues:
   - Inconsistent or skipped heading levels (e.g., jumping from `#` to `###`)
   - Mixed list markers (`-`, `*`, `+`)
   - Inconsistent spacing between sections
   - Malformed tables, links, or images
   - Code block fencing issues
   - Trailing whitespace
3. Fix heading hierarchy to follow logical, sequential order without changing wording.
4. Standardize list markers to a single consistent style throughout.
5. Normalize spacing and blank lines per Markdown conventions.
6. Repair malformed tables and links where the intent is clear; flag ambiguous issues instead of guessing.
7. Fix code block fencing: ensure every opening fence has a matching closing fence, standardize on triple-backtick fences (converting tilde fences if mixed), and add a language identifier where the code's language is unambiguous from context — flag as a manual-review item if the language can't be determined.
8. Preserve all content and meaning—formatting and syntax fixes only, no rewrites.
9. Show the cleaned document and a summary of fixes in chat, then ask via `AskUserQuestion`: *"Save this to `[original-name]-formatted.md` alongside the original — is that okay?"* — options **Yes, save it (Recommended)** / **No, don't save**. Only write after the user explicitly confirms.
10. Report a summary of fixes applied and flag any manual review items.

## Output

- A cleaned Markdown file saved to disk only after explicit confirmation (e.g., `README-formatted.md`).
- A brief summary of fixes: heading normalization, list standardization, spacing, code fence repairs, table/link repairs.
- Flagged items for manual review if any.

## Guardrails

- Do not rewrite, summarize, or shorten content.
- Do not change the meaning of headings or text.
- Do not overwrite the original file.
- Always show the cleaned document and fix summary in chat first; save to disk only after the user explicitly confirms.
- Flag broken syntax that cannot be safely auto-fixed.

## Notes

- Clickable-question convention: the Inputs intake-method choice and the Step 9 save confirmation use `AskUserQuestion`. The Markdown content itself stays free text -- genuine data, not a finite menu.
