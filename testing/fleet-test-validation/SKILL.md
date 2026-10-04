---
name: fleet-test-validation
description: How QA validates completed work against predefined TC-XXX criteria — the review-side of QA's dual role. Verify each criterion with evidence.
---

# Test Validation — QA's Review-Side Skill

QA has two phases: PREDEFINITION (before work) and VALIDATION (during review). This skill covers validation — verifying that the implementation satisfies every predefined test criterion.

## When Validation Happens

1. Engineer calls `fleet_task_complete` → task enters review
2. Fleet-ops starts review → may request QA validation
3. QA calls `qa_test_validation(task_id)` → gets validation context
4. QA validates each TC-XXX → posts validation report

## The Validation Process

### Step 1: Call qa_test_validation

```
qa_test_validation(task_id="the-completed-task")
```

This reads:
- Your predefined TC-XXX criteria (from contribution comments)
- The completion summary and PR URL
- Returns a validation context with both side by side

### Step 2: For Each TC-XXX — Check With Evidence

For every criterion you defined during predefinition:

| Verdict | Meaning | Evidence Required |
|---------|---------|-------------------|
| MET | Implementation satisfies criterion | Specific code location or test that proves it |
| NOT MET | Implementation does not satisfy | What's missing specifically |
| PARTIALLY MET | Some aspects satisfied | What's done vs what's still needed |
| CANNOT VERIFY | Need more info to assess | What you need to verify |

Example validation:
```
TC-001: API returns 200 for valid input — MET
  Evidence: fleet/tests/api/test_tasks.py:42 — test_create_task_valid_input

TC-002: API returns 400 for missing required fields — MET
  Evidence: fleet/tests/api/test_tasks.py:58 — test_create_task_missing_title

TC-003: API handles timeout gracefully (3s) — NOT MET
  Missing: No timeout configuration found. No test for timeout scenario.
  Default httpx timeout is 5s, not the 3s specified in requirement.

TC-004: Rate limiting enforced (100 req/min) — CANNOT VERIFY
  Need: Access to rate limit configuration. Not visible in PR diff.
```

### Step 3: Post Validation Report

Post your validation as a typed comment on the target task:
```
## QA Validation Report

**Task:** {task_title}
**Predefined Criteria:** 4 TC-XXX
**Result:** 2 MET, 1 NOT MET, 1 CANNOT VERIFY

### Details:
TC-001: MET — [evidence]
TC-002: MET — [evidence]
TC-003: NOT MET — [what's missing]
TC-004: CANNOT VERIFY — [what's needed]

### Recommendation:
REJECT — TC-003 not addressed. TC-004 needs clarification.
```

### Step 4: Flag to Fleet-Ops

If any criteria are NOT MET, your validation feeds into fleet-ops' review decision. Fleet-ops sees your report and factors it into approve/reject.

## Phase-Appropriate Validation Depth

Match your validation rigor to the delivery phase:

| Phase | What to Validate | How Deep |
|-------|-----------------|----------|
| poc | Happy path only (TC-001 style) | Does it work at all? |
| mvp | Main flows + critical edges | Does it handle the important cases? |
| staging | All predefined criteria + integration | Does it work with other components? |
| production | Everything + performance + resilience | Does it work under stress? |

## What Validation is NOT

- NOT a code review (fleet-ops does that)
- NOT a security review (devsecops does that)
- NOT a design review (architect does that)
- NOT finding new bugs (your predefined criteria IS the checklist)

If you discover issues BEYOND your predefined criteria during validation, create a new concern task — don't expand your validation scope mid-review.
