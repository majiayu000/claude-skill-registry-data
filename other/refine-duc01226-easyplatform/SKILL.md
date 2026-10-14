---
name: refine
description: '[Project Management] Use when converting ideas to PBIs, validating problem hypotheses, adding acceptance criteria, or refining requirements.'
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

**Goal:** Transform raw ideas into a Definition-of-Ready PBI using BA best practices, hypothesis validation, and domain research — problem-validated, tech-agnostic, with testable acceptance criteria, estimates, and a Dependencies table — so a team can build it without re-asking what or why.

**Summary:**

- **Purpose:** turn a raw idea into a groomable, Definition-of-Ready PBI a team can build without re-asking what or why.
- **Main steps — run in order, track EACH (AI keeps forgetting sub-phases):** Phase 0 locate active plan → 1 idea intake + module detect → 2 domain research → 3 problem-hypothesis validation (GATE) → 4 BABOK elicitation → 5 BDD acceptance criteria → 5.1 AI-SDD M1-M5/M7 gate (BLOCKING) → 5.5 testability assessment → 6 prioritization + draft estimate → 7 validation interview (GATE, 3-5 Qs) → 7.5 RE-DERIVE estimate vs locked scope → 8 PBI artifact generation.
- Two gates are NON-OPTIONAL: validate the problem hypothesis (Phase 3) before building, and run the 3-5 question validation interview (Phase 7) before writing the PBI — the user decides assumptions, scope, and dependencies, never the AI.
- Acceptance criteria are BDD GIVEN/WHEN/THEN (min 3: happy/edge/error) and MUST satisfy the AI-SDD M1-M5 and M7 gate (Phase 5.1): tech-agnostic Business Intent, logical FR-/BR- IDs first, observable single-interpretation ACs, rebuild-from-scratch validity, and every AC demoable as a business outcome (M7).
- Estimate twice: Phase 6 drafts story points/man-days against draft scope, then Phase 7.5 RE-DERIVES them against the locked post-interview scope (per SYNC:estimation-framework) — shipping stale Phase 6 numbers is the cardinal failure.
- The PBI frontmatter MUST carry `story_points`, `complexity`, `man_days_traditional`, `man_days_ai`, and every PBI MUST include a complete Dependencies table (`must-before`/`can-parallel`/`blocked-by`/`independent`).

**Workflow:**

| Phase | Name                      | Key Activity                             | Output                 |
| ----- | ------------------------- | ---------------------------------------- | ---------------------- |
| 0     | Locate Active Plan        | Load `plan.md` if in workflow            | Plan context           |
| 1     | Idea Intake               | Load artifact, detect module             | Context loaded         |
| 2     | Domain Research           | WebSearch market/competitors             | Research summary       |
| 3     | Problem Hypothesis (GATE) | Validate problem exists                  | Confirmed hypothesis   |
| 4     | Elicitation               | Apply BABOK techniques                   | Requirements extracted |
| 5     | Acceptance Criteria       | Write BDD scenarios                      | GIVEN/WHEN/THEN        |
| 5.1   | AI-SDD Gate (M1-M5/M7)    | Tech-agnostic, FR/BR IDs first, demoable | Mandate-compliant ACs  |
| 5.5   | Testability               | Test approach + per-AC outlines          | Test seed for `$spec`  |
| 6     | Prioritization            | RICE/MoSCoW + DRAFT Story Points         | Priority + draft est.  |
| 7     | Validation (GATE)         | Interview user (MANDATORY, 3-5Q)         | Assumptions confirmed  |
| 7.5   | Re-estimate               | RE-DERIVE vs LOCKED scope                | Final estimate         |
| 8     | PBI Generation            | Create artifact                          | PBI file saved         |

**Key Rules:**

- NEVER skip hypothesis validation for new features
- Validation interview NOT optional — always ask 3-5 questions
- Use project domain-specific vocabulary when available
- MUST ATTENTION include `story_points`, `complexity`, `man_days_traditional`, `man_days_ai` in PBI frontmatter
- Every PBI MUST ATTENTION include Dependencies table — types: `must-before` | `can-parallel` | `blocked-by` | `independent`
- `docs/specs/` — read existing TCs for related features; recommend test spec generation for new PBIs
- `docs/project-reference/domain-entities-reference.md` — read when task involves business entities/models

---

## Frontend/UI Context (if applicable)

- Component patterns: `docs/project-reference/frontend-patterns-reference.md`
- Styling/BEM guide: `docs/project-reference/scss-styling-guide.md`
- Design system tokens: `docs/project-reference/design-system/README.md`

---

## Greenfield Mode

> **Auto-detected:** No discovered source directories and no manifest files found. Planning artifacts (docs/, plans/, .claude/) don't count.

**When greenfield detected:**

