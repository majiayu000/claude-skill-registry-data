---
name: git-style-commit
description: Analyze git history for commit style, stage changes logically, and commit without pushing. Use when the user wants to commit changes matching their repository's existing style.
---

# Git Style-Aware Commit

This skill instructs the agent to autonomously analyze repository commit conventions, logically group pending changes into atomic commits, and generate matching commit messages.

## 🎯 Trigger Conditions
- User asks to "commit changes", "save work", or "create a commit".
- User provides specific files to commit.
- User wants to ensure commit messages follow existing repository standards.

## 🛠️ Execution Steps

### 1. Inspect Repository State and Analyze Commit Style
First inspect all pending work:
```bash
git status --short
git diff
git diff --staged
```

If there are no pending changes, report that and do not create an empty commit unless the user explicitly requests one.

Then run `git log -n 15 --pretty=format:"%s"` to detect the prevailing pattern:
- **Format:** Conventional Commits (`feat:`, `fix:`), bracket prefixes (`[API]`), or plain text.
- **Capitalization & Tense:** Sentence case, title case, lowercase; present vs. past tense.
- **Emoji Usage:** Detect if Gitmoji or other emoji conventions are used.

### 2. Autonomously Stage Changes (Atomic Commits)
Review all pending changes (`git diff` and `git diff --staged`).
- **Logical Grouping:** Do NOT blindly `git add -A`. Group changes into atomic, focused commits (e.g., separate bug fixes from new features).
- **Hunk-Level Staging:** Simulate `git add -p` by staging specific files (`git add <file>`) or applying patch files for specific hunks.
- **Sequential Commits:** Create multiple commits sequentially if changes encompass distinct logical units.
- **Preserve User Work:** Stage only changes belonging to the current commit; leave unrelated working-tree and pre-existing staged changes untouched.
- **Review Before Commit:** Run `git diff --staged` after staging. If it mixes unrelated work, adjust the staging before continuing.

### 3. Generate Commit Message
Draft a concise message (subject < 72 chars) that perfectly matches the detected style.
- **Gitmoji Integration:** If Gitmoji is detected, choose exactly one Gitmoji from the embedded guide below based on the dominant user-facing intent of the commit. Do not rotate emojis randomly for variety, and do not default to a small handful of familiar emojis unless they are genuinely the best fit.
- **Pick the dominant change:** Prefer the primary reason the commit exists, not every file touched.
- **One emoji per atomic commit:** Split unrelated work into separate commits instead of stacking multiple emojis into one subject.
- **Conventional Commits:** Include appropriate scope if used in the repo (e.g., `feat(auth):`).
- **No AI Attribution:** Do not mention AI agents, AI tools, assisted generation, or authorship claims in commit messages unless the repository change is directly about that tool as product content.

#### Gitmoji Quick Reference
Use this compact embedded set for the vast majority of commits:

- `✨` Introduce new features.
- `🐛` Fix a bug.
- `🩹` Apply a simple fix for a non-critical issue.
- `🚑️` Critical hotfix.
- `♻️` Refactor code.
- `🎨` Improve structure / format of the code.
- `⚡️` Improve performance.
- `🔥` Remove code or files.
- `🚚` Move or rename resources such as files, paths, or routes.
- `📝` Add or update documentation.
- `💬` Add or update text and literals.
- `✅` Add, update, or pass tests.
- `🧪` Add a failing test.
- `🔒️` Fix security or privacy issues.
- `🔐` Add or update secrets.
- `🔧` Add or update configuration files.
- `🔨` Add or update development scripts.
- `👷` Add or update CI build system.
- `💚` Fix CI build.
- `🚨` Fix compiler / linter warnings.
- `➕` Add a dependency.
- `➖` Remove a dependency.
- `⬆️` Upgrade dependencies.
- `⬇️` Downgrade dependencies.
- `📌` Pin dependencies to specific versions.
- `🏷️` Add or update types.
- `🗃️` Perform database related changes.
- `🌱` Add or update seed files.
- `🏗️` Make architectural changes.
- `💄` Add or update the UI and style files.
- `♿️` Improve accessibility.
- `📱` Work on responsive design.
- `💥` Introduce breaking changes.
- `🔖` Release / version tags.
- `👽️` Update code due to external API changes.
- `🧱` Infrastructure related changes.
- `🧑‍💻` Improve developer experience.

For rarer commit types, use the closest semantic Gitmoji only if the repository clearly uses that broader Gitmoji vocabulary.

#### Gitmoji Selection Rules
- Prefer `🐛` over `🩹` for normal bug fixes. Reserve `🩹` for very small, non-critical fixes.
- Prefer `♻️` for behavior-preserving refactors. If behavior changes, pick the behavior change instead.
- Prefer `🔧` for config changes and `🔨` for dev scripts/tooling. Do not use them interchangeably.
- Prefer `👷` for CI workflow files, and `💚` when the point of the commit is fixing a broken CI run.
- Prefer `✅` when the commit is mainly about tests. If tests only support a feature or bug fix, use `✨` or `🐛`.
- Prefer `📝` for docs-only commits. If docs accompany code, choose the code-related emoji.
- Prefer `🚚` for renames and moves, even if imports or references also need small follow-up edits.
- Prefer `🚨` for commits that mainly silence linter, compiler, or type-check warnings. If the same commit also fixes a real bug or adds behavior, use the bug or feature emoji instead.
- Prefer `⬆️`, `⬇️`, and `📌` for dependency version changes. Use `➕` or `➖` only when the dependency itself is being added or removed.
- Prefer `🏷️` for type-only changes. If the type update is only part of a bug fix, refactor, or feature, choose the higher-level intent instead.
- Prefer `💬` for user-facing copy and string literal changes, and `💡` for source-code comments. Do not use `📝` unless the change is actual documentation.
- Prefer `🗃️` for schema, migration, or database-layer changes, and `🌱` specifically for seed data. If the main change is business logic that happens to touch the database, use the business logic emoji.
- Prefer `🏗️` for structural or architectural redesigns that reshape modules, boundaries, or system layout. Use `♻️` for smaller local refactors that stay within the existing architecture.

### 4. Execute Commit
Run the commit with the generated message:
```bash
git commit -m "YOUR_GENERATED_MESSAGE"
```
*(If multiple atomic commits were identified in Step 2, repeat Steps 3-4 for each logical group).*

## ⚠️ Constraints & Error Handling
- **NEVER PUSH:** Stop immediately after creating the commit(s).
- **No History Rewrites or Cleanup:** Do not amend, rebase, reset, force-push, run `git clean -fd`, or use similar destructive commands.
- **No History:** If no commit history exists, default to Conventional Commits (`feat:`, `fix:`, etc.).
- **Staging/Commit Failures:** If staging, hooks, or `git commit` fail, report the exact failure and halt. Do not bypass hooks, retry automatically, or broaden staging.
- **Verification:** Print each final commit's short hash and subject with a success indicator (e.g., `✅ Committed: abc1234 feat: add import validation`).
