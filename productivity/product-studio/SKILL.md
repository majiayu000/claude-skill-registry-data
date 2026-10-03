---
name: product-studio
description: "Run a persistent product-and-design operating system for multi-session website, app, brand, and digital-product work. Use when ChatGPT should maintain durable design state across sessions or agents, organize research and decisions, coordinate Design Maestro and specialist skills, create or update a .design workspace, manage design territories and human decisions, run readiness/quality gates, and produce implementation handoffs without losing product rationale. JEV/TypeSafe AI and Firecrawl are optional accelerators, never hard dependencies."
---

# Product Studio

Operate as the persistent product/design system around a project. Maintain durable state, coordinate Design Maestro for creative direction, record important decisions, and keep research, brand, UX, content, QA, and implementation handoff aligned over time.

Product Studio is not a visual style and not a code generator. It is the project's design memory and operating model.

## Core relationship

Use **Product Studio** for persistence and lifecycle management.
Use **Design Maestro** for creative orchestration and design judgment.
Use specialist skills for domain depth.

```text
Product Studio (state + process)
        -> Design Maestro (creative direction)
                -> specialist skills
        -> Product Studio (record stable decisions)
```

If Design Maestro is unavailable, continue with the Product Studio workflow and apply the same product-first principles, but do not claim Design Maestro ran.

## Non-negotiable rules

1. Treat `.design/` as the durable source of truth for product/design decisions when a working directory exists.
2. Never replace approved decisions silently. Record meaningful changes in `DECISIONS.md`.
3. Do not dump chat transcripts into the workspace. Persist conclusions, evidence, rationale, constraints, and open questions.
4. Separate facts, assumptions, experiments, and approved decisions.
5. Preserve provenance for external research so future agents can verify it.
6. Keep product strategy, brand, UX, content, and implementation constraints connected.
7. Code is downstream of product/design decisions unless the user is explicitly working in an implementation phase.
8. JEV and Firecrawl are optional accelerators. Their absence must never block the workflow.
9. JEV can inform routing and readiness; it cannot become the creative authority.
10. Human/user decisions control irreversible or identity-level choices.
11. Read existing `.design/` state before proposing changes. Never assume a blank slate when project state exists.
12. Prefer small, explicit updates to the workspace after each meaningful phase.

## Workspace contract

When a working directory is available, use this project-local structure:

```text
.design/
├── BRIEF.md
├── PRODUCT.md
├── RESEARCH.md
├── BRAND.md
├── DESIGN.md
├── EXPERIENCE.md
├── CONTENT.md
├── DECISIONS.md
├── QA.md
├── HANDOFF.md
├── territories/
├── references/
└── reviews/
```

Use `scripts/init_design_workspace.py` to create missing files without overwriting existing work.

Read `references/design-state.md` for ownership and update rules.

## Startup procedure

### If `.design/` already exists

1. Read `BRIEF.md`, `PRODUCT.md`, `DESIGN.md`, `DECISIONS.md`, and `QA.md` first.
2. Read other files only as needed for the current task.
3. Identify current phase, approved decisions, open questions, and stale assumptions.
4. Continue from the existing state; do not restart discovery by default.

### If `.design/` does not exist

1. Initialize the workspace.
2. Seed `BRIEF.md` with known facts and assumptions.
3. Create the smallest useful product frame.
4. Continue into the appropriate workflow.

### If no writable working directory exists

Run in conversational mode. Keep the same mental model and produce a proposed `.design/` state as a handoff artifact if useful, but do not pretend files were persisted.

## Lifecycle

### Phase 0 - Orient

Resolve:

- project identity
- current artifact/state
- current phase
- target outcome
- constraints
- approved decisions
- unresolved decisions

Update `BRIEF.md` only when the project frame materially changes.

### Phase 1 - Product frame

Maintain in `PRODUCT.md`:

- audience / user roles
- primary jobs
- business goal
- product promise
- primary success event
- value/proof model
- constraints and non-goals
- product principles

Do not jump to visual styling when product logic is unresolved.

### Phase 2 - Research

Use research only when it can change a product/design decision.

Maintain `RESEARCH.md` as a synthesis, not a bookmark dump:

- question being investigated
- sources and dates
- findings
- confidence / limitations
- implications
- decisions influenced

Use normal web/search first. Escalate to Firecrawl for deeper crawling, multi-page extraction, or structured research sets when it adds value.

If JEV is available, it may rerank/classify research fragments before synthesis. Preserve citations/provenance.

### Phase 3 - Product story and content

Maintain `CONTENT.md` with:

- core message hierarchy
- terminology
- primary claims
- proof requirements
- CTA language
- content modules
- voice constraints
- unresolved copy questions

Content structure should support product comprehension before SEO optimization.

### Phase 4 - Design territories

Use Design Maestro for creative exploration when available.

Store each serious territory as a file under `territories/`, for example:

```text
territories/
├── 01-precision-infrastructure.md
├── 02-editorial-intelligence.md
└── 03-autonomous-motion.md
```

Each territory should define:

- thesis
- product story
- composition / layout language
- typography character
- color logic
- imagery/illustration
- interaction/motion character
- signature moment
- differentiation
- tradeoffs / risks
- best-fit contexts

Do not treat palette swaps as separate territories.

### Phase 5 - Decision checkpoint

For materially different territories or identity-level choices, keep the human/user in the decision loop.

When a choice is made, append to `DECISIONS.md`:

