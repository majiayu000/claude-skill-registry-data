---
name: civiltekk-git-commits-skill
description: >-
  Conventional Commits and compact-commit budgets — type, scope, breaking
  changes, semver guidance, atomic-commit granularity by layer; 72-char
  subject, 150-word body, semantic grouping. Triggers: commit and push,
  make a commit, write a commit message, commit message format, semantic
  commit, compact commit, concise commit, terse commit. Not for release
  pipelines (semantic-release-convention-skill).
license: Apache-2.0
compatibility: opencode
category: Git/Workflow
---

Consolidates git-semantic-commits-skill + git-compact-commits-skill (#603).

## What I do

Write, format, or tighten commit messages to this config's commit doctrine:

1. **Detect the route** (§Routes) — explicit > inferred > ask-once.
   Explicit: the request names the concern ("semantic commit", "commit
   message format" → `conventional-format`; "compact", "concise",
   "terse" → `brevity-budget`). Inferred: the complaint shape (wrong
   type/scope/breaking notation → `conventional-format`; running long,
   word-count over budget, squash output → `brevity-budget`). Ambiguous
   ("make a commit") → ask once — one ask per run, then proceed on the
   answer.
2. **Load the route's values file** (`references/semantic.md` /
   `references/compact.md`) and apply its contract.
3. Most real commits need both files' values — format from `semantic.md`,
   budgets from `compact.md`; the route only decides which file leads.

## Side files (load rules)

| Read | When | Use |
|------|------|-----|
| `references/semantic.md` | route `conventional-format` | Conventional Commits format (types, scope, subject, footers, `!` / `BREAKING CHANGE:`), semver mapping, atomic-commit granularity by layer, project overrides |
| `references/compact.md` | route `brevity-budget` | length budgets (72-char subject, 150-word body), semantic grouping, compact writing techniques, commitlint enforcement |

Side files carry VALUES only; this file carries the METHOD. A commit
concern outside formatting/brevity (release PR titles, merge strategy,
release tags, GitHub Actions) is not this skill's space — route it to
`semantic-release-convention-skill` instead of improvising.

## Routes

| Situation | Route |
|-----------|-------|
| "commit and push", "make a commit", "write a commit message", "commit message format", "semantic commit"; wrong type/scope/breaking notation | `conventional-format` |
| "compact commit", "concise commit", "terse commit"; commits running long; squashing a branch into one message; tightening commitlint rules | `brevity-budget` |
| Ambiguous ("fix this commit message") | ask once (§What I do step 1), then route |

## Boundaries

- The two routes were formerly peer skills that cross-referenced each
  other as alternatives ("not for brevity" / "owns types and scopes") —
  that boundary is internal now; the route table above is the boundary
  logic.
- Release pipeline conventions (PR titles, merge strategy, release tags,
  GitHub Actions) → `semantic-release-convention-skill`.
- Project `AGENTS.md` and `.commitlintrc*` / `commitlint.config.*`
  override every default in the values files — always check the project's
  AGENTS.md first.

## Agent behavior rules

- One ask per run maximum (route detection); headless/CI: no asks —
  infer from the request, defaulting to `conventional-format`
  (formatting is the superset concern; budgets apply inside it).
- Never mix style-only changes with logic in one commit; each commit
  compiles and passes tests on its own (granularity doctrine lives in
  `references/semantic.md`).

> **Harness binding — interactive asks** (AGENTS.md §Portability contract):
> OpenCode — `question` tool. Claude Code — `AskUserQuestion`. Other/none —
> ask in a plain reply; headless/no-answer rule above applies.
