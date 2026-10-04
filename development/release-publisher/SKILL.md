---
name: release-publisher
description: "Publish a new Canvas Notebook release. Use this skill whenever the user asks to bump a version, prepare release notes, update CHANGELOG.md, create or push a git tag, publish a GitHub Release, deploy, or automate the release workflow. This skill covers the full release sequence for this repository: inspect commits/tags, push completed product-code commits first when authorized, confirm the pushed code has built on GitHub, choose the next calendar version, update package and CLI versions, update the changelog, run the required local build, commit, push the release commit, wait for the remote Build and Push worker on the pushed branch, tag, push the tag, and publish the release."
metadata:
  version: "1.0"
  author: canvas-studios
---

# Release Publisher

Use this skill to publish Canvas Notebook releases consistently.

## Guardrails

- Read the repository instructions first, especially `AGENTS.md` if present.
- Do not build containers locally unless the user explicitly asks. A user request to publish, deploy, or complete a release is explicit permission to run the remote GitHub `Build and Push` workflow required by this release process.
- Do not start multiple dev or test containers.
- Do not use Playwright unless the user explicitly asks or approves it.
- Do not push the branch unless the user explicitly asks. A request to publish, deploy, or complete a release counts as explicit permission to push the branch, push the release tag, and publish the GitHub Release as required by this workflow. When the user explicitly asks to deploy or push, push completed product-code commits before release-prep commits so CI builds the real source state before any release tag is created.
- Keep user changes intact. If unrelated working tree changes exist, do not overwrite them.
- Commit finished release-prep work before moving to tag or publish steps.
- Do not create or push a release tag until the release commit itself has been pushed to the remote branch and the pushed branch has completed the remote Build and Push worker successfully.
- Do not rely on pushing a tag to upload unpublished local commits. `origin/main` must already point at the release commit before a tag is created or pushed.
- Do not create the GitHub Release manually with `gh release create`. The `build-both.yml` workflow creates the GitHub Release and uploads all assets as part of the tag-triggered build. Creating the release early causes the `Notify Control Plane Release` workflow to run before assets exist and fail.

## Versioning

Canvas Notebook uses calendar-style versions:

```text
YYYY.M.D.N
```

Example for the first release on June 6, 2026:

```text
2026.6.6.1
```

Tag names use a leading `v`:

```text
v2026.6.6.1
```

Choose the next version by:

1. Reading the current date.
2. Listing existing tags sorted by creation date and version.
3. If today already has releases, increment the final counter.
4. Otherwise use counter `1`.

## Required Files

Update all of these when bumping the release version:

- `package.json`
- `package-lock.json`
- `install/bin/canvas-notebook`
- `install/lib/shared/output.sh`
- `CHANGELOG.md`

The CLI version lines are:

```bash
CANVAS_CLI_VERSION="VERSION"
CANVAS_CLI_VERSION="${CANVAS_CLI_VERSION:-VERSION}"
```

Because the project uses four-part calendar versions, `npm version` may reject the version. If so, update `package.json` and `package-lock.json` directly with a structured edit.

## Workflow

### 1. Inspect State

Run:

```bash
git status --short --branch
git log --oneline -n 20
git tag --sort=-creatordate --format='%(refname:short) %(creatordate:short) %(subject)' | head -30
```

Check:

- Current branch.
- Whether the tree is clean.
- Whether `main` is ahead of `origin/main`.
- Latest release tag.
- Current version in `package.json`.
- CLI version in `install/bin/canvas-notebook` and `install/lib/shared/output.sh`.

If the tree has unrelated changes, either work around them or ask before touching those files.

### 2. Push Product Code Before Release Prep

When the branch is ahead of the remote and the user asked to deploy/push:

1. Separate already-finished product-code commits from release-prep commits.
2. If a previous local release-prep commit/tag was never pushed or built remotely, treat it as unpublished. Do not publish that stale tag by default.
3. Push the branch before creating a new version/changelog release commit:

```bash
git push origin CURRENT_BRANCH
```

4. Confirm the pushed commit is visible on GitHub:

```bash
git ls-remote origin refs/heads/CURRENT_BRANCH
```

5. Confirm GitHub has built the pushed code before continuing. Use the repo's available workflow:

```bash
gh run list --repo canvascoding/canvas-notebook --limit 10
```

Canvas Notebook's `Build and Push` workflow does not run automatically on branch pushes; it runs on tags, schedule, or `workflow_dispatch`. If the current release/deploy request authorizes remote release work, manually dispatch `Build and Push` on the pushed branch and wait for success before continuing:

```bash
gh workflow run build-and-push.yml --repo canvascoding/canvas-notebook --ref CURRENT_BRANCH
gh run list --repo canvascoding/canvas-notebook --workflow "Build and Push" --branch CURRENT_BRANCH --limit 5
gh run watch RUN_ID --repo canvascoding/canvas-notebook --exit-status
```

Expect the GitHub Actions build/push worker to take about 8-10 minutes. Continue only after the relevant remote run succeeds, or after the user explicitly accepts continuing without a remote branch build.

### 3. Summarize Changes Since Last Published Tag

Use the previous published release tag as the base. If the latest local tag was never pushed to the remote and never built on GitHub, skip it and use the latest remote/published tag instead:

```bash
git log --reverse --pretty=format:'- %s' PREVIOUS_TAG..HEAD
git show --stat --oneline PREVIOUS_TAG..HEAD
```

