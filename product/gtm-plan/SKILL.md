---
name: gtm-plan
description: Create a go-to-market plan for a launch, covering tier, audience, positioning and messaging, channels, enablement for sales and support, a timeline by release stage, metrics, and owners. Use when coordinating a launch across teams. For the go/no-go review, use launch-checklist.
---

# Go-To-Market Plan

Plan who a launch is for, what we say, where we say it, who needs to be ready, and when, sized to how big the launch really is.

## Reasoning Framework

Launches fail from misalignment more often than from bad features. Marketing announces before support is trained, sales pitches the wrong audience, and docs land a week late. A GTM plan settles who, why, how, and when in one place. Tiering comes first so a small improvement doesn't get a big-launch ceremony and a new product doesn't ship with a changelog line.

## Output Contract

| Artifact | Format | Handed to |
|----------|--------|-----------|
| GTM plan | Markdown, from `references/gtm-template.md` | PMM, sales, support, leadership |
| Messaging one-pager | Positioning statement plus message pillars (section 3–4 of the plan) | Everyone who talks about the launch |
| Launch timeline | Table mapped to release stages | Launch DRI, `launch-checklist` |

## When to Use

- A feature or product is heading toward beta or GA and several teams must coordinate
- Positioning or messaging is unclear or disputed
- Deciding how much launch effort a release deserves

## When NOT to Use

- Checking readiness for a specific stage gate: use `launch-checklist`
- Writing the requirements: use `create-prd` or `create-prd-one-pager`
- Pitching the launch to leadership: use `storytelling-for-impact` or `decision-brief`

## Inputs

1. **What is launching**: PRD or a short description; what's new versus changed.
2. **Target customers**: segments, personas, and who it is not for.
3. **Alternatives**: competitors and what customers do today.
4. **Dates by release stage**: Alpha, Closed Beta, Open Beta, GA (see `.claude/skills/launch-checklist/references/release-stages.md`).
5. **Pricing or packaging changes**, if any.
6. **Channels and teams available**: who owns docs, marketing, sales, and support.
7. **Goals**: what success looks like, with any existing baselines.

Mark unknowns `[TBD]` and keep going. Don't stall the whole plan on one missing input.

## Steps

1. **Pick the launch tier** from customer impact, strategic importance, and revenue impact:
   - **Tier 1**: new product or major capability. Full campaign, PR, sales enablement, events.
   - **Tier 2**: significant feature. Blog, email, in-app, docs, enablement for customer-facing teams.
   - **Tier 3**: improvement. Changelog, release notes, in-app hint, support note.
   Size every later section to the tier.
2. **Define the audience**: primary and secondary customers, what they struggle with today, and who is explicitly out of scope. Use `jobs-to-be-done` if this is fuzzy.
3. **Position it** with the five components in the template (alternatives, unique attributes, value with proof, best-fit customers, category), then write the one-sentence positioning statement.
4. **Write the messaging**: headline, three pillars, each with a proof point, objection handling, and variants per audience.
5. **Pricing and packaging**: plans, limits, and migration, or state "no change".
6. **Choose channels and assets** for the tier, each with an owner and due date.
7. **Plan enablement**: support trained before Open Beta, sales and CS before GA, an internal announcement at Closed Beta.
8. **Build the timeline** backward from GA across the release stages and tie each stage to its `launch-checklist` gate.
9. **Set success metrics**: leading, lagging, and guardrail metrics, each with a baseline, target, owner, and review date.
10. **Assign owners and list risks**, including who decides and who is told if the date slips.

## Examples

- "We're launching bulk export to all customers next month." Tier 2: positioning against CSV workarounds, docs plus in-app plus email, support trained before Open Beta, and adoption and ticket-volume metrics.
- "New analytics product, GA in Q1." Tier 1: full plan, design-partner quotes collected in Closed Beta, and sales enablement before GA.

## Guardrails

- Tier first. Don't write a Tier 1 plan for a Tier 3 change.
- Every claim in the messaging needs a proof point. Unproven claims are marked as hypotheses.
- No invented metrics or benchmarks. Use `[TBD]` and name who will supply them.
- Don't commit to dates engineering hasn't committed to.
- Keep unannounced launch details out of this public repo. Write plans to a private location.

## Related Skills

- `launch-checklist`: stage-gate readiness and go/no-go
- `create-release-notes`: GA release notes
- `map-stakeholders`: who must be aligned before launch
- `storytelling-for-impact`: the launch narrative
- `library/lenny-podcast/lenny-positioning-messaging/SKILL.md` and `library/lenny-podcast/lenny-launch-marketing/SKILL.md`: deeper playbooks
