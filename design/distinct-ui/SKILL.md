---
name: distinct-ui
description: "Builds distinctive, production-grade UI by committing to one of 12 named visual directions (editorial, brutalist, luxury-minimal, terminal/dev-native, playful-geometric, glassmorphic, retro-futurist, swiss-grid, organic-soft, data-dense, art-deco-revival, neo-memphis)."
version: "2.0.1"
category: ux
platforms:
  - CLAUDE_CODE
---

You are an autonomous UI designer-implementer. Do NOT ask the user questions. Read the context, pick a direction, commit to it, build it, and verify it against measurable gates. If a decision is ambiguous, make the strongest defensible call and record it in the output.

TARGET: $ARGUMENTS

- With arguments: treat them as the scope (a screen, component, page path, or an explicitly requested style from the taxonomy below). An explicitly named style overrides Phase 2 selection.
- Without arguments: apply to the primary user-facing surface of the current repo (landing page, main screen, or the app shell).

=== PRE-FLIGHT ===

1. Confirm a UI codebase exists: look for package.json, pubspec.yaml, index.html, or src/ with components. If none, you are creating a standalone page; note this and continue with vanilla HTML/CSS.
2. Detect the stack: React/Next/Vue/Svelte (package.json deps), Flutter (pubspec.yaml), Tailwind (tailwind.config.*), plain CSS. Recovery: if detection is ambiguous, grep for `className=`, `styled`, `@apply`, `ThemeData` and pick the dominant pattern.
3. Locate existing design assets: design tokens (tokens._, theme._, tailwind.config.*, ThemeData), a CLAUDE.md design section, brand assets (logo files, brand colors in CSS vars). Recovery: if none exist, you will define tokens in Phase 3 rather than reuse.
4. Confirm you can render or at least build the target (dev server script, `flutter analyze`, or open the HTML file). Recovery: if no runnable check exists, rely on static verification in Phase 5 and state that limitation in the output.

Fail fast with a one-line message only if the target path in $ARGUMENTS does not exist.

=== PHASE 1: CONTEXT READ ===

1. Read CLAUDE.md (project and any design section), README, and existing token/theme files.
2. Identify the product's job and audience: developer tool, consumer app, luxury/premium, data product, creative/portfolio, B2B SaaS. Infer from copy, routes, and dependencies; do not guess blindly.
3. Inventory what already exists: fonts loaded, color variables, spacing values, component library (shadcn, MUI, Material). List the 5 most-reused components.
4. Note hard constraints: existing brand colors are immovable; component library primitives should be restyled, not replaced.

VALIDATION: You can state in one sentence who the user is and what feeling the UI should produce.
FALLBACK: If the product context is genuinely unreadable (empty repo), default persona is "technical early adopter" and proceed.

=== PHASE 2: PICK AND COMMIT TO A DIRECTION ===

1. Choose exactly ONE style from this taxonomy. Each entry is name: core moves / typical type / signature risk to avoid.
   1. editorial: strong headlines, generous measure, rules and bylines / serif display + humanist sans / avoid: newspaper cosplay
   2. brutalist: raw borders, system colors, exposed structure / mono or grotesque, huge / avoid: illegibility
   3. luxury-minimal: vast whitespace, hairline rules, muted palette / high-contrast serif, wide tracking on labels / avoid: emptiness without hierarchy
   4. terminal/dev-native: mono type, dense chrome, keyboard affordances / monospace everywhere / avoid: green-on-black cliche
   5. playful-geometric: bold shapes, saturated accents, rounded geometry / geometric sans / avoid: children's-app look
   6. glassmorphic: layered translucency, depth, glow / clean sans / avoid: more than 2 frosted surfaces
   7. retro-futurist: chrome gradients, grid horizons, phosphor accents / display + mono pairing / avoid: vaporwave parody
   8. swiss-grid: strict columns, flush-left, functional color / Helvetica-class grotesque / avoid: sterility
   9. organic-soft: curves, warm neutrals, soft shadows / rounded sans / avoid: mush with no edges
   10. data-dense: tight rhythm, tabular numerals, inline viz / compact sans + mono numerals / avoid: crowding below 4px gaps
   11. art-deco-revival: symmetry, gold/ink palette, stepped ornament / high-contrast geometric display / avoid: Gatsby template
   12. neo-memphis: clashing brights, patterns, hard shadows / chunky grotesque / avoid: randomness without a grid
2. Selection rule: match direction to Phase 1 audience (dev tool -> terminal/dev-native or swiss-grid; premium consumer -> luxury-minimal or editorial; data product -> data-dense; creative -> neo-memphis, retro-futurist, or brutalist). If existing brand tokens strongly imply a direction, follow them.
3. Write a 3-line design brief: chosen style, the one signature flourish (see Phase 3), and the two styles you rejected and why. This goes in the output verbatim.

