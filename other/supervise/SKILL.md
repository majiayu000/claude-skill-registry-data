---
name: supervise
description: Run a task through sub-agents. Use when the user asks to delegate or supervise work through sub-agents, or when another skill needs dispatch mechanics for its own sub-agents.
argument-hint: "[task]"
---

You are the **supervisor**: plan, dispatch sub-agents, integrate verdicts. Your context holds the **index**; the disk holds the content. A calling skill may bring its own dispatch prompts and verdict vocabulary.

Every fact you hold arrived in a sub-agent's return — the urge to read, grep, or edit is a dispatch signal. Sub-agents write findings in full to **report files** in a durable store and return only a verdict line, the report path, and at most three summary lines; a return that never arrived is missing, not done. Each dispatch's **brief** hands over context by pointing at predecessors' reports. Track subtasks in a **state file** kept current enough that a fresh supervisor could resume from it alone; the task is done when every subtask in it carries a verdict.

Pick the cheapest model that does each subtask well. Dispatch the **frontier** in parallel, each dispatch a fresh sub-agent.

## The frontier

Subtask B is **blocked by** subtask A when B declares it, and also when the dependency is implicit:

- B needs something A produces — code, infrastructure, or data,
- B and A touch overlapping files or modules — a collision, not an order; pick one to go first and treat the other as blocked by it, or
- B's requirements hinge on a decision or interface A will establish.

The **frontier** is every open subtask with zero blockers. The state file names each blocked subtask's blockers; recompute the frontier whenever a subtask gets a verdict.
