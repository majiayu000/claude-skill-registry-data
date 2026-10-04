---
name: fleet-ops-review-protocol
description: How fleet-ops does a REAL review — 10-step structured protocol. Verbatim match, trail verification, contribution check, phase standards. Not a rubber stamp.
user-invocable: false
---

# Fleet-Ops Review Protocol

## The Principle

Fleet-ops does NOT rubber-stamp. A review under 30 seconds is a red flag.
You READ the actual work. You COMPARE to the verbatim requirement. You
VERIFY the trail. You CHECK that contributions were received and addressed.

The immune system watches for rubber-stamping.

## When This Applies

When you have pending approvals. Call `ops_real_review(task_id)` — your
group call that gathers task data, trail events, contributions, phase
standards, and produces a structured review. Then apply this protocol.

## The 10-Step Review

### Step 1: Read the Verbatim Requirement
- What did the PO ask for, in their exact words?
- If no verbatim → this is ALREADY a finding ("No verbatim set — cannot verify work matches PO intent")

### Step 2: Read the Completion Summary
- What does the agent CLAIM they did?
- Does the summary explain WHAT, WHY, and HOW to verify?
- A vague summary ("Implemented the feature") is a finding

### Step 3: Read the PR (if exists)
- Conventional commits? (`type(scope): description [task:XXXXXXXX]`)
- PR body has changelog, diff table, references?
- Code changes match what was claimed?

### Step 4: Verify the Trail
- Are stage transition events recorded in board memory?
- Did the task go through ALL required stages for its type?
  - epic: conversation → analysis → investigation → reasoning → work
  - story: conversation → reasoning → work
  - task: reasoning → work
  - bug: analysis → reasoning → work
- MISSING TRAIL = finding ("No trail events — methodology compliance cannot be verified")

### Step 5: Verify Contributions
- For the task type and delivery phase, what contributions were REQUIRED?
  (Check synergy matrix via the review data)
- Were they received? Check typed comments:
  - `**Contribution (design_input)** from architect`
  - `**Contribution (qa_test_definition)** from qa-engineer`
  - `**Contribution (security_requirement)** from devsecops-expert`
- MISSING REQUIRED CONTRIBUTION = finding

### Step 6: Check Phase Standards
- What delivery phase is this task? (poc/mvp/staging/production)
- Does the work meet that phase's standards from `config/phases.yaml`?
  - poc: happy path tests, readme, no secrets
  - mvp: main flows + edges, setup docs, auth + validation
  - staging: comprehensive tests, full docs, dep audit
  - production: complete everything
- Work below phase standard = finding

### Step 7: Compare Work to Verbatim (Criterion by Criterion)
- For EACH acceptance criterion in the verbatim:
  - Is it addressed in the implementation?
  - Can you point to specific code/commit/test?
  - Not "probably covered" — EVIDENCE
- Unaddressed criterion = finding

### Step 8: Check QA Validation (if QA contributed)
- Did QA validate their predefined TC-XXX criteria?
- Is there a `qa_validation` typed comment?
- Did all TC-XXX pass? Or are there flagged gaps?

### Step 9: Check Security (if DevSecOps contributed)
- Did DevSecOps do a security review?
- Is `security_hold` set? If so, it BLOCKS your approval.
- Were security requirements addressed?

### Step 10: Decision

| Situation | Decision | What to Do |
|-----------|----------|-----------|
| All checks pass, no findings | **APPROVE** | `fleet_approve(id, "approved", "Requirement met: {specifics}")` |
| Minor issues, judgment call | **ESCALATE** | `fleet_escalate("Needs human review: {issues}")` |
| Missing trail, contributions, or criteria unaddressed | **REJECT** | `fleet_approve(id, "rejected", "Issues: {specific feedback}")` |

### On Rejection

Your rejection comment MUST include:
1. **What** specifically failed (which step, which criterion)
2. **Why** it failed (what was expected vs what was found)
3. **What to fix** (specific action the agent should take)
4. **Which stage** to return to (readiness regresses, stage may regress)

The system automatically:
- Regresses readiness
- Regresses task stage (back to reasoning)
- Signals the doctor (repeated rejections → pattern detection)
- Posts to IRC #reviews
- Records trail

## Red Flags (Immune System Watches For)

- Approval in < 30 seconds (didn't read the work)
- "Looks good" without specifics (rubber stamp)
- Approving without trail verification (skipped step 4)
- Approving with missing required contributions (skipped step 5)
- Approving below phase standards (skipped step 6)

## Using pr-review-toolkit

For PRs, you have 6 parallel sub-agents via `/review-pr`:
- **code-reviewer** — CLAUDE.md compliance, style, bugs (0-100 score)
- **code-simplifier** — clarity, consistency, maintainability
- **comment-analyzer** — comment accuracy, doc completeness
- **pr-test-analyzer** — behavioral coverage, test gaps (1-10 rating)
- **silent-failure-hunter** — error handling audit
- **type-design-analyzer** — type encapsulation, invariants (1-10)

These handle the TECHNICAL review dimensions. YOU handle the METHODOLOGY
review: verbatim match, trail, contributions, phase standards, PO intent.

Together = a thorough review. Neither alone is sufficient.
