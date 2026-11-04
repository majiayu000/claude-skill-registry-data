---
name: structured-brainstorming
description: "Structured design process before new features, enhancements, or architectural changes. Brainstorming + plan creation + approval flow."
---

# Structured Brainstorming + Plan Creation

## Overview

Turn ideas into mature designs and actionable plans. First understand context, then ask questions one by one, build the design, get approval, write the plan.

**Core principle:** Do NOT start implementation without approval. Every project goes through this process.

<HARD-GATE>
Until the design is presented and the user gives approval:
- Do NOT write code
- Do NOT create files
- Do NOT call implementation skills
- Do NOT scaffold anything
- Do NOT make changes via exec

This rule applies to EVERYTHING, including projects that seem simple.
</HARD-GATE>

## Anti-Pattern: "This Is Too Simple for Design"

Every project goes through this process. A config change, a single function, a simple addition -- all of them. "Simple" projects are where unexamined assumptions cause the most damage. The design can be short (a few sentences), but you MUST present it and you MUST get approval.

## Checklist

Complete these steps IN ORDER:

1. **Explore project context** -- examine existing files, docs, recent changes
2. **Ask clarifying questions** -- one at a time; understand goals, constraints, success criteria
3. **Propose 2-3 approaches** -- with tradeoffs, including your recommendation
4. **Present the design** -- in sections scaled to complexity, get approval after each section
5. **Write the design document** -- save as `docs/plans/YYYY-MM-DD-<topic>-design.md`
6. **Move to execution** -- create a plan file, hand off to `subagent-execution` skill

## Process Flow

```
Explore project context
        |
        v
Ask clarifying questions (one at a time)
        |
        v
Propose 2-3 approaches (tradeoffs + recommendation)
        |
        v
Present design sections
        |
        v
 User approved?
  NO  --> Revise design --> present again
  YES --> continue
        |
        v
Write design document
        |
        v
Create plan file (bite-size tasks)
        |
        v
Hand off to subagent-execution
```

**Terminal state: creating the plan file and handing off to subagent-execution.** Do not call any other implementation skill.

## Process Details

### 1. Understanding the Idea
- First check the current project state (files, docs, recent commits)
- Ask questions one at a time -- one question per message
- Prefer multiple-choice questions when possible, but open-ended is fine
- Focus: goals, constraints, success criteria

### 2. Exploring Approaches
- Propose 2-3 different approaches, each with tradeoffs
- Lead with your recommendation and explain why
- Present in a conversational tone

### 3. Presenting the Design
- Present the design when you believe it is ready to build
- Scale each section to complexity: a few sentences if simple, 200-300 words if nuanced
- After each section, ask "does this look right so far?"
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something is unclear

### 4. Design Document
- Save the validated design as `docs/plans/YYYY-MM-DD-<topic>-design.md`
- Keep it short, clear, actionable

### 5. Plan File Creation (Bite-Size Tasks)

**Every task must be independently executable, assuming zero context:**

```markdown
## Task N: [Component Name]

**Files:**
- Create: `full/path/to/file.ts`
- Modify: `full/path/to/existing.ts:123-145`
- Test: `tests/full/path/to/test.ts`

**Step 1: Write a failing test**
[Full test code -- not "add validation", write the code]

**Step 2: Verify the test fails**
Run: `npm test tests/path/to/test.ts`
Expected: FAIL -- "function is not defined"

**Step 3: Write minimal implementation**
[Full implementation code]

**Step 4: Verify the test passes**
Run: `npm test tests/path/to/test.ts`
Expected: PASS

**Step 5: Commit**
`git add ... && git commit -m "feat: ..."`
```

**Rules:**
- Always use full file paths
- Full code in the plan (not just "add this")
- Full commands with expected output
- DRY, YAGNI, TDD, frequent commits
- YAGNI pruning: if you spot unnecessary features, remove them from the design

### 6. Execution Handoff

When the plan is complete:
- **REQUIRED SKILL:** Hand off to `subagent-execution`
- Fresh session per task, two-stage review

## Core Principles

- **One question at a time** -- do not overwhelm with multiple questions
- **Prefer multiple-choice** -- easier to answer than open-ended
- **YAGNI ruthlessly** -- remove unnecessary features from the design
- **Explore alternatives** -- always present 2-3 approaches before deciding
- **Incremental validation** -- present, get approval, proceed
- **Stay flexible** -- if something is unclear, go back and clarify

## Platform Adaptation

This skill uses generic tool references. Adapt to your platform:

- **File operations:** Use your framework's read/write/edit tools
- **Subagent spawning:** Replace `[spawn subagent]` with your platform's mechanism
- **Task tracking:** Use your framework's task management or a markdown file
- **Search:** Use your platform's file search and content search tools

## Red Flags -- STOP

If you catch yourself thinking:
- "Too simple, no design needed" --> SIMPLE = MOST ASSUMPTIONS
- "Let me code first, I will get approval later" --> HARD-GATE VIOLATION
- "I will ask all questions at once" --> ONE QUESTION, ONE MESSAGE
- "One approach is enough" --> AT LEAST 2 ALTERNATIVES
- "I did the design in my head" --> WRITTEN DESIGN + APPROVAL REQUIRED
- "User was in a hurry, I skipped" --> Hurry = MISTAKES, process = SPEED
