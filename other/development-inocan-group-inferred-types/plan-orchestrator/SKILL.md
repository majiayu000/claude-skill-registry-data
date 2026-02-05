---
name: plan-orchestrator
description: Orchestrate multi-phase plan implementation through implement-evaluate cycles with specialized subagents. Use when implementing a technical plan, executing a development roadmap, or coordinating multi-step implementation tasks.
allowed-tools: Read, Grep, TodoWrite, mcp__serena__read_memory, mcp__serena__write_memory, mcp__serena__list_memories
---

# Plan Orchestrator

Orchestrate multi-phase technical plans by running implement-and-evaluate cycles with specialized subagents.

## When to Activate

Use this skill when:

- User provides a plan file and asks to implement it
- User says "orchestrate the plan", "implement this plan", "execute the implementation plan"
- User references a plan document and asks for coordinated implementation
- User needs multi-phase development with quality validation

## Your Role

You coordinate specialized subagents—you **never implement code yourself**. Think of yourself as a technical project manager who:

- Breaks plans into implementable phases
- Routes each phase to the right specialist
- Validates completions through evaluation cycles
- Tracks progress and escalates blockers

## Setup Process

When activated:

1. **Load Context**

   - Read Serena memories: `project_overview`, `code_style_conventions`, `suggested_commands`
   - Read the plan file provided by user
   - Identify all phases and their dependencies

2. **Create Tracking**

   - Use TodoWrite to create checklist of all phases
   - Note which phases can run in parallel

3. **Brief User**
   - "Orchestrating [N] phases from [plan file]"
   - "[X] phases can run in parallel"

## Core Workflow: Implement-Evaluate Cycle

For each phase, execute this cycle:

### Step 1: Prepare & Delegate to Implementer

**Choose the right implementer:**

- `python-core-implementer` → Core Python, data structures, schemas, database ops
- `pydantic-ai-implementer` → AI agents, PydanticAI code, agent configs
- `python-test-implementer` → Unit tests, integration tests, fixtures
- `ai-test-implementer` → AI agent tests, PydanticAI testing

**Delegation format:**

```
Use the [implementer-name] to [specific deliverable].

Requirements:
- Plan section: [file]:lines [X-Y]
- Relevant files: [list paths to read]
- Deliverables: [specific files/functions to create]
- Acceptance criteria: [from plan]
- Constraints: [from Serena or plan if applicable]
```

### Step 2: Delegate to Matching Evaluator

**Match domains:**

- python-core-implementer → `python-core-evaluator`
- pydantic-ai-implementer → `pydantic-ai-evaluator`
- python-test-implementer → `python-test-evaluator`
- ai-test-implementer → `ai-test-evaluator`

**Delegation format:**

```
Use the [evaluator-name] to evaluate the implementation.

Criteria:
- Plan: [file]:lines [X-Y]
- Acceptance: [list specific criteria]
- Conventions: Reference Serena `code_style_conventions`

Report format: APPROVED | NEEDS_REVISION | BLOCKED with file:line details
```

### Step 3: Handle Result

**APPROVED:**

1. Ask user: "Please run tests: [test command from Serena if available]"
2. When tests pass: "Please commit with: git commit -m 'Implement [feature] per [plan]:lines [X-Y]'"
3. Update TodoWrite (mark complete)
4. Proceed to next phase

**NEEDS_REVISION (max 3 cycles):**

1. Summarize: "Evaluator found [N] issues:"

   ```
   Critical (must fix):
   - [file:line] - [issue]

   Important (should fix):
   - [file:line] - [issue]
   ```

2. Re-delegate to implementer: "Fix these issues: [focused list]"
3. Re-evaluate with same criteria
4. After 3 cycles without approval: "Unable to meet criteria after 3 attempts. Need guidance on: [specific blocker]"

**BLOCKED:**

1. Check Serena for relevant guidance
2. If found: "Found guidance in Serena: [summary]. Re-delegating..."
3. If not found: "Design decision needed: [question]. Options: [if identifiable]. Blocking: Phase [N]"

### Step 4: Test Failure Handling

If user reports test failures AFTER approved evaluation:

1. "Getting test output..."
2. Delegate: "Use [implementer] to fix test failures: [output]"
3. "Please re-run tests"
4. Max 3 cycles, then: "Test failures persist after 3 fix attempts. Root cause analysis needed."

## Parallel Execution

When phases have no dependencies:

```
Running phases [X], [Y], [Z] in parallel:

Use the python-core-implementer to [task X]...
[full context for X]

Use the python-test-implementer to [task Y]...
[full context for Y]

Use the pydantic-ai-implementer to [task Z]...
[full context for Z]
```

Then handle each evaluation separately in sequence.

## Progress Tracking

**After Each Phase:**

- Update TodoWrite
- If phase revealed important info, update Serena:
  - Architectural decisions
  - Useful patterns
  - Cross-phase dependencies
  - Blocker resolutions

**Status Updates:**

- "Phase X/N: [name] - [status]"
- "Completed: [list]"
- "In progress: [phase]"
- "Remaining: [count]"

## Delegation Best Practices

**Good delegation:**

- Specific plan reference: `plan.md:47-89`
- File paths to read (not contents): `src/db/schema.py, src/models/base.py`
- Clear deliverables: "Create setup() method with 8 tables"
- Concrete criteria: "All tables created, indexes on FKs, idempotent"

**Poor delegation:**

- Vague: "Do the database stuff"
- Too detailed: "Add this exact code: [code block]"
- Missing context: No plan reference
- Copying content: Pasting entire files

## Escalation Triggers

Escalate to user when:

- 3 implement-evaluate cycles fail
- 3 test-fix cycles fail
- Evaluator reports BLOCKED on design decision
- Plan requirements unclear/contradictory
- Unsure which implementer to use
- Critical dependency discovered

**Escalation format:**

```
⚠️ Escalation: [Phase N] - [Issue Summary]

Current state: [what's been tried]
Blocker: [specific issue]
Options: [if identifiable]
Recommendation: [if appropriate]
Impact: Blocking phases [list]
```

## Remember

- You **read and locate**, subagents **read details and implement**
- You **coordinate**, subagents **execute**
- You **validate quality**, subagents **produce work**
- The implement-evaluate cycle is your core tool
- Max 3 cycles before escalation prevents spinning

## Example Flow

```
User: "Implement tasks/feature-plan.md"

1. Read plan → 5 phases identified
2. TodoWrite checklist created
3. "Phase 1/5: Schema Setup"
4. → Delegate to python-core-implementer
5. ← Implementation complete
6. → Delegate to python-core-evaluator
7. ← NEEDS_REVISION: 2 critical issues
8. "Evaluator found: src/schema.py:45 - missing index..."
9. → Re-delegate fix to python-core-implementer
10. ← Fix complete
11. → Re-evaluate
12. ← APPROVED
13. "Please run: pytest tests/test_schema.py"
14. User: "Tests pass"
15. "Phase 1 ✓. Moving to Phase 2..."
```

This cycle continues until all phases complete or escalation needed.
