---
name: slop-radar
description: Use when the user asks to audit, critique, or detect AI slop, vibe-coded sameness, generic template aesthetics, or unmotivated frontend design choices in a screenshot, live URL, route, component, or source tree.
---

# AI Slop Design Audit

Audit whether a frontend feels authored for its product or assembled from common AI defaults.

**The brief overrides the baseline. Every tell is a heuristic, never a conviction by itself. Judge clusters and intent, not isolated stylistic choices.**

This skill audits and reports. Do not edit the frontend unless the user separately asks for implementation.

## Vocabulary

- **Tell**: one observable convention associated with generic AI-generated frontends.
- **Cluster**: multiple tells in one region, or the same tell repeated across the experience.
- **Defaultness**: how interchangeable and unexplained the design choices feel.
- **Fitness**: how well the choices serve the product, audience, brand, and task.
- **Finding**: an evidence-backed problem worth acting on, not a personal taste preference.

Do not claim that AI produced a frontend. `slop-like` describes the observable result, not its provenance.

## Pin the audit

Before judging, state what evidence is available:

| Input | Evidence you may claim |
|---|---|
| Screenshot or mockup | Visible composition, typography, color, copy, hierarchy, and apparent state only |
| Live URL | Visible design plus responsive behavior, focus, hover, motion, interaction, and browser-observable accessibility |
| Route or repository | Render it when safely runnable, then combine visual and source evidence |
| Source only | Implementation patterns only; do not claim the final rendered appearance |

Record the target, inspected viewports or files, and missing evidence. If a brief, design system, brand guide, or audience description exists, treat it as the governing standard.

## Audit workflow

1. **Read intent.** Identify the product, audience, primary task, desired tone, and supplied design constraints. If these are unknown, mark Fitness as `unknown` where necessary instead of inventing intent.
2. **Inspect the rendered experience first.** Record the initial hierarchy, specificity, coherence, and repeated visual language before source details anchor the judgment.
3. **Inspect source when available.** Corroborate visible patterns through shared tokens, components, typography imports, icon usage, copy, and motion primitives. Cite exact `file:line` locations.
4. **Judge the two axes independently.** A familiar convention may fit the product; an unusual design may still fit poorly.
5. **Report and stop.** Prioritize no more than five actionable findings. Do not manufacture findings to fill the quota.

## Two axes

### Defaultness

- `low`: sparse or clearly motivated tells; the experience has product-specific authorship.
- `medium`: one meaningful cluster or repeated defaults dilute otherwise specific work.
- `high`: multiple clusters dominate layout, typography, copy, materials, icons, or motion.

### Fitness

- `strong`: choices clearly support the brief, audience, and primary task.
- `mixed`: important choices help while others weaken clarity, trust, or distinctiveness.
- `weak`: the visual language conflicts with the product, audience, task, or accessibility needs.
- `unknown`: evidence does not establish the intended product context.

Derive the overall verdict without arithmetic:

- `authored`: coherent, specific choices; tells are sparse or justified.
- `defaulted`: noticeable clustered defaults, but meaningful product-specific authorship remains.
- `slop-like`: repeated clusters overwhelm product rationale and make the experience feel interchangeable.

## Tell catalog

Use this as a detection baseline, not a ban list.

| Area | Common tells |
|---|---|
| Color and material | Purple-to-blue gradients; gradient hero text; colored-border cards; glassmorphism cards; grain layered over gradients |
| Typography and copy | Inter everywhere; emojis in headings; generic buzzword copy; serif italic accents; Space Grotesk paired with Instrument Serif; em dashes everywhere |
| Composition | Three icon boxes in a row; a badge or eyebrow above the heading; untouched shadcn UI; inconsistent spacing |
| Icons and motion | Lucide icons everywhere; fade-in on scroll; cursor-following beams; buttons that merely fade on hover |
| Theme quality | Low-contrast dark mode |

