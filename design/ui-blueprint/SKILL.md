---
name: ui-blueprint
description: Convert an approved UI brief into a concrete layout and visual blueprint — visual direction, information hierarchy, text wireframe, and responsive behavior — before any component-level work or code begins. Use this skill whenever the user has a brief (from ui-brief or equivalent) and is ready to think about layout, or when they jump straight to "design the screen" / "draw a wireframe" / "what should the layout look like" without yet having a layout spec. Always use it before ui-component-spec or ui-generate-code, because component and code work without an agreed layout is the most reliable way to get a result the user did not envision.
status: stable
---

# UI Blueprint

Converts an approved brief into a concrete layout spec. The output is the agreed map of the screen — where elements live, how they're ranked, how they reflow on small screens. It is the document that the user and the model align on before any component-level or code-level work happens.

## When to use this skill

Use this skill when:
- A brief exists (preferably from `ui-brief`) and the user is ready to think about layout.
- The user asks "what should this screen look like" or "wireframe this for me".
- A previous attempt at building this UI produced something the user didn't envision — re-blueprinting can recover.
- **Spec Recovery:** An implementation exists but no blueprint was created. Use this skill to document the as-built layout and hierarchy before improvements.

Do **not** use this skill when:
- No brief exists. Run `ui-brief` first. If the user refuses, document the brief inline at the top of the blueprint as a compressed `## Implied brief` block — but tell the user this is a substitute, not a replacement.
- The user only wants component-level details on an existing layout. Use `ui-component-spec` instead.

## Core principle

**A blueprint is the contract between the user's mental picture and the model's understanding.** ASCII or markdown table wireframes are deliberately ugly — that is the point. They strip away the seductive distractions (color, type, polish) and force agreement on the only thing that matters at this stage: what is on the screen, how it is ranked, and how it reflows.

## Pre-flight check

Before drafting, confirm:

1. **Brief exists and is current.** If no brief, run `ui-brief` first or insert a compressed brief at the top of the blueprint.
2. **Primary action from the brief is known.** The blueprint must visually privilege this action.
3. **Primary device is known.** The wireframe is drawn for the primary device first; other breakpoints are derivations.
4. **Information density preference is known.** Dense (B2B data tables, dashboards) vs. sparse (consumer onboarding, marketing). If the brief did not specify, ask before drafting.

If any of the four is missing, ask the user. Do not pick a default silently.

## Observed vs. Target (Spec Recovery protocol)

When using this skill for **Spec Recovery**, distinguish between the current implementation and the desired layout:

- **Observed:** The layout, hierarchy, and responsive behavior as they exist in the current UI (the "as-built").
- **Target:** The intended or improved layout and hierarchy.
- **Gap:** Any mismatch or unintentional layout decision in the current UI.

Use this pattern to ensure the recovered blueprint is a faithful document of intent, not just a description of accidental code.

## Workflow

### Step 1 — Establish visual direction

Translate the brief's tone into concrete UI properties. Banned vague words (modern, clean, sleek, etc.) must be converted before the blueprint can proceed.

Ask the user to name **one or two reference products** whose UI they want this to resemble. If they cannot, propose 2–3 candidates based on the brief and ask them to pick.

Then describe the visual direction as a short list of concrete properties — see template.

### Step 2 — Rank information hierarchy

List every element that needs to appear on the screen. Rank them 1 to N by importance. The primary action must be in the top 3. Anything below rank 8 should probably be removed or pushed to a secondary screen — flag it for the user.

### Step 3 — Draw the wireframe

Use ASCII or a markdown table to draw the layout for the **primary device first**. Do not skip this step. The wireframe must show:

- Where each ranked element lives.
- Approximate proportions (relative widths/heights — exact pixels are not needed yet).
- Empty space (whitespace is a design decision, label it).
- Reading order (which element does the eye hit first, second, third).

If you can't draw it in ASCII or a markdown table, the layout is not yet decided.

### Step 4 — Specify responsive behavior

For each non-primary breakpoint, describe how the layout reflows. Use the keywords: `stack`, `collapse`, `hide`, `move`, `resize`, `swap`. Be specific about which elements do what.

### Step 5 — Confirm with the user

End with a numbered list of every layout decision and every assumption. Ask for sign-off. Do not move to `ui-component-spec` until the user has approved.

## Output template

Always produce output in this exact structure.

