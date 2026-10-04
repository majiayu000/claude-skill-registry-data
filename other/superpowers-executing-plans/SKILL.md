---
name: superpowers-executing-plans
description: 'Use when executing a written implementation plan in the current session
  — load the plan, execute tasks in sequence with verification checkpoints, handle
  waves of concurrent tasks, and integrate with the ship pipeline to finish. Purpose:
  Translate a written plan into verified code by following each step exactly, running
  specified verifications after each task, stopping on blockers, and surfacing concerns
  before forcing through. Key capabilities: Pre-execution critical review of the plan
  with flag-and-ask workflow; TodoWrite tracking with in_progress/completed states
  per task; wave execution model for grouped tasks (complete a wave before starting
  the next); stop-and-ask guardrails for blockers, missing dependencies, unclear instructions,
  or repeated verification failures; mandatory integration with finishing-a-development-branch
  at the end. When to trigger: running a multi-step plan from a design document; executing
  a phased checklist from a task manager; following a step-by-step setup or onboarding
  guide; carrying out retro action items; implementing a feature from a written spec
  with sequenced tasks; executing a deployment checklist with verification gates between
  steps. Also for: single-feature branch lifecycles; hotfix execution from an incident
  report plan; experiment landing from a spike doc.'
---

# Executing Plans Skill

**Purpose:** Execute a written implementation plan in the current session with review checkpoints.

## Step 1: Load and Review Plan

1. Read the plan file
2. Review critically and flag any questions or concerns
3. Raise concerns with your human partner before proceeding
4. If clear, create a TodoWrite and move forward

## Step 2: Execute Tasks

For each task in sequence:
1. Mark as `in_progress`
2. Follow each step exactly
3. Run the specified verifications
4. Mark as `completed`

### Wave Execution
If tasks are grouped into waves in the plan:
- Execute all Wave 1 tasks before Wave 2
- Tasks within a wave can run concurrently if they are truly independent
- Always complete a full wave before starting the next
1. Mark as `in_progress`
2. Follow each step exactly
3. Run the specified verifications
4. Mark as `completed`

## Step 3: Complete Development

- Announce use of the `finishing-a-development-branch` skill
- **Required:** Follow `superpowers-finishing-a-development-branch` to verify tests and present/execute options

## Guardrails

**Stop immediately and ask for help when:**
- Hitting a blocker (missing dependency, test failure, unclear instruction)
- The plan has critical gaps preventing progress
- Verification fails repeatedly

**Return to Step 1 review when:**
- Your partner updates the plan based on your feedback
- The fundamental approach needs rethinking

**Never** force through blockers — ask for clarification instead.

## Integration

- **Required sub-skill:** `superpowers-finishing-a-development-branch` — completes development
- **Prerequisite:** written plan from `superpowers-writing-plans`
- **Note:** Quality improves significantly when run on platforms with subagent support
