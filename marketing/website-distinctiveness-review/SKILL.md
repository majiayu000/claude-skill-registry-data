---
name: website-distinctiveness-review
description: Reviews an existing website, page concept, mockup, or creative direction for whether it feels uniquely owned by the brand rather than generic, template-led, or AI-default. Use when the user asks whether a design stands out, feels memorable, attracts the right audience, repels the wrong audience, expresses a specific brand personality, or belongs unmistakably to one business.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: ui-ux-polish
  task_type: review
  audience: web-designers-product-designers-creative-directors-brand-teams
  tags:
    - distinctiveness
    - brand-world
    - audience-fit
    - creative-direction
    - web-design
    - ai-sameness
  status: draft
  side_effects: none
---

# Website Distinctiveness Review

## Purpose

Review whether a website or proposed design direction feels specific, ownable, and intentional enough to belong unmistakably to one business and one audience.

This skill does not judge novelty for novelty's sake. It tests whether the design translates real brand characteristics into recognizable visual, verbal, structural, and experiential signals rather than relying on category clichés, fashionable surface treatments, template defaults, or undirected AI output.

The review should help sharpen an existing direction. It should not code the interface or replace broader brand strategy.

## When to use this skill

Use this skill when:

- The user asks whether a website stands out or feels generic.
- A design looks polished but could plausibly belong to several competitors.
- The user suspects a layout feels template-led, trend-led, or AI-generated.
- A team wants the site to attract a specific audience rather than appeal vaguely to everyone.
- The brand personality is known, but the website does not express it strongly.
- A concept needs a clearer emotional position before visual refinement.
- Multiple touchpoints exist and the website should feel like part of the same brand world.
- A redesign risks removing the features that made the original recognizable.

Do not use this skill when:

- The main problem is unclear purpose, audience, content, or requirements; use `design-problem-framer` first.
- The user needs several new structural layout options; use `layout-direction-explorer`.
- The task is primarily hierarchy, balance, alignment, spacing, or composition; use `layout-principles-review`.
- The user needs to compare finished design directions and choose one; use `design-direction-decision`.
- The main goal is conversion architecture, CTA strategy, objection handling, or detailed trust design; use `conversion-creative-director`.
- The user wants radical concept territories before interface design; use `provocative-concept-director`.
- The request is to implement, code, or recreate the interface.

## Inputs to inspect

Inspect the smallest useful set of available inputs:

- Website URL, screenshots, mockups, wireframes, or prototypes
- Brand brief, positioning statement, values, or verbal identity
- Product or service description
- Intended audience, customer segments, or user personas
- Competitor or category references
- Existing visual identity, campaigns, packaging, social content, or editorial material
- Copy, headlines, claims, testimonials, case studies, or proof assets
- Design rationale or creative-direction notes
- AI prompts or generated assets when sameness is a concern

If important context is missing, identify the gap and make bounded assumptions. Do not invent a detailed brand strategy from a screenshot alone.

## Core review question

Ask:

> If the logo, company name, and product name disappeared, what evidence would still make this design belong to this brand and appeal to this audience?

A strong result should have several mutually reinforcing answers. A weak result depends mainly on the logo, generic copy, fashionable styling, or category-standard imagery.

## Review lenses

### 1. Brand ownability

Determine whether the design contains recognizable signals rooted in the business rather than borrowed from the category.

Inspect:

- Distinctive point of view
- Business-specific language and imagery
- Recognizable visual devices
- Meaningful symbols, materials, metaphors, or behaviors
- Signature interactions or content structures
- Elements competitors could not copy without appearing derivative

Do not confuse unusual decoration with ownability. A strange gradient is not a brand idea.

### 2. Audience specificity

Determine whether the design is clearly shaped for a particular audience.

Inspect:

- What the intended audience values, fears, rejects, or aspires to
- Cultural and category references the audience will recognize
- Tone, density, pacing, and interaction expectations
- Signals of price level, seriousness, energy, expertise, or belonging
- Whether the design is trying to please incompatible audiences simultaneously

The goal is not hostility toward everyone else. The goal is confident relevance.

### 3. Emotional polarity

Determine whether the design creates an immediate, appropriate reaction rather than neutral acceptance.

Inspect:

- The likely five-second impression
- Emotional temperature
- Confidence versus caution
- Familiarity versus surprise
- Restraint versus exuberance
- Whether the reaction supports the brand and task

A strong design may not appeal to everyone, but its intended audience should understand why it exists.

### 4. Brand-world continuity

Determine whether the website feels like one part of a coherent wider experience rather than an isolated landing page.

Inspect:

- Continuity with social, editorial, campaign, product, packaging, or in-person touchpoints
- Reusable visual and verbal rules
- Whether the website can absorb future content without losing its identity
- Whether each page feels like the same world at a different intensity
- Whether the brand remains recognizable across large and small surfaces

