---
name: visual-companion
description: 'Choose, build and check the visual for a reply or page meant for a person: a table, a collapsed evidence block, a callout, a Mermaid diagram, or a companion artifact page, picked by what the surface renders (GitHub, chat, Notion, artifact pages). Use when the content has the shape of a board of tracked items, a flow (a sequence, a race between writers, a state machine), a before/after, or a set of options; structured-depth''s Visuals section sends readers here. Holds the surface table, the companion-page rules, the Mermaid guardrails and the render-and-look check, with scripts that pre-render Mermaid to light and dark SVG, inline it into an HTML page, and screenshot the page at desktop and phone widths.'
license: Unlicense
metadata:
  tags: "Visualization, Mermaid, Artifacts, Output Style"
  category: "productivity"
  version: "0.2"
---

# visual-companion

structured-depth decides *whether* a visual is due (its Visuals gate). This skill decides *which* one, on *which surface*, and how it is checked before it goes out. Text stays the record: every number, identifier and verbatim line in a visual also exists in the text it accompanies. A visual is a way to see the record, never the only copy of it.

## The ladder: lowest rung that carries the shape

| Rung | Use it for | Renders on |
| --- | --- | --- |
| 1 Table | items with attributes; State · Next; Checked; options | everywhere |
| 2 Collapsed block `<details><summary>…</summary>` | evidence, logs, mutation tables, long quotes a reader may skip | GitHub, artifact pages, Notion (toggle); not in plain chat |
| 3 Callout `> [!IMPORTANT]` / `[!WARNING]` / `[!NOTE]` | the one line the reader must not miss: a wall, a stop condition, an authorization | GitHub only (chat and Notion: a bold first line instead) |
| 4 Diagram (Mermaid) | a sequence, a race, a state machine, a flow with branches | GitHub and Notion render a `mermaid` fenced block; on an artifact page, pre-render it to SVG (see *Scripts*); plain chat shows the code |
| 5 Companion page (artifact) | a board the reader filters or returns to; more than six tracked lanes; a diagram beside its evidence | sessions with an artifact or page-publishing tool; otherwise an HTML file sent, or rung 4 |

What you have decides the rung: no way to publish a page means rung 5 is out; no renderer means rung 4 is a code block the reader cannot read, so drop to a table.

## Glyphs

The five are structured-depth's (`✅ landed` · `🔄 in flight` · `⏳ waiting on someone else` · `⛔ blocked` · `↗ moved this turn`); a page uses the same five on its chips and tiles, beside the word, so a reader moves between the reply and the page without relearning them.

## Companion page rules (rung 5)

- **A view of the record, dated.** Header carries "as read <date time zone>" and the record's own anchors (trunk SHA, version, the ledger or issue it mirrors). The reply in chat still carries the point, the State table and Your move; the page is additive.
- **One page, one file, no data fetched at load.** Self-contained HTML with the record written into it; scripts only from cdnjs/jsdelivr/unpkg pinned to an exact version; fonts from Google Fonts; everything else inline. Light and dark via tokens on `:root`; works at phone width with no horizontal page scroll (a wide diagram scrolls inside its own panel).
- **Cards, not prose.** One card per tracked item: identifier · title · stage chip · "moved" chip when it changed since the last read · the one next action with its owner and what it waits on · a collapsed Evidence block with SHAs, run IDs, comment IDs.
- **Filters only past six items.** Owner and open/all are enough; a filter the reader never clicks is noise.
- **One diagram per page unless asked**, beside the two sentences that say what it shows, with a figcaption that states the before and the after.
- **Republish the same file path** so the link stays; say in one line what changed.

## Mermaid guardrails

Checked against Mermaid 11.12.0.

