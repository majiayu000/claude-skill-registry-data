---
name: specification-refiner
description: >
  Systematic analysis and refinement of specifications, requirements, architecture designs, and project plans.
  Use when the user wants to identify gaps, weaknesses, inefficiencies, or complications in a proposed plan, specification, or design document.
  Triggers on gap analysis, specification review, requirements analysis, architecture critique, design validation, plan assessment, weakness identification, assumption auditing, or when users share specs/plans asking for feedback.
  Produces actionable findings with remediations and maintains analysis state across iterations.
---

# Specification Refiner

Systematically analyze and refine specifications, requirements, and architectural designs through iterative gap analysis with persistent memory and explicit user confirmation at each phase.

## Core Workflow

```
0. ASSESS     → Evaluate complexity, select mode, confirm with user
1. INGEST     → Load document, confirm understanding with user
2. ANALYZE    → Run SEAMS + Critical Path, present preliminary findings
3. PRESENT    → Surface detailed findings, manage questions with user
4. ITERATE    → Accept changes, re-analyze, present deltas
5. SYNTHESIZE → Present comprehensive summary for user approval
6. OUTPUT     → Generate refined specification(s) in Draft status
7. VALIDATE   → Review, validate traceability, advance status
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

Run analysis frameworks based on mode.

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

### Question Management
- Add new questions discovered during analysis with "Raised In: Phase 2: ANALYZE"
- Note which findings are blocked by unanswered questions

### Phase 2 Gate

Present preliminary findings summary with severity counts, top 3 issues, question status, and blocked findings. See `references/gate-templates.md` for format. Wait for user confirmation—user may answer blocking questions here.

---

## Phase 3: PRESENT

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

### Phase 3 Gate

Present findings summary with severity counts, question status, and assumptions made. Offer options: (1) Iterate, (2) Skip to Synthesize, (3) Answer questions, (4) Review details. See `references/gate-templates.md` for format.

---

## Phase 4: ITERATE

When user provides new information, constraints, or requests changes:

### Actions
1. **Validate new input** against existing analysis
2. **Identify affected areas** in the specification
3. **Re-run analysis** on affected sections only (delta analysis)
4. **Assess cascading effects** on previously-identified issues
5. **Update memory file** with new state

### Question Management
- Add new questions with "Raised In: Phase 4: ITERATE"
- Check if new input answers existing questions
- Update all question statuses

### Phase 4 Gate

Present delta summary: changes incorporated, new/modified/resolved findings, key changes, question status. Offer options: (1) Continue iterating, (2) Synthesize, (3) Review findings. See `references/gate-templates.md` for format.

---

## Phase 5: SYNTHESIZE

Before generating any output, present a comprehensive summary for user approval.

### Summary Contents

Present comprehensive summary covering:
- **Document Overview**: Title, mode, iteration count
- **Findings Resolution**: By severity with resolved/unresolved breakdown, key resolutions, unresolved critical/high items
- **Questions Status**: Answered, unanswered (with impact), deferred (with reason)
- **Assumptions**: Confirmed vs. unverified
- **Proposed Output Structure**: Based on mode (single doc for SIMPLE, separate files for COMPLEX)

See `references/gate-templates.md` for full format.

### Phase 5 Gate

Offer options: (1) Approve and output, (2) Return to iterate, (3) Modify structure, (4) Answer questions. Wait for explicit approval before generating output.

---

## Phase 6: OUTPUT

Generate refined specification(s) based on mode, all in **Draft** status.

### SIMPLE Mode Output
Generate single A-Spec document (`refined-specification.md`) with:
- Numbered requirements (`A-REQ-001`, `A-REQ-002`, etc.)
- All resolved findings incorporated
- Selected remediations applied
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
5. Prompt transition to Phase 7

### Phase 6 Completion

Present: mode, files created with requirement counts, RTM summary (COMPLEX mode), findings addressed, assumptions documented. Prompt user to proceed to Phase 7. See `references/gate-templates.md` for format.

---

## Phase 7: VALIDATE

Final review and validation phase ensuring specifications are comprehensive, traceable, and approved. **Mandatory for both SIMPLE and COMPLEX modes.**

### Status Workflow
Specifications progress through statuses:
```
Draft → Reviewed → Approved → Baselined
```

- **Draft**: Initial output from Phase 6 (automatic)
- **Reviewed**: Technical review complete, no critical gaps
- **Approved**: Stakeholder sign-off received
- **Baselined**: Locked for change control

### Validation Actions
1. **Completeness check**: All required sections present, cross-references valid
2. **RTM validation** (COMPLEX): Coverage percentage, gap identification
3. **Traceability check** (COMPLEX): All B-Reqs trace to A-Reqs
4. **Consistency check**: Terminology, formatting, priority scales aligned
5. **Present validation findings** with severity

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

### Phase 7 Gate
Present validation summary with:
- Current status and proposed advancement
- RTM coverage metrics (COMPLEX mode)
- Completeness and consistency checklist
- Validation findings
- Options: advance status, return to fix issues, review details

See `references/gate-templates.md` for full template.

---

## Question Tracking System

### Question Categories
- **Technical**: Architecture, implementation, performance
- **Process**: Workflow, governance, approval
- **Scope**: Boundaries, requirements, features
- **Stakeholder**: Roles, responsibilities, ownership
- **Timeline**: Sequencing, dependencies, deadlines

### Question Lifecycle
1. **Raised**: Question identified, logged with phase
2. **Answered**: Response received from user or inferred from analysis
3. **Deferred**: Explicitly set aside with reason and revisit trigger

### Question Table Format

Track questions in `analysis-state.md` using tables for Unanswered (ID, Question, Category, Raised In, Blocks), Answered (ID, Question, Answer, Answered By, Answered In), and Deferred (ID, Question, Reason, Deferred In, Revisit When).

---

## Memory File Management

### Required Memory File: `analysis-state.md`

Use the template from `assets/analysis-state-template.md`. Key sections:

- Document metadata (title, version, hash)
- Mode selection (SIMPLE/COMPLEX)
- Analysis iterations table
- Active and resolved findings
- Question tracking tables (per-phase)
- Assumption register
- User-provided constraints

### Update Protocol

After EACH phase:
1. Read current `analysis-state.md`
2. Update phase completion status
3. Update finding statuses
4. Update question tables
5. Record new assumptions
6. Log user decisions
7. Write updated file

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

---

## Handling Incomplete Information

When specifications are incomplete:
1. Note the gap explicitly
2. State what would be needed to complete analysis
3. Offer reasonable assumptions (clearly marked)
4. Add question to tracking system
5. Ask user to confirm or provide missing details at next gate
6. Document in assumption register

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
