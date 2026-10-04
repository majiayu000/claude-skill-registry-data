---
name: fleet-completion-checklist
description: Pre-completion verification — everything to check before calling fleet_task_complete. Prevents incomplete submissions.
user-invocable: false
---

# Fleet Completion Checklist

## Before You Call fleet_task_complete

Go through this checklist. Every item must be verified — not assumed.
If an item fails, fix it before completing.

## 1. Verbatim Requirement Check

- [ ] Read your task's `requirement_verbatim` field
- [ ] For EACH acceptance criterion in the verbatim: can you point to specific code/commit that addresses it?
- [ ] If verbatim is empty: STOP — this is a problem. Post a comment asking PM to set it.

## 2. Plan Adherence

- [ ] Your commits match the plan you accepted via `fleet_task_accept`
- [ ] You did NOT add scope beyond the plan (no "while I'm here" changes)
- [ ] You did NOT modify files outside the plan's target files (unless dependencies required it)

## 3. Contributions Consumed

- [ ] Check: did you receive all required contributions? (use `eng_contribution_check`)
- [ ] Architect's design_input → your implementation follows the specified patterns
- [ ] QA's test_definition → your implementation passes all TC-XXX criteria
- [ ] DevSecOps' security_requirement → your implementation satisfies all controls
- [ ] If any required contribution is missing: do NOT complete. Call `fleet_request_input`.

## 4. Tests

- [ ] Tests exist for new functionality
- [ ] All tests pass (run them — don't assume)
- [ ] Run: `.venv/bin/python -m pytest fleet/tests/ -v --tb=short`
- [ ] If tests fail: fix them. If you can't, create a blocker task.

## 5. Code Quality

- [ ] Conventional commits: `type(scope): description [task:XXXXXXXX]`
- [ ] Type hints on public functions
- [ ] No hardcoded paths or secrets
- [ ] No TODO/FIXME left without a follow-up task created

## 6. Delivery Phase Standards

Check your task's `delivery_phase` against `config/phases.yaml`:

| Phase | Tests | Docs | Security |
|-------|-------|------|----------|
| poc | Happy path | README | No secrets in code |
| mvp | Main flows + edges | Setup + usage | Auth + validation |
| staging | Comprehensive | Full docs | Dep audit, pen-test mindset |
| production | Complete | Everything | Certified, compliance-verified |

If your work doesn't meet the phase standard: either improve it or flag to PM
that the phase may need reassessment.

## 7. Summary Quality

Your `fleet_task_complete(summary=...)` summary should answer:
- **What** was done (specific files, specific changes)
- **Why** it was done (references the verbatim requirement)
- **How** it can be verified (specific test command or steps)

**Bad:** "Implemented the feature"
**Good:** "Added JWT auth middleware in fleet/core/auth.py with RS256 signing per architect's design input. 5 tests in test_auth.py cover valid/invalid/expired tokens. Run: pytest fleet/tests/core/test_auth.py"

## 8. What Happens When You Call fleet_task_complete

The tool fires a 12+ operation tree:
1. Push branch to remote
2. Create PR (publication-quality via fleet-pr skill)
3. Update task status → review
4. Create approval for fleet-ops
5. Post completion comment on task
6. Notify IRC #reviews and #fleet
7. Send ntfy notification to PO
8. Update Plane issue state + labels
9. Record trail event
10. Notify contributors (QA, DevSecOps) their input is in review
11. Evaluate parent task (all children done → parent to review)
12. Update sprint progress

You do NOT need to do any of these manually. The tree handles it.
But fleet-ops WILL review your work against this checklist. Submitting
incomplete work wastes a review cycle and gets rejected.

## Quick Decision Tree

```
Did I read the verbatim requirement?
├── No → read it first
└── Yes → Does every criterion have code addressing it?
    ├── No → implement the missing parts
    └── Yes → Did I consume all required contributions?
        ├── No → fleet_request_input for missing ones
        └── Yes → Do all tests pass?
            ├── No → fix the tests
            └── Yes → Does the summary explain what/why/how?
                ├── No → write a proper summary
                └── Yes → fleet_task_complete(summary)
```
