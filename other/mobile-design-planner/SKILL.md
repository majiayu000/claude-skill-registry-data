---
name: mobile-design-planner
type: planner
description: "Plan mobile app flows — screen architecture, gestures, platform conventions, offline support."
version: 0.1.0
---

# Mobile Design Planner Skill

Plan mobile UI architecture before coding. Emphasize platform fit, interaction ergonomics, and resilient state behavior.

## JTBD (Jobs To Be Done)

### Primary Job
When I need to design a mobile app flow or screen system but platform conventions, navigation model, and gesture interactions are not yet decided,
I want a mobile-specific design plan before implementation begins,
so I can close the gap between screens that look right in Figma and an experience that feels wrong in hand — because touch targets are too small, gestures conflict with platform defaults, or the navigation model fights iOS or Android conventions.

### Secondary Jobs
- When the app needs to ship on both iOS and Android, I want platform-convention differences documented and shared-abstraction decisions made up front, so I can avoid building a single design that violates both platforms' expectations.
- When flows involve offline states, degraded connectivity, or error recovery, I want those states planned in the design before implementation, so engineers don't invent edge-case behavior that contradicts the intended experience.
- When a mobile-design-critic review returned REVISE or REJECT findings, I want a structured remediation plan targeting the specific platform-fit, ergonomics, or navigation gaps identified, so I can fix the actual failure modes rather than surface-level polish.

### Job Layers
- Functional: Turn product requirements into a mobile design plan with explicit navigation model, iOS/Android convention notes, touch-target and ergonomics requirements, gesture model, dynamic type support, and offline/error state strategy before any screens are built.
- Emotional: Reduce the fear that a flow will pass design review looking polished but feel unnatural in users' hands — gestures that conflict with back navigation, tap targets that require two attempts, or text that breaks layout when accessibility font sizes are enabled.
- Social: Helps the designer or product team demonstrate platform expertise to iOS/Android engineers, product leads, and accessibility reviewers before implementation commits.

### This Skill Is For
- A designer or product team starting a mobile app flow, screen system, or navigation refactor who needs platform conventions, gesture model, and state coverage settled before Figma screens are handed to engineers.
- A team building for both iOS and Android who needs explicit platform-variant decisions and shared abstraction boundaries defined before implementation diverges.
- A designer recovering from a mobile-design-critic REVISE or REJECT verdict who needs a structured fix plan addressing the specific platform-fit, ergonomics, or accessibility gaps found.

### This Skill Is NOT For
- A user with existing mobile flows or screens who needs a quality verdict; use `mobile-design-critic` instead.
- A user looking for quick ad hoc tips with no real planning or scope-setting problem.

### Paired With
- `mobile-design-critic`: After the mobile app flow or screen system exists, use it to audit the result and surface real risks.
- `design-partner`: Use this when the unresolved problem is more about setting broader visual direction before mobile-specific planning.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Has requirements but no platform-fit plan or navigation model | The skill defines navigation model, platform conventions, gesture model, state coverage, and ergonomics requirements | A platform-ready mobile design plan ready for implementation |
| Needs to ship on both iOS and Android | The skill documents platform-convention differences and shared-abstraction decisions | Platform variant plan with documented divergence boundaries |
| Has failed mobile-design-critic findings | The skill converts platform-fit, ergonomics, or navigation gaps into targeted remediation tasks | A fix plan with evidence-linked remediation steps and platform-convention grounding |

### When to Escalate
- If the user already has implemented or designed screens and needs a platform-fit quality verdict, escalate to `mobile-design-critic`.
- If the user's unresolved problem is primarily about setting broader visual direction before mobile-specific planning, escalate to `design-partner`.

## Use When
- Designing iOS/Android/RN app screens and navigation
- Planning new mobile flows or refactors
- Translating mobile mocks to implementation tasks
- Defining platform-specific variants and shared abstractions

## MCP Baseline
- Figma MCP for mobile design source context
- Playwright MCP (or equivalent mobile viewport automation) for behavior targets
- Pencil MCP for rapid screen and flow prototyping

## Shared Research Reference
Apply the shared research-backed workflow before producing a plan:
`design-skills/shared-design-core/.claude/skills/shared-design-core/references/research-backed-design-workflow.md`

## Research-Backed Planning Preflight
Before Phase 1:
- Build a `Reference Inventory` from project-local mobile patterns, user examples, public research-only references, platform guidelines, style vocabulary, anti-patterns, and missing evidence.
- Read DESIGN.md and DESIGN_MEMORY.md when present. Preserve existing token names, rationale, and rejected directions unless the user requests a change.
- Capture `Design Memory Notes` for durable navigation, gesture, platform, visual, token, and state decisions.
- For assistant/agent mobile surfaces, include an AG-UI-inspired state model: visible status, generated UI regions, tool invocation affordances, user confirmation points, cancellation, retry, and error recovery.
- Keep evaluation assumptions local-first: device/viewport simulation, accessibility and dynamic type checks, and no Anthropic API for benchmark execution unless explicitly overridden by the user.

## Planning Protocol
1. Scope & Context (audience, device context, key jobs-to-be-done, reference inventory, style vocabulary, anti-patterns)
2. Existing Architecture Analysis (navigation, component patterns, technical stack, DESIGN.md/DESIGN_MEMORY.md continuity)
3. Mobile Domain Design
- navigation model, platform conventions, gesture model, State Matrix, offline/degraded behavior, accessibility model
4. Assumption Register (fragility-rated)
5. Test Strategy (unit/integration/e2e/device matrix)
6. Implementation Tasks (ordered with dependencies)
7. Review Checkpoint Plan (mobile-design-critic + ui-critic)

## Hard Gates
- No plan without a Reference Inventory and Design Memory Notes section
- No plan without iOS/Android convention notes
- No plan without touch-target and one-hand ergonomics considerations
- No plan without dynamic type / text scaling requirements
- No plan without error/offline state strategy
- No agentic mobile plan without visible status, generated UI region, user control/recovery, and trust boundary decisions

## Required Output Contract
Use these top-level headings exactly:
- `## Scope & Context`
- `## Existing Architecture Analysis`
- `## Mobile Domain Design`
- `## Reference Inventory`
- `## Design Memory Notes`
- `## Assumption Register`
- `## Test Strategy`
- `## Implementation Tasks`
- `## Review Checkpoint Plan`
- `## Contract Appendix`

Inside `## Contract Appendix`, include:
- `### Architecture Overview`
- `### State Matrix`
- `### Source/Provenance Notes`
- `### Implementation Tasks`
- `### Failure Modes`
