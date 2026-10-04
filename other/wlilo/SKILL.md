---
name: wlilo
description: Create WLILO (White Leather Industrial Luxury Obsidian) SVGs and CSS — the luxury design language of cream-leather backgrounds, deep obsidian panels, scarce gold accents, gemstone CTAs, and emoji/unicode iconography. Use this skill whenever the user says WLILO, white leather, obsidian, industrial luxury, or asks for a premium/luxury-styled SVG, diagram, poster, status board, dashboard mockup, or matching CSS theme — and also when they ask to "illustrate" a topic or system as a styled visual, even if they never name a style. Covers research-before-drawing, choosing how much vector drawing a task needs, exact palette/typography tokens, gemstone and panel construction recipes, and validation.
---

# WLILO — White Leather Industrial Luxury Obsidian

A design language for **work artifacts**: diagrams agents study, dashboards humans scan while
debugging, posters that must stay legible at a glance. Its ruling principle is *clarity under
cognitive load* — every choice reduces friction, and beauty emerges from function:

- **White leather** (cream `#faf9f7`→`#ebe8e2`) carries the page — soft on eyes over long reads.
- **Obsidian panels** (`#2d2d2d`→`#1a1a1a`, thin gold frame) anchor attention: figure-ground
  separation; what's inside a panel matters more than what's outside.
- **Gold is scarce by design** (`#c9a962`→`#e8d5a3`): thin strokes, headers, separators,
  arrowheads. *When everything glows, nothing does.* The same scarcity law governs emoji.
- **Depth is soft**: low-blur shadows (stdDeviation 3–4), never harsh; surfaces always carry a
  gentle diagonal gradient — flat fills look cheap.
- **Gemstone CTAs** carry fixed meaning: sapphire = start/primary, emerald = decision/branch,
  ruby = result/destructive.

Reference files (read as needed): `references/tokens.md` (all palette/type/geometry values,
two registers, CSS variable schema) · `references/svg-recipes.md` (defs block, panel/gemstone/
connector constructions, width math, validation) · `references/glyphs.md` (emoji + unicode
vocabulary and rendering gotchas) · `references/finish.md` (the professional finish pass —
composition, hierarchy, inhabitation) · `assets/white-leather-obsidian.json` (machine-readable
theme for CSS generation).

## Step 1 — Research the topic before you draw it

A WLILO artifact is a *claim about its subject*. Wrong content in beautiful chrome is worse
than ugly truth, because the luxury register makes errors look authoritative. So before any
visual decision:

1. **Research the subject** until you can state the 3–7 load-bearing facts or relationships
   the visual must communicate. Use whatever the topic demands: web search for external
   topics, reading the actual code for systems, querying the actual data for dashboards.
   Depth scales with stakes — a hero poster explaining TLS deserves real sources; a status
   card of data you already hold needs none.
2. **Write the fact sheet down** (a short list or JSON). Every element you later draw must
   trace back to an entry here; anything you can't trace, you cut.
3. **Model the structure** — turn the fact sheet into a small JSON data model (items, types,
   states, relations, an `icon` emoji field per item). This is the corpus's First Law:
   *Structure First — define content before any visual design.* Layout and styling operate on
   this model, never on vibes.

## Step 2 — Choose the vector intensity

Not every task deserves full vector drawing. Pick the lightest tier that serves the purpose;
you can always climb one tier on request:

| Tier | When | What you draw |
| --- | --- | --- |
| **1 · Glyph-led** | Quick status boards, lists, tables, terminal-flavored cards | Leather bg + one obsidian panel; everything else is text: emoji icons, block-bar charts `▇▇▂▁`, box-drawing, geometric dots. Minutes, near-zero paths. |
| **2 · Hybrid** (default) | Explanatory diagrams, flows, architecture, dashboards | Vector panels + bezier connectors + gold accents; emoji as node icons; unicode for inline data. The corpus's "simple" pipeline: model → manual layout → inline components → validate. |
| **3 · Full luxe** | Hero pieces, posters, launch art, UI mockups with gemstone CTAs | Everything in tier 2 plus gemstone buttons, brushed-metal textures, grain patterns, careful optical spacing — the corpus's full generator-grade pipeline with both spatial validators. |

## Step 3 — Choose the register, then compose

Two sibling palettes exist — **diagram register** (warmer; docs and diagrams) and **Luxe/UI
register** (crisper; UI mockups, gemstone CTAs, HTML/CSS). Pick ONE per artifact and never mix
them (`references/tokens.md` has both tables and the tells).