VALIDATION: Exactly one style chosen; brief written; the flourish is nameable in five words.
FALLBACK: If two styles tie, pick the one farther from the anti-slop defaults in Phase 4 (e.g. prefer editorial over glassmorphic).

=== PHASE 3: IMPLEMENT ===

1. Typography scale: define a real modular scale (e.g. 1.25 ratio: 12/14/16/20/25/31/39/49) as tokens. Load at most 2 font families with specific weights. Never leave the browser default stack unless the style demands system fonts.
2. Spacing system: 4px or 8px base grid as tokens (space-1 .. space-12). Replace magic-number padding in every file you touch.
3. Color: build the palette from the style, not from defaults. Define semantic tokens (surface, surface-raised, ink, ink-muted, accent, danger) in BOTH light and dark values. Wire dark mode via prefers-color-scheme or the framework's theme mechanism.
4. Signature flourish: implement exactly one memorable element that only this style would produce, e.g. an oversized numbered section index (editorial), a scanline hover state (retro-futurist), a hairline gold divider system (art-deco-revival). One, not five.
5. States: every interactive element gets hover, focus-visible, active, and disabled styles consistent with the direction.
6. Apply to the full target scope; do not restyle one component and leave siblings generic.

VALIDATION: Tokens exist and are referenced (grep shows zero new hardcoded hex values in touched files); both themes render; flourish is present.
FALLBACK: If the component library blocks a token (hardcoded internals), use its theming API; if none, scope an override stylesheet and note it.

=== PHASE 4: ANTI-SLOP GATE ===

Check every item; each failure must be fixed before proceeding:

1. No purple/violet gradient on a white hero, and no purple-to-pink gradient text.
2. No emoji used as icons; use inline SVG or the project's icon set.
3. No lorem ipsum or placeholder copy; write real copy matched to the product.
4. No three-card feature grid with icon-title-blurb; if features must be listed, use the style's own layout (editorial list, dense table, asymmetric grid).
5. No floating blob/orb background decorations; no glassmorphism outside style 6.
6. Not Inter/Roboto-only typography (unless swiss-grid deliberately chose a grotesque, stated in the brief).
7. Dark AND light mode both complete, not one inverted from the other.
8. At least one layout decision is asymmetric or unexpected (not everything centered in a 1200px column).

VALIDATION: 8/8 pass, or each failure has a written justification tied to the brief.
FALLBACK: None. This gate is mandatory; fix and re-check.

=== PHASE 5: MEASURABLE VERIFICATION ===

1. Contrast: compute the contrast ratio for every text/background token pair in both themes (WCAG formula; use a quick node/python one-liner if needed). Require >= 4.5:1 for body text, >= 3:1 for large text and UI borders.
2. Touch targets: every button, link-as-button, and input is >= 48x48 px (or 48dp Flutter) including padding; verify in the code, cite file:line for anything you had to fix.
3. Render check: run the dev server or build; screenshot with Playwright if available; confirm no layout overflow at 320px width.
4. Keyboard: tab through the primary flow; focus-visible ring must be visible against both themes.

VALIDATION: All contrast pairs pass; zero sub-48px targets remain; build/render succeeds.
FALLBACK: If a brand-mandated color fails contrast, adjust lightness of the paired surface, never silently ship a failing pair; document the adjustment.

OUTPUT
Deliver, in this order:

1. Design brief (from Phase 2, verbatim): style, flourish, rejected alternatives.
2. Files changed list with one-line purpose each.
3. Token summary: type scale, spacing scale, semantic colors (light/dark values).
4. Anti-slop gate result: 8 checks with pass/fixed status.
5. Verification table: contrast pairs with computed ratios, touch-target fixes (file:line), render/build status.
6. Run instructions to view the result.

=== SELF-REVIEW ===
Score Complete, Robust, Clean 1-5. Complete: whole scope styled, both themes, all states. Robust: verification actually executed, not asserted. Clean: tokens only, no dead CSS introduced. If any score < 4, fix it now if possible in-run; otherwise state the gap explicitly as a known limitation in the output.

=== LEARNINGS CAPTURE ===
Append to ~/.claude/skills/distinct-ui/LEARNINGS.md (create if missing):

- Date + repo + chosen style and why
- What worked, what was awkward (e.g. taxonomy gap, library fought the tokens)
- Suggested patch to this skill
- Verdict: [Smooth/Minor friction/Major friction]

STRICT RULES

1. NEVER present more than one style direction in the implementation; commit fully.
2. NEVER ship lorem ipsum, emoji icons, or a default purple-gradient hero.
3. NEVER hardcode a color in a component you touched; tokens only.
4. ALWAYS implement dark and light mode together, never one "for later".
5. ALWAYS compute contrast ratios; never eyeball them.
6. NEVER skip the anti-slop gate, even for "quick" changes.
7. ALWAYS name the signature flourish in the output; if you cannot name it, you did not build one.
8. NEVER replace an existing brand color; restyle around it.
