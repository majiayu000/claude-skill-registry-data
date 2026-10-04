---
name: qa-review-hidden-text
section: content
description: "Reviews text hidden in DOM attributes — placeholders, alt text, title tooltips, aria-labels, input values, and select options — for spelling, grammar, word choice, and untranslated keys. Catches what qa-review-content can't see in document.body.innerText."
model: sonnet
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
interactive: true
---
## What it checks

A lot of user-facing text never appears in `document.body.innerText` — it lives in DOM attributes. The companion skill `qa-review-content` skips all of this. This skill closes the gap.

Specifically reviews text in:

| Bucket | Source | Why it matters |
|---|---|---|
| `placeholders` | `<input placeholder="...">` | Most common hidden-typo location |
| `altText` | `<img alt="...">` | Accessibility audit fails; screen-reader announces the typo |
| `titles` | `<element title="...">` | Hover tooltip text |
| `ariaLabels` | `<element aria-label="...">` | Screen-reader-only labels — sighted users never see the typo |
| `valueAttrs` | `<input type="submit" value="..."> / <button>` value attribute | Default button labels |
| `optionLabels` | `<select> <option>` | Dropdown labels — only visible when dropdown is open |

Same issue categories as `qa-review-content`:

| issueType | severity | What it catches |
|---|---|---|
| `spellingError` | medium | Misspelled words in any attribute |
| `grammarError` | medium | Grammar mistakes in tooltip / placeholder copy |
| `wordChoice` | medium | your/you're, their/there, its/it's |
| `placeholderText` | high | "TODO", "Enter text", "placeholder" left in production |
| `untranslatedKey` | high | `common.button.save`, `{{var}}` in alt/title/aria-label |
| `htmlEntityLiteral` | medium | `&amp;`, `&lt;` rendered in an alt tag |
| `encodingMojibake` | medium | Broken UTF-8 in attributes |
| `attributeEmpty` | medium | Empty alt/aria-label/title where text is expected |
| `attributeRedundant` | low | Alt text duplicating visible caption (a11y noise) |

## Orchestrator flow

Interactive Sonnet skill. Same pattern as `qa-review-content`.

