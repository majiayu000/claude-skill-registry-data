---
name: adapt-to-project
description: Fit this Claude Code template to the repository it was copied into by filling .claude/project.env, AGENTS.md, the conventions docs and their rule loaders, and the architecture, security and glossary docs, then pruning skills and agents the project cannot use.
argument-hint: "Optional focus, e.g. 'only the API conventions' or 're-run after adding a frontend'"
disable-model-invocation: true
---

# Adapt to project

The template ships stack-agnostic: every project-specific slot carries a `TODO(adapt)` marker, and every hook no-ops until `.claude/project.env` names a command. This skill turns the skeleton into this project's config. It is re-runnable: fill only what is still `TODO(adapt)` or what the focus argument names, and never overwrite filled content without asking.

**Facts come from the code; decisions come from the user.** Never invent a convention, a rationale, or a security property. What the code cannot tell you becomes a question, or stays a `TODO(adapt)` the report lists as deferred.

## 1. Inventory

1. Confirm you are in a worktree on a feature branch (see `AGENTS.md` §Git workflow).
2. List the open slots: `grep -rn "TODO(adapt):" --exclude-dir=node_modules --exclude-dir=.worktrees --exclude-dir=adapt-to-project .` (the colon form marks a slot; the bare form is a mention).
3. If the repo already had its own `CLAUDE.md`, `AGENTS.md`, `.cursor/rules`, `CONTRIBUTING.md` or style guide, those are primary sources: merge their content into the template files, never discard it.

## 2. Survey

Delegate to an `Explore` subagent on a large repo so file dumps stay out of context. Establish:

- **Stack and package manager**: manifests and lockfiles (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle`, `Gemfile`, ...).
- **Real commands**: lint, format, typecheck, test, install, dev, codegen, migrations. CI workflows and task runners (`Makefile`, `justfile`, `package.json` scripts) show what the team actually runs.
- **Areas**: top-level layout, workspace members, and the boundaries where rules change (API, database, frontend, workers, infra).
- **Generated code**: codegen configs, `generated/` directories, protobuf/OpenAPI outputs.
- **Patterns**: read 5-10 representative source files per area and 3-5 tests. Note naming, layering, error handling, logging and test layout that recur. A pattern the code breaks more often than it follows is not a convention; ask instead.

## 3. Confirm the profile

Present in one message: the detected stack, the proposed `.claude/project.env` values, the list of areas with their path globs, and the questions the code could not answer (code owners, whether the automated PR review is wanted, which personal-integration tools are in use). Wait for answers before writing.

## 4. Project profile

1. Fill `.claude/project.env` and delete its `TODO(adapt)` line. Run every command once before writing it: `LINT_CMD` and `FORMAT_FIX_CMD` against one real source file (they receive file paths as arguments; wrap a tool that doesn't accept paths), `TYPECHECK_CMD` and `TEST_CMD` as-is. A command that fails on a clean trunk is not ready; report it rather than writing it.
2. Set `SOURCE_EXTENSIONS` to the project's languages and narrow the extension glob in `.claude/rules/core-conventions.md` to match.
3. `GENERATED_PATHS_REGEX` from the generated code found. `FILE_NAMING_*` only when the codebase already follows one naming rule consistently (count violations with `git ls-files`); otherwise leave empty.
4. `GIT_TRUNK` from `git symbolic-ref --short refs/remotes/origin/HEAD` (strip `origin/`).
5. Add the project's safe commands to `permissions.allow` in `.claude/settings.json` (e.g. `Bash(<test command>*)`).
6. `.github/CODEOWNERS`: the owners the user named.

## 5. Conventions

`docs/conventions/` holds obligations only; system description belongs in `docs/reference/`. Don't restate what the linter or formatter already enforces. Each doc is paid in tokens once per session per area, so keep each lean.

1. `core.md` and `testing.md`: replace each `TODO(adapt)` section with observed rules, or delete the section when the project has nothing to say.
2. For each area whose rules differ from core, create:
   - `docs/conventions/<area>.md` with the same title and genre-contract line as `core.md`;
   - `.claude/rules/<area>-conventions.md`: `paths:` frontmatter plus a single `@docs/conventions/<area>.md` import, nothing else;
   - a row in the `AGENTS.md` Conventions table and in `.claude/rules/README.md`.
3. `.claude/spot-checks.tsv`: add only cheap, near-zero-false-positive structural checks for rules the linter cannot express (a forbidden import in a layer, a banned API in a directory). Each message cites its conventions section.

## 6. Knowledge docs

- `AGENTS.md`: heading, one-paragraph description, role, extra key commands and their gotchas.
- `docs/reference/architecture.md`: components, layout, request and data flow, external dependencies.
- `docs/explanation/security-model.md`: from the auth middleware, secret loading and input validation code. Mark unverified properties as open questions, never as guarantees.
- `docs/glossary.md`: the 5-15 domain nouns that recur across modules, defined as the code uses them.
- `docs/README.md`: list the area docs you created.

## 7. Prune

Present a keep-or-delete table for every skill and agent, with a one-line reason each, and delete only after the user confirms. Coupled sets go together:

| Set | Delete when |
| :-- | :---------- |
| `migration-reviewer` agent | the project has no database schema or migrations |
| CI review pipeline: `.github/workflows/claude-code-review.yml`, `tools/review/`, `pr-ci-review`, `review-retro`, the `review-*` agents | the repo is not on GitHub, or the user doesn't want automated PR review |
| `obsidian-vault` + `daily-note` | the user doesn't use Obsidian |
| `backfill-issues` | no issue-tracker MCP (`to-spec` / `to-tickets` fall back to local files, keep them) |
| `fix-sonar` / `wiz` + `fix-wiz` | no SonarQube / no Wiz |
| `prototype/UI.md` | the project has no UI (keep `LOGIC.md`) |

Then drop the matching keys from `.env.example` and update every catalog: `.claude/skills/README.md`, `.claude/agents/README.md`, the counts and trees in `.claude/README.md` and `README.md`.

## 8. Verify

1. The step 1 grep returns only slots the user chose to defer.
2. No dangling references: grep the repo for each deleted skill, agent and doc name.
3. Every `.claude/rules/*.md` import target exists, and every `docs/conventions/*.md` has a loader.
4. `bash -n .claude/hooks/*.sh scripts/*.sh`, and hooks and scripts are executable.
5. Run the quality gate for real: add a trivial edit to one source file, run `CLAUDE_PROJECT_DIR="$PWD" .claude/hooks/quality-checks.sh`, confirm it passes, then revert the edit.

## 9. Report

End with a table of what was filled, created, deleted and deferred, plus the verification results. Suggest committing the adaptation as its own PR.
