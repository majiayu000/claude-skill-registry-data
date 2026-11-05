---
name: agents-context-router-release
description: Prepare, review or publish an agents-context-router release through its Release Please PR and GitHub draft release. Use when preparing a release, choosing the next version, reviewing a Release PR or publishing a new version.
---

Read `docs/releasing.md` before acting. It owns the version policy, automation,
distribution paths and check commands; this skill supplies the order of work.
A version argument chooses a version and does not authorize public actions.

Identify whether the user authorized preparation or publication. An explicit
publication request includes the necessary Release PR merge and draft
publication within that scope. Bypassing required approvals or changing GitHub
permissions needs specific authorization. Do not ask again for actions already
authorized.

## 1. Find the release

Preserve unrelated edits, refresh `origin/main`, and inspect the pending release:

```sh
gh pr list --label 'autorelease: pending' --state open
gh release list --limit 3
gh run list --workflow release-please.yml --limit 3
```

If no Release PR exists, inspect the workflow failure and the setting that lets
Actions create PRs. Do not change permissions or dispatch a workflow without
authorization. For a requested version, follow the `Release-As` procedure in the
release guide and confirm the pending PR reflects it.

## 2. Review the exact Release PR head

Pin the PR head SHA and review its version changes and changelog. Use
`agents-context-router-code-review` for the diff. Run the release guide's checks
against that exact head, including `scripts/check-version.py`, the router tests
and fixture. Confirm all configured version fields and source-version markers
agree. Check public skill behavior, README locales, native installation guidance
and migration notes against the release range.

Confirm CI covers that head. A bot-created PR may require a manually dispatched
Check workflow; a successful dispatch is not a completed check. Report the
version, user-visible changes, checks and any blockers before publication.

## 3. Merge and inspect the draft

Within the authorized scope, merge the reviewed head with
`gh pr merge NUMBER --squash --match-head-commit SHA`. Follow the resulting
Release Please run to completion and inspect the draft. Resolve the tag to its
commit, confirm it matches the tested merge revision and verify the Check jobs
for that revision passed. Do not substitute a prior head's green CI.

This repository ships Git source, not binary archives, npm or Homebrew. Inspect
the tagged manifests, public skill, scripts and templates. Run the tagged
router's `--version` and fixture check from an isolated checkout. Verify native
skill discovery with installed clients; report unavailable clients explicitly.

## 4. Write notes and publish

Prepare concise English user-facing release notes from the verified release
range. Include the concrete behavior changes, contributor credit, relevant
update commands, migration guidance and actual limitations. The generated
changelog is input, not finished release copy. Keep scratch notes outside tracked
files and use `--notes-file` when applying them to the draft.

Read the draft back with `gh release view TAG --json name,body,isDraft,targetCommitish`.
Confirm its title is exactly the tag, its body matches the reviewed notes and it
is still a draft. With publication authorized, publish that existing draft with
`gh release edit TAG --draft=false`, then read it back and verify the published
tag, title, body and source version. Do not create a replacement tag or release
to work around a failed check.

Report the release link, exact tag/SHA, version, executed checks and publication
state separately. Stop only when the authorized work is complete or a concrete
blocker requires user input or an external change.
