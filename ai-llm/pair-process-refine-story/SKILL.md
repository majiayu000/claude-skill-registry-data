---
name: pair-process-refine-story
description: "Refines a user story from Draft to Ready — the single Draft→Ready path (D24): phase 0 capability-grill(sync), Given-When-Then acceptance criteria, process-map-subdomains/process-map-contexts scoped analysis, classify matrix, sprint readiness. Composes /pair-capability-grill, /process-map-subdomains, /process-map-contexts, /pair-capability-classify, /pair-capability-write-issue. Not for sizing an already-refined story (use /pair-capability-estimate)."
version: 0.7.0
author: Foomakers
---

# /pair-process-refine-story — Story Refinement (single Draft→Ready)

Transform a user story from rough breakdown (Draft) into a development-ready specification (Ready). This is **THE single Draft→Ready path** — no separate "make-ready" skill exists and none is ever born (R3.12, D24); refinement IS the transition (canonical-states.md). **Section-level idempotency** — see [idempotency convention](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/idempotency.md): each refinement section is checked before acting; partial refinements resume from the first missing section, an already-Ready story is confirmed and exits.

## Process Profile

<!-- process-step: id=refine-story -->

Executable form of the **`refine-story`** step, and a composer of `define-subdomains`, `define-bounded-contexts`. A **direct** invocation while a step is disabled by the project's profile warns and asks for confirmation; a **composed** one never prompts — it degrades exactly as a step that is not installed. No section ⇒ no-op. See [process-profile gate](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/process-profile-gate.md).

## Composed Skills

| Skill             | Type       | Required                                                                                                          |
| ----------------- | ---------- | ---------------------------------------------------------------------------------------------------------------- |
| `/pair-capability-grill`          | Capability | Yes — phase 0 shared-understanding sync (R3.11 alignment gate). If not installed, warn and fall back to the per-step approval gates. |
| `/process-map-subdomains` | Capability | Optional — functional/domain placement (Step 2), scoped to the story. If not installed, warn and skip domain placement.             |
| `/process-map-contexts`   | Capability | Optional — touched-context mapping (Step 3), scoped; feeds the coupling dimension. If not installed, warn and skip.                  |
| `/pair-capability-classify`       | Capability | Optional — shift-left classification matrix into the story body (Step 3b). If not installed, warn and continue.  |
| `/pair-capability-write-issue`    | Capability | Yes — creates or updates the story issue in the PM tool                                                          |

## Arguments

| Argument | Required | Description                                                                                                     |
| -------- | -------- | --------------------------------------------------------------------------------------------------------------- |
| `$story` | No       | Story identifier (e.g., `#42`). If omitted, the skill selects the highest-priority `Draft` story from the backlog. |

## Algorithm

### Step 0: Story Selection

1. **Check**: Is `$story` provided?
2. **Skip**: If provided, load the story from the PM tool and proceed to Step 1.
3. **Act**: If not provided, query the PM tool for stories in the `Draft` macrostate (the board's Todo/backlog column via the state mapping — symmetric with Step 5's `Ready`→`Refined`). Apply selection criteria:
   - **Priority**: P0 > P1 > P2
   - **Sprint need**: stories required for upcoming sprint
   - **Dependency chain**: stories blocking other work
4. **Act**: Present recommendation and ask developer to confirm:

   > Recommend refining Story `#[ID]: [Title]` (Priority: [P0/P1/P2]).
   > Reason: [business value / sprint urgency / unblocks other work].
   > Proceed?

5. **Verify**: A story is identified (from `$story` or developer confirmation) and its current body is available for Step 1's section detection.

### Phase 0: Shared-Understanding Sync (grill — BLOCKING)

**This is the R3.11 AI↔human alignment gate — a prerequisite, not optional.** No DoR section is authored until shared understanding is explicit; it is the reason no separate "make-ready" step exists (D24). Phase 0 runs between Step 0 (selection) and Step 1 (detection): the already-Ready check below is a light read of the body to decide whether to skip the sync — Step 1's detection table is where that state is formally determined.

