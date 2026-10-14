---
name: story
description: '[Project Management] Use when creating user stories from PBIs, slicing features, or breaking down requirements.'
---

> Codex compatibility note:
>
> - Invoke repository skills with `$skill-name` in Codex; this mirrored copy rewrites legacy Claude `/skill-name` references.
> - Task tracker mandate: BEFORE executing any workflow or skill step, create/update task tracking for all steps and keep it synchronized as progress changes.
> - User-question prompts mean to ask the user directly in Codex.
> - Ignore Claude-specific mode-switch instructions when they appear.
> - Strict execution contract: when a user explicitly invokes a skill, execute that skill protocol as written.
> - Subagent authorization: when a skill is user-invoked or AI-detected and its protocol requires subagents, that skill activation authorizes use of the required `spawn_agent` subagent(s) for that task.
> - Do not skip, reorder, or merge protocol steps unless the user explicitly approves the deviation first.
> - For workflow skills, execute each listed child-skill step explicitly and report step-by-step evidence.
> - If a required step/tool cannot run in this environment, stop and ask the user before adapting.

<!-- CODEX:PROJECT-REFERENCE-LOADING:START -->

## Codex Project-Reference Loading (No Hooks)

Codex uses static project-reference loading instead of runtime-injected project docs.
When coding, planning, debugging, testing, or reviewing, open project docs explicitly using this routing.

**Always read:**

- `docs/project-config.json` (project-specific paths, commands, modules, and workflow/test settings)
- `docs/project-reference/docs-index-reference.md` (routes to the full `docs/project-reference/*` catalog)
- `docs/project-reference/lessons.md` (always-on guardrails and anti-patterns)

**Missing/stale context route:** If `docs/project-config.json`, the docs index, `lessons.md`, `CLAUDE.md`, `AGENTS.md`, or any task-required reference doc is missing or stale, auto-run `$project-init` or the narrow setup route (`$project-config`, `$docs-init`, `$scan-all`, `$scan --target=<key>`, `$claude-md-init`) before ordinary project-specific work. If Codex mirrors or `AGENTS.md` are missing/stale, ask the user to run `$sync-codex`; do not auto-run it.

**Situation-based docs:**

- Project structure/architecture/tech-stack/deployment/setup (any layer — backend, frontend, or infra): `project-structure-reference.md`
- Backend/CQRS/API/domain/entity changes: `backend-patterns-reference.md`, `domain-entities-reference.md`
- Frontend/UI/styling/design-system: `frontend-patterns-reference.md`, `scss-styling-guide.md`, `design-system/README.md`
- Spec authoring, `docs/specs/` pathing, or TC format: `feature-spec-reference.md`, `spec-system-reference.md`, `spec-principles.md`
- Behavior/public-contract changes or spec-test-code sync: `workflow-spec-test-code-cycle-reference.md` plus the spec docs above
- Derived spec indexes/ERDs/reimplementation guides: `spec-system-reference.md` and source Feature Specs under `docs/specs/`
- Integration test implementation/review: `integration-test-reference.md`
- E2E test implementation/review: `e2e-test-reference.md`
- Code review/audit work: `code-review-rules.md` plus domain docs above based on changed files

Do not read all docs blindly. Start from `docs-index-reference.md`, then open only relevant files for the task.

<!-- CODEX:PROJECT-REFERENCE-LOADING:END -->

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:START -->

> **[BLOCKING]** Execute skill steps in declared order. NEVER skip, reorder, or merge steps without explicit user approval.
> **[BLOCKING]** Before each step or sub-skill call, update task tracking: set `in_progress` when step starts, set `completed` when step ends.
> **[BLOCKING]** Every completed/skipped step MUST include brief evidence or explicit skip reason.
> **[BLOCKING]** If Task tools are unavailable, create and maintain an equivalent step-by-step plan tracker with the same status transitions.

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:END -->

## Quick Summary

**Goal:** Produce sprint-ready, INVEST-valid user stories — tech-agnostic, testable GWT criteria, evidence-cited estimates, dependency-mapped — by breaking Product Backlog Items into implementable stories via vertical slicing and SPIDR splitting, so a team with zero codebase knowledge can implement on any stack.

**Summary:**

- **Main steps (the pipeline):** (1) read PBI + active plan, load domain context — module, entities, BR-IDs; (2) identify VERTICAL end-to-end slices; (3) SPIDR-split anything SP >8 (MUST) / >5 (SHOULD) until INVEST-valid; (4) write each story with min 3 GWT scenarios + 1 authorization scenario; (5) estimate bottom-up (Blast-Radius pre-pass → phase-hours → days; SP DERIVED) and emit full estimate frontmatter; (6) emit Story Dependencies table (no orphans); (7) run MANDATORY ask the user directly validation; (8) save to `team-artifacts/pbis/stories/{YYMMDD}-ba-story-{slug}.md`; (9) suggest `$spec [mode=tests]` next.
- Slice VERTICALLY (thin end-to-end), NEVER horizontally (backend/frontend split) — apply SPIDR (Spike/Paths/Interfaces/Data/Rules) until each story is INVEST-valid — why: horizontal slices delay deliverable user value.
- Every story is tech-agnostic + rebuild-from-scratch + demoable (AI-SDD M1-M5 and M7): no framework/class/file names in prose, carry the inherited `FR-`/`BR-` logical ID plus a `[Source: namespace/service/id]` abstract anchor (NEVER `file:line`), and every criterion states an outcome a stakeholder could SEE — reject and rework on any STOP condition.
- Min 3 GIVEN/WHEN/THEN scenarios (happy + edge + error) PLUS a mandatory authorization scenario per story; every criterion has exactly ONE observable interpretation.
- Estimate bottom-up (phase-hours → days × productivity factor; SP DERIVED, never the driver) with explicit `test_count` and Blast-Radius pass; emit full `man_days_*` / `risk_*` / `blast_radius` / `estimate_reasoning` frontmatter — why: SP-first anchors to a guess, downstream `$prioritize`+`$plan` read these fields.
- Story Dependencies table is mandatory (no orphan stories) and the ask the user directly validation interview runs before handoff — NEVER auto-decide slicing/scope/effort.

