---
name: docs-architect
version: 1.0.0
description: Project documentation system — a folder-per-doc-type docs/ tree (ADRs, backlog, ideas, plans, designs, reviews, changes, guides), mandatory frontmatter, lifecycle by moving files, weekly/monthly routine, and a stdlib linter. Scaffold, write-doc and migrate modes. Use when setting up docs/, writing a plan/design/ADR/review, triaging a backlog, or reorganizing an existing docs folder.
---

# Docs Architect

A `docs/` convention where **the folder is the doc type, the frontmatter is the state, and moving a file is a state change**. One source of truth per item and per decision. Companion to [grill-with-docs](../grill-with-docs/SKILL.md) (owns `CONTEXT.md` and the ADR *threshold*) and [feature-planner](../feature-planner/SKILL.md) (produces the plans this tree stores). Schemas in [FRONTMATTER.md](FRONTMATTER.md), backlog rules in [BACKLOG.md](BACKLOG.md), templates in [TEMPLATES.md](TEMPLATES.md), the classify/migrate procedure in [MIGRATION.md](MIGRATION.md).

Suggestion-mode: the tree is a default. Adopt the folders a project actually needs.

## 1. Modes

- **Scaffold** — no `docs/` yet. Create `docs/README.md` and `docs/templates/`; create every other folder lazily, when its first doc exists.
- **Write-doc** — pick the folder by the doc's job ([§2](#2-where-a-doc-goes)), copy the template, fill the frontmatter, link it to its origin.
- **Migrate** — a `docs/` exists in another shape. Classify, propose moves and renames, wait for approval, then move ([MIGRATION.md](MIGRATION.md)).

## 2. Where a doc goes

| Folder | Job | Name | Edited after writing? |
|---|---|---|---|
| `adr/` | One decision: context, options, decision, consequences | `0001-slug.md` | Body never; `status` and `superseded_by` only |
| `ideas/` | Not yet a plan | `YYYY-MM-DD-project-topic.md` | Yes, while `draft` |
| `plans/` | Scope, phases, exit criteria | dated | Yes |
| `designs/` | How it is built; links ADRs instead of repeating them | dated | Yes |
| `reviews/` | Findings of one review or audit — a snapshot | dated | No |
| `changes/` | What changed and why — migrations, impact | dated | No |
| `guides/` | Current procedures and runbooks | `topic.md` | Yes, always current |
| `methodology/` | Working rules and standards | `topic.md` | Yes |
| `backlog/` | `inbox.md`, `<project>.md`, `done/YYYY-MM.md` | see [BACKLOG.md](BACKLOG.md) | Yes |
| `archive/` | Finished or obsolete | keeps its name | No |

`guides/` and `methodology/` are living documents and carry no date; everything else describes a moment and does. Reviews and changes are history — never rewrite them, add a new one.

## 3. Flow

`inbox` → `ideas` → `plans` → `designs` → `adr` (only if a real architecture decision) → backlog `Next` → `Doing` → `done/`. Reviews and changes feed new backlog items, each linked to its origin.

1. Capture in `backlog/inbox.md`, one line, no format.
2. Weekly triage: drop it, move it to a project backlog, or grow it in `ideas/`.
3. A mature idea becomes a plan with scope and exit criteria.
4. The plan yields a design; each non-trivial decision becomes an ADR.
5. The approved design leaves linked items in `Next`.
6. On close the item moves to `done/YYYY-MM.md`; the doc becomes `status: done`, then moves to `archive/`.

## 4. ADRs

- One decision per ADR, one page: Context, Options considered, Decision, Consequences.
- Numbering is sequential and never reused. Take the next number by scanning `adr/`.
- Whether something deserves an ADR is decided by the three-part test in [ADR_FORMAT.md](../grill-with-docs/ADR_FORMAT.md) (hard to reverse, surprising, real trade-off). This skill adds the mandatory frontmatter and the supersede mechanics on top of it.
- Changing a decision: write a new ADR with `supersedes: N`, then set the old one to `status: superseded` and fill its `superseded_by`. That is the only edit an accepted ADR gets.
- ADRs are cross-cutting: a decision spanning projects uses `project: global`. Keep `adr/` flat — the number already orders it.
- Designs link ADRs (`[ADR 0002](../adr/0002-slug.md)`) instead of restating the reasoning.

## 5. Links and frontmatter

Every doc except `README.md`, `inbox.md` and `templates/` carries frontmatter ([FRONTMATTER.md](FRONTMATTER.md)): `status`, `project`, `date`, `related`. ADRs use their own schema.

- Use **relative markdown links** (`../adr/0003-slug.md`). They resolve on GitHub, in editors and for agents. Wikilinks only if the project already standardises on an Obsidian-style vault.
- `related` lists paths relative to `docs/`. A doc nothing links to is an orphan; the linter reports it.

## 6. Routine

| When | What | Time |
|---|---|---|
| Daily | Capture in `inbox.md` | 0 |
| Weekly | Triage the inbox; review `Next` | 10 min |
| Monthly | Prune `Later`, close to `done/`, archive obsolete, resolve drafts older than 2 months | 15 min |

A draft older than 2 months is promoted or deleted. A backlog item sitting in `Later` for 2–3 months is deleted or demoted to `Someday` — prune, don't archive. If the project tracks work in GitHub Issues, the backlog lives there and only the docs stay here.

## 7. Scale rules

- A per-project subfolder inside a type (`designs/<project>/`) only after ~10 files of that type. Never for `adr/`.
- Several repos: `docs/` per repo by default; a central docs repo only when projects cross-reference heavily. Then `project:` is mandatory and filters the views.
- Keep `CLAUDE.md` / `AGENTS.md` short and pointing at `docs/` — snippet in [TEMPLATES.md](TEMPLATES.md#agent-pointer-section). Do not duplicate the conventions there.

## 8. Linter

`python3 scripts/docs_lint.py [docs-dir]` — stdlib only, read-only, exit code 1 on errors. Checks frontmatter schema and enums, ADR numbering and supersede symmetry, broken relative links, orphans, drafts older than 60 days, backlog size limits. `--index` prints a generated index to stdout. Run it before declaring a docs change done and in the monthly routine.

## 9. Output naming

Docs this skill generates use kebab-case, lowercase, no accents: `0004-use-nats.md`, `2026-10-20-agent-verification.md`, `inbox.md`. The skill's own support files stay `UPPER_SNAKE_CASE`.

## 10. Out of scope

- **`CONTEXT.md` glossary and when to offer an ADR** → [grill-with-docs](../grill-with-docs/SKILL.md)
- **Requirement → design → slices** → [feature-planner](../feature-planner/SKILL.md)
- **Commit messages and `CHANGELOG.md` wording** → [commit-author](../commit-author/SKILL.md)
- **Root `README.md` / `CHANGELOG.md` authoring** — the user-facing entry points are not generated here; `changes/` entries may link a changelog line.