1. **Check**: Has phase 0 already reached explicit shared understanding this session, or does a prior `/pair-capability-grill` sync handoff for this story exist in `.pair/working/`, or is the story already Ready (Step 1 confirms-and-exits)?
2. **Skip**: If shared understanding is already confirmed (or the story is already Ready), move to Step 1.
3. **Act**: Is `/pair-capability-grill` installed?
   - **Yes**: Compose `/pair-capability-grill` with `$mode: sync`, `$story: [story-id]`, and `$context: <current story body>` so grill doesn't re-fetch it. Grill systematically covers all six aspects (goal, AC, edge cases, dependencies, design, risks) one question at a time and returns the alignment synthesis pre-mapped to the Refined template sections. **Resume**: if a prior sync was interrupted, its partial synthesis handoff is loaded and the sync resumes from the first open aspect — prior answers are not re-asked.
   - **No**: Warn (`/pair-capability-grill not installed — skipping the phase 0 sync; alignment falls to the per-step human-judgment gates in Steps 2–4`) and proceed; the explicit approval gates in Steps 2–4 remain the alignment mechanism.
4. **Verify**: `/pair-capability-grill` returned **explicit shared understanding** (grill never auto-exits on an empty queue — only an explicit human "yes" ends it), or the skip was warned. Without shared understanding → **HALT**: refinement does not proceed on an unaligned story.

### Step 1: Detect Refinement State

1. **Check**: Read the current story body and classify each section as **present** or **missing**:

   | Section                               | Detection                                                                  |
   | ------------------------------------- | -------------------------------------------------------------------------- |
   | Story Statement                       | Has `**As a**` / `**I want**` / `**So that**` with non-placeholder content |
   | Epic Context                          | Has `**Parent Epic**` with actual link                                     |
   | Acceptance Criteria (Given-When-Then) | Has `**Given**` / `**When**` / `**Then**` blocks                           |
   | Business Rules                        | Has non-placeholder business rules                                         |
   | Edge Cases                            | Has non-placeholder edge case handling                                     |
   | Technical Analysis                    | Has `### Implementation Approach` or `### Strategy` with content           |
   | Design flag                           | Has a `Design:` line under Technical Analysis → Implementation Approach, set to `not required` or `required — reference: <link>` (DoR criterion 6, [definition-of-ready-and-done.md](../../../.pair/knowledge/guidelines/collaboration/project-management-tool/definition-of-ready-and-done.md)) |
   | Doc team flag                         | Has a `Doc team:` line under Technical Analysis → Implementation Approach, set to `non richiesta` or `richiesta — team: <team name>` (a row of Notion `Globale - Teams` without the `Team ` prefix; never `Tech`) (DoR criterion 7, [definition-of-ready-and-done.md](../../../.pair/knowledge/guidelines/collaboration/project-management-tool/definition-of-ready-and-done.md)) |
   | Technical Risks                       | Has risk table with entries                                                |
   | Definition of Done                    | Has DoD checklist with items                                               |
   | Story Sizing                          | Has `**Final Story Points**` with value                                    |
   | Dependencies                          | Has dependency information                                                 |
   | Validation Strategy                   | Has testing approach                                                       |

2. **Act**: Determine refinement state:
   - **All sections present** → story is already Ready. Offer selective update (Step 6).
   - **Some sections present** → partial refinement. Resume from first missing section (Steps 2–5).
   - **No sections (only Initial Breakdown)** → full refinement needed (Steps 2–5).
3. **Verify**: Refinement state determined. Report:

   > Refinement state: [N/M sections complete]. [Resuming from: Section X | Full refinement | Already Ready — offering update].

### Step 2: Requirements Analysis

**Skip if**: Acceptance Criteria, Business Rules, and Edge Cases are all present.

1. **Act**: Expand the story scope into detailed, testable acceptance criteria:
   - Convert requirements into **Given-When-Then** scenarios.
   - Identify **business rules** with measurable criteria.
   - Address **edge cases** and error handling conditions.