Compose in the five-layer order — in SVG, document order is the only z-order:
background gradient (+ grain) → connectors (BEFORE nodes, so nodes paint on top) → panels/
nodes → labels/glyphs → top ornaments. Position with `<g transform="translate()">` groups and
local coordinates. Center text with `text-anchor="middle"` at computed centers. Constructions,
the paste-ready defs block, and the connector formula live in `references/svg-recipes.md`.

**Budget text width before placing anything** — text overflow is the #1 defect class:
`width = chars × font_size × ratio` (mono 0.60 / sans 0.52 / serif 0.55), +8–16px padding per
side, text ≤80% of its container, **emoji count double**. You cannot see the render; the
arithmetic is your eyes.

## Emoji & unicode

Emoji and unicode glyphs are the illustration shorthand — iconography at text cost. One emoji
per node/section doing a label's job (🗄️ ⚙️ 🌐 🔒 📊 ✅ ❌ ⚠️); block characters as instant
bar charts; geometric glyphs (`● ◆ ✦`) as token-colorable marks (they obey `fill`; emoji
don't); `✦` in gold is the house accent star. This vocabulary is *required illustration* — even
a serious engineering diagram carries roughly one semantic icon per actor/section; the finish
pass trims glyph density, never removes the vocabulary (a zero-glyph result is an over-correction).
The full vocabulary, the tone rules, and the rendering gotchas (platform emoji fonts,
monospace-only box drawing, never entity-encode emoji) are in `references/glyphs.md` — read it
whenever glyphs feature in the piece.

## CSS surface

When the deliverable includes CSS (theme a page, style a component set):
- Define `--wlilo-*` custom properties on `:root` or a `.wlilo-app` scope from
  `references/tokens.md` (or generate from `assets/white-leather-obsidian.json`).
- Style through semantic classes (`.wlilo-panel`, `.wlilo-header`, `.wlilo-cta--ruby`) —
  never per-element inline styles, never freestyled hex.
- Dual-surface rule: dark panels sit on a light page, so provide text tokens for BOTH surfaces
  (page text `#0a0d14` family; on-panel text `#f0ece4`/leather family).
- Shadows/radii/transitions come from the token tables; gemstone CTAs use the 3-layer recipe
  translated to CSS (frame border + gradient + glow).
- Inline SVG inside your own page may use the CSS variables; SVG delivered as files/`<img>`
  must bake colors in at build time (variables won't resolve there).

## Step 4 — The finish pass (valid ≠ designed)

Validation makes an artifact correct; composition makes it professional. Read
`references/finish.md` and run its pass after layout, every time: the **void check** (panel
content occupies ≥65% of the panel — obsidian is a stage, not a warehouse), **optical
relationships** (8px grid; badges never glued to wordmarks; constant repeated offsets),
the **hierarchy ladder** (three text roles per container; mono for literals only; hero
elements sized with confidence), **line hierarchy** (structural lines quiet, flow arrows
assertive, at most ONE gold path), **perceptible craft** (claimed luxury must pass the
point-at-it test at 100% zoom), and finally the **squint test** at ~25%.

## Step 5 — Validate before you declare done

An agent that trusts its mental model ships overlapping text. Always run the validation pass
in `references/svg-recipes.md`: the repo toolchain when available (`svg-validate` →
`svg-collisions --strict`, zero HIGH → `svg-overflow`, zero HIGH), otherwise the portable
checklist (parse, viewBox + `<title>`/`<desc>`, escaping, width math re-run, pairwise overlap
walk, palette audit). Repair loop: fix HIGH first, move the later element minimally, re-check
for cascades. If it feels off, the three sanctioned remedies in order: reduce glow, lighten
the leather midtone, widen padding.

## Anti-patterns

- Freestyled colors (any hex not in the token tables) · mixed registers in one artifact.
- Gold or emoji everywhere — scarcity is the aesthetic.
- Obsidian nested in obsidian; crowded panels; text touching strokes.
- Flat fills on surfaces; harsh/high-blur glows.
- Drawing before researching; elements that trace to no fact-sheet entry.
- **Valid-but-void**: panels mostly empty, content floating in dark space.
- **Glued ornaments**: badges/chips touching wordmarks; orphan elements anchored to nothing.
- **Terminal-dump typography**: prose in mono; one text size for everything in a container.
- **Rumored luxury**: grain/metal/bezels present in markup but invisible at viewing scale.
- Declaring done without the finish pass AND the validation pass.
