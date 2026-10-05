---
name: web-design-planner
type: planner
description: "Plan website/web app interfaces — layout, interaction, responsive design, component architecture."
version: 0.1.0
---

# Web Design Planner Skill

Plan web UI architecture before code. Focus on structure, responsive behavior, interaction models, and design-system alignment.

## JTBD (Jobs To Be Done)

### Primary Job
When I need to design a website or web app interface but the responsive structure, component responsibilities, and interaction states are not yet decided,
I want a web design architecture plan before implementation starts,
so I can avoid the gap between a desktop mockup that looks finished and a responsive design that breaks at real breakpoints or collapses under real interaction states.

### Secondary Jobs
- When a design system exists but no one has defined how it maps to this surface's components, tokens, and state behavior, I want that mapping specified before code is written, so the implementation doesn't invent inconsistent patterns mid-build.
- When stakeholders disagree about layout priorities across mobile, tablet, and desktop, I want breakpoint decisions and responsive tradeoffs documented, so I can stop resolving layout conflicts during development.
- When a web-design-critic review returned REVISE or REJECT findings, I want a structured remediation plan addressing the specific responsive, interaction, or hierarchy gaps found, so I can fix the real defects rather than patching symptoms.

### Job Layers
- Functional: Turn audience requirements and design-system constraints into a web design architecture plan with explicit breakpoint strategy, component responsibility map, state coverage (loading/empty/error), and interaction model before code is written.
- Emotional: Reduce the fear that the desktop mockup approved in Figma will look correct but behave inconsistently on real devices — with undefined hover states, collapsing layouts, and missing empty states discovered only in production.
- Social: Helps the designer or tech lead present a defensible responsive architecture to engineers, product managers, and design-system owners before implementation commits.

### This Skill Is For
- A designer or product team starting a new web page, app shell, or componentized surface who needs breakpoints, interaction patterns, and state behavior defined before any code is written.
- A team translating a Figma design to implementation tasks who needs a structured plan covering responsive behavior and design-system token usage, not just a visual spec.
- A designer recovering from a web-design-critic REVISE or REJECT verdict who needs a targeted remediation plan for responsive, accessibility, or interaction gaps.

### This Skill Is NOT For
- A user with an existing website or web app design who needs a quality verdict; use `web-design-critic` instead.
- A user looking for quick ad hoc tips with no real planning or scope-setting problem.

### Paired With
- `web-design-critic`: After the website or web app interface exists, use it to audit the result and surface real risks.
- `design-partner`: Use this when the unresolved problem is more about setting broader aesthetic direction before committing to web-specific structure.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Has requirements but no responsive structure or state plan | The skill defines breakpoints, component map, state coverage, and interaction model | An implementation-ready web design architecture plan |
| Has design system but no surface mapping | The skill specifies token usage, component responsibilities, and design-system alignment for this surface | A design-system-aligned implementation spec |
| Has failed web-design-critic findings | The skill converts responsive, interaction, or hierarchy gaps into targeted remediation tasks | A fix plan with evidence-linked remediation steps |

### When to Escalate
- If the user already has an implemented or designed artifact and needs a quality verdict, escalate to `web-design-critic`.
- If the user's unresolved problem is primarily about setting broader aesthetic direction before committing to web-specific structure, escalate to `design-partner`.

## Use When
- Designing new web pages, app shells, or componentized surfaces
- Refactoring layout or interaction architecture
- Translating Figma designs into implementation plans
- Defining responsive breakpoints, token usage, and state behavior before coding

## MCP Baseline
- Figma MCP: source-of-truth design context and token extraction
- Playwright MCP: behavior and viewport verification targets
- Pencil MCP: rapid layout prototyping and variable validation

## Shared Research Reference
Apply the shared research-backed workflow before producing a plan:
`design-skills/shared-design-core/.claude/skills/shared-design-core/references/research-backed-design-workflow.md`

## Design Direction Input (Optional)
If `design-partner` was invoked first, accept its structured output as input:
- Visual thesis (mood, material, energy in one sentence)
- Typography rationale and font pairing
- Color strategy and palette
- Spatial approach and anti-generic commitments

When design direction input is present, propagate it into the Compositional Design phase and the Design Token Table.