1. Skip existing backlog refinement (no backlog exists)
2. Enable DDD domain modeling: bounded contexts, aggregates, entities, value objects
3. Capture constraints: team skills, expected scale, hosting preferences, budget — as input signals only
4. Use WebSearch for market research + competitor analysis
5. Output domain model artifact alongside PBI artifact
6. Increase ask the user directly frequency — validate domain boundaries, entity relationships, business rules
7. **[CRITICAL] NEVER ask about tech stack during refinement.** Tech stack decided after business analysis. Capture team skills + scale expectations as signals only.

**Be skeptical. Every claim needs traced proof, confidence >80%.**

---

## Phase 0: Locate Active Plan (if in workflow)

If running in workflow (big-feature, greenfield-init, etc.):

1. Glob `plans/*/plan.md` sorted by modification time, or check the current task list for plan context
2. Read `plan.md` — project scope, goals, architecture decisions, domain model
3. Read existing research — `{plan-dir}/research/*.md` for business evaluation, domain analysis
4. Read `docs/project-reference/domain-entities-reference.md` (if exists) — existing domain entities
5. Use plan context — don't re-ask questions answered in prior steps

## Phase 1: Idea Intake & Context Loading

1. Read idea artifact from path or find by ID in `team-artifacts/ideas/`
2. Extract: problem statement, value proposition, target users, scope
3. Check `module` field; if absent, detect via keywords or prompt user

---

## Phase 2: Domain Research

**Trigger:** New domain, unclear competitors, `--research` flag.
**Skip:** Internal tooling, well-understood domain, time-constrained.

Use WebSearch with domain terms. Summarize in max 3 bullets (market context, competitors, best practices).

---

## Phase 3: Problem Hypothesis Validation

Validate hypothesis with user by asking the user directly. 42% of startups fail from no market need — validate before building.

**Skip:** `--skip-hypothesis`, validated hypothesis exists, bug fix/tech debt.

### Problem Hypothesis Template

```markdown
**We believe** [target users/persona]
**Experience** [specific problem]
**Because** [root cause]
**We'll know this is true when** [validation metric/evidence]
```

### Value Hypothesis Template

```markdown
**We believe** [feature/solution]
**Will deliver** [value/benefit]
**To** [target users]
**We'll know we're right when** [success metric]
```

### Validation Process

1. Draft hypothesis from idea content
2. Use ask the user directly to validate:
    - "Is this the core problem we're solving?"
    - "Who exactly experiences this? How often?"
    - "What evidence do we have this problem exists?"
3. Validated → proceed to elicitation
4. Invalidated → return idea for clarification

---

## Phase 4: Requirements Elicitation (BABOK Core 5)

**Think:** What information gaps exist? Which technique fills them with least effort + highest confidence?

| Technique             | When to Choose                                      | What to Extract                                 |
| --------------------- | --------------------------------------------------- | ----------------------------------------------- |
| **Interviews**        | Deep insights needed, stakeholder perspectives vary | Stakeholder needs, pain points, constraints     |
| **Workshops**         | Group consensus needed, multiple stakeholders       | Prioritized requirements, consensus decisions   |
| **Document Analysis** | Existing systems/processes, regulatory requirements | As-is state, compliance requirements, gaps      |
| **Observation**       | Users can't articulate needs, workflow unclear      | Actual vs stated workflow, hidden requirements  |
| **Prototyping**       | Visual validation needed, UI/UX requirements vague  | Validated UI requirements, interaction patterns |

**Technique notes:**

- Interviews: Open-ended questions (why, how, what-if) → active listening → follow-up on unexpected → document verbatim quotes
- Workshops: Define agenda + 90 min timebox → neutral facilitator → round-robin/silent voting → document decisions AND dissent
- Observation: Shadow users → note workarounds/pain points → don't interrupt → ask clarifying questions afterward

---

## Phase 5: Acceptance Criteria (BDD Format)

Write GIVEN/WHEN/THEN scenarios. Minimum 3: happy path, edge case, error case.

```gherkin
Scenario: {Descriptive title}
  Given {precondition/context}
    And {additional context}
  When {action/trigger}
    And {additional action}
  Then {expected outcome}
    And {additional verification}
```

| Practice                  | Rule                              |
| ------------------------- | --------------------------------- |
| Single trigger            | "When" clause has ONE action      |
| 3 scenarios minimum       | Happy path, edge case, error case |
| No implementation details | Behavior, not how                 |
| Testable outcomes         | "Then" must be verifiable         |
| Stakeholder language      | No technical jargon               |

### Example Scenarios

```gherkin
Scenario: User creates invoice with valid data
  Given user has permission to create invoices
    And user is on the invoice creation page
  When user submits invoice form with all required fields
  Then invoice is created with status "Draft"
    And invoice appears in user's invoice list

Scenario: Invoice creation fails with missing required field
  Given user is on the invoice creation page
  When user submits form without title
  Then validation error "Title is required" is displayed
    And invoice is not created

Scenario: Approver reviews a submitted invoice
  Given approver has invoices awaiting approval
    And an invoice has been submitted for approval
  When approver opens the invoice review page
  Then the invoice is visible with "Pending Review" status
```

