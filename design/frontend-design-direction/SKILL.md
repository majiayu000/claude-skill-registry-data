---
name: frontend-design-direction
description: Set an ECC-specific frontend design direction — Purpose / Audience / Tone / Memorable-detail / Constraints — BEFORE any UI code is written. Use when a website, dashboard, app, component, or landing page needs a decided direction, or when existing UI reads flat, generic, or mismatched to its audience. Do NOT use for implementation once the direction is settled (that is `frontend-design`), for token-system generation or drift audits (`design-system`), or for SkyyRose brand-canon calls (`luxury-design-taste` — the direction there is already locked by `.impeccable.md`).
origin: community
---

# Frontend Design Direction

Use this skill when the work is not just making UI function, but making it feel
purposeful, polished, and appropriate to the product domain.

Source: salvaged from stale community PR #1659 by `linus707`.

Note: ECC intentionally does not rebundle the canonical Anthropic
`frontend-design` skill. Install that from `anthropics/skills` when you want the
official upstream skill. This skill is the ECC-specific design-direction salvage
of the useful local guidance from #1659.

## When to Use

- The user asks to build a web page, app, dashboard, artifact, component, or UI.
- The user asks to make an interface more polished, distinctive, beautiful, or
  less generic.
- The implementation needs visual hierarchy, typography, color, motion, layout,
  and interaction choices.
- The current UI works but reads as flat, generic, templated, or mismatched to
  the audience.

**When NOT to use:** the direction is already decided and you are writing code — that is
`frontend-design`. A token system needs generating or auditing for drift — that is
`design-system`. The surface is skyyrose.co, where the direction is already locked in
`.impeccable.md` and `docs/brand/visual-references.md` — read those and use
`luxury-design-taste`; re-deriving a direction there is a canon violation, not a service.
Native iOS — `liquid-glass-design`.

## Inputs

A direction is a decision about a product and its users. **You cannot infer it from code — code
tells you what was built, not who it is for.** Each missing input is a stop.

| Input | Where | If absent |
|---|---|---|
| Stated purpose + audience | the user, or a written design-context file (`.impeccable.md`, `docs/brand/*`, PRD) | **Stop and ask.** Do not infer audience from the codebase — that is the failure this skill exists to prevent |
| Existing direction, if any | `.impeccable.md`, `CLAUDE.md`, `BRAND.md`, `STYLEGUIDE.md` | Run Verification #1. A hit means the direction exists: adopt it, do not replace it |
| Existing tokens + component vocabulary | `tailwind.config.*`, `theme.json`, `tokens.css`, `components/` | Run Verification #2. The direction must be expressible in what already exists, or you must say what you are adding and why |
| Anti-references ("must not look like…") | the user | Ask. Without them, "distinctive" collapses to your training default |

## Design Direction

Before coding, choose a specific direction:

1. Purpose: what job does the interface do?
2. Audience: who repeats this workflow, and what do they need to scan first?
3. Tone: utilitarian, editorial, playful, industrial, refined, technical,
   maximal, minimal, dense, calm, or another explicit direction.
4. Memorable detail: one design idea that makes the result feel intentional.
5. Constraints: framework, accessibility, performance, responsiveness, and
   existing design system.

Match the direction to the domain. A SaaS operations tool should usually be
dense, quiet, and scannable. A portfolio, launch page, game, or editorial piece
can be more expressive. Do not force a landing-page composition onto a tool that
needs repeated daily use.

## Implementation Guidance

- Build the actual usable experience as the first screen unless the user
  explicitly asks for marketing copy.
- Use existing project components, tokens, icon libraries, and routing patterns
  before introducing a new visual system.
- Use real or generated visual assets when the interface depends on images,
  products, places, people, gameplay, charts, or inspectable media.
- Prefer contextual typography and spacing over generic oversized hero text.
- Keep palettes multi-dimensional: avoid a UI dominated by one hue family.
- Use CSS variables or existing design tokens so the direction remains
  coherent across states.
- Design responsive constraints explicitly: grids, aspect ratios, min/max
  sizes, stable toolbars, and fixed-format controls should not shift when labels
  or hover states appear.
- Use motion sparingly but deliberately. Prefer high-signal transitions that
  clarify state over decorative animation.
- Verify text fit on mobile and desktop. Long labels must wrap or resize
  cleanly rather than overflowing.

## Anti-Patterns

- Do not default to common generated patterns: purple gradients, decorative
  blobs, oversized cards, vague hero copy, or stock-like atmospheric media.
- Do not add UI cards inside other cards.
- Do not use a single decorative style everywhere when the domain calls for
  restraint.
- Do not hide the primary product, tool, object, or workflow behind generic
  marketing sections.
- Do not add a new dependency for a design flourish unless it clearly pays for
  itself.
- Do not describe the UI's features inside the UI when the controls can speak
  for themselves.

## Review Checklist

- The first viewport immediately communicates the product, workflow, or object.
- The visual hierarchy supports scanning and repeated use.
- Typography fits the container and does not overlap adjacent content.
- Color choices have contrast and do not collapse into a one-note palette.
- Icons are used for familiar tool actions where available.
- Responsive layout has stable dimensions for boards, grids, toolbars,
  controls, tiles, and counters.
- Assets render and carry the subject matter instead of acting as filler.
- Motion improves orientation and does not mask sluggishness.
- The result matches the repo's existing frontend conventions unless there is a
  clear reason to depart.

