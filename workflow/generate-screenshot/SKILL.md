---
name: generate-screenshot
description: For each [SCREENSHOT placeholder] in the cited draft, generate a deep-link URL pointing to the brand's tool/report so the editor can capture the screenshot manually. URL placeholders only — no headless browser automation.
allowed-tools: Read, Write, Edit
---

# Generate Screenshot Skill

The cited draft contains placeholders like `[SCREENSHOT: Cannibalization report showing overlapping rankings]`. This skill generates the deep-link URLs the editor visits to capture each screenshot. The actual screenshot capture is manual — that's deliberate (Ryan Law called this out as the part still requiring human judgment).

## Input

For slug `{slug}`:
- `content-pipeline/6-drafts-cited/{slug}.md` (the cited draft with placeholders)
- `brand-config.md` (product URLs — **primary source** for the Pleasur.AI deployment)
- `references/_archive/ahrefs-products-catalog.md` (legacy non-Pleasur reference — URL-pattern shapes only, kept as a fallback when brand-config doesn't enumerate a needed report)

## Process

1. **Read the cited draft.**
2. **Find every `[SCREENSHOT: description]` placeholder.** Note the surrounding context — what concept does the screenshot illustrate?
3. **For each placeholder, decide:**
   - Which brand tool / report would naturally show this?
   - Use brand-config product URLs and the legacy URL-pattern catalog reference to construct a deep-link URL when possible. brand-config is the authoritative list for the Pleasur.AI deployment; the archived catalog is only a shape hint when brand-config doesn't cover the report type.
   - Default URL is the product's landing page if no specific report URL applies.
4. **Write a screenshot URLs file** to `content-pipeline/images/{slug}/screenshot-urls.md`:

```markdown
# Screenshot URLs for {slug}

For each placeholder below, visit the URL, capture the screenshot, save to this folder, then update the draft to reference the saved image.

## Screenshot 1: [Cannibalization report showing overlapping rankings]
- **Context in draft:** "Open ProductA's Cannibalization Report..."
- **Tool URL:** https://app.brand.com/tools/cannibalization-report?example=...
- **Filename to save:** screenshot-1-cannibalization.png
- **Notes:** Use the example dataset on a domain with visible overlap

## Screenshot 2: ...
```

5. **Optionally update the draft** to reference the planned filenames. Replace `[SCREENSHOT: ...]` with `![Cannibalization report](images/{slug}/screenshot-1-cannibalization.png)` so the markdown is publishable once the editor saves the screenshots.
6. **If updating the draft, save** an updated copy as `content-pipeline/6-drafts-cited/{slug}.md` (overwrite). Otherwise leave the draft unchanged and only emit the URLs file.

## Output

`content-pipeline/images/{slug}/screenshot-urls.md`

(Optionally) updated `content-pipeline/6-drafts-cited/{slug}.md` with image references in place of placeholders.

## Quality checklist

- [ ] Every `[SCREENSHOT: ...]` placeholder in the draft has a corresponding entry
- [ ] URLs use the brand's actual tool URL patterns (not made up)
- [ ] Filenames are predictable and sequential
- [ ] Each entry includes context (what concept it illustrates)
- [ ] If the draft is updated, image references match planned filenames

## When no good URL exists

If the placeholder describes something the brand can't directly screenshot (e.g., a Google SERP, a third-party tool):
- Note "External screenshot — capture manually" instead of a URL
- Keep the placeholder in the draft for the editor to handle
