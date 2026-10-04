---
name: preview
description: Render the cited draft as an HTML preview styled like the brand's blog so the writer can review the article in browser before publishing.
allowed-tools: Read, Write, Bash
---

# Preview Skill

Markdown files don't read like blog posts. Some problems only become visible in styled HTML. This skill renders the cited draft into a preview HTML file that mimics the published look.

**The preview now renders the `:::component` fences STYLED, not as raw `:::` text.** A pre-pass in `render_preview.py` converts each `:::name attrs … :::` block into the matching `<div class="cmp-name">…</div>` (inner rendered as markdown) and applies the inline treatments (`` `code` `` chip, `{lead}…{/lead}` → lead paragraph, `==mark==` → `<mark>`). The `cmp-*` CSS and the Tabler icon webfont are baked into `templates/preview.html`, so callouts, stat cards, methodology panels, CTAs, etc. look like the published page — matching `examples/component-mockup.html`. An unknown fence degrades to a plain aside (content is never dropped). This is the editor's last look before the `components` gate + publish.

## Input

For slug `{slug}`:
- `content-pipeline/6-drafts-cited/{slug}.md` (the cited draft)
- `templates/preview.html` (HTML shell — carries the `cmp-*` component CSS + Tabler icon `<link>`)

## Process

1. **Read the cited draft.** Extract the H1 as the title, the rest as body.
2. **Run the preview renderer:**
   ```bash
   python .claude/skills/preview/scripts/render_preview.py "<slug>"
   ```
   The script reads the draft, **converts each `:::component` fence to its styled `cmp-*` HTML and applies inline treatments**, converts the surrounding markdown to HTML, substitutes `{{TITLE}}`, `{{DATE}}`, `{{BODY_HTML}}` into `templates/preview.html`, and writes the result.
3. **Tell the user** the preview path so they can open it in a browser.

## Output

`content-pipeline/7-preview/{slug}.html`

A self-contained HTML file. Open it in a browser to see the article rendered with the brand's typography, callouts, and screenshot placeholders.

## Quality checklist

- [ ] HTML file exists at the expected path
- [ ] Title in HTML matches the H1 in the cited draft
- [ ] All H2/H3 headings are styled
- [ ] Internal links are clickable
- [ ] Screenshot/visual placeholders are visually distinct (dashed border, typed label)
- [ ] `:::component` fences render as STYLED `cmp-*` blocks (no raw `:::` text leaking through) — callouts (tip/note/warning/important/sidenote/definition) carry their Tabler icon + tint; nutshell / methodology / key-takeaways / stat(-group) / expert / pullquote / cta / further-reading render per `examples/component-mockup.html`
- [ ] Inline treatments applied: `` `code` `` chips, `{lead}` opening paragraph, `==mark==` highlights

## When the preview looks broken

If the rendered HTML drops content, mangles tables, or misses headings:
- Check for unbalanced markdown (unmatched `**`, broken links, stray HTML)
- If a `:::component` fence shows up as raw `:::` text, the fence is malformed (no closing `:::`, or a stray opener) — run the `components` gate (`python scripts/lint_components.py content-pipeline/6-drafts-cited/<slug>.md`) to get the exact line; the preview intentionally leaves unbalanced fences verbatim
- Re-run with the same slug — script overwrites
- If a CSS rule is wrong, edit the `<style>` block (the `cmp-*` rules + tokens) in `templates/preview.html` directly — the CSS is inlined into the shell, so no rebuild is needed

## Note on Python markdown library

The renderer uses Python's standard library + `markdown` package if installed, falling back to a simple inline converter if not. For best fidelity install:

```bash
pip install markdown
```

Without it, fenced code blocks and tables may render as plain text.
