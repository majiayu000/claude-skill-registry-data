---
name: verification-gate
description: "Verification gate before claiming task completion. No completion claim without fresh evidence."
---

# Verification Gate

## Overview

Claiming work is done without verification is not efficiency -- it is dishonesty.

**Core principle:** Evidence first, claims second. Always.

**Violating the letter of this rule violates its spirit.**

## Iron Rule

```
NO COMPLETION CLAIM WITHOUT FRESH VERIFICATION EVIDENCE
```

If you did not run the verification command in this message, you cannot claim it passes.

## 3 Stages

### Stage 1: Evidence Collection

```
BEFORE ANY status claim or satisfaction expression:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Read the full output, check exit code, count failures
4. VERIFY: Does the output support the claim?
   - NO: State the real status with evidence
   - YES: State the claim with evidence
5. ONLY THEN: Make the claim

Skip any step = not verification, but fabrication
```

**Common verification requirements:**

| Claim | Required Evidence | NOT Sufficient |
|-------|-------------------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, guessing |
| Build succeeds | Build command: exit 0 | Linter passes, logs look fine |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Subagent completed | VCS diff shows changes | Subagent said "success" |
| Requirements met | Line-by-line checklist | Tests pass |

### Stage 2: Code Review

When all tasks are complete, run an independent review:

```
[Spawn a reviewer subagent]:

task="Code Review -- [feature/change name]

## What Was Done
[Summary]

## Requirements
[From plan/spec]

## Changed Files
[List]

## Task
1. Read the changed files
2. Compare requirements line by line
3. Security check (OWASP Top 10)
4. Clean code check
5. Test quality check

Report:
- Strengths
- Issues (Critical / Important / Minor)
- Verdict: Approved / Changes required"
```

**Review result:**
- Critical issue --> Fix IMMEDIATELY
- Important issue --> Fix before proceeding
- Minor issue --> Note it, fix later
- Reviewer is wrong --> Object with technical justification

### Stage 3: Completion

After review passes, present options:

1. **Merge** -- Merge into the main branch
2. **PR** -- Create a pull request
3. **Keep** -- Keep the branch, merge later
4. **Delete** -- Delete the branch (if it did not work out)

Steps for each option:
- Merge: `git checkout main && git merge <branch>`
- PR: `gh pr create --title "..." --body "..."`
- Keep: Inform the user of the branch name
- Delete: `git branch -d <branch>` (get confirmation)

## Red Flags -- STOP

If you catch yourself thinking or saying:

- **"It probably works"** --> VERIFY
- **"I am sure"** --> Certainty is not evidence
- **"The agent said it succeeded"** --> Verify independently
- **"Great!", "Perfect!", "Done!", "All set!"** --> No satisfaction expressions BEFORE verification
- **"Should pass"**, **"probably"**, **"looks like"** --> RUN the verification command
- **"Just this once"** --> No exceptions
- **"Linter passed"** --> Linter is not a compiler
- **"I am tired"** --> Fatigue is not an excuse
- **"Partial check is enough"** --> Partial proves nothing

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "It works now" | RUN the verification |
| "I am sure" | Confidence is not evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter is not a compiler |
| "Agent said success" | Verify independently |
| "I am tired" | Fatigue is not an excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words, rule does not apply" | Spirit overrides letter |

## Verification Patterns

**Tests:**
```
CORRECT: [Run test command] [See: 34/34 passed] "All tests pass"
WRONG:   "Should pass now" / "Looks correct"
```

**Regression tests (TDD Red-Green):**
```
CORRECT: Write --> Run (passes) --> Revert fix --> Run (MUST FAIL) --> Restore --> Run (passes)
WRONG:   "I wrote a regression test" (without red-green verification)
```

**Build:**
```
CORRECT: [Run build] [See: exit 0] "Build passes"
WRONG:   "Linter passed" (linter does not check compilation)
```

**Requirements:**
```
CORRECT: Re-read plan --> Create checklist --> Verify each --> Report gaps or completion
WRONG:   "Tests pass, phase complete"
```

**Subagent delegation:**
```
CORRECT: Subagent said success --> Check VCS diff --> Verify changes --> Report real status
WRONG:   Trust the subagent report
```

## When to Apply

**ALWAYS, BEFORE any of these:**
- Any form of success/completion claim
- Satisfaction expressions
- Any positive statement about work status
- Commit, PR creation, task completion
- Moving to the next task
- Delegating to subagents

## Integration

**Related skills:**
- **`tdd-workflow`** -- For regression test verification
- **`subagent-execution`** -- Pass through this gate after every task
- **`systematic-debugging`** -- When verification fails
