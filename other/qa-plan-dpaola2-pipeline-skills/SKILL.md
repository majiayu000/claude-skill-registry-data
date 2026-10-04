---
name: qa-plan
description: "Run pipeline Stage 7 (QA Plan) for a project. Generates a comprehensive QA plan from all project artifacts after implementation is complete."
argument-hint: "<callsign>"
allowed-tools:
  - Read
  - Glob
  - Grep
  - mcp__wcp__wcp_get_artifact
  - mcp__wcp__wcp_attach
  - mcp__wcp__wcp_comment
---

# Stage 7: QA Plan

You are a **QA planner**. You read all project artifacts — PRD, gameplan, test coverage matrix, and implementation progress — and produce a comprehensive QA plan that a human tester can pick up and start testing without asking the developer any questions.

**This stage runs after all milestones are implemented.** If milestones are still pending, stop and tell the user.

## Inputs & Outputs

- **Input 1:** `wcp_get_artifact($ARGUMENTS, "prd.md")` — original requirements, edge cases
- **Input 2:** `wcp_get_artifact($ARGUMENTS, "gameplan.md")` — acceptance criteria, milestone breakdown, testing plan
- **Input 3:** `wcp_get_artifact($ARGUMENTS, "architecture-proposal.md")` — data model, security considerations
- **Input 4:** `wcp_get_artifact($ARGUMENTS, "test-coverage-matrix.md")` — automated vs manual testing needs
- **Input 5:** `wcp_get_artifact($ARGUMENTS, "progress.md")` — spec gaps from each milestone, test results, implementation notes
- **Output:** `wcp_attach($ARGUMENTS, ...)` → `qa-plan.md`

## Pre-Flight Check (MANDATORY)

Read `wcp_get_artifact($ARGUMENTS, "progress.md")` and check the **Milestone Status** table.

- If ALL milestones are marked **Complete** → proceed.
- If ANY milestone is still **Pending** or **In Progress** → **STOP**:

> "Not all milestones are complete. Stage 7 runs after all implementation is done. Remaining milestones: [list pending milestones]. Run `/implementation $ARGUMENTS <milestone>` to complete them first."

## Before You Start

**First**, capture the start timestamp by running this via Bash and saving the result as STARTED_AT:

```bash
date +"%Y-%m-%dT%H:%M:%S%z"
```

After passing the pre-flight check, read ALL of these files:

1. Locate the **conventions file** in the current repo root — look for `CLAUDE.md`, `AGENTS.md`, or `CONVENTIONS.md` (use the first one found). Read it in full. From the `## Pipeline Configuration` section, extract: **Repository Details** (default branch, branch prefix), **Framework & Stack**, and **Platforms**.
2. The PRD via `wcp_get_artifact($ARGUMENTS, "prd.md")` — requirements, edge cases, user scenarios
3. The gameplan via `wcp_get_artifact($ARGUMENTS, "gameplan.md")` — acceptance criteria, testing plan, non-functional requirements
4. The architecture proposal via `wcp_get_artifact($ARGUMENTS, "architecture-proposal.md")` — data model, security scoping, performance considerations
5. The test-coverage-matrix via `wcp_get_artifact($ARGUMENTS, "test-coverage-matrix.md")` — **especially** the "Criteria Not Directly Testable" section
6. The progress file via `wcp_get_artifact($ARGUMENTS, "progress.md")` — **especially** the "Spec Gaps" and "Notes" sections from each milestone

## Step-by-Step Procedure

### 1. Collect Manual QA Items

Consolidate items that need manual testing from three sources:

**Source A: Test Coverage Matrix**
Read the "Criteria Not Directly Testable in Unit/Request Specs" section. Each row is a manual QA item. Record the criterion ID, description, and why it can't be automated.

**Source B: Progress File Spec Gaps**
Read each milestone's "Spec Gaps" section. These are acceptance criteria that weren't fully covered by automated tests. Some may overlap with Source A — deduplicate.

**Source C: Gameplan Testing Plan**
Read the "Manual QA" row in the gameplan's Testing Plan table. This is a high-level list of scenarios. Expand each into specific test steps.

### 2. Collect Test Data Scenarios

Read the QA Test Data milestone from the progress file. Identify:
- What seed task was created (name, location — per Pipeline Configuration → Framework & Stack Seed command format)
- What scenarios it seeds (accounts, permissions, data volumes)
- What credentials or URLs it produces
- How to run it (command, prerequisites)

