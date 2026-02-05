---
name: workflow-design
description: Design, discover, and refactor multi-command workflows for Claude Code
---

# Workflow Design

## Purpose

Help define multi-command workflows that guide users through complex processes. Workflows are sequences of commands that accomplish a larger goal, with each command representing a discrete phase.

## Core Concepts

### What is a Workflow?

**Workflow:** A documented sequence of commands that accomplish a goal.

**Components:**
- Workflow document (narrative + metadata)
- Individual command files (phases)
- Command-workflow links (metadata in commands)

**Not a workflow:**
- Single command
- Ad-hoc command sequences
- Unrelated commands

### Workflow vs Command

**Command:** Single discrete action
- Example: `/plan-chat`, `/plan-breakdown`, `/work`

**Workflow:** Sequence of commands with shared goal
- Example: `epic-development` workflow uses `/plan-chat` → `/plan-breakdown` → `/plan-create` → `/work`

### Good Workflow Candidates

✅ **Multi-step processes with clear phases**
- Epic planning → breakdown → implementation
- Setup → configure → verify
- Analyze → refactor → test

✅ **Processes users repeat**
- Every new feature follows same flow
- Every refactor needs same steps
- Every deployment has same gates

✅ **Processes with decision points**
- Interactive phases where context matters
- Branching based on project type
- Optional phases based on needs

❌ **Bad workflow candidates:**
- Single-step operations
- Rarely-used sequences
- Completely linear with no decisions

## Three Modes

### 1. Discovery Mode - Analyze Existing Commands

**When:** You have related commands, need to identify the workflow

**Process:**
1. List related commands
2. Identify natural sequence
3. Find phase boundaries
4. Determine dependencies
5. Spot decision points
6. Generate workflow doc

**Example:**
```
Input: /plan-chat, /plan-breakdown, /plan-create, /work commands
Output: epic-development workflow document
```

### 2. Design Mode - Create New Workflow

**When:** Designing a new multi-step process from scratch

**Process:**
1. Understand the goal
2. Break into logical phases
3. Identify phase outputs and dependencies
4. Determine interactive vs automated phases
5. Create workflow doc
6. Scaffold command stubs

**Example:**
```
Input: "Need workflow for database migration"
Output: migration-workflow.md + command stubs
```

### 3. Refactor Mode - Improve Existing Workflow

**When:** Workflow exists but needs improvement

**Process:**
1. Analyze current workflow structure
2. Identify gaps or redundancies
3. Check phase ordering
4. Verify dependencies
5. Suggest improvements
6. Update workflow doc and command metadata

**Example:**
```
Input: existing deployment-workflow.md
Output: Improved workflow with added verification phase
```

## Workflow Document Structure

Location: `workflows/[workflow-name].md`

Template:
```markdown
# [Workflow Name]

## Overview
[1-2 sentence description of goal]

## When to Use
- [Use case 1]
- [Use case 2]

## Phases

### 1. [Phase Name] (interactive/automated)
- **Command:** /command-name
- **Purpose:** What this phase accomplishes
- **Output:** What it produces
- **Requires:** Dependencies (optional)
- **Repeatable:** yes/no (optional)

### 2. [Next Phase]
...

## Execution

**Manual (step-by-step):**
```bash
/command1
/command2
/command3
```

**Automated (full workflow):**
```bash
/workflow-run [workflow-name]
```

**Hybrid (check progress):**
```bash
/workflow-status [workflow-name]
```

## Notes
- [Important considerations]
- [Common pitfalls]
- [When to deviate]
```

## Command-Workflow Metadata

Commands reference workflows BELOW frontmatter:

```markdown
---
name: command-name
description: What command does
---

**Workflow:** [workflow-name](../../aug-core/workflows/workflow-name.md) • **Phase:** phase-name (step X/Y) • **Next:** /next-command

[rest of command]
```

**Key elements:**
- Link to workflow doc
- Phase name (matches workflow doc)
- Step number (X of Y total)
- Next command suggestion

## Discovery Mode Details

**Given:** Set of related commands
**Goal:** Identify and document the workflow

**Steps:**

1. **List commands and their purposes**
   ```
   /plan-chat - Interactive design session
   /plan-breakdown - Decompose into tasks
   /plan-create - Generate GitHub issues
   /work - Execute task
   ```

2. **Identify natural sequence**
   - What order do users run these?
   - What dependencies exist?
   - What's the entry point?

3. **Group into phases**
   ```
   Planning Phase:
   - /plan-chat
   - /plan-breakdown
   - /plan-create

   Execution Phase:
   - /work (repeatable per task)
   ```