## Procedure

1. Run Verification #1. If a design-context file exists, **read it and adopt its direction** — this
   skill's job then becomes applying it, not re-deriving it.
2. If none exists, ask the user for Purpose, Audience, Tone, Memorable detail, and anti-references.
   Do not substitute inference from the codebase.
3. Run Verification #2 to inventory the tokens and components the direction must live inside.
4. Write the direction down as five one-line answers (Purpose / Audience / Tone / Memorable detail /
   Constraints). Unwritten, it will not survive the first implementation decision.
5. Name the default you would have reached for, and reject it unless the project already uses it.
   State the alternative and its one-line justification.
6. Persist the direction to the project's design-context file so the next session inherits it rather
   than re-deriving a different one.
7. Hand off to `frontend-design` for implementation, then confirm with Verification #3 and #4.

## Verification

Direction is a judgment; these checks bind the parts of it that are falsifiable — whether a
direction already exists, whether it is expressible in the existing system, and whether the
implementation that followed it holds up.

1. **Does a direction already exist?** (Re-deriving over an existing one is the top failure mode.)

```bash
ls .impeccable.md CLAUDE.md BRAND.md STYLEGUIDE.md docs/brand/visual-references.md 2>/dev/null
```

   **PASS:** either nothing is listed (genuinely undecided → gather it), or something is listed and
   you have read it and are extending it. A listed file you did not read is a FAIL. `[repo]`

2. **Is the direction expressible in the existing system?**

```bash
grep -nE "colors|fontFamily|#[0-9a-fA-F]{6}" frontend/tailwind.config.ts | head -6
```

   **PASS:** every color and family the direction calls for is present, or each addition is written
   down with a justification. `[repo]`

3. **Anti-pattern grep** — the Anti-Patterns section above has literal CSS signatures:

```bash
grep -rnE 'background-clip:\s*text|linear-gradient\([^)]*(purple|#8b5cf6|#a855f7)' \
  frontend/app/globals.css wordpress-theme/skyyrose-flagship/assets/css/*.css 2>/dev/null \
  | grep -v '.min.css' | head
```

   **PASS:** zero hits. Any hit is the "purple gradient / gradient text" default this skill exists
   to reject. `[repo]`

4. **Text-fit and responsive claims must be rendered, not asserted.** The Review Checklist items
   about wrapping, overflow, and stable dimensions are BROWSER aspects — `verify-theme.sh --list`
   labels `responsive` and `a11y-interactive` as BROWSER, meaning the agent flags them for a
   browser-capable caller. **A SKIP is not a PASS:** name who runs the 390px and desktop capture,
   and do not claim the checklist is green until they report back. `[live]` is required for any
   claim about the deployed site.

Inherited: a check that errors or times out produced an artifact, not a pass — re-run it by hand
(bug-230). Before attributing a grep hit to your direction, run the same grep against a pristine
tree via `git archive HEAD <path> | tar -x -C <scratch>` and diff the contents — **never
`git stash`**, the stack is shared across worktrees.

## Worked example

Real run in this repo, 2026-07-28 — asked to "set a design direction" for the SkyyRose storefront:

```bash
$ ls .impeccable.md docs/brand/visual-references.md
.impeccable.md
docs/brand/visual-references.md
```

Check #1 returns hits, so the direction is **already decided** and the correct action is adopt, not
derive. Reading `.impeccable.md` gives the locked answers verbatim `[repo]`:

- Purpose — a drop storefront where "the garment is the protagonist"
- Audience — "Luxury-streetwear buyers, Oakland / Bay Area rooted and culture-literate"
- Tone — "Oakland-forged · declarative-armor · athletic-luxury"
- Constraints — "no qualifiers, no urgency timers, no related-products clutter"

Check #2 against the dashboard's token layer returned `'rose-gold': '#B76E79'`, `charcoal: '#1A1A1A'`
at `frontend/tailwind.config.ts:19-22` `[repo]` — the direction is expressible in existing tokens,
so no additions needed. Outcome: zero new direction authored; handed to `frontend-design` for
implementation. Deriving a fresh direction here would have contradicted founder-locked canon.

## Failure modes

- **Re-deriving a direction that already exists.** The most expensive failure: the output looks
  thoughtful and quietly contradicts locked canon. Check #1 first, every time.
- **Inferring audience from the codebase.** Code shows what was built, not who it serves. A direction
  built on inferred audience is confident and wrong.
- **The direction is never written down.** Held only in the response, it is gone by the next session
  and the following one invents a different one. Persist it.
- **Rejecting a default by picking its neighbour.** "Not Inter, so Space Grotesk" is the same
  fingerprint one step over.
- **Claiming the Review Checklist is green from reading code.** Text fit, overflow, and stable
  dimensions are observable only in a render; assert them from `[repo]` and you are one scope-jump
  from a false severity claim (bug-287).
- **Proceeding when the user has not supplied Purpose/Audience.** Absent input is a stop, not a
  default (bug-230, ×6).

## See Also

For production-build defaults (accessibility WCAG 2.2 AA, Core Web Vitals budgets,
anti-fingerprint) and codebase-aware implementation, use the `frontend-design` skill.
This skill owns the upstream *design-direction* decision
(Purpose / Audience / Tone / Memorable-Detail / Constraints) made BEFORE coding.
