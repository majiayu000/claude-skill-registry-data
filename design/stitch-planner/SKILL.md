---
name: stitch-planner
type: planner
description: "Generate UI screens and multi-page prototypes using Stitch with design system documentation."
version: 0.1.0
---

# Stitch Planner Skill

Plan and orchestrate Google Stitch prototyping workflows. Turn design direction or raw user intent into Stitch screen generation plans, design system extraction, and component export strategies.

## JTBD (Jobs To Be Done)

### Primary Job
When I have a design direction or rough UI concept but need rapid visual prototypes before committing to implementation,
I want a structured plan that leverages Google Stitch's AI screen generation to produce high-fidelity prototypes,
so I can validate visual direction, page flow, and component patterns before any code is written.

### Secondary Jobs
- When I need to generate a multi-page website prototype from a single design brief, I want a Stitch loop plan that sequences screen generation with consistent design tokens, so I get a coherent multi-page prototype rather than disconnected screens.
- When I have Stitch-generated screens and need to extract a reusable design system, I want a design-md extraction plan, so the design decisions are documented and machine-readable for downstream executors.
- When a design-partner direction exists and I need to bridge the gap to implementation, I want Stitch prototypes that embody the design direction, so I can hand off concrete visuals to web-design-executor rather than abstract descriptions.

### Job Layers
- Functional: Turn design intent into a sequenced plan of Stitch MCP operations (prompt enhancement, screen generation, design system extraction, optional component export) with quality gates between each phase.
- Emotional: Reduce the anxiety of going from abstract design direction to concrete visuals by providing rapid, AI-generated prototypes that can be iterated on before committing to code.
- Social: Helps designers and product leads show stakeholders tangible prototypes early, building confidence and alignment before expensive implementation begins.

### This Skill Is For
- A designer or product team with a design direction (from design-partner or their own brief) who needs rapid visual prototypes before implementation.
- A team wanting to generate a multi-page website prototype from a single concept using Stitch's AI screen generation.
- A team that needs to extract and document a design system from generated or existing Stitch screens.

### This Skill Is NOT For
- A user who already has implemented code and needs a quality review; use `web-design-critic` instead.
- A user who needs to set aesthetic direction from scratch with no design constraints; use `design-partner` first.
- A user who needs production-ready HTML/CSS code; use `web-design-executor` after prototyping.

### Paired With
- `jtbd-interviewer`: Far upstream -- JTBD switching-story interviews can surface the user needs and struggling moments that inform the design brief fed to design-partner or directly to stitch-planner.
- `design-partner`: Upstream -- provides design direction input (visual thesis, typography, color, spatial approach) that feeds into Stitch prompt enhancement.
- `web-design-executor`: Downstream -- consumes the Stitch prototype and design system docs to generate production HTML/CSS. Primary executor for general web targets.
- `infographic-executor`: Downstream (parallel) -- can consume Stitch-generated visual direction for SVG infographic deliverables.
- `web-design-critic`: Downstream -- reviews Stitch-generated screens or the resulting implementation for responsive, interaction, and hierarchy quality.
- `graphic-design-planner`: Parallel -- for static graphic deliverables that complement Stitch-generated interactive screens.
- stitch-kit framework executors (external): `stitch-nextjs-components`, `stitch-svelte-components`, `stitch-react-native-components`, `stitch-swiftui-components` -- alternative downstream executors when the target framework is not general web HTML/CSS.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Has design direction, needs visual prototypes | Stitch-planner sequences prompt enhancement + screen generation | Stitch-generated screens + generation plan |
| Needs multi-page prototype from single concept | Stitch-planner plans a stitch-loop workflow with page sequencing | Coherent multi-page prototype + design system docs |
| Has Stitch screens, needs design system extraction | Stitch-planner plans design-md extraction workflow | DESIGN.md with tokens, patterns, component inventory |
| Has Stitch prototype, needs implementation handoff | Stitch-planner plans component export + executor handoff | React components or structured spec for web-design-executor |

### When to Escalate
- If the user needs aesthetic direction before prototyping, escalate to `design-partner`.
- If the user has production code to review, escalate to `web-design-critic`.
- If the Stitch MCP server is unavailable, degrade gracefully: document the intended Stitch workflow as a spec and suggest `web-design-executor` as the implementation path.

## Use When
- Rapid UI prototyping with AI-generated screens
- Multi-page website prototype generation
- Design system extraction from visual prototypes
- Bridging design-partner direction to implementation-ready visuals
- Exploring visual variations before committing to code

## MCP Dependency
- **Stitch MCP** (required): Screen generation, prompt enhancement, design-md extraction
- **Figma MCP** (optional): Import existing design tokens to inform Stitch prompts
- **Playwright MCP** (optional): Verify generated screens at multiple viewports

## Shared Research Reference
Apply the shared research-backed workflow before producing a Stitch plan:
`design-skills/shared-design-core/.claude/skills/shared-design-core/references/research-backed-design-workflow.md`

