---
name: graphic-design-planner
type: planner
description: "Plan graphic assets and campaign systems — visual direction, brand alignment, deliverables."
version: 0.1.0
---

# Graphic Design Planner Skill

Plan graphic deliverables before production work begins.

## JTBD (Jobs To Be Done)

### Primary Job
When I need to produce graphic assets or a campaign system but the visual direction, format requirements, and production specs are not yet settled,
I want a concrete graphic design direction and production plan before asset creation begins,
so I can avoid the expensive cycle of revising half-finished work when brand requirements, channel specs, or export rules surface too late.

### Secondary Jobs
- When a campaign spans multiple channels and formats, I want asset matrix, dimension specs, and export rules defined up front, so I can hand off files that don't require production rework.
- When stakeholders disagree on visual direction or brand application, I want the tradeoffs between concept options made explicit and decided before design work begins, so I can stop iterating on undecided direction.
- When a graphic-design-critic review returned REVISE or REJECT findings, I want a structured remediation plan that addresses hierarchy, legibility, or brand gaps, so I can close the specific defects rather than guessing what to fix.

### Job Layers
- Functional: Turn brand constraints, channel requirements, and content goals into an executable graphic design direction with named visual direction, asset matrix, production specs, and handoff package definition.
- Emotional: Reduce the fear of delivering files that look polished on screen but fail in print, export incorrectly at scale, or violate brand requirements discovered at the last stage.
- Social: Helps the user present a defensible production plan to creative directors, brand leads, and channel owners before expensive design work starts.

### This Skill Is For
- A designer or creative lead about to produce campaign visuals, social asset packs, infographics, or presentation graphics who needs brand-aligned specs and a production plan before the first file is opened.
- A team with conflicting channel requirements (print bleed vs. screen color profiles vs. social crop zones) who needs one agreed production direction.
- A designer recovering from a graphic-design-critic REVISE or REJECT verdict who needs a structured fix plan addressing the specific gaps found.

### This Skill Is NOT For
- A user with finished graphic assets who needs a quality verdict; use `graphic-design-critic` instead.
- A user looking for quick ad hoc tips with no real planning or scope-setting problem.

### Paired With
- `graphic-design-critic`: After the graphic asset or campaign system exists, use it to audit the result and surface real risks.
- `design-partner`: Use this when the unresolved problem is more about broader design direction before production-specific planning.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Has requirements but no visual direction or production specs | The skill defines concept direction, asset matrix, channel specs, and export rules | A production-ready plan with named visual direction and handoff package definition |
| Has multi-channel or multi-stakeholder conflicts | The skill makes format, color, and brand tradeoffs explicit and sets decision checkpoints | Agreed production direction with documented tradeoffs |
| Has failed graphic-design-critic findings | The skill converts hierarchy, legibility, or brand gaps into remediation tasks | A targeted fix plan with evidence-linked remediation steps |

### When to Escalate
- If the user already has finished or near-finished assets and needs a quality verdict, escalate to `graphic-design-critic`.
- If the user's unresolved problem is primarily about setting broader design concept or creative direction before production planning, escalate to `design-partner`.

## Use When
- Designing campaign visuals, social assets, infographics, or presentation graphics
- Defining brand-consistent visual systems for non-UI deliverables
- Planning asset packs across channels and formats

## MCP Baseline
- Figma MCP for source components/tokens and review context
- Pencil MCP for composition iteration
- Playwright MCP when validating graphics embedded in web contexts

## Shared Research Reference
Apply the shared research-backed workflow before producing a plan:
`design-skills/shared-design-core/.claude/skills/shared-design-core/references/research-backed-design-workflow.md`

## Research-Backed Planning Preflight
Before Phase 1:
- Build a `Reference Inventory` from brand sources, prior assets, user examples, public research-only references, channel specs, style vocabulary, anti-patterns, and missing evidence.
- Read DESIGN.md and DESIGN_MEMORY.md when present. Preserve token names, visual rationale, source provenance, and rejected directions unless the user requests a change.
- Capture `Design Memory Notes` for durable concept, typography, color, layout, asset-system, and export decisions.
- Translate inspiration into local principles. Do not copy public reference assets, branded styles, screenshots, or prompt bodies into the deliverable.
- Keep evaluation assumptions local-first: legibility checks, crop/safe-zone checks, contrast checks, export validation, and no Anthropic API for benchmark execution unless explicitly overridden by the user.

