---
name: widget-design
description: MANDATORY before every genspark_render_widget call. Read this skill and copy the closest reference skeleton under references/ before writing any widget_code — comparison tables, ranked lists, schedule/match cards, stat summaries. Adapting a proven skeleton beats designing from scratch every time.
---

# Widget design — reference-first workflow

The host renders `widget_code` in a sandboxed iframe with the Genspark design
tokens injected (CSS variables + system fonts + light/dark). Widgets must read
as **native product cards** — consistent with the host UI — not as standalone
art pieces or styled documents.

## Workflow (do these in order)

1. **Pick the closest reference skeleton** from `references/` in this skill's
   directory:
   - `comparison-card.html` — N columns of attributes compared side by side
     (product A vs B, company comparison, spec sheets)
   - `ranked-list.html` — ordered rows with a magnitude bar + value
     (odds, market share, benchmark scores, top-10 lists)
   - `schedule-card.html` — chronological event rows with status
     (match schedules, itineraries, timelines, release calendars)
2. **Read the skeleton file** (`cat` it). Understand its grid before touching it.
3. **Plan before CSS**: list your sections (max 3), your grid columns, and the
   ONE accent color. If the content doesn't fit a skeleton's structure, keep
   its grid/spacing/type system and change only the row template.
4. **Fill in real data.** Keep every structural rule below intact.

Designing from scratch is a last resort — only when no skeleton's structure
fits at all. Even then, every rule below still applies.

## Non-negotiable rules

- **One accent color** per widget: `--color-brand-secondary` or a single
  categorical ramp (`.c-blue` etc.). Semantic `--color-success/error` ONLY for
  true win/loss/alert states. Never 3+ decorative hues.
- **Two text sizes, two weights**: `--text-body` (600) for titles/values,
  `--text-small`/`--text-caption` (400) for meta. No `--text-h1/h2` inside cards.
- **One grid**: the header row AND every data row live in the SAME CSS grid
  container — `grid-template-columns` defined once, rows as
  `display: contents` wrappers. Never a separately-padded header bar (its
  edges drift out of alignment with the body). Tint header CELLS, never a
  full-width strip.
- **Numbers**: right-aligned, `font-variant-numeric: tabular-nums`.
- **Spacing**: ONE padding value per level (`--space-12` or `--space-16`).
  Cap inner content width at ~640px; never stretch sparse rows full-width.
- **Emphasis**: key row gets a subtle background tint (`--color-bg-subtle` or
  a ramp `-50`), NEVER a thick/colored/dashed border.
- **Chips**: one pill style per widget, placed next to the text they qualify.
- **Banned**: emoji as icons/bullets/section markers (content glyphs like
  flag emoji in a team name are fine), gradients, dashed borders, left-border
  accent stripes, inner-element shadows, decorative stats.
- **Density caps**: ≤3 sections, ≤10 rows, ≤2 meta lines per row, ≤1 action.
  Long-form analysis belongs in your Markdown reply, not in the card.

## Technical contract (host iframe)

- HTML body markup only — no `<!DOCTYPE>/<html>/<head>/<body>`; optional
  `<style>`/`<script>`. SVG mode: start with `<svg`.
- Only the injected CSS variables for colors/spacing/type — never hard-coded
  hex, never `font-family`.
- Transparent outer background (the host card provides the chrome).
- In-memory JS only — no `localStorage`/`sessionStorage`. External libs only
  from cdn.jsdelivr.net / unpkg.com / cdnjs.cloudflare.com / esm.sh; no
  external images or fonts.
