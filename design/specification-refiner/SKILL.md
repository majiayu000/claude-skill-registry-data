---
name: specification-refiner
description: >
  Systematic analysis and refinement of specifications, requirements, architecture designs, and project plans.
  Use when the user wants to identify gaps, weaknesses, inefficiencies, or complications in a proposed plan, specification, or design document.
  Triggers on gap analysis, specification review, requirements analysis, architecture critique, design validation, plan assessment, weakness identification, assumption auditing, or when users share specs/plans asking for feedback.
  Produces actionable findings with remediations and maintains analysis state across iterations.
  Features sequential clarification with one question at a time, recommended answers, and immediate integration.
---

# Specification Refiner

Systematically analyze and refine specifications, requirements, and architectural designs through iterative gap analysis with persistent memory, sequential clarification, and explicit user confirmation at each phase.

## Core Workflow

```
0. ASSESS     → Evaluate complexity, select mode, confirm with user
1. INGEST     → Load document, confirm understanding with user
2. ANALYZE    → Run SEAMS + Critical Path, build coverage map
3. CLARIFY    → Sequential questions (one at a time), immediate integration
4. PRESENT    → Surface detailed findings, manage remaining questions
5. ITERATE    → Accept changes, re-analyze, present deltas
6. SYNTHESIZE → Present comprehensive summary for user approval
7. OUTPUT     → Generate refined specification(s) in Draft status
8. VALIDATE   → Review, validate traceability, advance status
```

Each phase ends with a **full summary gate** requiring user confirmation before proceeding.

---

## Phase 0: ASSESS

On receiving a specification document, first assess complexity to determine the appropriate mode.

### Complexity Assessment

Evaluate these factors:
- **Document size**: Page/word count
- **Domains identified**: Single vs. multi-domain
- **Stakeholder count**: How many perspectives involved
- **Scope clarity**: Clear, moderate, or ambiguous boundaries

### Mode Selection

Present to user:

```
Based on initial assessment:
- Document size: [X pages / Y words]
- Domains identified: [list domains]
- Stakeholder count: [N stakeholders]
- Scope clarity: [Clear/Moderate/Ambiguous]

Recommended mode: [SIMPLE/COMPLEX]

Options:
1. Proceed with recommended mode
2. Override to SIMPLE mode
3. Override to COMPLEX mode
4. Explain the modes in more detail

Your choice:
```

**SIMPLE Mode**: Single-domain, <10 pages, clear scope
- SEAMS analysis only
- Single A-Spec output with numbered requirements (`A-REQ-NNN`)

**COMPLEX Mode**: Multi-domain, >10 pages, ambiguous scope
- Full dual-framework analysis (SEAMS + Critical Path)
- A-Spec/B-Spec hierarchy per domain (see `references/spec-hierarchy.md`)
- Requirements Traceability Matrix generation

### Phase 0 Gate

Present gate summary (see `references/gate-templates.md` for full format). Wait for user confirmation before proceeding.

---

## Phase 1: INGEST

### Actions
1. Parse document structure (sections, dependencies, interfaces)
2. Create initial memory file: `analysis-state.md` using template from `assets/analysis-state-template.md`
3. Record mode selection in memory file
4. Identify document type and select appropriate analysis lenses
5. Note any questions that arise during parsing

### Question Management
- Add questions to the Open Questions list with "Raised In: Phase 1: INGEST"
- Attempt to answer any Phase 0 questions from document content
- Update question statuses

### Phase 1 Gate

Present full summary including: document info, sections identified, key entities, dependencies, and question status. See `references/gate-templates.md` for format. Wait for user confirmation—user may answer questions here.

---

## Phase 2: ANALYZE

Run analysis frameworks based on mode AND build the coverage map for clarification.

### SIMPLE Mode
Run SEAMS Analysis only (see `references/seams-framework.md`).

### COMPLEX Mode
Run BOTH frameworks in parallel:

#### Framework A: SEAMS Analysis
**S**tructure → **E**xecution → **A**ssumptions → **M**ismatches → **S**takeholders