## Stitch Access And Provenance Guardrails
- Treat Stitch as an account-backed Google design tool. Use it only when the user has access, MCP is configured, and the workflow is explicitly in scope.
- Do not use Stitch, stitch-kit, or public Stitch examples as a shortcut around source provenance. Record what each generated screen, exported component, or DESIGN.md section came from.
- Stitch and stitch-kit references are planning/prototyping inputs, not copied skill bodies. Do not vendor external prompt text into this repository.
- Keep benchmark and hardening evaluation local-first through Codex/local tooling. Do not use Anthropic API, SDK calls, or `ANTHROPIC_API_KEY` for benchmark execution unless explicitly overridden by the user.

## External Skill References (No Copy Policy)

This skill references two external Stitch skill repositories. Do not copy external skill body content into this repository. Use manifest IDs/URLs and pinned commit metadata for traceability. If a referenced skill is unavailable at runtime, continue with local planning fallback and state the limitation.

- Canonical reference file: [stitch-skills-manifest.yaml](references/stitch-skills-manifest.yaml)

### Official: google-labs-code/stitch-skills (7 skills)

| Skill | Purpose | When Used |
|-------|---------|-----------|
| `enhance-prompt` | Transform rough UI ideas into optimized Stitch prompts | Phase 2 (always) |
| `stitch-design` | Unified prompt enhancement + screen generation | Phase 3 (single screens) |
| `stitch-loop` | Multi-page website generation from single prompt | Phase 3 (multi-page) |
| `design-md` | Extract design system documentation from Stitch projects | Phase 4 (always) |
| `react-components` | Convert Stitch screens to React component systems | Phase 5 (optional, React targets) |
| `remotion` | Walkthrough video generation | v2 (deferred) |
| `shadcn-ui` | shadcn/ui component integration | v2 (deferred) |

### Community: gabelul/stitch-kit (35 skills, 5 layers)

stitch-kit wraps the official skills with additional capabilities. Prefer stitch-kit equivalents when available, as they add MCP ID format safety, batch generation, and accessibility auditing that the official skills lack.

| Skill | Purpose | Replaces/Extends |
|-------|---------|-----------------|
| `stitch-ideate` | Design research + trend analysis + direction proposals | New (no official equivalent) |
| `stitch-orchestrator` | End-to-end workflow coordination with routing | New (our planner adds feedback loop) |
| `stitch-ui-prompt-architect` | Two-mode prompt enhancement | Extends `enhance-prompt` |
| `stitch-mcp-*` (14 wrappers) | ID-format-safe MCP API wrappers | Wraps all Stitch MCP tools |
| `stitch-a11y` | WCAG 2.1 AA auditing + auto-fixes | New (critical gap fill) |
| `stitch-design-md` | Enhanced design documentation with system notes | Extends `design-md` |
| `stitch-design-system` | Token extraction to CSS custom properties | Extends `design-md` |
| `stitch-nextjs-components` | Next.js 15 server/client component export | New framework target |
| `stitch-svelte-components` | Svelte 5 runes + scoped styling export | New framework target |
| `stitch-react-native-components` | React Native/Expo export | New framework target |
| `stitch-swiftui-components` | SwiftUI iOS 16+ export | New framework target |

### Routing Priority

When both official and stitch-kit skills cover the same capability:
1. Prefer stitch-kit wrappers for MCP operations (ID format safety)
2. Prefer stitch-kit `stitch-a11y` over manual a11y review planning
3. Prefer official `stitch-design`/`stitch-loop` if stitch-kit is unavailable
4. Always load max 3 external skills per phase (same as design-partner policy)

## Design Direction Input (Optional)
If `design-partner` was invoked first, accept its structured output:
- Visual thesis (mood, material, energy)
- Typography rationale and font pairing
- Color strategy and palette
- Spatial approach and anti-generic commitments
- Motion intent

When present, weave design direction into the prompt enhancement phase so Stitch screens embody the intended aesthetic.

## Planning Protocol

### Phase 1: MCP Availability Gate
- Detect whether Stitch MCP server is available.
- **If available:** Proceed to Phase 2.
- **If unavailable:** Produce a Stitch workflow spec document describing the intended prompts, screen sequence, and design system extraction plan. Recommend `web-design-executor` as the alternative implementation path. STOP — do not proceed with Stitch-specific planning.
- Detect optional MCPs (Figma, Playwright) and note their availability for downstream phases.

### Phase 2: Scope & Prompt Strategy
- Define the prototyping objective: single screen, multi-page site, or design system extraction.
- Build a `Reference Inventory` from project-local sources, user examples, public research-only references, style vocabulary, anti-patterns, and missing evidence.
- Read DESIGN.md and DESIGN_MEMORY.md when present. Preserve prior token names, rationale, rejected directions, and system constraints unless the user asks to change them.
- Identify target audience, key pages/screens, interaction patterns, and constraints.
- If `jtbd-interviewer` output exists, extract user struggling moments, desired outcomes, and job statements to ground the prototyping brief in real user needs.
- If `design-partner` direction exists, extract visual thesis, typography, color, and spatial approach.
- Draft enhanced prompts using `enhance-prompt` conventions:
  - Specific visual language (not "modern" or "clean" — name the aesthetic)
  - Component-level descriptions (hero, nav, card patterns, CTAs)
  - Responsive intent (mobile-first? desktop-first? specific breakpoints?)
  - Brand constraints (colors, fonts, imagery style)
