---
name: design-system
description: >
  Turn a chosen design direction into a canonical DESIGN.md plus production tokens that
  don't look vibecoded — state-level colors (8-step neutral ramp, rest/hover/active/
  disabled, focus ring), APCA-checked contrast, typography, spacing/radius/motion/elevation,
  an icon strategy, and component contracts for the core atoms. Emits tokens in the project's
  stack format (shadcn HSL vars or Tailwind v4 @theme). Load when the user asks to build a
  design system, generate design tokens, create a DESIGN.md, set up a theme, design a color
  or type system, pick icons, or when frontend-design routes here. Replaces design-tokens-craft
  and icon-craft. Sub-skill of frontend-design. Reads DIRECTION.md first.
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: project-specific
  sources: Google design-md, W3C DTCG tokens, APCA, design-tokens-craft + icon-craft (merged)
  resources:
    references:
      - design-md-template.md
      - state-tokens.md
      - token-recipes.md
      - typography-pairings.md
      - banned-palettes.md
      - icon-strategies.md
      - svg-craft.md
      - examples.md
---

# Design System

You are the Design Systems Engineer. You take a chosen direction and produce ONE canonical
`DESIGN.md` (the source of truth) plus real token files. Your tokens go "all the way down"
so the model never fills seams from the corpus mean — that is what kills generic output.

## Hard Rules

- **Read `DIRECTION.md` first.** Never generate a system without a chosen direction. If none exists, route back to `design-direction`.
- **One canonical DESIGN.md.** Emit a single `DESIGN.md` (per `references/design-md-template.md`) + `tokens.css`. Do NOT scatter ARCHETYPE/TOKENS/ICONS files.
- **Tokens all the way down.** Every interactive variant ships rest/hover/active/disabled + text-on-accent + focus ring; 8-step oklch neutral ramp; dark mode hand-set, never inverted. See `references/state-tokens.md`.
- **APCA, not WCAG ratio.** Every text/bg and text-on-accent pair meets the APCA targets (body Lc≥75, large ≥45, non-text ≥30).
- **Semantic + component tokens, never literals.** Components consume `--surface-1`/`--button-bg`, never raw hex or `slate-500`.
- **One icon family.** Pick ONE strategy; stroke matches type weight. No mixed libraries, no Lucide default drop-in.
- **Banned defaults stay banned.** Run `references/banned-palettes.md`; re-derive anything that smells default.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Accent + a few greys is enough" | The slop lives in the unstated 95% — define every state or the model guesses the mean. |
| "Invert light mode for dark" | Inverted lightness reads cheap. Dark is a separate hand-set story. |
| "WCAG 4.5:1 is fine" | WCAG misreads dark themes and thin type. Use APCA Lc targets. |
| "Skip DESIGN.md, just write CSS" | DESIGN.md is the contract every later step reads; without it each screen re-negotiates and drifts. |
| "Lucide is fine if the colors are good" | Default Lucide is the #2 slop tell after Inter. Tune or go custom. |

---

## Workflow

### Step 1 — Read inputs
Read `.design/<feature>/DIRECTION.md`: direction name, feels-like, posture, type pair, color story, motion, density, icon stance. Note the stack + token format passed by `frontend-design`.

### Step 2 — Seed from the recipe
Read `references/token-recipes.md` and `references/typography-pairings.md` for the direction's starting palette + type pairing. Weave in the user's brand color into the accent slot (kept in the direction's hue range).

### Step 3 — Build color tokens (state-level)
Per `references/state-tokens.md`: 8-step oklch neutral ramp; semantic surfaces/text/border; accent rest/hover/active/disabled + text-on-accent; focus-ring color/opacity/width; status colors. Light + hand-set dark. No opacity-only hover.

### Step 4 — Typography, spatial, motion, elevation
Type scale + weights + tracking + reading column; log-spaced spacing; one radius scale (chip<card<modal); 0-3 elevation (borderless-card default); 3-4 motion durations + real curves + reduced-motion.

### Step 5 — APCA pass
Check every text/bg and text-on-accent pair against APCA targets. Fix failures (shift L or add overlay) before emitting.

### Step 6 — Icon strategy
Read `references/icon-strategies.md` (and `svg-craft.md` if custom). Pick ONE strategy, weight matched to type. Record it; defer drawing/sourcing to the build. For **animated** SVG (loaders, morphs, path-draw) outside token contracts, invoke `svg-creation` instead of improvising in the build step.

### Step 7 — Component contracts
For the core atoms (button, input, card, nav, modal, table row): variants, tokens consumed, composition rule / use-when, and the full state set. This is the agent-readable contract.

### Step 8 — Emit
Write `DESIGN.md` (per template) + `tokens.css` (shadcn HSL channels if shadcn, else `oklch` under `:root`/`[data-theme="dark"]` or Tailwind v4 `@theme`) + optional `tokens.ts`. Run the Step-9 self-audit.

### Step 9 — Self-audit
Run the checklist in `references/state-tokens.md` and `references/banned-palettes.md`. Re-emit any section that leaks a default.

---

## Output Format (DESIGN.md)
Use `references/design-md-template.md` verbatim — sections: Theme, Color (semantic light+dark + ramp + APCA), Typography, Spacing/Radius/Elevation/Motion, Icons, Components (contracts), Nevers, Files. Keep under ~120 lines; depth lives in references.

---

## Verification
- [ ] `DESIGN.md` + `tokens.css` emitted; no scattered ARCHETYPE/TOKENS/ICONS files
- [ ] 8-step oklch ramp; dark hand-set; rest/hover/active/disabled + text-on-accent + focus ring for every interactive variant
- [ ] Every text/bg + text-on-accent pair passes APCA (body Lc≥75, large ≥45, non-text ≥30)
- [ ] One icon strategy, stroke matched to type weight
- [ ] Component contracts present for button/input/card/nav/modal/table row
- [ ] `banned-palettes.md` audit clean (no slate/zinc default ramp, no purple→pink, no Inter-only, no inverted dark)

---

## Red Flags

- DESIGN.md generated without reading DIRECTION.md first
- Multiple competing token sources instead of one canonical file
- Interactive states missing hover/active/disabled variants
- Icons or fonts shipped without license or attribution check
## Reference Files
- `references/design-md-template.md` — canonical DESIGN.md structure (copy verbatim)
- `references/state-tokens.md` — tokens-all-the-way-down: ramp, states, focus ring, APCA, tiers
- `references/token-recipes.md` — per-direction starting palettes (seed in Step 2)
- `references/typography-pairings.md` — vetted display/body pairings (paid + free)
- `references/banned-palettes.md` — vibecoded color/type/spacing/motion tells to refuse
- `references/icon-strategies.md` — the 5 strategies + per-direction defaults
- `references/svg-craft.md` — drawing rules for custom SVG sets (grid, stroke, optical sizing)

---

## File Output
Append to `docs/skill-outputs/SKILL-OUTPUTS.md`:
```
| YYYY-MM-DD HH:MM | design-system | DESIGN.md + src/styles/tokens.css | [direction] tokens + icon strategy |
```

---

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report
```
Design system built: [feature]
Direction: [name]
Token format: [shadcn HSL / oklch / @theme]
Color slots (with states): [count] | Neutral ramp: 8-step
APCA: [all pass / fixes applied]
Icon strategy: [name] | Component contracts: [count]
Files: DESIGN.md, src/styles/tokens.css[, tokens.ts]
Handoff to: frontend-design (build)
```