2. **Act**: Domain check — if `context-map.md` (in `.pair/adoption/product/`) exists, read it (plus any linked `subdomain/<slug>.context.md` this story touches). When the story introduces or sharpens a domain term, update the map inline per the [Context Map Maintenance](../../../.pair/knowledge/guidelines/architecture/design-patterns/context-map-maintenance.md) guideline. When a proposed criterion conflicts with a registered rule, flag it citing that rule (and the DDR, when one exists) and resolve with the developer before proceeding. Skip this step entirely if the map doesn't exist — its absence is expected, not an error.
3. **Act**: Domain placement (functional). Is `/process-map-subdomains` installed? Compose `/process-map-subdomains` with `$scope: [the business capability this story touches]` — **scoped to the story, never `$scope: all`** (that is `/pair-process-bootstrap`-only). It classifies the touched capability as core/supporting/generic with a Volatility rating; that placement feeds the **Business impact** dimension of the classification matrix (Step 3b) and the volatility input to coupling (Step 3). Not installed, or no domain artifacts and no PRD/initiatives to classify from → degrade: skip domain placement with a note, still produce the functional analysis.
4. **Act**: Present the proposed criteria to the developer for validation:

   > Proposed acceptance criteria for `#[ID]`:
   > [List Given-When-Then scenarios]
   > [Business rules]
   > [Edge cases]
   > Approve or adjust?

