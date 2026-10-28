---
name: epic
description: >-
  Use when the user asks to plan a LARGE feature spanning multiple sessions or
  phases — produces an epic under the `tasks` role with dependency-ordered
  phases, atomic tasks and per-phase status. Use plan for single-session tasks,
  not for roadmaps.
argument-hint: feature name or description
effort: high
---

# Feature Epic

## Overview

Create a structured, decomposed epic under the `tasks` role resolved from AGENTS.md for features too large for a single agent session. The template default uses today's date as a directory hierarchy; the file slug begins with `epic-` (no date prefix in the slug).

## When to Use

- Use `epic` when feature spans >3 files AND requires >2 sessions, OR has >5 phases
- Use `plan` for tasks completable within one agent session
- When unsure: start with `plan`; if it outgrows a single task, upgrade to `epic`

## Context

<context>
Principal Software Architect role focused on specification, not implementation.
You are autonomous and proactive. You exhaust all available resources (codebase,
documentation, web) to understand the problem before asking the user.
</context>

## Rules & Constraints

<rules>
1. **Pure Specification**: MUST NOT write code. Allowed-to-write artifacts:
   - (a) The epic file under the resolved `tasks` role. If the parent directories do not exist, CREATE them (use `mkdir -p`).
   - (b) The resolved `SRS` role — **surgical-edit only**. May insert/extend a single line `- **Tasks:** [epic-<name>](tasks/<relative-epic-path>.md)[, ...]` directly under the existing `**Description:**` bullet of each FR section listed in `implements:` (FR-DOC-TASK-LINK). All other SRS lines MUST remain byte-identical. See step 7a.
