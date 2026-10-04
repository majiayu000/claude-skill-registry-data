---
name: html-research-notes
description: Create structured research, engineering, and thesis workflow notes as standalone HTML instead of Markdown, with metadata blocks, internal links, readable academic styling, print-friendly layout, templates, and optional Playwright screenshot validation. Use when Codex should document workflows, decisions, manifests, checklists, or reusable project knowledge in HTML form.
---

# HTML Research Notes

Use this skill to make local, linkable, print-friendly HTML notes that work without a build step.

## Workflow

1. Choose the note type:
   - hub/index;
   - decision log;
   - claim manifest;
   - experiment manifest;
   - figure manifest;
   - review report;
   - how-to/workflow guide.
2. Start from a template in `assets/` when possible.
3. Include a metadata block near the top:
   - owner;
   - status;
   - last updated;
   - source links or commit;
   - intended audience.
4. Use semantic HTML:
   - `header`, `main`, `section`, `table`, `nav`;
   - stable IDs for headings;
   - relative links between pages.
5. Apply a utilitarian reading style:
   - dense but readable;
   - strong tables;
   - no decorative landing-page treatment;
   - print-friendly CSS.
6. Validate links and viewport fit. Use Playwright when a visual check matters.

## Guardrails

- Do not create Markdown workflow records unless an external tool requires it.
- Do not embed secrets, raw private logs, or bulky generated outputs.
- Do not rely on a build system for basic navigation.
- Keep pages readable when opened directly from disk.

## Useful Resources

- Read `references/html-note-rules.html` for styling and structure rules.
- Use `assets/note-template.html` as a starter page.
