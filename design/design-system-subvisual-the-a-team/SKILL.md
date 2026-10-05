---
name: design-system
description: Use when a project's visual foundation — typography scale, color palette, spacing — needs establishing as canonical design tokens; the target has no design system yet (the 0→1 case), the A-Team design phase needs tokens for the lofi and the spec's design-system mapping, or a human runs the token flow standalone ("set up the design system", "pick fonts and colors", "define design tokens"). In the A-Team pipeline it is conducted by ateam-design in pipeline mode — no interview; inputs derive from context.md's ## Design context, a missing brand seed becomes a TBD-draft plus a blocking flag, and outputs land durable at docs/product/design-system/. Standalone keeps the upstream two-pass interview. Do not use to edit an existing token (edit the source file directly), to regenerate an existing system (consume it — regeneration only on explicit human instruction), or to pick a brand identity from scratch.
metadata:
  version: 0.1.0
  owner: Design (implemented on their behalf; every design opinion traces to the upstream skill)
  provenance: ported 2026-08-11 from subvisual/harness skills/design/design-system @ 940c86631660. The design-lead-authored guideline content — preset table, anti-collision rule, OKLCH seed rules, WCAG nudge loop, token formats, generate-scale.mjs — is preserved verbatim; adaptation is confined to interaction mode (pipeline vs standalone) and A-Team paths. The shadcn bridge is an A-Team extension and is marked as such.
---

# design-system

Establish typography, an OKLCH color palette, and spacing as canonical design
tokens. Typography drives the spacing scale; the palette is generated from the
design briefing (or a supplied brand seed) into perceptually uniform OKLCH
tint scales. **Light mode only in v1** — dark mode is an open item for
`research-plan.md`, never an invented palette.

`generate-scale.mjs` (in this skill directory, no dependencies) does the
mechanics: `typography <base> <ratio>` · `color <kind> <hue> <chroma>
[lAdjust]` · `contrast <hex1> <hex2>`.

## Modes

Exactly one fires per invocation — declare which in your first output line.

- **Pipeline** — conducted by `ateam-design`. Never asks a question: every
  input derives from `context.md`'s `## Design context` per the derivation
  table below; what cannot derive becomes a visible `TBD` and a flag. Variant
  choice is the human's at the design gate; under a non-block `gate_policy`
  the skill self-selects the recommended variant **only if** the design bank's
  self-select consent was captured at the grill, recording it as a provisional
  call in `research-plan.md`.
- **Standalone** — a human invoked it directly. Run the upstream interactive
  flow exactly as written in Process below: ask, confirm, then write. Durable
  writes still require the read-back — standalone is not a back door.

## Where tokens live (A-Team paths)

Source of truth, **durable layer of the target repo** — gate-reviewed, never
silently overwritten (CONTRACT.md durable rules):

- `docs/product/design-system/scale.ts` — typography + spacing tokens
- `docs/product/design-system/palette.ts` — color tokens
- `docs/product/design-system/shadcn-theme.css` — the shadcn role-variable
  bridge (A-Team extension, below)

Materialised for the lofi (when `docs/features/<slug>/lofi/` exists):

- `docs/features/<slug>/lofi/src/styles/tokens.css` — `:root { --... }` block
- `docs/features/<slug>/lofi/tailwind.config.mjs` — references `var(--...)`
- `docs/features/<slug>/lofi/scale-variants/{name}.css` and
  `palette-variants/{name}.css` — alternate token blocks for `?scale=` /
  `?palette=` comparison

If no lofi exists yet, write only the source-of-truth files; the lofi picks
them up when `build-lofi` runs.

Production materialisation (the target's `src/`, Tailwind config, shadcn
install) is **never this skill's write** — the dev phase materialises against
`spec.md`'s mapping. Whether the target uses Tailwind v3 config or v4
`@theme` is a dev-time fact read from the target repo; the CSS variables here
are version-agnostic.

## Create-once

Before generating anything, check for an existing system:

1. `docs/product/design-system/` exists, or A-Team Config's `design system
   path` points at a real token source → **consume, don't regenerate**. Read
   the tokens as settled facts; report them; stop.
2. If `## Design context` now contradicts the existing tokens (e.g. "avoid
   blue" while `brand-500` is blue), do **not** auto-regenerate — surface the
   contradiction as a flag at the design gate and let the human decide.
3. Regeneration has exactly two triggers: an explicit human instruction (gate
   revision notes, or standalone invocation saying so). Never spontaneous.

