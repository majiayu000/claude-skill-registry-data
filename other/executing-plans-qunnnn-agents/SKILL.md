---
name: executing-plans
description: Use when you have a written implementation plan to execute with review checkpoints
tags: [meta, workflow, execution]
applies-to: [antigravity, cursor, copilot, gemini]
level: project
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks, report when complete.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

## The Process

### Step 1: Load and Review Plan
1. Read plan file
2. Review critically — identify any questions or concerns about the plan
3. If concerns: Raise them with your human partner before starting
4. If no concerns: Create task list and proceed

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

### Flutter Verification Steps
After completing code changes, always run:

```bash
# Generate code if freezed/json_serializable/retrofit models were changed
dart run build_runner build --delete-conflicting-outputs

# Static analysis
flutter analyze

# Run tests
flutter test

# Verify no import issues
dart fix --dry-run
```

### Step 3: Complete Development

After all tasks complete and verified:
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use finishing-a-development-branch
- Follow that skill to verify tests, present options, execute choice

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly
- `build_runner` generates errors that indicate model inconsistencies
- `flutter analyze` reports errors (warnings can be noted and continued)

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** — stop and ask.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Stop when blocked, don't guess
- Never start implementation on main/master branch without explicit user consent
- Always run `build_runner` after modifying generated code models
- Always run `flutter analyze` before claiming completion

## Integration

**Required workflow skills:**
- **writing-plans** — Creates the plan this skill executes
- **finishing-a-development-branch** — Complete development after all tasks
- **verification-before-completion** — Verify before claiming done
