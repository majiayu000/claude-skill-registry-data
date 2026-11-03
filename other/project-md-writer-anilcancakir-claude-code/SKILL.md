---
name: project-md-writer
description: "Write or audit a PROJECT.md (what, scope, constraints, decisions) for agents; commands and conventions go in AGENTS.md. Use when creating or updating a project overview doc, or when agents keep re-proposing ruled-out work."
---
<!-- ported-from: plugins/ac/skills/project-md-writer/SKILL.md sha256:4b5c234babe5c9930d0354f97254615c4066a8486765be7bf47b4ec1c61e76d4 -->

# PROJECT.md Writer

PROJECT.md answers three questions an agent cannot get from the code: what this project is for, what is in and out of scope, and which choices are already made. An agent reads it before it proposes or scopes work, then goes back to the code. This skill writes it, updates it, or audits an existing one, in the shape an agent reads best.

Scope: one file (or the split files the size rule names), plus one pointer line in the rules file. It does not edit code, README or CHANGELOG, and it does not write commands or conventions. Report adjacent problems instead of fixing them.

## Where it sits

| Layer | File | Loaded | Holds |
|---|---|---|---|
| Rules | AGENTS.md | every session | commands, conventions, off-limits; write it by hand |
| Why and scope | PROJECT.md | when an agent reads it | what, value, scope, constraints, decisions; a feature's PRD and roadmap from `/ac/product` feed its scope and non-goals |
| How it is built | ARCHITECTURE.md | when an agent reads it | architecture; route through the `architecture-md-writer` skill (DESIGN.md is how it looks, through the `design-md-writer` skill) |
| State | a notes or plan file | per task | progress and next steps |

PROJECT.md stays out of the always-loaded layer on purpose. opencode loads AGENTS.md into every agent in full at session start, and Anthropic's memory docs target under 200 lines per file because adherence drops as it grows. A pointer line with a trigger gives the agent the file when the task needs it and costs one line otherwise.

## Pick the mode

- No PROJECT.md exists: write.
- One exists and is mostly right: update in place, keep its headings.
- One exists and the user says agents ignore it, or its quality is unknown: audit first and report ranked findings with line numbers; edit only when the user asked for the fix.

If the content is commands or conventions, use AGENTS.md. If it is architecture, use ARCHITECTURE.md. If it is progress or a to-do list, use a notes file. If it is one feature's spec, use the `plan` skill.

## Workflow

### 1. Find what exists

`glob` `PROJECT.md`, `docs/PROJECT.md`, `.planning/PROJECT.md`; read the README and any AGENTS.md. Keep an existing location; otherwise use `docs/PROJECT.md`.

Success: you know the mode, the target path, and what AGENTS.md already says, so nothing gets duplicated.

### 2. Gather facts

Derive from the README, manifests, git log and code; use `ac/explore` when the repo is large. Ask the user only what the code cannot show: the core value, what is out of scope and why, each constraint's reason, the alternatives already rejected. Use the `question` tool in the user's language, one concrete guess as the first option, and finish everything else first.

If you cannot ask (a subagent or a non-interactive run), omit the section and list the open question in the report.

Success: every section has a source (code, the user's answer) or is deleted.

### 3. Write from the template

Read `assets/PROJECT.template.md` and fill it per the section contract below. `references/example.md` shows a filled one; match its register.

Success: no placeholder left, no empty section, target 100 lines or fewer.

### 4. Verify

`glob` every path you cited. Run or read the source for every version, limit and number. Remove what you cannot confirm; do not hedge it.

Success: each claim traces to a file, a command output or the user.

### 5. Wire the pointer

Add one line to AGENTS.md if none points here: "Before proposing or scoping work, read <target path>." Use a plain path, not an `@import`. Skip it when a pointer exists.

Success: `grep -n PROJECT.md` on the rules file finds the line.

## Section contract

| Section | Holds | Rule |
|---|---|---|
| What this is | Two or three sentences: what it does, for whom | Plain nouns, no marketing |
| Core value | One sentence | The tiebreaker when scope conflicts |
| Scope, Active | Capabilities in flight or maintained | One line each; a maintained capability stays, a finished one-off moves to CHANGELOG |
| Scope, Out of scope | Excluded items | Each has its reason and a revisit condition; this is what stops agents re-adding them |
| Constraints | Hard limits | `Type: limit. Why: reason.` A constraint without its reason gets questioned or broken |
| Context | Facts the code cannot show | One fact per bullet; never a tour of the code |
| Decisions | Choices that bind later work | Reason plus rejected alternatives; Status is Active, Revisit or Superseded |
| Where to look | Pointers | Paths only, one line each |
| Last reviewed | Date and trigger | Stamp on every edit |

## Rules

- Record only what code, git history and the README do not already show. Test each line: would an agent make a wrong change without it? If not, cut it.
- State what is true now. No aspirations ("we aim for"), no marketing, no progress or status; volatile state goes in a notes file, because a stale doc is worse than none.
- Be checkable: name paths, versions, limits. "Fast" and "scalable" tell an agent nothing.
- Anchor to paths or symbol names, never line numbers; they survive edits.
- Give each fact one home. If AGENTS.md or ARCHITECTURE.md holds it, point there.
- Keep the headings exactly as in the contract, so agents can grep them. Prefer bullets and tables to paragraphs.
- State a rule once with its reason. No capitals for emphasis.
- Write in the project's documentation language, English by default.
- At more than 15 Decisions rows, move the table to `docs/decisions.md` and leave a pointer.

## Update rules

Run these after a milestone or a scope change:

1. Finished one-off: remove it from Active; CHANGELOG records it. A capability the project still maintains stays.
2. Dropped or invalidated item: move it to Out of scope with the reason.
3. New work: add to Active.
4. New binding choice: add a Decisions row. A reversed choice marks the old row Superseded and adds the new one.
5. Re-read What this is and Core value; edit only if reality drifted.
6. Update the Last reviewed stamp.

## Audit checklist

- Every cited path exists.
- No line duplicates AGENTS.md or ARCHITECTURE.md.
- Out of scope items each carry a reason.
- Constraints each carry a reason.
- No status, progress or aspiration lines.
- Under 100 lines, or the excess is justified in the report.
- A pointer from the rules file exists.
- The stamp is within the last milestone.

## References

| File | Load when |
|---|---|
| `assets/PROJECT.template.md` | Writing or restructuring the file |
| `references/example.md` | Matching register and level of detail |

Basis for the format: Anthropic's memory docs (`https://code.claude.com/docs/en/memory.md`: size, structure, concrete instructions), Anthropic's context engineering article (`https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents`: smallest set of high-signal tokens, lightweight pointers loaded just in time), and the GSD PROJECT.md template (core value, out of scope with reasons, constraints with reasons, key decisions). The rejected-alternatives column and the pointer-instead-of-import wiring are this skill's own additions.
