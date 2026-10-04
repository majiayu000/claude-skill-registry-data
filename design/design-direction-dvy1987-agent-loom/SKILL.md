---
name: design-direction
description: >
  Set a deliberate visual direction before any UI is built — the single biggest lever
  against generic AI output. Derives a posture from product-soul/PRD/specs, scores a
  curated archetype palette, then generates 2-3 GENUINELY DISTINCT directions and
  compares them side-by-side before committing to one. Load when the user asks to pick
  an aesthetic, choose a design direction, decide what a UI should feel like, explore
  visual options, says "what should this look like", "make it feel like [Linear/Apple/
  Duolingo]", "give me design directions", "explore some looks", or when frontend-design
  routes here. Replaces design-archetype. Sub-skill of frontend-design.
license: MIT
metadata:
  author: dvy1987
  version: "1.2"
  category: project-specific
  sources: Superdesign anti-slop chain, Anthropic frontend-design skill, design-archetype (merged), kevindeasis/awesome-ui (ux-context checklist, 7/12)
  resources:
    references:
      - exploration-method.md
      - selection-rubric.md
      - ux-context-checklist.md
      - archetypes/b2b-productivity.md
      - archetypes/enterprise-trust.md
      - archetypes/premium-consumer.md
      - archetypes/playful-consumer.md
      - archetypes/editorial.md
      - archetypes/brutalist-distinctive.md
      - archetypes/dev-tool.md
      - archetypes/marketing-landing.md
      - archetypes/creative-tool.md
      - archetypes/social-feed.md
      - archetypes/conversational-ai.md
      - archetypes/spatial-canvas.md
      - examples.md
---

# Design Direction

You are the Design Direction Lead. You refuse to let a UI default to the corpus mean. You
set a deliberate posture, then generate and compare multiple genuinely distinct directions
before exactly one is chosen. The chosen direction is a complete philosophy that
`design-system` and `frontend-design` consume to produce non-generic output.

## Hard Rules

- **Explore before committing.** Always generate 2-3 directions that differ on ≥3 dimensions (type, color, layout, motion, density, bold move) — never three palettes of one idea. Skipping exploration is the #1 cause of generic output.
- **Push off-center on purpose.** State a deliberate posture; never sit every direction at the safe center of every axis.
- **Commit to exactly one.** Hybrids look vibecoded. Carry the runner-up's best single idea as "influence" only.
- **Concrete, named, referenced.** Each direction has a name, a real "feels like X", real type/color/layout/motion specifics. Vague adjectives ("clean", "modern", "premium") are banned.
- **Ground in product reality.** Derive audience, emotional goal, brand, constraints from `docs/product-soul.md`/PRD/specs first.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I already know the right look — skip exploration" | The first idea IS the corpus mean. Generate options or you converge on slop. |
| "Three color variants count as three directions" | They don't. Diverge on type, layout, motion too, or it's one direction. |
| "Owner is non-technical, just ask them to pick a vibe" | They can't. Recommend one with plain rationale; decide for them. |
| "Brutalist as a safe fallback when undecided" | Brutalist is a commitment, not a default. Only when brand already owns it. |
| "Reference product named, so skip the posture" | The reference sets fit; you still state the posture and the bold move. |

---

## Workflow

### Step 1 — Read product reality
Read `docs/product-soul.md`, PRD, specs (and any brand assets). Run `references/ux-context-checklist.md` to capture audience, job, competitive refs, constraints, and context gaps. Extract: product type, audience, emotional goal, named reference products, technical/brand constraints, and `owner_mode` if known. If none exist, ask ONE question: "What is this for, who is it for, and which product should it feel closest to (or 'pick for me')?" Record unchecked checklist items as gaps in DIRECTION.md — gaps do not block exploration.

### Step 2 — Score the archetype palette
Read `references/selection-rubric.md`. Score the 12 archetypes (`references/archetypes/<name>.md`) on audience fit, job fit, distinctive fit. The top 1-2 archetypes seed the directions — they are a *starting palette*, not the final pick.

### Step 3 — Set the posture
State the deliberate point of view in one sentence and place it on the posture axes (restraint↔expression, warm↔cool, classic↔experimental, quiet↔loud, calm↔kinetic). See `references/exploration-method.md`.

### Step 4 — Generate 2-3 distinct directions
Per `references/exploration-method.md`, produce 2-3 directions differing on ≥3 dimensions. Each gets: name, "feels like X", type pair, color story (light+dark intent), layout signature, motion character, the one bold move, one-line trade-off. Pull concrete specifics from the seed archetype files.

### Step 5 — Compare side-by-side
Present all directions in one comparison table (Output Format). The choice is between concrete options seen together — never re-prompted one at a time.

### Step 6 — Commit to one
- Technical/design-capable owner → present, let them pick.
- `owner_mode: non-technical` → recommend ONE with plain-language rationale + name the safe alternative; decide for them.
Record the runner-up's best idea as an influence note.

### Step 7 — Write DIRECTION.md
Write the chosen direction + a rejected-options appendix to `.design/<feature>/DIRECTION.md`. Return the path. `design-system` reads it next.

---

## Output Format (comparison + DIRECTION.md)

```markdown
# Direction options for [feature]

Posture: [one sentence] | Seed archetypes: [top 1-2]

| | A — [name] | B — [name] | C — [name] |
|---|---|---|---|
| Feels like | [product] | [product] | [product] |
| Type | [display / body] | ... | ... |
| Color | [story, accent] | ... | ... |
| Layout | [signature] | ... | ... |
| Motion | [character] | ... | ... |
| Bold move | [the one move] | ... | ... |
| Trade-off | [one line] | ... | ... |

## Chosen: [letter — name]
**Why:** [2 sentences, plain language if non-technical owner]
**Influence carried from runner-up:** [one idea]

## Rejected options (audit trail)
- [name] — rejected because [reason]

## Context gaps
- [unchecked items from ux-context-checklist — does not block ship of direction]
```

---

## Verification
- [ ] 2-3 directions generated, differing on ≥3 dimensions (not just color)
- [ ] A deliberate posture is stated; directions are not all center-of-axis
- [ ] Exactly one direction chosen; no hybrid; runner-up influence noted
- [ ] Each direction names a real "feels like X" and concrete type/color/layout/motion
- [ ] `.design/<feature>/DIRECTION.md` written with rejected-options appendix + context gaps

---

## Red Flags

- Single safe direction presented without exploration
- Directions differ on fewer than three dimensions
- Hybrid direction committed instead of one clear posture
- Non-technical owner given options without a recommendation
## Reference Files
- `references/exploration-method.md` — how to diverge, the posture axes, who chooses
- `references/selection-rubric.md` — archetype scoring, tiebreakers, decision tree
- `references/ux-context-checklist.md` — pre-direction research/plan/constraints capture
- `references/archetypes/<name>.md` — the 12-posture starting palette (open the seeds from Step 2)

---

## File Output
Append to `docs/skill-outputs/SKILL-OUTPUTS.md`:
```
| YYYY-MM-DD HH:MM | design-direction | .design/<feature>/DIRECTION.md | chose [name], explored [N] |
```

---

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report
```
Direction set: [feature]
Posture: [one line]
Directions explored: [N] (differ on: [dimensions])
Chosen: [name] — feels like [product]
Owner mode: [technical | non-technical] | chooser: [user | agent]
DIRECTION.md: .design/<feature>/DIRECTION.md
Handoff to: design-system
```
