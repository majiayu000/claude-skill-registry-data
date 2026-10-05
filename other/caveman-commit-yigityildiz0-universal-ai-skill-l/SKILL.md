---
name: caveman-commit
description: "Manual Caveman-style Conventional Commit message generator that preserves intent, rationale, breaking-change details, and repository conventions. Use only when explicitly invoked as $caveman-commit, /caveman-commit, 'Caveman commit', or an equally unambiguous request for a Caveman-style commit message. Never activate for generic commit, staging, or commit-message requests. Turkish triggers: Caveman commit, mağara modu commit mesajı."
license: MIT
---

# Caveman Commit

Draft the message only. Do not stage, commit, amend, push, or change files.

Safety-adapted from [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman), MIT licensed. Preserve the included `LICENSE` when redistributing.

## Workflow

1. Inspect the relevant diff and recent commit convention when available.
2. Identify the change type, scope, user-visible effect, and non-obvious why.
3. Draft the shortest message that preserves those facts.
4. Check breaking changes, migrations, security impact, issue references, and
   required repository trailers.

## Format

- Subject: `<type>(<scope>): <imperative summary>`; omit scope when unhelpful.
- Prefer 50 characters or fewer; never exceed 72.
- Use the repository's existing capitalization and type conventions.
- Use an imperative verb and no trailing period.
- Add a wrapped body only for rationale, breaking changes, migrations,
  security implications, reverts, or issue context.
- Keep `BREAKING CHANGE:` and required trailers exact.

Do not add AI attribution unless the user's or repository's rule explicitly
requires it. Do not remove a required attribution trailer.

## Output

Return one paste-ready code block. If evidence is insufficient, state the
missing fact before the draft rather than inventing it.