4. **Extract patterns**
   - Which phases are interactive?
   - Which are automated?
   - Which repeat?
   - What are the outputs?

5. **Generate workflow document**
   - Create `workflows/[name].md`
   - Document phases with metadata
   - Add usage examples

6. **Update command metadata**
   - Add workflow reference to each command
   - Specify phase and step number
   - Link to next command

## Design Mode Details

**Given:** Description of needed workflow
**Goal:** Create new workflow and commands

**Steps:**

1. **Clarify the goal**
   - What's the overall objective?
   - Who uses this workflow?
   - How often?

2. **Break into phases**
   - What are the major steps?
   - What's produced at each step?
   - What are the dependencies?

3. **Identify decision points**
   - Where does user choose?
   - Where does context determine path?
   - What's interactive vs automated?

4. **Create workflow document**
   - Follow template structure
   - Define each phase clearly
   - Document execution modes

5. **Scaffold commands**
   - Create command files
   - Add frontmatter
   - Add workflow metadata
   - Outline command instructions

6. **Implement commands**
   - Flesh out instructions
   - Add examples
   - Link to related skills

## Refactor Mode Details

**Given:** Existing workflow
**Goal:** Improve structure and clarity

**Analysis questions:**

1. **Completeness**
   - Missing phases?
   - Missing optional branches?
   - Missing error handling?

2. **Ordering**
   - Logical sequence?
   - Dependencies respected?
   - Parallel opportunities?

3. **Clarity**
   - Phase purposes clear?
   - Outputs well-defined?
   - Next steps obvious?

4. **Consistency**
   - Commands follow same patterns?
   - Metadata consistent?
   - Terminology aligned?

**Output:**
- Updated workflow document
- Updated command metadata
- Migration notes (if breaking changes)

## Workflow Naming

**Pattern:** `[goal]-workflow.md` or `[domain].md`

**Good names:**
- `epic-development.md` - Clear goal
- `database-migration.md` - Specific domain
- `feature-release.md` - Understandable process

**Bad names:**
- `stuff.md` - Too vague
- `the-way-we-do-things.md` - Too wordy
- `process-1.md` - No meaning

## Phase Design Principles

### 1. Clear Boundaries
Each phase should have:
- Distinct purpose
- Clear entry conditions
- Defined outputs
- Obvious transition to next phase

### 2. Single Responsibility
Phase does ONE thing well:
- ✅ "Design architecture"
- ❌ "Design architecture and write tests"

### 3. Checkpoints
Interactive phases are natural checkpoints:
- Validate progress
- Adjust direction
- Decide next steps

### 4. Automation-Friendly
Phases should be automatable with context:
- Questions answerable from codebase
- Decisions based on CLAUDE.md
- No creative leaps required

## Integration with Hemingwayesque

Apply hemingwayesque principles to workflow docs:
- Concise phase descriptions
- Clear purpose statements
- No ceremony or fluff
- Dense, scannable structure

**Before:**
"This phase is designed to help you interactively work through the architectural design decisions that need to be made."

**After:**
"Interactive architecture design session. Output: design decisions, component breakdown."

## Success Criteria

### Good Workflow Document
- ✅ Goal immediately clear
- ✅ Phases logically ordered
- ✅ Each phase has clear output
- ✅ Dependencies explicit
- ✅ Scannable structure
- ✅ Automation-friendly

### Good Command Integration
- ✅ Command knows its workflow
- ✅ Links to workflow doc
- ✅ Shows current step and next step
- ✅ Matches workflow phase description

### Good Workflow Design
- ✅ Repeatable process
- ✅ Clear value proposition
- ✅ Natural checkpoints
- ✅ Supports both manual and automated execution

## Common Patterns

### Linear Workflow
```
Phase 1 → Phase 2 → Phase 3 → Done
```
Example: epic-development

### Loop Workflow
```
Phase 1 → Phase 2 → Phase 3 → (repeat Phase 3) → Done
```
Example: task execution (work on multiple tasks)

### Branching Workflow
```
Phase 1 → (choice) → Phase 2a OR Phase 2b → Phase 3 → Done
```
Example: project setup (different stacks)

### Parallel Workflow
```
Phase 1 → (Phase 2a + Phase 2b in parallel) → Phase 3 → Done
```
Example: setup (install deps + configure tools)

## Remember

Workflows document existing patterns, they don't invent them. Good workflows emerge from observing how users actually accomplish goals, then formalizing that sequence for reuse and automation.

Commands remain primary. Workflows organize them. User stays in control.
