---
name: requesting-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements - dispatches reviewing-code subagent to review implementation against plan or requirements before proceeding
---

# Requesting Code Review

## When to Request Review

Code review MUST always be obtained (without exception) for ALL code changes.

**Mandatory** (code review IS REQUIRED):
- After each task in subagent-driven-development
- After completing ANY feature (any size, any language/framework)
- After ANY bug fix (any severity, any language/framework)
- After ANY refactoring (any scope, any language/framework)
- Before merge to main
- Before creating pull request
- Before claiming work complete
- ALL code changes (regardless of lines changed)
- Changes to critical paths (auth, payment, data handling)
- Test code changes
- Configuration changes with logic
- Database migrations
- Infrastructure-as-code changes

**Exceptions** (ONLY these, code review NOT required):

1. **Pure documentation**: *.md files in docs/ directory only
   - ZERO code changes
   - ZERO configuration changes
   - Documentation ONLY

2. **Configuration-only**: Dependency updates in package.json, tsconfig.json
   - NO logic changes
   - NO script modifications
   - Updates ONLY

3. **Emergency hotfix**: Production down, security breach
   - MUST be reviewed within 24 hours after deployment
   - MUST create incident ticket
   - Emergency = production completely down, active security breach, data loss occurring
   - NOT emergency = "important", "urgent", "CEO wants it", "customer demo"

**When in doubt**: Request code review. There are ONLY 3 exceptions above, no others.

**If you skip review without valid exception 1, 2, or 3**: You violate verifying-before-completion and cannot claim work complete.

## Cannot Proceed Without Review

**IMPORTANT**: Code review is not optional for substantive work.

### What "Cannot Proceed" Means

You CANNOT:
- Mark tasks as complete without code review
- Merge to main without code review
- Create PR without code review
- Claim "work is done" without code review
- Start next batch without reviewing current batch

### Review Gate

```
BEFORE proceeding to next step:

  IF code changes made:
    Has code review been requested?
      NO → STOP - Request review now
      YES → Continue

    Has review been completed?
      NO → STOP - Wait for review completion
      YES → Continue

    Are there Critical issues?
      YES → STOP - Fix before proceeding
      NO → Continue

    Are there Important issues?
      YES → STOP - Fix OR convert to tracked issue with ID
      NO → Continue

    Review status: [Approved / Approved with minor items]
      Other → STOP - Address issues before proceeding

  ONLY THEN: Proceed to next step
```

### Consequences of Skipping Review

If you skip code review without explicit exception:
- Your human partner will lose trust in your work
- You violate practicing-tdd (no verification)
- You violate verifying-before-completion (incomplete verification)
- Issues will be caught later (more expensive to fix)
- You create technical debt (unreviewed code)

## How to Request Review

### Step 1: Prepare for Review

BEFORE requesting review:

- [ ] All tests passing
- [ ] No errors or warnings
- [ ] Code follows TDD (tests written first)
- [ ] Requirements met
- [ ] Evidence of verification captured

**If ANY unchecked**: Fix before requesting review. Don't waste reviewer's time.

### Step 2: Provide Context

When requesting review, include:

```markdown
I need code review for [feature/bugfix/refactor name].

**Context:**
- Completed tasks: [list]
- Requirements met: [reference to plan/spec]
- Tests added: [count] tests, all passing
- TDD followed: [Yes/No with attestation]

**Files for review:**
- src/[file].ts (modified - [what changed])
- src/[file].ts (new - [what it does])
- tests/[file].test.ts (modified - [tests added])

**Testing evidence:**
```
[paste test output showing all passing]
```

**Ready for review.**
```

### Step 3: Get git SHAs

```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

### Step 4: Dispatch reviewing-code subagent

Use Task tool with `general-purpose` subagent type, instructing it to use the `reviewing-code` skill.

**Provide to subagent:**
- What was implemented (feature/task description)
- Plan or requirements it should meet (file path or description)
- Git range to review (BASE_SHA..HEAD_SHA)
- Any specific concerns to focus on

### Step 5: Act on feedback

- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with reasoning)

## Handling Review Status

### Review Outcomes

**Status: Approved**
```
All issues resolved or no issues found.

Action: You may proceed to next step (merge, next batch, etc.)
```

**Status: Approved with minor items**
```
No Critical or Important issues.
Minor suggestions noted for future work.

Action: You may proceed, but address minor items when practical.
```

**Status: Needs revision**
```
Critical or Important issues found.

