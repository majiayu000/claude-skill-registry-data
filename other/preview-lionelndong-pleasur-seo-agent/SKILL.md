---
name: preview
description: Render the cited draft as an HTML preview styled like the brand's blog so the writer can review the article in browser before publishing.
allowed-tools: Read, Write, Bash
---

# Preview Skill

Markdown files don't read like blog posts. Some problems only become visible in styled HTML. This skill renders the cited draft into a preview HTML file that mimics the published look.

## Input

For slug `{slug}`:
- `content-pipeline/6-drafts-cited/{slug}.md` (the cited draft)
- `templates/preview.html` (HTML shell)
- `templates/preview.css` (styles)

## Process

1. **Read the cited draft.** Extract the H1 as the title, the rest as body.
2. **Run the preview renderer:**
   ```bash
   python .claude/skills/preview/scripts/render_preview.py "<slug>"
   ```
   The script reads the draft, converts markdown to HTML, substitutes `{{TITLE}}`, `{{DATE}}`, `{{BODY_HTML}}` into `templates/preview.html`, and writes the result.
3. **Tell the user** the preview path so they can open it in a browser.

## Output

`content-pipeline/7-preview/{slug}.html`

A self-contained HTML file. Open it in a browser to see the article rendered with the brand's typography, callouts, and screenshot placeholders.

## Quality checklist

- [ ] HTML file exists at the expected path
- [ ] Title in HTML matches the H1 in the cited draft
- [ ] All H2/H3 headings are styled
- [ ] Internal links are clickable
- [ ] Screenshot placeholders are visually distinct (dashed border, "screenshot would go here" treatment)
- [ ] Tip / sidenote / editor-note callouts are styled if present in the draft

## When the preview looks broken

If the rendered HTML drops content, mangles tables, or misses headings:
- Check for unbalanced markdown (unmatched `**`, broken links, stray HTML)
- Re-run with the same slug — script overwrites
- If a CSS rule is wrong, edit `templates/preview.css` directly (rebuild not needed; CSS is referenced by relative path)

## Note on Python markdown library

The renderer uses Python's standard library + `markdown` package if installed, falling back to a simple inline converter if not. For best fidelity install:

```bash
pip install markdown
```

Without it, fenced code blocks and tables may render as plain text.
