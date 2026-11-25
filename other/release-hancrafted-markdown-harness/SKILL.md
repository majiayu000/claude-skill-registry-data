---
name: release
description:
  Cut and publish the next version of @hancrafted/markdown-harness. Releases are tag-driven — bump the version, push a
  vX.Y.Z tag, and GitHub Actions publishes to npm over trusted publishing (OIDC). This skill drafts release notes from
  the commit log and stops at a review gate for approval before anything publishes. Use when the user wants to release,
  publish a new version, ship, bump the version, or push a release tag.
---

A `v*` tag is the only thing that publishes. Merging to `main` publishes nothing.

The mechanics are a contract that must work with no skill installed:
[`docs/agents/release.md`](../../../docs/agents/release.md). This skill sits on top of that path — drafting notes,
judging the bump, holding a review gate — and never replaces it. **When a step here disagrees with that page, that page
wins and this file is what needs fixing.** Consult it whenever a step below surprises you.

Nothing publishes until the user approves a version and notes at the **review gate** (step 3). Work the steps in order;
each ends on a criterion you check before moving on.

## 1. Pre-flight

Every gate below is a hard stop, not a warning:

1. On an up-to-date trunk. Run `git worktree list` first: this repo keeps several worktrees, and when one of
   them holds `main`, `git checkout main` does not switch — it fails with `'main' is already used by worktree
at ...`. Work from the checkout that holds `main` and `git pull` there, rather than switching to it.
2. Working tree clean: `git status --porcelain` prints nothing.
3. `npm run verify` exits 0. Run the whole thing, in this order, not a subset — `verify` builds before it tests, and
   `tsc --noEmit` runs before `vitest`, which never typechecks anything (docs/agents/verification.md, traps 8 and 9).
4. CI is green on `main` in the Actions tab. Publish re-runs `verify` and the same Trivy gate, but catch it here.

**Do not read a green `archgate check` inside step 3 as governance evidence.** It is scoped to the files changed against
`origin/main`, so on an up-to-date trunk its scope is empty by construction and it passes over zero rules. It is in
`verify` because it belongs in `verify`; it tells you nothing at release time.

**Done when:** all four gates pass.

## 2. Draft the notes and propose a version

1. Find the last release tag: `git describe --tags --abbrev=0`. If the command fails there is no prior tag, and this is
   the first real release — that is a `minor`, because `0.0.x` means "not a release".
2. Gather every commit since it: `git log --no-merges <last-tag>..HEAD --pretty=format:'%h %s'`.
3. Group them under the Keep a Changelog categories the commit bodies already use — `Added`, `Changed`, `Deprecated`,
   `Removed`, `Fixed`, `Security`.
4. Propose `vX.Y.Z`. The package stays in `0.x` until the command surface is deliberately declared stable, so most
   releases are `patch` or `minor`. Anything that moves `bin`, an exit code, the response envelope or the supported Node
   range is breaking for an adopter whatever the number says — say so in the notes.

**Never propose a prerelease.** `publish.yml` passes no `--tag`, and npm refuses a prerelease version under the default
tag, so a `v0.1.0-rc.1` tag fails the publish step outright. Release candidates are not a way to rehearse this pipeline;
enabling them means giving that step a `--tag`, deliberately, as its own change.

**Done when:** you have proposed a `vX.Y.Z` and grouped notes that account for every commit since the last tag.

## 3. Review gate — approve before releasing

Show the user the proposed `vX.Y.Z` and the full notes, then **stop and wait**. Advance to step 4 only once the user
explicitly approves both. If they change the bump or edit the notes, revise and show the updated version and notes
again.

Approving here authorises the push in step 4. That push is the irreversible act: published versions are immutable, and a
tag that reaches the remote fires Publish.

**Done when:** the user has approved a specific version and specific notes.

## 4. Cut the release

```bash
npm version <patch|minor|major> --no-git-tag-version   # bumps package.json + package-lock.json; no commit, no tag
# commit both files with the `commit` skill — see the second warning below
git tag -a vX.Y.Z -m "vX.Y.Z"                          # ANNOTATED — see the first warning below
git push --follow-tags                                 # pushes the commit AND the tag, firing Publish
git ls-remote --tags origin | grep vX.Y.Z              # prove the tag landed; no tag, no publish
```

Three ways this step fails, two of them silently:

- **`git push --follow-tags` pushes annotated tags only.** A lightweight tag — `git tag vX.Y.Z`, no `-a` — is skipped
  without a word. The push prints `main -> main`, exits `0`, and Publish never fires: the release looks finished and
  nothing reached npm. That is what the `-a` and the `ls-remote` line are for. Do not read a clean push as proof.
- **The commit-msg gate rejects a bare release commit.** It requires a Keep a Changelog `### <category>` section with at
  least one numbered item, plus a `Source:` trailer, so `git commit -m "chore(release): 0.2.0"` is refused. Use the
  `commit` skill, which writes a conforming message and runs the gate before committing.
- **A tag that disagrees with the manifest is refused, loudly.** `publish.yml`'s first step compares
  `GITHUB_REF_NAME` against `package.json`'s version and aborts before `npm ci`. This is a backstop for forgetting the
  bump, not a step to lean on — it costs a failed run and a re-tag.

**Done when:** `git ls-remote --tags origin` lists the `vX.Y.Z` tag.

## 5. Watch Publish

The **Publish** workflow fires on the tag: it re-runs `npm run verify` and the same HIGH/CRITICAL Trivy gate
`security.yml` applies, then publishes over OIDC with provenance attached. A red verify, a red scan or a failed build
aborts before anything reaches the registry.

A job-level `success` is not per-step evidence. If a step's outcome matters, read that step — a step skipped by an `if:`
also reports `success`.

**Done when:** the Publish run for the tag is green in the Actions tab.

## 6. Verify and record the notes

1. The registry agrees: `npm view @hancrafted/markdown-harness version` reports the tag you cut.
2. The npm package page shows a **provenance** attestation. A manual publish cannot produce one, so its absence means
   the version did not come from the workflow.
3. Publish the approved notes as a GitHub Release. Write them to a file first so multi-line markdown survives:
   `gh release create vX.Y.Z --title vX.Y.Z --notes-file <file>`.

**Done when:** the registry reports the new version and its GitHub Release carries the approved notes.

If anything went wrong, **never overwrite a published version** — bump again and re-tag. Troubleshooting is in
[`docs/agents/release.md`](../../../docs/agents/release.md).
