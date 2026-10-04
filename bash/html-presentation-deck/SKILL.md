---
name: html-presentation-deck
description: "Use this skill when the user wants a browser-native HTML presentation, web deck, single-file slides, horizontal swipe deck, keynote-style web page, investor/demo-day HTML deck, or a shareable presentation that opens in a browser. Also use when the user asks for an editorial deck, clean grid deck, presentation microsite, slide landing page, or HTML slides. Do not use this for .pptx files; use the pptx skill for PowerPoint input or output."
---

# HTML Presentation Deck

Create polished, browser-native presentation decks as standalone HTML files. The output is a web presentation, not a PowerPoint file.

## Skill directory (`<skill-dir>`)

**`<skill-dir>`** is always the folder that contains **this** `SKILL.md`. Install method chooses where that folder lives — do not mix paths across installs.

### `@citedy/skills` (Claude Code / Codex CLI)

`npx @citedy/skills install` copies into the **user project** (where you run the command), not into the npm cache:

| Target | Skill folder | Slash command |
|--------|--------------|---------------|
| Codex | `<project>/.codex/skills/html-presentation-deck` | `<project>/.codex/commands/html-deck.md` |
| Claude | `<project>/.claude/skills/html-presentation-deck` | `<project>/.claude/commands/html-deck.md` |

If both exist, prefer the namespace that matches where `/html-deck` was invoked (see `commands/html-deck.md` in the npm package).

### AdClaw agent (built-in skill)

AdClaw does **not** install skills under `.codex/skills` or `.claude/skills`. It resolves skills from the working directory (default `~/.adclaw`, overridable with `ADCLAW_WORKING_DIR`):

| Context | `<skill-dir>` |
|---------|----------------|
| Runtime (normal use) | `$ADCLAW_WORKING_DIR/active_skills/html-presentation-deck` |
| User customized copy | `$ADCLAW_WORKING_DIR/customized_skills/html-presentation-deck` (wins over active when present) |
| AdClaw repo development | `src/adclaw/agents/skills/html-presentation-deck` (built-in source; synced into `active_skills` on init) |

When AdClaw loads this skill, use the resolved directory from the agent — not a `.codex` path.

### Both in one machine

AdClaw and `@citedy/skills` keep **separate copies**. Updating one does not update the other. Pick the `<skill-dir>` that matches the tool you are using for this deck.

### Validators (any install)

Run from the **deck project root** (where `deck/index.html` lives):

```bash
python3 <skill-dir>/scripts/validate_html_deck.py deck/index.html
python3 <skill-dir>/scripts/validate_deck_quality.py deck/index.html
```

Never paste `src/adclaw/agents/...` into a Codex/Claude project after `npx @citedy/skills install` — that path exists only inside an AdClaw source checkout.

## Default Mode: Product Grid v2

Use **Product Grid v2** by default for product, launch, sales, investor, demo,
operating-model, data, and strategy decks. This is the strict quality path.

Product Grid v2 uses:

- Template: `assets/template-product-grid.html`
- Layout registry: `references/layout-lock.md`
- Layout skeletons: `references/layouts-product-grid.md`
- Component contract: `references/components-product-grid.md`
- Quality validator: `scripts/validate_deck_quality.py`

The older `template-clean-grid.html` and `template-editorial.html` files remain
available for legacy decks, but new work should start from Product Grid v2 unless
the user explicitly asks for the legacy editorial system.

### Product Grid v2 Non-Negotiables

- Every slide must use `data-system="product-grid"`.
- Every slide must use a registered `data-layout="PGxx"`.
- Start by writing a slide map: `slide / message / layout / density / image slot / risk`.
- Do not invent one-off classes in the deck HTML.
- Do not use inline `font-size`; edit copy or choose another layout.
- Do not use negative letter spacing, gradients, shadows, decorative blobs, or nested cards.
- Every local image must include `alt` and `data-image-slot`.
- SVG may draw geometry only; visible labels must be HTML.
- If content does not fit, split the slide instead of shrinking text.

### Product Grid v2 Workflow

1. Read `references/layout-lock.md`.
2. Read `references/components-product-grid.md`.
3. Read only the required skeletons from `references/layouts-product-grid.md`.
4. Copy `assets/template-product-grid.html` to `deck/index.html`.
5. Replace the `<title>` placeholder and `<!-- SLIDES_HERE -->`.
6. Use the slide map to pick `PG01`-`PG14` layouts before writing HTML.
7. Run both validators (see commands above).
8. Open in a browser and check desktop plus mobile for overflow and image legibility.

## When To Use

Use this skill for:

