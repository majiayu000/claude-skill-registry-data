---
name: gaia-release
description: >-
  Helper for release operations, compilation of changelogs between tags, version lockstep syncing,
  and promotion of GitHub releases from canary/pre-release to latest/production. Use when the user asks to
  "compile the changelog", "promote release to latest", "tag a release", or do version release operations.
version: 1.0.0
---

# gaia-release

A skill for managing releases, compiling changelogs across tags, verifying version lockstep, and promoting releases from canary/beta to latest/production.

## When to invoke

Trigger when the user requests release operations, including:
- "Compile the changelog from previous latest" / "generate release notes"
- "Mark tag vX.Y.Z as Latest" / "promote release to latest"
- "Update release notes on GitHub"
- Release bump checks and tag auditing

Do NOT use for:
- Standard git branch merging (use standard git procedures)
- Regular document sync routines (use `gaia-docs-sync` or similar)

## Operating Contract

### 1. Compile Changelogs
To compile a changelog from a previous version/tag to the target tag:
1. Fetch all tags from remote to ensure your local tag list is up-to-date:
   ```bash
   git fetch --tags
   ```
2. Find the commits and tags between the starting tag and the target tag:
   ```bash
   git log <start_tag>..<target_tag> --decorate --oneline
   ```
3. Group commits by their release tags and format them into readable changelog groups:
   - **Features** (`feat:`, `chore:`, etc.)
   - **Bug Fixes** (`fix:`, etc.)
   - **Documentation** (`docs:`, etc.)
   - **CI / Testing / Housekeeping** (`infra:`, `test:`, etc.)
4. Keep the list concise and link to the relevant Pull Requests or Issues.

### 2. Verify / Sync Version Lockstep
If requested to update version files:
1. The three manifest files must remain in lockstep:
   - `pyproject.toml`
   - `packages/cli-npm/package.json`
   - `registry/gaia.json` (gitignored pipeline-internal, but updated locally)
2. Use `python3 scripts/verify_lockstep.py` to check current lockstep alignment.
3. Sync versions using:
   ```bash
   gaia dev release <patch|minor|major> --sync
   ```
   Or if not bumping and only syncing manifests to the highest version:
   ```bash
   python3 -m gaia_cli.main dev release --sync
   ```

### 3. Promote GitHub Release to Latest / Production

> **⚠️ Ancestry guard (mandatory — issue: split-brain release state).**
> Before promoting **or** publishing any tag, verify the tag's commit is an
> ancestor of `main`. Promoting/publishing a tag whose commit never landed on
> `main` desyncs the published version from the branch manifests, which makes
> `sync-artifacts.yml` recompute the *same* patch version on every subsequent
> merge and hard-fail on `fatal: tag 'vX.Y.Z' already exists` (this is exactly
> what happened with `v6.8.9`). Run this and **abort** if it fails:
>
> ```bash
> git fetch --tags origin main
> if ! git merge-base --is-ancestor "$(git rev-list -n1 <tag>)" origin/main; then
>   echo "ABORT: <tag> commit is not on main — land the version-bump commit first."
>   exit 1
> fi
> ```
>
> If the tag is legitimately ahead of `main` (e.g. the release commit is still
> in flight), do **not** promote/publish yet — merge the bump to `main` first,
> or reconcile `main`'s manifests to the tag version so the branch owns it.

To change a canary or beta release to the latest production release on GitHub:
1. Generate the changelog/notes in a markdown file (e.g. `generated-output/changelog_vX.Y.Z.md`).
2. Run the `gh release edit` command with the appropriate flags to update the title, remove the prerelease flag, mark it as latest, and upload the notes:
   ```bash
   gh release edit <tag> --title "<tag>" --prerelease=false --latest --notes-file <path_to_notes.md>
   ```
3. Run `gh release view <tag>` to verify that the release shows `prerelease: false` and the title/notes are correct.

### 4. Manually Publish to PyPI
If the release needs to be manually published to PyPI (e.g., when bypassing automated CI triggers or for manual publication control):

> **⚠️ Apply the same ancestry guard from §3 first.** Publishing a version to
> PyPI that `main`'s `pyproject.toml` does not carry is unrecoverable (PyPI
> versions are immutable) and strands `main` behind the published version. Only
> publish when `main`'s version ≥ the version being published.
>
1. Use the GitHub CLI to trigger the `Publish gaia-cli to PyPI` workflow manually. Specify the `main` branch as the reference, which will build the version defined in `pyproject.toml` on the `main` branch:
   ```bash
   gh workflow run publish-pypi.yml --ref main
   ```
2. Monitor the run to confirm that the build and publish steps complete successfully.

### 5. Code Change Constraint
- Always respect user instructions regarding code changes. If the user states "commit no code" or "just do the tagging and release," perform all tag/release modifications on GitHub directly using `gh` CLI commands and output the compiled changelog text in the chat, rather than committing edits to `CHANGELOG.md`.

## Example Invocation

```
User: Work on tag v5.4.10 and change it as Latest. Compile the CHangelog from previous latest. I will be publishing it to pypi.
Agent:
  1. Fetches tags and inspects commits between v5.1.1 and v5.4.10.
  2. Compiles a detailed changelog grouped by release.
  3. Uses `gh release edit v5.4.10 --title "v5.4.10" --prerelease=false --latest --notes-file generated-output/changelog_v5.4.10.md` to promote the release to Latest.
  4. Verifies the status using `gh release view`.
  5. Presents the changelog to the user and confirms the release update.
```