### Project Test Case Format

- **Format:** `TC-{FEATURE}-{NNN}` (e.g., TC-GM-001)
- **Evidence:** `[Source: namespace/service/id]` abstract-anchor format (never `file:line`)
- See `business-analyst` skill for detailed patterns

---

### Phase 5.1: AI-SDD Mandate Gate (M1-M5 and M7) — BLOCKING

See `.claude/skills/shared/sdd-artifact-contract.md` → "AI-SDD Mandates (M1-M7)" for BLOCKING criteria. The generated PBI MUST satisfy M1-M5 and M7 or be reworked before Phase 8 writes it:

- **Separate intent from implementation (M1/M2):** Keep a tech-agnostic **Business Intent** narrative (Description, Business Value, Acceptance Criteria) free of framework/product/language/design-pattern names and source identifiers. Put any optional implementation hints in a clearly separated **Implementation Notes** block, and put source references only in evidence carriers (`[Source: namespace/service/id]`, `**Evidence**`). Prose stays tech-agnostic per `docs/project-reference/spec-principles.md` §3.
- **Logical Requirement ID first (M3):** Assign each requirement a logical ID (`FR-`/`BR-`) as the PRIMARY citation spine; keep `[Source: namespace/service/id]` abstract-anchor evidence (never physical code coordinates or repository-root paths — those live only in the provenance sidecar) as a SECONDARY carrier in a separate evidence column/section — KEEP it, never remove it.
- **Testable, observable acceptance criteria (M4):** Every acceptance criterion has ONE valid interpretation, observable completion states, named failure modes, and NO implementation details. Reject vague phrasing ("handle appropriately", "fast", "user-friendly").
- **Rebuild-from-scratch validation (M5):** Before emitting, confirm a competent team with zero codebase knowledge could re-implement identical business behavior on ANY stack from the PBI alone. If a reader would have to guess a rule, limit, role, or failure mode, add it as a clarification — never guess.
- **Business-visibility (M7):** Apply the demo test to each acceptance criterion's BODY: _"what would a stakeholder SEE change?"_ — no answer → FAIL as TECHNICAL-ONLY and drop it from the PBI. Every `GIVEN` = a state a user could arrange; every `WHEN` = an action a user could take; every `THEN` = an outcome a user could see. FAIL a `WHEN` that is an invocation (a handler runs, a consumer receives, a job fires, data syncs) or a `THEN` asserting schema/type/nullability/call-count. Judge the BODY, never the AC's title or ID. Never derive the AC count from an architecture inventory (handlers, consumers, jobs) — that count moves when the system is re-architected though no business behavior changed, falsifying M5.

> **M1 governs vocabulary; M7 governs subject matter.** A technical AC in impeccably tech-free prose satisfies M1 while violating M7 — _"the system correctly synchronizes the record"_ names no framework and is still a technical case in a business costume. That gap is the most common way business specs rot. Ask what a user could SEE, not which words were used.

---

### Phase 5.5: Testability Assessment

Use ask the user directly with 2-3 questions:

1. "Which testing approach fits this PBI?"
    - TDD-first: Write test specs before implementation (Recommended for complex features)
    - Implement-first: Build feature, then create test specs
    - Parallel: Spec and implement simultaneously

2. "What test levels are needed?"
    - Integration tests only (Recommended for backend CQRS)
    - Integration + E2E
    - Unit + Integration + E2E

For EACH acceptance criterion, generate corresponding test case outline:

| AC   | Test Outline                                               | Priority |
| ---- | ---------------------------------------------------------- | -------- |
| AC-1 | TC: Create invoice with valid data → verify persisted      | P0       |
| AC-2 | TC: Create invoice without title → verify validation error | P1       |

Seed for `$spec [mode=tests]` if user chooses TDD-first. Document in PBI under `## Testability Assessment`.

---

## Phase 6: Prioritization & Estimation

Apply RICE score or MoSCoW for priority. Estimate using **Story Points (Modified Fibonacci 1-21)**.

### Quick RICE Score

```
Score = (Reach x Impact x Confidence) / Effort

Reach: Users affected per quarter (100, 500, 1000+)
Impact: 0.25 (minimal) | 0.5 (low) | 1 (medium) | 2 (high) | 3 (massive)
Confidence: 0.5 (low) | 0.8 (medium) | 1.0 (high)
Effort: Story points (1, 2, 3, 5, 8, 13, 21)
```

### MoSCoW Categories

| Category        | Meaning                  | Action              |
| --------------- | ------------------------ | ------------------- |
| **Must Have**   | Critical, non-negotiable | Include in MVP      |
| **Should Have** | Important but not vital  | Plan for release    |
| **Could Have**  | Nice to have, low effort | If time permits     |
| **Won't Have**  | Out of scope this cycle  | Document for future |

