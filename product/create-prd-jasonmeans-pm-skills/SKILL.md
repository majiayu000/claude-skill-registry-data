---
name: create-prd
description: Write a complete Product Requirements Document (PRD) for a feature, product area, or initiative. Trigger this skill whenever someone asks to write a PRD, requirements doc, spec, or product brief — or says things like "I need to document this feature," "help me write up what we're building before sprint planning," or "my VP wants a spec for this project." This is the default PRD format covering problem statement, goals, user stories, success metrics, technical considerations, milestones, and risks — designed to align engineering, design, TPM, and leadership. Do NOT trigger for one-pagers for exec approval (use create-prd-one-pager), specs optimized for AI coding agents (use create-prd-claude-code), deep engineering specs with API contracts (use create-prd-engineering), or build-vs-buy decisions (use decision-brief).
---

# Create PRD (Standard)

Generate a general-purpose Product Requirements Document. This is the default PRD format -- covers the full lifecycle from problem definition through launch milestones. Designed for cross-functional audiences: engineering, design, TPM, and leadership.

## When to Use

- You are defining a new feature or product area and need a shared spec
- Engineering, design, and leadership all need to align on what you are building and why
- You need a document that lives in your wiki and serves as the single source of truth for the project
- You want a structured format that covers product context, user needs, and technical considerations without going deep on implementation

## When NOT to Use

- You need a PRD optimized for an AI coding agent to build from -- use `create-prd-claude-code`
- You need deep technical specs with data models, API contracts, and acceptance criteria per story -- use `create-prd-engineering`
- You need a concise one-pager for leadership approval or partner alignment -- use `create-prd-one-pager`

## Inputs

Ask the user for:

1. **Product/feature name** -- What are we calling this?
2. **Problem statement** -- What problem does this solve? Who has this problem?
3. **Goals** -- What does success look like? What are we NOT trying to do?
4. **Target users** -- Who are the primary users? Any secondary audiences?
5. **Context** -- Any existing docs, design files, prior art, or markdown specs?
6. **Constraints** -- Timeline, technical limitations, dependencies, or organizational constraints?

If the user provides partial input, fill in what you can and mark gaps with `[TBD]` placeholders.

## Outputs

A complete PRD in markdown, following the template in `references/template.md`. The document includes:

- Metadata header (author, date, status, stakeholders)
- Problem statement with user impact
- Goals and non-goals
- User stories
- Success metrics with baselines and targets
- Solution overview
- Technical considerations
- Milestones and timeline
- Risks and mitigations
- Open questions

## Steps

1. **Gather inputs** -- Ask the user for the inputs listed above. If they provide a design doc or markdown file, read it for context.
2. **Draft the problem statement** -- Write a clear, specific problem statement. Avoid jargon. Focus on the user's pain, not the solution.
3. **Define goals and non-goals** -- Goals should be measurable. Non-goals are just as important -- they set boundaries and prevent scope creep.
4. **Write user stories** -- Use "As a [user], I want to [action], so that [outcome]" format. Cover the primary persona first, then secondary.
5. **Set success metrics** -- Each metric needs a baseline (where we are today) and a target (where we want to be). If baselines are unknown, say so.
6. **Describe the solution** -- High-level solution overview. Include key user flows or wireframe references if available. Do not write implementation details here.
7. **Note technical considerations** -- Dependencies, integration points, performance requirements, data concerns. This section is for engineers to flag risks, not to spec the architecture.
8. **Build the milestone plan** -- Break work into phases. Each phase should have a clear deliverable and an approximate timeline.
9. **Identify risks** -- What could go wrong? What are the mitigations? Include both technical and organizational risks.
10. **List open questions** -- Every PRD has unknowns. Capture them explicitly with an owner and a target date for resolution.
11. **Review with the user** -- Walk through the draft. Ask: "Does this accurately capture what we are building and why? What is missing?"

## Example Usage

**User:** "I need a PRD for a new notification preferences feature. Users have been complaining they get too many emails and can't control which ones they receive."

**Agent:** Asks clarifying questions about target users, current notification types, any existing designs or docs, and timeline constraints. Then produces a full PRD using the template.

**User:** "Write a PRD for adding SAML SSO support. Here's the design doc: docs/saml-sso.md."

**Agent:** Reads the design doc for context, then produces a PRD that fills in product context around the technical work.

## Guardrails

- **Stay at the product level.** This is not an engineering spec. Technical considerations are for flagging risks and dependencies, not for designing the architecture.
- **Be specific about metrics.** "Improve user satisfaction" is not a metric. "Increase NPS from 32 to 45 within 90 days of launch" is.
- **Non-goals matter.** If you cannot articulate what is out of scope, the scope is not defined.
- **Mark unknowns honestly.** A PRD with `[TBD]` placeholders is better than a PRD with guesses presented as facts.
- **Keep it living.** Remind the user this document should be updated as decisions are made and open questions are resolved.

## Related Skills

- `create-prd-claude-code` -- PRD optimized for AI coding agents
- `create-prd-engineering` -- PRD with deep technical specs for engineering teams
- `create-prd-one-pager` -- Concise one-pager for leadership and partners
- `decision-brief` -- When the real need is a decision, not a spec
- `jobs-to-be-done` -- When you need to ground the PRD in user research