5. **Verify**: Human-judgment gate — the developer explicitly approves the presented Given-When-Then scenarios, business rules, and edge cases (or requests changes, looping back to Step 2's Act). Only an explicit approval finalizes the criteria.

### Step 3: Technical Analysis

**Skip if**: Technical Analysis, Technical Risks, and the Design flag are present.

1. **Act**: Assess the implementation approach:
   - **Strategy**: high-level technical approach and architecture alignment.
   - **Key components**: modules, integration points, data flow.
   - **Risks**: technical unknowns, complexity, dependencies.
   - **Design flag** (DoR criterion 6): set the `Design:` line under Implementation Approach to `not required` when the approach is understood, or `required — reference: <link>` when a design doc/spike is needed — per [definition-of-ready-and-done.md](../../../.pair/knowledge/guidelines/collaboration/project-management-tool/definition-of-ready-and-done.md). This is the criterion Step 5 verifies as the sixth DoR criterion.
   - **Doc team flag** (DoR criterion 7): set the `Doc team:` line under Implementation Approach to `richiesta — team: <team name>` (a row of Notion `Globale - Teams` without the `Team ` prefix — today `Corsi`, `Growth`, `User`, `Social`, `B2B`, `Amministrazione`; never `Tech`, which produces the guide rather than reading it) when the story introduces a feature usable by a non-technical team **or** changes an operational flow for one, otherwise `non richiesta` (refactor, internal change, bugfix with no perceivable flow change) — criterion in [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md#documentazione-funzionalità-per-gli-altri-team), guide format in [feature-guide-template.md](../../../.pair/knowledge/guidelines/collaboration/templates/feature-guide-template.md). **Decide it with the developer** — never default to `non richiesta` silently: an unasked flag is a flag that produces no guide. When set to `richiesta`, the guide becomes a Done condition for the story (its link is attached to the issue).
   - Reference [architecture.md](../../../.pair/adoption/tech/architecture.md) and [tech-stack.md](../../../.pair/adoption/tech/tech-stack.md).
2. **Act**: Touched-context mapping (technical). Is `/process-map-contexts` installed? Compose `/process-map-contexts` with `$scope: [the contexts/services this story touches]` — **scoped, never `$scope: all`** (that is `/pair-process-bootstrap`-only). It maps the touched subdomains to bounded contexts and assesses each relationship (integration strength, socio-technical distance, volatility) to derive a balanced/unbalanced verdict. **When it reports an unbalanced integration this story introduces — strong coupling toward a distant and/or volatile context — record it as a row in the Technical Risks and Mitigation table** (D38): the coupling risk this story adds, its impact, and the mitigation. This same map-contexts output feeds the **Coupling balance** dimension of the classification matrix (Step 3b) — refine-story runs no coupling assessment of its own; the inputs come from the scoped map-contexts output and the subdomain catalog volatility (D24). Not installed, or no domain artifacts → coupling is "not assessed", excluded from the matrix max, never blocks (D21).
3. **Act**: Present technical analysis (strategy, key components, integration points, and any coupling risk from the mapping) to developer for validation.
4. **Verify**: Human-judgment gate — the developer explicitly approves the presented strategy, key components, and risks (or requests changes, looping back to Step 3's Act). Only an explicit approval finalizes the analysis.

### Step 3b: Classification (shift-left matrix)

**Skip if**: the story body already carries a classification matrix section for the current model + adoption (deterministic — re-running yields the same matrix).

1. **Check**: Is `/pair-capability-classify` installed?
2. **Skip**: If not installed, warn (`/pair-capability-classify not installed — skipping the shift-left risk matrix; classify at review time`) and move to Step 4.
3. **Act**: Compose `/pair-capability-classify` with `$context: refinement` and `$target: [story-id]`. It applies the [quality model](../../../.pair/knowledge/guidelines/quality-assurance/quality-model.md) to the story context, writes the matrix as 1 line + `<details>` into the story body's **`## Classification`** section — the first-class template slot in [user-story-template.md](../../../.pair/knowledge/guidelines/collaboration/templates/user-story-template.md) (D22) — and, the first time, proposes the `## Tag Projection` declaration before emitting any tag (adoption-gated). The **Coupling balance** dimension is fed by the scoped `/process-map-contexts` output from Step 3 (and subdomain volatility from Step 2); with no such output it is "not assessed" and excluded from the tier max (D38, D21). An unbalanced/volatile integration recorded as a risk in Step 3 therefore also raises the coupling dimension here — contributing to the tier via the existing max rule (D38). No `tech/risk-matrix.md` ⇒ KB defaults, matrix only, no tags (D21).
4. **Verify**: The story body's `## Classification` section carries the matrix (or the skip was warned). `/pair-capability-classify` HALTs only if the quality model doc (#221) is absent — surface that pointer to the developer.

### Step 4: Sprint Readiness

**Skip if**: Story Sizing, Dependencies, and Validation Strategy are present.

1. **Act**: Re-estimate story size with detailed requirements:
   - Apply refined sizing: XS(1), S(2), M(3), L(5), XL(8).
   - Assess sprint fit — split if oversized while preserving user value.
   - Map dependencies (prerequisite and dependent stories).
   - Define validation and testing strategy.
2. **Act**: Present sizing assessment to developer.
3. **Verify**: Human-judgment gate — the developer explicitly approves the sizing, dependencies, and validation strategy presented in Step 4's Act. Only an explicit approval confirms sprint readiness.

### Step 5: Documentation and PM Tool Update

1. **Act**: Assemble the complete refined story body using the [user-story-template.md](../../../.pair/knowledge/guidelines/collaboration/templates/user-story-template.md) (resolve override-first — [template resolution](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/template-resolution.md)) Refined template:
   - **Functional sections first**: Story Statement → Epic Context → Classification (the Step 3b matrix) → Acceptance Criteria → Definition of Done → Story Sizing → Dependencies → Validation → Notes.
   - **Technical sections last**: Technical Analysis → (Task Breakdown added later by `/pair-process-plan-tasks`).
2. **Act**: Compose `/pair-capability-write-issue` with:
   - `$type: story`
   - `$content`: the assembled refined story body
   - `$id`: the story identifier (update mode — story already exists)
   - `$status: Ready` — **pass it only when a board state maps to the `Ready` macrostate** (a presence check on the `state-mapping`, not a resolution). `/pair-capability-write-issue` owns the board-field write: it resolves `Ready` to the target board state via the [canonical-states.md](../../../.pair/knowledge/guidelines/collaboration/project-management-tool/canonical-states.md) writing rule (first board state mapped to `Ready`; e.g. `Refined` on pair's own board) and updates the Status field (its Step 6). **Omit `$status` when no board state maps to `Ready`** (a minimal board, D4): the completed DoR sections on the body are themselves the readiness signal per the [definition-of-ready-and-done.md](../../../.pair/knowledge/guidelines/collaboration/project-management-tool/definition-of-ready-and-done.md) **Readiness Fallback**, and omitting it avoids `/pair-capability-write-issue`'s unmapped-macrostate HALT (its Step 6). Idempotent: a story already at `Ready` is confirmed, not re-moved — refine-story runs no board-field write of its own (D24).
3. **Verify**: Either `/pair-capability-write-issue` wrote the board state resolved from `$status: Ready` (mapping present), or (no mapping, `$status` omitted) all seven DoR criteria are satisfied on the body as the readiness signal.

### Step 6: Already-Ready Update (optional path)

Reached only when Step 1 detects all sections are present.

1. **Act**: Ask the developer which sections to update:

   > Story `#[ID]` is already Ready. Which sections need updating?
   > 1. Acceptance Criteria
   > 2. Technical Analysis
   > 3. Sprint Sizing
   > 4. All sections

2. **Act**: For selected sections, re-execute the corresponding step (2, 3, or 4).
3. **Act**: Compose `/pair-capability-write-issue` with `$type: story`, `$id: [story-id]`, and updated `$content`.
4. **Verify**: Story updated.

## Output Format

```text
STORY REFINEMENT COMPLETE:
├── Story:    [#ID: Title]
├── Status:   [Ready | Updated | Ready (DoR-on-body — no board mapping)]
├── Sync:     [shared understanding confirmed | grill skipped — per-step gates]
├── Sections: [N/N complete]
├── Matrix:   [risk:<tier> · cost:<class> | classify not installed — no matrix]
├── Domain:   [subdomain placement + touched contexts | map-* not installed — skipped]
├── Sizing:   [X points — fits sprint: Yes/No]
├── PM Tool:  [Issue updated — #ID]
└── Next:     /pair-process-plan-tasks to create task breakdown
```

## HALT Conditions

- **No Draft stories in backlog** (Step 0) — nothing to refine.
- **Story not found** (Step 0) — invalid `$story` identifier.
- **No shared understanding** (Phase 0) — `/pair-capability-grill` sync ended without an explicit human "yes"; refinement never proceeds on an unaligned story.
- **PM tool not accessible** — cannot read or update stories.
- **Developer rejects criteria** (Steps 2–4) — must resolve before proceeding.

## Graceful Degradation

See [graceful degradation](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/graceful-degradation.md) (optional skill `/pair-capability-write-issue` not installed / PM tool not accessible → produce the refined story content, ask developer to update manually) for the standard scenarios. Additional cases:

- **`/pair-capability-grill` not installed** (Phase 0): warn and skip the sync; the per-step human-judgment approval gates in Steps 2–4 remain the alignment mechanism — refinement still completes.
- **`/process-map-subdomains` / `/process-map-contexts` not installed, or no domain artifacts** (Steps 2–3): the functional and technical analysis sections are still produced; domain placement and touched-context mapping are skipped with a note, and the coupling dimension is "not assessed" (never a HALT).
- **`/pair-capability-classify` not installed** (Step 3b): refinement completes without a matrix; the skip is flagged in the summary and the `## Classification` section stays empty.
- **No state mapping resolves to `Ready`** (Step 5): the completed DoR sections on the body are the readiness signal (definition-of-ready-and-done.md Readiness Fallback) — not an error.
- If adoption files (architecture, tech-stack) are not found, skip technical analysis alignment checks and warn.
- If `context-map.md` is not found, skip the domain check in Step 2 — its absence is the expected steady state, not an error.

## Notes

- **The single Draft→Ready path** (R3.12, D24): refinement IS the transition to `Ready` — there is no separate "make-ready" skill and none is ever added. Phase 0's grill sync is the R3.11 alignment gate that makes this one skill sufficient.
- **R3.11 is "not optional" as a gate, not as a specific skill**: the AI↔human alignment gate always runs. When `/pair-capability-grill` is installed it runs the systematic phase 0 sync; when it is not, the explicit per-step human-judgment approval gates in Steps 2–4 are the accepted satisfaction of R3.11 (graceful-degradation convention). What is never skipped is explicit human alignment before the story reaches `Ready`.
- This skill **modifies PM tool state** — it updates story issues and transitions the item to `Ready`.
- **Composes, never re-derives**: domain placement comes from `/process-map-subdomains`, touched-context/coupling from `/process-map-contexts`, the matrix from `/pair-capability-classify` — refine-story orchestrates them scoped to the story and owns no assessment criteria of its own (D24).
- Template ordering (Step 5) positions Technical Analysis as the bridge to Task Breakdown (added by `/pair-process-plan-tasks`).
- INVEST validation: the refined story must satisfy Independent, Negotiable, Valuable, Estimable, Small, Testable criteria.
- The `/pair-process-refine-story` skill handles the transition from Initial Breakdown template format to Refined template format.
