---
name: create-prd-one-pager
description: Write a single-page PRD for leadership and partner audiences. Covers problem, proposal, impact, timeline, ask, and risks using business language. Use when you need to drive alignment and approval, not detail implementation.
---

# Create PRD (One-Pager)

Generate a single-page Product Requirements Document for leadership and partner audiences. This format is deliberately concise -- it covers the problem, proposed solution, business impact, timeline, resource ask, and key risks. Everything a decision-maker needs to say yes, nothing they do not.

The discipline of a one-pager is compression. If you cannot explain it in one page, you do not understand it well enough yet.

## When to Use

- You need leadership approval or alignment on an initiative
- You are pitching a feature or project to a partner team
- You want to circulate a proposal before investing in a full PRD
- The audience cares about "what and why," not "how"
- You need a document that can be read in under 5 minutes

## When NOT to Use

- The audience is engineering and they need to build from this -- use `create-prd-engineering`
- You need a full cross-functional spec -- use `create-prd` (standard)
- You need an AI agent to build from this -- use `create-prd-claude-code`
- You need a formal decision with options and comparison -- use `decision-brief`

## Inputs

Ask the user for:

1. **Initiative name** -- What are we calling this?
2. **Problem** -- What problem are we solving? Why does it matter now?
3. **Proposed solution** -- What are we proposing? (2-3 sentences max.)
4. **Impact** -- What is the expected business impact? Revenue, retention, efficiency, strategic positioning?
5. **Timeline** -- When would this ship? What are the key milestones?
6. **Ask** -- What do you need from the reader? Approval, resources, alignment, feedback?
7. **Risks** -- What could go wrong? What are the top 2-3 concerns?
8. **Audience** -- Who will read this? (This shapes the language and emphasis.)

If the user has an existing full PRD, distill it into one-pager format.

## Outputs

A single-page PRD in markdown, following the template in `references/template.md`. The document fits on one printed page and includes:

- Title and metadata
- Problem statement (2-3 sentences)
- Proposed solution (2-3 sentences)
- Business impact (quantified where possible)
- Timeline (3-5 milestones max)
- The ask (what you need from the reader)
- Key risks (2-3 max)

## Steps

1. **Gather inputs** -- Ask for the inputs above. If the user has an existing longer doc, read it and distill.
2. **Write the problem statement** -- Two to three sentences. Lead with the user or business pain. Avoid jargon. If the reader does not feel the problem, they will not care about the solution.
3. **Write the proposal** -- Two to three sentences describing what you are proposing. Stay at the "what," not the "how." No architecture, no technical details.
4. **Quantify the impact** -- Use numbers. "Reduces support tickets by 30%" is better than "improves customer experience." If exact numbers are not available, use estimates with ranges: "Expected to reduce churn by 5-10% based on comparable features."
5. **Build the timeline** -- Three to five milestones maximum. Each milestone is a date and a deliverable. Keep it high-level: "Q2: Beta with 10 pilot customers" not "Sprint 4: Complete API endpoint refactoring."
6. **State the ask** -- Be direct. "I am requesting approval to staff a team of 3 engineers for Q2-Q3" is clear. "I would love your thoughts" is not an ask.
7. **List risks** -- Two to three maximum. Each risk gets one sentence for the risk and one sentence for the mitigation. Do not list more than three -- this is a one-pager, not a risk register.
8. **Edit for length** -- The entire document should fit on one printed page. If it does not, cut. Every sentence must earn its place.
9. **Review with the user** -- Key question: "If a VP reads this in 3 minutes, will they understand the problem, the proposal, and what you need from them?"

## Example Usage

**User:** "I need a one-pager to get VP approval for building a self-service analytics dashboard. We have 200+ ad-hoc data requests per month from clients."

**Agent:** Asks about the expected impact (time savings, CSAT improvement), timeline expectations, and what specifically the VP needs to approve (headcount, budget, priority). Produces a one-page PRD focused on business impact.

**User:** "Turn this 8-page PRD into a one-pager for the leadership review next week."

**Agent:** Reads the full PRD, identifies the core problem/solution/impact, and distills it into one-pager format. Flags if key information (like the ask or impact metrics) is missing from the source doc.

## Guardrails

- **One page means one page.** If the rendered markdown exceeds approximately 500 words, it is too long. Cut ruthlessly.
- **Business language, not engineering language.** "REST API migration" means nothing to a VP. "Faster integrations for partners, reducing onboarding time from weeks to days" is what they care about.
- **Quantify impact.** Unquantified impact sounds like opinion. Even rough estimates with ranges are better than qualitative statements.
- **The ask must be specific.** "Thoughts?" is not an ask. "Approval to allocate 3 engineers in Q2" is. If the user does not know what they are asking for, help them figure it out before writing the doc.
- **Do not hide risks.** Leadership respects PMs who surface risks with mitigations. Two honest risks build more trust than zero risks, which reads as naive.
- **Do not add sections.** The power of a one-pager is constraint. Resist the urge to add "nice to have" sections. If it does not fit the template, it does not belong.

## Related Skills

- `create-prd` -- Full PRD when the one-pager gets approved and you need to spec it out
- `create-prd-engineering` -- Engineering spec for the build phase
- `decision-brief` -- When you need a formal decision with options and comparison
- `storytelling-for-impact` -- When the one-pager needs a compelling narrative