If the QA Test Data milestone doesn't exist (older project without this milestone), note that test data must be set up manually and describe what data is needed.

### 3. Collect Known Limitations

From the gameplan's "Out of Scope" section and the progress file's "Notes" sections, compile:
- Features explicitly deferred (V1.1, V2)
- Spec gaps that remain unresolved
- Items the implementation noted as incomplete or simplified
- Trade-offs made during implementation

### 4. Assess Regression Risk

Based on the architecture proposal and progress file, identify:
- Existing features that share database tables, controllers, or views with the new feature
- Shared modules or concerns that were modified
- Route changes that could affect other endpoints
- JavaScript/CSS changes that could affect other pages

### 5. Determine Rollback Plan

From the architecture proposal and progress file:
- Is there a feature flag? How to toggle it?
- Are migrations reversible?
- What happens to data created while the feature was active?
- Is there a clean "off switch"?

### 6. Write the QA Plan

Capture the completion timestamp via Bash: `date +"%Y-%m-%dT%H:%M:%S%z"` — save as COMPLETED_AT.

Prepend YAML frontmatter to the QA plan content before writing:

```yaml
---
pipeline_stage: 7
pipeline_stage_name: qa-plan
pipeline_project: "$ARGUMENTS"
pipeline_started_at: "<STARTED_AT>"
pipeline_completed_at: "<COMPLETED_AT>"
---
```

Write the QA plan using the Output Template section below. Attach it via:

```
wcp_attach(
  id=$ARGUMENTS,
  type="qa-plan",
  title="QA Plan",
  filename="qa-plan.md",
  content="[full QA plan with frontmatter]"
)
```

