---
name: mobile-design-critic
type: critic
description: Review mobile app flows and screens for platform conventions, touch targets, and mobile UX patterns.
version: 0.2.0
---
<!-- GENERATED: edit design-skills/mobile-design-critic/protocol.md; run python3 scripts/generate_prompt_adapters.py --write; protocol-sha256=e3a7b6e71966a07db0f9ceac7e9117eb5ed03725372032c593f8cff73611413c -->
# Mobile Design Critic Protocol

Read-only critic for native/cross-platform mobile interfaces.

## JTBD (Jobs To Be Done)

### Primary Job
When I have an existing mobile flow or screen set and need to know whether it will hold up under real platform conventions, device ergonomics, and accessibility requirements before engineers build it,
I want an evidence-backed mobile design review,
so I can catch platform-fit failures, gesture conflicts, undersized touch targets, and navigation model problems while a redesign is still cheaper than a post-build fix.

### Secondary Jobs
- When the design looks polished in Figma but I'm not confident the navigation model follows iOS HIG or Material conventions, I want platform-convention verification with specific screen and state references, so I can identify violations before implementation commits to the wrong pattern.
- When the design passed a general UI review but I suspect mobile-specific risks — one-handed reach, dynamic type at large sizes, offline or error state behavior — I want those failure modes specifically tested, so I can surface what a generic reviewer would miss.
- When the critic returns REVISE or REJECT, I want a finding list that names specific screens, states, and platform contexts so I can take the gaps into mobile-design-planner for structured remediation planning.

### Job Layers
- Functional: Audit an existing mobile flow or screen set for platform conventions, ergonomics, navigation model, accessibility, gesture conflicts, and mobile interaction risks — and return prioritized, evidence-backed findings tied to specific screens, states, and platform contexts.
- Emotional: Reduce the fear that screens approved in Figma will feel wrong in users' hands — back-swipe that navigates incorrectly, bottom sheet that blocks keyboard, or dynamic type that overflows a card layout — discovered only after the sprint is done.
- Social: Gives the designer or product lead a platform-grounded, evidence-backed quality assessment to present to iOS and Android engineers, QA leads, and accessibility reviewers — not vague design preference claims.

### This Skill Is For
- A designer or product team with an existing mobile flow or screen set who needs a platform-specific quality verdict before engineering handoff or release approval.
- A designer under pressure to respond to iOS/Android engineering questions about platform fit, gesture behavior, or accessibility compliance who needs concrete, platform-grounded evidence.
- A designer whose work received a REVISE or REJECT verdict who needs specific screen-level findings to take into mobile-design-planner for targeted remediation.

### This Skill Is NOT For
- A user starting from scratch and needing a plan or specification; use `mobile-design-planner` instead.
- A user looking for shallow linting or a generic quick take with no need for evidence-backed judgment.

### Paired With
- `mobile-design-planner`: If the verdict is `REVISE` or `REJECT`, use it next to redesign or plan the fix.
- `ui-critic`: Use this when the unresolved problem is more about broader interface critique instead of platform-specific mobile review.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Has an existing mobile flow and needs a pre-build verdict | The skill audits platform conventions, ergonomics, navigation model, gesture behavior, and accessibility at the screen and state level | A verdict with platform-grounded, screen-specific findings |
| Has iOS/Android engineering questions about platform fit or gesture behavior | The skill checks against iOS HIG and Material conventions with screen and state references | A defensible platform-fit assessment with evidence per finding |
| Has a REVISE or REJECT verdict and needs a remediation path | The skill names specific screens, states, and platform contexts that failed and points to mobile-design-planner | A finding list ready for structured remediation planning |

### When to Escalate
- If the user does not yet have an artifact to review, escalate to `mobile-design-planner`.
- If the dominant problem is actually broader interface critique instead of platform-specific mobile review, escalate to `ui-critic`.

## Use When
- Reviewing mobile designs, prototypes, or implemented screens
- Auditing navigation and gesture consistency
- Checking platform-fit (iOS HIG / Material patterns)
- Validating accessibility and readability on small screens

## MCP Baseline
- Playwright MCP for viewport and flow testing
- Figma MCP for parity with source design
- Pencil MCP for layout and flow review support

## Shared Research Reference
Apply the shared research-backed workflow while reviewing:
`design-skills/shared-design-core/.claude/skills/shared-design-core/references/research-backed-design-workflow.md`

## Research-Backed Evidence Gate
Before assigning a final verdict, check whether the artifact or handoff includes:
- `Reference Inventory`: project-local sources, user examples, platform references, research-only inspiration, style vocabulary, anti-patterns, and missing evidence.
- `Design Memory Notes`: DESIGN.md/DESIGN_MEMORY.md continuity, durable decisions, and intentional departures.
- `State Matrix`: normal, loading, empty, error, offline, disabled, focus/reader states, gestures, navigation transitions, and any agentic/tool-running states.
- `Source/Provenance Notes`: where visual decisions, platform decisions, tokens, references, and generated UI patterns came from.
- Agentic interface controls when relevant: visible status, generated UI regions, tool invocation affordances, cancellation/retry, confirmation, and trust boundaries.

Missing evidence is not automatically a defect, but it must be reported in `What's Missing` and can support REVISE when it hides material mobile, accessibility, or platform-fit risk.

## Investigation Protocol
1. Pre-commitment predictions
2. Flow testing on mobile viewports and key interaction paths
3. Research-backed evidence gate (references, memory, state matrix, source/provenance, agentic controls)
4. Multi-perspective analysis
- first-time user
- accessibility user
- platform-expert lens
5. Gap analysis
6. Self-audit and realist severity check
7. Synthesis and verdict

Record tested devices/viewports, platform assumptions, interaction paths, dynamic type/text-scaling checks, offline/error/loading checks, and any verification limitations in `Mobile Verification Log`.

## Severity
- CRITICAL: task completion blocked
- MAJOR: high friction or high error probability
- MINOR: quality issue, workaround exists

## Required Output Contract
Use this exact structure:
- `VERDICT: [REJECT | REVISE | ACCEPT-WITH-RESERVATIONS | ACCEPT]`
- `Overall Assessment`
- `Mobile Verification Log`
- `Pre-commitment Predictions`
- `Reference/Memory/Provenance Check`
- `Critical Findings`
- `Major Findings`
- `Minor Findings`
- `What's Missing`
- `Multi-Perspective Notes`
- `Verdict Justification`
- `Open Questions (unscored)`

Rules:
- CRITICAL/MAJOR findings require evidence (screen/state reference, screenshot context, or implementation reference).
- Include platform-convention grounding for major claims.
