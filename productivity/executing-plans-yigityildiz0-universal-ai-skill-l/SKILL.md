---
name: executing-plans
description: "Use when you have a written implementation plan to execute in a separate session with review checkpoints. Turkish triggers: hazır planı uygula, adım adım yürüt, kontrol noktalarıyla tamamla."
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks, report when complete.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

If subagent support is available and current user or project rules permit delegation, prefer the installed `subagent-driven-development` skill. Otherwise execute this workflow in the current session; lack of subagents is not itself a blocker.

## The Process

### Step 1: Load and Review Plan
1. Read plan file
2. Review critically - identify any questions or concerns about the plan
3. If concerns: Raise them with your human partner before starting
4. If no concerns: create or update a visible task plan with the current host's planning mechanism, then proceed

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

### Step 3: Complete Development

After all tasks complete and verified:
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use the installed `finishing-a-development-branch` skill
- Follow that skill to verify tests, present options, execute choice

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Stop when blocked, don't guess
- Never start implementation on main/master branch without explicit user consent

## Integration

**Required workflow skills:**
- **using-git-worktrees** - Ensures an isolated workspace when one is needed
- **writing-plans** - Creates the plan this skill executes
- **finishing-a-development-branch** - Completes development after all tasks
