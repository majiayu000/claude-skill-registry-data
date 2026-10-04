---
name: update-preview
description: Render a side-by-side HTML diff of the original article vs the updated draft so the editor can review every change in browser.
allowed-tools: Read, Write, Bash
---

# Update Preview Skill

The editor reviewing an update wants to see exactly what changed. This skill produces a side-by-side HTML diff: original on the left, updated on the right, with changes highlighted.

## Input

`/update-preview <slug>`

Reads:
- `content-pipeline/updates/1-extracted/{slug}.md` (original)
- `content-pipeline/updates/7-updated-draft/{slug}.md` (updated)

## Process

1. **Run the diff renderer:**
   ```bash
   python .claude/skills/update-preview/scripts/render_diff.py "<slug>"
   ```
   The script:
   - Reads both files
   - Renders each side as HTML
   - Wraps both in a side-by-side layout
   - Highlights additions (green), removals (red), and unchanged (default)
2. **Tell the user** the diff path so they can open in browser.

## Output

`content-pipeline/updates/5-update-preview/{slug}.html`

A self-contained HTML page with the diff side-by-side.

## Quality checklist

- [ ] Diff opens in browser without errors
- [ ] Both columns have visible content
- [ ] Additions are visually distinct from removals
- [ ] Editor's notes from the updated draft are included at the bottom of the right column
- [ ] Long content is scrollable, not truncated

## Limitations

- Whitespace-only differences may show as changes (this is fine; it tells the editor where formatting shifted)
- Markdown→HTML conversion uses the same library as `/preview` (may not handle exotic markdown perfectly)
- The diff is line-based — small in-paragraph edits show as full-paragraph changes
