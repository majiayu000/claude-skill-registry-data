---
name: scaffold-exercises
description: Scaffold course exercise directories with numbered sections, exercise variants, required readmes, and repo-specific validation. Use when creating exercise stubs, adding a course section, or safely renaming exercises.
---

# scaffold-exercises

Create course exercise directory structures that match the owning repository's documented conventions, then validate them with that repository's configured checks.

## When to use

- User asks to scaffold exercises, exercise stubs, or a new course section.
- User provides a course plan with numbered sections and exercises.
- User wants to move, renumber, or rename exercise directories safely.

## Before scaffolding

1. Read local repo guidance first: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, course docs, and any existing exercise README conventions.
2. If the work is tracked, inspect the bead with `bd show <id>` and add a concise `worklog:` comment before broad filesystem edits.
3. Inspect existing `exercises/` structure and naming before creating new directories.
4. Confirm the owning repo's validation command. Use `pnpm ai-hero-cli internal lint` only when that repo documents it; otherwise use the local lint, test, or validation script.

## Directory naming

- Sections live under `exercises/` as `XX-section-name/`, for example `01-retrieval-skill-building/`.
- Exercises live inside a section as `XX.YY-exercise-name/`, for example `01.03-retrieval-with-bm25/`.
- Section number is `XX`; exercise number is `XX.YY`.
- Names are dash-case: lowercase words separated by hyphens.
- Preserve the numbering in the source plan unless the user explicitly asks to resequence.

## Exercise variants

Each exercise needs at least one variant subfolder:

- `problem/` - student workspace or prompt material.
- `solution/` - reference implementation or answer.
- `explainer/` - conceptual material with no student work required.

When the plan does not specify variants, default to `explainer/`. If the source course uses numbered explainer variants such as `explainer.1/`, follow the local pattern.

## Required files

Each created variant folder needs a `readme.md` that:

- Is not empty.
- Has a meaningful title and short description.
- Avoids broken links.
- Avoids repo-level TODO-list artifacts such as `TODO.md` files or stray code TODO comments. Student-facing exercise prompts are fine when the course format expects them.

Minimal stub:

```md
# Exercise Title

Description here.
```

If a variant contains code, add a `main.ts` only when the owning repo or exercise format requires it. For stub-only exercises, a readme-only variant is acceptable unless local validation says otherwise.

## Scaffold workflow

1. Parse the plan for section names, exercise names, exercise numbers, and variant types.
2. Map names to dash-case paths without changing numeric prefixes.
3. Preview the paths before writing when the scaffold touches multiple exercises.
4. Create only the requested directories and variant folders.
5. Add one `readme.md` per variant with a title and description.
6. Add `main.ts` only for variants that need executable code.
7. Run the owning repo's documented validation command and fix reported issues.
8. Add a `worklog:` comment summarizing what was scaffolded when the work is tracked in Beads.

## Validation checklist

Use the repo's own checks. Typical validation looks for:

- Each exercise has at least one expected variant folder such as `problem/`, `solution/`, `explainer/`, or a documented numbered explainer variant.
- Required `readme.md` files exist and are non-empty.
- README links resolve.
- Generated placeholder files such as `.gitkeep` are not present unless local docs explicitly require them.
- Undocumented files such as `speaker-notes.md` are not introduced.
- README commands match the owning repo's current scripts.
- `main.ts` exists only where required and contains more than a placeholder line when validation expects executable code.

Example conditional command selection:

```bash
# If documented by the owning repo:
pnpm ai-hero-cli internal lint

# Otherwise use local repo checks, for example:
bun run lint
bun run test
pnpm test
```

## Moving or renaming exercises

When renumbering or moving exercises:

1. Use `git mv` for tracked directories so history follows the rename.
2. Update numeric prefixes to maintain the section and exercise order.
3. Update references, links, imports, indexes, manifests, and course navigation that mention the old path or title.
4. Run the owning repo's validation command after the move.
5. Record the rename in a Beads `worklog:` comment when the work is tracked.

Example:

```bash
git mv exercises/01-retrieval/01.03-embeddings exercises/01-retrieval/01.04-embeddings
```

## Example: stubbing from a plan

Given:

```text
Section 05: Memory Skill Building
- 05.01 Introduction to Memory
- 05.02 Short-term Memory (explainer + problem + solution)
- 05.03 Long-term Memory
```

Create:

```text
exercises/05-memory-skill-building/05.01-introduction-to-memory/explainer/readme.md
exercises/05-memory-skill-building/05.02-short-term-memory/explainer/readme.md
exercises/05-memory-skill-building/05.02-short-term-memory/problem/readme.md
exercises/05-memory-skill-building/05.02-short-term-memory/solution/readme.md
exercises/05-memory-skill-building/05.03-long-term-memory/explainer/readme.md
```

The `05.02-short-term-memory` exercise gets all three requested variants; the others default to `explainer/`.