## Pipeline derivation — replaces the interview

The upstream questions are answered from durable context, not asked. **Scan
the target first** (the design bank's own rule): existing tokens/CSS
variables, brand assets, style guides — a fact the repo already answers is
read, not derived.

| Upstream input | A-Team source | When absent |
|---|---|---|
| Specimen category (sans/serif/mono/display) | `## Design context` typography answer (design-intake bank) | default sans-serif (upstream default); mark *derived* |
| Scale preset (base, ratio) | `## Design context` density/feel answer | derive from aesthetic direction — calm/airy/editorial → Relaxed · dense/fast/technical → Compact · spacious/luxury → Spacious · else Balanced; mark *derived*, emit 2–3 scale variants for the gate |
| Brand seed (hex/hue/brand name) | `## Design context` color constraints; brand assets found in the target | **TBD-draft** (below) + blocking flag |
| Domain/industry | `context.md ## Overview` | — |
| Mood axes | `## Design context` users & emotional goals + brand personality | *derived* from adjacent fields; flag |
| Reference / anti-reference brands | `## Design context` aesthetic direction | skip nudging toward references; note the gap |
| Audience sophistication | `## Design context` users | *derived*; flag |
| Colors to avoid | `## Design context` color constraints | — |
| WCAG bar | `## Design context` accessibility | default AA (4.5:1 body) |

**TBD-draft (no brand seed anywhere):** the design lead's red flag —
never pick colors from nothing — holds in substance: generate everything that
needs no brand opinion (neutral scale at a default hue bias, the four
fixed-hue semantics, the full typography pass), write `brand`/`accent` as
explicit `TBD: no brand seed in Design context`, and report it as a
**blocking flag** in the phase report. The lofi stays greyscale regardless,
so nothing downstream is blocked from *rendering* — only from shipping a
brand nobody chose.

Every derived value is listed in `design.md`'s options/reasoning section and
appended to `research-plan.md`'s `## Assumptions` tagged `· [design phase]`
with a confidence level.

## Process

*The guideline content below is the design lead's, preserved from upstream.
"Ask" steps fire in standalone mode; pipeline mode answers them from the
derivation table.*

### Pass 1: Typography

1. **Specimen category.** Ask: sans-serif (default), serif, monospace, or
   display? Don't ask for a specific font yet — the `fontFamily` block gets a
   `TODO: project font` placeholder; system fallback stack is filled per
   category.

2. **Pick presets.** Show the four curated presets plus an optional custom tuple:

   | Preset | Base | Ratio | Character |
   |---|---|---|---|
   | Compact | 16 | 1.2 | fast, dense |
   | Balanced | 16 | 1.333 | steady |
   | Relaxed | 18 | 1.414 | calm |
   | Spacious | 20 | 1.5 | airy |
   | Custom | user-supplied (base, ratio) | — |

   Ask the user to pick one preset, or "show me a few to compare." Multiple →
   emit as variants under `scale-variants/`.

3. **Compute the scale.** Invoke `node generate-scale.mjs typography <base>
   <ratio>`. The script returns:
   - `sizes`: { caption, body, h3, h2, h1 } — each snapped to a multiple of 4,
     with anti-collision applied.
   - `lineHeights`: matching, each a multiple of 8 (baseline grid is half, so
     a multiple of 4).
   - `spacing`: { xs:4, s:8, m:16, l:24, xl:32, xxl:48 } — fixed for v1.
   - `warnings`: any string describing collisions that required ≥2 bumps.

4. **Surface warnings.** If `warnings` is non-empty, print the message
   verbatim. Soft warning only — do not block, do not auto-pick another
   preset. Let the user decide (pipeline: keep the preset, carry the warning
   into the gate report).

### Pass 2: Color

1. **Brand seed check.** Ask: "Do you already have brand colour(s) you need
   to lock — hex, hue, or a brand name?" If yes → skip the vibe interview;
   convert the supplied input into a seed hue/chroma pair and continue.

2. **Vibe interview** (only if no seed; pipeline reads these from
   `## Design context`). Five questions, in order:
   1. What domain or industry is the product in?
   2. Mood on three axes: warm↔cool, calm↔energetic, sophisticated↔playful.
   3. Reference brand to lean toward + one to feel distinct from.
   4. Audience sophistication.
   5. Anything to actively avoid.

3. **Propose seed hues** (reasoning from the interview). Surface these before
   generating (pipeline: in `design.md`'s reasoning, reviewed at the gate).
   - Brand hue (H 0–360°), chroma 0.10–0.20 (low for sophisticated/calm, high
     for energetic/playful).
   - Neutral hue, chroma 0.01–0.03, biased ±15° from brand for tonal harmony.
   - Optional accent hue (90° or 180° from brand) if the vibe needs a
     counter-colour.
   - Semantic placeholders: success 145°, warning 70°, error 25°, info 240°.
     These are fixed per-language convention; only the lightness curve adapts.

4. **Generate tint scales.** Invoke `node generate-scale.mjs color <kind>
   <hue> <chroma>` for each scale (brand, neutral, accent if any, four
   semantics). The script returns 10 steps (50, 100, …, 900) as
   `{ oklch, hex }` pairs.

5. **WCAG nudge loop** (max 2 iterations).
   - Check contrast: `brand-500` on `neutral-50`, and `neutral-50` on
     `brand-500`.
   - If either is below 4.5:1, regenerate with the L curve adjusted down 0.02
     at the relevant steps (`lAdjust`).
   - After 2 nudges, if still failing, surface the failure. Don't ship a
     low-contrast palette silently.

6. **Generate variants if requested.** "Show me 3 palettes" (pipeline: the
   diverge-by-default requirement) → generate two or three with slightly
   varied hue/chroma seeds, write to `palette-variants/`, and record in
   `design.md` why each exists and which is recommended.

## Anti-collision rule (typography)

Body is the anchor. Snap each scale level to nearest multiple of 4. Walk
levels above body upward: each must be ≥ previous + 4 (bump if not). Walk
levels below body downward: each must be ≤ previous − 4 (bump if not).

If any level required ≥2 bumps, surface a soft warning: "Ratio X at base Y
collides too tight. Try a wider ratio or larger base." Continue writing — do
not hard-stop. The user picks.

## Token format

### `docs/product/design-system/scale.ts`
```typescript
export const scale = {
  fontFamily: {
    // TODO: project font
    sans: 'ui-sans-serif, system-ui, -apple-system, sans-serif',
  },
  base: 16,
  ratio: 1.333,
  sizes: { caption: 12, body: 16, h3: 20, h2: 24, h1: 32 },
  lineHeights: { caption: 16, body: 24, h3: 28, h2: 32, h1: 40 },
  spacing: { xs: 4, s: 8, m: 16, l: 24, xl: 32, xxl: 48 },
} as const;
```

### `docs/product/design-system/palette.ts`
```typescript
export const palette = {
  brand: {
    50: { oklch: 'oklch(0.985 0.02 240)', hex: '#f6faff' },
    // ... 100–900
  },
  neutral: { /* same shape */ },
  semantic: {
    success: { default: { oklch: '...', hex: '...' }, bg: { oklch: '...', hex: '...' } },
    warning: { /* ... */ },
    error:   { /* ... */ },
    info:    { /* ... */ },
  },
} as const;
```

### `docs/features/<slug>/lofi/src/styles/tokens.css`
```css
:root {
  /* Typography */
  --font-sans: ui-sans-serif, system-ui, -apple-system, sans-serif;
  --size-body: 16px;
  --line-body: 24px;
  /* ...other sizes/line-heights/spacing */

  /* Brand scale (OKLCH triplets — space-separated, no commas) */
  --brand-50: 0.985 0.02 240;
  --brand-100: 0.965 0.04 240;
  /* ...200–900 */

  /* Neutral, semantic — same pattern */
}
```

### `docs/features/<slug>/lofi/tailwind.config.mjs`
```js
import { scale } from '../../../product/design-system/scale.ts';

export default {
  content: ['./src/**/*.{astro,html,js,ts}'],
  theme: {
    extend: {
      fontFamily: { sans: 'var(--font-sans)' },
      fontSize: {
        caption: ['var(--size-caption)', { lineHeight: 'var(--line-caption)' }],
        body:    ['var(--size-body)',    { lineHeight: 'var(--line-body)' }],
        h3:      ['var(--size-h3)',      { lineHeight: 'var(--line-h3)' }],
        h2:      ['var(--size-h2)',      { lineHeight: 'var(--line-h2)' }],
        h1:      ['var(--size-h1)',      { lineHeight: 'var(--line-h1)' }],
      },
      spacing: scale.spacing,
      colors: {
        brand: {
          50:  'oklch(var(--brand-50))',
          100: 'oklch(var(--brand-100))',
          // ...
        },
        neutral: { /* ... */ },
        success: 'oklch(var(--success))',
        warning: 'oklch(var(--warning))',
        error:   'oklch(var(--error))',
        info:    'oklch(var(--info))',
      },
    },
  },
};
```

`lofi-lint.mjs` treats the `fontSize` keys above as type roles and accepts
color keys only when their effective configured leaf value is bound through a
CSS custom property (for example, `oklch(var(--brand-500))`). It merges
`theme.colors` with `theme.extend.colors` before granting names, so a literal
override removes an earlier token binding. Fallbacks must also be token-only:
`var(--surface, var(--fallback))` is valid, while `var(--surface, red)` is not.
Keep target-specific nested role names intact: a `surface.raised` binding
authorizes `bg-surface-raised`, while a literal value such as `red` authorizes
nothing. This lets canonical
`text-h1`/`text-body`/`text-caption` and semantic utilities pass without
allowing raw Tailwind palette or CSS named colors.

## shadcn bridge — A-Team extension

*Not upstream content. This section exists because shadcn/ui is the A-Team's
declared-default component library (design-intake `## Declared defaults`);
shadcn themes through semantic role variables, and someone has to bind roles
to scale steps exactly once. The binding is contrast-driven mechanics — every
aesthetic opinion already lives in the scales above.*

Write `docs/product/design-system/shadcn-theme.css`: a `:root` block binding
shadcn's role variables to OKLCH scale steps. Default mapping (light mode):

| Role var | Scale step | Role var | Scale step |
|---|---|---|---|
| `--background` | `neutral-50` | `--muted` | `neutral-100` |
| `--foreground` | `neutral-900` | `--muted-foreground` | `neutral-600` |
| `--card` / `--popover` | `neutral-50` | `--accent` | `accent-100`, else `neutral-100` |
| `--card-foreground` / `--popover-foreground` | `neutral-900` | `--accent-foreground` | `accent-900`, else `neutral-900` |
| `--primary` | `brand-600` | `--destructive` | `error` default |
| `--primary-foreground` | `neutral-50` | `--destructive-foreground` | `neutral-50` |
| `--secondary` | `neutral-100` | `--border` / `--input` | `neutral-200` |
| `--secondary-foreground` | `neutral-900` | `--ring` | `brand-500` |

Rules:

- **Every foreground/background pair must pass the WCAG bar** (default AA
  4.5:1) via `generate-scale.mjs contrast`. A failing pair walks its scale
  step darker/lighter one step at a time, max 2 steps — the same nudge
  discipline as the palette. Still failing → surface it, don't ship it.
- **`--radius` has no source in the subvisual tokens**: write `--radius:
  0.5rem; /* TBD: no radius opinion in the design system */` and record the
  open item in `research-plan.md`.
- **Light mode only**: no `.dark` block. Dark mode is an open item in
  `research-plan.md`, not an invented palette.
- File header comments record the mapping table and the contrast results, so
  the gate reviews the binding, not just the values.

## Common mistakes

- **Hard-coding hex without OKLCH source.** Always store OKLCH primary, hex
  fallback. Editing hex by hand drifts the scale.
- **Forgetting the WCAG nudge.** Generated palettes can fail AA on key
  pairings. Run the check — on the palette *and* on the shadcn bridge pairs.
- **Letting the user pick "any font".** Push for the specimen category. Even
  "system sans-serif" is more useful than "TBD".
- **Generating both passes silently.** Standalone is interactive: ask,
  confirm, then write. Pipeline is derived: every non-obvious call lands in
  `design.md`'s reasoning and the assumptions ledger — derived is not silent.
- **Skipping the brand-seed branch.** Most real projects have at least a
  brand color already. Always check `## Design context` and the target's
  assets before deriving anything.
- **Regenerating instead of consuming.** An existing system is a settled
  fact. Re-running the generator over it is a silent overwrite of a durable
  artifact.

## Red flags — STOP

- Standalone: user says "skip the vibe interview, just pick colors" without
  supplying a seed. Decline; ask for at least domain + mood.
- Pipeline: `## Design context` has no brand/aesthetic data. Do the
  TBD-draft; never invent a seed to keep the run tidy.
- Generated palette fails WCAG after 2 nudges. Surface the failure; don't
  ship low-contrast tokens.
- Custom typography tuple produces ≥2 collision bumps on any level. Warn
  explicitly; offer (standalone) or fall back to (pipeline, flagged) a
  curated preset.
- Existing `docs/product/design-system/` and no explicit regeneration
  instruction. Consume it; report; stop.
