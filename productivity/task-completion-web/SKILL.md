---
name: task-completion-web
description: >
  Task lifecycle protocol for web-research swarm subagents. Extends the
  base task-completion protocol with a mandatory self-assessment checklist
  for source verification and coverage.
---

# Task Completion Skill (Web Research)

## Task Lifecycle

Tasks are automatically assigned to you by the framework — you do not
need to claim them manually.

1. **Execute the task** — follow your domain skill's workflow to
   complete the work.
2. **Post results** — post your findings to the appropriate BBS channel.
3. **Complete the task** — use `complete_task` with a summary of what
   you accomplished.

## Rules

- Focus on YOUR assigned task — don't try to do everything.
- You CANNOT create tasks for other agents. Only execute tasks assigned
  by the orchestrator.
- Always post or share results before calling `complete_task`.
- If a task fails or you cannot complete it, still call `complete_task`
  with an explanation of what went wrong.

## Completion Self-Assessment (MANDATORY)

Before calling `complete_task`, run through this checklist:

1. **Coverage**: Did I address every dimension of the assigned task?
2. **Verification**: Did I cross-verify key facts from 2+ independent sources?
3. **Precision**: Am I using exact values, names, and terms from sources
   (not paraphrased or approximated)?
4. **Conflicts**: Did I identify and flag any conflicting information?
5. **Sources**: Did I include URLs for every factual claim?

**If any item fails, do more work before completing.** Do not call
`complete_task` until you have genuinely exhausted your ability to
improve the answer. Default to doing MORE work, not less.