- **In a sequence diagram, `;` ends the statement**, inside a message or a note too. `Note over R: stamp kept; a lost race re-reads` fails with `Parse error on line 3 … Expecting 'SOLID_OPEN_ARROW' …`. Use a full stop, or `#59;` for a literal semicolon.
- **In a sequence diagram, `#` cuts the message off.** `P->>R: before #330: PutItem whole row` renders as `before`. Write `PR 330`, or `#35;330` for a literal hash. Flowchart labels in `[…]` or quotes take both `;` and `#` unharmed.
- **A long note overflows its box.** Notes do not wrap the way messages do; text wider than the box spills past its edges, and in the neutral theme the spill is white on white. Break the line with `<br/>`.
- Braces in a participant alias are fine: `participant P as PATCH /items/{id}`.
- A `rect rgba(127,127,127,0.15)` band reads in both the neutral and the dark theme; a band in a theme colour does not, so render both themes when the page has both.
- **A diagram that did not render shows as code and reads as a defect.** Validate before sending (next section). Where nothing can render it (a plain chat reply), use a table.

## Validate by looking, not by exit code

1. Render the definition with the host's own renderer where the host has one (GitHub preview, Notion block). For an artifact page, pre-render to SVG and inline it (`render.mjs`, `inline.mjs`); a page that renders Mermaid at load shows code to any viewer whose browser fails to run it.
2. Screenshot the result at desktop width in light and dark, and at phone width, and read the images: `shot.mjs`, or the host's browser tool (a browser pane, Chrome DevTools) with the viewport and colour scheme set. The check is the picture: every label present and inside its box, both bands visible, no page-level horizontal scroll. At phone width a wide diagram is cut off at its panel's edge by design; the panel scrolls, the page does not.
3. Say in the reply that the visual was inspected, and at which widths and themes. "No console errors" is not the check.

## Scripts

Three Node scripts in `scripts/` (Node 18+). They run headless Chromium through `playwright-core` and load Mermaid from a local install, so nothing is fetched at render time. Install the two packages in a scratch directory and run the scripts from there; they resolve both from the working directory, so the skill folder is never written to:

```
cd <scratch dir>
npm install --no-save mermaid@11.12.0 playwright-core@1.56.0
node <skill dir>/scripts/render.mjs race.mmd race   # → race-light.svg, race-dark.svg; a parse error exits 1 with Mermaid's message
node <skill dir>/scripts/inline.mjs page.html race   # replaces <pre class="mermaid" data-diagram="race"> with both SVGs
node <skill dir>/scripts/shot.mjs page.html shot     # → shot-desktop-light.png, shot-desktop-dark.png, shot-phone.png
```

- **`render.mjs <file.mmd> [out-name] [--light neutral] [--dark dark] [--width 190]`** renders one SVG per theme (`--width` is the actor box width; Mermaid's default is 150) and suffixes Mermaid's unscoped ids (arrowheads, markers) with the render id (`arrowhead-race-light`), so the light and dark copies, and several diagrams, share a page without drawing each other's markers.
- **`inline.mjs <page.html> <name> [--svg dir] [--out file]`** swaps the `<pre class="mermaid">` for a block between `<!-- diagram:<name> -->` markers (re-running it replaces that block) and adds one `<style id="diagram-themes">` that shows the dark SVG under `@media (prefers-color-scheme: dark)` guarded by `:root:not([data-theme="light"])`, and under `:root[data-theme="dark"]`. The diagram shrinks to 70% of its natural width at most, then scrolls inside its panel.
- **`shot.mjs <page.html|url> [prefix]`** writes the three full-page screenshots and prints, per view, `{scrollWidth, innerWidth}`, the rendered size of each visible SVG, and console errors; it exits 1 when the page itself scrolls sideways.
- **Browser**: `$CHROMIUM_PATH` if set, else Playwright's own Chromium (`npx playwright install chromium`), else an installed Chrome, else Edge. `mmdc` (mermaid-cli) downloads its own browser through puppeteer, which fails where downloads are blocked; these scripts use whatever browser is already there.

**Not verified**: rendering of `rect` bands inside Notion (GitHub and Notion render Mermaid; band colours were checked only on an artifact page).
