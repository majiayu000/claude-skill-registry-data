---
name: to-tickets
description: Research an initiative, design its fit with the current system, turn that design into a dependency-ordered execution plan, and then break the plan into tracer-bullet tickets under .work/tickets.
disable-model-invocation: true
---

# To Tickets

Build reviewed **research**, **design**, and **execution plan** documents, then break that plan into **tickets** — tracer-bullet vertical slices, each declaring the tickets that **block** it.

Initiative documents and ticket files are plain Markdown under `.work/tickets/`. Ticket frontmatter is the status and links each ticket to its authoritative document set.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, a doc, a URL) as an argument, read its full contents first.

If a prototype was made for this initiative, inspect it and establish what it is authoritative for before writing the design. Use explicit decisions already in the conversation; if its intended fidelity is unclear, ask the user. Never infer authority from how polished the prototype looks.

- **Pixel-perfect reference:** Preserve both the visual design (layout, typography, colours, spacing, and component appearance) and the agreed UX flow, interactions, states, and behaviour.
- **UX-flow reference:** Preserve the agreed journey, information hierarchy, interactions, states, and behaviour. Its visual styling is not a target to copy; use the project's design system and conventions for the finished UI.

Use the prototype as the source for the design, execution plan, and tickets within that declared scope—not merely as inspiration. Record its exact path or URL, reference mode, and any explicitly agreed exceptions in the design. If authority differs by screen or aspect, record those boundaries explicitly. Departures from authoritative aspects require user approval; visual improvements to a UX-flow reference do not.

### 2. Explore the codebase

If you have not already explored the codebase, do so to understand the current state of the code. Ticket titles and descriptions should use the project's own vocabulary and respect the conventions and decisions already documented in the repo (`CLAUDE.md`, `docs/`, ADRs) in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Write and review the research

Choose a short, stable initiative slug. Create `.work/tickets/<initiative-slug>/`; never overwrite another initiative's documents.

Write `.work/tickets/<initiative-slug>/research.md` before designing the solution. Build the grounding information needed to make the project's decisions:

- Use the project's vocabulary and separate verified facts from assumptions or open questions.
- Use authoritative primary sources: official documentation, specifications, standards, maintainer-authored material, and peer-reviewed research where relevant.
- Reject tertiary summaries, SEO content, Medium-style posts, and other unsourced blog material.
- Cite every externally grounded claim inline with a descriptive Markdown link to the exact URL. Include a sources section, but never use it as a substitute for inline citations.
- Cover only information that can affect the design, constraints, compatibility, or implementation.

Give the completed research document and the project context to a fresh reviewer subagent. Require it to open the cited sources and check source authority, citation support, factual accuracy, missing decision-relevant facts, and unsupported conclusions. Fix every substantiated finding before proceeding. Do not start the design while research findings remain open.

### 4. Write and review the design

Write `.work/tickets/<initiative-slug>/design.md` only after the research review fixes are complete. Describe how the proposed capability fits the existing system. Keep the document project-agnostic: use terms such as MCP only when they are part of the actual initiative.

The design must:

- Reuse the system's existing architecture, boundaries, and conventions.
- Define responsibilities, interfaces, data and control flow, failure handling, and recovery.
- Account for expected load, concurrency, capacity limits, backpressure, and overload behaviour where relevant.
- Identify performance-sensitive paths, budgets or targets, and how they will be measured.
- Define useful monitoring and observability: signals, health indicators, and actionable failure detection.
- Identify deliberate extension seams without building abstractions or infrastructure for hypothetical futures.
- Prefer the simplest robust solution that satisfies current requirements; justify every new moving part.

Give the completed design, reviewed research, and project context to a fresh reviewer subagent. Ask it to check system fit, traceability to evidence, correctness under failure and load, performance and monitoring coverage, extension boundaries, and avoidable complexity. Fix every substantiated finding before proceeding. Do not start the plan while design findings remain open.

### 5. Write and review the execution plan

Write `.work/tickets/<initiative-slug>/plan.md` only after the design review fixes are complete. This is a high-level execution plan for coding agents, not a ticket list.

The plan must:

- Define outcome-oriented stages in dependency order.
- State what must exist and what gate must pass before each later stage can begin.
- Trace every stage to the relevant design decisions and project outcomes.
- Include stage-level verification without prescribing low-level implementation steps.
- Avoid ticket-sized tasks, file paths, function or class names, code snippets, and command-by-command instructions.
- Use direct, concrete language that another coding agent can execute without filler.

Give the completed plan, design, research, and project context to a fresh reviewer subagent. Ask it to check dependency order, missing prerequisites, design coverage, stage boundaries, verification gates, and usefulness to coding agents. Fix every substantiated finding.

Finally, read all three documents together. Resolve contradictions, ensure the design is grounded in the research, and ensure the plan covers the complete design before drafting any tickets.