- date
- decision
- status
- rationale
- evidence
- alternatives considered
- consequences
- owner if relevant

Do not hide a creative choice behind a JEV score.

### Phase 6 - Brand and visual system

Maintain `BRAND.md` and `DESIGN.md`.

`BRAND.md` owns:

- positioning-relevant personality
- visual metaphor
- identity principles
- logo/mark rules when applicable
- typography direction
- palette intent
- imagery direction
- voice/tone relationship
- forbidden/avoid patterns

`DESIGN.md` owns:

- grid/container logic
- hierarchy
- spacing rhythm
- semantic color roles
- typography roles
- surfaces/depth
- shape/radius rules
- iconography
- motion principles
- signature moments
- responsive design principles

Document intent and roles, not only raw pixels.

### Phase 7 - Experience model

Maintain `EXPERIENCE.md` with:

- sitemap/screen map
- navigation model
- key flows
- state model
- primary/secondary actions
- feedback
- empty/loading/error/success states
- keyboard/touch/pointer behavior
- responsive transformations
- accessibility requirements

Use specialist skills for interaction, adaptation, Apple-platform guidance, or accessibility as needed.

### Phase 8 - Reviews and gates

Store substantial review outputs in `reviews/` and keep `QA.md` as the current summary.

Recommended gate families:

- **Discovery ready**: enough context to explore product/design directions.
- **Direction ready**: enough evidence and product clarity to choose a territory.
- **Build ready**: hierarchy, content, system, states, responsive behavior, and accessibility requirements are sufficiently specified.
- **Ship ready**: implementation has passed the relevant design/accessibility/content checks.

JEV may evaluate atomic gate criteria if available. Record the rubric and evidence. Do not use one vague "quality score".

Read `references/gates.md`.

### Phase 9 - Handoff

Maintain `HANDOFF.md` as the current implementation contract.

It should include:

- goal and audience
- approved direction
- page/screen map
- content hierarchy
- design-system decisions
- interaction states
- responsive rules
- accessibility requirements
- SEO/AI-discovery requirements when relevant
- assets/references
- things not to change
- open questions
- implementation constraints
- recommended specialist skills for the next phase

Handoff is a decision document, not a transcript.

### Phase 10 - Maintain

After implementation feedback, user testing, review, or a strategic change:

1. update the source document that owns the decision
2. append major changes to `DECISIONS.md`
3. refresh `QA.md`
4. update `HANDOFF.md` if implementation expectations changed
5. mark obsolete territory/review docs as superseded rather than deleting useful history without reason

## Optional JEV layer

Read `references/integrations.md` before use.

Appropriate JEV roles:

- classify incoming intent
- suggest relevant specialist skills from the live catalog
- rerank research fragments
- classify review findings
- evaluate atomic readiness criteria

JEV must not:

- invent the product strategy
- choose the brand identity as an unquestioned authority
- generate the final design direction
- replace evidence or user research
- replace accessibility verification

If `TYPESAFE_API_KEY` or the integration is unavailable, fall back to ordinary reasoning.

## Optional Firecrawl layer

Use Firecrawl only when the research problem benefits from deeper web extraction/crawling.

Examples:

- competitor homepage + product-page comparison
- multi-page content inventory
- structured category research
- extracting dynamic websites
- discovering a site's information architecture

If Firecrawl is unavailable, use the environment's normal web/search tools and continue.

## Design Maestro integration

When Design Maestro is installed, invoke it for:

- product/design direction
- design territories
- specialist routing
- visual-system synthesis
- critique/review orchestration
- implementation handoff synthesis

After the Maestro phase finishes, Product Studio must translate stable results into the appropriate `.design/` documents.

Product Studio owns persistence; Design Maestro owns creative orchestration.

## State precedence

When sources disagree, use this order unless the user explicitly overrides it:

1. latest explicit user decision
2. latest approved entry in `DECISIONS.md`
3. current owning document (`PRODUCT.md`, `BRAND.md`, `DESIGN.md`, etc.)
4. verified external evidence
5. specialist recommendation
6. old exploration/review material

Do not silently let an old territory override a newer approved design direction.

## Multi-agent behavior

For work distributed across agents:

- give each agent the smallest relevant `.design/` subset
- tell the agent which files are authoritative
- require returned findings to distinguish facts, proposals, and decisions
- merge stable outcomes back into the owning documents
- avoid multiple agents editing the same source-of-truth file concurrently when possible

Use `HANDOFF.md` as the implementation-facing contract and `DECISIONS.md` as the durable history of major choices.

## Output behavior

For each substantial session, finish with a compact state summary:

- what changed
- which `.design/` files were updated
- decisions made
- decisions still open
- current gate/status
- recommended next phase

Do not output this bookkeeping when it adds no value to a tiny task.

## References

Read only what the current phase needs:

- `references/operating-model.md` - architecture and Product Studio vs Design Maestro.
- `references/design-state.md` - `.design/` file ownership and state rules.
- `references/workflows.md` - end-to-end workflows for websites, apps, redesigns, and reviews.
- `references/gates.md` - readiness and quality gate patterns.
- `references/integrations.md` - JEV/TypeSafe AI and Firecrawl optional integration rules.
- `references/handoff.md` - handoff contract and multi-agent patterns.
- `references/examples.md` - concrete usage examples.

## Scripts

- `scripts/init_design_workspace.py` - create missing `.design/` structure without overwriting existing state.
- `scripts/check_design_workspace.py` - report required files, empty files, and current workspace completeness.
