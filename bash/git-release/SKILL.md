---
name: git-release
description: Use when preparing an approved user-run handoff for one annotated Git tag and matching GitHub release without changing branches or normal commits.
metadata:
  compatibility: Requires Git, GitHub CLI, and a shell capable of running the generated handoff script
---

# Git release

Prepare exactly one release handoff. The agent may inspect and validate, but it
must not create the tag, push, publish the release, change branches, commit,
stage, merge, rebase, reset, delete tags, force-push, or push normal commits.

## Accepted input

Accept no argument, `patch`, `minor`, `major`, or one explicit SemVer tag in
the form `vMAJOR.MINOR.PATCH`, with an optional prerelease or build suffix,
optionally with `--draft`. Reject other input. Treat a prerelease suffix and
draft status as intentional only when explicitly supplied, and pass
`--prerelease` for an explicitly supplied prerelease.

With `patch`, `minor`, `major`, or no argument, derive the next stable version
from the highest reachable exact `vMAJOR.MINOR.PATCH` tag. If none exists,
recommend `v1.0.0` and require it in the preview. Validate explicit versions,
and check the proposed tag locally, remotely, and in GitHub before continuing.

Read [preflight-and-notes.md](references/preflight-and-notes.md) for the
complete input, preflight, version-selection, validation, release-notes, and
approval contract.

## Read-only preflight

Before drafting the preview:

1. Inspect the current branch, regular and push `origin` URLs, and normalize
   them to one supported GitHub host/repository. Reject ambiguity, mismatch,
   userinfo in HTTPS URLs, unsupported hosts, or multiple push destinations.
2. Verify `gh` exists, authentication succeeds for that host, and
   `GH_REPO=<host>/<owner>/<repo> gh repo view` matches the remote.
3. Require a regular checkout, clean worktree, `origin` upstream, and `HEAD`
   exactly equal to the refreshed upstream tip. Release the primary branch by
   default; use another branch only when the user explicitly named it.
4. Inspect reachable tags and GitHub releases. Distinguish absence from an
   inspection failure. Refuse any existing local, remote, or GitHub release for
   the proposed version.
5. Discover and run the repository's authoritative validation command. Stop on
   failure.

Never infer a provider, repository, version baseline, or branch from ambiguous
evidence. Do not invoke `github-cli-workflow` as a release workflow.

## Notes and approval

Draft concise notes from the correct tag baseline using verified repository
evidence only. Show the complete preview: repository, branch, expected SHA,
exact URLs, previous/proposed version, validation result, title, full notes,
and the exact user-run mutations. Ask for approval of that exact preview and
stop until approval is explicit.

## Handoff

After approval, read [references/handoff.md](references/handoff.md), generate
the private release artifacts through Git metadata, and report their absolute
paths and the exact user command. Do not write release notes into the working
tree or leave a local tag. Validate the generated script with `bash -n` and
report the handoff as incomplete until the user runs it.

## Stop conditions

Stop on dirty state, branch/upstream drift, remote changes, tag or release
collision, missing authentication, validation failure, unsupported URL,
linked worktree, changed approved notes, or any uncertain inspection. Report
the blocking evidence and the next user action.
