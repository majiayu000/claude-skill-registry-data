---
name: changelog-authoring
description:
  Generate or update CHANGELOG.md and release notes from commit messages in a pull request or the current branch
  compared with its base, usually main, or from project specifications and planning records. Use for changelog drafts,
  release summaries, and comparison-based updates. Preserve existing changelog entries when adding new dated blocks.
---

# Changelog Authoring

Turn commit messages, project records, or both into concise changelog entries that explain changes to users and
operators. Support a pull request, the current branch compared with its base, or an explicit release range. A planning
directory is optional.

## Workflow

1. Preserve Git index and working-tree state while gathering evidence. Do not stage, unstage, commit, amend, reset,
   switch branches, or discard files unless explicitly asked. Exclude uncommitted changes from a commit-based summary.
2. Honor the requested source: commit messages, project records, or both. For a PR or branch request with no specified
   source, start with its commit messages and use targeted diffs or linked records to clarify consequential claims.
3. Resolve the comparison using the rules below. Record the selected refs and commit SHAs so the evidence has a stable
   scope.
4. Read the selected evidence using the relevant source guidance below. Do not require planning documents for a
   commit-based changelog or invent completed implementation from a planning record.
5. Consolidate related changes into product-facing entries. Use diffs to resolve vague messages, duplicate descriptions,
   fixups, or reverts when that evidence is available. If the request limits evidence to messages, state consequential
   uncertainty instead of inventing details.
6. Return a draft when requested. When asked to create or update a file, use the requested path or root `CHANGELOG.md`
   and follow the prepend-only contract below. Generating release notes does not itself authorize publishing a release.

## Resolve the comparison

- **Explicit refs:** Honor the user's base and head refs before applying defaults.
- **Pull request:** Read the PR's repository, target base, head revision, and complete commit list through the available
  provider tool or CLI, including pagination. Use its actual base, which may differ from main. A fork's head branch name
  alone does not identify the right local revision. For a merged PR, use the provider's PR commit list or recorded
  comparison; comparing the current base with an already-merged head can incorrectly produce an empty result.
- **Current branch:** Use `HEAD` as the head. Prefer its known PR target or project-configured integration branch.
  Otherwise resolve the primary remote's default branch; if unavailable, try `origin/main`, then `main`. A tracking
  branch for the same feature is not evidence of its integration base. Do not use the latest tag as the base of a branch
  comparison.
- **Release since a tag:** Use the requested release refs. If the user asks for changes since the last release without
  naming a base, use the latest reachable release tag according to project conventions.

Verify that refs exist and identify the intended repository. Missing or stale local PR refs can be resolved through a
read-only provider comparison. Fetch only the required refs when network access and task authorization permit it; never
change the active checkout to inspect a PR. State when the result uses an unrefreshed local snapshot. If the required
base cannot be established, ask for that ref rather than silently choosing an unrelated range.

## Read commit evidence

For a local branch comparison, use the resolved base and head SHAs in these read-only commands:

```bash
git log --reverse --format=fuller <base>..<head> --
git diff --name-status <base>...<head> --
git diff <base>...<head> -- <relevant-paths>
```

The two-dot log selects commits reachable from the head but not the base. The three-dot diff shows the head's changes
since the common ancestor, avoiding unrelated changes made only on the base branch. For an explicit release-to-release
tree comparison, use `git diff <base> <head> -- <relevant-paths>` instead.

Read commit subjects and bodies. Do not rely only on the PR title or require Conventional Commit formatting. Do not
globally exclude merge commits, since a merge can contain meaningful conflict resolutions. Group commits by resulting
behavior, avoiding duplicate entries for merge descriptions, fixups, and repeated messages. Reconcile reverted or
superseded changes with the final diff when available. Cite commit IDs or PR links when useful, using only verified
repository URLs.

Commit messages are valid evidence for a changelog draft. They do not prove successful tests, deployment, or production
availability. State material verification gaps, especially when only messages were supplied.

## Read project-record evidence

Use the root named by the user. Otherwise inspect the project's workflow guidance and likely roots such as
`.changeset/`, `backlog/`, or `docs/` to identify the active records. A directory with `GUIDE.md` and `MILESTONES.md`
can help identify the planning workflow. Consult `.agents/plans/` or `.agents/memory/` only when the project uses them
for this purpose. Ask about ambiguity only when the choice would materially change the summary.

Start with changed paths in the selected comparison, then read changed records and directly linked evidence needed to
understand release impact. Prefer explicit `Changelog Impact` fields in plans, checkpoints, and bug-fix records. Use
targeted diffs, `git show <ref>:<path>`, and searches for fields such as `Fixed`, `Security`, `Operations`, or
`QA / Verification`; do not bulk-read the planning root.

Separate proposed work, accepted requirements, completed implementation, and verified runtime behavior. Planning changes
may be included as planning changes, but must not imply that a feature has shipped. Link to source records where useful.
If the requested records are unavailable, explain the gap; commit-based generation remains possible when that source is
within the user's scope.

## What To Include

Include meaningful changes that affect users, operators, product behavior, domain rules, security posture, setup/env
requirements, QA expectations, defect outcomes, release checks, or agent/human handoff state.

Use these sections only when they have content:

- `Added`
- `Changed`
- `Fixed`
- `Removed`
- `Security`
- `Operations`
- `QA / Verification`

Each bullet should explain the outcome to a mixed internal audience. Summarize commit messages and records in plain
language; include relevant breaking changes and migration requirements. Keep evidence links useful and proportionate.

Do not include:

- coordination-board churn
- template-only edits
- pure formatting
- internal refactors with no behavior, operation, QA, or release impact
- noisy status/date-only changes
- a raw commit-log dump unless the user explicitly requests that format

## Prepend-Only Update Contract

Use the requested changelog path, or `CHANGELOG.md` at the project root by default. This contract applies when writing
the file; a request for an inline draft needs no file mutation.

Use a dated block:

```markdown
## YYYY-MM-DD
```

If the user provides a version, milestone, or release label, use:

```markdown
## YYYY-MM-DD - <label>
```

When `CHANGELOG.md` does not exist, create it with:

```markdown
# Changelog

## YYYY-MM-DD

### Added

- ...
```

When `CHANGELOG.md` already exists:

- preserve all existing content exactly except for inserting the new block
- insert after the top `# Changelog` title and any short intro directly below it
- insert before the first existing `## ` changelog entry
- do not rewrite, reorder, deduplicate, merge, or clean up older entries unless the user explicitly asks
- when generating another chunk on the same date, create a new dated block instead of merging into the existing block

If there are no meaningful changelog entries, leave the file unchanged and report that the selected evidence had no
release-relevant changes.

## Final Response

Report:

- draft delivered, or changelog path created, updated, or left unchanged
- comparison refs and SHAs, or PR identity and provider evidence used
- sources used: commit messages, diffs, and/or project records, including the planning root when applicable
- number of entries added by section
- significant omissions or unresolved ambiguity, including reverted changes or uncertain implementation status
- checks run and material verification limits

Keep the response concise. Do not paste the full changelog unless the user asks.
