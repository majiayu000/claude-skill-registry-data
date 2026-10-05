---
name: common-changelog
description: Draft and normalize user-facing CHANGELOG.md entries in Common Changelog format from release notes, pull requests, and Conventional Commits (including git trailers like Category, Ref, and Co-authored-by). Use this skill whenever the user asks for changelog text, release notes, "what changed", version summaries, or Unreleased notes, even if they do not explicitly mention CHANGELOG.md.
---

# Common Changelog

Write human-facing changelog entries in Common Changelog format.

## When to use

Use this skill when asked to generate, update, or normalize `CHANGELOG.md` from commits, PRs, or
release notes.

## When not to use

- Do not use for commit message wording; route to `git-commits`.
- Do not use for branch/rebase/PR process guidance; route to `git-trunk-based-workflow`.

## Goal

Help readers answer: what changed and how it affects them.

## Output contract

Choose exactly one output mode:

1. Full-file mode:
   - Use when the user asks to create, replace, or normalize an entire `CHANGELOG.md`.
   - Output MUST be a complete markdown file that starts with `# Changelog`.
2. Release-fragment mode:
   - Use when the user asks for a single release entry (for example `1.4.0` or `Unreleased`).
   - Output MUST contain exactly one release heading and its non-empty groups, unless `FMT-9`
     applies and the release should be skipped due to no user-facing changes.

If user intent is ambiguous, default to release-fragment mode.

When metadata is incomplete, keep producing output and append:

```text
Warnings:
- <warning 1>
- <warning 2>
```

Only include `Warnings:` when at least one warning exists.
Warnings are out-of-band metadata and MUST appear after the primary changelog artifact.

## Normative language

- `MUST`: mandatory requirement; fail output if violated
- `SHOULD`: recommended default; may be overridden only by explicit user instruction
- `MAY`: optional behavior

## Canonical rules table

Use this table as the single source of truth for output structure and bullet formatting.

| ID      | Scope                  | Requirement                                                                                                                                                                                                                                                                    |
| ------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `FMT-1` | Output scope           | In full-file mode, output MUST be a valid `CHANGELOG.md` and first heading MUST be `# Changelog`; in release-fragment mode, output MUST contain exactly one release block. Optional trailing `Warnings:` metadata MAY appear after the artifact when needed.                   |
| `FMT-2` | Release ordering       | If present, `Unreleased` MUST be the first release heading and MUST NOT be included in semantic version ordering.                                                                                                                                                              |
| `FMT-3` | Release ordering       | Released versions (excluding `Unreleased`) MUST be sorted latest-first by semantic version.                                                                                                                                                                                    |
| `FMT-4` | Release headings       | Released version headings MUST include ISO date `YYYY-MM-DD`; linked format `## [1.2.3] - YYYY-MM-DD` is SHOULD, plain `## 1.2.3 - YYYY-MM-DD` is MAY. `Unreleased` SHOULD be undated (`## [Unreleased]` or `## Unreleased`) unless the user explicitly asks for a dated form. |
| `FMT-5` | Link refs              | If any release heading is linked (`## [<label>] - YYYY-MM-DD`), trailing link references MUST be present at file end and define each linked label exactly once.                                                                                                                |
| `FMT-6` | `Unreleased` link      | If `Unreleased` is a linked heading, its reference MUST use a compare URL ending with `...HEAD`.                                                                                                                                                                               |
| `FMT-7` | Release links          | Linked released versions SHOULD point to release tags (matching repository tag conventions).                                                                                                                                                                                   |
| `FMT-8` | Sections               | Release groups MUST use only, and in this order: `Changed`, `Added`, `Removed`, `Fixed`; empty groups MUST NOT be emitted.                                                                                                                                                     |
| `FMT-9` | No user-facing changes | If a release has no user-facing changes, default is skip (including release-fragment mode). If explicitly requested, MAY add a one-line maintenance notice under the release heading.                                                                                          |
| `BUL-1` | Writing style          | Use imperative style (`Add`, `Fix`, `Remove`, `Bump`), keep bullets concise, and describe user impact (not internal trivia).                                                                                                                                                   |
| `BUL-2` | Breaking changes       | Breaking changes MUST be prefixed with `**Breaking:**`.                                                                                                                                                                                                                        |
| `BUL-3` | Bullet group order     | Every bullet MUST follow this order: optional references group, required commit-links group, required final authors group. Commit-links group MUST contain at least one commit link when available; otherwise use `source unavailable` and emit a warning.                     |
| `BUL-4` | Group formatting       | References, commit links, and authors MUST each appear in one parentheses group; multi-item groups MUST use comma-separated lists.                                                                                                                                             |
| `BUL-5` | Template source        | Bullet shape and full file layout MUST follow `references/CHANGELOG.md`.                                                                                                                                                                                                       |
| `BUL-6` | Missing metadata       | If author metadata is missing, authors group MUST be `(Unknown author)` and a warning MUST be emitted.                                                                                                                                                                         |

## Input model

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Recognize trailers and reference keywords:

- `Category:`
- `Ref:`
- `Re:`
- `Co-authored-by:`
- `BREAKING CHANGE:`

Also recognize GitHub issue-linking keywords:

- `close`, `closes`, `closed`
- `fix`, `fixes`, `fixed`
- `resolve`, `resolves`, `resolved`

For `Ref`, `Re`, and the keywords above:

- matching is case-insensitive
- `:` is optional (for example `Ref ABC-123` and `Ref: ABC-123` are both valid)
- treat GitHub keywords as reference signals only when an issue target is present (for example
  `Fixes #123`)

## Classification algorithm

Apply in this order:

1. `Category:` trailer override
2. Conventional Commit type mapping
3. Semantic fallback

### 1) Category override (highest priority)

If `Category:` maps to a group, use it:

