---
name: simple-full-refactor
description: Refactor the entire repo with minimal changes to remove redundancy (DRY), dead code, leftovers, and unused files, without changing behavior. Use when the user asks for a full, whole-repo, or deep refactor or cleanup.
disable-model-invocation: true
metadata:
  author: denniemok
  version: "1.0.0"
license: MIT
---

# Simple Full Refactor

Clean up the whole repo without breaking it. Same idea as `simple-refactor`, but across every file, and it also removes leftovers and unused files. The golden rule is to change only what is necessary. If the code is good enough, leave it.

## Scope

The entire repo. Skip third-party, generated, and build output folders (`node_modules`, `dist`, lock files, and similar).

## Workflow

1. Read the tree and detect the repo's conventions, entry points, and tooling.
2. Find:
   - Repeated logic, data, or patterns, including across modules
   - Dead code, unused imports, and unreachable branches
   - Leftovers: debug logs, commented-out code, and temp or backup files
   - Files and dependencies that nothing references
   - Long functions or files doing more than one job
   - Deep nesting that early returns would flatten
   - Magic numbers and strings that need a named constant
   - Unclear names
3. Read nearby usage and existing tests to confirm current behavior.
4. Propose a plan: the code changes in short, plus every file and dependency to delete with the reason. Wait for approval before deleting.
5. Apply the fixes and update call sites. Add or adjust tests only when needed to guard against regressions.
6. Run the build, type check, or tests. If you cannot, say what should be run.

## Rules

- Keep behavior and public APIs unchanged unless the user asks otherwise.
- Prefer small edits over sweeping changes. Work module by module.
- Extract only when the duplication is meaningful. Two similar lines are not a reason to add an abstraction.
- Do not add layers that bring indirection without clear benefit.
- Keep comments and move them with the code they describe.
- Follow the repo's existing naming, style, and file layout.

## Deleting files

- Before deleting a file, confirm nothing references it. Search imports, dynamic imports, configs, scripts, HTML, and docs.
- Never delete entry points, config files, or files the tooling or framework loads by path or convention (routes, migrations, public assets, workflows).
- Keep files that may be valuable later, even if unused now: docs, notes, examples, templates, fixtures, seed data, migrations, scripts, design assets, and drafts of planned features. When unsure, keep it and list it as "unused, kept".
- Delete with `git rm` when in a git repo, so it can be restored.

## Output

A short summary of what changed, the deleted files and dependencies, the unused files kept and why, plus any risks or areas that need testing.