- Single-file HTML slide decks that open locally or can be hosted.
- Horizontal swipe or keyboard-driven presentations.
- Product launches, demo days, internal talks, sales narratives, research summaries, and strategy presentations.
- Screenshot-heavy decks where product UI needs to be framed cleanly.

Use the `pptx` skill instead when the user needs a `.pptx` file, PowerPoint template editing, or slide XML manipulation.

## Visual Systems

Choose one system per deck. Do not mix systems in the same presentation.

### Editorial

Use for narrative talks, opinionated strategy decks, customer stories, founder updates, and presentations that need a magazine-like rhythm.

Design traits:

- Warm paper backgrounds, serif display titles, restrained ink-like accents.
- Large opening and closing statements.
- Alternating hero slides, image pages, quote pages, and structured evidence pages.
- Best when the deck needs a memorable point of view.

Template: `assets/template-editorial.html`
References: `references/themes.md`, `references/typography.md`, `references/layouts-editorial.md`, `references/screenshot-framing.md`

### Clean Grid

Use for data, product, engineering, roadmap, comparison, operating model, and board-style decks.

Design traits:

- Strict grid, left-aligned typography, high contrast, sharp rectangular modules.
- One accent color only.
- Strong hierarchy for numbers, timelines, tables, diagrams, and product screenshots.
- Best when the deck needs clarity, precision, and executive readability.

Template: `assets/template-clean-grid.html`
References: `references/themes.md`, `references/typography.md`, `references/layouts-clean-grid.md`, `references/screenshot-framing.md`

## Workflow

1. Clarify the brief.
   - Audience and setting.
   - Target duration or slide count.
   - Required message, data, screenshots, and constraints.
   - Preferred visual system: Editorial or Clean Grid.

2. Create the project folder.
   - Put the deck at `deck/index.html`.
   - Put images at `deck/images/`.
   - Use short English filenames such as `01-cover.jpg` or `06-dashboard.png`.

3. Copy one template.
   - Editorial: copy `assets/template-editorial.html`.
   - Clean Grid: copy `assets/template-clean-grid.html`.
   - Replace the title placeholder immediately.
   - Replace the `<!-- SLIDES_HERE -->` marker with slide sections.

4. Build the outline before writing slides.
   - One idea per slide.
   - Use 8-12 slides for short product or strategy decks.
   - Use 15-25 slides for talks longer than 25 minutes.
   - Alternate dense slides with breathing-room slides.

5. Choose layouts from the matching reference file.
   - Editorial layouts are not interchangeable with Clean Grid layouts.
   - Do not invent many new classes; use the template classes first.
   - If a custom adjustment is unavoidable, prefer a small inline style on the slide section.

6. Choose typography through tokens (legacy Editorial / Clean Grid only).
   - Read `references/typography.md` before changing fonts, tracking, or type scale.
   - Use the default system-safe preset unless the user asks for a stronger typographic voice.
   - Keep offline rendering by default; use external fonts only when the user explicitly allows them.
   - Change `--display-font`, `--text-font`, and `--label-font` tokens instead of editing every heading class.

7. Handle screenshots deliberately.
   - Read `references/screenshot-framing.md` before placing product screenshots.
   - Preserve screenshot content when details matter.
   - Use generated background assets only as neutral framing surfaces.
   - Do not crop away important UI text, numbers, or controls.

8. Validate before presenting.
   - From the project root, run `python3 <skill-dir>/scripts/validate_html_deck.py deck/index.html`.
   - Open the deck in a browser.
   - Check keyboard navigation, slide index, mobile scaling, broken images, and text overflow.

## Output Requirements

- The deck must be English-only unless the user explicitly asks for another language.
- Never include non-English text, non-English comments, non-English font names, or non-English placeholders.
- Never mention the upstream inspiration, repository names, or author names in generated decks.
- Keep all visible deck text user-facing and presentation-ready.
- Keep source comments in English.
- Avoid external runtime dependencies when possible; templates must work offline.
- Do not use bright accent colors for small text on light panels. Use contrast-safe text tokens such as `--accent-text`.

## Slash Command (`/html-deck`)

When invoked as `/html-deck` via `@citedy/skills`, discover `<skill-dir>` under `.codex/skills` or `.claude/skills` first (see npm `commands/html-deck.md`). When invoked inside AdClaw, use the agent-resolved active/customized skill path.

After building the deck, run both validators with that `<skill-dir>`, then print `deck/index.html` and how to open it locally.

## Related Skills

- **pptx**: PowerPoint input/output, template editing, and `.pptx` manipulation.
- **marketing-sales-enablement**: Pitch deck strategy, slide narrative, sales collateral.
- **marketing-image**: Image generation and visual asset planning.
- **marketing-video**: Video or animated presentation assets.
