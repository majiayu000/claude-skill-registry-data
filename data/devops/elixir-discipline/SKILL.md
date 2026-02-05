---
name: elixir-discipline
description: MANDATORY pre-check before ANY response - ensures you use applicable skills and follow best practices. Use this skill FIRST before responding to any Elixir/Phoenix request.
---

# Elixir Discipline: Mandatory Skill Enforcement

## ABSOLUTE REQUIREMENT

Before you respond to ANY request about Elixir/Phoenix code, you MUST complete this checklist.

This is NOT optional. This is NOT negotiable. You CANNOT rationalize your way out of this.

## PRE-RESPONSE CHECKLIST

**STOP. Before typing ANY response, ask yourself:**

1. **Is this about implementing a feature or fixing a bug?**
   → USE `elixir-tdd-enforcement` skill FIRST
   → NO CODE without failing test first

2. **Is this about debugging an error or issue?**
   → USE `elixir-root-cause-only` skill
   → NO quick fixes, trace to root cause first

3. **Did I claim something works?**
   → USE `elixir-verification-gate` skill
   → Run the actual command, read actual output

4. **Am I about to modify an ignore file (dialyzer.ignore, .credo.exs exclude)?**
   → STOP IMMEDIATELY
   → USE `elixir-no-shortcuts` skill
   → Fix the real problem

5. **Am I creating placeholder code or default values for required data?**
   → STOP IMMEDIATELY
   → USE `elixir-no-placeholders` skill
   → Fail loud, fail fast, no silent failures

6. **Am I proposing to "just try" something?**
   → STOP
   → Use systematic debugging instead

## IF A SKILL APPLIES, YOU MUST USE IT

**This means:**
- Announce which skill you're using
- Follow it EXACTLY
- Do not skip steps
- Do not modify the process

**IF YOU SKIP A SKILL WHEN IT APPLIES = TASK FAILURE**

## RATIONALIZATIONS THAT ARE WRONG

### "This is just a simple question"
WRONG. Check the skills list anyway.

### "I remember this skill, I don't need to read it"
WRONG. Read it every time. The details matter.

### "The skill probably doesn't apply here"
WRONG. If there's even a 1% chance it applies, you MUST read it.

### "I'll just do this quickly"
WRONG. Quick usually means wrong. Use the appropriate skill.

### "The user just wants a simple answer"
WRONG. The user wants a CORRECT answer. Use skills to ensure correctness.

### "This would take too long"
WRONG. Doing it wrong takes longer. Use the skills.

## ENFORCEMENT

**Every response about Elixir/Phoenix code MUST start with:**

```
[Checking applicable skills...]
- elixir-tdd-enforcement: [YES/NO - reason]
- elixir-root-cause-only: [YES/NO - reason]
- elixir-verification-gate: [YES/NO - reason]
- elixir-no-shortcuts: [YES/NO - reason]
- elixir-no-placeholders: [YES/NO - reason]

[Using skill: SKILL_NAME]
```

**If you respond WITHOUT this checklist = automatic failure.**

## SKILL DESCRIPTIONS

**elixir-tdd-enforcement**
- When: Implementing ANY feature or bugfix
- Enforces: Test first, watch it fail, then implement
- Prevents: Code without tests, untested changes

**elixir-root-cause-only**
- When: Debugging ANY error or issue
- Enforces: Trace to root cause before proposing fixes
- Prevents: Symptom fixes, random changes

**elixir-verification-gate**
- When: Claiming ANYTHING works (tests pass, build succeeds, etc.)
- Enforces: Run actual command, read actual output
- Prevents: Assumptions, "should work", premature completion

**elixir-no-shortcuts**
- When: About to modify ignore files or suppress warnings
- Enforces: Fix the real problem
- Prevents: Technical debt accumulation

**elixir-no-placeholders**
- When: Creating ANY code or data structures
- Enforces: No placeholder code, no defaults for required data, fail loud
- Prevents: Silent failures, debugging nightmares, masked bugs

## CONSEQUENCES OF SKIPPING SKILLS

**If you skip applicable skills:**
1. Code will be wrong
2. Tests won't actually verify behavior
3. Bugs won't actually be fixed
4. Technical debt will accumulate
5. The user will have to redo the work

**The time "saved" by skipping skills is lost 10x over in debugging.**

## REMEMBER

> "If a skill for your task exists, you must use it or you will fail at your task."

This is not about preference. This is about producing correct, maintainable Elixir code.

## THE RULE

**IF EVEN 1% CHANCE A SKILL APPLIES → YOU ABSOLUTELY MUST USE IT**

No exceptions. No special cases. No "just this once."