---

## Phase 7: Validation Interview (MANDATORY)

Generate 3-5 questions covering assumptions, scope, dependencies, edge cases. Use ask the user directly. Document in PBI. **NOT optional.**

| Category            | Example Question                                                            |
| ------------------- | --------------------------------------------------------------------------- |
| **Assumptions**     | "We assume X is true. Correct?"                                             |
| **Scope**           | "Should Y be included or explicitly excluded?"                              |
| **Dependencies**    | "This requires Z. Is that available?"                                       |
| **Edge Cases**      | "What happens when data is empty/null?"                                     |
| **Business Impact** | "Will this affect existing reports/workflows?"                              |
| **Entities**        | "Create new entity or extend existing X?"                                   |
| **Prod Readiness**  | "Does this feature need linting, error handling, loading, or Docker setup?" |
| **Authorization**   | "Who can perform this action? What roles/permissions are needed?"           |
| **Seed Data**       | "Does this feature need reference/lookup data to function?"                 |
| **Data Migration**  | "Does this change entity schema? Is data transformation needed?"            |

1. Generate 3-5 questions from assumptions, scope, dependencies
2. Use ask the user directly to interview
3. Document in PBI under `## Validation Summary`
4. Update PBI based on answers

### Validation Output Format

```markdown
## Validation Summary

**Validated:** {date}

### Confirmed Decisions

- {decision}: {user choice}

### Assumptions Confirmed

- {assumption}: Confirmed/Modified

### Open Items

- [ ] {follow-up items}
```

---

## Cross-Cutting & Production Readiness

> Capture in PBI template sections: Production Readiness Concerns, Authorization & Access Control, Seed Data, Data Migration.

---

## Phase 7.5: Re-evaluate Estimation (MANDATORY — runs after Validation Interview)

> **Why this phase exists:** Phase 6 estimation runs against a draft scope. Phase 7 (Validation Interview) and Cross-Cutting capture often resolve unknowns, add constraints, or trim/expand scope. The numbers in `story_points`, `complexity`, `man_days_traditional`, `man_days_ai` MUST be re-derived against the locked scope BEFORE Phase 8 writes them into the PBI frontmatter. Estimating once at draft and forgetting is the #1 source of estimation drift in PBIs.

### Inputs (locked by end of Phase 7)

- Confirmed assumptions, scope inclusions/exclusions
- Authorization, seed data, migration, prod-readiness decisions
- Newly discovered dependencies or edge cases
- Any rescoping the user requested during validation

### Re-derive (per `SYNC:estimation-framework`)

1. Walk the **locked** scope acceptance criteria + cross-cutting concerns; assign hours per slice.
2. `bottom_up_hours = Σ slice_hours` (use the SP table mapping in Phase 6, not eyeballing).
3. `likely_days = ceil(bottom_up_hours / 6)` × productivity factor for the team/AI mode.
4. Recompute `risk_margin_pct` based on remaining unknowns AFTER Phase 7 (margin should usually shrink because validation removed unknowns; rises only if new risks surfaced).
5. Recompute `min-max range` from the new likely_days ± margin.
6. Re-pick the closest Fibonacci `story_points` and `complexity` bucket from the re-derived likely_days.

### Compare against Phase 6 draft estimate

Compute `delta_pct = (new_likely_days - draft_likely_days) / draft_likely_days × 100`.

| Delta             | Action                                                                                                                                                                                                                                                                                                                             |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `\|delta\| ≤ 20%` | Keep draft estimate. Note `reestimate_delta_pct: <signed>` + `reestimate_reason: "within tolerance, no change"` in PBI frontmatter for transparency.                                                                                                                                                                               |
| `\|delta\| > 20%` | UPDATE `story_points`, `complexity`, `man_days_traditional`, `man_days_ai`. Add `reestimate_delta_pct: <signed>` + 1-line `reestimate_reason` explaining what changed (e.g., "auth scope confirmed wider", "seed data dropped per validation").                                                                                    |
| `\|delta\| > 50%` | UPDATE values AND flag `SHOULD-RESCOPE`. Surface to user by asking the user directly BEFORE Phase 8 writes the PBI: "Re-estimate is +/-X% vs original. Options: (a) accept new estimate as-is, (b) split into 2 PBIs, (c) trim scope back to original estimate, (d) defer." Record the user's decision in `## Validation Summary`. |

### Output

- Updated estimation values (carry into Phase 8 frontmatter)
- New frontmatter fields: `reestimate_delta_pct`, `reestimate_reason` (always populate even when within tolerance — creates a paper trail for retrospective comparison against actual implementation time)
- If rescoped: updated acceptance criteria/scope sections reflecting the user's choice