2. **Planning**: The agent MUST use a task management tool (e.g., `todo_write`, `todowrite`, `Task`) to track execution steps.
3. **Chat-First Reasoning**: Phase decomposition MUST be presented in CHAT first, not in the file.
4. **No SwitchMode**: Do not call SwitchMode tool.
5. **Proactive Resolution**: Follow `Proactive Resolution` rule from `## Planning Rules` in AGENTS.md.
6. **Stop-Analysis Protocol**: Follow Stop-Analysis rules from `# YOU MUST` in AGENTS.md.
7. **AGENTS.md Planning Rules**: Follow all rules from `## Planning Rules` section in AGENTS.md.
8. **Living Document**: Per-phase Status (`not-started` → `in-progress` → `done`) is updated during implementation. Top-level frontmatter `status` is auto-derived from epic-wide `## Definition of Done` checkboxes by `commit` / `review-and-commit`; do NOT update it manually.
9. **Phase Size Guard**: Each phase SHOULD contain ≤50 requirements and target ≤5 files per task. If exceeded → split.
10. **Implementation Hints Only in Notes**: Epic describes WHAT and WHY. HOW — only in Notes section as implementation hints (patterns, gotchas, references), not as code.
11. **Traceability**: If task implements known FR-* requirements, add `implements:` YAML frontmatter with FR-* codes from the resolved `SRS`. Optional — omit if FR-* not yet defined.
12. **Frontmatter Shape**: Required keys — `date: <YYYY-MM-DD>` (today's date as quoted ISO string), `status: to do` (initial value; auto-derived later), `tags: [...]` (may be empty `[]`), `related_tasks: [...]` (relative paths to other tasks under the resolved `tasks` role, may be empty). Optional: `implements: [FR-...]`.
</rules>

## Question Format (FR-UNIVERSAL.QA-FORMAT)

Binds on EVERY question you ask — the research questions in Step 2 and the phase-approval question in Step 4 alike:

- **Numbered** — each question is a numbered list item (`1.`, `2.`, …), not a heading, a bold-only line, or a paragraph.
- **Self-contained** — the question is answerable from itself and its options alone. Name what is being decided and what the answer changes, inside the question. "Which of the above?", a bare "Your choice?", and "Which variant do you prefer?" with nothing restated are defects: they send the reader back up the transcript to reconstruct the question.
- **Each option stands on its own** — a reader often jumps straight to the options, so an option's title and the lines under it must be enough to choose without the text above the question or the earlier turns. The title is a short name after the option's letter or number, and the reader answers with that letter or number; the `**Essence:**` line under it says what would be done, to what, and what the reader gets. A short reply option with no analysis of its own (Apply / Skip / Edit) has no Essence line, and its title says it alone. **Inside an option, name things in words, never by a report's ids.** Every line of the option — title, Essence, Pros, Cons, Risks, Best for — is read without the report, and ids slip in most often in Pros, Cons and Risks. Write what the thing is instead of its label: "the checkout errand on the shop site", not `E4`; "the search box ignoring the first keystroke", not `N3`. A label in parentheses after a general phrase — "the two most expensive errands (E4, E3)" — is still a bare label: name each item. A number taken from a report keeps what it measures in the same sentence: a percentage names the whole it is a share of ("page text takes about 40% of the cost", not "a 40% share"), and a sum says whose cost it is. **Any phrase that stands for a group is a pointer**: a count ("the four slow pages", "the same three errands"), a category ("the anomalies", "the issues found"), a rank or superlative ("the costliest runs"), "these", "as above", "the current round" — and so is a partial list, a count followed by a few examples or a "such as". Replace it with every member of the group, named in words, in that option — even when the list is long, even when the report above already lists them; if the whole set does not fit, drop the group from the option. Test: with the report deleted, could the reader name every member from this option alone? A word coined in this session gets a short explanation in the option. An explanation elsewhere in the reply does not count — not in the report above the question, not in another option. Before sending, read each option alone, line by line, and list every label (letters plus digits such as `E4` or `N3`), number, group phrase (a count, a category, a superlative, "the same", "these") and coined term in it; replace each with words or remove it.
- **No catch-all option** — never add an option whose only content is an invitation to answer freely ("Other", "Something else", "Your own variant", "Tell me what you need"). The user can always type a free-form reply instead of a letter or number, and an IDE's question tool (`AskUserQuestion` and the like) already offers a free-text answer of its own, so such an option adds a line and no choice. An option that names a concrete alternative is a real option, even when its title starts with "Other".
- **`agent's choice`** — on a multi-select where the user delegates with `agent's choice` (or its language equivalent), pick the subset yourself, justify the pick in one line, and proceed without re-asking for confirmation.

The phase breakdown itself stays ABOVE the question: the phases are a dependency-ordered sequence, not a set of alternatives, so they are not the question's options. That makes the self-containment rule do all the work — the approval question must restate what it is asking about. Critique-points selection (Step 7) is auto-classified by the agent and asks the user nothing.

## Instructions

<step_by_step>

1. **Initialize**
   - Use a task management tool (e.g., `todo_write`, `todowrite`) to create a plan based on these steps.
   - Compute today's date in `YYYY-MM-DD` format (e.g. via `date +%Y-%m-%d`). Hold it as `<DATE>`. Derive `<YYYY>`, `<MM>`, `<DD>` (zero-padded). Resolve `tasks` from AGENTS.md and derive the eventual epic path from that role's layout.

2. **Deep Context & Research**
   - Resolve `SRS` and `SDS` from AGENTS.md. If you don't know their current content — read the resolved files now.
   - Follow `Proactive Resolution` from AGENTS.md: analyze prompt, codebase, search for gaps.
   - Use search tools (e.g., `glob`, `grep`, `ripgrep`, `search`, `webfetch`) for unknowns.
   - If uncertainties remain: ask user clarifying questions. STOP and wait.

3. **Draft Spec Header**
   - Create the resolved epic file's parent directories (use `mkdir -p`).
   - Write to the resolved epic file the following sections:
     - YAML frontmatter with all required keys (rule 12): `date`, `status: to do`, `tags`, `related_tasks`, optional `implements`.
     - Title and metadata table (Status: Draft, Created/Updated dates)
     - Goal (business/user value — why are we building this?)
     - Overview (current state, why now, relevant context)
     - Non-Goals (explicit exclusions — critical for AI agents)
     - Architecture & Boundaries (three-tier: Always / Ask First / Never)
     - Definition of Done (measurable acceptance criteria)
   - **CRITICAL**: Do NOT fill Phases yet.

4. **Decompose into Phases (Chat Only)**
   - Present phase breakdown in chat:
     - Each phase: goal, scope (files/components), dependencies, estimated task count
     - Phases ordered by dependency (foundations first)
     - Target: ≤30-50 requirements per phase (within ~150-200 instruction limit)
   - Then ask ONE numbered question that stands on its own: name the epic and the number of phases being approved, and list the reply options — approve the split as presented, or say which phase to split, merge, or reorder. A bare "Approve?" or "Does this look right?" is a defect: it is unanswerable without scrolling back over the breakdown. STOP and wait for the answer.

5. **Detail Phases**
   - Write approved phases into the resolved epic file. Each phase contains:
     - Status (not-started / in-progress / done)
     - Prerequisites (which phases must be done first)
     - Goal (what this phase achieves)
     - Scope (files/components affected, target 1-5 files per task)
     - Tasks (numbered list of atomic, testable tasks)
     - Verification (specific commands/checks to confirm phase completion)
     - Notes (implementation hints, gotchas, references)

6. **Critique**
   - Present epic to user in chat and offer to critique it before finalizing.
   - If user agrees, critically analyze the epic for:
     - Missing phases or hidden dependencies
     - Tasks too large (should be split) or too small (should be merged)
     - Vague verification criteria
     - Missing non-goals or boundary gaps
     - Over-specification of trivial parts
   - Present critique in chat.

7. **Refine & Finalize**
   - Ask the user which critique points to address.
   - Update the resolved epic file with accepted improvements.
   - Update the metadata table Status from "Draft" to "Ready". (Frontmatter `status:` is auto-derived from DoD; do not change it manually.)

7a. **Write SRS-inline `**Tasks:**` Back-Pointer (FR-DOC-TASK-LINK)** — execute immediately, no permission needed. This is a write step.
   - For each FR-ID in the epic's `implements:` frontmatter, locate the heading `### <FR-ID>:` in the resolved `SRS`.
   - If the heading does not exist (new FR introduced by the epic), SKIP this FR and emit a chat note: "FR-XXX SRS section pending — task back-pointer deferred."
   - If the heading exists, find the section's `**Description:**` bullet. Look at the line(s) immediately following it.
     - If a `- **Tasks:** [...]` bullet already exists: append `, [epic-<name>](tasks/<YYYY>/<MM>/epic-<name>.md)` to the comma-separated list. Idempotent: skip if the exact link is already present.
     - If no `**Tasks:**` bullet exists yet: insert a new line `- **Tasks:** [epic-<name>](tasks/<YYYY>/<MM>/epic-<name>.md)` immediately AFTER the `**Description:**` bullet.
   - **Surgical edit only**: rest of the SRS file MUST remain byte-identical.

8. **TOTAL STOP**

</step_by_step>

## Output Format

```markdown
---
date: YYYY-MM-DD
status: to do
implements:
  - FR-XXX
tags: []
related_tasks: []
---
# Epic: {Feature Name}

| Field   | Value                       |
|---------|-----------------------------|
| Status  | Draft/Ready/In-Progress/Done |
| Created | YYYY-MM-DD                  |
| Updated | YYYY-MM-DD                  |

## Goal

{Why are we building this? Business/user value.}

## Overview

{Current state, why now, relevant context.}

## Non-Goals

<!-- Examples: "No backward compatibility with v1 API", "No UI changes in this phase", "No performance optimization", "No migration of existing data" -->
- {Explicit exclusion 1}
- {Explicit exclusion 2}

## Architecture & Boundaries

### Always (agent autonomy)

- {Things agent can always do}

### Ask First

- {Things requiring user confirmation}

### Never

- {Things agent must never do}

## Definition of Done

- [ ] {Measurable criterion 1}
- [ ] {Measurable criterion 2}

---

## Phase 1: {Name}

**Status:** not-started | **Prerequisites:** none

### Goal

{What this phase achieves.}

### Scope

- {file/component 1}
- {file/component 2}

### Tasks

1. {Atomic, testable task}
2. {Atomic, testable task}

### Verification

- [ ] {Specific check or command}

### Notes

- {Implementation hints, gotchas}

---

## Phase 2: {Name}

...
```

## Verification

<verification>
- [ ] ONLY the resolved epic file modified, plus optional surgical `**Tasks:**` line edits in the resolved `SRS` (FR-DOC-TASK-LINK), plus optional resolved `index` row updates.
- [ ] Frontmatter contains `date`, `status: to do`, `tags`, `related_tasks` keys
- [ ] For every FR-ID in `implements:` whose SRS section already exists, the corresponding `### FR-XXX:` section now carries a `- **Tasks:**` bullet linking to the epic file. Other SRS lines unchanged.
- [ ] Each phase has: Goal, Prerequisites, Scope, Tasks, Verification
- [ ] Non-Goals section is non-empty
- [ ] Boundaries (Always/Ask First/Never) are specified
- [ ] No phase exceeds 50 requirements
- [ ] Tasks target ≤5 files each
- [ ] All phases have dependency ordering (no circular deps)
</verification>
