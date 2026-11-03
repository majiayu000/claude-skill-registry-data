---
name: architecture-md-writer
description: "Write or audit an ARCHITECTURE.md for agents: boundaries, invariants with verify commands, flows and a change guide."
when_to_use: "Use when creating or updating the architecture doc, or when agent changes keep landing in the wrong place; a UI style spec is ac:design-md-writer."
---

# ARCHITECTURE.md Writer

ARCHITECTURE.md tells an agent what it cannot work out by reading the code: where the boundaries sit, which rules must hold, how the main flows cross modules, why a choice was made, and which places move together for a given change. An agent reads it before it changes structure, then goes back to the code. This skill writes it, updates it, or audits an existing one.

Scope: one file (or the split files the size rule names), plus one pointer line in the rules file. It does not edit code, README or CHANGELOG, and it does not write the project's why and scope (`ac:project-md-writer`), its commands and conventions (`ac:claude-md-rules-creator`) or how a UI looks (`ac:design-md-writer`, which owns DESIGN.md). Report adjacent problems instead of fixing them.

## Why the file is thin

Three sources decide the shape, and the first two argue against the file most people picture.

- Claude reads the repository itself. Anthropic's best-practices page lists "describe your architecture and file layout in CLAUDE.md" as advice that is gone, and its memory page says `/doctor` cuts "directory layouts, dependency lists, and architecture overviews" while keeping "pitfalls, rationale, and conventions that differ from tool defaults".
- A 2026 study of context files (arXiv 2602.11988) found that they did not generally raise task success, added over 20 percent inference cost, and that repository overviews were not helpful. Files written by a model did worse than files written by developers.
- matklad's essay and rust-analyzer's document show what survives: a short codemap of the modules whose boundaries are not obvious, invariants (many of them absences), and the cross-cutting rules.

So the file records only what code and git history do not show, and every line is checked against the code. A model writes this file, which is the case the study measured as weakest: take facts from files you opened or from the user, never from inference.

## Line test

Keep a line only when it passes both questions.

1. Would an agent put a change in the wrong place, or break a rule, without it?
2. Is it out of reach of two or three opens (a directory listing, imports, signatures, a schema, the README)?

## Decide first

Write the file only when the project has real internal boundaries: roughly 10k lines or more, or several modules that depend on each other in a way the names do not show. For a handful of files the README and CLAUDE.md carry everything; say so and stop. When no section would survive the line test, the file does not exist.

## Which ARCHITECTURE.md

- Default: `ARCHITECTURE.md` at the repository root, the name tools and contributors look for. Keep an existing location.
- An existing `DESIGN.md` that describes architecture is the old home. DESIGN.md now means the visual-identity file that `ac:design-md-writer` owns. Propose `git mv DESIGN.md ARCHITECTURE.md` with `AskUserQuestion` and do not rename unasked; a DESIGN.md that opens with YAML tokens is the visual file and stays.

## Where it sits

| Layer | File | Loaded | Holds |
|---|---|---|---|
| Rules | CLAUDE.md, AGENTS.md | every session | commands, conventions, off-limits |
| Why and scope | PROJECT.md | when read | what, scope, constraints |
| How it is built | ARCHITECTURE.md | when read | boundaries, invariants, flows, change guide |
| How it looks | DESIGN.md | when read | UI tokens and rationale |

ARCHITECTURE.md stays out of the always-loaded layer. Claude Code loads every CLAUDE.md from the working directory upward in full at launch, and an `@import` loads together with the file that imports it, so it costs the same. A pointer line with a trigger is the cheaper wiring.

## Pick the mode

- No architecture doc exists: write.
- One exists and is mostly right: update in place, keep its headings.
- One exists and agents ignore it, or its quality is unknown: audit first and report ranked findings with line numbers; edit only when the user asked for the fix.

## Workflow

### 1. Find what exists

Glob `ARCHITECTURE.md`, `docs/ARCHITECTURE.md`, `docs/architecture*` and `DESIGN.md` (check which kind it is). Read the README, PROJECT.md and CLAUDE.md. Read `git log --stat` for the last 30 or so commits: the files that move together are the raw material of the Change guide.

Success: you know the mode, the target path and what other files already say.

### 2. Map the code

Open the entry points, the module boundaries, the schema and the tests. Use `ac:explore` for a large repository and LSP for symbol-level questions. Never describe a component you have not opened. Ask the user, with `AskUserQuestion` in their language and your best guess first, only what the code cannot show: why a boundary sits where it does, which alternatives were rejected, which places mislead.

If you cannot ask (a subagent or a non-interactive run), omit what only the user knows and list the open question in the report. Never invent a reason.

Success: you can name each module's responsibility, boundary and dependencies from files you read.

### 3. Write from the template

Read `${CLAUDE_SKILL_DIR}/assets/ARCHITECTURE.template.md` and fill it per the section contract. `${CLAUDE_SKILL_DIR}/references/example.md` shows a filled one; match its register. Delete a section that has nothing passing the line test.