> **Run this re-estimation phase against the locked scope — never skip it.** A PBI that ships with stale Phase 6 estimates is the source of unreliable velocity data. The whole point is to make the post-validation numbers — not the pre-validation guesses — the ones the team commits to.

---

## Phase 8: PBI Artifact Generation

**Path:** `team-artifacts/pbis/{YYMMDD}-pbi-{slug}.md` | **ID Pattern:** `PBI-{YYMMDD}-{NNN}`

> **Artifact Path (canonical convention)** — Command `$refine` → base path `team-artifacts/pbis/`, role token `ba`, type `pbi`. General filename pattern: `{YYMMDD}-{role}-{type}-{slug}.md` → e.g. `260119-ba-pbi-invoice-approval.md`. Slug = lowercased basename, non-alphanumeric → `-`, trimmed, max 50 chars.

### PBI Template

```markdown
---
id: PBI-{YYMMDD}-{NNN}
title: '{Brief descriptive title}'
module: '{ModuleName — detect from project-config.json modules[]}'
priority: Must Have | Should Have | Could Have | Won't Have
rank: { numeric 1-999, ascending — populated/updated by $prioritize during cross-PBI ranking; omit until prioritized }
story_points: 1 | 2 | 3 | 5 | 8 | 13 | 21
complexity: Low | Medium | High | Very High
man_days_traditional: '{ Xd (Yd code + Zd test) — from SP table }'
man_days_ai: '{ Xd (Yd code + Zd test) — from SP table with AI }'
status: draft | refined | ready | in_progress | done
rice_score: { calculated }
created: '{YYYY-MM-DD}'
source_idea: '{idea artifact path or ID}'
---

# {PBI Title}

> **Business Intent (tech-agnostic — M1/M2):** Description, Business Value, Business Rules, and Acceptance Criteria below describe observable business behavior only — no framework/product/language/design-pattern names, no source identifiers. Keep implementation hints in `## Implementation Notes` and source references in evidence carriers.

## Requirement IDs (M3 — logical-IDs-first)

| Logical ID   | Statement (tech-agnostic) | Evidence (secondary, re-anchorable)       |
| ------------ | ------------------------- | ----------------------------------------- |
| FR-{MOD}-XXX | {functional requirement}  | `[Source: path:line]` or `TBD (pre-impl)` |
| BR-{MOD}-XXX | {business rule}           | `[Source: path:line]` or `TBD (pre-impl)` |

## Description

**As a** {user role}
**I want** {capability}
**So that** {business value}

## Business Value

- {Quantified benefit 1}
- {Quantified benefit 2}

## Problem Hypothesis

**We believe** {target users}
**Experience** {specific problem}
**Because** {root cause}
**We'll know this is true when** {validation metric}

## Business Rules

- BR-{MOD}-XXX: {Rule description}

## Acceptance Criteria

### AC-1: {Title}

Scenario: {Happy path}
Given {context}
When {action}
Then {outcome}

### AC-2: {Title}

Scenario: {Edge case}
Given {edge state}
When {action}
Then {handling}

### AC-3: {Title}

Scenario: {Error case}
Given {context}
When {invalid action}
Then error "{message}"

## Testability Assessment

| AC   | Test Outline       | Priority |
| ---- | ------------------ | -------- |
| AC-1 | {test description} | P0       |
| AC-2 | {test description} | P1       |

## Out of Scope

- {Explicitly excluded item 1}
- {Explicitly excluded item 2}

## Dependencies

| Dependency            | Type         | Description                    |
| --------------------- | ------------ | ------------------------------ |
| {PBI/service/feature} | must-before  | {Why this must be done first}  |
| {PBI/service/feature} | can-parallel | {Why this can run in parallel} |
| {PBI/service/feature} | blocked-by   | {What blocks this PBI}         |
| -                     | independent  | {No dependencies — first item} |

## Production Readiness Concerns

| Concern                | Required        | Notes                                                                   |
| ---------------------- | --------------- | ----------------------------------------------------------------------- |
| Code linting/analyzers | Yes/No/Existing | {tool preference or "scaffold default"}                                 |
| Error handling setup   | Yes/No/Existing | {pattern: toast/inline/error-page}                                      |
| Loading indicators     | Yes/No/Existing | {pattern: spinner/skeleton/progress}                                    |
| Docker integration     | Yes/No/Existing | {scope: infra-only/full/none}                                           |
| CI/CD quality gates    | Yes/No/Existing | {mutation-score gate (line-coverage diagnostic only), lint enforcement} |
| Security scanning      | Yes/No/Existing | {dependency audit, SAST}                                                |

## Authorization & Access Control

| Role   | Can Create | Can Read | Can Update | Can Delete | Notes         |
| ------ | ---------- | -------- | ---------- | ---------- | ------------- |
| {Role} | ✅/❌      | ✅/❌    | ✅/❌      | ✅/❌      | {scope notes} |

