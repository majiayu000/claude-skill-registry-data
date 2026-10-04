---
name: sdlc-checkpoint
description: Save, load, validate, and check status of SDLC artifacts for a TriStar feature. Manages checkpoint state across pipeline phases to enable session continuity.
allowed-tools: Read, Write, Glob, Bash
---

# SDLC Checkpoint Skill

## Prime Directive

**"Never lose progress. Never repeat work."**

This skill manages pipeline state persistence so that SDLC phases can be resumed across sessions without losing context or repeating completed work.

## Arguments

- `--feature=<name>` (required) - Feature name for checkpoint management
- Operation is the first positional argument: `save`, `load`, `status`, `validate`

## Usage

```
/sdlc-checkpoint save --feature=weather-activation
/sdlc-checkpoint load --feature=weather-activation
/sdlc-checkpoint status --feature=weather-activation
/sdlc-checkpoint validate --feature=weather-activation
```

## Operations

### save

Persist the current state of all artifacts for the feature.

1. Scan `docs/artifacts/<feature>/` for spec artifacts
2. Scan `.claude/checkpoints/<feature>/` for execution artifacts
3. Record which artifacts exist and their last-modified timestamps
4. Record the current pipeline stage based on which artifacts are present
5. Write checkpoint state to `.claude/checkpoints/<feature>/checkpoint.json`

### load

Restore context from a saved checkpoint.

1. Read `.claude/checkpoints/<feature>/checkpoint.json`
2. Verify all referenced artifacts still exist at their paths
3. Display current pipeline stage and next expected action
4. Display summary of each artifact (title, date, key metrics)
5. Return the loaded state for the calling skill to use

### status

Display the current pipeline status without modifying anything.

1. Check which artifacts exist for the feature
2. Determine current pipeline stage
3. Display a status table showing each phase and its completion state
4. Highlight the next action needed

### validate

Verify artifact integrity and completeness.

1. Read all artifacts for the feature
2. Check required sections are present in each artifact
3. Verify cross-references between artifacts are valid
4. Report any gaps or inconsistencies

## Storage Rules

| Artifact Type | Storage Path | Phase |
|--------------|-------------|-------|
| Problem Spec | `docs/artifacts/<feature>/problem_spec.md` | requirements |
| Design Spec | `docs/artifacts/<feature>/design_spec.md` | architecture |
| Design Review | `docs/artifacts/<feature>/design_review.md` | design-review |
| Implementation Plan | `docs/artifacts/<feature>/implementation_plan.md` | impl-planning |
| Code Review | `docs/artifacts/<feature>/code_review.md` | code-review |
| Verification Report | `docs/artifacts/<feature>/verification_report.md` | verify |
| Risk Assessment | `docs/artifacts/<feature>/risk_assessment.md` | risk |
| Checkpoint State | `.claude/checkpoints/<feature>/checkpoint.json` | all |
| Artifact Digest | `.claude/checkpoints/<feature>/artifact_digest.md` | all |
| Execution Log | `.claude/checkpoints/<feature>/execution_log.md` | all |

## Pipeline Stage Detection

Determine the current stage by checking which artifacts exist:

```
No artifacts           -> stage: not-started
problem_spec.md        -> stage: requirements-complete
design_spec.md         -> stage: architecture-complete
design_review.md       -> stage: design-review-complete
implementation_plan.md -> stage: impl-planning-complete
(source code exists)   -> stage: implementation-complete
code_review.md         -> stage: code-review-complete
verification_report.md -> stage: verification-complete
risk_assessment.md     -> stage: risk-complete
(PR created)           -> stage: pr-created
```

## Required Sections Validation

### problem_spec.md
- [ ] Feature name and summary
- [ ] Layers affected
- [ ] Requirements with priorities (P0/P1/P2)
- [ ] Acceptance criteria (Given/When/Then)
- [ ] Non-goals with rationale
- [ ] Assumptions with risk_if_wrong
- [ ] Edge cases
- [ ] Quality gate results

### design_spec.md
- [ ] Component catalog (COMP-IDs with paths)
- [ ] Data flows
- [ ] API contracts
- [ ] Data models
- [ ] ADRs (at least 1)
- [ ] Implementation guidelines
- [ ] Quality gate results

### design_review.md
- [ ] Review summary with score
- [ ] Findings by dimension (A through F)
- [ ] Score breakdown table
- [ ] Gate decision (APPROVE / APPROVE_WITH_CONCERNS / REJECT)
- [ ] Recommendations

### implementation_plan.md
- [ ] Wave plan (Waves 1-7)
- [ ] File list with actions (NEW/MODIFY)
- [ ] Acceptance criteria mapping
- [ ] Risk register
- [ ] Design review concerns addressed

### verification_report.md
- [ ] Requirement coverage matrix
- [ ] Test results summary
- [ ] Edge case verification
- [ ] Domain verification results
- [ ] Overall score
- [ ] Quality gate decision

### risk_assessment.md
- [ ] Risk catalog
- [ ] Severity scoring
- [ ] Mitigation strategies
- [ ] Ship recommendation

### code_review.md
- [ ] Files reviewed
- [ ] Findings by severity
- [ ] Positives noted
- [ ] Verdict

## Checkpoint JSON Schema

```json
{
  "feature": "<feature-name>",
  "current_stage": "<stage>",
  "last_updated": "<ISO timestamp>",
  "artifacts": {
    "problem_spec": { "exists": true, "path": "...", "modified": "..." },
    "design_spec": { "exists": true, "path": "...", "modified": "..." },
    "design_review": { "exists": false },
    "implementation_plan": { "exists": false },
    "code_review": { "exists": false },
    "verification_report": { "exists": false },
    "risk_assessment": { "exists": false }
  },
  "pipeline_history": [
    { "stage": "requirements", "completed_at": "...", "result": "approved" },
    { "stage": "architecture", "completed_at": "...", "result": "complete" }
  ]
}
```

## Status Display Format

```
Feature: <name>
Current Stage: <stage>
Last Updated: <timestamp>

Pipeline Status:
  [x] Requirements    -> problem_spec.md (approved)
  [x] Architecture    -> design_spec.md (complete)
  [ ] Design Review   -> (next step)
  [ ] Impl Planning
  [ ] Implementation
  [ ] Code Review
  [ ] Verification
  [ ] Risk Assessment
  [ ] PR Creation
```