Action:
1. STOP - Do not proceed
2. Fix all Critical issues (MUST be 0)
3. Fix all Important issues OR convert to tracked issue with ID (cannot be "acknowledged" without issue)
4. Re-run tests
5. Provide evidence of fixes
6. Request follow-up review if needed
7. Only proceed after approval
```

**Status: Blocked**
```
Fundamental issues requiring rework.

Action:
1. STOP - Do not proceed
2. Discuss issues with reviewer or human partner
3. May require significant rework or redesign
4. Do NOT attempt to "work around" blocking issues
```

### Cannot Proceed Until Approved

**Important**: You cannot claim work complete or proceed to next phase until review status is "Approved" or "Approved with minor items".

Attempting to proceed with "Needs revision" or "Blocked" status violates verifying-before-completion skill.

## Example

### Example: Required Code Review

```
Agent: "I've completed the user authentication feature."

[Check: Is code review required?]

Code changes made: Yes
Lines changed: 350
Feature complete: Yes

→ Code review IS REQUIRED

Agent: "I need code review before marking this complete."

[Requests review]

Review outcome: Needs revision (2 Important issues)

Agent: [Thinks: "These are minor, I'll just merge"]

RED FLAG: Cannot proceed with "Needs revision" status

Agent: "I need to fix the Important issues before proceeding."

[Fixes issues, re-runs tests]

Agent: "Issues fixed. Ready for follow-up review."

[Requests follow-up review]

Review outcome: Approved

Agent: "Code review approved. Feature complete."

[Can now proceed to merge/PR]
```

### Example: Task-Based Review

```
[Just completed Task 2: Add verification function]

You: Let me request code review before proceeding.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Use Task tool with general-purpose subagent:]
"Use the reviewing-code skill to review my implementation of Task 2 from
.wrangler/plans/deployment-plan.md. Review changes from a7981ec..3df7661.

I implemented verification and repair functions for conversation index
(verifyIndex() and repairIndex() with 4 issue types). Please check if
implementation meets plan requirements and identify any quality issues."

[Subagent returns structured review]:
  Overall Assessment: Ready to merge with minor fixes

  Strengths:
  - Clean architecture with proper separation
  - Real integration tests, not just mocks
  - Comprehensive issue type detection

  Critical Issues: 0
  Important Issues: 1
    - Missing progress indicators for long-running operations
  Minor Issues: 1
    - Magic number (100) for reporting interval should be constant

  Recommendation: Fix Important issue, Minor can be deferred

You: [Fix progress indicators]
You: [Continue to Task 3]
```

## Integration with Workflows

**Subagent-Driven Development:**
- Review after EACH task
- Catch issues before they compound
- Fix before moving to next task

**Executing Plans:**
- Review after each batch (3 tasks)
- Get feedback, apply, continue

**Ad-Hoc Development:**
- Review before merge
- Review when stuck

## Common Rationalizations (DO NOT ACCEPT)

| Rationalization | Why It's Wrong | Correct Action |
|----------------|----------------|----------------|
| "This is too trivial to review" | Trivial changes cause production incidents | Request review anyway (takes 2 minutes) |
| "I'm the expert, no one else can review" | Experts have blind spots review catches | Request review from anyone on team |
| "We're too busy for review" | Busy doesn't exempt safety | If too busy to review, too busy to merge safely |
| "I'll get review after merging" | Post-merge review never happens | Review BEFORE merge, always |
| "The tests pass, that's enough" | Tests necessary but not sufficient | Tests + human review both required |
| "It's only N lines changed" | Size doesn't determine bug potential | ALL code changes require review |
| "No one else is available" | If not P0, it can wait | Wait for reviewer or escalate |
| "This is blocking me" | Being blocked doesn't exempt review | Work on different task while waiting |
| "I'll skip review just this once" | "Just once" becomes habit | Follow process every time without exception |

## Red Flags - STOP IMMEDIATELY

If you catch yourself:
- Thinking "I'll skip review this time"
- Thinking "It's too small to need review"
- Thinking "I'll just merge and review later"
- Proceeding to next batch without reviewing current batch
- Marking work complete without code review
- Assuming review is optional for your workflow
- Creating PR without code review first
- Merging to main without code review
- Claiming any exception other than 1, 2, or 3
- Using vague exception language ("it's simple", "it's small")

THEN:
- STOP immediately
- Request code review
- Wait for approval
- This is mandatory, not optional

**If reviewer wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification

See `reviewing-code` skill for detailed review framework and output format.