Convert raw commit subjects into user-facing release notes. Prefer categories:

- `Added`
- `Changed`
- `Fixed`
- `Security`
- `Verification`

Avoid dumping every tiny commit into the public release body unless the user asks for exhaustive notes.

### 4. Update CHANGELOG.md

Maintain `CHANGELOG.md` using Keep a Changelog style:

```markdown
## [Unreleased]

### Added

- Nothing yet.

## [VERSION] - YYYY-MM-DD

### Added

- ...
```

For a new release:

1. Add a new version section directly below `Unreleased`.
2. Move relevant unreleased items into that section if any exist.
3. Add release notes based on commits since the last tag.
4. Add `### Verification` with the commands actually run.

If an unpublished local release section exists, merge its relevant notes into the new release section instead of publishing a stale version.

### 5. Update Versions

Update:

- Root package version.
- Lockfile root version and package entry version.
- CLI version constant.
- Shared CLI output fallback.

Then verify:

```bash
rg -n 'OLD_VERSION|NEW_VERSION|CANVAS_CLI_VERSION' package.json package-lock.json install/bin/canvas-notebook install/lib/shared/output.sh
git diff --check
```

### 6. Build Before Release Commit

Always run the production build before committing and tagging a release:

```bash
npm run build
```

If the build injects the CLI version, confirm the injected version matches the new version.

For UI or end-to-end behavior changes, follow the repository instructions. If Playwright is required but the user did not explicitly authorize it, ask before using it.

### 7. Commit Release Prep

Commit the changelog and version bump together unless the user asks for separate commits:

```bash
git add CHANGELOG.md package.json package-lock.json install/bin/canvas-notebook install/lib/shared/output.sh
git commit -m "Prepare release VERSION"
```

Do not include unrelated files.

### 8. Push Release Commit

Push the release-prep commit before creating the tag:

```bash
git push origin CURRENT_BRANCH
git ls-remote origin refs/heads/CURRENT_BRANCH
git status --short --branch
```

If the push fails, stop. Do not create the tag or GitHub Release.

Confirm `origin/CURRENT_BRANCH` points at the release commit and the local branch is no longer ahead. If the release commit is not visible on the remote branch, stop.

### 8.5. Build Pushed Branch Before Tagging

After the release commit is visible on `origin/CURRENT_BRANCH`, run the remote Build and Push worker on that branch before creating or pushing any tag. This updates the deployed/latest image from the branch commit first, so the GitHub Release is not described while `main` still points at old code.

```bash
gh workflow run build-and-push.yml --repo canvascoding/canvas-notebook --ref CURRENT_BRANCH
gh run list --repo canvascoding/canvas-notebook --workflow "Build and Push" --branch CURRENT_BRANCH --limit 5
gh run watch RUN_ID --repo canvascoding/canvas-notebook --exit-status
```

Record the run URL/ID and result for the final report and the release notes verification section if appropriate. Expect this remote build to take about 8-10 minutes. If the workflow fails, stop before creating the tag or GitHub Release and inspect/fix the failure.

### 9. Create Annotated Tag

Create an annotated tag on the release commit only after the pushed-branch Build and Push run has succeeded:

```bash
git tag -a vVERSION -m "Canvas Notebook VERSION"
git show --no-patch --pretty=fuller vVERSION
```

If the tag already exists, stop and inspect. Do not overwrite a published tag unless the user explicitly instructs you to.

### 10. Push Tag

Push the tag only after the release commit is visible on the remote branch:

```bash
git push origin vVERSION
```

If the local branch is ahead of `origin/main`, stop and resolve that first. The tag must point to a commit reachable from the remote branch.

After pushing the tag, confirm the tag is visible remotely:

```bash
git ls-remote origin refs/tags/vVERSION refs/tags/vVERSION^{}
```

The tag push will trigger another `Build and Push` run for the versioned tag. Track that run separately from the pre-tag branch run and report its status.

### 11. GitHub Release Is Created by CI

Do **not** run `gh release create` manually. The `build-both.yml` workflow's `merge` job creates the GitHub Release automatically after the multi-arch image manifest is built and the CLI/compliance assets are packaged. The release is published with auto-generated notes, which is acceptable because the changelog lives in `CHANGELOG.md`.

After the tag-triggered `Build and Push` run succeeds, verify that the release exists and contains the expected assets:

```bash
gh api "repos/canvascoding/canvas-notebook/releases/tags/vVERSION" --jq '.tag_name, .name, (.assets | map(.name))'
```

The `Notify Control Plane Release` workflow will run automatically once the release is published by CI.

### 12. Final Report

Report:

- Version.
- Commit hash.
- Tag.
- Release URL.
- Verification commands and result.
- Remote branch push status.
- Pre-tag pushed-branch Build and Push run URL/ID/status.
- Tag-triggered Build and Push run URL/ID/status, if the tag was pushed.

Keep the final response short and factual.

## Failure Handling

- If `npm run build` fails, stop before committing/tagging and fix the failure if it is in scope.
- If `gh auth status` fails, stop before release creation and tell the user what credential is missing.
- If pushing the tag fails, do not create the GitHub Release until the tag is visible on GitHub.
- If the tag-triggered `Build and Push` run fails, do not attempt to create or fix the GitHub Release manually. Fix the build failure and restart the release process from the tag push.
- If the CI-created release is missing assets, inspect the `merge` job logs of the tag-triggered `Build and Push` run; the workflow handles release creation and asset upload there.