Do not require every channel to look identical. Look for shared logic, not copy-and-paste consistency.

### 5. Evidence and authenticity

Review whether major claims are supported by credible, concrete material.

Inspect:

- Work samples, demonstrations, before-and-after evidence, or process visibility
- Specific outcomes rather than vague praise
- Real voices, faces, artifacts, environments, or customer language
- Third-party or independently verifiable sources where appropriate
- Proximity between a claim and the evidence supporting it

Keep this lens at the level of distinctiveness and credibility. Route a full persuasion or conversion audit to `conversion-creative-director`.

### 6. Intentional system signals

Determine whether typography, spacing, composition, imagery, and motion appear governed by a deliberate system.

Inspect:

- Consistent type roles and scale relationships
- Repeatable spacing and layout logic
- Clear visual hierarchy
- Consistent image treatment
- Recurring motion or interaction grammar
- Purposeful exceptions that create emphasis

Do not perform a full layout audit here. Record system-level concerns and route detailed composition issues to `layout-principles-review`.

### 7. Human authorship versus AI-default sameness

Determine whether AI or templates appear to have amplified a point of view or replaced one.

Common AI-default signals include:

- Generic hero composition with interchangeable copy
- Abstract 3D objects unrelated to the business
- Polished but context-free imagery
- Safe gradients, glass cards, floating pills, and empty dashboard motifs
- Repeated section rhythms with no narrative reason
- Broad claims unsupported by specific evidence
- A visual style chosen because it is fashionable rather than meaningful

Do not reject AI-generated material merely because AI was used. Judge whether the result has been selected, edited, combined, and directed through a specific human perspective.

## Workflow

1. **Establish the review target**
   - Identify the page, concept, prototype, or direction being reviewed.
   - State whether the evidence is sufficient for a full review or only a provisional one.

2. **Summarize the intended identity**
   - Describe the business, audience, offer, and desired impression in one compact paragraph.
   - Separate confirmed facts from inferred characteristics.

3. **Map the category default**
   - Identify the familiar visual, verbal, and structural patterns used by competitors or comparable products.
   - Mark which defaults are useful conventions and which create sameness.

4. **Run the substitution test**
   - Remove or mentally replace the logo, brand name, product name, and headline.
   - Ask whether a competitor could adopt the design with minimal changes.
   - Record the exact elements that survive the substitution and those that collapse.

5. **Run the audience pull-and-push test**
   - State what should strongly attract the intended audience.
   - State what may appropriately signal “not for me” to a mismatched audience.
   - Flag accidental repulsion caused by confusion, inaccessibility, exclusion, or poor usability. Do not mislabel these failures as bold positioning.

6. **Run the five-second reaction test**
   - Record the likely immediate descriptors a visitor would use.
   - Compare them with the intended descriptors.
   - Identify neutral, contradictory, or misleading signals.

7. **Review the brand world**
   - Check whether visual, verbal, content, proof, and interaction signals reinforce one another.
   - Check whether the logic can extend across pages and adjacent touchpoints.
   - Identify isolated effects that do not belong to the wider system.

8. **Identify ownable signals**
   - Preserve strong existing signals.
   - Select three to five signals that can become a recognizable system.
   - Each signal must have a reason connected to the brand or audience.

9. **Locate generic or borrowed signals**
   - Identify category clichés, unexplained trends, AI-default patterns, and competitor-like choices.
   - Explain what makes each signal generic in this context.
   - Do not recommend removing conventions that support comprehension unless a better replacement is defined.

10. **Propose intervention levels**
    - `Preserve`: strong, ownable elements that should remain.
    - `Sharpen`: promising elements that need stronger consistency, contrast, specificity, or repetition.
    - `Replace`: generic or contradictory elements that weaken the direction.
    - `Introduce`: missing signals needed to complete the brand world.

11. **Route specialist follow-up**
    - Name only the smallest set of related skills needed next.
    - Explain the unresolved question each selected skill should answer.

## Distinctiveness verdict

Use one verdict:

- **Ownable** — The design has a clear point of view, audience fit, and several mutually reinforcing signals that would remain recognizable without the logo.
- **Emerging** — The direction contains specific ideas, but generic patterns still dominate or the signals are not yet repeated consistently.
- **Interchangeable** — The design is competent but could belong to many businesses with minor copy and asset changes.
- **Misaligned** — The design is distinctive, but its strongest signals conflict with the intended audience, offer, or brand position.
- **Insufficient evidence** — The supplied material does not support a responsible verdict.

Do not average away contradictions. A polished but misaligned design is not “mostly good.”

## Output format

Return:

```md
## Distinctiveness verdict

**Verdict:** Ownable | Emerging | Interchangeable | Misaligned | Insufficient evidence

One-paragraph explanation grounded in the supplied design.

## Intended identity

- Business or product:
- Intended audience:
- Intended impression:
- Confirmed inputs:
- Assumptions:

## Five-second reaction

**Likely reaction:** ...

**Intended reaction:** ...

**Gap:** ...

## Review findings

| Lens | Rating | Evidence | Why it matters |
|---|---|---|---|
| Brand ownability | Strong / Partial / Weak / Unknown | ... | ... |
| Audience specificity | Strong / Partial / Weak / Unknown | ... | ... |
| Emotional polarity | Strong / Partial / Weak / Unknown | ... | ... |
| Brand-world continuity | Strong / Partial / Weak / Unknown | ... | ... |
| Evidence and authenticity | Strong / Partial / Weak / Unknown | ... | ... |
| Intentional system signals | Strong / Partial / Weak / Unknown | ... | ... |
| Human authorship | Strong / Partial / Weak / Unknown | ... | ... |

## Substitution test

- Elements that remain recognizable without the logo:
- Elements a competitor could reuse unchanged:
- Overall result:

## Audience pull and push

### Pulls the intended audience

- ...

### Appropriately filters mismatched audiences

- ...

### Accidental friction or exclusion

- ...

## Ownable signal system

| Signal | Brand or audience rationale | Current state | Recommended use |
|---|---|---|---|
| ... | ... | Preserve / Sharpen / Introduce | ... |

## Generic signals to remove or transform

| Signal | Why it feels generic here | Better direction |
|---|---|---|
| ... | ... | ... |

## Recommended interventions

### Preserve

- ...

### Sharpen

- ...

### Replace

- ...

### Introduce

- ...

## Recommended next skill

- `skill-name` — unresolved question it should answer.
```

Do not fill every section with generic advice. Omit empty rows and state when evidence is unavailable.

## Quality bar

The task is complete only when:

- The verdict is based on visible or supplied evidence.
- The review distinguishes distinctiveness from decoration.
- Audience attraction is separated from accidental usability or accessibility problems.
- The substitution test identifies concrete interchangeable elements.
- Recommendations preserve useful conventions while replacing generic expression.
- Every proposed signature signal has a brand or audience rationale.
- The review recognizes existing strengths instead of redesigning everything by reflex.
- AI use is judged by direction and editing, not by ideology.
- The output does not drift into code or implementation details.
- Specialist follow-up is limited to the smallest useful set of related skills.

## Edge cases

- **No brand strategy exists:** Produce a provisional review, list the missing decisions, and route to `design-problem-framer`.
- **The brand intentionally uses category conventions:** Check whether copy, proof, content, behavior, or service model supplies the distinctiveness instead of demanding visual novelty.
- **A utility product should feel neutral:** Review clarity, tone, interaction behavior, and proof for ownability; do not force theatrical styling.
- **A regulated or high-trust sector limits experimentation:** Favor distinctive evidence, language, structure, material choices, and calm confidence over novelty that reduces credibility.
- **Multiple audiences are required:** Identify a stable brand core and specify where content or emphasis may adapt by audience.
- **The design is intentionally minimal:** Test precision, editing, typography, imagery, pacing, and verbal identity. Minimal does not mean interchangeable.
- **The design is intentionally maximal:** Test whether the density follows a coherent world rather than accumulating unrelated effects.
- **Only one screenshot is supplied:** Limit claims about navigation, continuity, responsiveness, motion, and the wider brand ecosystem.
- **Generated imagery is inconsistent:** Review the shared art direction, subject logic, lighting, framing, texture, and narrative rather than merely asking for more images.
- **Distinctiveness conflicts with accessibility:** Accessibility and usability take priority. Route the conflict to the relevant accessibility review instead of defending exclusion as creative boldness.

## Related skills

- `design-problem-framer` — defines the problem, audience, purpose, message, and priorities before direction work.
- `layout-direction-explorer` — generates alternative structural directions.
- `layout-principles-review` — audits hierarchy, balance, contrast, alignment, repetition, and flow in detail.
- `design-direction-decision` — compares candidate directions and selects one.
- `provocative-concept-director` — creates unexpected conceptual territories before interface design.
- `experimental-web-art-director` — develops a visual and emotional premise with signature moments.
- `editorial-digital-designer` — strengthens typography, composition, hierarchy, and pacing.
- `minimalist-brand-director` — builds distinction through reduction and restraint.
- `conversion-creative-director` — develops persuasion, proof, trust, objection handling, and CTA strategy.
- `motion-experience-director` — translates the chosen identity into purposeful motion behavior.
- `design-review-orchestrator` — selects and sequences the smallest useful group of design skills.
