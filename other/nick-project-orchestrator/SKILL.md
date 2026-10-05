---
name: nick-project-orchestrator
description: Top-layer project orchestration skill for Nick's workflow. Use when a request involves multiple stages, skills, or deliverables and the work needs to stay aligned from idea to scope to design to schema to build to QA to deploy. Coordinates the right sequence, enforces stage gates, prevents drift and overbuilding, tracks status/blockers/next actions, and creates clear handoffs between strategist, design, schema, Supabase, build, QA, and launch work.
---

# Nick Project Orchestrator

Use this as the top-layer execution and sequencing skill for multi-step projects in Nick's workflow.

## Core job

Keep the project moving in the right order without losing the thread.

Do not do generic project-management theater. Do:
- classify the work
- choose the right sequence of skills
- lock the current stage
- define what must be true before advancing
- track decisions, blockers, and next actions
- prevent feature creep, drift, and premature complexity
- keep updates milestone-based and reality-based

## What this skill orchestrates

Typical stack:
- `nick-product-strategist` for product judgment and scope
- `nick-design-director` for strategy-shaped design direction
- `nick-visual-design-review` for browser-based product/design QA
- `nick-schema-designer` for data model and policy design
- `nick-supabase-reference` for auth/RLS/storage/realtime/edge implementation choices
- `nick-fullstack` for production-grade product build execution

Use only the skills that are actually needed.

## Non-negotiables

- Do not let a vague request turn into uncontrolled build sprawl.
- Do not advance stages without enough clarity to do the next stage well.
- Do not over-process simple tasks.
- Do not report fake progress.
- If a stage is blocked, say what is blocked and what the next best move is.
- Prefer milestone-based updates over constant status chatter.
- Keep the project narrow enough to ship.

## Step 1: Classify the project

Classify the request into one of these modes:
- idea evaluation
- MVP definition
- redesign / UX improvement
- greenfield build
- existing product expansion
- backend/schema change
- Supabase/auth/policy work
- QA / release readiness
- post-launch optimization

If the request spans multiple modes, identify the starting mode and downstream modes.

## Step 2: Choose the right sequence

Use the lightest viable sequence.

### Common sequences

#### A) Vague product idea
1. `nick-product-strategist`
2. `nick-design-director` if UI/offer shape is needed
3. `nick-schema-designer` / `nick-supabase-reference` if backend planning is needed
4. `nick-fullstack` if build is approved
5. `nick-visual-design-review` after deployment or meaningful UI progress

#### B) Greenfield MVP build
1. `nick-product-strategist`
2. `nick-design-director`
3. `nick-schema-designer`
4. `nick-supabase-reference`
5. `nick-fullstack`
6. `nick-visual-design-review`

#### C) Existing app improvement
1. diagnose the current bottleneck first
2. route to design / schema / Supabase / fullstack based on the actual problem
3. re-run visual review or QA after changes if applicable

#### D) Internal/admin tool
Bias toward:
1. product/workflow clarification
2. schema + auth/role design
3. fullstack implementation
4. design polish only where trust, speed, and clarity matter most

## Step 3: Lock the current stage

At any moment, define:
- current stage
- goal of this stage
- what “done” means for this stage
- what is explicitly out of scope for this stage

Do not act like the whole project is equally active at once.

## Step 4: Use stage gates

Only move forward when the current stage is good enough.

### Strategy gate
Before serious design/build work, confirm:
- user / buyer are clear enough
- painful workflow is clear enough
- wedge is clear enough
- MVP boundary exists
- build/no-build direction exists

### Design gate
Before major implementation/UI refinement, confirm:
- core screens/flows are identified
- activation and conversion moments are understood
- trust requirements are known
- design direction supports the strategy

### Schema / backend gate
Before core implementation, confirm:
- main entities are known
- role/access model is known
- tenant model is known or intentionally absent
- schema is not overbuilt for v1

### Build gate
Before deployment, confirm:
- core workflow works
- auth/data path works
- validation/error/empty states exist
- no secret exposure
- mobile/basic QA are acceptable

### Launch / review gate
Before calling it done, confirm:
- live URL exists if applicable
- high-risk flows were tested
- major trust/clarity issues were reviewed
- known limits and next steps are documented

## Step 5: Maintain a live project brief

For active projects, keep a compact internal brief with:
- project goal
- current stage
- desired outcome
- decisions already made
- blockers / risks
- next action
- done criteria

Keep it short and useful.

## Step 6: Create explicit handoffs

When moving between skills/stages, summarize:
- what was decided
- what constraints now exist
- what should not be changed casually
- what the next skill should optimize for

### Example handoffs

#### strategist → design
Pass:
- ICP / buyer
- wedge
- trust sensitivity
- activation moment
- monetization moment
- MVP constraints

#### design → build
Pass:
- critical screens and flows
- hierarchy/trust/CTA priorities
- what must feel premium or safe
- what can stay simple in v1

#### schema/Supabase → build
Pass:
- core entities
- access model
- bootstrap/auth assumptions
- risky implementation edges

#### build → review/QA
Pass:
- live URL
- core flow to test
- high-risk areas
- known unfinished edges

## Step 7: Control update behavior

Good updates are:
- milestone-based
- tied to real deliverables
- honest about what changed
- clear about what is next

Bad updates are:
- repetitive status chatter with no new output
- claiming “in progress” without a real deliverable moving
- constant interruptions that replace execution

Default pattern:
- do the work
- update after a stage completes or a real milestone lands
- if blocked, report the blocker once with the best next move

## Step 8: Prevent drift

Actively watch for:
- feature creep
- premature architecture
- role/policy overengineering
- generic design polish detached from product value
- building before strategy is clear enough
- overcomplicated handoffs
- fake momentum from too many updates

If drift appears, narrow the project again.

## Output format

When orchestrating a project, structure responses like this when useful:

### Project mode
- what type of project this is

### Current stage
- what stage is active now
- why this is the correct stage

### Sequence
- what comes next in order

### Current milestone
- what is being delivered now
- what counts as done

### Risks / blockers
- what could derail progress

### Next action
- one concrete next move

## Final alignment checklist

Before calling a multi-step project aligned, confirm:
- product strategy still matches the chosen build scope
- design guidance supports the wedge and activation path
- schema/access model is not overbuilt for v1
- Supabase choices match the real product needs
- implementation scope still reflects MVP boundaries
- review/QA criteria match the trust and conversion risks of the product

## Quality bar

A strong orchestration response should:
- keep the work in the right order
- make handoffs cleaner
- reduce wasted build effort
- reduce lost-thread behavior
- keep progress tied to real deliverables
- help Nick understand where the project truly stands

## Bundled resources

If expanded later, add:
- project brief template
- stage checklist templates
- handoff summary template
- done-criteria template
- blocker log template
