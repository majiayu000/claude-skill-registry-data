---
name: release
description: Walk the maintainer through a PPDS release by following docs/runbooks/release.md — scope advisory, CHANGELOGs, version bumps, the tag commands the maintainer runs, CI monitoring and publish verification. Use when preparing a prerelease, stable or patch release of the CLI, TUI, MCP, Extension or NuGet libraries.
---

# Release

The release procedure lives in [docs/runbooks/release.md](../../../docs/runbooks/release.md).
Read it in full, then follow it step by step. The model and policy it relies on
are in [docs/RELEASE.md](../../../docs/RELEASE.md). This skill adds only what is
specific to an agent doing the work; it does not restate the procedure.

## When to Use

- "Let's cut a release", "time for a new prerelease", "ship v1.x.0"
- A patch after a `release:patch` fix has merged
- A release issue opened by the release-check workflows

Not for implementing a hot-fix (open a PR first) or documentation-only changes.

Arguments: `/release` (prerelease, the default), `/release prerelease`, or
`/release stable v1.0.0` (stable, version given).

## Never Done by a Session

The maintainer creates and pushes every tag and makes every publication
([VERSIONING.md](../../../docs/VERSIONING.md#9-decisions-in-documents), rule
9.2). You prepare the release and verify it; you never run any of these, and the
maintainer's yes in chat does not change that:

- `git tag` for a release tag, and every tag push (`git push origin
  "refs/tags/..."`, `git push --tags`), including the unified `v*` tag
- every `gh release` write (`create`, `edit`, `upload`, `delete`, including of a
  draft)
- `gh workflow run` of `extension-publish.yml` or `docs-release.yml`, and any
  other publish or signing workflow
- `gh run rerun` of a publish or docs workflow
- anything that deletes, unlists, deprecates, moves or replaces a published tag,
  release or package

For each of these, prepare the exact command with the real versions and the full
hash of the commit it applies to (every `git tag` command names that hash), put it in a block headed **Maintainer runs**
(as the runbook does), hand it to the maintainer in chat, and wait for them to
say it has run. Then verify the result with the read-only probes below.

## Confirm With the User Before Running

Ask in chat and wait for an explicit yes, separately for each action.

- **Branches and PRs:** pushing a `release/prerelease-*`, `release/vX.Y.Z` or
  `release/X.Y` branch or `main`; deleting a remote branch
  (`git push origin :release/X.Y`); `gh pr create`, `gh pr ready`, merging
- **Issues and contributors:** commenting on or closing any issue (the
  co-release issue is the durable opt-out record), filing follow-up issues,
  sending a contributor reply, closing a contributor's original PR
- **The maintainer's machine:** `dotnet tool install -g`/`uninstall -g PPDS.Cli`
  (replaces their installed CLI) and `code --install-extension`

Reading state is fine without asking: `release_plan.py`, `gh run list`,
`gh release view`, `git tag -l`, the public verification probes.

## Working as an Agent

- Draft the per-package CHANGELOG entries in parallel if you can (one
  sub-agent per package, each given the package path and the commit range from
  runbook Step 3), then curate them yourself. Check every cited PR number with
  `gh pr view` before inserting it.
- For the stable-release security review gate, run `/security-review` on the
  diff since the last stable tag and save the result as the
  `docs/qa/security-review-*.md` artifact the runbook requires.
- Report each wave's public verification result before handing over the next
  wave's tag commands. Never batch waves to save time.
- If a step in the runbook is wrong or missing, propose the correction to
  docs/runbooks/release.md at the end of the release.