```markdown
---
spec_type: blueprint
spec_id: <slug, ideally matching the brief slug>
based_on: brief-<slug>
created: <YYYY-MM-DD>
status: draft
---

# Blueprint: <descriptive title>

## 1. Implied or referenced brief
<Either a one-line pointer to the brief file, OR a compressed 3-line summary if no brief exists.>
- **Goal:** ...
- **Primary user:** ...
- **Primary action:** ...

## 2. Visual direction

### 2.1 Reference products
- **Primary reference:** <named product, with one sentence on what specifically to take from it>
- **Secondary reference (optional):** <named product, what to take>
- **Anti-references:** <named products this should NOT resemble, with reason>

### 2.2 Concrete visual properties
| Property | Decision | Rationale |
|---|---|---|
| Information density | dense / medium / sparse | <one-line reason from the brief> |
| Layout paradigm | sidebar / top-nav / split / single-column / canvas | <reason> |
| Type | sans / serif / mixed | <reason> |
| Color treatment | monochrome / accent / multi-color / brand-led | <reason> |
| Surface treatment | flat / soft-shadow / raised-cards / borderless | <reason> |
| Corner radius | sharp / subtle / rounded / pill | <reason> |
| Mood | <one or two concrete adjectives, e.g. "calm and serious", "energetic and playful"> | <reason> |

## 3. Information hierarchy

Ranked from most to least important. The primary action must be in the top 3.

| Rank | Element | Why it ranks here |
|---|---|---|
| 1 | <element> | <reason tied to brief goal> |
| 2 | <element> | ... |
| 3 | <element> | ... |
| ... | ... | ... |

**⚠️ Flagged for review:** <elements ranked 8 or below — should they be on this screen at all?>

## 4. Wireframe — primary device

Drawn for: <desktop @ ~1280px | mobile @ ~390px | tablet @ ~768px>

```
+------------------------------------------------------------+
| [Logo]                  [Nav]              [User menu] [⚙] |  <- 64px header
+------------------------------------------------------------+
| Sidebar          | Main content area                       |
| (240px)          |                                         |
|                  |  [Page title]                           |
| - Item 1         |  [Primary action button]   <- rank 1    |
| - Item 2         |                                         |
| - Item 3         |  +-----------------------+              |
|                  |  | Data table            |  <- rank 2   |
|                  |  +-----------------------+              |
|                  |                                         |
|                  |  [Secondary action]   <- rank 4         |
+------------------------------------------------------------+
```

### Reading order
1. <element the eye hits first — explain why>
2. <element the eye hits second>
3. <element the eye hits third>

### Whitespace decisions
- **Generous whitespace around:** <element, and why — usually the primary action>
- **Tighter spacing between:** <element group, and why — usually related items>

## 5. Responsive behavior

| Breakpoint | Behavior |
|---|---|
| Desktop (≥1024px) | Primary layout as drawn above. |
| Tablet (768–1023px) | <Specifically describe what changes. Use keywords: stack, collapse, hide, move, resize, swap.> |
| Mobile (<768px) | <Same.> |

**Critical reflow rules:**
- The primary action must remain in the top half of the viewport at every breakpoint.
- <Other rules specific to this layout.>

## 6. What is NOT decided yet

These will be determined in `ui-component-spec` or later, not here:
- Specific component states (hover, focus, error, empty, loading)
- Exact colors, font sizes, spacing values (those come from `ui-system`)
- Validation rules, behavior on submit
- Microcopy / button labels (those come from `ui-microcopy`)

## 7. Open questions
- <Numbered, specific.>

## 8. Assumptions made
- ⚠️ <Each assumption flagged.>
```

## Examples

### Example 1 — dense B2B dashboard

**User has approved a brief for "internal admin tool to monitor server health for a 12-person ops team." Primary action: triage incidents. Density: dense. Device: desktop.**

The blueprint should pick:
- Reference: a tool like Datadog, Grafana, or Linear (whichever the user names).
- Layout paradigm: sidebar nav, dense data table as primary content.
- Density: dense — stats packed tightly, small type, minimal whitespace.
- Hierarchy: 1) incident list, 2) filter controls, 3) status overview, 4) navigation.

The wireframe is desktop-first because ops teams work at desks. Mobile reflow likely says "primary use case is desktop; mobile collapses sidebar to a drawer and shows incident list as cards" — but flag whether mobile is even a target.

### Example 2 — consumer onboarding screen

**Brief: first-time signup screen for a meditation app. Primary action: complete account creation. Primary user: novice, mobile-first.**

The blueprint should pick:
- Reference: whatever consumer app the user names (e.g. Calm, Headspace).
- Layout paradigm: single-column, centered.
- Density: sparse — generous whitespace, large touch targets.
- Hierarchy: 1) primary CTA, 2) value proposition, 3) social-login alternatives, 4) "skip for now" or fine print.

Wireframe is mobile-first (390px wide). Desktop reflow says: "constrain max-width 480px, center on the page; do not let form stretch."

## Rules that prevent hallucinated decisions

1. **Never name a reference product the user did not approve.** If the user said "modern", ask them to name a product. Do not assume.
2. **Never decide information density without confirmation.** Dense vs. sparse is a load-bearing decision and the user often has strong opinions.
3. **Never invent secondary actions.** Only list elements the brief implies or the user explicitly named. If you think something is missing, surface it as an open question.
4. **Never skip the wireframe.** If you cannot draw the layout in ASCII or a markdown table, the layout is not decided yet — say so and ask.
5. **Never specify exact pixel values.** Blueprints work in approximate proportions and visual ranking, not in design tokens. Tokens come from `ui-system`.

## Acceptance criteria for this skill's output

A blueprint produced by this skill is acceptable only if every one of these is true:

- [ ] Frontmatter links to a brief (or a compressed implied brief is included inline).
- [ ] At least one named reference product appears, with a specific note on what to take from it.
- [ ] The Information density row uses one of: dense / medium / sparse — not a vague phrase.
- [ ] The Layout paradigm row uses one of the named paradigms — not a free-form description.
- [ ] Every element listed in the hierarchy table has a "why it ranks here" justification, not just a number.
- [ ] The primary action from the brief appears in the top 3 hierarchy ranks.
- [ ] An ASCII or markdown table wireframe is present for the primary device.
- [ ] Reading order is explicitly listed.
- [ ] Every non-primary breakpoint has reflow behavior described using the verbs: stack, collapse, hide, move, resize, swap.
- [ ] No banned vague words (modern, clean, sleek, intuitive, etc.) appear in the body without a concrete translation.
- [ ] An "open questions" or "assumptions" section is present (one of the two must have content; both empty means you didn't push hard enough).

If any check fails, revise before delivering.
