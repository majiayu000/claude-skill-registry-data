---
name: superpowers-en
description: Software development methodology workflow assistant (Superpowers). Trigger when users mention "brainstorming", "requirements clarification", "design spec", "writing plans", "implementation plan", "TDD", "test-driven development", "red-green-refactor", "systematic debugging", "root cause analysis", "code review", "subagent", "parallel agents", "git worktree", "finishing a branch", "merge/PR", "verification", "writing skills", "development workflow", "engineering discipline", "YAGNI", "DRY". Provides end-to-end engineering discipline from brainstorming to planning, TDD implementation, review, and delivery.
license: MIT
packageType: instruction-skill
instructionOnly: true
---

# Software Development Methodology Workflow Assistant (Superpowers)

## Prerequisites

This Skill is a pure instruction type. It does not depend on external APIs, MCP servers, or CLI tools. It is a **complete software development methodology** for coding agents whose core value is **process discipline**: clarify before coding, test before implementing, find the root cause before debugging, and gather evidence before claiming completion.

> Priority iron law: **user's explicit instructions > this methodology's skills > default system behavior**. User instructions say WHAT, not "skip the process"; but if the user explicitly asks to skip a process (e.g., "don't use TDD"), follow the user — the user is always in control.
>
> Skills come in two types: **rigid** (TDD, systematic debugging — follow exactly, don't adapt the discipline away) and **flexible** (patterns — adapt the principles to context).

## Core Capabilities

### I. Skill System Principles

**User triggers**: at the start of any development task

**Points**:
1. Before acting, judge whether any skill applies — even a 1% chance means check first (a clarifying question is a task too; check before asking)
2. When adopting a skill, announce "Using [skill] to [purpose]"
3. For skills with a checklist, create a TodoWrite task per item and complete them in order
4. Recognize red-flag thoughts ("this is too simple", "skip just this once"); see references/workflow-details.md section 9

### II. Brainstorming and Design Clarification

**User triggers**: "I want to build…", "Add a feature", "Design this"

**Hard gate**: do not write code, scaffold, or invoke implementation skills until you present a design and the user approves it. Every project goes through this, including "simple" ones.

**Flow**: explore context → (offer visual companion as its own message for visual topics) → ask clarifying questions one at a time → propose 2-3 approaches + recommendation → present design in sections with per-section approval → write design doc → spec self-review → user reviews → transition to writing plans.

### III. Writing Implementation Plans

**User triggers**: "Write an implementation plan", "Break the spec into tasks"

**Flow**: plan the file structure first (single responsibility); break work into 2-5 minute tasks, each with exact file paths, complete code, verification steps; apply DRY/YAGNI/TDD/frequent commits. Multi-subsystem specs must be split into independent sub-project plans.

### IV. Executing Plans

**User triggers**: "Execute the plan", "Start implementing"

**Flow**: batch execution with checkpoints; confirm at human checkpoints after each batch; follow the plan strictly, stop on deviation.

### V. Subagent-Driven Development

**User triggers**: "Develop with subagents", "Dispatch agents per task"

**Flow**: dispatch a fresh subagent per task with two-stage review — spec compliance first, then code quality; advance only on pass.

### VI. Dispatching Parallel Agents

**User triggers**: "Process in parallel", "Run multiple tasks at once"

**Points**: for 2+ independent tasks with no shared state or sequential dependency, dispatch subagents in parallel; run serially when there are dependencies or shared state.

### VII. Git Worktree Isolated Workspace

**User triggers**: "Isolate the work", "Set up a worktree"

**Flow**: before feature work needing isolation or executing a plan, create an isolated workspace via native tools or git worktree, run project setup, verify a clean test baseline.

### VIII. Test-Driven Development (TDD)

**User triggers**: before implementing any feature or bugfix

**Iron law**: no production code without a failing test first. Red-Green-Refactor: write failing test → watch it fail → write minimal code to pass → watch it pass → commit. Code written before tests gets deleted and redone. Details in references/workflow-details.md section 1.

### IX. Systematic Debugging

**User triggers**: on any bug, test failure, or unexpected behavior

**Iron law**: no fixes without root cause investigation first. Four phases: root cause investigation → hypothesis and verification → minimal fix → verification. Symptom fixes are failure. Details in section 2.

### X. Verification Before Completion

**User triggers**: before claiming "complete/fixed/passing", committing, or opening a PR

**Principle**: evidence before assertions. Actually run verification commands and confirm pristine output before any success claim. Never say "should be fine" without evidence. Checklist in section 6.

### XI. Requesting Code Review

**User triggers**: on completing tasks, major features, or before merging

**Flow**: review against the plan, report issues by severity (Critical/Major/Minor); Critical blocks progress.

### XII. Receiving Code Review

**User triggers**: on receiving review feedback, before implementing changes

**Principle**: respond with technical rigor, no performative agreement and no blind implementation; verify before implementing when feedback is unclear or questionable.

### XIII. Finishing a Development Branch

**User triggers**: after implementation is complete and tests pass

**Flow**: present structured options — merge / open PR / keep branch / discard; after confirmation clean up the worktree; don't decide the merge strategy unilaterally.

### XIV. Writing Skills (Meta-Skill)

**User triggers**: "Write a skill", "Improve a skill"

**Flow**: create/edit skills following best practices, with precise triggering descriptions and tone matched to the skill type; test with subagents before deployment to verify triggering and execution.

## Execution Priority (Strict Constraints)

1. **User Instructions First**: user's explicit instructions outrank all skill discipline.
2. **Gates Are Non-Skippable**: design approval, test-fails-first, root-cause-before-fix, verify-before-completion — these gates are not waived for being "simple" or "in a hurry".
3. **No Slack on Rigid Skills**: TDD and systematic debugging are followed exactly; violating the letter violates the spirit.
4. **Evidence Over Claims**: any "complete/passing" claim must be backed by real run output.
5. **YAGNI / DRY / TDD Throughout**: build only what's needed now, remove duplication, test first.
6. **Announce and Track**: announce when adopting a skill; create tasks per checklist item and complete them in order.

## Reference Templates

Discipline details, gates, and red-flag tables for each workflow are in `references/workflow-details.md`, covering the TDD red-green-refactor cycle, the 4-phase systematic debugging process, the brainstorming checklist, code-review severity levels, the verification checklist, and the red-flag/rationalization table. Refer to the matching section when running a workflow.

## Communication Rules

- Respond in English by default.
- When adopting a skill, first announce "Using [skill] to [purpose]".
- For workflows with a checklist, create tasks per item and complete in order.
- Lead with the workflow conclusion, then expand into detail.
- Follow each gate strictly; do not skip steps.

## Common Pitfalls

1. "This is too simple to need a design/test" — simple projects are exactly where unexamined assumptions cause the most rework.
2. "I'll test after" — tests written after pass immediately and prove nothing.
3. "Just patch this one place" — symptom fixes mask the root cause and create new bugs.
4. "Should be fixed" — no verification run means no completion claim.
5. "Deleting hours of work is wasteful" — sunk cost fallacy; keeping untrusted code is technical debt.
6. "TDD is dogmatic, I'm being pragmatic" — TDD IS pragmatic; test-first beats debugging after.
7. Treating the user's "what" as permission to skip the process — don't skip workflows unless the user says so.
8. When skill discipline conflicts with explicit user instructions — follow the user; the user is always in control.
