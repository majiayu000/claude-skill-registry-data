---
name: changelog-assembly
description: This skill should be used when the user mentions "changelog", "release notes", "keep a changelog", "conventional commits", "commit message", "what changed", or "release summary". Provides a standardized methodology to turn raw, possibly non-conventional git history into human-readable changelogs and release notes.
---

# Changelog Assembly

## Purpose

Provide a consistent, repeatable methodology for converting raw git history, whether or not it follows Conventional Commits, into release notes and changelog entries that a human reader actually benefits from. Covers classification, grouping, de-duplication, audience-appropriate phrasing, linking, and the Unreleased section. Tech-agnostic.

## The assembly pipeline

1. **Collect** the commit range (`<last-tag>..HEAD`, or an explicit range). Exclude merge commits from the entry list; mine them only for PR numbers.
2. **Classify** each commit into a Keep a Changelog category. If the message is conventional, map the type; if not, infer from the diff.
3. **De-duplicate & fold**: collapse "fix typo", "wip", and follow-up commits into the logical change they belong to.
4. **Rephrase** each surviving item into user-facing language: describe the observable effect, not the code mechanics.
5. **Order** by category (Added, Changed, Deprecated, Removed, Fixed, Security) and by impact within each.
6. **Elevate** breaking changes into a prominent callout at the top.
7. **Link** PR/issue references and add compare links.

## Category mapping

| Conventional type | Keep a Changelog category | Notes |
|-------------------|---------------------------|-------|
| `feat` | Added | New capability |
| `fix` | Fixed | Bug fix |
| `perf` | Changed | Behavior/characteristics changed |
| `refactor` | usually omitted | Internal; include only if user-observable |
| `docs`/`test`/`ci`/`build`/`chore` | usually omitted | Internal unless user-facing |
| any `!` / `BREAKING CHANGE:` | Changed/Removed + top callout | Always surfaced |
| dependency CVE bump | Security | Even if labeled `chore`/`build` |

## Inferring type from non-conventional history

When the message is uninformative, read the diff:

| Diff signal | Category |
|-------------|----------|
| New files / new public exports / new endpoints / new flags | Added |
| Deleted exports / endpoints / flags / files | Removed |
| `@deprecated` markers, deprecation notices | Deprecated |
| Changed defaults, signatures, output shape | Changed |
| Bug-fix pattern (guard added, off-by-one, null check) | Fixed |
| Auth hardening, input sanitization, dependency vuln bump | Security |

## Phrasing rules (write for humans)

- Lead with the user-visible effect: "Dark mode now persists across sessions", not "refactor theme store."
- Present tense, imperative-adjacent: "Add", "Fix", "Remove".
- One line per change; move detail to a nested bullet only when a migration step is needed.
- Name the affected surface (command, endpoint, option) so readers can tell if it affects them.
- Never expose internal churn (rename of a private helper, lint fixes) in user-facing notes.

## The Unreleased section

Keep an `## [Unreleased]` section at the top of `CHANGELOG.md`, populated as changes merge. At release time, rename it to the version with a date and open a fresh empty Unreleased. This keeps notes accurate instead of reconstructed under deadline.

## Additional Resources

### Reference Files
- **`references/conventional-commits.md`**: the full Conventional Commits 1.0.0 taxonomy: every type, scope, the `!` breaking marker, the `BREAKING CHANGE:` footer, good vs bad message examples, and how each type maps to a semver bump.
- **`references/keep-a-changelog.md`**: the Keep a Changelog format: the six categories, Unreleased section, dated version headers, compare links, and good vs bad entry examples.
