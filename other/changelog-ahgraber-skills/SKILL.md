---
name: changelog
description: |-
  Use when writing, updating, or generating a CHANGELOG.md — for a new release, an unreleased section update, or drafting from git history or diff. Triggers: "update the changelog", "write release notes", "what changed since X", "generate changelog for v1.2.0", "add this to the changelog", "draft unreleased section". Not for commit messages (use commit-message skill) or internal deployment runbooks.
---

# Changelog

Draft or update a `CHANGELOG.md` following Keep a Changelog conventions.

## When to Use

- Writing or updating `CHANGELOG.md` for an upcoming or recent release
- Drafting or appending to an `[Unreleased]` section from recent merged work
- Generating a changelog from git history, a commit range, or a diff
- Editing or cleaning up an auto-generated changelog draft

## When Not to Use

- Writing a git commit message — use `commit-message` skill
- Writing internal release notes or deployment runbooks (audience is operators, not users)
- Full code review — use `code-review` skill

## Invocation Notice

- Tell the user when this skill is running: `changelog`.
  Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
  A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

## Workflow

### 1. Determine scope

Infer target version, release date, and commit range from context.
Ask only if neither the version nor the range can be determined.

- Default range: `git log <previous-tag>..HEAD --oneline --no-merges`
- If no prior tag exists: `git log --oneline --no-merges`
- If updating `[Unreleased]` only: use commits since last tagged release

Check for an existing `[Unreleased]` section in `CHANGELOG.md` — do not duplicate entries already there.

### 2. Collect commits

```bash
git log <range> --oneline --no-merges
```

Also read the existing `CHANGELOG.md` to understand document structure and last version.

### 3. Filter noise

Exclude commits with no user-visible effect.
Retain only what matters to users.
See `references/entry-guidelines.md` for the full include/exclude list.

**Quick exclusion rule:** if a user reading the changelog would not care, cut it.

### 4. Categorize

Map surviving entries to Keep a Changelog categories (in display order):

| Category             | When to use                                                    |
| -------------------- | -------------------------------------------------------------- |
| **Breaking Changes** | Any change requiring user action — config, API, CLI, behavior  |
| **Added**            | New features, commands, endpoints, options                     |
| **Changed**          | Modified behavior, performance improvements, visible refactors |
| **Deprecated**       | Things that still work but will be removed                     |
| **Removed**          | Deleted features, commands, options                            |
| **Fixed**            | Bug fixes                                                      |
| **Security**         | Vulnerability patches                                          |

Breaking changes get their own subsection at the top of the version block.
See `references/entry-guidelines.md` for the Conventional Commits → category mapping.

### 5. Write entries

- One entry per **logical user-visible outcome** — consolidate multi-commit features into one line
- Imperative present tense: `Add X`, `Fix Y`, `Remove Z`
- For breaking changes: state what broke AND the migration path (e.g., `Remove X — replace with Y; see docs/migration.md`)
- One reference link per entry; prefer PR over commit hash over issue number
- Do not include implementation details, commit hashes in entry text, or "WIP" notes

### 6. Insert into CHANGELOG.md

See `references/changelog-format.md` for the exact block structure and version comparison link format.

**New release (no `[Unreleased]` section):** insert `## [x.y.z] - YYYY-MM-DD` block at the top of the file.

**New release (existing `[Unreleased]` section):**

- If `[Unreleased]` IS the release being cut: replace `## [Unreleased]` with `## [x.y.z] - YYYY-MM-DD`; add a fresh empty `## [Unreleased]` above it.
- If `[Unreleased]` contains unrelated upcoming work: insert the new versioned block between `[Unreleased]` and the previous version.

**Updating `[Unreleased]` only:** append entries under the matching category subsection; create the subsection if absent.

Add or update the version comparison link at the bottom of the file.

### 7. Verify before delivering

- [ ] Version bump is semantically correct: breaking → major, new feature → minor, fix → patch
- [ ] No CI/CD, formatting, test-only, or dev-tooling entries present
- [ ] Breaking changes include a migration path
- [ ] Date is ISO 8601 (`YYYY-MM-DD`)
- [ ] No duplicate entries from the existing `[Unreleased]` section

## Output

An updated `CHANGELOG.md` with the new version block inserted (or `[Unreleased]` section updated), ready for user review before commit.

## References

- `references/entry-guidelines.md` — include/exclude heuristics and Conventional Commits mapping
- `references/changelog-format.md` — full Keep a Changelog format rules and examples
