---
name: git-flow
description: The git working method for this repo — branch, commit, and PR routine. Use before committing, branching, merging, or opening a pull request.
---

# Git flow — the working method

All work reaches `main` through pull requests. Never commit or merge
directly on `main`, never force-push, never rewrite pushed history
(root CLAUDE.md hard rule 4 — a hook enforces the main/force-push part).

## Branch

- One branch per coherent piece of work, prefixed by kind:
  `feat/`, `fix/`, `chore/`, `docs/` (e.g. `feat/button-razor-renderer`).
- Branch from up-to-date `main`.

## Before committing

- `dotnet build TsugiteUmbraco.slnx` builds clean, and `dotnet test
  TsugiteUmbraco.slnx` passes once test projects exist.
- If the client changed: `npm run typecheck` and `npm run build` in
  `src/TsugiteUmbraco.Web/ClientApp`.
- If the work changed a component contract, the rendered DOM is checked
  against Tsugite's conformance suite for that component.

## Commit

- Stage explicitly — name the files or directories. Never `git add -A` or
  `git add .`.
- Narrative messages in English: a subject that states what and why,
  body only when the subject cannot carry the reasoning alone.
- One argument step per commit — split unrelated movements.
- **No people in the record.** Commit messages and PR bodies describe
  the change and its argument, never who asked for it or who did it, and
  never in the first person. Authorship is what the commit metadata is for.

## Pull request

- Open with `gh pr create` against `main`; the body summarizes the
  argument of the branch, not the file list — and, as in commits, names
  no one and says nothing in the first person.
- Merge happens on GitHub, never locally into `main`.
