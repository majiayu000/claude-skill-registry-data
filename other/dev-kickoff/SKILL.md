---
name: dev-kickoff
description: Use for feature/component additions, cross-file behavior changes, refactors, migrations, or changes to data models, dependencies, security, or deployment, and when task size is unclear. Skip Trivial/Small work (typos, formatting, one-line or single-file fixes). If direction is vague, use mak:brainstorming first.
---

# Development Kickoff — Turning Requirements into an Approvable Design

This skill owns conversational orchestration. Before implementation starts, the main thread narrows requirements, requests non-interactive architecture consultation from `mak:planner` when needed, and converges user decisions into an approved design. It is not the repeated author of the final design doc.

Conduct the conversation and all user-facing output in the user's language (or the project's documented language policy).

## Sizing criteria (entry judgement)

Enter for behavior changes spanning multiple files/modules, new features/components, architecture decisions, or suspected impact on data models, dependencies, security, or migration. When the boundary is unclear, judge by impact: roughly single-file/few-lines with no change to public interfaces, data shapes, or dependencies → Trivial / Small (do not enter); spanning 2+ files/modules or changing interfaces, data models, dependencies, or security → Standard or above (enter).

### Route to a different skill when

- Direction itself is vague and idea divergence is needed first → `mak:brainstorming`
- Establishing/updating the project-wide **phase structure** or mid/long-term roadmap → `mak:roadmap-planning`
- Writing a feature/module **design doc** to spec → `mak:design-doc-template`
- The task itself is undecided and must be derived from the documents → `mak:dev-resume`

## Approval gate

Write nothing — no file creation, modification, or deletion — until the user approves the design (§6). Scope and approach are the user's decision, and anything written earlier may be thrown away. Between approval and implementation the only write is the design doc itself (§7) and edits to it. Reading files, read-only commands, and search are fine throughout. If sizing comes out clearly Trivial / Small, leave this skill for the lightweight flow.

## Checklist

Complete in order:

1. **Explore project context** — README, CLAUDE.md, docs/, recent commits, related source files
2. **Clarifying questions** — ask the ones whose answers would materially change the work, together in one message
3. **Decide on planner consultation** — Standard: as needed; Risky / multi-module / migration: request a `mak:planner` Architecture Brief as a rule
4. **Propose 2–3 approaches** — with trade-offs and a recommendation, based on the planner report or main-thread investigation (include at least one simpler alternative)
5. **Convert to verifiable goals** — turn the task into measurable success criteria and a `Step → verify: check` plan
6. **Present the design** — the whole design at once; get one approval
7. **Documentation handoff** — the main thread saves the approved design per the `mak:design-doc-template` spec
8. **Self-review** — unconfirmed decisions, contradictions, scope problems + simplicity / precise-changes self-check
9. **Report and proceed** — give the saved path; re-confirm only if self-review or a requested change alters an approved decision
10. **Handoff to next stage** — see the Handoff section below

## Procedure

### 1. Explore project context

Before asking questions:

- `README.md` for project overview, setup, purpose
- `CLAUDE.md` (or `AGENTS.md`, `GEMINI.md`) for project rules and agent definitions
- `docs/` and the project's design-doc path for existing architecture decisions
- Recent git commits for current direction
- Existing patterns related to the request

### 2. Clarifying questions

- Ask only questions whose answers would materially change scope, approach, or success criteria
- Batch them in one message; use the AskUserQuestion tool when choices are enumerable (up to 4 questions per call)
- Decide routine details yourself and list them as assumptions
- Split into a later round only when an answer changes which questions come next
- If the request spans independent subsystems, confirm the decomposition first

### 3. Decide on planner consultation

Decide by task grade whether to call `mak:planner`.

