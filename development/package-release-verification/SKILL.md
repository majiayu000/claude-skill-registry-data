---
name: package-release-verification
description: >-
  Cut a versioned package release and verify the registry serves the intended version. When
  publishing X.Y.Z or npm still shows an old version, check the changelog, tag or dispatch, passing
  gates on the exact release commit, and package provenance if claimed. Not for gdd.
metadata:
  revision: "3"
  areas: "software-development"
  targets: "runtime-agnostic"
  summary: "changelog → gate-on-the-same-commit → dispatch → per-version registry check → approved cleanup"
  summary_zh: "发版：先补 changelog、同一 commit 的门禁、分派、按版本号核 registry、单独获批的清理"
  kind: "entry"
---

# Package release verification

Merging is not shipping. A release is complete when the registry serves the version you intended, with
provenance if the repo claims it, and the release commit is the one your gates ran on. Not for landing the
increment itself — that is the merge phase of `gdd`.

## When to Use

- "Cut the release", "打一个版本", "publish X.Y.Z", "why does npm still show the old version?".
- A repo whose release runs from a workflow dispatch or a tag, especially one that moves the changelog and
  publishes with provenance.
- After a merge, when the increment is packaged and the question is whether it actually shipped.

Not for landing code (merge is a different phase), and not for a deliverable that is a service you reload
rather than a versioned package.

## 1. Prepare the release notes before you dispatch

Release workflows usually move an `Unreleased` changelog section under the new version and commit only
`package.json` plus `CHANGELOG.md` — deliberately, so a release cannot carry unreviewed code. Therefore:

- Read the release workflow first: which files its tag/commit job allows, and what it refuses.
- Confirm the section it consumes (`## [Unreleased]` or equivalent) states the headline feature of this
  increment. An empty or missing entry ships a version whose notes omit what justified it.
- Land that changelog edit through the normal PR path *before* dispatching.
- Move doc pin examples (`@vX.Y.Z`, install snippets) only after the tag exists, ideally in the same
  follow-up docs PR as the goal/status update.

## 2. Dispatch only from a commit whose gate run is green

Tag-release workflows commonly refuse to run unless the default branch has a **push** gate run for the
exact commit — a PR run does not count, and a squash-merge commit is a new SHA.

1. Merge, then `git fetch && git merge --ff-only origin/main`.
2. `gh run list --workflow <verify>.yml --commit $(git rev-parse HEAD) --event push --limit 1` and wait for
   `completed/success`. A missing run one commit after a previous release is normal when the release bot's
   own push starts no workflow — land the next human commit before releasing again.
3. `gh workflow run <release>.yml -f level=patch` (or the repo's equivalent). Watch the version/tag job,
   then the publish job it dispatches on the tag.

Confirm in the publish log that the job re-ran the gates on the tag's tree before the registry saw a byte.
If it did not, treat the tag as unverified and run the gates yourself.

## 3. Verify at the registry, per version

This is the step that matters and the one that is easy to get wrong.

- Query the **version manifest**, not the package summary:
  `curl -s -o /dev/null -w '%{http_code}' https://registry.npmjs.org/<scope>%2F<name>/<version>` → `200`.
  Other ecosystems: the equivalent per-version endpoint.
- Query `dist-tags` separately (`https://registry.npmjs.org/-/package/<pkg>/dist-tags`); `latest` is what
  lags, so it is the wrong gate on its own.
- Compare the registry's `dist.shasum` with the shasum the publish log printed — that is how you prove the
  bytes you checked are the bytes that shipped.
- If the repo claims provenance, require `dist.attestations` with
  `predicateType: https://slsa.dev/provenance/v1` and keep the transparency-log index from the log.
- A 404 on the version manifest right after a successful publish is **expected**: npm prints `Your package
  is being processed and may take a few minutes to become available`. Poll the version endpoint every
  30–45 s; `npm view <pkg> version` showing the previous version in that window is the same lag through a
  different endpoint.

## 4. Clean up only after the release is verified

Deleting the release branch, removing a worktree and deleting a local branch are destructive and belong in
their **own** command, after an approval that names all three. Never bundle them with read-only
verification: when such a bundle is blocked or times out, the safe reads are lost with it and the retry is
ambiguous about what actually ran. Check `git status --porcelain` is empty and that needed artifacts
(reports, tarballs, logs) live outside the worktree before removing it.

## Output shape

1. One line: `version X.Y.Z published` or `not published, blocked at <step>`.
2. Registry evidence: manifest status, dist-tag, shasum match, attestation type.
3. What was NOT verified (live provider round trip, platform matrix, downstream install) stated as a gap,
   never folded into "released successfully".

## Pitfalls

- Judging a publish by `latest` or by `npm view <pkg> version` within minutes of the dispatch; the log's
  own notice already said processing takes a few minutes.
- Reading `+ pkg@version` in the log as proof the registry serves it: that means npm accepted the upload,
  not that replication finished.
- Releasing with an empty changelog section, so the version's notes omit the feature that justified it.
- Dispatching from a commit whose only gate run is the PR's, then reading the workflow's refusal as a
  transient failure.
- Leaving doc pin examples on the previous tag, or updating them before the tag exists.
- Bundling branch/worktree deletion with verification commands, and losing the verification when the
  destructive part is blocked.
