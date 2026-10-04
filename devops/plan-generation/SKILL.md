---
name: plan-generation
description: Generate implementation plans for projects. Use when creating a plan, drafting implementation steps, or when user mentions "create plan", "implementation plan", "planning phase", or "plan this project".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# Plan Generation Skill

You are creating an implementation plan for a POS project. This is a critical document that must be approved before any work begins.

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

## Process

1. **Load Project Context**
   - Read the project YAML from `{teams_dir}/{team}/projects/{project-name}.yaml`
   - Understand requirements, constraints, and acceptance criteria
   - Identify the assigned team and available engineers

2. **Analyze the Workspace**
   - If workspace path is specified, explore the codebase
   - Understand existing architecture and patterns
   - Identify files that will need modification

3. **Design Technical Approach**
   - Determine architecture decisions
   - Choose appropriate technologies/patterns
   - Document key decisions with rationale

4. **Break Down into Tasks**
   - Create phases for logical groupings
   - Each task should be:
     - Assignable to a single engineer specialty
     - Completable in a focused work session
     - Have clear inputs and outputs
   - Define dependencies between tasks
   - Assign appropriate engineer type to each task

5. **Identify Risks**
   - Technical risks
   - Dependency risks
   - Timeline risks
   - Document mitigations for each

6. **Create Plan Document**
   - Save to: `{teams_dir}/{team}/projects/{project}/plans/plan-v1.md`
   - Update project.yaml status to `planning`

## Available Engineer Specialties

| Engineer | Use For |
|----------|---------|
| eng-backend | APIs, services, business logic, databases |
| eng-frontend | UI components, pages, client-side logic |
| eng-testing | Tests, coverage, quality assurance |
| eng-devops | CI/CD, deployment, infrastructure |
| eng-security | Security reviews, vulnerability fixes |

## Plan Template

```markdown
# Implementation Plan: {PROJECT_NAME}

**Version:** 1.0
**Created:** {DATE}
**Author:** tpm-{team}
**Status:** PENDING_APPROVAL

---

## Overview

{Brief description of what this project accomplishes}

## Requirements

From project.yaml:
1. {Requirement 1}
2. {Requirement 2}

## Technical Approach

### Architecture
{Describe the architectural approach}

### Key Decisions
1. **{Decision 1}**: {Rationale}
2. **{Decision 2}**: {Rationale}

### Technologies/Patterns
- {Technology/pattern 1}: {Why}

## Task Breakdown

### Phase 1: {Phase Name}
- [ ] **Task 1.1**: {Description}
  - Engineer: eng-{specialty}
  - Files: {files to create/modify}
  - Dependencies: none
  - Estimated complexity: low/medium/high

- [ ] **Task 1.2**: {Description}
  - Engineer: eng-{specialty}
  - Files: {files to create/modify}
  - Dependencies: Task 1.1

### Phase 2: {Phase Name}
...

## Testing Strategy

- Unit tests: {approach}
- Integration tests: {approach}
- Manual verification: {steps}

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {Risk 1} | Medium | High | {Mitigation} |

## Dependencies

### External
- {External dependency 1}

### Internal
- {Internal dependency}

## Definition of Done

- [ ] All tasks completed
- [ ] Tests passing
- [ ] Code reviewed by TPM
- [ ] Documentation updated
- [ ] Acceptance criteria met

---

## Approval

**Submitted for approval:** {DATE}

**CTO Review:**
- [ ] Technical approach approved
- [ ] Risk assessment adequate
- [ ] Resource allocation appropriate

**Decision:** PENDING

**Notes:**
```

## Output Format

When reporting results:
1. **Summary** — 2-3 sentence overview of what was done
2. **Details** — Specific findings, changes, or recommendations
3. **Next Steps** — What should happen next (if applicable)
4. **Artifacts** — Files created or modified, with paths

## Output

After creating the plan:
- Report the plan file path
- Summarize the phases and task count
- List any risks identified
- Note that plan requires CTO approval before execution

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
