---
model_tier: inherit
name: iconography
description: "Resolve an icon request to a concrete Iconify name and emit the embedding for the project's stack. Use when adding icons, picking an icon set, or wiring Lucide/Heroicons/Phosphor/Tabler."
domain: product
personas: []
workspaces:
  - engineering
packs:
  - frontend-design
trust:
  level: professional
install:
  removable: true
scope:
  write: []
  verification_reason: "execution declares no handler, so this skill runs nothing of its own — every write is the calling agent's, under the rules that govern it. No command can prove a scope the skill never executes."
execution:
  type: manual
---

# iconography

> Resolve an icon request to a verified Iconify name (`set:name`) and emit the
> correct embedding for the project's stack — CSS class, inline SVG, or
> framework component — while keeping icon-set usage consistent across the UI.

## When to use

- Adding any icon to a component or page.
- Picking an icon set for a new project or feature area.
- Wiring Lucide, Heroicons, Phosphor, or Tabler into a stack (React, Blade, Tailwind).
- Auditing inconsistent icon usage across a UI surface.

## Procedure

1. **Identify the icon need** — what does the icon communicate? Name the semantic
   intent (e.g., "download action", "warning state", "user profile") rather than
   visual description alone.
2. **Choose the icon set — three rungs, and record which one answered.** The
   set is *chosen*, never inherited: adopting one because a scaffold shipped it
   is the anti-pattern [`icon-consistency`](../../rules/icon-consistency.md)
   § What this gates names by name. Stop at the first rung that answers.
   1. **A brand token or brand guide that names an icon set** — authoritative,
      stop here (`brand-source-of-truth`).
   2. **The set already in use in this project** — detected at the Inspect step
      of the Iconography floor below. One icon system per project; a second
      visual language is the defect, not a preference.
   3. **Neither exists → select from the open candidates by the criterion the
      surface actually imposes, and state which criterion decided it.** The
      candidates, unordered: **Heroicons**, **Lucide**, **Phosphor**, **Tabler**.

   | Criterion the surface imposes | Candidates that satisfy it |
   |---|---|
   | Several stroke weights inside one UI (thin captions, bold empty states) | Phosphor (six weights) |
   | One uniform stroke across a dense admin UI | Lucide, Tabler |
   | First-party match to a component library the project already adopted | Heroicons (Tailwind UI), Lucide (shadcn/ui) |
   | Widest glyph coverage for domain-specific nouns | Tabler, Phosphor |

   Two criteria pointing at different candidates is a real trade-off — name it
   and pick one; do not split the UI across both. Brand and provider marks are
   a separate axis and use **lobe-icons** (`lobe-icons:openai-color`) whatever
   the UI set is.
3. **Resolve to a concrete Iconify name** in `set:name` format, e.g.
   `lucide:arrow-right`, `heroicons:user-solid`, `ph:warning-bold`,
   `tabler:download`. Verify the name exists on
   [iconify.design](https://iconify.design) before emitting.
4. **Emit the embedding** matched to the stack:
   - **CSS class (web-font path)** — `<span class="iconify" data-icon="lucide:arrow-right"></span>` plus the Iconify CDN or build-time bundle.
   - **Inline SVG** — fetch the SVG from the Iconify API (`https://api.iconify.design/{set}/{name}.svg`) and embed directly.
   - **Framework component** — `<Icon icon="lucide:arrow-right" />` via `@iconify/react`, `@iconify/vue`, or the stack's Iconify wrapper.
5. **Verify** — check the resolved name on `iconify.design/icon/{set}:{name}`;
   confirm the icon renders as expected before shipping.

## Which set each stack ships with — an observation, not a pick

Recorded so rung 2 above can recognise an incumbent. Finding one of these in a
project is rung-2 evidence. Reaching for it because the stack is *new* skips
rung 3 and is exactly the scaffold inheritance
[`icon-consistency`](../../rules/icon-consistency.md) forbids.

| Stack / consumer | Ships with |
|---|---|
| `react-shadcn-ui` | Lucide |
| `blade-ui` | Heroicons (Tailwind first-party) |
| `tailwind-engineer` | none of its own — any web-font-friendly set |

## Iconography floor (design fidelity)

Before resolving any new icon, honour the project's existing icon system — the
Inspect stage of the
[design-artifact lifecycle](../../../docs/contracts/design-artifact-lifecycle.md).

- **Inspect first.** Detect the icon set already in use (imports, existing
  `set:name` usages, brand assets) before picking one. A new icon matches the
  incumbent set's **stroke weight, fill style, corner radius, size, and
  metaphor** — do not introduce a second visual language (see
  [`icon-consistency`](../../rules/icon-consistency.md)).
- **No emoji-as-icon in serious UI.** An emoji is not an icon — never substitute
  `⚙️`/`🔔`/`✅` for a real icon in a product/admin/marketing surface (functional
  CLI/status markers are a different context, out of scope here).
- **No hand-rolled icons when a set exists.** If the project has an icon library
  or brand mark, use it — do not hand-author a one-off SVG that drifts from the
  system. Hand-rolling is for a genuinely missing glyph, and then it matches the
  set's grid + stroke.
- **Flag substitutions when the exact asset is absent.** When the needed icon or
  brand mark does not exist in the set, pick the nearest and **state the
  substitution** ("no exact 'sync' glyph in Heroicons; used `arrow-path`") rather
  than silently approximating or inventing. (fixtures: `daf-emoji-as-icon`,
  `daf-fake-svg-logo`.)

## Output format

1. **Iconify name** — `set:name` string, e.g. `lucide:arrow-right`.
2. **Embedding snippet** — the ready-to-paste code for the project's stack
   (CSS class, inline SVG, or component import + usage).
3. **Set/consistency note** — which set was chosen, why, and whether it matches
   the icons already in use in this codebase.

## Gotcha

- **Mixing icon sets in one UI looks inconsistent.** Lucide and Heroicons have
  different stroke weights and visual rhythm; mixing them without a deliberate
  brand reason produces a jarring result. Audit the existing set before
  introducing a second one.
- **Nonexistent Iconify names 404 silently.** A name like `lucide:arrowRight`
  (camelCase) or `heroicons:user` (missing `-solid`/`-outline` suffix) resolves
  to nothing at render time — the slot is empty with no error. Always verify on
  `iconify.design` before committing the snippet.

## Do NOT

- Do NOT mix multiple icon sets in the same UI surface without an explicit brand
  reason and a note in the set/consistency output.
- Do NOT inline hundreds of raw SVGs when a CSS-class web-font set is available —
  the bundle cost is orders of magnitude higher than a single Iconify CDN include.
- Do NOT invent Iconify names — every name must be verified to exist in the
  Iconify registry; a plausible-sounding name that doesn't exist renders as
  nothing.

## See also

- [`design-canon.md`](../../../docs/guidelines/design-canon.md) § Icon systems — prefer a named system's icon set (Material Symbols / SF Symbols / Fluent / Carbon) when that system is in play.
- [`design-tokens`](../design-tokens/SKILL.md) — token system the icon color/size variables should reference.
- [`typography-system`](../typography-system/SKILL.md) — sibling visual-consistency skill.
- [`fe-design`](../fe-design/SKILL.md) — broader frontend design discipline.
- [`icon-consistency`](../../rules/icon-consistency.md) — enforced rule for set discipline across the project.
- [`docs/guidelines/design-antipatterns.md`](../../../docs/guidelines/design-antipatterns.md) — icon-relevant slop tells: V5 (hand-drawn SVG mixed with crisp icon-system icons) and T3 (small rounded-square icon tile above every feature heading — the universal AI feature-card template).