**New permissions needed:** {Yes/No — list if yes}
**Multi-tenant isolation:** {Yes/No}

## Seed Data Requirements

| Data Type          | Description                          | Owner        | Required |
| ------------------ | ------------------------------------ | ------------ | -------- |
| Reference data     | {lookups, statuses, types}           | Application  | Yes/No   |
| Configuration data | {default settings}                   | Application  | Yes/No   |
| Test seed data     | {entities for integration tests}     | Test project | Yes/No   |
| Performance data   | {large-volume data for load testing} | Test tooling | Yes/No   |

> If no seed data needed: `N/A — no seed data required for this feature.`

## Data Migration

| Change                      | Type                                   | Backward Compatible | Reversible |
| --------------------------- | -------------------------------------- | ------------------- | ---------- |
| {schema change description} | Add field / Remove field / Type change | Yes/No              | Yes/No     |

> If no schema changes: `N/A — no schema changes required.`

## Domain Context

**Entities:** {Entity1}, {Entity2}
**Related Features:** {feature doc paths}

## Implementation Notes

> Optional, clearly separated from Business Intent. Implementation hints / source identifiers may appear here and in evidence carriers only — never in the tech-agnostic sections above. If none: `N/A — no implementation hints; rebuild from Business Intent + Requirement IDs.`

## UI Layout

