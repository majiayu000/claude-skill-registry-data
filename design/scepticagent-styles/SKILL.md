---
name: scepticagent-styles
description: ScepticAgent UI and styles reference. Use whenever the user wants to change the side panel UI, modify highlight colours, update the markdown renderer, work with CSS architecture, add or change category colours, or understand how the sidepanel renders analysis output.
---

## Highlight categories

| Category | CSS class suffix | Color | Meaning |
|----------|-----------------|-------|---------|
| misinformation | `misinformation` | `#ff6b6b` (red) | False, misleading, or lacking critical context |
| emotional | `emotional` | `#ffa94d` (orange) | Fear appeals, outrage bait, us-vs-them framing |
| bias | `bias` | `#ffd43b` (yellow) | Biased framing, selective emphasis, loaded language |
| supported | `supported` | `#69db7c` (green) | Well-supported, verified claim |
| logical | `logical` | `#da77f2` (purple) | Internal contradiction, non-sequitur, false dichotomy |

All five category colours are duplicated across four CSS selectors each:
`.scan-pill.{cat}`, `.hl-dot.{cat}`, `.hl-item-dot.{cat}`, `.summary-bullet-{cat}`

---

## Markdown renderer (`sidepanel/app.js` — `renderMarkdown` function)

- `listType` is a **string** (`"ul"` / `"ol"` / `null`) — **not a boolean**. The `closeList()` helper checks `if (listType)`.
- List items are matched against `trimmed` lines (after `.trim()`), not raw lines — required to handle indented list items correctly.
- `## heading` lines → collapsible `<h2>` + `<div class="section-body">`. Clicking the heading toggles `.collapsed` class, which hides the body via CSS.
- Blank lines → `<br>` (not `</p><p>`).
- Links: `[text](url)` → `<a target="_blank" rel="noopener noreferrer">`.
- Analysis preamble appearing **before** the first `\n## ` heading is skipped entirely and not rendered — the renderer starts output from the first `##` section.

---

## CSS architecture (`sidepanel/style.css`)

**Dark theme palette (hardcoded — no CSS custom properties):**

| Role | Value |
|------|-------|
| Background | `#1a1b1e` |
| Surface (cards, inputs) | `#25262b` |
| Border | `#373a40` |
| Primary text | `#c9d1d9` |
| Accent blue | `#4dabf7` |

**Key component classes:**
- `#highlight-summary` — summary card: `background: #25262b`, `border: 1px solid #373a40`, `border-radius: 8px`
- `.section-body` — collapsible analysis section body, hidden when parent `<h2>` has `.collapsed`
- `.scan-pill` — top-of-panel category pill counts (e.g. "3 misinformation")
- `.hl-item` — individual highlight entry in the list
- `.hl-dot` / `.hl-item-dot` — colored dot next to a highlight

**Note:** There are no CSS custom properties (`--var`) in this codebase. All colour values are hardcoded literals. When adding new colours, continue this pattern.