## Planning Protocol
1. Scope & Context (audience, channel, reference inventory, style vocabulary, anti-patterns, non-goals)
2. Existing Architecture Analysis (brand system, prior assets, DESIGN.md/DESIGN_MEMORY.md continuity, constraints)
3. Graphic Domain Design
- concept direction, hierarchy, typography/color system, asset matrix (formats/sizes), State Matrix for production/review states, accessibility checks
4. Assumption Register
5. Test Strategy (legibility, format validation, channel simulation)
6. Implementation Tasks
7. Review Checkpoint Plan

## Executor Routing Decision Matrix

After defining the asset matrix and visual direction, determine which executor backend should generate each asset. Apply these signals:

| Signal | Route To | Reason |
|--------|----------|--------|
| Social media graphics (Instagram, LinkedIn, Twitter/X) | `gemini-image-executor` | Atmospheric quality, platform-ready PNG |
| Event posters, flyers | `gemini-image-executor` | Organic depth, visual richness |
| Hero/marketing images | `gemini-image-executor` | Natural atmosphere, dimensional feel |
| Product feature showcases | `gemini-image-executor` | Atmospheric backgrounds, organic gradients |
| Data visualizations, statistical charts | `infographic-executor` | Data integrity, accessibility, editability |
| Brand guidelines, style sheets | `graphic-design-executor` | Precision, verifiable values, editability |
| Infographics with data claims | `infographic-executor` | Proportional accuracy, accessible text, citations |
| Icons, logos | `graphic-design-executor` | Scalability, vector precision |
| Reference documents, spec sheets | `graphic-design-executor` | Editability, systematic layout |
| Campaign sets (mixed channel) | SPLIT | Route each asset individually |

**Contested cases** (where both formats are viable) default to `gemini-image-executor` unless the task requires any of: data accuracy verification, accessibility compliance, post-generation editability, or scalability to arbitrary resolution. Any of those signals flip the default to `graphic-design-executor`.

## Hard Gates
- No plan without a Reference Inventory and Design Memory Notes section
- No plan without a named visual direction and rationale
- No plan without channel-specific asset specs (dimensions, format, export rules)
- No plan without contrast/legibility requirements
- No plan without handoff package definition
- No plan without an Executor Routing section
- No plan that copies public reference assets or branded visual systems

## Required Output Contract
Use these top-level headings exactly:
- `## Scope & Context`
- `## Existing Architecture Analysis`
- `## Graphic Domain Design`
- `## Reference Inventory`
- `## Design Memory Notes`
- `## Assumption Register`
- `## Test Strategy`
- `## Implementation Tasks`
- `## Review Checkpoint Plan`
- `## Executor Routing`
- `## Contract Appendix`

### Executor Routing Section Format
```
## Executor Routing

**Recommended executor:** gemini-image-executor | graphic-design-executor | infographic-executor
**Rationale:** [1-2 sentences citing the deciding factor from the routing matrix]
**Override:** To use a different executor, state "use [executor name]" when invoking.
**Fallback:** If Gemini is unavailable (missing GOOGLE_API_KEY), fall back to graphic-design-executor.
```

For campaign sets with mixed channels, emit a per-asset routing table:
```
**Mixed campaign — per-asset routing:**
| Asset | Executor | Rationale |
|-------|----------|-----------|
| Instagram 1:1 card | gemini-image-executor | Atmospheric, platform-ready |
| Brand guideline page | graphic-design-executor | Precision, editability |
```

Inside `## Contract Appendix`, include:
- `### Architecture Overview`
- `### State Matrix`
- `### Source/Provenance Notes`
- `### Implementation Tasks`
- `### Failure Modes`
