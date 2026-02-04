---
name: edit-page-content
description: Edit and refine Dutch copy for existing pages, limited to content updates only. Use when updating text in content/behandelingen/*.md or app/features/**/*.vue without changing layout, structure, or creating new components/files.
---

# Edit Page Content

## Overview

Edit existing page content only. Fix Dutch grammar and flow automatically, keeping the meaning intact and the layout unchanged.

## Scope And Constraints

- Work only in `content/behandelingen/*.md` and `app/features/**/*.vue`.
- Do not create new files, components, routes, or layouts.
- Do not change HTML structure, Vue component structure, CSS classes, or layout markup.
- Modify only textual content (headings, paragraphs, labels, button text, copy blocks).
- Keep frontmatter keys and content block structure intact; update values only when needed for copy changes.

## Workflow

1. Identify the target file(s) and confirm they are in scope.
2. Read the current copy and apply Dutch corrections and smoothing while preserving meaning.
3. Edit only text nodes or string literals; keep markup structure unchanged.
4. If requested changes imply new layout or components, ask for clarification and propose a content-only alternative.

## Output Quality

- Use fluent, natural Dutch and consistent tone.
- Avoid adding new claims or details not present in the source text.
- Keep copy concise and clear; prefer active voice.