1. Run `probe.extractAttributeText` — collects all attribute text into buckets.
2. **Self-skip** the cell if every bucket is empty (no attributes worth reviewing).
3. Pass the buckets + cell context to a Sonnet sub-agent:

   ```
   Agent(
     subagent_type: "general-purpose",
     model         = "sonnet",
     prompt = `You are reviewing text hidden in DOM attributes for content quality issues.

     Cell context:
       route: {cell.route}
       viewport: {cell.viewport}
       browser: {cell.browser}

     Extracted attribute text (each item has source / text / locator):

     PLACEHOLDERS:
     {placeholdersJson}

     ALT TEXT:
     {altTextJson}

     TITLE ATTRIBUTES:
     {titlesJson}

     ARIA-LABELS:
     {ariaLabelsJson}

     INPUT VALUE ATTRS:
     {valueAttrsJson}

     SELECT OPTIONS:
     {optionLabelsJson}

     Find any issues from these categories (only emit if you're confident):
       - spellingError
       - grammarError
       - wordChoice
       - placeholderText        (TODO / placeholder / Lorem ipsum / "Enter text here" generic)
       - untranslatedKey        (common.foo, {{var}}, [error.x], __MSG_*)
       - htmlEntityLiteral      (&amp;, &lt;, &nbsp;)
       - encodingMojibake       (Ã©, â€™ — broken UTF-8)
       - attributeEmpty         (empty alt on a non-decorative image, empty aria-label on a button)
       - attributeRedundant     (alt text duplicates visible caption word-for-word)

     Rules:
       - Do NOT flag product names, brand names, or technical acronyms as misspellings.
       - Do NOT flag intentional casing like iPhone, macOS, GitHub.
       - For "attributeEmpty", only flag images that look content-bearing (>100px wide), not pure decorations.
       - Limit to 15 findings per cell.
       - Output ONLY a valid JSON array — no prose, no markdown.

     Return JSON:
     [
       {
         "issueType":  "<one of the categories above>",
         "severity":   "low" | "medium" | "high",
         "source":     "placeholder" | "altText" | "title" | "ariaLabel" | "valueAttr" | "option",
         "snippet":    "<the offending text, max 80 chars>",
         "suggestion": "<corrected text, max 80 chars, or null>",
         "locator":    "<selector or descriptor of the element, max 80 chars>"
       }
     ]
     If nothing is wrong, return [].`
   )
   ```

4. Convert each finding into the standard issue record:
   ```js
   {
     skill: "qa-review-hidden-text",
     issueType: <finding.issueType>,
     severity: <finding.severity>,
     selector: <finding.locator>,
     description: `[${finding.source}] "${finding.snippet}"` +
                  (finding.suggestion ? ` (suggestion: "${finding.suggestion}")` : ''),
     bbox: null
   }
   ```

5. Append to issues. No screenshot annotation — attribute findings don't have bboxes.

## Probe (browser_evaluate)

```js
// probe.extractAttributeText
() => {
  const selFor = el => {
    const id = el.id ? `#${el.id}` : '';
    const name = el.name ? `[name="${el.name}"]` : '';
    return (el.tagName.toLowerCase() + id + name).slice(0, 100);
  };

  const placeholders = [];
  const altText = [];
  const titles = [];
  const ariaLabels = [];
  const valueAttrs = [];
  const optionLabels = [];

  // Placeholders
  for (const el of document.querySelectorAll('input[placeholder], textarea[placeholder]')) {
    if (placeholders.length >= 25) break;
    const t = el.getAttribute('placeholder');
    if (t && t.trim()) placeholders.push({ text: t.slice(0, 200), locator: selFor(el), inputType: el.type || 'text' });
  }

  // Alt text — include empty alts on visible images (potential a11y issues)
  for (const img of document.querySelectorAll('img')) {
    if (altText.length >= 25) break;
    const r = img.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) continue;
    const alt = img.getAttribute('alt');
    const src = (img.src || img.currentSrc || '').split('/').pop().slice(0, 30);
    altText.push({
      text: alt === null ? null : alt.slice(0, 200),
      locator: selFor(img) + `[src=…${src}]`,
      decorative: img.getAttribute('aria-hidden') === 'true' || img.getAttribute('role') === 'presentation',
      widthPx: Math.round(r.width)
    });
  }

  // Title attributes (skip on html/body/script/style)
  const SKIP_TITLE_TAGS = new Set(['HTML', 'BODY', 'SCRIPT', 'STYLE', 'LINK', 'META']);
  for (const el of document.querySelectorAll('[title]')) {
    if (titles.length >= 20) break;
    if (SKIP_TITLE_TAGS.has(el.tagName)) continue;
    const t = el.getAttribute('title');
    if (t && t.trim()) titles.push({ text: t.slice(0, 200), locator: selFor(el) });
  }

  // Aria-labels
  for (const el of document.querySelectorAll('[aria-label]')) {
    if (ariaLabels.length >= 25) break;
    const t = el.getAttribute('aria-label');
    if (t && t.trim()) ariaLabels.push({ text: t.slice(0, 200), locator: selFor(el) });
  }

  // Input/button value attributes
  for (const el of document.querySelectorAll('input[type="submit"], input[type="button"], input[type="reset"]')) {
    if (valueAttrs.length >= 15) break;
    if (el.value && el.value.trim()) valueAttrs.push({ text: el.value.slice(0, 200), locator: selFor(el) });
  }

  // Select <option> labels
  for (const opt of document.querySelectorAll('select option')) {
    if (optionLabels.length >= 30) break;
    const t = (opt.innerText || opt.value || '').trim();
    if (!t) continue;
    const select = opt.closest('select');
    optionLabels.push({
      text: t.slice(0, 200),
      locator: select ? selFor(select) + ` option[value="${(opt.value || '').slice(0,30)}"]` : 'option'
    });
  }

  const totalCount = placeholders.length + altText.length + titles.length +
                     ariaLabels.length + valueAttrs.length + optionLabels.length;

  return { totalCount, placeholders, altText, titles, ariaLabels, valueAttrs, optionLabels };
}
```

## Cell-skipping rules

- **Self-skip** if `totalCount === 0` — no attribute text on this page.
- Honors the same `[grammar].critical_routes` and `[grammar].max_cells` config as `qa-review-content` — both skills share the scope.

## Notes

- Same Sonnet pricing as `qa-review-content`. Per-cell input is smaller (attribute text is shorter than body text), so this skill is cheaper per cell.
- No DOM mutation, no `data-argus-*` attributes, no cleanup needed.
- Findings have a `source` tag (`placeholder` / `altText` / `title` / `ariaLabel` / `valueAttr` / `option`) prepended to the description so the bug report makes it obvious which attribute is broken.