> **MANDATORY IMPORTANT MUST ATTENTION** Plan ToDo Task to READ the following project-specific reference docs:
>
> - `project-structure-reference.md` -- project patterns and structure
> - `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)
> - `docs/specs/` — Test specifications by module (read existing TCs for related features; include test story/acceptance criteria for new stories)
>
> If file not found, search for: project documentation, coding standards, architecture docs.

**Workflow:**

1. **Read PBI** — Load PBI artifact, acceptance criteria, and domain context
2. **Vertical Slice** — Identify end-to-end slices of functionality
3. **SPIDR Split** — Apply Spike/Paths/Interfaces/Data/Rules splitting if effort >5
4. **Write Stories** — INVEST-validated stories with min 3 GIVEN/WHEN/THEN scenarios each
5. **Validate** — Interview user to confirm slicing, acceptance criteria, and effort estimates

**Key Rules:**

- Slice VERTICALLY (thin end-to-end); NEVER horizontally (backend/frontend split) — why: a horizontal slice ships no user-visible value on its own.
- SP >8 MUST ATTENTION be split; >5 SHOULD be split — apply SPIDR until each story is INVEST-valid.
- Every story MUST ATTENTION carry `story_points`, `complexity`, `man_days_traditional`, `man_days_ai` — plus the `risk_*` / `blast_radius` / `estimate_reasoning` fields `$prioritize` and `$plan` read downstream.
- SP is DERIVED from bottom-up phase-hours → days × productivity factor — NEVER the driver.
- Min 3 GIVEN/WHEN/THEN scenarios (happy + edge + error) PLUS a mandatory authorization scenario; each criterion has exactly ONE observable interpretation.
- Tech-agnostic prose ONLY — no framework/class/file names; anchor with `[Source: namespace/service/id]`, NEVER `file:line`.
- Story Dependencies table is mandatory — NEVER leave an orphan story.
- Run the ask the user directly validation interview before handoff — NEVER auto-decide slicing, scope, or effort.

### Frontend/UI Context (if applicable)

> When the task involves frontend or UI changes, read:

- Component patterns: `docs/project-reference/frontend-patterns-reference.md`
- Styling/BEM guide: `docs/project-reference/scss-styling-guide.md`
- Design system tokens: `docs/project-reference/design-system/README.md`

## Greenfield Mode

> **Auto-detected:** no existing codebase (no discovered source directories, no manifest files, no populated `project-config.json`) → greenfield mode switches on automatically. Planning artifacts (`docs/`, `plans/`, `.claude/`) do NOT count — the repository needs actual code directories with content.

**When greenfield is detected:**

1. Generate **foundation PBIs** instead of feature stories: infrastructure setup, project scaffold, CI/CD pipeline, first feature vertical slice
2. Dependency ordering: infrastructure stories BEFORE feature stories
3. Skip the `project-structure-reference.md` read — it will not exist
4. Include setup stories: dev environment, build tooling, deployment pipeline, monitoring
5. Priority order: infra → scaffold → first feature → remaining features
6. **[CRITICAL] Architecture Scaffolding Story:** FIRST story = "Architecture Scaffolding" — every OOP/SOLID base abstract class, generic interface, and infrastructure abstraction the chosen stack needs. AI self-investigates which base classes the project requires; every feature story depends on it — why: features built on an unscaffolded foundation encode the wrong abstractions permanently.
7. Scaffolding acceptance criteria: base classes compile/type-check, DI/IoC registrations resolve, smoke test passes
8. **UI System Foundation Story:** If the project has a frontend, generate a "UI System Foundation" story (Sprint 0) with these sub-stories:

    | Sub-Story                                                                 | SP  | Priority  | Depends On               |
    | ------------------------------------------------------------------------- | --- | --------- | ------------------------ |
    | "Set up design token system"                                              | 2-3 | Must Have | Architecture Scaffolding |
    | "Create base layout and responsive grid"                                  | 2-3 | Must Have | Design tokens            |
    | "Create core UI components (loading, error, empty, toast, button, input)" | 3-5 | Must Have | Design tokens + layout   |

**Dependency rule:** All UI feature stories MUST ATTENTION depend on "UI System Foundation" stories.

- Each story needs happy path, edge case, and error scenario (minimum)
- Use correct project domain vocabulary when available (check project docs for terminology)

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# User Story Creation

Break Product Backlog Items into implementable user stories using vertical slicing and SPIDR patterns.

---

## Step 0: Locate Active Plan (if in workflow)

If running within a workflow (big-feature, greenfield-init, etc.):

1. **Search for active plan** — Glob `plans/*/plan.md` sorted by modification time, or check the current task list for plan context
2. **Read `plan.md`** — understand project scope, architecture decisions, domain model, implementation plan
3. **Read existing research** — `{plan-dir}/research/*.md` and `{plan-dir}/phase-*.md` for domain model, tech stack, architecture
4. **Read `docs/project-reference/domain-entities-reference.md`** (if exists) — understand existing domain entities for accurate story scoping
5. Use plan context to inform story slicing (architecture decisions affect how stories are split)

---

## When to Use

- PBI ready for story breakdown
- Feature needs vertical slicing
- Creating sprint-ready work items
- Story too large (effort >8)

---

## Quick Reference

### Workflow

1. Read PBI artifact and acceptance criteria
2. **Load domain context** (if project module detected)
3. Identify vertical slices (end-to-end functionality)
4. **Apply SPIDR splitting** if stories too large
5. Apply INVEST criteria to each story
6. Create user stories with GIVEN/WHEN/THEN (min 3 scenarios)
7. Save to `team-artifacts/pbis/stories/`
8. **Validate stories** (MANDATORY) - Interview user to confirm slicing, acceptance criteria, and effort
9. Suggest next: `$spec [mode=tests]` or `$design-spec`

### Output

- **Path:** `team-artifacts/pbis/stories/{YYMMDD}-us-{pbi-slug}.md`
- **Format:** Single file with all stories (use ## headers per story)

> **Artifact Path (canonical convention)** — Command `$story` → base path `team-artifacts/pbis/stories/`, role token `ba`, type `story`. General filename pattern: `{YYMMDD}-{role}-{type}-{slug}.md` → e.g. `260119-ba-story-invoice-approval.md`. Slug = lowercased basename, non-alphanumeric → `-`, trimmed, max 50 chars.

---

## Project Domain Context Loading

When slicing domain-related PBIs, automatically load business context.

### Step 1: Detect Module

**From PBI frontmatter:**

1. Check `module` field
2. If missing, detect module from `docs/specs/` directory names

### Step 2: Load Feature Context

```
Glob("docs/specs/{module}/*.md")
```

1. Read module README (first 200 lines)
2. Identify related feature from `related_features` list
3. Extract existing business rules (BR-{MOD}-XXX)
4. Note entity names from feature docs

### Step 3: Apply Domain Vocabulary

Read `docs/project-config.json` modules[] and `docs/specs/` to detect domain vocabulary per module. Use entity names from feature docs — avoid ambiguous synonyms.

### Step 4: Include in Story

```markdown
## Domain Context

**Module:** {detected module}
**Feature:** {related feature}
**Entities:** {Entity1}, {Entity2}
**Business Rules:** BR-{MOD}-XXX (from feature docs)
```

---

## INVEST Criteria

| Criterion       | Definition                       | Validation Question                  |
| --------------- | -------------------------------- | ------------------------------------ |
| **I**ndependent | No dependencies on other stories | Can this be developed in any order?  |
| **N**egotiable  | Details can change               | Is the "how" open for discussion?    |
| **V**aluable    | Delivers user value              | Does user get observable benefit?    |
| **E**stimable   | Can estimate story points        | Can team size this? (Fibonacci 1-21) |
| **S**mall       | Completable in sprint            | SP ≤8? (prefer ≤5)                   |
| **T**estable    | Clear acceptance criteria        | Can we write pass/fail tests?        |

---

## SPIDR Splitting Checklist

**When to apply:** Story SP >8 MUST ATTENTION split. SP >5 SHOULD split. SP 13 = SHOULD split into 2-3 stories. SP 21 = MUST ATTENTION split (epic-level).

| Pattern        | Question                     | Split Strategy                            |
| -------------- | ---------------------------- | ----------------------------------------- |
| **S**pike      | Unknown complexity?          | Create research spike first, then stories |
| **P**aths      | Multiple workflow branches?  | One story per path/choice                 |
| **I**nterfaces | Multiple UIs or APIs?        | One story per interface                   |
| **D**ata       | Multiple data formats/types? | One story per data variation              |
| **R**ules      | Multiple business rules?     | One story per rule variation              |

### Splitting Examples

**Paths:** "User can pay by card OR PayPal" → Story A: Card payment, Story B: PayPal payment

**Data:** "Import CSV, Excel, JSON" → Story A: CSV import, Story B: Excel import, Story C: JSON import

**Rules:** "Different approval flows by amount" → Story A: <$1000 auto-approve, Story B: >$1000 manager approval

### Size Validation

```
SP 1-5:   ✅ Good size
SP 6-8:   ⚠️ Consider splitting (apply SPIDR)
SP 13:    ❌ SHOULD split into 2-3 stories
SP 21:    ❌ MUST ATTENTION split — epic-level, not sprint-ready
```

---

## Scenario Templates

**Minimum 3 scenarios per story:**

### 1. Happy Path (Positive)

```gherkin
Scenario: User successfully {completes action}
  Given {user has required permissions/state}
  And {required data exists}
  When user {performs valid action}
  Then {primary expected outcome}
  And {secondary verification if needed}
```

### 2. Edge Case (Boundary)

```gherkin
Scenario: System handles {boundary condition}
  Given {edge state: empty list, max items, zero value}
  When user {attempts action at boundary}
  Then {appropriate handling: pagination, warning, default}
```

### 3. Error Case (Negative)

```gherkin
Scenario: System prevents {invalid action}
  Given {precondition}
  When user {provides invalid input OR unauthorized action}
  Then error message "{specific error message}"
  And {system remains in valid state}
  And {no partial changes saved}
```

### 4. Authorization (MANDATORY per story)

```gherkin
Scenario: Unauthorized user cannot {perform action}
  Given user has role {unauthorized role}
  When user attempts to {action}
  Then system rejects with "Forbidden" or "Unauthorized"
  And no data is modified
```

### Additional Scenario Types

**Performance:** Response time under load
**Concurrency:** Simultaneous user actions
**Integration:** External service unavailable

---

## AI-SDD Mandate Gate (M1-M5 and M7) — BLOCKING

See `.claude/skills/shared/sdd-artifact-contract.md` → "AI-SDD Mandates (M1-M7)" for BLOCKING criteria. Every generated story MUST satisfy M1-M5 and M7:

- **Separate intent from implementation (M1/M2):** The story narrative and acceptance criteria stay tech-agnostic — describe observable business behavior, no framework/product/language/design-pattern names, no source identifiers. Keep optional hints in `## Technical Notes` and source references in evidence carriers as stack-portable abstract anchors (`[Source: namespace/service/id]`, never `file:line`). Prose follows `docs/project-reference/spec-principles.md` §3.
- **Logical Requirement ID (M3):** Each story carries a logical requirement ID (`FR-`/`BR-`) inherited from its parent PBI as the PRIMARY citation spine; keep the `[Source: namespace/service/id]` abstract anchor as a SECONDARY, stack-portable carrier — KEEP it, never remove it and never replace it with `file:line` (physical coordinates live only in the provenance sidecar).
- **Testable GWT/EARS criteria (M4):** Every Given/When/Then or EARS criterion has ONE valid interpretation, observable completion states, and named failure modes — no vague phrasing ("fast", "user-friendly", "handle appropriately") and no implementation details.
- **Rebuild-from-scratch (M5):** A team with zero codebase knowledge can implement identical behavior on ANY stack from the story alone.
- **Business-visibility (M7):** Apply the demo test to each criterion's BODY: _"what would a stakeholder SEE change?"_ — no answer → FAIL as TECHNICAL-ONLY and drop it from the story. Every `GIVEN` = a state a user could arrange; every `WHEN` = an action a user could take; every `THEN` = an outcome a user could see. FAIL a `WHEN` that is an invocation (a handler runs, a consumer receives, a job fires, data syncs) or a `THEN` asserting schema/type/nullability/call-count. Judge the BODY, never the story's title or ID. Never derive the story or scenario count from an architecture inventory (handlers, consumers, jobs) — that count moves when the system is re-architected though no business behavior changed, falsifying M5.

> **M1 governs vocabulary; M7 governs subject matter.** A technical story in impeccably tech-free prose satisfies M1 while violating M7 — _"the system correctly synchronizes the record"_ names no framework and is still a technical case in a business costume. That gap is the most common way business specs rot. Ask what a user could SEE, not which words were used.

> **[STOP — rework before emitting]** Reject and rework a story when ANY of these failure conditions holds:
>
> 1. Tech-specific prose — narrative/criteria name a framework, product, language type, or design-pattern class.
> 2. Source code reference in prose — a class/method name, file path, or namespace appears outside an evidence carrier.
> 3. Missing logical ID or evidence — no `FR-`/`BR-` ID, OR a requirement/rule with no `[Source: namespace/service/id]` abstract-anchor evidence (or explicit `TBD (pre-implementation)` marker).
> 4. Vague acceptance criteria — non-testable, non-observable, or more than one valid interpretation.
> 5. Not implementable from the artifact alone — a reader would have to read source or guess a rule, limit, role, or failure mode.
> 6. Not demoable (M7) — a criterion's body fails the demo test: its `WHEN` is an invocation, or its `THEN` asserts schema/type/nullability/call-count, or no stakeholder-visible change answers _"what would they SEE?"_ — it is TECHNICAL-ONLY and belongs to the technical tree, not this story.

---

## Story Artifact Template

````markdown
---
id: US-{YYMMDD}-{NNN}
parent_pbi: '{PBI-ID}'
title: '{Brief story title}'
persona: '{User persona}'
priority: P1 | P2 | P3
story_points: 1 | 2 | 3 | 5 | 8 | 13
complexity: Low | Medium | High | Very High
man_days_traditional: '{ Xd (Yd code + Zd test) — from SP table }'
man_days_ai: '{ Xd (Yd code + Zd test) — from SP table with AI }'
sprint: 0 | 1 | 2 | ...
status: draft | ready | in_progress | done
module: '{ServiceA | ServiceB | ServiceC | ServiceD}'
---

# User Stories for {PBI Title}

## Story 1: {Title}

**As a** {user role}
**I want** {goal}
**So that** {benefit}

### Acceptance Criteria

#### Scenario 1: {Happy path title}

```gherkin
Given {context}
When {action}
Then {outcome}
```

#### Scenario 2: {Edge case title}

```gherkin
Given {edge state}
When {action}
Then {handling}
```

#### Scenario 3: {Error case title}

```gherkin
Given {context}
When {invalid action}
Then error "{message}"
```

---

## Story 2: {Title}

{Repeat structure...}

---

## Out of Scope

- {Explicitly excluded items}

## Story Dependencies

| Story    | Depends On | Type         | Reason                            |
| -------- | ---------- | ------------ | --------------------------------- |
| US-{NNN} | -          | independent  | First slice, no dependencies      |
| US-{NNN} | US-{NNN}   | must-after   | Needs entity/API from prior story |
| US-{NNN} | US-{NNN}   | can-parallel | Independent feature slice         |
| US-{NNN} | US-{NNN}   | blocked-by   | Requires external service/infra   |

## Domain Context

**Module:** {module}
**Related Feature:** {feature doc path}
**Entities:** {Entity1}, {Entity2}
**Requirement IDs (M3 — inherited from PBI):** {FR-XXX / BR-XXX — primary citation spine}
**Business Rules:** {BR-XXX references}
**Evidence (secondary, stack-portable):** {`[Source: namespace/service/id]` abstract anchor per requirement, or `TBD (pre-implementation)`}

## UI Wireframe

### Layout

{ASCII wireframe showing this story's UI slice — see UI wireframe protocol}

### Components

- **{ComponentName}** — {behavior for this story} _(tier: common | domain-shared | page/app)_

> Classify per **Component Hierarchy** in `UI wireframe protocol` — search existing libs before proposing new components.

### Interaction Flow

1. User {action} on {component}
2. System {response/feedback}
3. UI updates to show {result}

### States

| State   | Behavior                   |
| ------- | -------------------------- |
| Default | {what user sees initially} |
| Loading | {spinner/skeleton}         |
| Empty   | {empty state message}      |
| Error   | {error handling}           |

> If backend-only: `## UI Wireframe` → `N/A — Backend-only change. No UI affected.`

## Technical Notes

- {Implementation hints if needed}

## Validation Summary

**Validated:** {date}

### Confirmed

- {decision}: {user choice}

### Action Items

- [ ] {follow-up if any}
````

---

## Sprint 0 / Foundation Stories (Production Readiness)

When the PBI includes a "Production Readiness Concerns" table with "Required" items, automatically generate Sprint 0 / foundation stories for each concern:

| PBI Concern                       | Story Title                                | Story Points | Priority  |
| --------------------------------- | ------------------------------------------ | ------------ | --------- |
| Code linting/analyzers = Required | "Set up code linting and formatting"       | 1-2 SP       | Must Have |
| Error handling setup = Required   | "Set up error handling foundation"         | 2-3 SP       | Must Have |
| Loading indicators = Required     | "Set up loading indicator infrastructure"  | 1-2 SP       | Must Have |
| Docker integration = Required     | "Set up Docker development environment"    | 2-3 SP       | Must Have |
| CI/CD quality gates = Required    | "Set up CI/CD quality gates"               | 2-3 SP       | Must Have |
| Seed data = Required              | "Set up seed data / data seeder"           | 2-3 SP       | Must Have |
| Data migration = Required         | "Create data migration for schema changes" | 1-3 SP       | Must Have |

### Rules

- Foundation stories MUST ATTENTION be completed before feature stories begin
- Mark as `sprint: 0` or `sprint: foundation` in story metadata
- Each foundation story references the specific protocol section for implementation guidance
- If PBI concern = "Existing", skip story generation (already set up)
- If PBI concern = "No", skip story generation (explicitly opted out)

---

## Anti-Patterns to Avoid

| Anti-Pattern       | Problem                                           | Correct Approach                              |
| ------------------ | ------------------------------------------------- | --------------------------------------------- |
| Horizontal slicing | "Backend story" + "Frontend story" = delays value | Vertical slice: thin end-to-end functionality |
| Single scenario    | Missing edge/error cases                          | Minimum 3 scenarios: happy, edge, error       |
| Vague criteria     | "Fast", "user-friendly" untestable                | Quantify: "< 200ms", "≤ 3 clicks"             |
| Solution-speak     | "Use Redis cache" constrains team                 | Outcome: "Results return within 200ms"        |
| Effort >8          | Won't fit sprint, hard to estimate                | Apply SPIDR, split until ≤8                   |
| No error scenario  | Missing negative test coverage                    | Always include invalid input handling         |
| Generic persona    | "As a user" too vague                             | Specific: "As a warehouse operator"           |

---

## Key Rules

- **Every story set MUST ATTENTION include a Story Dependencies table** — with types: `must-after`, `can-parallel`, `blocked-by`, `independent`. This enables `$prioritize` and `$plan` to respect implementation ordering.
- **SPIDR splits MUST ATTENTION include dependency chains** — When splitting a story, declare which split stories depend on others.
- **No orphan stories** — Every story must appear in the dependency table, even if independent.

## Quality Checklist

Before completing user stories:

- [ ] Each story follows "As a... I want... So that..." format
- [ ] SPIDR splitting applied (effort ≤8, prefer ≤5)
- [ ] At least 3 scenarios per story: happy, edge, error
- [ ] All scenarios use GIVEN/WHEN/THEN format
- [ ] Effort estimated in Fibonacci (1, 2, 3, 5, 8)
- [ ] Stories independent (can develop in any order)
- [ ] Out of scope explicitly listed
- [ ] Story Dependencies table included with all stories listed
- [ ] Dependency types correct (must-after, can-parallel, blocked-by, independent)
- [ ] Parent PBI linked in frontmatter
- [ ] Domain vocabulary used correctly (if the project)
- [ ] Authorization scenario included per story (unauthorized access rejection)
- [ ] Seed data story included if PBI has seed data requirements
- [ ] Data migration story included if PBI has schema changes
- [ ] Validation interview completed

---

## Validation Step (MANDATORY)

After creating user stories, validate with user.

### Question Categories

| Category         | Example Question                                    |
| ---------------- | --------------------------------------------------- |
| **Slicing**      | "Are the story slices independent enough?"          |
| **Size**         | "Any story >8 effort that needs further splitting?" |
| **Scenarios**    | "Any acceptance criteria missing for edge cases?"   |
| **Dependencies** | "Are there hidden dependencies between stories?"    |
| **Scope**        | "Should anything be explicitly excluded?"           |

### Process

1. Generate 2-4 questions focused on slicing quality, scenarios, and dependencies
2. Use ask the user directly tool to interview
3. Document in story artifact under `## Validation Summary`
4. Update stories based on answers (split if needed)

**This step is NOT optional.**

---

## Related

| Type           | Reference                                           |
| -------------- | --------------------------------------------------- |
| **Role Skill** | `business-analyst`                                  |
| **Command**    | `$story`                                            |
| **Input**      | `$refine` output (PBI)                              |
| **Next Steps** | `$spec [mode=tests]`, `$design-spec`, `$prioritize` |

---

## MANDATORY: Systematic Task Breakdown for Stories

**MANDATORY IMPORTANT MUST ATTENTION** break down ALL stories into small, systematic todo tasks using task tracking BEFORE starting implementation. Each story MUST ATTENTION have its own set of tasks that cover:

1. **Read & understand story** — Load story artifact, acceptance criteria, domain context
2. **Identify vertical slice layers** — Backend entity/command/query, frontend component/store/API, integration points
3. **Create implementation subtasks per layer** — One task per file or logical unit (entity, command handler, DTO, component, service, test)
4. **Include spec tasks** — Each story MUST ATTENTION have corresponding test specifications (unit, integration, or E2E as appropriate)
5. **Include validation task** — Verify story against acceptance criteria GIVEN/WHEN/THEN after implementation
6. **Include review task** — Final quality check per story

### Task Naming Convention

```

[Story US-{ID}] {Layer}: {Description}

```

Example for a "Create Invoice" story:

```

[Story US-001] Entity: Create Invoice entity with validation rules
[Story US-001] Command: CreateInvoiceCommand + Handler
[Story US-001] DTO: InvoiceDto with mapping
[Story US-001] API: POST /api/invoices endpoint
[Story US-001] Component: InvoiceCreateFormComponent
[Story US-001] Store: InvoiceVmStore with create action
[Story US-001] Test: Integration test for CreateInvoiceCommand
[Story US-001] Test: E2E test for invoice creation flow
[Story US-001] Review: Verify against AC scenarios

```

**Why:** Without systematic task breakdown, stories become monolithic — missed edge cases, incomplete specs, context loss during implementation.

---

## Next Steps

**MANDATORY IMPORTANT MUST ATTENTION — NO EXCEPTIONS** after completing this skill, you MUST ATTENTION use ask the user directly to present these options. Do NOT skip because the task seems "simple" or "obvious" — the user decides:

- **"$spec [mode=tests] (Recommended)"** — Generate test specifications from stories
- **"$pbi-mockup"** — Generate HTML mockup report from PBI and stories
- **"$plan-validate"** — If stories need validation against plan
- **"Skip, continue manually"** — user decides

> **[IMPORTANT]** Use task tracking to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ATTENTION ask user whether to skip.

> **External Memory:** For complex or lengthy work (research, analysis, scan, review), write intermediate findings and final results to a report file in `plans/reports/` — prevents context loss and serves as deliverable.

> **Evidence Gate:** MANDATORY IMPORTANT MUST ATTENTION — every claim, finding, and recommendation requires `file:line` proof or traced evidence with confidence percentage (>80% to act, <80% must verify first).

<!-- SYNC:estimation-framework -->

> **Estimation Framework** — Bottom-up first; SP DERIVED; output min-max range when likely ≥3d. Stack-agnostic. Baseline: 3-5yr dev, 6 productive hrs/day. AI estimate assumes Claude Code + project context.
>
> **Method:**
>
> 1. **Blast Radius pass** (below) — drives code AND test cost
> 2. Decompose phases → hours/phase → `bottom_up_hours = Σ phase_hours`
> 3. `likely_days = ceil(bottom_up_hours / 6) × productivity_factor`
> 4. Sum **Risk Margin** (base + add-ons) → `max_days = likely_days × (1 + margin)`
> 5. `min_days = likely_days × 0.9`
> 6. Output as range when `likely_days ≥3`; single point allowed `<3` (still record margin)
> 7. `man_days_ai` = same range × AI speedup
> 8. `story_points` DERIVED from `likely_days` via SP-Days — NEVER driver. Disagreement >50% → trust bottom-up
>
> **Productivity factor:** 0.8 strong scaffolding+codegen+AI hooks · 1.0 mature default · 1.2 weak patterns · 1.5 greenfield
>
> **Cost Driver Heuristic (apply BEFORE work-type row):**
>
> - **UI dominates** in CRUD/business apps — 1.5-3x backend (states, validation, responsive, a11y, polish)
> - **Backend dominates ONLY:** multi-aggregate invariants, cross-service contracts, schema migrations, heavy query/perf, new event flows
>
> **Reuse-vs-Create axis (PRIMARY lever, per layer):**
>
> | UI tier                                      | Cost     |
> | -------------------------------------------- | -------- |
> | Reuse component on existing screen           | 0.1-0.3d |
> | Add control/column to existing screen        | 0.3-0.8d |
> | Compose components into NEW screen           | 1-2d     |
> | NEW screen, custom layout/states/validation  | 2-4d     |
> | NEW shared/common component (themed, tested) | 3-6d+    |
>
> | Backend tier                                         | Cost      |
> | ---------------------------------------------------- | --------- |
> | Reuse query/handler from new place                   | 0.1-0.3d  |
> | Small update existing handler/entity                 | 0.3-0.8d  |
> | NEW query on existing repo/model                     | 0.5-1d    |
> | NEW command/handler on existing aggregate (additive) | 1-2d      |
> | NEW aggregate/entity (repo, validation, events)      | 2-4d      |
> | NEW cross-service contract OR schema migration       | 2-4d each |
> | Multi-aggregate invariant / heavy domain rule        | 3-5d      |
>
> **Rule:** Sum tiers across UI+backend+tests, apply productivity factor. Reuse short-circuits tiers — call out.
>
> **Test-Scope drivers (compute test_count EXPLICITLY — "+tests" hand-wave is #1 failure):**
>
> | Driver                            | Count                                                  |
> | --------------------------------- | ------------------------------------------------------ |
> | Happy-path journeys               | 1 per story / AC main flow                             |
> | State-machine transitions         | reachable transitions × allowed actors                 |
> | Multi-entity state combos         | state(A) × state(B) — REACHABLE only, not Cartesian    |
> | Authorization matrix              | (owner, non-owner, elevated, unauth) × each mutation   |
> | Validation rules                  | 1 per required field / boundary / format / cross-field |
> | UI states (per new screen/dialog) | happy, loading, empty, error, partial — present only   |
> | Negative paths / invariants       | 1 per violatable business rule                         |
>
> | Test tier (Trad, incl. setup+assert+flake) | Cost     |
> | ------------------------------------------ | -------- |
> | 1-5 cases, fixtures reused                 | 0.3-0.5d |
> | 6-12 cases, 1 new fixture                  | 0.5-1d   |
> | 13-25 cases, multi-entity setup            | 1-2d     |
> | 26-50 cases OR new state-machine coverage  | 2-3d     |
> | >50 cases OR full E2E journey              | 3-5d     |
>
> **Test multipliers:** new fixture/seed harness +0.5d · cross-service/bus assertion +0.3d each · UI E2E ×1.5 · each new role +1-2 cases
>
> **Blast Radius (mandatory pre-pass — affects code AND test):**
>
> 1. Files/components directly modified — count
> 2. Of those, "complex" (>500 LOC, multi-handler, central, frequently-modified) — count
> 3. Downstream consumers (callers, event subscribers, cross-service) — list
> 4. Shared/common code touched (multi-app blast) — yes/no
> 5. Regression scope — areas needing re-test
>
> **Rule:** Complex touch → add `risk_factors`. Each downstream consumer → +1-3 regression cases. Blast >5 areas OR >2 complex → re-evaluate SPLIT before estimating.
>
> **Risk Margin (drives max bound):**
>
> | likely_days         | Base margin                     |
> | ------------------- | ------------------------------- |
> | <1d trivial         | +10%                            |
> | 1-2d small additive | +20%                            |
> | 3-4d real feature   | +35%                            |
> | 5-7d large          | +50%                            |
> | 8-10d very large    | +75%                            |
> | >10d                | +100% AND **flag SHOULD SPLIT** |
>
> **Risk-factor add-ons (additive — enumerate in `risk_factors`):**
>
> | Factor                                                                | +margin |
> | --------------------------------------------------------------------- | ------- |
> | `touches-complex-existing-feature` (>500 LOC, multi-handler, central) | +20%    |
> | `cross-service-contract` change                                       | +25%    |
> | `schema-migration-on-populated-data`                                  | +25%    |
> | `new-tech-or-unfamiliar-pattern`                                      | +30%    |
> | `regression-fan-out` (≥3 downstream areas re-test)                    | +20%    |
> | `performance-or-latency-critical`                                     | +20%    |
> | `concurrency-race-event-ordering`                                     | +25%    |
> | `shared-common-code` (multi-consumer/multi-app)                       | +25%    |
> | `unclear-requirements-or-design`                                      | +30%    |
>
> **Collapse rule:** total margin >100% → STOP, split (padding past 2x is dishonesty). Margin <15% on `likely_days ≥5` → under-estimated, widen.
>
> **Work-Type Caps (hard ceilings on `likely_days`):**
> | Work type | Max SP | Max likely |
> | --- | --- | --- |
> | Single field / config flag / style fix | 1 | 0.5d |
> | Add property to existing model + bind to existing UI | 2 | 1d |
> | **Additive endpoint + minor UI control** (button/menu/column), reuses fixtures | **3** | **2-3d** |
> | Additive endpoint + **NEW UI surface** OR additive multi-layer + new domain rule + 2+ test files | 5 | 3-5d |
> | NEW model/aggregate OR migration OR cross-module contract OR heavy test (>1.5d) OR NEW UI + non-trivial backend | 8 | 5-7d |
> | NEW UI surface + (NEW aggregate OR migration OR cross-service contract) | 13 | SHOULD split |
> | Cross-service contract + migration combined | 13 | SHOULD split |
> | Beyond | 21 | MUST split |
>
> **SP→Days (validation only):** 1=0.5d/0.25d · 2=1d/0.35d · 3=2d/0.65d · 5=4d/1.0d · 8=6d/1.5d · 13=10d/2.0d (Trad/AI likely)
> **AI speedup:** SP 1≈2x · 2-3≈3x · 5-8≈4x · 13+≈5x. AI cost = `(code_gen × 1.3) + (test_gen × 1.3)` (30% review overhead).
>
> **MANDATORY frontmatter:**
>
> ```yaml
> story_points: <n>
> complexity: low | medium | high | critical
> man_days_traditional: '<min>-<max>d' # range when likely ≥3d; '<N>d' when <3d
> man_days_ai: '<min>-<max>d'
> risk_margin_pct: <n> # base + add-ons
> risk_factors: [touches-complex-existing-feature, regression-fan-out] # closed-list from add-ons; [] if none
> blast_radius:
>     touched_areas: <n>
>     complex_touched: <n>
>     downstream_consumers: [list or count]
>     shared_common_code: yes | no
> estimate_scope_included: [code, integration-tests, frontend, i18n, docs]
> estimate_scope_excluded: [unit-tests, e2e, perf, deployment, code-review-rounds]
> estimate_reasoning: |
>     5-7 lines covering:
>     (a) UI tier — row applied
>     (b) Backend tier — row applied
>     (c) Test scope — case breakdown by driver, file count, fixtures, tier row
>     (d) Cost driver — dominant tier + why
>     (e) Blast radius — touched, complex, regression scope
>     (f) Risk factors — list driving margin; why not larger/smaller
>     Example: "UI: compose Form/Table/Dialog → NEW screen (~1.5d). Backend: NEW command on existing aggregate,
>     reuses validation+repo (~1d). Tests: 4 transitions × 2 actors + 3 validation + 2 UI states = 13 cases,
>     1 new fixture → tier 13-25 ~1.5d. Driver: UI composition + new states. Blast: 4 areas, 1 complex.
>     Risk: base 35% + touches-complex +20% = 55% → max 3.9d → range 2.5-4d."
> ```
>
> **Sanity self-check:**
>
> - `likely_days ≥3d` and single-point? → reject, must be range
> - Margin <15% on `likely_days ≥5d`? → under-estimated, widen
> - Margin >100%? → STOP, split instead of buffer
> - Complex existing feature touched, no regression budget in `(c)`? → reject
> - Blast `>5` areas OR `>2` complex, no split discussion? → reject
> - Purely additive on existing model AND existing UI? → cap SP 3 unless tests >1.5d
> - NEW UI surface (page/complex form/dashboard)? → SP 5+ even if backend one endpoint
> - Backend cross-service / migration / multi-aggregate? → SP 8+ regardless of UI
> - `bottom_up_hours / 6` vs SP-Days disagreement >50%? → trust bottom-up, downgrade SP
> - Without tests, SP drops ≥1 bucket? → tests dominate; state explicitly
> - Reasoning called out UI vs backend vs blast vs risk factors? → if missing, add

<!-- /SYNC:estimation-framework -->

<!-- SYNC:ui-system-context -->

> **UI System Context** — For ANY task touching `.ts`, `.html`, `.scss`, or `.css` files:
>
> **MUST ATTENTION READ before implementing:**
>
> 1. `docs/project-reference/frontend-patterns-reference.md` — component base classes, stores, forms
> 2. `docs/project-reference/scss-styling-guide.md` — BEM methodology, SCSS variables, mixins, responsive
> 3. `docs/project-reference/design-system/README.md` — design tokens, component inventory, icons
>
> Reference `docs/project-config.json` for project-specific paths.

<!-- /SYNC:ui-system-context -->

<!-- SYNC:ui-wireframe -->

> **UI Wireframe** — Process visual design input (Figma URLs, screenshots, wireframes) via appropriate tool BEFORE creating wireframes. Use box-drawing ASCII characters for spatial layout. Classify every component into exactly ONE tier: Common (cross-app reusable) / Domain-Shared (cross-domain) / Page (single-page). Duplicate UI code = wrong tier. Search existing component libraries before creating new (>=80% match = reuse). Detail level varies by skill (idea=rough, story=full decomposition).

<!-- /SYNC:ui-wireframe -->

<!-- SYNC:critical-thinking-mindset -->

> **Critical Thinking Mindset** — Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
> **Anti-hallucination:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.

<!-- /SYNC:critical-thinking-mindset -->

<!-- SYNC:sequential-thinking-protocol -->

> **Sequential Thinking Protocol** — Structured multi-step reasoning for complex/ambiguous work. Use when planning, reviewing, debugging, or refining ideas where one-shot reasoning is unsafe.
>
> **Trigger when:** complex problem decomposition · adaptive plans needing revision · analysis with course correction · unclear/emerging scope · multi-step solutions · hypothesis-driven debugging · cross-cutting trade-off evaluation.
>
> **Format (explicit mode — visible thought trail):**
>
> 1. `Thought N/M: [aspect]` — one aspect per thought, state assumptions/uncertainty
> 2. `Thought N/M [REVISION of Thought K]: ...` — when prior reasoning invalidated; state Original / Why revised / Impact
> 3. `Thought N/M [BRANCH A from Thought K]: ...` — explore alternative; converge with decision rationale
> 4. `Thought N/M [HYPOTHESIS]: ...` then `[VERIFICATION]: ...` — test before acting
> 5. `Thought N/N [FINAL]` — only when verified, all critical aspects addressed, confidence >80%
>
> **Mandatory closers:** Confidence % stated · Assumptions listed · Open questions surfaced · Next action concrete.
>
> **Stop conditions:** confidence <80% on any critical decision → escalate by asking the user directly · ≥3 revisions on same thought → re-frame the problem · branch count >3 → split into sub-task.
>
> **Implicit mode:** apply methodology internally without visible markers when adding markers would clutter the response (routine work where reasoning aids accuracy).
>
> **Deep-dive:** see `$sequential-thinking` skill (`.claude/skills/sequential-thinking/SKILL.md`) for worked examples (API design, debugging, architecture), advanced techniques (spiral refinement, hypothesis testing, convergence), and meta-strategies (uncertainty handling, revision cascades).

<!-- /SYNC:sequential-thinking-protocol -->

<!-- SYNC:ai-mistake-prevention -->

> **AI Mistake Prevention** — Failure modes to avoid on every task:
>
> **Re-read files after context changes.** Context compaction, resume, or long-running work can make memory stale; verify current files before acting.
> **Verify generated content against source evidence.** AI hallucinates APIs, names, claims, and document facts. Check the relevant source before documenting or referencing.
> **Check downstream references before deleting or renaming.** Removing an artifact can stale docs, generated mirrors, configs, and callers; map references first.
> **Trace the full impact chain after edits.** Changing a definition can miss derived outputs and consumers. Follow the affected chain before declaring done.
> **Verify ALL affected outputs, not just the first.** One green check is not all green checks; validate every output surface the change can affect.
> **Assume existing values are intentional — ask WHY before changing OR flagging one as a defect.** Before changing or reporting a constant, limit, flag, cutoff, wording, or pattern, read nearby context and history, the CALLER's ordering, and 2+ sibling call sites of the same convention. A doc stating WHAT without WHY is missing rationale, not proof of a missing guard.
> **Surface ambiguity before acting — don't pick silently.** Multiple valid interpretations require an explicit question or stated assumption with risk.
> **Assert the outcome your system owns, not the intermediate state your infrastructure owns.** When verifying async work, assert the final business state — never the delivery/retry bookkeeping held in shared infrastructure that any co-running process can write. Such a check passes when run alone and flakes the moment anything else shares that infrastructure.
> **Keep shared guidance role-relevant.** Universal guidance must help every receiving skill or agent; code-specific obligations belong only in code-specific protocols.

<!-- /SYNC:ai-mistake-prevention -->

<!-- SYNC:estimation-framework:reminder -->

- **MANDATORY MUST ATTENTION** estimation: bottom-up phase hours drive `man_days_traditional` (`Σh/6 × productivity_factor`); SP DERIVED. UI cost usually dominates — bump SP one bucket if NEW UI surface (page/complex form/dashboard). Frontmatter MUST include `story_points`, `complexity`, `man_days_traditional`, `man_days_ai`, `estimate_scope_included`, `estimate_scope_excluded`, `estimate_reasoning` (UI vs backend cost driver). Cap SP 3 for additive-on-existing-model+existing-UI unless test scope >1.5d. SP 13 SHOULD split, SP 21 MUST split.
  <!-- /SYNC:estimation-framework:reminder -->

<!-- SYNC:ui-system-context:reminder -->

**IMPORTANT MUST ATTENTION** read frontend-patterns-reference, scss-styling-guide, design-system/README before any UI change.

<!-- /SYNC:ui-system-context:reminder -->

<!-- SYNC:critical-thinking-mindset:reminder -->

**MUST ATTENTION** apply critical + sequential thinking — every claim needs appropriate traced evidence (`file:line` for repo/code claims; source URL or artifact section for research, product, content, and docs claims); confidence >80% to act, <60% DO NOT recommend. Anti-hallucination: never present guess as fact, admit uncertainty freely, cross-reference independently, stay skeptical of own confidence.

<!-- /SYNC:critical-thinking-mindset:reminder -->

<!-- SYNC:sequential-thinking-protocol:reminder -->

**MUST ATTENTION** apply sequential-thinking — multi-step Thought N/M, REVISION/BRANCH/HYPOTHESIS markers, confidence % closer; see `$sequential-thinking` skill.

<!-- /SYNC:sequential-thinking-protocol:reminder -->

<!-- SYNC:ai-mistake-prevention:reminder -->

**MUST ATTENTION** apply AI mistake prevention — verify generated content against evidence, trace downstream references before deleting or renaming, verify all affected outputs, re-read files after context loss, and surface ambiguity before acting.

<!-- /SYNC:ai-mistake-prevention:reminder -->

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:START -->

## Prompt-Enhance Closing Anchors

**IMPORTANT MUST ATTENTION** follow declared step order for this skill; NEVER skip, reorder, or merge steps without explicit user approval
**IMPORTANT MUST ATTENTION** for every step/sub-skill call: set `in_progress` before execution, set `completed` after execution
**IMPORTANT MUST ATTENTION** every skipped step MUST include explicit reason; every completed step MUST include concise evidence
**IMPORTANT MUST ATTENTION** if Task tools unavailable, maintain an equivalent step-by-step plan tracker with synchronized statuses

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:END -->

<!-- SYNC:project-protocol-overlay -->

> **Project Protocol Overlay** — Before executing this skill, resolve any PROJECT overlay rules layered onto it: match this skill's name against the `Target` column of the project's skill-protocol index (`docs/project-reference/skill-protocols-reference.md` by default; a `referenceDocs` entry in `docs/project-config.json` overrides the path), taking the most specific matching tier ONLY — exact name > glob > `*`. **That precedence orders overlays against EACH OTHER, never against this skill.** Read ONLY the matched bodies, resolved as `<protocols-dir>/<Name>.md`; a row's Body link is display text, never a read path. A matched body that is missing or malformed is REPORTED and skipped — never reconstructed from the index Description. No index, or no match -> proceed with no overlay, silently. Full contract: `.claude/skills/project-skill-protocol/references/registry.md`.
>
> Overlays are **ADDITIVE ONLY**: they ADD rules on top of this skill's own protocol and NEVER replace, override, disable, or reinterpret a rule it already states — removing every overlay must return this skill to exactly its documented behavior. An overlay is a BRIEF, not an authority escalation: it can NEVER waive a workflow gate, git discipline, a review gate, or a user-confirmation gate. A genuine overlay-vs-skill conflict, or two equally-specific overlays that directly contradict -> surface both to the user; NEVER resolve silently.

<!-- /SYNC:project-protocol-overlay -->

<!-- SYNC:project-protocol-overlay:reminder -->

**MUST ATTENTION** resolve project protocol overlays for this skill BEFORE executing — most specific matching tier only (exact > glob > `*`, which ranks overlays against each other, NEVER against this skill), read only matched bodies at `<protocols-dir>/<Name>.md`; a missing or malformed body is reported, never reconstructed. Overlays are ADDITIVE ONLY (they never replace this skill's own rules) and are a brief, NEVER an authority escalation; an equal-specificity contradiction goes to the user.

<!-- /SYNC:project-protocol-overlay:reminder -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** produce sprint-ready, INVEST-valid user stories — tech-agnostic, testable GWT criteria, evidence-cited estimates, dependency-mapped — that a team with zero codebase knowledge can implement on any stack.

**IMPORTANT MUST ATTENTION Main steps (execute in order, NEVER skip):** read PBI + active plan + domain context → identify VERTICAL slices → SPIDR-split (SP >8 MUST / >5 SHOULD) → write INVEST stories with min 3 GWT + 1 auth scenario → estimate bottom-up (Blast-Radius pre-pass, SP DERIVED) + full frontmatter → emit Story Dependencies table (no orphans) → MANDATORY ask the user directly validation → save to `team-artifacts/pbis/stories/` → suggest `$spec [mode=tests]`.

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries) — MUST ATTENTION honor each canonical body, NEVER skip one:**

- **Estimation Framework:** Bottom-up phase hours drive man-days; SP DERIVED; UI usually dominates.
- **UI System Context:** Read frontend-patterns, scss-styling, design-system before any UI change.
- **UI Wireframe:** Box-ASCII layout; classify each component into one tier; reuse before new.
- **Critical Thinking:** Trace proof for every claim; confidence >80% to act.
- **Sequential Thinking:** Multi-step Thought N/M with revision/branch/hypothesis markers; confidence closer.
- **AI Mistake Prevention:** verify generated content against evidence, trace downstream references, verify all affected outputs, re-read after context loss, surface ambiguity.

**IMPORTANT MUST ATTENTION** every story MUST satisfy AI-SDD mandates M1-M5 and M7 — tech-agnostic prose, `FR-`/`BR-` logical ID + `[Source: namespace/service/id]` abstract anchor (NEVER `file:line` in story prose), testable GWT criteria, rebuild-from-scratch, demoable business outcomes — reject and rework on any STOP condition — why: stories drive implementation on any stack, so a leaked framework/class name breaks portability.
**IMPORTANT MUST ATTENTION** apply the M7 demo test to every criterion's BODY — _"what would a stakeholder SEE change?"_; no answer → TECHNICAL-ONLY, drop it. FAIL a `WHEN` that is an invocation (handler runs, consumer receives, job fires, data syncs) or a `THEN` asserting schema/type/nullability/call-count; NEVER derive the story/scenario count from an architecture inventory — why: M1 governs vocabulary, M7 governs subject matter — a technical story in tech-free prose passes M1 and still rots the business tree.
**IMPORTANT MUST ATTENTION** every story set includes a Story Dependencies table with no orphan stories; SP >8 MUST split, >5 SHOULD split via SPIDR — why: ordering feeds `$prioritize` and `$plan` and oversized stories miss the sprint.
**MANDATORY IMPORTANT MUST ATTENTION** break work into small todo tasks using task tracking BEFORE starting; mark one `in_progress` and `completed` immediately — why: long story files exhaust context and lose findings without external tracking.
**MANDATORY IMPORTANT MUST ATTENTION** estimation is bottom-up — phase hours drive `man_days_traditional` (`Σh/6 × productivity_factor`), SP DERIVED never the driver; run the Blast Radius pre-pass and compute `test_count` explicitly per driver — NEVER hand-wave "+tests" (the #1 failure) — why: SP-first estimates anchor to a guess, not the work.
**MANDATORY IMPORTANT MUST ATTENTION** emit the full estimate frontmatter — `story_points`, `complexity`, `man_days_traditional`, `man_days_ai`, `risk_margin_pct`, `risk_factors`, `blast_radius`, `estimate_scope_*`, `estimate_reasoning` (UI vs backend cost driver) — why: downstream `$prioritize` and `$plan` read these fields, blanks block them.
**MANDATORY IMPORTANT MUST ATTENTION** write min 3 GWT scenarios (happy + edge + error) PLUS a mandatory authorization scenario per story; every criterion has exactly ONE observable interpretation — why: a vague or single-scenario story ships untested edge/error/auth paths.
**MANDATORY IMPORTANT MUST ATTENTION** slice VERTICALLY (thin end-to-end), NEVER horizontally (backend/frontend split) — why: horizontal slices delay deliverable user value.
**MANDATORY IMPORTANT MUST ATTENTION** search existing component libraries and domain vocabulary BEFORE proposing new components/entities (>=80% match = reuse); use the project's own entity names — why: duplicate UI/domain code = wrong tier and fragments the codebase.
**MANDATORY IMPORTANT MUST ATTENTION** cite `file:line` (or grep/graph) evidence with a confidence % for every claim about existing code/entities — >80% to act, <80% verify first — why: AI hallucinates entity/API names; unverified scoping mis-slices the story.
**MANDATORY IMPORTANT MUST ATTENTION** validate stories with the user by asking the user directly before handoff — NEVER auto-decide slicing/scope/effort — why: silent assumptions on ambiguous scope ship the wrong stories.
**MANDATORY IMPORTANT MUST ATTENTION** add a final review todo task to verify every story against its AC scenarios, the dependency table, and the Quality Checklist.

**Anti-Rationalization:**

| Evasion                                 | Rebuttal                                                                                                            |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| "Story is small, skip SPIDR/estimate"   | SP >8 MUST split, >5 SHOULD — and SP is DERIVED from bottom-up hours, not eyeballed. Estimate.                      |
| "Tech notes need the class name"        | Source identifiers belong only in evidence carriers as `[Source: namespace/service/id]` — never in prose (M1/M2).   |
| "Happy path is enough"                  | Min 3 scenarios + a mandatory authorization scenario per story. Edge + error + auth are NOT optional.               |
| "+tests covers the test cost"           | Compute `test_count` explicitly per driver (auth matrix, validation, states). Hand-wave is the #1 estimate failure. |
| "Independent story, skip the dep table" | No orphan stories — every story appears in the dependency table, even if `independent`.                             |
| "Slicing is obvious, skip validation"   | ask the user directly validation is MANDATORY, not optional. The user confirms slicing/scope/effort.                |

**IMPORTANT MUST ATTENTION** AI-SDD M1-M5/M7 (tech-agnostic + demoable) + dependency table + bottom-up estimate are the three rules this skill must never skip — re-anchored here (recency) and in the Quick Summary (primacy).

**MANDATORY IMPORTANT MUST ATTENTION** READ the project-reference docs named in the Quick Summary blockquote BEFORE starting — `project-structure-reference.md`, `docs/project-reference/domain-entities-reference.md` (business entities/models), `docs/specs/` (existing TCs for related features) — plus the Frontend/UI Context docs when the PBI touches UI. File not found → search for the project's documentation, coding standards, and architecture docs instead — why: story scoping that guesses at entity names and module structure mis-slices the work.

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break it into small todo tasks and sub-tasks using task tracking.

> **[IMPORTANT]** Analyze how big the task is and break it into many small todo tasks systematically before starting — this is very important.

<!-- CODEX:SYNC-PROMPT-PROTOCOLS:START -->

## Hookless Prompt Protocol Mirror (Auto-Synced)

Source: `.claude/.ck.json` + `.claude/skills/shared/sync-inline-versions.md` (`:full` blocks) + `.claude/scripts/lib/hookless-prompt-protocol.cjs`

## [WORKFLOW-EXECUTION-PROTOCOL] [BLOCKING] Workflow Execution Protocol — MANDATORY IMPORTANT MUST CRITICAL. Do not skip for any reason.

**Generic portability boundary:** Reusable skills and protocol text stay project-neutral; project-specific conventions are discovered from docs/project-config.json and docs/project-reference/. Apply shared AI-SDD from `shared/sdd-artifact-contract.md`. Read `docs/project-config.json` and `docs/project-reference/docs-index-reference.md`, then open the project reference docs named there. For spec, test-case, behavior-change, public-contract, or `docs/specs/` work, route through the local spec docs named by the docs index: `feature-spec-reference.md`, `spec-system-reference.md`, `spec-principles.md`, and `workflow-spec-test-code-cycle-reference.md` when specs/tests/code must stay synchronized. If either file or a required reference doc is missing or stale, auto-run `$project-init` (or the narrow lower-level route such as `$project-config`, `$docs-init`, `$scan-all`, or `$scan --target=<key>`) before ordinary project-specific work. Any supported AI tool may execute when this shared context and local docs are available.

1. **DETECT:** If the prompt starts with an explicit slash skill/workflow command, execute it directly. Otherwise match the prompt against the workflow catalog and skill list.
2. **ANALYZE:** Choose the best option: execute directly, invoke a skill, activate a standard workflow, or compose a custom step combination.
3. **AUTO-SELECT:** Pick the best option yourself. Do not ask the user to choose between direct execution, skill, standard workflow, or custom workflow.
4. **ACTIVATE:** For a selected workflow, call `$start-workflow <workflowId>`; for a selected skill, invoke that skill; for a custom workflow, sequence custom steps directly; for direct execution, proceed with the task.
5. **CREATE TASKS:** task tracking for ALL workflow/skill/custom steps before execution when the selected path has multiple steps.
6. **PARALLELIZE:** Before executing the task list, tag each task `PAR` (independent inputs + write set disjoint from every other `PAR` task) or `SEQ` (name the blocking dependency), group `PAR` tasks into waves, declare the wave plan, and spawn each wave's sub-agents in ONE message — all-return barrier per wave, fan-out one level deep unless a sub-agent's own definition authorizes further fan-out. Sequential-by-default is a defect when tasks are independent; do not parallelize shared write targets, output-consuming tasks, trivial single-file work, ordering a skill or workflow explicitly fixes, or user-approval gates.
7. **EXECUTE:** Advance per the **Workflow Step Advancement & Parallel Phases** rule in your context instructions — model-driven; a sub-agent completion advances a step identically to an inline call; a parallel-phase group is an all-return barrier (advance only after ALL members return, never serialize it)

## Shared AI-SDD Protocol Markers

Source: `.claude/skills/shared/sync-inline-versions.md`

## SYNC:ai-sdd-artifact-contract

> **AI-SDD Artifact Contract** — Shared spec-driven development rules stay portable and source-owned.
>
> 1. Keep reusable AI-SDD principles in `.claude`; put repository-specific paths, commands, owners, products, and formats in project config/reference docs.
> 2. Preserve cycle: `spec -> plan -> tasks -> implement -> verify -> update spec/docs`.
> 3. Trace every requirement or invariant through decision, task, TC/test, source evidence, and docs/spec update.
> 4. Treat code-to-spec extraction as reference-only until accepted by the canonical spec owner.
> 5. Any supported AI tool may plan, implement, review, or verify with synced context; using multiple tools is optional.
> 6. Update `.claude` source first, then sync generated mirrors; do not manually edit `.agents`, `.codex`, or `AGENTS.md`. — why: mirrors are generated artifacts; hand-edits are overwritten on the next sync
> 7. If `docs/project-config.json`, root instruction files, or a required project-reference doc is missing or stale, auto-run `$project-init` or the narrow lower-level route before ordinary project-specific work.
>
> **Active reference:** `shared/sdd-artifact-contract.md` in the active skills root.

---

## SYNC:ai-sdd-artifact-contract:reminder

- **MANDATORY** Apply `shared/sdd-artifact-contract.md`; keep reusable AI-SDD in `.claude` and local rules in project docs.
- **MANDATORY** Code-to-spec extraction is reference-only until canonical acceptance; any supported AI tool may execute with synced context.
- **MANDATORY** Update `.claude` source before syncing generated mirrors; do not manually edit `.agents`, `.codex`, or `AGENTS.md`.
- **MANDATORY** Missing or stale project config, root instruction files, or required reference docs route project-specific work through `$project-init` or the narrow setup route automatically.
  **[TASK-PLANNING] [MANDATORY]** BEFORE executing any workflow or skill step, create/update task tracking for all planned steps, then keep it synchronized as each step starts/completes.

## [LESSON-LEARNED-REMINDER] [BLOCKING] Task Planning & Continuous Improvement — MANDATORY. Do not skip.

Break work into small tasks (task tracking) before starting. Add final task: "Analyze AI mistakes & lessons learned".

**Extract lessons — ROOT CAUSE ONLY, not symptom fixes:**

1. Name the FAILURE MODE (reasoning/assumption failure), not symptom — "assumed API existed without reading source" not "used wrong enum value".
2. Generality test: does this failure mode apply to ≥3 contexts/codebases? If not, abstract one level up.
3. Write as a universal rule — strip project-specific names/paths/classes. Useful on any codebase.
4. Consolidate: multiple mistakes sharing one failure mode → ONE lesson.
5. **Recurrence gate:** "Would this recur in future session WITHOUT this reminder?" — No → skip `$learn`.
6. **Auto-fix gate:** "Could `$code-review`/`$code-simplifier`/`$security-review`/`$lint` catch this?" — Yes → improve review skill instead.
7. BOTH gates pass → ask user to run `$learn`.
   **[CRITICAL-THINKING-MINDSET]** Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
   **Anti-hallucination principle:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.
   **AI Attention principle (Primacy-Recency):** Put the 3 most critical rules at both top and bottom of long prompts/protocols so instruction adherence survives long context windows.
   **Goal-driven execution:** Define success criteria first, loop until verified, and stop only when observable checks pass.
   **Tests verify intent:** Tests must protect business rules/invariants and fail when the protected intent breaks, not only mirror current behavior.

## Common AI Mistake Prevention (System Lessons)

- **Re-read files after context compaction.** Edit requires prior Read in same context; compaction wipes read state. Re-read before editing.
- **Grep for old terms after bulk replacements.** AI over-trusts find/replace completeness. Grep full repo after bulk edits for missed refs in docs/configs/catalogs.
- **Check downstream references before deleting.** Deletions cascade doc/code staleness. Map referencing files before removal.
- **After memory loss, check existing state before creating new.** Compaction wipes prior-work memory. Query current state to resume — never blindly duplicate.
- **Verify AI-generated content against actual code.** AI hallucinates APIs, class names, method signatures. Grep to confirm existence before documenting/referencing.
- **Trace full dependency chain after edits.** Changing a definition misses downstream consumers. Trace the full chain.
- **When renaming, grep ALL consumer file types.** Some file types silently ignore missing refs (no compile error). Search code, templates, configs, generated files.
- **Trace ALL code paths when verifying correctness.** Code existing ≠ code executing. Trace early exits, error branches, conditional skips — not just happy path.
- **Update docs that embed canonical data when source changes.** Docs inlining derived data (workflows, schemas, configs) go stale silently. Update all embedding docs alongside source.
- **Verify sub-agent results after context recovery.** Background agents may finish while parent compacted — grep-verify output, don't trust assumed completion.
- **Cross-check full target list against sub-agent assignments.** Parallel sub-agents by category miss boundary items. Reconcile union of assignments against target list before proceeding.
- **Sub-agents inherit knowledge only from their agent .md definition — use custom agent types, not built-in Explore.** Tool adoption = permission + knowledge + enforcement (numbered workflow step).
- **Persist sub-agent findings incrementally, not as a final batch.** Long sub-agents hit cutoffs before final write — findings lost. Instruct append-per-section to report file.
- **When debugging, ask "whose responsibility?" before fixing.** Trace caller (wrong data) vs callee (wrong handling). Fix at responsible layer — never patch symptom site.
- **Test failure → record a provisional verdict before trace/edit, then investigate.** Use the full five-way taxonomy: SOURCE-WRONG (production violates intent), TEST-WRONG (assertion/setup is stale), TEST-NOT-OPTIMAL (valid but fragile or low-signal test), ENVIRONMENT-BLOCKED (external state prevents a verdict), or AMBIGUOUS (intent/evidence cannot choose safely). Then trace root cause and triangulate against the governing spec (`docs/specs/**` if one exists) AND source. NEVER weaken an assertion, add a skip, relax a timeout, or change source merely to force green.
- **Grep ALL removed names after extraction/refactoring.** Primary file "done" ≠ secondary files clean. Grep entire scope for every removed symbol before declaring complete.
- **Assume existing values are intentional — ask WHY before changing OR flagging one as a defect.** Pattern-matching as "wrong" skips context. Before changing or reporting any constant/limit/flag/cutoff: read comments, git blame, the CALLER's ordering (the guarantee that makes the value correct usually lives in code running immediately BEFORE the cited line), and 2+ sibling call sites of the same convention. A doc stating WHAT without WHY is missing rationale, not proof of a missing guard — and in a validation pass, an accurate `file:line` citation proves the transcription, never the defect.
- **Verify ALL affected outputs, not just the first.** One build green ≠ all green. Multi-stack changes (backend/frontend/tests/docs) require verifying EVERY output.
- **Evaluate fit before copying a nearby pattern.** Closest example ≠ matching preconditions — verify the new context shares the same constraints, base classes, scope, lifetime.
- **Holistic-first debugging — resist nearest-attention trap.** Don't dive into first plausible cause. List EVERY precondition (config, env vars, paths, DB, endpoints, creds, versions, DI, data). Verify each against evidence (grep/query — not reasoning). Ask "what would falsify this?" — if nothing, it's not a hypothesis. Most expensive failure: going deeper in "obvious" layer while bug sits in layer never questioned.
- **Surgical changes — apply the diff test (context-aware).** Two modes: (1) Bug fix → every line traces to the bug; no restyling; orphan cleanup only for imports YOUR changes made unused. (2) Review/enhancement → implement improvements AND announce as "Enhancement beyond main request: [what]". Never silently scope-creep. Diff test: "Would this line exist if I wasn't asked to do X?" — if no, delete or announce.
- **Surface ambiguity before coding — don't pick silently.** Multiple valid interpretations → present each with effort: "[Request] could mean (1) [N h], (2) [N h]. Which matters?" List scope/format/volume/constraints assumptions first. If simpler path exists, say so. Never silently pick.
- **[MANDATORY FIRST ACTION] ALWAYS activate a suitable skill or workflow BEFORE responding.** Match task against workflow catalog + skill list; invoke via skill invocation or `$start-workflow <workflowId>`. NEVER answer or write code before checking. Skip = protocol violation.
- **Why-Review adversarial mindset — apply when reviewing any plan, decision, or design.** Default SKEPTIC not VALIDATOR: steel-man a rejected alternative, invert each stated reason ("what does it sacrifice?"), stress-test top 2-3 assumptions, run pre-mortem ("ships, fails in 3 months — what breaks?"), surface 1-2 alternatives author missed. Section presence ≠ quality; quality = causal reasoning + concrete mitigations + evidence, not "it's better" or "monitor closely".
- **Front-load report-write in sub-agent prompts for large reviews.** Many-file sub-agents hit budget before final write — findings lost. Design prompts so: (1) report-write is first explicit deliverable, (2) append per-file/section (not batched), (3) scope bounded so reads don't exhaust budget. Truncated mid-sentence with no report file → spawn narrower scope, don't retry same prompt.
- **After context compaction, re-verify all prior phase outcomes before continuing.** Summaries describe intent, not environment state (git index, filesystem, processes). On resume, FIRST audit: git status, re-read modified files, verify filesystem. Every "completed" claim is an untested hypothesis until evidence confirms.
- **OOM/memory: check row count before row size.** Triage: (1) Unbounded query — no DB filter for trigger? Push filter to DB; eliminates OOM. (2) Large rows? Projection reduces proportionally. Row reduction > projection in ROI.
- **Assert the outcome your system OWNS, never the intermediate state your INFRASTRUCTURE owns.** When testing anything asynchronous (queue/broker delivery, retries, background jobs, caches, replication), assert the final business/entity state. NEVER assert the delivery bookkeeping — consume/send status, attempt counts, last-error, row existence or counts in a broker, scheduler, or outbox/inbox table. That bookkeeping lives in shared infrastructure that ANY co-running process (a peer worker, a second replica, a leftover local container) can write, usually under a deterministic shared key, so the assertion silently tests the developer's environment instead of the system: green when run alone, flaky the instant anything else shares that broker + database. Gate question for every assertion: "would this hold no matter WHICH process did the work?" — if no, assert the converged data state instead. Corollary: process-local fault injection and in-process telemetry cannot gate work any process may perform — use them as stress amplifiers (arm → bounded window → disarm → assert convergence), never as preconditions.
- **Keep domain concepts out of generic/shared/infrastructure layers.** Reusable layer (shared library, framework, infra module) must reference NO consumer-specific domain concept — tenant/customer/product IDs, business entities, feature rules. Leak compiles + runs → passes review silently while coupling the "reusable" layer to one consumer. Keep shared type domain-free; push domain fields/logic down into the consumer via subclass/composition. — why: a layer coupled to one consumer's domain is no longer reusable.

<!-- CODEX:SYNC-PROMPT-PROTOCOLS:END -->
