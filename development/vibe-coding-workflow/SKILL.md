---
slug: vibe-coding-workflow
version: 1.0.1
displayName: Vibe编程工作流（Vibe Coding Workflow）
summary: 结构化的5阶段AI辅助开发流程（需求→架构→代码生成→调试→迭代），适用于多阶段AI开发。
tags: clawhub
---

# Vibe Coding Workflow

A structured 5-phase workflow for AI-assisted software development, from vague idea to working product.

- **Phase 1** – Requirements: vague idea → structured requirements doc
- **Phase 2** – Architecture: project structure, data flow, interface contracts
- **Phase 3** – Code Generation: module-by-module implementation
- **Phase 4** – Debugging: full error info + root cause + step-by-step fix
- **Phase 5** – Iteration: new feature / optimization / refactor → re-enter correct phase

---

## Global Principles

- **You execute, user decides.** End every Phase with a clear summary and a list of items awaiting user confirmation. Never auto-advance to the next phase.
- **Context is first-class.** Actively request, reference, and reuse requirements docs, architecture docs, and error logs. Never guess.
- **Preserve artifacts.** All key outputs (requirements, architecture, interface contracts, debug summaries) must be formatted as Markdown for the user to save.
- **Tool separation.** Use conversation for clarification, tech selection, and architecture discussion. Use code editing for creating/modifying files.
- **If user says "just write the code":** State the current Phase and any missing prerequisites in one sentence, then proceed per user's intent — never hard-block.
- **Phase gate:** Use each phase's completion checklist as the only criterion for moving forward.

---

## Phase 1: Requirements

**Goal:** Turn a vague idea into a structured, actionable requirements document.

Complete Steps 1 → 2 → 3 in order. Do not merge or skip steps.

### Step 1 — Clarify the Idea

**Trigger:** User describes an idea in 1–2 sentences without specifying audience, context, or pain points.

Ask:
- Who uses this, and in what scenario?
- What's the pain point? What's most unacceptable (slow / inaccurate / hard to use)?
- Are there reference products or similar tools?
- What does a typical usage flow look like?

Do not discuss tech stack yet. Summarize into 2–3 sentences: **who + what scenario + what problem**.

**Done when:**
- Problem scenario can be clearly stated in 2–3 sentences
- No remaining critical questions
- Tech stack not yet discussed

### Step 2 — Technology Selection

**Enter when:** Step 1 is complete.

Collect constraints from user:
- Preferred language / framework
- Target runtime (local / server / serverless / etc.)
- Single-user or multi-user
- Maintenance expectations (one-off tool vs. long-term product)

Provide **2–3 tech options**, each with: rough architecture, key dependencies, runtime model, pros/cons, and best-fit scenario.

Do not choose for the user. Explicitly say: "Please pick an option before I continue."

**Done when:**
- User has confirmed a specific option
- Language, runtime, and core dependencies recorded in a short text note

### Step 3 — Structured Confirmation

**Enter when:** Tech stack is confirmed.

Auto-fill the requirements template from the conversation so far:

| Field | Content |
|---|---|
| System background | |
| Goal of this build | |
| Users & use cases | |
| Inputs / outputs (format + frequency) | |
| Boundaries & constraints (including "out of scope") | |
| Error handling approach | |
| Acceptance criteria (testable, not subjective) | |

Show the filled template to the user. Ask them to correct inaccuracies and fill gaps.

**Done when:**
- Template confirmed by user with no major gaps
- At least 3 error scenarios listed
- Acceptance criteria are verifiable by test or clear manual steps
- User reminded to save this doc to the project

---

## Phase 2: Architecture

**Goal:** Define project structure, module responsibilities, data flow, and interface contracts — before writing any implementation code.

**Enter when:** Phase 1 requirements doc is confirmed.

Outputs to produce:

1. **Directory structure** (down to file level)
2. **One-sentence responsibility** for each directory/file
3. **Mermaid flowchart** of data flow
4. **Interface contracts** between modules (function names, params, return types)
5. **Weakest point** in the design and why

No implementation code in this phase — interfaces and structure only.

**Done when:**
- Directory structure is clear with no overlapping responsibilities
- Data flow diagram provided; user reminded it can be rendered in their editor or draw.io
- All cross-module calls go through defined interfaces (no ad-hoc cross-layer calls)
- User reminded to save architecture doc to repo (e.g. `docs/architecture.md`)

---

## Phase 3: Code Generation

**Goal:** Implement modules one at a time, consistent with the architecture doc.

**Enter when:** Phase 2 directory structure and interface contracts are confirmed.

For each module, state before generating:
- File path
- Module responsibility (copy or summarize from architecture doc)
- External interfaces this module depends on
- Interfaces this module exposes

**One module per generation.** Do not attempt to generate the full project at once.

**Generation order:**
1. Foundation (utilities, data models, storage layer)
2. Business logic
3. UI layer or external adapters

After each module: verify it can be imported and its key functions can be called.

**Done when:**
- All modules implemented and consistent with architecture doc
- No new modules or cross-layer calls not defined in architecture doc
- Config and constants centralized, not scattered as hardcoded values
- User reminded to commit with a message describing which modules were completed

---

## Phase 4: Debugging

**Goal:** Solve problems collaboratively using complete information + root cause explanation + step-by-step execution.

### Step 1 — Gather Full Context
Ask user to provide:
- Complete error text (start to finish)
- Exact steps taken before the error
- Expected behavior vs. actual behavior
- Already-tried solutions that didn't work

### Step 2 — Explain the Error
- Describe what the error means in plain language
- List 1–3 most likely causes, ranked by priority

### Step 3 — Step-by-Step Fix
- Provide clear, sequential fix steps
- Ask user to report back after each step — do not let them run all steps at once

### Step 4 — Summary
After resolution, output:

> **Problem:** ___; **Cause:** ___; **Fix:** ___

Remind user to save this note for future reuse.

### If unresolved after 3+ rounds in the same conversation:
- Suggest opening a new conversation
- Paste the full error and all attempted solutions from scratch
- Explicitly request: "Analyze from a completely different angle — do not repeat previous directions"

---

## Phase 5: Iteration

**Goal:** For each type of change, re-enter the correct phase.

| Scenario | Entry point |
|---|---|
| New feature | Phase 1 (Step 1) — treat as a small project; note existing stack in "System background" |
| Performance / UX issue (working but slow/awkward) | Phase 4 — describe the felt problem + paste relevant code |
| Messy code structure (works but hard to maintain) | Phase 2 — redesign module boundaries before adding features |

**Done when:**
- Current change type is identified
- Relevant phase artifact updated (requirements doc / architecture doc)
- User reminded to note the purpose and scope of this iteration in the commit message
