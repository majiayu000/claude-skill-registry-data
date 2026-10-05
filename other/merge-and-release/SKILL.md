---
name: merge-and-release
description: "Reference document describing merge prerequisites (approval, CI checks, mergeable, conversations resolved, stale approval), release versioning (semantic semver), and changelog generation. Explains why Tier 3 confirmation is structural: merge and release cost is borne by downstream people. Reference only (`disable-model-invocation: true`); consumed by `/flow:merge` and `/flow:release`."
allowed-tools: Read
agent: Explore
disable-model-invocation: true
---

# Merge and Release

Policy reference for `/flow:merge` and `/flow:release`; the runnable bash lives in `commands/merge.md` and `commands/release.md`.

## Contract

Iron law: **merge is irreversible in practice — every prerequisite is verified with fresh evidence, never memory, and merge and release are Tier 3 (explicit human confirmation, even in autonomous mode).** Consumed by `/flow:merge` Phase 1 (five-check gate plus finding-ledger check), Phase 2 (Merge Assessment), Phase 3 (confirm and execute), Phase 4 (post-merge), and by `/flow:release` Phases 2–5 (version, changelog, confirm and execute, post-release). Returns the checks, stop conditions, settings, and execution sequence those commands apply. Permitted skips: none — a failed prerequisite stops the command without asking "merge anyway?"; an override happens only by the human acting outside the command.

## Five-Check Gate (`/flow:merge` Phase 1)

| # | Check | Requirement |
|---|-------|-------------|
| 1 | Approval | At least one approval, no outstanding requested changes |
| 2 | CI checks | `statusCheckRollup` all success |
| 3 | Mergeable | `mergeable == "MERGEABLE"` |
| 4 | Conversations | Unresolved review threads == 0 (GraphQL `reviewThreads`; the REST field is incomplete) |
| 5 | Stale approval | No commits after the last approval timestamp |

Plus the `pr-lifecycle` finding-ledger check: non-empty `ESCALATED` or unmatched `FINDINGS` blocks.

**Stale approval**: compare the latest `submittedAt` among reviews with `state == "APPROVED"` against the `committedDate` of the newest commit. Commits after approval: warn "Approval may be stale", request re-review, do not merge — the approver has not seen what would be merged.

## Stop Conditions

Any prerequisite fails, stale approval, unresolved conversations > 0, unfinished checks, or ledger gate fails: stop. No "override the gate" option exists in autonomous mode. Never `--auto`: it waits only for *required* checks (`commands/merge.md`).

## Merge Execution (Phases 2–4)

Display the Merge Assessment table (each prerequisite's status, strategy, branch-delete decision), then ask; proceed only on a clear "yes".

- `merge.strategy`: `squash` | `merge` | `rebase` (default `squash`)
- `merge.deleteBranch`: default `true`, bundled into the merge confirmation
- `merge.markerTrust.allowedAssociations`: default `["OWNER","MEMBER","COLLABORATOR"]`; filters whose ledger markers are honored, pinned to the plugin tier rather than the settings cascade (`references/finding-ledger-parser.md`)

Post-merge: `gh pr view $PR_NUM --json state` must return `MERGED`; then suggest switching to the default branch and pulling.

## Release (`/flow:release`)

**Version** (Phase 2): tag = `release.tagPrefix` (default `v`) + version.

| Bump | Format | When |
|------|--------|------|
| `patch` | 0.0.X+1 | Bug fixes only, no behavior change |
| `minor` | 0.X+1.0 | New features, no breaking changes |
| `major` | X+1.0.0 | Breaking changes |

No prior tag: first release is `v1.0.0`.

**Changelog** (Phase 3): merged PRs since the last tag, grouped by conventional prefix — Features (`feat:`), Bug Fixes (`fix:`), Other Changes (`docs:`, `chore:`, …) — each with PR number and author, plus a "Full Changelog" compare link `{prev}...{new}`.

**Execute** (Phase 4): show the Release Preview (version, previous tag, PR count, changelog), confirm via `AskUserQuestion`, then in one sequence:

```bash
git tag -a "$TAG" -m "Release $TAG"
git push origin "$TAG"
gh release create "$TAG" --title "$TAG" --notes "$CHANGELOG"
```

One confirmation covers all three; they are never split across turns.

**Post-release** (Phase 5): `gh release view "$TAG"` must succeed; suggest updating plugin version files if applicable.

## Why Tier 3 Is Structural

An unwanted merge or release is paid for by people outside this conversation; only the human in the loop can speak for them.

## Keeping Policy and Bash Aligned

Merge prerequisites and execution: `commands/merge.md`. Version, tagging, GitHub release: `commands/release.md`. A new prerequisite, strategy, or versioning rule changes the command and this reference together.
