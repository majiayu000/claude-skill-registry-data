---
name: claude-workflow
description: >-
  CWF knowledge repository providing plan structure, tasklist format, checkpoint
  definitions, amendment rules, and validation requirements. Load this skill when:
  (1) executing CWF commands like /write-plan, /implement-plan, /amend-plan,
  (2) answering questions about CWF workflow or plan/tasklist format,
  (3) validating plan or tasklist documents,
  (4) understanding phase structure or task conventions.
  This is KNOWLEDGE context, not an action - do NOT confuse with the /write-plan,
  /implement-plan, /amend-plan, or /brainstorm commands which are user-invoked.
---

# Claude Workflow

Knowledge repository for Claude Workflow (CWF).

## Overview

CWF is a plan-driven development workflow using complementary documents that work together to guide feature implementation. All documents are stored in `.cwf/{feature-name}/`.

**Plan Document (`.cwf/{feature-name}/{feature-name}-plan.md`):**

- Captures architectural context and design rationale
- Documents WHY decisions were made and WHAT the solution is
- **Structure defined in `plan-spec.md`**

**Tasklist Document (`.cwf/{feature-name}/{feature-name}-tasklist.md`):**

- Provides step-by-step execution guidance
- Documents WHEN to do tasks and HOW to implement them
- **Structure defined in `tasklist-spec.md`**

**Mockup (`.cwf/{feature-name}/{feature-name}-mockup.html`) [Optional]:**

- Visual reference for UI/frontend features
- **Conventions defined in `mockup.md`**

**All documents follow the conformance requirements defined below.**

---

## Conventions

### Feature Naming

Feature names MUST:

- Use kebab-case (lowercase with hyphens)
- Be 1-3 words, concise and descriptive
- Contain only lowercase letters, numbers, and hyphens
- Start with a letter

Feature names MUST NOT contain uppercase, underscores, or start/end with hyphens.

**Validation pattern:** `^[a-z][a-z0-9]*(-[a-z0-9]+)*$`

**Examples:** `query-command`, `user-auth`, `oauth2-flow`

### Directory Structure

CWF planning documents MUST be stored in `.cwf/{feature-name}/`:

```text
.cwf/
└── {feature-name}/
    ├── {feature-name}-plan.md       [REQUIRED]
    ├── {feature-name}-tasklist.md   [REQUIRED]
    └── {feature-name}-mockup.html   [OPTIONAL]
```

The `.cwf/` directory is hidden to keep project root clean. Per-feature subdirectories contain related artifacts.

---

## Conformance and Tailoring

**All CWF planning documents (plans and tasklists) use RFC 2119 keywords to define requirements.**

The specifications in `plan-spec.md` and `tasklist-spec.md` use these keywords as described in RFC 2119.

- **MUST** / **REQUIRED** / **SHALL** - Mandatory requirements for all plans
- **SHOULD** / **RECOMMENDED** - Strongly recommended; include unless there's good reason not to
- **MAY** / **OPTIONAL** - Optional enhancements; include when they add value
- **MUST NOT** / **SHALL NOT** - Absolute prohibitions
- **SHOULD NOT** - Generally inadvisable; avoid unless there's good reason

---

## Checkpoints

Checkpoints are end-of-phase validation operations that provide quality control for AI-driven development.

**Purpose:**

- Validate code quality independent of functional testing
- Ensure AI-generated code meets project standards
- Catch issues early before accumulating technical debt

**Checkpoint Types:**

- **Self-review:** Agent reviews implementation against phase deliverable
- **Code quality:** Linting, formatting, type checking (project-specific tools)
- **Code complexity:** Complexity analysis (project-specific thresholds)

Human review occurs after checkpoints complete, when "Phase X Complete" is signaled.

**Where checkpoints appear:**

- **Plan:** Checkpoint strategy explains WHY these checkpoints and WHAT tools
- **Tasklist:** Checkpoint checklist specifies WHEN to run and HOW to execute

**Key principle:** Checkpoints are validation operations performed after phase task completion but before moving to the next phase. They are distinct from functional tests, which validate feature behavior.

---

## CWF Workflow

The CWF planning workflow follows this command-driven flow:

```text
  /brainstorm (optional) [Human runs]
         ↓
  Design Summary [Agent writes]
         ↓
     /write-plan [Human runs]
         ↓
   Plan + Tasklist [Agent writes]
         ↓
   /implement-plan [Human runs]
         ↓
  Phase 1 [Agent implements] → Checkpoints [Agent runs] → Review [Human] → ✓ → /clear [Human runs]
         ↓
 Phase 2 [Agent implements] → Checkpoints [Agent runs] → Review [Human] → ✓ → /clear [Human runs]
  [Changes?] → /amend-plan [Human runs] ──┐
         ↓                                │
  Continue development [Agent] ←──────────┘
         ↓
  Feature Complete ✓ [Human confirms]
```

### Stage Breakdown

**1. `/brainstorm` Command (Optional)**

- **Human:** Runs `/brainstorm` command (optional step for structured exploration)
- **Agent:**
  - Systematically extracts requirements through guided questions
  - Explores 2-3 alternative approaches with trade-offs
  - Incrementally builds design with validation checkpoints
  - Produces design summary document in `docs/brainstorms/`
- **Outcome:** Complete design context ready for `/write-plan`
- **Note:** Can be skipped in favor of informal planning discussion or written specification

**2. `/write-plan` Command**

- **Human:** Runs `/write-plan` command
- **Agent:** Generates two documents:
  - Plan: Architectural context and WHY/WHAT decisions
  - Tasklist: Step-by-step HOW/WHEN execution guidance
  - Validates structure and consistency between documents

**3. Phase-by-Phase Implementation**

The implementation follows this repeating cycle:

- **Human:** Runs `/implement-plan` command
- **Agent:**
  - Reads plan for architectural understanding
  - Checks tasklist to identify completed tasks and current phase
  - Works through tasks for current phase sequentially
  - Marks tasks complete as work progresses
  - Executes checkpoints (code quality, complexity checks, etc)
  - Signals phase completion for human review at phase boundary
- **Human:**
  - Reviews phase results when agent signals completion
  - Runs `/clear` to start fresh session for next phase
  - **Repeats cycle:** Runs `/implement-plan` again for next phase

**Note:** Conversation history is lost after `/clear`; only plan, tasklist checkboxes, and committed code persist across cycles.

**4. `/amend-plan` Command (When Needed)**

- **Human:** Discusses amendment and runs `/amend-plan` when requirements change during development
- **Agent:**
  - Adds tasks to incomplete phases
  - Creates new phases for additional work
  - Updates plan sections with new context
  - Follows amendment safety rules
- **Agent:** Continues development with amended plan

**5. Feature Completion**

- **Agent:** Completes all phases and signals completion
- **Human:** Reviews and confirms feature is complete (✓)

## Quick Reference

| Need to understand... | Read This Reference | Contains |
|----------------------|---------------------|----------|
| **Plan document specification** | `references/plan-spec.md` | Plan structure requirements with RFC 2119 keywords |
| **Tasklist document specification** | `references/tasklist-spec.md` | Tasklist structure requirements with RFC 2119 keywords |
| **Amendment rules and safety** | `references/amendment.md` | Rules for safely modifying plans and tasklists |
| **Mockup conventions** | `references/mockup.md` | When and how to create HTML mockups |

---

**Skill loaded.** CWF planning concepts and patterns are now available.
