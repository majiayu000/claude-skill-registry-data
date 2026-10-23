---
name: executing-plans
description: Executes a written multi-step implementation plan end to end - loads the plan, reviews it critically for gaps, works through each task with its verification steps, and reports when everything is done. This is the execution stage inside the delivery-flow workflow, entered by requests like "implement this plan", "run the plan", "execute the plan", or "work through these tasks" once delivery-flow has produced a written plan. Do not activate directly for a standalone request that has not gone through delivery-flow first.
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks, report when complete.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

**Note:** Execution runs inline in this agent; use an independent reviewer for the review stage when the harness supports it.

## The Process

### Step 1: Load and Review Plan
1. Verify that the current workspace is appropriate for the task; do not create or switch worktrees unless the user asks
2. Read plan file
3. Review critically - identify any questions or concerns about the plan
4. If concerns: Raise them with your human partner before starting
5. If no concerns: Create todos for the plan items and proceed

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run the verification the plan names for that task (a build, test, or lint command, or a manual check) and confirm it passes before moving on
4. Mark as completed

### Step 3: Complete Development

After all tasks complete and verified:
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use `finishing-a-development-branch` only when the user authorized an integration action; otherwise return to `delivery-flow` for a PR-ready handoff
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
- Reference skills when plan says to
- Never start implementation on main/master branch without explicit user consent
