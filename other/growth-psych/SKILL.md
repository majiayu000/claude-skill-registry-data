---
name: growth-psych
description: Audit landing, pricing and signup pages, review multi-step flows, and design growth experiments using 106 named psychology principles. Use for CRO or UX audits, flow reviews, A/B test ideas, "why isn't this converting", or a URL to critique.
---

# growth-psych

Conversion work anchored to named psychology principles. A finding without a principle is an opinion; one without a fix is a complaint. Serves lead or enquiry forms, self-serve signup and direct purchase.

Principle catalogue adapted from [growth.design/psychology](https://growth.design/psychology) (free cheat-sheet PDF linked there). Names and four categories follow it; every definition here is our own wording.

## Modes

Pick from the request; ask if unclear.

- **audit**: teardown of an existing page (landing, pricing, signup, campaign). Read `sections/audit-zones.md`, then `sections/deliverable.md`.
- **flow**: step-by-step review of a multi-step flow or mock (signup, onboarding, checkout, enquiry, booking), before or after build. Read `sections/flow-review.md`, then `sections/deliverable.md`.
- **experiment**: turn a principle into a testable hypothesis with metric, sample size and stop rule. Read `sections/experiments.md`.

## Core (all modes)

1. **Context.** If `.grid/project.yaml` exists, read it for brand, audience, funnel and metrics. Never assume them; ask for the goal and audience if absent.
2. **Visitor and job.** Who arrives, from where, wanting what; what the page or flow wants (lead sent, account created, payment made). Competing goals are a finding.
3. **Finding = observation + principle + why + fix.** Quote the real copy or describe the real element. Name the principle with its one-line meaning. Say why it matters for this goal. Write the actual replacement copy, not "be more benefit-driven".
4. **Balance.** Report principles used well, violated and missing. Depth over breadth: 8-15 findings.
5. **Rate** each finding: Impact 🔴 high / 🟠 medium / 🟡 low; Effort 🟢 copy or setting / 🟡 new asset / 🔴 redesign. Quick wins first.
6. **Principles.** Read only the categories the step needs: `sections/principles-information.md` (perception, layout, actions), `-meaning.md` (proof, offer, trust), `-time.md` (pricing, friction, commitment), `-memory.md` (endings, delight, retention).

## Capture

Fetch copy and structure with WebFetch. For visual claims use a browser: `browse` (gstack) or `anthropic-skills:chrome-browser`, at desktop and mobile widths. With neither, work from fetched copy and say "visual claims unverified". User screenshots win for visuals.

## Ethics

Persuade, never trick. Flag as trust findings, even if they convert: fake or resetting scarcity, pre-ticked opt-ins, confirmshaming, hidden costs, obstructed exits. When a manipulative pattern would work, say so and give the ethical alternative.

## Sections

Read a section only when its condition applies; do not preload them.
- sections/audit-zones.md: read when running audit mode (zone checklist, two passes)
- sections/flow-review.md: read when running flow mode
- sections/experiments.md: read when running experiment mode or turning findings into tests
- sections/deliverable.md: read when building an audit or flow report (structure, scoring, HTML)
- sections/principles-information.md: read when checking perception, hierarchy, layout, calls to action
- sections/principles-meaning.md: read when checking proof, offer, positioning, trust, copy
- sections/principles-time.md: read when checking pricing, defaults, friction, commitment, urgency
- sections/principles-memory.md: read when checking endings, onboarding, delight, retention