**Design Spec:** {link to the `$design-spec` artifact — or inline UI specs ref — that owns this PBI's screen/component design. REQUIRED for any PBI with UI work. Produce it AFTER inventorying existing UI + connected flows (per `SYNC:existing-ui-research`) so it faithfully matches the current UI system. If backend-only: `N/A — Backend-only change. No UI affected.`}

### Wireframe

{ASCII wireframe using box-drawing characters}

**Layout:** {description with approximate proportions/dimensions}

### Components

- **{ComponentName}** — {behavior description} _(tier: common | domain-shared | page/app)_

> Classify per **Component Hierarchy** in UI wireframe protocol — search existing libs before proposing new components.

### States

| State   | Behavior                   |
| ------- | -------------------------- |
| Default | {what user sees initially} |
| Loading | {spinner/skeleton}         |
| Empty   | {empty state message}      |
| Error   | {error handling}           |

> If backend-only: `## UI Layout` → `N/A — Backend-only change. No UI affected.`

## Validation Summary

**Validated:** {date}

### Confirmed Decisions

- {decision}: {user choice}

### Assumptions Confirmed

- {assumption}: Confirmed/Modified

### Open Items

- [ ] {follow-up items}
```

---

## Anti-Patterns to Avoid

| Anti-Pattern                   | Better Approach                     |
| ------------------------------ | ----------------------------------- |
| Refining vague ideas           | Return to `$idea` for clarification |
| Skipping hypothesis validation | Always run Phase 3 for new features |
| Solution-first thinking        | Start with problem, not solution    |
| Generic acceptance criteria    | Use GIVEN/WHEN/THEN with specifics  |
| Ignoring domain context        | Load project docs if applicable     |
| Too large PBI (XL+)            | Break into smaller items            |
| Missing "Out of Scope"         | Explicitly list exclusions          |
| Assuming instead of asking     | Run validation interview            |

---

## Key Rules

- **Every PBI MUST ATTENTION include Dependencies table** — types: `must-before`, `can-parallel`, `blocked-by`, `independent`. Enables `$prioritize` and `$plan` to respect ordering.
- **No vague dependency descriptions** — Each dependency must specify concrete PBI, service, or feature and WHY relationship exists.

## BA Team Refinement Context (canonical)

> Applies to Writes/Edits under `team-artifacts/pbis/`, `.../stories/`, `team-artifacts/ideas/`. Mirrored for Codex via `SYNC:ba-team-decision-model` / `SYNC:refinement-dor-checklist` in AGENTS.md (do not hand-edit the mirror).

**Decision Model:** 2/3 majority vote (UX BA + Designer BA + Dev BA PIC). Dev BA PIC has technical veto.
**Disagree-and-Commit:** Once decided, everyone commits. No re-litigating.
**Grooming Override:** BA team decision changes only if >75% remaining team votes to override.

**Role Scopes:**

- **UX BA:** UI/UX flows, wireframes, interaction AC, user research
- **Designer BA:** Design feasibility, product thinking, visual design, equal vote
- **Dev BA PIC:** Technical feasibility review, AI pre-review, DoR gate, grooming presentation

**DoR Gate (ALL must pass before grooming):**

- [ ] User story template (As a... I want... So that...)
- [ ] AC testable (GIVEN/WHEN/THEN, no vague language)
- [ ] Wireframes attached (UX BA) + UI design ready (Designer BA)
- [ ] (UI PBIs) Design spec linked — `$design-spec` artifact or inline UI specs present in `## UI Layout`; backend-only PBIs exempt (`N/A — Backend-only`)
- [ ] AI pre-review passed (`$artifact-review --type=pbi` or `$pbi-challenge`)
- [ ] Story points estimated by AI
- [ ] Dependencies table complete

**Refinement Cadence:** Always one sprint ahead. Weekly meeting (60 min + ~3h async).
**Skills:** Use `$pbi-challenge` for collaborative review, `$dor-gate` before grooming.

## Definition of Ready (INVEST)

| Criterion           | Check                        |
| ------------------- | ---------------------------- |
| **I**ndependent     | No blocking dependencies     |
| **N**egotiable      | Details can be refined       |
| **V**aluable        | Clear user/business value    |
| **E**stimable       | Team can estimate (XS-XL)    |
| **S**mall           | Single sprint                |
| **T**estable        | 3+ GIVEN/WHEN/THEN scenarios |
| Problem Validated   | Hypothesis confirmed         |
| Domain Context      | BR/entity context loaded     |
| Stakeholder Aligned | Validation interview done    |
| Prod Readiness      | Concerns documented          |

---

## Project Integration

For domain PBIs: detect module from `docs/specs/` directory names, extract business rules from `docs/specs/{module}/`, load entity context from feature doc. Target 8-12K tokens for feature context.

---

## Related

- **Role Skill:** `business-analyst` (detailed patterns)
- **Input:** `$idea` output
- **Next Step:** `$story`, `$spec [mode=tests]` (Recommended for TDD), `$design-spec`
- **Prioritization:** `$prioritize`

---

## Next Steps

**MANDATORY IMPORTANT MUST ATTENTION** after completing this skill, use ask the user directly to present these options. NEVER skip because task seems "simple" or "obvious":

- **"$why-review (Recommended)"** — Validate design rationale, alternatives, risk assessment before `$story` or implementation
- **"$domain-analysis"** — If PBI creates/modifies domain entities, model bounded contexts before writing stories
- **"$story"** — Break PBI into implementable user stories
- **"$pbi-mockup"** — Generate HTML mockup from PBI
- **"$spec [mode=tests]"** — If using TDD approach
- **"Skip, continue manually"** — user decides

---

> **[IMPORTANT]** Use task tracking to break ALL work into small tasks BEFORE starting. Simple tasks: ask user whether to skip.

> **External Memory:** Complex/lengthy work → write findings to `plans/reports/` — prevents context loss.

> **Evidence Gate:** MANDATORY IMPORTANT MUST ATTENTION — every claim requires `file:line` proof or traced evidence, confidence >80% to act.

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

- **IMPORTANT MUST ATTENTION Goal:** transform a raw idea into a Definition-of-Ready PBI — problem-validated, tech-agnostic, with testable acceptance criteria, estimates, and a Dependencies table — so a team can build it without re-asking what or why.
- **IMPORTANT MUST ATTENTION — run + track EVERY step (AI forgets sub-phases):** Phase 0 locate active plan → 1 idea intake + module detect → 2 domain research → 3 problem-hypothesis GATE → 4 BABOK elicitation → 5 BDD acceptance criteria → 5.1 AI-SDD M1-M5/M7 BLOCKING gate → 5.5 testability → 6 prioritization + DRAFT estimate → 7 validation interview GATE → 7.5 RE-DERIVE estimate vs locked scope → 8 PBI generation — NEVER skip, reorder, or merge a phase without explicit user approval.

**Protocols in force — MUST ATTENTION (concise digest of the SYNC/shared blocks this skill carries):**

- **AI Mistake Prevention:** verify generated content against evidence, trace downstream references, verify all affected outputs, re-read after context loss, surface ambiguity.
- **UI System Context:** ALWAYS read frontend-patterns, scss-styling-guide, design-system before any UI change.
- **Estimation Framework:** bottom-up hours drive man-days; SP derived; UI cost usually dominates.
- **UI Wireframe:** ASCII layout, classify every component into ONE tier, reuse before creating.
- **Critical Thinking:** traced proof per claim, confidence >80% to act, NEVER guess.
- **Sequential Thinking:** multi-step Thought N/M with REVISION/BRANCH/HYPOTHESIS markers, confidence-% closer.

- **IMPORTANT MUST ATTENTION** Phase 3 problem-hypothesis validation + Phase 7 validation interview (3-5 questions) are NON-OPTIONAL for new features — user decides assumptions/scope/dependencies, AI NEVER auto-decides — why: 42% of products fail from no market need; a silent AI assumption ships an unvalidated build
- **IMPORTANT MUST ATTENTION** Phase 7.5 RE-DERIVES `story_points`/`complexity`/`man_days_traditional`/`man_days_ai` against the LOCKED post-interview scope (per `SYNC:estimation-framework`) — NEVER ship stale Phase 6 draft numbers — why: pre-validation guesses are the #1 source of unreliable velocity data
- **MANDATORY IMPORTANT MUST ATTENTION** break work into small tasks via task tracking BEFORE starting; mark one `in_progress`, complete it before the next; on context loss the current task list first — why: compaction wipes prior-work memory, resume don't duplicate
- **MANDATORY IMPORTANT MUST ATTENTION** validate decisions with user by asking the user directly — NEVER auto-decide
- **IMPORTANT MUST ATTENTION** acceptance criteria are BDD GIVEN/WHEN/THEN (min 3: happy/edge/error) and MUST satisfy the Phase 5.1 AI-SDD M1-M5 and M7 gate — tech-agnostic Business Intent, logical `FR-`/`BR-` IDs first, observable single-interpretation ACs, rebuild-from-scratch validity, every AC demoable as a business outcome — why: a reader who must guess a rule/limit/role re-implements the wrong behavior
- **IMPORTANT MUST ATTENTION** apply the M7 demo test to every AC's BODY — _"what would a stakeholder SEE change?"_; no answer → TECHNICAL-ONLY, drop it. FAIL a `WHEN` that is an invocation (handler runs, consumer receives, job fires, data syncs) or a `THEN` asserting schema/type/nullability/call-count; NEVER derive the AC count from an architecture inventory — why: M1 governs vocabulary, M7 governs subject matter — a technical AC in tech-free prose passes M1 and still rots the PBI
- **IMPORTANT MUST ATTENTION** every PBI MUST include `story_points`, `complexity`, `man_days_traditional`, `man_days_ai` frontmatter AND a complete Dependencies table (`must-before`/`can-parallel`/`blocked-by`/`independent`) — fill even when `independent`
- **IMPORTANT MUST ATTENTION** keep PBI Business Intent prose tech-agnostic — NO framework/product/language/design-pattern names; implementation hints go ONLY in `## Implementation Notes`, source refs ONLY in `[Source: namespace/service/id]` evidence carriers — why: a tech-leaked spec is not rebuildable on another stack (M1/M2)
- **IMPORTANT MUST ATTENTION** greenfield mode: NEVER ask about tech stack during refinement — capture team skills/scale as signals only; tech decided after business analysis
- **MANDATORY IMPORTANT MUST ATTENTION** before refining domain PBIs, read existing TCs in `docs/specs/` and `docs/project-reference/domain-entities-reference.md`; grep 3+ existing PBIs/specs for local conventions before authoring — why: project vocabulary and patterns override generic BABOK/INVEST defaults
- **MANDATORY IMPORTANT MUST ATTENTION** cite `file:line` (or `[Source: ...]`) evidence for every claim, confidence >80% to act, <60% DO NOT recommend — NEVER present a guess as fact
- **IMPORTANT MUST ATTENTION** complex/lengthy work → persist findings to `plans/reports/` incrementally — why: prevents silent loss of all findings on context exhaustion
- **MANDATORY IMPORTANT MUST ATTENTION** add final review task to verify work quality
- **MANDATORY IMPORTANT MUST ATTENTION** add task: run `$why-review` — validate PBI design rationale before `$story` or `$spec [mode=tests]`
- **MANDATORY IMPORTANT MUST ATTENTION** add task: run `$pbi-challenge` — Dev BA PIC review before `$dor-gate` or `$story`

**Anti-Rationalization:**

| Evasion                                    | Rebuttal                                                                                 |
| ------------------------------------------ | ---------------------------------------------------------------------------------------- |
| "Simple PBI, skip hypothesis validation"   | Wrong assumption wastes more time than validation check. Apply Phase 3 always.           |
| "Validation interview is optional here"    | NEVER optional — Phase 7 user decides assumptions, AI doesn't                            |
| "Phase 6 estimate is fine, skip re-derive" | Phase 7.5 is MANDATORY — interview changed scope; stale numbers corrupt velocity         |
| "Skip Dependencies table, no blockers"     | Unknown blockers exist. Always fill table — even if `independent`                        |
| "Skip story points, just write ACs"        | `story_points`, `man_days_traditional`, `man_days_ai` mandatory in frontmatter           |
| "Add a stack hint, it clarifies the AC"    | Business Intent stays tech-agnostic (M1/M2) — hints go to `## Implementation Notes` only |
| "Domain context not needed for small PBI"  | Small PBIs touch entities. Read domain-entities-reference first                          |

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break it into small todo tasks and sub-tasks using task tracking.

**IMPORTANT MUST ATTENTION** Phase 3 hypothesis + Phase 7 interview are NON-OPTIONAL — user decides, AI never auto-decides.
**IMPORTANT MUST ATTENTION** Phase 7.5 re-derives estimates against locked scope — never ship stale Phase 6 numbers.
**IMPORTANT MUST ATTENTION** keep Business Intent tech-agnostic; cite `file:line`/`[Source:]` evidence, confidence >80% to act.

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
