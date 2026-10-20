---
name: release
description: >-
  Load this skill when shipping a version: bump, changelog, land it, tag, publish the GitHub
  release. Trigger on "cut a release", "bump the version", "tag a release", "hotfix", or a version
  field changing in a project manifest. Not for a branch with no version (use
  ceh-git-workflow:pull-request).
argument-hint: "[version]"
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Requires the git CLI on PATH, the GitHub CLI (`gh`) authenticated via `gh auth login`, a git
  repository with a GitHub remote, permission to push branches and tags, and network access.
license: Apache-2.0
---

# Release

Ships vX.Y.Z: the bump lands on `main` through a reviewed PR, and the tag and GitHub release
happen only after the merge, pointing at the merge commit, never at the feature branch.

## Procedure

Pick the path, then run it top to bottom. Each step gates the next.

| Situation                                           | Path                                |
| --------------------------------------------------- | ----------------------------------- |
| Ship a version (default)                            | [Full release](#full-release)       |
| The bump already merged to `main`, only tag + notes | [Tag and publish](#tag-and-publish) |
| P1/P2 production issue that cannot wait             | [Hotfix](#hotfix)                   |

### Full release

1. **Decide the bump** per the [bump table](#versioning). Never below the current version.
2. **Branch** `chore/release-vX.Y.Z` from up-to-date `main`.
3. **Bump** the version in every manifest the project ships. All must read the same vX.Y.Z.
4. **Changelog:** invoke the Skill tool with skill="ceh-git-workflow:update-changelog" to write
   the vX.Y.Z section. Gate: section written and semver-validated.
5. **Docs:** refresh the README per `ceh-git-workflow:update-readme` if the release is
   user-facing, and CLAUDE.md if project facts changed. Otherwise record "no update needed".
6. **Commit** with the [release commit message](#release-commit-message). Tree clean.
7. **Land** the branch: open the PR and merge it per `ceh-git-workflow:pull-request`. Gate: CI
   green, approvals met, merged to `main`.
8. **Tag and publish** per [Tag and publish](#tag-and-publish).

### Tag and publish

On `main`, after the merge:

```bash
git checkout main && git pull origin main   # the merge commit is now HEAD
git tag -a vX.Y.Z -m "vX.Y.Z — <summary>"   # annotated: some repos reject lightweight tags
git push origin vX.Y.Z
gh release create vX.Y.Z --title "vX.Y.Z" --notes-file notes.md && rm notes.md
```

`notes.md` is the vX.Y.Z changelog section plus the attribution footer (see
[Attribution](#attribution)).

### Hotfix

The [Full release](#full-release) with these differences:

1. Branch `fix/critical-<description>` from `main`, and commit the fix itself as
   `fix(<scope>): <description>`. Minimal scope: nothing unrelated rides along.
2. The bump is PATCH. It may commit on the same branch after the fix.
3. Review is fast-tracked to 1 approval, but CI must pass. A broken hotfix is worse than a delayed
   one.
4. The PR body links the incident and names the symptom, so the merge commit explains itself.
5. After publishing, deploy staging then production (both, however abbreviated), because a rushed
   fix that skips staging can ship a second failure straight to production. Confirm the
   symptom is gone and error rates are back to baseline before declaring the incident resolved,
   and be ready to roll back. A P1/P2 gets a post-mortem within 48 hours.

## Rules

### Versioning

Tags are `v<major>.<minor>.<patch>`.

| Change                                                  | Bump  |
| ------------------------------------------------------- | ----- |
| Breaking change (`BREAKING CHANGE:` footer or `!` type) | MAJOR |
| New backward-compatible feature                         | MINOR |
| Fixes, chores, docs, refactors                          | PATCH |

When in doubt, PATCH. Versions only increase. Pre-releases take a suffix (`v1.4.0-rc.1`,
`v1.4.0-beta.1`) and sort below the final `v1.4.0`.

### Gates

- One version everywhere: every manifest reads the same vX.Y.Z before the commit.
- Tag the merge commit on `main`, never the feature branch, because the tag must name the tree
  that passed the gate on `main`: `git pull origin main` first.
- Never tag or release on a red gate. Surface it and wait.

### Attribution

| Artifact             | Setting              | Where the footer goes           |
| -------------------- | -------------------- | ------------------------------- |
| Release commit       | `attribution.commit` | Last line of the commit message |
| GitHub release notes | `attribution.pr`     | Last line of the notes file     |

Reproduce the line the session's Git instructions supply, verbatim. Never substitute a literal
from this skill or from memory. If the setting is empty, omit it. The tag message takes none.

## Output

### Release commit message

The release commit is where the diff explains least: it shows version strings and changelog prose,
not what shipped or why the bump is that level. Always multi-line, written to a temp file and
committed with `git commit -F`, never `-m`:

```
chore: release vX.Y.Z

<1-3 sentences: what this release ships, in the changelog's terms>

- Bump: <PATCH|MINOR|MAJOR>: <the change that forces this level>
- Manifests: <which moved, old -> new>
- Docs: <changelog / README / CLAUDE.md updated, or "no update needed" and why>

<attribution footer>
```

## Stop conditions

- Bump level unclear between MINOR and MAJOR → state the breaking candidate and ask. With no human
  to answer, take MAJOR and say why, because an unflagged break costs users more than an extra
  major version.
- CI red or approvals missing at step 7 → surface it and wait. Never tag around it.
- No human present and no standing authorization to publish → prepare everything up to the tag,
  then stop and report. Tagging and publishing are outward-facing and cannot be taken back.

## Hands off to

- Invoke the Skill tool with skill="ceh-git-workflow:update-changelog" to write the vX.Y.Z
  section at step 4 of [Full release](#full-release).
