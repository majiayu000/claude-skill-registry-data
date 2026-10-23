---
name: docs-drift-review
description: Review documentation for drift caused by the current code or configuration change. Use to identify concrete inaccuracies and, when authorized, repair only directly affected documentation; not for general documentation quality, which belongs to docs-review.
---

# Documentation Drift Review

Find the documentation that the current change made wrong, and, when authorized, correct only that documentation.

## Workflow

1. Identify the changed behavior, and whether the task authorizes edits or only a read-only report.
2. List the identifiers that the change adds, renames, or removes: commands, flags, environment variables, configuration keys, endpoints, fields, error messages, file paths, and default values. Search all documentation for each one, including old names, with a text search such as `git grep`.
3. Also read the canonical, generated, mirrored, and external documentation for the changed surface: READMEs, agent instructions, API and schema references, operational documents, examples, templates, and command help.
4. Report each concrete drift with the affected claim, the implementation evidence, the canonical owner, and the required correction.
5. When edits are authorized, update only the directly affected canonical documents, in their existing style. Change generated documentation or help at its source, and regenerate it with the repository's established command.
6. For authorized prose edits, use `text-improve` on the changed text without widening the drift scope.

Use `docs-review` for broader documentation quality, `repo-context-document` for deliberate `docs/context/` work, `plan-update` for plan mechanics, and `spec-update` for semantic contract decisions. Do not restructure documentation, hand-edit generated content, change product behavior, or modify external documentation without authority.

## Result

Report the changed documents, or an evidenced no-drift result with the identifiers searched, and any owner decisions that remain open.
