---
name: design-architecture
description: >
  Reviews the current codebase architecture and proposes improvements using four parallel specialist subagents:
  System Architect, Software Architect, Data Architect, and an Adversarial Architect that red-teams failure paths,
  LLM adversarial output scenarios, silent corruption risks, and invariant bypasses. Each subagent independently
  analyzes the codebase from their domain perspective, then their findings are consolidated into a living
  `architecture.md` file with a tracked to-do list and change log. Use this skill whenever the user asks to
  review, analyze, audit, or improve the architecture — or when they ask questions like "what should we change
  structurally?", "how is the system organized?", "what are our architecture problems?", "can you do an
  architecture review?", or "let's redesign X". Also trigger when the user mentions technical debt, structural
  improvements, security concerns, failure modes, vulnerabilities, or wants a second opinion on design decisions,
  even if they don't use the word "architecture".
---

# Design Architecture Skill

This skill performs a structured architecture review by dispatching four specialist subagents in parallel, then
consolidating their findings into a maintained `architecture.md` document. One of the four subagents is a dedicated
adversarial red-team agent that probes failure paths, invariant bypasses, and silent corruption scenarios that
the structural review agents would not naturally surface.

The goal is not to produce a one-time report — it's to maintain a living architectural record that evolves as the
codebase evolves. The to-do list inside `architecture.md` becomes the actionable roadmap.

---

## Workflow

### Step 1 — Read existing architecture.md (if it exists)

Before spawning subagents, check whether `architecture.md` already exists in the project root. If it does, read it
so you understand what was previously documented, what to-dos are already tracked, and what changes have already
been logged. This context shapes what the subagents should focus on (new ground vs. follow-up on prior findings).

### Step 2 — Spawn four subagents in parallel

Launch all four at once (same message, parallel Agent tool calls). Each subagent is defined in
`.claude/agents/` — use the `subagent_type` parameter to route to each one:

| Subagent | File | `subagent_type` | Lens |
|----------|------|-----------------|------|
| System Architect | `.claude/agents/system-architect.md` | `system-architect` | Pipeline structure, orchestration, re-entry |
| Software Architect | `.claude/agents/software-architect.md` | `software-architect` | Code design, abstractions, invariant enforcement |
| Data Architect | `.claude/agents/data-architect.md` | `data-architect` | Data models, formats, deduplication, output correctness |
| Adversarial Architect | `.claude/agents/adversarial-architect.md` | `adversarial-architect` | Failure paths, LLM adversarial output, silent corruption |

Each agent file contains its full focus areas, files to read, questions to answer, and required report format.
You do not need to repeat those instructions in the prompt — the agent definitions carry them. Just tell each
agent what to do:

```
Perform a full architecture review of the mykg codebase at:
/Users/senolisci/Desktop/antigravity projects/mykg

Read your agent definition for full instructions on what to examine and how to format your report.
[Optional: if architecture.md already exists, include a note like: "Pay particular attention to previously
flagged issues in areas X and Y — check whether they have been addressed."]
```

The Adversarial Architect has a different mandate from the other three: it is not looking for design
improvements, only failure paths. Give it the same prompt — its agent definition constrains its focus.

### Step 3 — Consolidate findings

After all four subagents return, synthesize their reports:

- De-duplicate overlapping findings (multiple subagents may flag the same issue)
- Identify cross-cutting themes (e.g., if all three structural agents mention poor error handling, that's a priority)
- Treat Adversarial Architect findings separately: every Critical Failure Path gets its own to-do item tagged `[critical]`, regardless of whether it overlaps with structural findings. These are not design suggestions — they are concrete exploitable paths.
- Prioritize: rank issues by impact × urgency
- Distinguish "fix now" from "consider later" from "track but defer"

### Step 4 — Write or update architecture.md

Write the consolidated findings to `architecture.md` in the project root using this template:

```markdown
# Architecture

Last reviewed: [date]

## System Overview
[2-4 sentence description of what the system does and how it's structured at the highest level]

## Architecture Diagram
[ASCII or text diagram of the major components and data flow — update as the system changes]

## Design Decisions
[Brief summary of the key decisions from CLAUDE.md that shape the architecture — D4, D5, D7, D15, etc.
Link to CLAUDE.md for the full record. Only include the decisions that most affect the structural choices.]

## Current State Assessment
[Honest 2-3 sentence assessment: what's solid, what needs work, what's incomplete]

---

## To-Do List

Items are tagged: `[critical]` `[high]` `[medium]` `[low]` and `[done]` when complete.
Add new items at the top. Never delete done items — mark them `[done]` so the history is preserved.

<!-- New items go here -->

| # | Priority | Area | Task | Added | Done |
|---|----------|------|------|-------|------|
| 1 | [priority] | [System/Software/Data] | [specific actionable task] | [date] | — |

---

## Change Log

Track architectural changes here as they are made. Each entry should say what changed and why.

| Date | Change | Reason |
|------|--------|--------|
| [date] | [what changed architecturally] | [why — drove by which issue/decision] |

---

## Subagent Findings (latest review)

### System Architect
[Paste or summarize the findings from the System Architect subagent]

### Software Architect
[Paste or summarize the findings from the Software Architect subagent]

### Data Architect
[Paste or summarize the findings from the Data Architect subagent]

### Adversarial Architect
[Paste or summarize the Critical Failure Paths, Moderate Risks, and Invariant Violation Analysis from the Adversarial Architect]
```

**If `architecture.md` already exists:**
- Preserve the existing Change Log — append to it, never rewrite it
- Preserve existing `[done]` to-do items — they are historical record
- Add new to-do items at the top of the table with today's date
- Update the "Last reviewed" date and "Current State Assessment"
- Replace the "Subagent Findings (latest review)" section with the new findings
- Update the System Overview and Diagram only if the architecture has materially changed

### Step 5 — Report back to the user

After writing `architecture.md`, give the user a short summary:
- How many issues were found and by which lens (system / software / data / adversarial)
- The top 3 priority to-do items from the structural agents
- The top 2 critical failure paths from the Adversarial Architect — these should always be called out explicitly even if they overlap with structural findings, because they represent concrete exploitable scenarios, not abstract concerns
- Whether any Key Invariants from CLAUDE.md appear to have bypass paths
- Point them to `architecture.md` for the full picture

---

## Maintaining architecture.md over time

Every time this skill runs, it updates the same `architecture.md` file. This creates a living record:

- **To-do list** grows as new issues are found; items are marked `[done]` when addressed (never deleted)
- **Change log** grows as architectural changes are made
- **Subagent findings** section is replaced each run with the latest review

Encourage the user to mark to-do items as `[done]` manually as they implement changes, or you can update them
when you observe that a previously-flagged issue has been resolved in the code.

---

## Notes on the mykg codebase

Key reference: `CLAUDE.md` in the project root contains 28 design decisions (D1–D28) and 5 key invariants.
These are authoritative. Subagents should treat deviations from them as issues, not as opportunities to suggest
alternatives (unless the deviation reveals the decision itself was flawed).

Key structural paths:
- Pipeline entry: `src/mykg/pipeline.py`, `src/mykg/cli.py`
- Pass 1: `src/mykg/pass1.py`, `src/mykg/chunker.py`
- Pass 2: `src/mykg/pass2.py`
- Assembly: `src/mykg/assembler.py`
- Export: `src/mykg/exporter.py`
- Steps: `src/mykg/steps/`
- LLM adapters: `src/mykg/llm/`
- Spec docs: `docs/superpowers/specs/`, `docs/superpowers/plans/`