Success: no placeholder left, no filler section, 150 lines or fewer for most projects.

### 4. Verify

Glob every path you cited, Grep every symbol, and run or read every command in the Verify column. Delete what you cannot confirm, then run the line test on what is left.

Success: each claim traces to a file, a symbol or a command output.

### 5. Wire the pointer

Add one line to the rules file if none points here: "Before changing module boundaries or a main flow, read ARCHITECTURE.md; update it in the same change when a boundary, flow or invariant moves." Put it in CLAUDE.md when one exists; use AGENTS.md only when the project has no CLAUDE.md, because Claude Code reads only the CLAUDE.md files when both exist. Use a plain path, not an `@import`.

Success: `grep -n ARCHITECTURE.md` on the rules file finds the line.

## Section contract

| Section | Holds | Rule |
|---|---|---|
| Overview | Three to six sentences on the shape the directory names do not show: a rule that holds everywhere, a pipeline, a plug-in point; a text diagram only for such a shape | Subject to the line test like every section; a layer list that repeats the directory names goes; under 15 lines of diagram |
| Codemap | One entry per module whose boundary the name does not show: what it owns, what it must not do, what it depends on | A map of a country, not an atlas of its states: name modules and types in backticks, do not link, do not list files, omit self-evident modules |
| Invariants | Rule, why, how to verify; many are absences ("the model layer does not import views") | The verify column is a test name or a command that runs; a rule local to one module stays in its Codemap entry |
| Flows | The two or three main paths, as numbered steps | Each step names `path` or `path:symbol`, never a line number |
| Decisions | Choice, why, rejected alternatives, status | Product and scope choices live in PROJECT.md; a long decision links to its ADR file |
| Change guide | Task, files to touch, coupled places to check | The section agents use most; write it from real changes in the git log |
| Cross-cutting | Errors, configuration, concurrency, testing: the contract in two to five lines | Only what differs from the framework default |
| Traps | Places where the code misleads, and unfinished seams | One line each with the path; remove it when fixed |
| Glossary | Terms whose domain meaning differs from the name in code | Only when they collide; otherwise omit |
| Last reviewed | Date and trigger | Stamp on every edit |

## Rules

- Document what the code does not show. Directory trees, dependency lists, signatures and schema are already readable; point to the schema file instead of copying it.
- State what is true now. No aspirations, no roadmap, no progress; a stale doc is worse than none.
- Anchor to paths and symbol names, never line numbers.
- Give each fact one home. Point to PROJECT.md, the config or the schema instead of copying.
- Keep the headings exactly as in the contract, so agents can grep them. Prefer tables and numbered steps to paragraphs.
- State a rule once with its reason. No capitals for emphasis.
- Over 200 lines, split by area into `docs/architecture/<area>.md`. The root file keeps Overview, Invariants, Decisions, the Change guide and one linked line per area. The memory-file hook blocks a growing file above 300 lines (`AC_ARCHITECTURE_MD_MAX_LINES`).
- Write in the project's documentation language, English by default.

## Update rules

Update ARCHITECTURE.md in the same change as the code when a change:

1. Moves a boundary or a dependency between modules, or adds or removes a module that has one.
2. Alters a main flow.
3. Breaks or adds an invariant.
4. Makes a Change guide row wrong.

Then refresh the Last reviewed stamp. A change that touches none of these needs no edit; the file is revisited, not synchronised line by line.

## Audit checklist

- Every cited path and symbol exists, and every Verify entry runs.
- Every line passes the line test; none repeats the README, CLAUDE.md or the code.
- The Codemap lists no files and no self-evident module.
- The Change guide covers the last few real changes in the git log.
- No decision also lives in PROJECT.md; no status, roadmap or aspiration lines.
- 200 lines or fewer, or split.
- A pointer from the rules file exists.
- A project below the "Decide first" bar has no ARCHITECTURE.md.

## References

| File | Load when |
|---|---|
| `${CLAUDE_SKILL_DIR}/assets/ARCHITECTURE.template.md` | Writing or restructuring the doc |
| `${CLAUDE_SKILL_DIR}/references/example.md` | Matching register and level of detail |

Basis, checked 2026-11-01: matklad's essay (`https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html`: codemap, invariants, cross-cutting concerns, keep it short, revisit rather than synchronise), rust-analyzer's document (`https://github.com/rust-lang/rust-analyzer/blob/84e25a76a6bb077783fd5218c89f2fc8b0f392b7/docs/book/src/contributing/architecture.md`: an `Architecture Invariant` marker per rule), Anthropic's best-practices and memory pages (`https://code.claude.com/docs/en/best-practices.md`, `https://code.claude.com/docs/en/memory.md`) and the context-file study (`https://arxiv.org/abs/2602.11988`). The Verify column, the Change guide, the Traps section and the update-in-the-same-change rule are this skill's own additions; no source prescribes them.