- If the prototype includes assistant or agent workflows, include visible status, generated UI regions, tool invocation affordances, confirmation points, cancellation, retry, error recovery, and trust boundaries.
- Record assumptions in the Assumption Register.

### Phase 3: Screen Generation Plan
- **Single screen path** (`stitch-design`):
  - Plan one enhanced prompt per screen.
  - Define acceptance criteria: what makes the screen "good enough" to proceed?
  - Plan iteration strategy: how many variations to generate, what to vary.
- **Multi-page path** (`stitch-loop`):
  - Define page inventory and navigation structure.
  - Plan the single master prompt that drives consistent multi-page generation.
  - Define per-page acceptance criteria and cross-page consistency checks.
  - Specify shared design tokens that must persist across pages.
- Define quality gate: review generated screens against design direction before proceeding.

### Phase 4: Design System Extraction Plan
- Plan `design-md` extraction from generated screens.
- Define what the DESIGN.md should capture: color tokens, typography scale, spacing system, component patterns, interaction states.
- Specify how extracted tokens map to the project's existing design system (if any).
- Plan validation: cross-check extracted tokens against design-partner direction.
- Plan a DESIGN_MEMORY.md entry for durable visual, token, component, prompt, or rejected-direction decisions introduced by the Stitch loop.

### Phase 5: Component Export & Handoff Plan (Optional)
- Route to the correct downstream executor based on target framework:
  - **General web (HTML/CSS)** → `web-design-executor` (internal) — primary path for production-ready markup
  - **React (Vite)** → `react-components` (official) or stitch-kit `stitch-react-components` (enhanced)
  - **Next.js** → stitch-kit `stitch-nextjs-components` (server/client split, next-themes)
  - **Svelte** → stitch-kit `stitch-svelte-components` (runes API, scoped styling)
  - **React Native/Expo** → stitch-kit `stitch-react-native-components` (safe areas, platform conventions)
  - **SwiftUI** → stitch-kit `stitch-swiftui-components` (iOS 16+, environment integration)
  - **SVG infographics** → `infographic-executor` (internal) — when Stitch screens inform static visual deliverables
- Define handoff artifact format:
  - Screen references (which Stitch screens to implement)
  - Design token mapping (DESIGN.md → CSS custom properties or framework-specific tokens)
  - Component responsibility map
  - Responsive behavior notes from Stitch screens
  - Target framework and build system constraints
- Plan critic review checkpoint: when to invoke `web-design-critic` (web targets) or `mobile-design-critic` (React Native/SwiftUI targets).

### Phase 6: Assumption Register
- List all assumptions with fragility ratings (VERIFIED / REASONABLE / FRAGILE).
- Key assumption categories:
  - Stitch MCP capabilities and version
  - Design direction stability (will the visual thesis change?)
  - Target framework and build system
  - Responsive requirements beyond what Stitch generates
  - Accessibility requirements (Stitch screens may not be WCAG-compliant)

### Phase 7: Review Checkpoint Plan
- Define when to invoke `web-design-critic` on Stitch output.
- Define when to invoke `ui-critic` for interaction quality.
- Define when to invoke `a11y-critic` (Stitch screens need accessibility review before production).
- Plan iteration: if critic returns REVISE, what's the re-prompting strategy?

## Hard Gates
- No plan without MCP availability check (Phase 1)
- No plan without Reference Inventory, Source/Provenance Notes, and Design Memory Notes
- No screen generation without enhanced prompts (vague prompts produce generic screens)
- No handoff to executor without design system extraction (DESIGN.md must exist)
- No production use of Stitch screens without accessibility review checkpoint
- If design-partner direction exists, it must be reflected in enhanced prompts — do not ignore upstream direction
- No agentic interface prototype without visible status, generated UI region, user control/recovery, and trust boundary decisions

## Required Output Contract
Use these top-level headings exactly:
- `## MCP Availability Assessment`
- `## Scope & Prompt Strategy`
- `## Reference Inventory`
- `## Screen Generation Plan`
- `## Design System Extraction Plan`
- `## Design Memory Notes`
- `## Component Export & Handoff Plan`
- `## Assumption Register`
- `## Review Checkpoint Plan`
- `## Contract Appendix`

Inside `## Contract Appendix`, include:
- `### Stitch Workflow Summary` (sequenced list of MCP operations)
- `### Handoff Artifacts` (what downstream skills receive)
- `### Source/Provenance Notes` (what came from project sources, user references, Stitch output, or research-only inspiration)
- `### Failure Modes` (what breaks if assumptions are wrong)