Also notice the larger pattern behind the catalog: repeated choices that cannot be explained by the product, audience, brand, information hierarchy, or interaction need.

### Decorative numbering and template eyebrows

- **Zero-padded index prefixes** such as `01 / RING`, `02 / HANDLE`, or `PHASE 01`: flag numbers and slash separators that dress ordinary content up as a technical process without helping readers navigate or understand order. Inspect the whole small, uppercase, widely tracked eyebrow too; removing only `01 /` can leave an equally redundant label above a heading that already says the same thing.
- **Oversized ghost numerals** pinned in a card corner: flag large, faint `01` / `02` decorations, especially when the same number appears in the eyebrow. They compete with the useful heading, reserve space, and make unrelated content look like a template.
- **The cluster matters**: numbered mono eyebrow + repeated corner numeral + generic bordered card is a strong defaultness signal when repeated across processes, features, and article lists without a content reason. Do not replace it reflexively with generic icons, pills, dots, or another decorative marker.
- **Correction**: let the useful heading lead; use typography, spacing, and content relationships to create hierarchy. Preserve genuine metadata (category, date, duration) and communicate necessary sequence through a semantic ordered list or a clear connected flow. A real day label (`Day 1`, `Day 5`), rank, reference number, or usable step navigator can be justified; do not erase information to pass the heuristic.

Calibration example: in a call-flow page showing `01 / RING` plus a ghost `01` in the card corner, the left green box marks `01 / RING` (primarily the `01 /` prefix, secondarily the redundant eyebrow treatment); the right box marks the duplicate oversized `01`. The green annotations identify audit targets, not desired UI styling.

### Repeated decorative hexagon icons

- **Empty hexagon bullets** repeated beside unrelated feature, AI, security, or compliance claims: flag identical geometric icons that do not distinguish the items or communicate state. Repetition beside bordered rows can create a generic technical aesthetic without useful meaning.
- **Correction**: remove the redundant icon and let clear text, spacing, and alignment organize the list. Do not substitute another stock icon, shield, sparkle, dot, or badge by default.
- **Exception**: a deliberate brand mark (e.g. a logo built on a hexagon) or a meaningful diagram node can be justified. This is a critique of decorative repetition, not a ban on hexagons or evidence of AI authorship.

Calibration example: the four identical outline hexagons in a compliance-claims list under a "Designed for X workloads" heading add no distinction between encryption, data minimization, audit trail, and contract statements. This treatment was rejected in review.

## Finding threshold

- One tell alone is weak evidence.
- A cluster, repetition, or system-level default is stronger evidence.
- A documented design system or explicit brief can justify a familiar convention.
- Accessibility and usability failures are valid Fitness findings, but they are not evidence of AI authorship.
- When a problem repeats, recommend the smallest shared correction, such as a token or shared component, instead of scattered cosmetic edits.

Each finding must contain:

1. **Location**: exact screen region, component, or `file:line`.
2. **Evidence**: the observed tell or cluster.
3. **Why it matters**: the product, clarity, trust, distinctiveness, or usability consequence.
4. **Confidence**: `high`, `medium`, or `low`, with uncertainty stated plainly.
5. **Smallest correction**: a concrete change that preserves working structure and intentional choices.

## Report contract

Return this shape:

```markdown
# Slop Radar Audit

**Target:** <URL, screen, route, or source scope>
**Evidence:** <what was actually inspected>
**Limitations:** <missing context or evidence, or "None">

**Verdict:** authored | defaulted | slop-like
**Defaultness:** low | medium | high
**Fitness:** strong | mixed | weak | unknown

## Findings

1. **<finding title>**
   - Location: <region or file:line>
   - Evidence: <tell or cluster>
   - Why it matters: <consequence>
   - Confidence: high | medium | low
   - Smallest correction: <specific change>

## Keep

- <up to three strengths or intentional choices to preserve>

## Top recommendation

<the single highest-leverage correction and why it comes first>
```

If no meaningful cluster exists, say so. A clean audit is a valid result.
