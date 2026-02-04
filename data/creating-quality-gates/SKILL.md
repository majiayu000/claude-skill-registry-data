---
name: Creating Quality Gates
description: Establish workflow boundary checklists with clear pass/fail criteria and escalation procedures
when_to_use: when creating pre-merge checklists, establishing workflow boundaries, building verification procedures, or defining quality gates between development phases
version: 1.0.0
---

# Creating Quality Gates

## Overview

Create structured quality gates at workflow boundaries with clear "Must Pass" vs "Should Review" criteria, exact commands, and escalation procedures.

**Announce at start:** "I'm using the creating-quality-gates skill to establish this quality gate."

## When to Use

- Establishing pre-merge verification
- Creating phase transition gates (design → implement)
- Building deployment checklists
- Defining code review criteria
- Any workflow boundary that needs enforcement

## Core Principle

**Wrong:** Vague criteria ("ensure quality", "review code")
**Right:** Explicit criteria with commands and pass/fail definitions

Quality gates must be:
- **Unambiguous** - Clear what passes/fails
- **Executable** - Exact commands provided
- **Categorized** - Must Pass vs Should Review
- **Actionable** - What to do when things fail

## The Process

### Step 1: Identify the Boundary

Determine where the gate belongs:

| Boundary | Purpose | Example Gate |
|----------|---------|--------------|
| Before merge | Code quality | Pre-merge checklist |
| Before deploy | Production readiness | Deploy checklist |
| After design | Implementation readiness | Design review gate |
| After implement | Test readiness | Implementation complete gate |

### Step 2: List All Checks

Brainstorm everything that should be verified:

- Automated checks (tests, linting, type checking)
- Manual reviews (code quality, documentation)
- Cross-functional checks (security, accessibility)
- Process checks (approvals, tickets updated)

### Step 3: Categorize Checks

Separate into two categories:

**Must Pass (Automated)**
- Binary pass/fail
- Can be automated
- Blocking - cannot proceed if fail
- Examples: tests, linting, type checks

**Should Review (Manual)**
- Requires judgment
- Human review needed
- May be non-blocking
- Examples: code quality, documentation completeness

### Step 4: Write Executable Checks

For each check, provide:

```markdown
### [Check Name]

- [ ] **[What to verify]**
  ```bash
  [exact command to run]
  ```
  Expected: [what success looks like]

  If fails: [what to do]
```

Be specific:
- ❌ "Run tests"
- ✅ "Run unit tests: `cargo test --lib` - Expected: All tests pass (0 failures)"

### Step 5: Document Failure Procedures

For automated checks:

```markdown
### If Automated Checks Fail

**STOP. Do not proceed.**

1. Read the error message carefully
2. Check if recent commit caused failure
3. Fix the issue (don't work around)
4. Re-run full check suite
5. If stuck > 30 minutes, ask for help
```

For manual checks:

```markdown
### If Manual Review Has Issues

| Severity | Action |
|----------|--------|
| Blocking | Must fix before proceeding |
| Non-blocking | Create follow-up task |
| Discussion | Flag for team review |
```

### Step 6: Add Prerequisites and Sign-Off

**Prerequisites** - What must be true before starting:
- All changes committed
- Branch up to date
- Feature complete

**Sign-Off** - How to record completion:
- Who verified
- When verified
- Any exceptions granted

### Step 7: Test the Gate

Verify the gate is usable:

- [ ] All commands work as written
- [ ] Pass/fail criteria are clear
- [ ] Time to complete is reasonable
- [ ] Failure procedures are actionable
- [ ] Someone unfamiliar can follow it

### Step 8: Integrate into Workflow

Add gate to workflow documentation:
- Link from relevant workflow stages
- Add to CI/CD if automatable
- Train team on new gate
- Schedule periodic reviews of gate effectiveness

## Checklist

- [ ] Boundary identified
- [ ] All checks listed
- [ ] Checks categorized (Must Pass / Should Review)
- [ ] Commands are exact and runnable
- [ ] Failure procedures documented
- [ ] Prerequisites specified
- [ ] Sign-off section added
- [ ] Gate tested with fresh eyes
- [ ] Integrated into workflow

## Template Structure

```markdown
# [Workflow Stage] Verification Checklist

**Purpose:** [What this validates]
**When:** [At what point]

## Prerequisites
- [ ] [What must be true first]

## Automated Checks (MUST PASS)

### [Category]
- [ ] **[Check]**
  ```bash
  [command]
  ```
  Expected: [success criteria]

## Manual Verification (SHOULD REVIEW)

### [Category]
- [ ] **[Check]** - [Guidance]

## If Checks Fail
[Procedures]

## Sign-Off
| Category | Status | Notes |
|----------|--------|-------|
| Automated | ✅/❌ | |
| Manual | ✅/⚠️ | |
```

**Use template:** `${CLAUDE_PLUGIN_ROOT}templates/verification-checklist-template.md`

## Anti-Patterns

**Don't:**
- Use vague criteria ("ensure quality")
- Skip the failure procedures
- Mix Must Pass with Should Review
- Make gates so long they get skipped
- Forget to test commands work

**Do:**
- Provide exact commands
- Separate blocking from advisory
- Keep gates focused and timely
- Update when processes change
- Automate what can be automated

## Example: Pre-Merge Gate

```markdown
# Pre-Merge Checklist

## Prerequisites
- [ ] All changes committed
- [ ] Branch rebased on main

## Automated Checks (MUST PASS)

### Tests
- [ ] **Unit tests**
  ```bash
  cargo test --lib
  ```
  Expected: 0 failures

- [ ] **Integration tests**
  ```bash
  cargo nextest run
  ```
  Expected: 0 failures

### Static Analysis
- [ ] **Linting**
  ```bash
  cargo clippy -- -D warnings
  ```
  Expected: 0 warnings

## Manual Verification (SHOULD REVIEW)

### Code Quality
- [ ] No magic numbers without explanation
- [ ] Error handling is appropriate
- [ ] Public APIs are documented

## If Automated Checks Fail
STOP. Fix issues. Re-run all checks.
```

## Related Skills

- **Organizing documentation:** `${CLAUDE_PLUGIN_ROOT}skills/organizing-documentation/SKILL.md`
- **Creating research packages:** `${CLAUDE_PLUGIN_ROOT}skills/creating-research-packages/SKILL.md`
- **Documenting debugging workflows:** `${CLAUDE_PLUGIN_ROOT}skills/documenting-debugging-workflows/SKILL.md`

## References

- Standards: `${CLAUDE_PLUGIN_ROOT}standards/documentation-structure.md`
- Template: `${CLAUDE_PLUGIN_ROOT}templates/verification-checklist-template.md`
