---
name: release
description: Version bump, generate changelog, tag, and prepare a release
type: shipping
version: v0.2
required_conventions: [alignment-page]
---

# Release

Invoke as `$release`.

Use this skill when the user wants to cut a release for the project.

## Process

1. Determine version bump from arguments or analyze commits to suggest one.
2. Run pre-release checks:
   - Ensure the working tree is clean.
   - Resolve the primary branch: prefer `main`; if it does not exist, use `master`. If neither exists, stop and explain the blocker.
   - Ensure the current branch is the primary branch. If not, stop and tell the user to cut releases only from `main`/`master`.
   - Ensure the primary branch is up to date with remote.
   - Run tests to verify everything passes.
3. Generate changelog from conventional commits since last tag.
4. Bump version in package.json and other version files.
5. Commit and create annotated git tag.
6. Ask about push, GitHub release, and deploy.

## Output

- **Changelog**: features, fixes, breaking changes
- **Files Updated**: version files and changelog
- **Tag**: version tag created
- **Next Steps**: awaiting confirmation for push/release/deploy

## Constraints

- Always confirm version with user before changes.
- Never push or create GitHub releases without explicit confirmation.
- **Do not push to an existing feature branch.** Releases should only be cut from `main`/`master`. If on a feature branch, stop and ask the user.
- Stop if tests fail — do not release broken code.


## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/release-{topic}.html`. By default, report results inline and write only this skill's normal durable artifacts; create an alignment page only when explicitly requested or when a concrete clarification/review need cannot be handled cleanly inline.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