- `change`, `changed` -> `Changed`
- `add`, `added` -> `Added`
- `remove`, `removed` -> `Removed`
- `fix`, `fixed` -> `Fixed`

Rules:

- case-insensitive matching
- if multiple `Category:` trailers exist, use the last recognized one
- ignore unknown values and continue

### 2) Conventional Commits mapping

- `feat` -> `Added`
- `fix` -> `Fixed`
- `perf` -> `Changed` only if user-facing; otherwise skip
- `refactor` -> `Changed` only if user-facing; otherwise skip
- `revert` -> `Changed` or `Fixed` based on actual user effect
- `docs`, `style`, `test`, `chore`, `ci`, `build` -> skip unless user-facing

### Type compatibility notes

- This skill classifies commit history, so it accepts both the strict type set used by
  `git-commits` and broader Conventional Commit variants observed in existing repositories.
- Accepted history-only variants include: `perf`, `style`, `test`, `ci`, `build`.
- This does NOT change the output type policy of `git-commits`; it only affects changelog
  classification of existing commits.

### 3) Semantic fallback

If type is missing or unclear:

- Existing behavior changed -> `Changed`
- New capability -> `Added`
- Capability removed -> `Removed`
- Bug corrected -> `Fixed`

### Conflict examples

- `fix(api): ...` + `Category: add` -> `Added`
- `feat!:` + `Category: remove` -> `Removed` + `**Breaking:**`
- `docs:` + `Category: fixed` -> `Fixed`

## Classification decision tree

1. If there is a recognized `Category:` value, map it and stop.
2. Else, if Conventional Commit type is recognized, apply the type mapping.
3. Else, classify by semantic user impact (`Changed`/`Added`/`Removed`/`Fixed`).
4. If breaking signal exists (`!` or `BREAKING CHANGE:`), prefix with `**Breaking:**`.

## Breaking change handling

- If header has `!` or body/footer contains `BREAKING CHANGE:`, prefix with `**Breaking:**`
- Keep the entry in `Changed`/`Added`/`Removed`/`Fixed` by impact (no extra section)

## User-facing quick test

Usually include:

- API contract or output changed
- CLI flags/defaults changed
- Config shape/defaults changed
- Runtime/performance behavior users notice
- Dependency bump that fixes production bug/security issue

Usually skip:

- Internal refactor without behavior change
- CI/test/style-only updates
- Dev tooling and internal docs only
- Dependency bump for dev/test-only tooling

## References and authors

- Commit hash SHOULD be a markdown link when available:
  - ``[`d23ba8f`](https://github.com/OWNER/REPO/commit/d23ba8f)``
- Group formatting for references, commit links, and authors MUST follow `BUL-3` and `BUL-4`
- Build references from:
  - explicit PR/issue links
  - `Ref` and `Re` trailers
  - GitHub keywords (`close*`, `fix*`, `resolve*`) with issue targets
- Normalize before deduplication:
  - treat `#123` and `https://github.com/OWNER/REPO/issues/123` as the same issue reference
  - normalize case for keyword-style references (for example `jira-123` -> `JIRA-123`)
- Reference order is deterministic:
  1. first: one high-signal repository reference (prefer PR, otherwise issue)
  2. then: remaining unique references in first-seen order
- Commit-link order is deterministic:
  1. deduplicate by commit hash
  2. keep first-seen order
- Use commit author as primary author
- Append `Co-authored-by:` names (extract name before `<email>`)
- Authors MUST be deduplicated in stable first-seen order
- For aggregated bullets, authors MUST be the deduplicated union of commit authors and
  `Co-authored-by:` names from all included commits, preserving stable first-seen order
- If commit author is a bot and merger is known, prefer the human merger name

## Metadata fallback policy

- If author cannot be determined from metadata, use `(Unknown author)` and emit a warning.
- If no commit link can be determined, use `(source unavailable)` as the commit-links group and emit
  a warning.
- Missing metadata MUST NOT be a sole reason to drop user-facing bullets.

## Fail policy

- If any structural `MUST` rule is violated and cannot be recovered with fallback policy, fail.
- Missing author/commit metadata alone MUST NOT trigger hard fail.
- If changelog scope is unclear, default to release-fragment mode instead of failing.

## Authoring workflow

1. Collect input: commits, PRs, issues, release notes.
2. Parse commit headers, body, and trailers.
3. Classify each change using rules above.
4. Remove non-user-facing noise and no-op pairs (change + immediate revert).
5. Rewrite into concise user-facing bullets.
6. Group by `Changed`, `Added`, `Removed`, `Fixed` in that order.
7. Validate against `Canonical rules table` and `references/CHANGELOG.md`.

## Anti-patterns

- Raw technical commit text with no user context
- Non-standard sections (`Security`, `Docs`, `Chore`, etc.)
- Internal-only noise in public changelog
- Missing `**Breaking:**` marker for incompatible changes

## Quality checklist

- Validate all applicable `FMT-*` and `BUL-*` requirements from `Canonical rules table`.
- Verify output shape against `references/CHANGELOG.md`.
- Ensure warning messages exist for every metadata fallback.
- Any checklist failure MUST trigger `Fail policy`.

## Prompt templates

- `Generate a Common Changelog entry for version <VERSION> from these commits and PRs. Keep only user-facing changes, include references, and mark breaking changes.`
- `Normalize this existing changelog fragment to Common Changelog format without losing important user-impact details.`
- `Classify these Conventional Commits into Changed/Added/Removed/Fixed and explain any skipped items.`

## References

- `references/CHANGELOG.md` (local formatting template)
- https://common-changelog.org/
- https://github.com/vweevers/common-changelog
- https://www.conventionalcommits.org/
- https://git-scm.com/docs/git-interpret-trailers
- https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword
