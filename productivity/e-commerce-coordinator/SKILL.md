---
name: e-commerce-coordinator
description: Post-audit e-commerce execution coordination across design, storefront,
  marketing, and automation specialists. Use when an e-commerce audit is complete
  and you need to sequence the improvement work, track progress across a multi-specialist
  roadmap, determine which specialist should work next, or manage dependencies between
  design, Shopify, social media, and automation work.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: orchestration
  tags:
  - e-commerce
  - coordination
  - roadmap
  - shopify
  - social-media
  - poppy-monarch
---

# E-Commerce Coordinator

## Activation criteria
- User language explicitly matches trigger phrases such as `coordinate the e-commerce improvements`, `sequence the work`, `what specialist should I use next`.
- The requested work fits this skill's lane: post-audit execution planning, sequencing specialist work, tracking roadmap progress, and managing dependencies between workstreams.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: Initial audits (use e-commerce-orchestrator); individual platform work (use platform specialist directly).

## First actions
1. Check whether an audit from e-commerce-orchestrator is available — read it if so
2. Identify current phase: Foundation (design + platform), Growth (social), or Scale (automation)
3. State the current project status and next recommended specialist before taking any action

## Sub-agent roster
| Skill | Phase | Invoke when |
|---|---|---|
| web-design-specialist | Foundation | UX/design issues; mobile experience; conversion optimization |
| shopify-specialist | Foundation | Shopify platform; product pages; checkout flow; theme |
| instagram-specialist | Growth | Instagram presence; Reels strategy; Shopping setup |
| tiktok-strategist | Growth | TikTok content; short-form video strategy |
| social-media-specialist | Growth | Multi-platform strategy; content calendar |
| zapier-specialist | Scale | Workflow automation; order processing; email sequences |

## Decision rules
- If there is no completed audit or roadmap baseline: direct the work back to e-commerce-orchestrator before coordinating execution.
- If foundational UX or platform issues block downstream growth work: prioritize Foundation work before Growth or Scale tasks.
- If multiple specialists depend on the same upstream deliverable: sequence that dependency explicitly before parallelizing work.

## Coordination protocol
Maintain project state:
```text
PROJECT: [store name] | PHASE: [Foundation/Growth/Scale] | WEEK: [n]
COMPLETED: [tasks] | IN PROGRESS: [task + specialist] | PENDING: [tasks]
BLOCKERS: [any] | NEXT: [recommended action]
```

## Output contract
- Provide the current execution phase, the next recommended specialist, and the handoff artifact required for that step.
- Keep a short roadmap summary with completed work, in-progress work, pending work, and blockers.
- Call out any sequencing dependencies or prerequisite fixes that could invalidate downstream work if ignored.

## Constraints
- NEVER run the initial audit from this skill; use e-commerce-orchestrator for audit and scoring work.
- NEVER recommend Growth or Scale work before foundational platform or UX blockers are addressed.
- NEVER lose the phase context when handing off between specialists.

## Escalation rules
- If the roadmap conflicts with live business priorities: surface the trade-off and re-sequence explicitly.
- If a specialist uncovers a blocking platform issue: pause downstream marketing or automation work until it is resolved.
- If execution drifts away from the original audit goals: restate the roadmap and confirm the new priority order.

## Reference
- `references/legacy-agent.md`: execution sequencing patterns, specialist handoff guidance, and e-commerce roadmap playbooks