- **Trivial / Small**: stop this skill and switch to the lightweight flow (direct, or `mak:coder` on the user's explicit request). Do not call planner.
- **Standard**: request a planner Architecture Brief when the existing structure is complex or options genuinely diverge.
- **Risky / multi-module / migration**: request a planner Architecture Brief as a rule.

When calling planner, pass along the requirements confirmed so far, constraints, relevant doc/code paths, and candidate user questions. Planner cannot talk to the user, so the main thread discusses the "decisions needed" items from planner's report with the user and confirms them.

### 4. Propose approaches

- Always present 2–3 options. Never just one
- Include at least one simpler alternative. If the user's initial idea seems excessive, push back explicitly and recommend the simpler option
- Lead with the recommendation and explain why
- Include concrete trade-offs (complexity, simplicity, performance, maintainability, reversibility)
- If hard constraints leave only one real option, state the constraint and proceed with a single option. Do not fabricate alternatives

### 5. Convert to verifiable goals

Before moving to design, convert the request into measurable success criteria.

**Conversion examples**:

| Vague request | Verifiable goal |
| :--- | :--- |
| "Add validation" | Write and pass tests for invalid inputs |
| "Fix the bug" | Write a test reproducing the bug and make it pass |
| "Refactor X" | Identical tests pass before and after |
| "Make the slow screen fast" | Specify measurement point, method, and target (e.g. initial render < 200ms) |

**Multi-step plan**: if the work has 2+ steps, produce:

```
1. <Step>  → verify: <check>
2. <Step>  → verify: <check>
3. <Step>  → verify: <check>
```

This table goes into the design doc as §5.0, inside its §5 verification plan (see `mak:design-doc-template`).

Clear success criteria enable independent iteration. Narrow vague criteria like "just make it work" before proceeding.

### 6. Present the design

- Present all sections in one message: architecture, component boundaries, data flow, error handling, test strategy — each at a length matching its complexity
- Request one approval. Revise on feedback

### 7. Documentation handoff

Runs only after §6 design approval. Save it with meta `Status: approved`. This step's core responsibility is pinning the approved design as a document **once**, written directly by the main thread per the `mak:design-doc-template` spec (sections, save location, file naming).

`mak:dev-kickoff` never loops draft-then-rewrite on the same document — write it once here; later steps only revise it (§8 self-review fixes, §9 user change requests).

**No git commits** — version control is done by the user, except on explicit request or when project rules say otherwise.

### 8. Self-review

After writing the design doc in §7, check:

- **Incomplete items** — any "TBD", "TODO", unclear requirements? Items needing user decisions get confirmed in the main thread; only genuinely technical uncertainty goes to §Assumptions/Unreviewed.
- **Consistency** — do sections contradict each other?
- **Scope** — focused on a single implementation cycle?
- **Ambiguity** — any requirement readable two ways? Pick one and make it explicit.
- **Simplicity** — unrequested features / speculative flexibility / impossible-scenario error handling / excessive abstraction? Remove them.
- **Precise changes** — does every §4 scope item connect directly to the user's request? Split out anything that doesn't.
- **Verifiability** — does §5.0 contain measurable success criteria or a `Step → verify` table?

Fix immediately. No re-review needed.

If self-review produced substantive changes beyond typos, mention them briefly when handing the document to the user.

### 9. Report and proceed

> "The design doc is saved at `<path>`. Moving to implementation — tell me if anything should change."

State the saved path and move to §10 without waiting for a second approval. The user may still request changes — apply them and re-run the self-review. If self-review or a requested change alters an already-approved decision (not wording), present that change and get approval before §10.

### 10. Handoff to next stage

```
1. Design approved at §6 — never move on without it
   - The doc was written once in §7, do not rewrite it

2. Delegate implementation to coder after approval
   - If the mak:coder agent is available:
       → delegate to mak:coder (pass the approved design doc path)
   - Otherwise:
       → implement directly (the design doc is the SSOT for scope)

3. Verify each step before any review handoff
   - If implementation was delegated to mak:coder:
       → coder runs mak:verify-checklist itself; confirm its reported results
   - Otherwise:
       → verify each step against its §5.0 verify criterion (run
         mak:verify-checklist when the project declares verification commands),
         and update that step's Status cell once it passes
         (per the mak:design-doc-template §5.0 status-column rule)

4. Delegate review on major-stage completion
   - If the mak:reviewer agent is available:
       → delegate to mak:reviewer (pass review scope and design doc path)
   - Otherwise:
       → self-review by applying the mak:review-report checklist directly

5. Delegate doc sync when needed
   - If the mak:doc-editor agent is available:
       → delegate to mak:doc-editor (pass the list of documents to sync)
   - Otherwise:
       → update documents directly
```

The design doc is the source of truth. All subsequent agents (or direct work) operate against it.
