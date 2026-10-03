---
name: release
description: Version bump, generate changelog, tag, and prepare a release
type: shipping
version: v0.2
required_conventions: [alignment-page]
argument-hint: "[patch|minor|major] or [specific version like 1.2.3]"
---

# Release

Manage the release ceremony: version bump, changelog generation, git tag, and optional deploy trigger.

## Process

1. **Determine the version bump** from `$ARGUMENTS`:
   - `patch`, `minor`, or `major` → compute the next version from the current one.
   - Specific version (e.g., `1.2.3`) → use it directly.
   - If no argument, analyze commits since the last tag to suggest a version:
     - Any `feat:` commits → suggest `minor`
     - Only `fix:` / `chore:` / `docs:` → suggest `patch`
     - Any `BREAKING CHANGE` or `!:` → suggest `major`
   - Confirm the version with the user before proceeding.

2. **Pre-release checks:**
   - Ensure the working tree is clean.
   - Resolve the primary branch: prefer `main`; if it does not exist, use `master`. If neither exists, stop and explain the blocker.
   - Ensure the current branch is the primary branch. If not, stop and tell the user to cut releases only from `main`/`master`.
   - Ensure the primary branch is up to date with remote.
   - Run tests to verify everything passes.
   - Check for any TODO or FIXME items in `tasks/roadmap.md`, `tasks/todo.md`, and `tasks/manual-todo.md` (if it exists) that should block the release. Count `tasks/record-todo.md` and `tasks/recurring-todo.md` as advisory only unless an item explicitly says it blocks release.

3. **Generate the changelog:**
   - Find the last git tag (or first commit if no tags exist).
   - Collect all commits since the last tag.
   - Group by conventional commit type:
     - **Features** (`feat:`)
     - **Bug Fixes** (`fix:`)
     - **Breaking Changes** (`BREAKING CHANGE` or `!:`)
     - **Other** (`refactor:`, `chore:`, `docs:`, `test:`, `perf:`)
   - Format as a markdown changelog entry with the version and date.

4. **Apply the version bump:**
   - Update `package.json` version (root and/or workspace packages as appropriate).
   - If a `CHANGELOG.md` exists, prepend the new entry. If not, create one.
   - If the project uses other version files (e.g., `version.ts`, `__version__.py`), update those too.

5. **Commit and tag:**
   - Stage the changed files.
   - Commit with message: `release: vX.Y.Z`
   - Create an annotated git tag: `vX.Y.Z` with the changelog entry as the tag message.

6. **Ask about next steps:**
   - Push the commit and tag? (ask for confirmation)
   - Create a GitHub release? (ask for confirmation)
   - Trigger a deploy? (ask for confirmation)

## Output

### Release vX.Y.Z

**Changelog:**

#### Features
- commit summary (hash)

#### Bug Fixes
- commit summary (hash)

#### Breaking Changes
- commit summary (hash)

**Files Updated:**
- `package.json` — version bumped
- `CHANGELOG.md` — entry added

**Tag:** `vX.Y.Z`

**Next steps:** push / GitHub release / deploy (awaiting confirmation)

## Constraints
- Always confirm the version with the user before making changes.
- Never push or create a GitHub release without explicit user confirmation.
- **Do not push to an existing feature branch.** Releases should only be cut from `main`/`master`. If on a feature branch, stop and ask the user.
- If tests fail during pre-release checks, stop and report — do not release broken code.
- For monorepos, ask the user whether this is a root release or a package-specific release.
- Do not modify code as part of the release — only version files, changelogs, and tags.


## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/release-{topic}.html`. By default, report results inline and write only this skill's normal durable artifacts; create an alignment page only when explicitly requested or when a concrete clarification/review need cannot be handled cleanly inline.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
