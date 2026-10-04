---
name: dogfood
description: |
  Test Prismstack by running a real domain through the full flow (plan → build → check).
  Records issues found for fixing. The ultimate integration test.
  Trigger: "dogfood", "test with real domain", "integration test", "try it for real"
  Do NOT use when: just want to run install tests (use `bash test/install-test.sh`)
user_invocable: true
---
<!-- Internal maintenance skill — edit this file directly -->

# /dogfood: Integration Test With a Real Domain

You are a QA tester dogfooding Prismstack. You run a real domain through the full product flow and record every issue you find.

## Phase 0: Pick a Test Domain

Parse `$ARGUMENTS` for a domain name. If not provided, suggest:

- **小型咖啡店行銷** (small coffee shop marketing) — simple, ~10 skills, fast
- **獨立遊戲開發工作流** (indie game dev workflow) — medium complexity
- **自由接案者專案管理** (freelancer project management) — diverse skill types

Ask the user to pick one or provide their own domain.

Create a temp working directory:

```bash
_DOGFOOD_DIR=$(mktemp -d)/dogfood-test
mkdir -p "$_DOGFOOD_DIR"
echo "Working in: $_DOGFOOD_DIR"
```

## Phase 1: Run /domain-plan

Read `skills/domain-plan/SKILL.md` and follow its flow for the test domain.

Execute the planning phase as if you were a real user. Record:

- **Did it work?** Did the skill produce a complete domain plan?
- **Awkward moments**: Any point where the flow was confusing or required backtracking?
- **Errors**: Any crashes, missing files, or broken references?
- **Timing**: Roughly how many tool calls / how long did the phase take?
- **Output quality**: Is the generated plan actually useful for the domain?

Save the plan output to `$_DOGFOOD_DIR/domain-plan-output/`.

## Phase 2: Run /domain-build

Read `skills/domain-build/SKILL.md` and follow its flow using the plan from Phase 1.

Build the domain stack in `$_DOGFOOD_DIR/generated-stack/`.

Record the same categories as Phase 1, plus:

- **Skill count**: Did it generate the expected number of skills?
- **Skill structure**: Do generated skills follow skill-craft-guide structure?
- **Shared resources**: Were methodology files and shared context created?
- **Completeness**: Can each generated skill actually be invoked?

## Phase 3: Run /skill-check on the Generated Stack

Read `skills/skill-check/SKILL.md` and run it with `--all` on the generated domain stack.

Record:

- **Scores**: What did each generated skill score?
- **Common issues**: What patterns appear across multiple skills?
- **Fix loop**: Did the fix loop workflow work? Could issues be resolved?
- **Rubric coverage**: Were all 15 dimensions actually scored?

## Phase 4: Issue Report

Compile all recorded issues into a structured report:

```markdown
# Dogfood Report: [domain name]
Date: YYYY-MM-DD
Prismstack version: <from VERSION>

## Summary
- Domain: [name]
- Skills generated: N
- Average quality score: X.XX / 5.00
- Issues found: N (C critical, I important, M minor)

## Issues

### Issue 1: [title]
- **Phase**: plan / build / check
- **Severity**: critical / important / minor
- **What happened**: description
- **Expected**: what should have happened
- **Root cause**: which Prismstack skill or methodology caused it
- **Suggested fix**: use /skill-dev on X, or edit methodology Y

### Issue 2: ...
```

Save the report to `.claude/skills/dogfood/last-dogfood-report.md`.

## Cleanup

Ask the user:
- **Keep** the generated stack in `$_DOGFOOD_DIR` for manual inspection?
- **Delete** it to save space?

Act on their choice.

## Output

Present:
1. **Pass/Fail**: Did the full flow complete without critical errors?
2. **Score Summary**: Average quality of generated skills
3. **Top Issues**: The 3 most impactful issues found
4. **Next Steps**: Which maintenance skill to run for each fix (/skill-dev, /self-check, /methodology-sync)
