---
name: project-product-router
description: "Choose the right Project + Product skill for a request and sequence multiple skills when the work spans discovery, requirements, delivery, launch, PRINCE2 governance, or team rituals."
---

# Project Product Router

Use this skill when the user asks for help but has not named a specific skill, or when the request spans multiple project/product workflows.

## Routing Rules

Start with the user's immediate artifact, not the broad topic.

### Meetings, Status, And Decisions

- Meeting notes, action items, decisions: `decision-meeting-notes`
- Project status, blockers, risks, decision requests: `delivery-status-brief`
- Stakeholder update: `stakeholder-decision-note`
- Executive update or leadership recommendation: `executive-product-note`

### Product Definition

- Requirements, product spec, feature brief: `product-requirements-blueprint`
- Engineering alignment, implementation constraints: `technical-alignment-brief`
- Objectives, key results, product outcomes: `outcome-map`
- Roadmap story or sequencing rationale: `roadmap-story-brief`
- Roadmap review deck structure: `roadmap-review-outline`
- Strategic narrative: `strategic-story-builder`

### Customer And Market Learning

- Discovery interview plan: `discovery-conversation-guide`
- Interview synthesis: `interview-signal-synthesis`
- Research synthesis across sources: `research-evidence-brief`
- Assumptions and validation risk: `assumption-risk-ledger`
- Jobs-to-be-done framing: `job-to-be-done-map`
- Competitive or market comparison: `market-landscape-scan`

### Metrics And Prioritization

- Metric tree or North Star metric: `metric-architecture`
- Product health review: `product-health-diagnostic`
- Retention review: `retention-diagnostic`
- Dashboard spec: `dashboard-decision-brief`
- Prioritization: `priority-decision-system`
- Experiment design: `learning-experiment-plan`
- Pricing and packaging: `pricing-packaging-brief`

### Delivery And Launch

- Delivery or sprint plan: `delivery-commitment-map`
- Sprint kickoff: `sprint-kickoff-brief`
- Retro synthesis: `retrospective-insight-brief`
- Design or implementation handoff: `handoff-readiness-brief`
- Launch readiness: `launch-readiness-review`
- Launch checklist: `launch-control-checklist`
- Market activation or go-to-market plan: `market-activation-plan`

### PRINCE2

- Which documents or management products are needed: `prince2-documentation-map`
- Starting Up a Project: `prince2-startup-brief`
- Initiating a Project: `prince2-initiation-pack`
- Directing a Project or project board decision: `prince2-direction-gate-brief`
- Controlling a Stage: `prince2-stage-control-pack`
- Managing Product Delivery: `prince2-product-delivery-pack`
- Managing a Stage Boundary: `prince2-stage-boundary-pack`
- Closing a Project: `prince2-closure-pack`

### Team Rituals And Team Building

- Workshop planning: `workshop-runbook`
- Team offsite: `team-offsite-agenda`
- Interview plan and hiring scorecard: `role-interview-kit`
- New team member onboarding: `team-onboarding-plan`

## Sequencing Guidance

If the request needs more than one skill, use the smallest useful sequence:

- New product idea: `assumption-risk-ledger` -> `discovery-conversation-guide` -> `product-requirements-blueprint`
- Messy project: `delivery-status-brief` -> `priority-decision-system` -> `delivery-commitment-map`
- Launch planning: `launch-readiness-review` -> `launch-control-checklist` -> `market-activation-plan`
- Governed PRINCE2 project: `prince2-documentation-map` -> the relevant phase skill
- Hiring a role: `role-interview-kit` -> `team-onboarding-plan`

## Output

When routing, respond with:

- Recommended skill
- Why that skill fits
- Any second skill to run next
- The first question or input needed

Keep it short unless the user asks for a full plan.