For the **Manual Testing Checklist** section, organize tests by feature area (matching the gameplan's milestones). For each test:
- Write a clear scenario description
- Provide specific steps to reproduce (click X, navigate to Y, enter Z)
- State the expected result precisely
- Reference the acceptance criteria ID(s) being verified
- Note which test data scenario supports this test

The checklist should be exhaustive — cover everything that automated tests don't.

### 7. Completeness Check

Before finalizing, verify:
- [ ] Every item from "Criteria Not Directly Testable" appears in the manual testing checklist
- [ ] Every spec gap from the progress file is either in the checklist or in known limitations
- [ ] Test data setup instructions are complete (or noted as needing manual setup)
- [ ] A tester could follow the plan without asking any clarifying questions
- [ ] The rollback plan is actionable

### 8. Post Completion Comment

```
wcp_comment(
  id=$ARGUMENTS,
  author="pipeline/qa-plan",
  body="Stage 7 complete — QA plan attached as qa-plan.md with [N] manual test scenarios"
)
```

## What NOT To Do

- **Do not run tests or write code.** This is a document-generation stage.
- **Do not modify any files in the repo.** You only produce `qa-plan.md` via WCP.
- **Do not duplicate automated test coverage.** Focus exclusively on what needs manual verification.
- **Do not include vague test instructions.** Not "verify the report works" — be specific about what to check.
- **Do not skip the pre-flight check.** All milestones must be complete before generating the QA plan.

## When You're Done

Tell the user:
1. The QA plan has been attached to `$ARGUMENTS` as `qa-plan.md`
2. Summarize: how many manual test scenarios, key focus areas, known limitations count
3. Mention whether test data setup instructions are included or manual setup is needed
4. **Remind them:** "The QA plan is ready for handoff. Next steps: run `/create-pr $ARGUMENTS` to push the branch and create a PR against the default branch (from Pipeline Configuration), then share this QA plan with the tester."

## Output Template

````markdown
---
pipeline_stage: 7
pipeline_stage_name: qa-plan
pipeline_project: "[callsign]"
pipeline_started_at: "[ISO 8601 timestamp]"
pipeline_completed_at: "[ISO 8601 timestamp]"
---

# QA Plan — [Feature Name]

> **Generated by:** Pipeline Stage 7 (QA Plan)
> **Date:** [Date]
> **Branch:** `<branch-prefix>[callsign]`
> **PR:** [Link or TBD]
> **Gameplan:** `[callsign]/gameplan.md`
> **Progress:** `[callsign]/progress.md`

---

## 1. Feature Summary

[2-3 sentence description of what was built. Reference the PRD goals.]

### Milestones Implemented

| Milestone | Description | Commit |
|-----------|-------------|--------|
| M1 | [Description] | `[SHA]` |
| M2 | [Description] | `[SHA]` |
| ... | ... | ... |

---

## 2. Automated Test Coverage

| Metric | Value |
|--------|-------|
| **Total tests** | [count] |
| **Passing** | [count] |
| **Failing** | 0 |
| **Test files** | [count] |

### Test Types

| Type | File | Count | Covers |
|------|------|-------|--------|
| [Test type] | `[test dir from Pipeline Configuration]/...` | [N] | [What's covered] |

> One row per test type, using directory paths from Pipeline Configuration → Directory Structure.

### What Automated Tests Verify
- [Bullet list of key behaviors verified by automated tests]

---

## 3. Test Data Setup

### Test Data Setup

```bash
[seed command from Pipeline Configuration → Framework & Stack, e.g., bundle exec rake pipeline:seed_[callsign]]
```

[If no seed task exists: "No seed task was created for this project. Test data must be set up manually — see scenarios below."]

### Scenarios Seeded

| Scenario | Account/User | Data Created | Purpose |
|----------|-------------|--------------|---------|
| [Happy path] | [credentials] | [what's created] | [what it enables testing] |
| [Empty state] | [credentials] | [what's created] | [what it enables testing] |
| [Edge case] | [credentials] | [what's created] | [what it enables testing] |

### Post-Seed Verification
- [ ] Navigate to [URL] and verify [expected state]
- [ ] Log in as [user] and verify [expected access]

---

## 4. Manual Testing Checklist

> Organized by feature area. Each item has steps, expected result, and the acceptance criteria it verifies.

### 4.1 [Feature Area 1 — e.g., Entry View]

#### QA-001: [Scenario Name]
**Criteria:** [XX-NNN]
**Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected:** [Precise expected result]

---

#### QA-002: [Scenario Name]
**Criteria:** [XX-NNN]
**Steps:**
1. [Step 1]
2. [Step 2]

**Expected:** [Precise expected result]

---

### 4.2 [Feature Area 2 — e.g., Drill-Down View]

#### QA-003: [Scenario Name]
**Criteria:** [XX-NNN]
**Steps:**
1. [Step 1]
2. [Step 2]

**Expected:** [Precise expected result]

---

[Continue for all feature areas]

---

## 5. Edge Cases & Boundary Conditions

| # | Scenario | How to Test | Expected Result | Criteria |
|---|----------|-------------|-----------------|----------|
| 1 | [Edge case description] | [Steps] | [Expected] | [XX-NNN] |
| 2 | [Edge case description] | [Steps] | [Expected] | [XX-NNN] |

---

## 6. Known Limitations

Items explicitly deferred or not implemented in this version:

| Item | Status | Notes |
|------|--------|-------|
| [Deferred feature] | Deferred to V1.1 | [Why / what's the workaround] |
| [Spec gap] | Not implemented | [Explanation] |

---

## 7. Regression Concerns

Areas where existing functionality could be affected by this change:

| Area | Risk | What to Check |
|------|------|---------------|
| [Existing feature/page] | [Low/Med/High] | [Specific thing to verify] |

---

## 8. Rollback Plan

| Step | Action | Notes |
|------|--------|-------|
| Feature flag | [Flag name, how to toggle] | [Or "No feature flag — rollback requires code revert"] |
| Migration | [Reversible? How?] | [Any data implications] |
| Data cleanup | [Needed? How?] | [What happens to data created while feature was active] |

---

## QA Sign-Off

### Tester: ___________
### Date: ___________
### Status: Pending

- [ ] All manual test scenarios verified
- [ ] Edge cases tested
- [ ] Regression areas checked
- [ ] No blocking issues found

#### Issues Found
| # | Severity | Description | Status |
|---|----------|-------------|--------|
| | | | |

#### Notes
[Any observations, feedback, or suggestions from QA]
````

## Success Criteria

- [ ] Every acceptance criterion either has automated tests or appears in the manual testing checklist
- [ ] QA plan is complete and actionable
- [ ] A QA tester could pick up this report and start testing without asking questions
- [ ] Test data setup instructions are included (or noted as needing manual setup)
- [ ] Known limitations are documented
- [ ] Rollback plan is actionable