| Lens | Questions to Answer |
|------|---------------------|
| **Structure** | Completeness of I/O paths? Cohesion? Coupling risks? Boundary clarity? |
| **Execution** | Happy path works? Edge cases covered? Failure modes handled? |
| **Assumptions** | Technical assumptions? Organizational? Environmental? |
| **Mismatches** | Requirements ↔ Design aligned? Design ↔ Implementation consistent? |
| **Stakeholders** | Operator view? Security view? Integrator view? End-user view? |

#### Framework B: Critical Path Analysis
See `references/critical-path-analysis.md` for detailed methods.

1. **Dependency Mapping**: Build N² matrix
2. **Critical Path Identification**: Find longest/riskiest chains
3. **Single Points of Failure**: Cascade risk components
4. **Bottleneck Detection**: Throughput limiters
5. **Temporal Analysis**: Sequencing issues

### Coverage Map Generation

**CRITICAL**: Build a structured coverage map using the 11-category taxonomy:

| Category | Status | Gap Count | Impact |
|----------|--------|-----------|--------|
| Functional Scope & Behavior | [Clear/Partial/Missing] | [N] | [High/Med/Low] |
| Domain & Data Model | [Clear/Partial/Missing] | [N] | [High/Med/Low] |
| Interaction & UX Flow | [Clear/Partial/Missing] | [N] | [High/Med/Low] |
| Non-Functional Quality Attributes | [Clear/Partial/Missing] | [N] | [High/Med/Low] |
| Integration & External Dependencies | [Clear/Partial/Missing] | [N] | [High/Med/Low] |
| Edge Cases & Failure Handling | [Clear/Partial/Missing] | [N] | [High/Med/Low] |
| Constraints & Tradeoffs | [Clear/Partial/Missing] | [N] | [High/Med/Low] |
| Terminology & Consistency | [Clear/Partial/Missing] | [N] | [High/Med/Low] |
| Completion Signals | [Clear/Partial/Missing] | [N] | [High/Med/Low] |
| Assumptions & Risks | [Clear/Partial/Missing] | [N] | [High/Med/Low] |
| Misc & Placeholders | [Clear/Partial/Missing] | [N] | [High/Med/Low] |

This map drives the CLARIFY phase question prioritization.

### Phase 2 Gate

Present preliminary findings summary with severity counts, coverage map summary, top 3 issues, and blocked findings. Prompt to proceed to CLARIFY phase. See `references/gate-templates.md` for format.

---

## Phase 3: CLARIFY

**CRITICAL**: This phase uses SEQUENTIAL QUESTIONING to reduce cognitive load and enable immediate integration.

### Clarification Principles

1. **One question at a time** - Never present multiple questions
2. **Constrained answers** - Multiple choice (2-5 options) OR short phrase (≤5 words)
3. **Recommended answer** - Always analyze and recommend the best option
4. **Immediate integration** - Update spec/analysis-state AFTER EACH answer
5. **Maximum 5 questions** - Per clarification session
6. **Maximum 10 questions** - Across entire analysis (including ITERATE loops)

### Question Prioritization

Generate prioritized queue using **Impact × Uncertainty** scoring:

1. Score each potential question:
   - **Impact**: How much does this affect architecture, data model, task decomposition, test design, UX, ops readiness, or compliance? (1-5)
   - **Uncertainty**: How ambiguous is the current state? (1-5)
   - **Priority Score** = Impact × Uncertainty

