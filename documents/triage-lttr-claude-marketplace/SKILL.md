---
name: triage
description: Triage requirements, specs, or tickets. Detect input (pasted text, markdown path, tracker ticket id/URL, or empty prompt). Explore codebase + docs, score completeness, ask clarifying questions, write a markdown report. Trigger when user says "triage", "review this spec", "is this requirement complete", or provides a ticket/spec to assess.
disable-model-invocation: true
---

# Triage

Analyze requirements for completeness. Explore code + docs, surface gaps, ask clarifying questions, write a report.

Tracker-agnostic and storage-agnostic: fetching a ticket, searching docs and choosing where the report lands are all pluggable (see `references/sources.md`). A tracker or a doc source can be a CLI, a connected server, or plain files in the repo.

## Arguments

`$ARGUMENTS` is a space-separated string. Parse optional flags first, then treat the remainder as the input.

| Flag             | Meaning                                          |
| ---------------- | ------------------------------------------------ |
| `--ticket <id>`  | Ticket / work-item id (label + fetch hint).      |
| `--name <title>` | Override inferred report title.                  |
| `--out <path>`   | Write report to this path; skip the save prompt. |
| `--print`        | Print report to stdout; skip the save prompt.    |

Wrappers may pre-pin any of these — user-passed flags WIN.

## Input Detection

After flags are stripped, the remainder selects the requirement source:

| Form                          | Source                          |
| ----------------------------- | ------------------------------- |
| empty                         | prompt user to paste / describe |
| path ending `.md`             | local markdown spec file        |
| bare id (`12345`, `PROJ-42`)  | tracker ticket → see below      |
| URL pointing at an issue/item | tracker ticket → see below      |
| anything else                 | treat as pasted text            |

Ambiguous → ask. Do NOT guess.

## Workflow

### 1. Resolve input

#### empty

Prompt: "Paste requirements / spec text, or give a ticket id, URL, or .md path."

#### `.md` path

Read file. Use content as input. Title from H1 or filename.

#### pasted text

Use as-is. Derive title from first line / sentence.

#### tracker ticket

Read `references/sources.md` and use the first available fetch path. The tracker may be a CLI, a connected server, or files in this repo. Never invent a CLI invocation, a file layout, or an API call — if nothing is available, ask the user to paste the ticket text.

Normalize whatever comes back to: title, description, acceptance criteria, state, type, assignee, area/labels, linked items. HTML descriptions → readable text.

### 2. Explore codebase + docs

#### Codebase (Explore agent)

- Project structure / architecture
- Existing code that would be modified
- Patterns and conventions
- Related features
- Test coverage patterns

#### Local docs

`docs/`, `documentation/`, `wiki/`, `README.md`, `CONTRIBUTING.md`, `ARCHITECTURE.md`, OpenAPI specs, ADRs, `GLOSSARY.md` (or `GLOSSARY-MAP.md`), inline code comments.

#### External docs (optional)

If a docs search tool is connected (see `references/sources.md`), search it for related material: by title keywords, by feature / area name, by domain terms from the description, plus any terms in `$ARGUMENTS`. Look for technical specs, ADRs, related-feature docs, business rules, prior decisions.

No such tool → skip silently, note it in the report only if a gap seems doc-shaped.

### 3. Assess completeness

| Dimension               | Questions                               |
| ----------------------- | --------------------------------------- |
| **Problem clarity**     | Goal stated? Why needed?                |
| **Scope**               | In scope? Explicitly out?               |
| **User impact**         | Who benefits? Journey affected?         |
| **Acceptance criteria** | Done definition? Success metrics?       |
| **Edge cases**          | Errors? Empty states? Boundaries?       |
| **Technical scope**     | Components/files affected? API changes? |
| **Dependencies**        | Blocked by? Coordination?               |
| **Non-functional**      | Performance? Security?                  |
| **Data**                | Schema? Migration?                      |
| **UX/UI**               | Designs? Patterns?                      |

Rate: **Ready** / **Mostly Ready** / **Needs Clarification** / **Underspecified**.

### 4. Generate questions

Categories:

1. **Blockers** — must answer before any work
2. **Scope clarification** — boundaries
3. **Technical decisions** — implementation
4. **Nice to know** — non-blocking

### 5. Ask interactively

Ask the user interactively. 1–4 questions per batch, 2–4 suggested options each. Record answers. Unanswered → output file.

### 6. Write output

`{date}` = `YYYY-MM-DD`. `{slug}` = with ticket: `<ticket-id>-<slugified-title>`, else `<slugified-title>`. Slugify: lowercase, spaces→hyphens, strip special chars, max 40 chars.

Destination, in order:

1. `--print` set → print markdown to stdout. Done.
2. `--out <path>` set → write there.
3. Project has an artifact convention (a protocol skill covers it, or an existing folder of reports makes it obvious) → follow it. See `references/sources.md`.
4. Otherwise ask the user:
   1. Print only (no save) — default
   2. Save to `/tmp/triage-{slug}.md`
   3. Other path

## Output Format

```markdown
# Triage: [Short title]

**Source**: [Ticket id/URL, file path, or "Manual input"]
**Date**: [YYYY-MM-DD]
**Completeness**: [Ready | Mostly Ready | Needs Clarification | Underspecified]

## Summary

[1-sentence summary]

### Understanding

[2-3 sentences from codebase exploration]

### What's Clear

- ...

### Implicit Requirements (from docs)

- [Reqs found in docs that the requirement assumes but doesn't state]

### Gaps Identified

- ...

### Questions

#### Blockers

1. [Question] — [Why it blocks]

#### Scope Clarification

1. ...

#### Technical Decisions

1. ...

#### Nice to Know

1. ...
```

Only unanswered questions go in output.

### 7. Summary to user

- Destination (path, or "printed")
- Completeness rating
- Blocker count

## Tips

- Don't ask what code/docs already answer — explore first
- Surface implicit requirements from docs — tickets assume documented knowledge
- 3 critical questions > 10 nice-to-haves
- Frame to unblock decisions, not gather trivia
- Docs contradict ticket → blocker question

## Notes

- Read-only against the tracker. Never updates ticket state — that's `dev-azdo:ticket` (if the `dev-azdo` plugin is installed) or the platform CLI.
- Tracker and docs recipes live in `references/sources.md` — load only when the input is a ticket or a docs search is wanted.
- Division of labor with `aiwork-protocol`: **`aiwork-protocol` decides where the artifact lands; `triage` decides what goes in it.** Both trigger on "triage" — if the user wants a report written, that's this skill.