The reviewed documents are the initiative-wide source of truth and must preserve the prototype's agreed decisions within its declared reference scope when one exists. Tickets may narrow a slice's scope, but must not replace or contradict documented evidence, decisions, constraints, or prerequisite order.

### 6. Draft vertical slices

Break the work into **tracer bullet** tickets.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests) — vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- Any prefactoring should be done first

</vertical-slice-rules>

Give each ticket its **blocking edges** — the other tickets that must complete before it can start. A ticket with no blockers can start immediately.

**Always end with a final verify-and-fix ticket.** The last ticket is blocked by every other ticket in this initiative. It reads the initiative's research, design, and plan; walks every preceding ticket's acceptance criteria against the actual code; and verifies the *whole* — end-to-end behaviour, plan requirements no single ticket owned, and integration seams between slices. Any gap it finds it **fixes right there, in this ticket**. The ticket is only done when the documented plan is delivered, not when gaps are catalogued. Only a gap too large to close in this ticket's context window is recorded under `## Notes` as concrete follow-up work. Its acceptance criteria list the plan's top-level outcomes, not per-ticket details.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change — rename a column, retype a shared symbol — whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own ticket blocked by the expand, keeping CI green batch to batch because the old form still exists. Finally contract: delete the old form once no caller remains, in a ticket blocked by every migrate batch.

### 7. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which other tickets (if any) must complete first
- **What it delivers**: the end-to-end behaviour this ticket makes work

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct — does each ticket only depend on tickets that genuinely gate it?
- Should any tickets be merged or split further?

Iterate until the user approves the breakdown. Do not write any ticket files before approval; the reviewed research, design, and plan already exist.

### 8. Write the ticket files

Write ticket files at the root of `.work/tickets/`. Write **one file per ticket** — never a single combined file — named `<NN>-<slug>.md`, numbered in dependency order (blockers first). Keep the three source documents in their existing initiative subdirectory.

If `.work/tickets/` already contains tickets, continue numbering from the highest existing id. Never renumber or overwrite existing tickets; `blocked_by` may point at them.

<ticket-file-template>

```markdown
---
id: "03"
title: Short descriptive name
status: todo
blocked_by: ["01", "02"]
context: ".work/tickets/<initiative-slug>"
---

# 03 — Short descriptive name

## What to build

The end-to-end behaviour this ticket makes work, from the user's perspective — not a layer-by-layer implementation list.

## Source documents

- [Research](<initiative-slug>/research.md)
- [Design](<initiative-slug>/design.md)
- [Plan](<initiative-slug>/plan.md)

Read all three before implementation. This ticket narrows the delivery slice; the documents define the initiative-wide evidence, decisions, constraints, and execution order.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Notes

Context an implementing agent needs that isn't obvious from the codebase. Omit if there is none.
```

</ticket-file-template>

If a prototype exists, add a `Prototype` link with its exact path or URL and declared reference mode under every ticket's `## Source documents`, and require implementing agents to inspect it before implementation. Acceptance criteria for affected slices and the final verify-and-fix ticket must verify fidelity within that scope: compare rendered visuals and exercise the UX for pixel-perfect references; exercise the UX flow without requiring visual matching for UX-flow references. Carry through any screen-specific boundaries and explicitly documented, user-approved departures.

<status-vocabulary>

- `todo` — not started. Every ticket you write starts here.
- `in-progress` — claimed by an implementing agent.
- `done` — implemented, reviewed, and committed.
- `blocked` — cannot proceed; the reason is recorded under `## Notes`.

`blocked_by` is a list of ticket ids as quoted strings, or `[]` for "can start immediately".

`context` is the repository-relative directory containing this ticket's reviewed `research.md`, `design.md`, and `plan.md`.

</status-vocabulary>

Avoid specific implementation file paths or code snippets in the ticket body — they go stale fast. Keep the exact `context` path and source-document links in every ticket. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to the decision-rich parts.

Before handoff, read every proposed ticket against all three source documents. Confirm that every plan stage is covered, acceptance criteria preserve the design, no ticket contradicts the research, and `blocked_by` edges enforce the plan's prerequisite gates. Fix every mismatch.

### 9. Hand back the implementation prompt

Finish by printing a fenced block the user can copy verbatim into a fresh agent. Nothing else after it.

<handoff-prompt-template>

````
```
/implement-tickets

Repo: <absolute path to the repo>
Branch: <current branch>
Tickets: .work/tickets — <NN>–<NN> (<count> tickets)
Documents: .work/tickets/<initiative-slug> — research.md, design.md, plan.md
Goal: <one line describing what the whole set delivers>
```
````

</handoff-prompt-template>

The `implement-tickets` skill is the orchestrator: it reads the source documents before each ticket, works the dependency frontier, delegates each ticket to a fresh agent, reviews the whole implementation against the documented plan, fixes findings, and commits per ticket without asking questions.
</content>