2. Apply constraints:
   - Only include questions whose answers materially change implementation or validation
   - Ensure category balance (don't ask 3 questions from same category)
   - Exclude already-answered questions
   - Exclude trivial stylistic preferences
   - Favor questions that reduce downstream rework risk

3. Select top 5 by priority score

### Question Format: Multiple Choice

When discrete options exist, present as:

```markdown
### CLARIFY-001 [CATEGORY]

[Context: What triggered this question]

**Question**: [The specific question]

**Recommended:** Option [X] - [1-2 sentence reasoning based on best practices, risk reduction, or project context]

| Option | Description |
|--------|-------------|
| A | [Option A description] |
| B | [Option B description] |
| C | [Option C description] |
| D | [Option D description] (if needed) |
| Short | Provide a different short answer (≤5 words) |

Reply with the option letter (e.g., "A"), accept the recommendation by saying "yes" or "recommended", or provide your own short answer.
```

### Question Format: Short Answer

When no meaningful discrete options exist:

```markdown
### CLARIFY-001 [CATEGORY]

[Context: What triggered this question]

**Question**: [The specific question]

**Suggested:** [Your proposed answer] - [Brief reasoning]

Format: Short answer (≤5 words). You can accept the suggestion by saying "yes" or "suggested", or provide your own answer.
```

### Answer Processing

1. **If user replies "yes", "recommended", or "suggested"**: Use the stated recommendation/suggestion
2. **If user provides option letter**: Map to that option
3. **If user provides custom answer**: Validate it fits ≤5 word constraint
4. **If ambiguous**: Ask for quick disambiguation (doesn't count as new question)

### Immediate Integration Protocol

**AFTER EACH accepted answer** (not at end of phase):

1. **Create Clarifications section** (if first answer this session):
   ```markdown
   ## Clarifications

   ### Session YYYY-MM-DD
   - Q: [question] → A: [final answer]
   ```

2. **Apply to appropriate section(s)**:

   | Answer Type | Update Location |
   |-------------|-----------------|
   | Functional ambiguity | Functional Requirements section |
   | User interaction/actor | User Stories or Actors subsection |
   | Data shape/entities | Data Model section (fields, types, relationships) |
   | Non-functional constraint | Quality Attributes section (convert vague → metric) |
   | Edge case/negative flow | Edge Cases / Error Handling section |
   | Terminology conflict | Normalize term across entire spec |

3. **Handle conflicts**:
   - If clarification invalidates earlier statement, REPLACE it (don't duplicate)
   - Leave no obsolete contradictory text

4. **Save immediately**: Atomic write after each integration

5. **Update analysis-state.md**: Log question as answered

### Early Termination

Stop asking questions when:
- All critical ambiguities resolved (remaining questions unnecessary)
- User signals completion ("done", "good", "no more", "proceed")
- 5 questions reached in this session
- 10 total questions reached across analysis

### No Questions Scenario

If no valid questions exist (full coverage), immediately report:
```
No critical ambiguities detected requiring formal clarification.
All categories show Clear status.
Recommend proceeding to Phase 4 (PRESENT).
```

### Phase 3 Gate

Present clarification summary:

```
PHASE 3 COMPLETE: CLARIFICATION

Questions asked this session: [N]
Total questions asked (all phases): [M]

COVERAGE UPDATE:
| Category | Before | After | Notes |
|----------|--------|-------|-------|
| Functional Scope | Partial | Clear | Q1 resolved |
| Data Model | Missing | Clear | Q2, Q3 resolved |
| Edge Cases | Partial | Partial | Deferred (low impact) |
...

Clarifications integrated:
1. [Q1]: [Answer] → Updated [Section]
2. [Q2]: [Answer] → Updated [Section]
...

DEFERRED TO LATER:
- [Category]: [Reason - e.g., better suited for planning phase]

OUTSTANDING (low impact):
- [Category]: [Why not addressed - e.g., exceeds question quota]

Options:
1. Proceed to Phase 4 (PRESENT) with findings
2. Run another clarification session (if quota allows)
3. Review updated specification sections

Your choice:
```

---

## Phase 4: PRESENT

### Finding Format

For EACH identified issue, include: ID, title, category, severity, confidence, blocked-by status, description, evidence, impact, remediation options (with trade-offs), and related issues. See `references/gate-templates.md` for full template.

### Presentation Order

Present findings grouped by:
1. **Critical blockers** (must fix before proceeding)
2. **Significant gaps** (high impact, clear remediation)
3. **Optimization opportunities** (efficiency improvements)
4. **Considerations** (context-dependent, need user input)

### Question Management
- Present all unanswered questions explicitly
- Ask user to answer questions or confirm assumptions
- Update question tracking with answers received

### Phase 4 Gate

Present findings summary with severity counts, question status, and assumptions made. Offer options: (1) Iterate, (2) Skip to Synthesize, (3) Run more clarification, (4) Review details. See `references/gate-templates.md` for format.

---

## Phase 5: ITERATE

When user provides new information, constraints, or requests changes:

### Actions
1. **Validate new input** against existing analysis
2. **Identify affected areas** in the specification
3. **Re-run analysis** on affected sections only (delta analysis)
4. **Update coverage map** based on new information
5. **Assess cascading effects** on previously-identified issues
6. **Update memory file** with new state

### Triggering Additional Clarification

If iteration reveals new ambiguities:
- Check if question quota allows (10 total max)
- If yes, offer to run additional CLARIFY session
- If no, note as deferred with reason

### Question Management
- Add new questions with "Raised In: Phase 5: ITERATE"
- Check if new input answers existing questions
- Update all question statuses

### Phase 5 Gate

Present delta summary: changes incorporated, coverage map update, new/modified/resolved findings, key changes, question status. Offer options: (1) Continue iterating, (2) Synthesize, (3) Run clarification, (4) Review findings. See `references/gate-templates.md` for format.

---

## Phase 6: SYNTHESIZE

Before generating any output, present a comprehensive summary for user approval.

### Summary Contents

Present comprehensive summary covering:
- **Document Overview**: Title, mode, iteration count, clarification count
- **Coverage Summary**: Final coverage map with all categories
- **Findings Resolution**: By severity with resolved/unresolved breakdown, key resolutions, unresolved critical/high items
- **Clarifications Applied**: All Q&A with section updates
- **Questions Status**: Answered, unanswered (with impact), deferred (with reason)
- **Assumptions**: Confirmed vs. unverified
- **Proposed Output Structure**: Based on mode (single doc for SIMPLE, separate files for COMPLEX)

See `references/gate-templates.md` for full format.

### Phase 6 Gate

Offer options: (1) Approve and output, (2) Return to iterate, (3) Modify structure, (4) Answer questions. Wait for explicit approval before generating output.

---

## Phase 7: OUTPUT

Generate refined specification(s) based on mode, all in **Draft** status.

### SIMPLE Mode Output
Generate single A-Spec document (`refined-specification.md`) with:
- Numbered requirements (`A-REQ-001`, `A-REQ-002`, etc.)
- All resolved findings incorporated
- Selected remediations applied
- Clarifications section with session log
- Documented assumptions
- Remaining open questions in dedicated section

### COMPLEX Mode Output
Generate specification hierarchy per domain:

**A-Spec files** (one per domain):
- Naming: `[domain]-a-spec.md`
- Requirements: `A-REQ-[DOMAIN]-NNN`
- High-level requirements defining WHAT

**B-Spec files** (one or more per domain):
- Naming: `[domain]-[subsystem]-b-spec.md`
- Requirements: `B-REQ-[DOMAIN]-NNN`
- Each requirement MUST include `Traces to: A-REQ-XXX-NNN`
- Detailed requirements defining HOW

**Supporting files**:
- `traceability-matrix.md` - Full RTM (see `assets/traceability-matrix-template.md`)
- `clarifications-log.md` - All clarification sessions
- `cross-cutting-concerns.md` (if applicable)
- `open-items.md`

See `references/spec-hierarchy.md` for detailed format specifications.

### RTM Generation (COMPLEX mode)
1. Extract all A-REQ-* from A-Spec files
2. Extract all B-REQ-* from B-Spec files with their traces
3. Build coverage matrix
4. Calculate coverage percentage
5. Identify gaps (A-Reqs with no B-Req coverage)
6. Generate `traceability-matrix.md`
7. Update `analysis-state.md` with RTM summary

### Final Actions
1. Set all specification statuses to **Draft**
2. Update `analysis-state.md` with completion status and RTM summary
3. Present output files to user
4. Summarize what was generated
5. Prompt transition to Phase 8

### Phase 7 Completion

Present: mode, files created with requirement counts, RTM summary (COMPLEX mode), findings addressed, clarifications integrated, assumptions documented. Prompt user to proceed to Phase 8. See `references/gate-templates.md` for format.

---

## Phase 8: VALIDATE

Final review and validation phase ensuring specifications are comprehensive, traceable, and approved. **Mandatory for both SIMPLE and COMPLEX modes.**

### Status Workflow
Specifications progress through statuses:
```
Draft → Reviewed → Approved → Baselined
```

- **Draft**: Initial output from Phase 7 (automatic)
- **Reviewed**: Technical review complete, no critical gaps
- **Approved**: Stakeholder sign-off received
- **Baselined**: Locked for change control

### Validation Actions
1. **Completeness check**: All required sections present, cross-references valid
2. **RTM validation** (COMPLEX): Coverage percentage, gap identification
3. **Traceability check** (COMPLEX): All B-Reqs trace to A-Reqs
4. **Consistency check**: Terminology, formatting, priority scales aligned
5. **Clarification integration check**: All answers properly incorporated
6. **Present validation findings** with severity

### Status Advancement
- Require explicit user approval to advance status
- Document status change with timestamp and approver
- Update `analysis-state.md` with new status and history

### Advancement Criteria
| Transition | Requirements |
|------------|--------------|
| Draft → Reviewed | No critical RTM gaps, completeness checks pass |
| Reviewed → Approved | All high-priority issues resolved, stakeholder review |
| Approved → Baselined | Formal approval documented, change control established |

### Phase 8 Gate
Present validation summary with:
- Current status and proposed advancement
- RTM coverage metrics (COMPLEX mode)
- Completeness and consistency checklist
- Clarification integration verification
- Validation findings
- Options: advance status, return to fix issues, review details

See `references/gate-templates.md` for full template.

---

## Ambiguity Taxonomy (11 Categories)

### 1. Functional Scope & Behavior
- Core user goals & success criteria
- Explicit out-of-scope declarations
- User roles / personas differentiation

### 2. Domain & Data Model
- Entities, attributes, relationships
- Identity & uniqueness rules
- Lifecycle/state transitions
- Data volume / scale assumptions

### 3. Interaction & UX Flow
- Critical user journeys / sequences
- Error/empty/loading states
- Accessibility or localization notes

### 4. Non-Functional Quality Attributes
- Performance (latency, throughput targets)
- Scalability (horizontal/vertical, limits)
- Reliability & availability (uptime, recovery)
- Observability (logging, metrics, tracing)
- Security & privacy (authN/Z, data protection)
- Compliance / regulatory constraints

### 5. Integration & External Dependencies
- External services/APIs and failure modes
- Data import/export formats
- Protocol/versioning assumptions

### 6. Edge Cases & Failure Handling
- Negative scenarios
- Rate limiting / throttling
- Conflict resolution (e.g., concurrent edits)

### 7. Constraints & Tradeoffs
- Technical constraints (language, storage, hosting)
- Explicit tradeoffs or rejected alternatives

### 8. Terminology & Consistency
- Canonical glossary terms
- Avoided synonyms / deprecated terms

### 9. Completion Signals
- Acceptance criteria testability
- Measurable Definition of Done indicators

### 10. Assumptions & Risks
- Technical assumptions (infrastructure, dependencies)
- Organizational assumptions (skills, process)
- Environmental assumptions (security, compliance)

### 11. Misc & Placeholders
- TODO markers / unresolved decisions
- Ambiguous adjectives ("robust", "intuitive") lacking quantification

---

## Question Tracking System

### Question Categories (Expanded)
Map to the 11-category taxonomy for better coverage tracking.

### Question Lifecycle
1. **Raised**: Question identified, logged with phase and category
2. **Queued**: Selected for clarification, prioritized by Impact × Uncertainty
3. **Asked**: Presented to user in sequential flow
4. **Answered**: Response received and validated
5. **Integrated**: Applied to specification with atomic write
6. **Deferred**: Explicitly set aside with reason and revisit trigger

### Question Table Format

Track questions in `analysis-state.md` using tables:

**Unanswered**:
| ID | Question | Category | Raised In | Priority Score | Blocks |
|----|----------|----------|-----------|----------------|--------|

**Answered**:
| ID | Question | Answer | Category | Asked In | Integrated To |
|----|----------|--------|----------|----------|---------------|

**Deferred**:
| ID | Question | Category | Reason | Deferred In | Revisit When |
|----|----------|----------|--------|-------------|--------------|

---

## Memory File Management

### Required Memory File: `analysis-state.md`

Use the template from `assets/analysis-state-template.md`. Key sections:

- Document metadata (title, version, hash)
- Mode selection (SIMPLE/COMPLEX)
- Coverage map (11 categories)
- Analysis iterations table
- Clarification sessions log
- Active and resolved findings
- Question tracking tables (per-phase)
- Assumption register
- User-provided constraints

### Update Protocol

After EACH phase AND after EACH clarification answer:
1. Read current `analysis-state.md`
2. Update phase completion status
3. Update coverage map
4. Update finding statuses
5. Update question tables
6. Record new assumptions
7. Log user decisions
8. Write updated file (atomic)

---

## Analysis Depth Calibration

Match depth to document maturity:

| Document Stage | Analysis Focus |
|----------------|----------------|
| **Concept/Idea** | Feasibility, scope clarity, key assumptions |
| **Draft Spec** | Completeness, internal consistency, missing sections |
| **Detailed Design** | Interface contracts, error handling, edge cases |
| **Implementation Plan** | Dependencies, sequencing, resource conflicts |
| **Review/Audit** | Full SEAMS sweep, stakeholder perspectives |

---

## Quick Assessment Mode

For rapid feedback when full analysis is not needed:

1. **Boundaries**: What's in/out of scope?
2. **One Thread**: Trace critical path from input to output
3. **Three Assumptions**: The riskiest unstated beliefs
4. **Silent Failure**: What breaks without notice?
5. **Naive Question**: What would a newcomer ask that has no answer?

Note: Quick Assessment skips the full phase gate workflow but still creates `analysis-state.md`.

---

## Output Formatting

### Severity Indicators
- 🔴 **Critical**: Blocks progress, must address
- 🟠 **High**: Significant risk, should address soon
- 🟡 **Medium**: Notable issue, plan to address
- 🟢 **Low**: Minor concern, address opportunistically

### Confidence Qualifiers
- **High confidence**: Clear evidence, well-understood domain
- **Medium confidence**: Reasonable inference, some ambiguity
- **Low confidence**: Pattern recognition, needs validation

### Coverage Status Indicators
- ✅ **Clear**: Sufficient information, no clarification needed
- ⚠️ **Partial**: Some gaps, may need clarification
- ❌ **Missing**: Critical gaps, clarification required

---

## Handling Incomplete Information

When specifications are incomplete:
1. Note the gap explicitly with category
2. Score Impact × Uncertainty for prioritization
3. Add to clarification queue if score warrants
4. State what would be needed to complete analysis
5. Offer reasonable assumptions (clearly marked)
6. Add question to tracking system
7. Document in assumption register

---

## Anti-Patterns to Avoid

- Vague criticism without specific evidence
- Recommendations without trade-off analysis
- Analysis paralysis on minor issues
- Ignoring stated constraints to suggest "ideal" solutions
- Failing to update memory after iterations
- Treating all findings as equal severity
- **Proceeding past a gate without user confirmation**
- **Losing track of open questions**
- **Generating output without synthesis approval**
- **Generating B-Specs without traces to A-Specs**
- **Skipping RTM generation for COMPLEX mode**
- **Advancing status without validation**
- **Baselining specs with unresolved critical gaps**
- **Presenting multiple questions at once during CLARIFY**
- **Failing to recommend an answer**
- **Delaying integration until end of CLARIFY phase**
- **Exceeding question limits (5 per session, 10 total)**
