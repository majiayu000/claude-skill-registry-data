---
name: phase-enforcement
description: AID methodology phase gate enforcement. Ensures work follows correct 6-phase order (Discovery -> PRD -> Tech Spec -> Impl Plan -> Dev -> QA & Ship). Enforces gates, validates transitions. Use before any work to check the current phase and refuse work belonging to a later phase.
---

# Phase Enforcement

Check current phase before any work. REFUSE work that belongs to a later phase.

## Exceptions (skill does not block these)

Always Allowed: Reading files, documentation updates, questions, /phase, /gate-check

Override: User says "override: [reason]" - logged to .aid/overrides.log

## Priority 1: Phase Gate Enforcement

Before any work:
1. Read `.aid/state.json` for current phase
2. Read `.aid/context.json` for current task and step
3. Classify the requested work
4. Check if work is allowed in current phase
5. REFUSE if not allowed (show violation)
6. At phase completion: mandatory sub-agent review
7. After review passes: collect feedback via /aid end

## Mandatory: Sub-Agent Review at Transitions

Before Phase N -> N+1:

1. Spawn the **phase-review-agent** using the Task tool:
   ```
   Task(
     subagent_type: "general-purpose",
     model: "opus",
     prompt: [Read ../../agents/phase-review-agent.md, replace {{PHASE_NUMBER}}, {{PHASE_NAME}}, {{PHASE_CHECKLIST}}, {{DELIVERABLES}}],
     description: "Phase gate validation"
   )
   ```
2. Sub-agent reviews all deliverables
3. Returns PASS/FAIL with findings
4. FAIL: Address issues, retry
5. PASS: Proceed to feedback

### Variable Extraction

| Variable | Source | How to Extract |
|---|---|---|
| `{{PHASE_NUMBER}}` | `.aid/state.json` | Read `current_phase` field |
| `{{PHASE_NAME}}` | `.aid/state.json` | Read `phase_name` field |
| `{{PHASE_CHECKLIST}}` | Gate Check Requirements (below) | Use the checklist for the current phase transition |
| `{{DELIVERABLES}}` | Phase output folders | Read all files from the phase's output folder (e.g., `docs/research/` for Phase 0, `docs/prd/` for Phase 1) |

## 6-Phase Development Lifecycle

| Phase | Name | Document | Folder |
|---|---|---|---|
| 0 | Discovery | Research & Validation | docs/research/ |
| 1 | PRD | Product Requirements | docs/prd/ |
| 2 | Tech Spec | Technical Specification | docs/tech-spec/ |
| 3 | Impl Plan | Task Breakdown | docs/implementation-plan/ |
| 4 | Development | Code & Tests | src/ |
| 5 | QA & Ship | Deployment | Production |

## Work Classification

| Category | Examples | First Allowed |
|---|---|---|
| research | Stakeholders, competitive analysis, discovery | Phase 0 |
| requirements | PRD, user stories, acceptance criteria | Phase 1 |
| architecture | System design, APIs, schemas | Phase 2 |
| planning | Jira, task breakdown, consolidation | Phase 3 |
| coding | Components, tests, implementation | Phase 4 |
| qa | Testing, deployment, release | Phase 5 |

## Phase Permissions

| Phase | Allowed | Blocked |
|---|---|---|
| 0 Discovery | research | requirements, architecture, planning, coding, qa |
| 1 PRD | research, requirements | architecture, planning, coding, qa |
| 2 Tech Spec | research, requirements, architecture | planning, coding, qa |
| 3 Impl Plan | research, requirements, architecture, planning | coding, qa |
| 4 Development | research, requirements, architecture, planning, coding | qa |
| 5 QA & Ship | all | - |

## Phase-Specific WHY Questions

| Phase | Core WHY Question |
|---|---|
| 0 Discovery | "WHY is this problem worth solving?" |
| 1 PRD | "WHY does the user need this?" |
| 2 Tech Spec | "WHY this architecture?" |
| 3a Consolidation | "WHY does this contradiction exist? WHY this resolution?" |
| 3b Breakdown | "WHY this task size? WHY these dependencies?" |
| 3c Jira Population | "WHY is this information complete? WHY can dev work from this alone?" |
| 4 Development | "WHY this code? WHY these connections?" |
| 5 QA & Ship | "WHY is this test? WHY is this ready?" |

## Gate Check Requirements

### Phase 0 -> 1
- [ ] Research folder exists in docs/research/
- [ ] Research report with problem statement (SCQ format)
- [ ] Stakeholders identified and mapped
- [ ] Competitive analysis documented
- [ ] Traceability matrix created
- [ ] Go/No-Go decision documented
- [ ] Sub-agent review PASSED

### Phase 1 -> 2
- [ ] PRD exists in docs/prd/
- [ ] User stories defined
- [ ] Acceptance criteria complete
- [ ] Requirements linked to research IDs (RES-XXX)
- [ ] Sub-agent review PASSED

### Phase 2 -> 3
- [ ] Tech Spec exists
- [ ] Architecture diagram
- [ ] API contracts
- [ ] Security assessment
- [ ] Sub-agent review PASSED

### Phase 3 -> 4
- [ ] Implementation Plan exists
- [ ] Tasks broken down
- [ ] Dependencies identified
- [ ] Test strategy defined
- [ ] Sub-agent review PASSED

### Phase 4 -> 5
- [ ] Code implemented
- [ ] Tests passing
- [ ] Coverage meets threshold
- [ ] Sub-agent review PASSED

## Violation Template

```
PHASE GATE VIOLATION

Current Phase: [N] [Name]
Requested: [What]
Category: [Category]

This work belongs to Phase [X].

Complete first: [List]

Commands: /phase, /gate-check, /aid end
```

## Sub-Agent Review Prompts

### Discovery Review (Phase 0 -> 1)
- [ ] Problem statement clear (SCQ format)
- [ ] Stakeholders identified
- [ ] Competitive analysis documented
- [ ] Traceability matrix created
- [ ] Go/No-Go decision with justification
- [ ] No implementation details

### PRD Review (Phase 1 -> 2)
- [ ] Problem statement clear
- [ ] User stories As/I want/So that
- [ ] Acceptance criteria per story
- [ ] Non-functional requirements
- [ ] Measurable success metrics
- [ ] No implementation details

### Tech Spec Review (Phase 2 -> 3)
- [ ] Architecture diagram
- [ ] Components defined
- [ ] Data models (TypeScript)
- [ ] API contracts
- [ ] Database schema
- [ ] Security assessment
- [ ] References PRD

### Impl Plan Review (Phase 3 -> 4)

Phase 3 Golden Rules:
1. NO WORD LEFT BEHIND - PRD → Epic/Story, Tech Spec → Task
2. SMALL TASKS - Larger docs = smaller tasks
3. PROCESS IN CHUNKS - Read → Write immediately
4. VERIFY - 100% coverage required

Sub-Phases: 3a Consolidation → 3b Breakdown → 3c Enrichment → 3d Jira → 3e Verification

Checklist:
- [ ] Contradiction log created
- [ ] Source documents fixed
- [ ] Consolidated spec created
- [ ] Hierarchy: Epic → Story → Task
- [ ] Tasks sized appropriately
- [ ] All 8 required fields per Task
- [ ] 100% PRD/Tech Spec coverage
- [ ] Enriched files staged
- [ ] Jira populated with ADF

### Development Review (Phase 4 -> 5)
- [ ] All tasks complete
- [ ] Tests passing
- [ ] Coverage >= 70%
- [ ] Lint passes
- [ ] Build succeeds
- [ ] No critical vulnerabilities

## State Files

Read both before enforcing gates: `state.json` determines the phase, `context.json` provides task-level awareness.

`.aid/state.json`
```json
{
  "current_phase": 2,
  "phase_name": "tech-spec",
  "feature_name": "user-auth",
  "phases_completed": [0, 1],
  "subagent_review": {"phase_0": {"status": "passed"}, "phase_1": {"status": "passed"}}
}
```

`.aid/context.json`
```json
{
  "current_task": "Design authentication API",
  "current_step": "Define API contracts",
  "progress": "in-progress",
  "last_updated": "2024-12-21T10:00:00Z"
}
```