## Research-Backed Planning Preflight
Before Phase 1:
- Build a `Reference Inventory` covering project-local sources, user-provided examples, public research-only references, style vocabulary, anti-patterns, and missing evidence.
- Read DESIGN.md and DESIGN_MEMORY.md when present. Use them as the foundation for token, component, and rationale decisions; explicitly flag intentional departures.
- Capture `Design Memory Notes` for any durable visual, interaction, token, or layout decision the plan introduces.
- For assistant/agent interfaces, include an AG-UI-inspired state model: visible status, generated UI regions, tool invocation affordances, user confirmation points, cancellation, retry, and error recovery.
- Keep evaluation assumptions local-first: Codex/local browser checks, Playwright-compatible viewport verification, contrast checks, and no Anthropic API for benchmark execution unless explicitly overridden by the user.

## Planning Protocol
1. Scope & Context
- Define audience, objective, critical flows, constraints, and success criteria.
 - Include reference inventory, style vocabulary, anti-patterns, and non-goals.
2. Existing Architecture Analysis
- Inventory current component patterns, token system, CSS/layout approach, and known UX debt.
- **DESIGN.md integration**: If a DESIGN.md exists (check `./DESIGN.md`, `./docs/DESIGN.md`, `./.design/DESIGN.md`), read it and use its tokens as the foundation for your Design Token Table output. Map DESIGN.md color/typography/spacing tokens directly into the plan's token assignments. When design-partner direction and DESIGN.md both exist, design-partner direction takes precedence for aesthetic choices but DESIGN.md token values should be preserved unless the direction explicitly overrides them.
2.5. Compositional Design (required for marketing/landing pages, recommended for all)
- **Visual Thesis**: One sentence capturing mood, material, and energy (e.g., "Warm editorial confidence with generous whitespace and serif authority").
- **Page Composition Sequence**: Define each section's single job:
  | Section | Job (one word) | Dominant Element | Secondary Element |
  |---------|---------------|-----------------|-------------------|
  | Hero | Attract | Full-bleed image | Brand + headline + CTA |
  | Support | Prove | Social proof / feature | Supporting copy |
  | Detail | Explain | Product depth | Workflow / demo |
  | Final CTA | Convert | CTA group | Urgency / reassurance |
- **First-Viewport Composition**: The first viewport must function as a poster — brand identity unmistakable, one dominant visual element, scannable in under 3 seconds. Specify: dominant visual, text placement strategy, CTA position.
- **Motion Intent**: 0-3 intentional motions. For each: trigger (load/scroll/hover), element, effect (fade/slide/scale/parallax), duration. Or explicitly state "No motion required."
- **Image Requirements**: For each section needing imagery: aspect ratio, mood/subject, compositional role (hero anchor, supporting context, atmospheric), text-safe zone description.
- **Card Justification**: Cards are interaction containers, not default layout. If the plan includes card grids, justify: what interactive behavior does the card boundary enable? If none, use cardless layout.
3. Web Domain Design
- Produce IA map, component responsibility map, state map (loading/empty/error), responsive breakpoint plan, and interaction patterns. The component map should be informed by compositional decisions from Phase 2.5.
 - Include the full State Matrix for normal, loading, empty, error, disabled, focus, hover, active, and any agentic/tool-running states.
4. Assumption Register
- List assumptions with fragility ratings, risk if wrong, and mitigation.
5. Test Strategy
- Define unit/integration/e2e/a11y/visual tests tied to core flows.
6. Implementation Tasks
- Break into dependency-ordered tasks with explicit acceptance criteria.
7. Review Checkpoint Plan
- Define when to invoke web-design-critic, ui-critic, and a11y-critic.

## Hard Gates
- No plan without a Reference Inventory and Design Memory Notes section
- No plan without explicit breakpoint strategy (mobile/tablet/desktop/wide)
- No plan without state coverage for loading/empty/error
- No plan without accessibility requirements and keyboard flow definition
- No plan without measurable acceptance criteria per task
- No plan without explicit Critic Handoff naming which critic(s) should review which artifacts and when
- No agentic interface plan without visible status, generated UI region, user control/recovery, and trust boundary decisions
- For marketing/landing pages: no plan without Compositional Design phase (visual thesis, section jobs, first-viewport composition, motion intent)

## Compositional Litmus Checks (verify before producing Contract Appendix)
- Is brand/product unmistakable in first viewport?
- Is there one strong visual anchor per section?
- Can the page be understood by scanning headlines only?
- Does each section have exactly one job?
- Are cards actually necessary (or is cardless layout better)?
- Does specified motion improve hierarchy or atmosphere?
- Would the design feel premium if all decorative shadows were removed?

## Required Output Contract
Use these top-level headings exactly:
- `## Scope & Context`
- `## Existing Architecture Analysis`
- `## Web Domain Design`
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
- `### Critic Handoff`
- `### Implementation Tasks`
- `### Failure Modes`
