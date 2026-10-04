---
name: improve-codebase-architecture
description: Surface architectural friction and propose deepening opportunities that improve testability and AI-navigability. Use when the user wants to improve architecture, find refactoring opportunities, consolidate tightly-coupled modules, or make a codebase easier for agents to navigate.
---

# Improve Codebase Architecture
Use this skill to find **deepening opportunities**: refactors that turn shallow **Modules** into deeper ones by putting more useful behavior behind a smaller, clearer **Interface**.
The output is candidates and a guided design conversation. Do not refactor, create a new **Interface**, or rewrite production code until the user selects a candidate and asks for implementation.

## Required Vocabulary
Use these terms exactly: **Module**, **Interface**, **Implementation**, **Depth**, **Seam**, **Adapter**, **Leverage**, and **Locality**. Do not replace them with "component," "service," "API," or "boundary." See [references/LANGUAGE.md](references/LANGUAGE.md).
Principles: run the **deletion test**; treat the **Interface** as the test surface; one **Adapter** is a hypothetical **Seam** and two **Adapters** make it real.

## Agent Forge Context
Load existing context first:

1. `knowledge/_shared.yaml`.
2. Relevant `knowledge/repos/*.yaml` for domain language and repo patterns.
3. Active Beads issue context, including `design:` and `worklog:` comments.
4. Existing ADRs when the repo already has them.

If knowledge or ADR files are absent, proceed silently. Do not create `CONTEXT.md`, ADRs, knowledge YAML, or Beads issues up front. Beads is the default place for durable decisions and follow-up work unless the user explicitly asks otherwise.

## Process
### 1. Explore Organically
Walk the codebase with focused searches, file reads, and exploration agents when the scope is broad. Note where understanding becomes expensive:

- Understanding one concept requires bouncing between many small **Modules**.
- A **Module** is shallow: its **Interface** is nearly as complex as its **Implementation**.
- Pure functions exist only for testability while real bugs hide in call choreography, with poor **Locality**.
- Tightly-coupled **Modules** leak across **Seams**.
- Code is untested or hard to test through its current **Interface**.

Apply the **deletion test** to suspected shallow **Modules**. A strong candidate is one where deletion would spread complexity across callers instead of making it disappear.

### 2. Present Candidates
Present a numbered list. For each candidate include:

- **Files/Modules** - files and **Modules** involved.
- **Problem** - why the current architecture causes friction.
- **Solution** - what would change in plain English.
- **Benefits** - **Leverage**, **Locality**, and test impact.

Use domain language from `knowledge/` and Beads with the architecture vocabulary. If a candidate conflicts with an ADR or Beads `design:` decision, surface it only when real friction justifies revisiting that decision. Do not propose new **Interfaces** yet. End by asking: "Which of these would you like to explore?"

### 3. Grilling Loop
After the user chooses a candidate, ask through constraints before proposing implementation: what behavior belongs behind the deepened **Interface**, where the **Seam** should live, which dependencies fit [references/DEEPENING.md](references/DEEPENING.md), what callers should stop knowing, and which tests should survive internal refactors.

Record durable decisions in Beads with `design:` or `worklog:` comments. If follow-up implementation work appears, create or suggest Beads issues with priority. If the user rejects a candidate for a load-bearing reason, ask whether to record it in Beads or an existing ADR mechanism.

### 4. Design Interfaces Only After Selection
When the user wants alternatives for the selected candidate, hand off to [references/INTERFACE-DESIGN.md](references/INTERFACE-DESIGN.md). That workflow compares multiple possible **Interfaces** only after candidate selection.
