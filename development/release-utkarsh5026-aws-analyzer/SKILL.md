---
name: release
description: Publish a new version of aws-analyzer to PyPI - check what's on main since the last release, write its CHANGELOG entry, pick the version, open a release pull request, and once the user confirms, merge it and publish the GitHub release that uploads to PyPI. Use when the user asks to release, publish, ship or cut a version, or to push their changes to PyPI.
argument-hint: "[patch | minor | major | 0.2.0]"
allowed-tools: Bash(.venv/bin/python .claude/skills/release/release.py:*), Bash(python .claude/skills/release/release.py:*), Bash(git fetch:*), Bash(git log:*), Bash(git diff:*), Bash(git status:*), Bash(gh pr view:*), Bash(gh pr checks:*), Bash(gh run list:*), Bash(gh run view:*), Bash(gh run watch:*)
---

# Release

Ship what's on `main` to PyPI as a new version. Publishing is the one step here that can't be undone: PyPI never
takes the same version twice, even after it's deleted. So everything up to the release pull request is safe to
redo, and the user confirms before anything is merged or published.

How it's wired (see "The PyPI package" in CLAUDE.md): a GitHub release tagged `v<version>` starts
`.github/workflows/release.yml`, which builds, checks, refuses a tag that doesn't match `__version__`, and uploads
with trusted publishing from the `pypi` environment. `release.py` does the mechanical parts. Use `.venv/bin/python`
if it exists, otherwise `python`.

## 1. See where main stands

```bash
.venv/bin/python .claude/skills/release/release.py status
```

It fetches, then prints `__version__`, the last `v*` tag, what PyPI shows, CI on `main`'s newest commit, the pull
requests merged since the last release, what kind of files they changed, and the `## [Unreleased]` entries in
`CHANGELOG.md`. It ends with notes and either `ready to release` or the reasons it isn't.

Stop and tell the user, without changing anything, when:

- **Nothing reaches pip users.** Only docs or development files changed: the guide site already publishes from
  `main` on its own, so there's nothing to release.
- **CI on main isn't green.** Releasing a red build ships the bug. Say which run failed and offer to look.
- **The work isn't on main yet.** Releases are cut from `origin/main`. If the user means changes still on a branch,
  they go through their own pull request first; ask whether to do that or release what `main` has.
- **The working tree is dirty.** Ask before stashing or committing anything.

## 2. Make the release branch

```bash
git switch -c release/v<version> origin/main
```

Use the version you expect from step 3's rules; rename the branch (`git branch -m`) if it changes.

## 3. Write the CHANGELOG entry

Pull requests should already have added their lines under `## [Unreleased]`, but check each pull request from
`status` against it, and fill in what's missing. To see what one changed: `gh pr view <n> --json title,body`,
`git diff v<last>..origin/main --stat`, and the README and `docs/` diffs, which already describe the change in
the user's words.

Write for a data scientist upgrading with `pip install -U aws-analyzer`, in README's voice:

- One bullet per change a user would notice, starting with the command or class (`S3Explorer`:,
  `DynamoDBView.scan()`), saying what they can do now or what looks different. End it with the pull request:
  `([#18](https://github.com/utkarsh5026/aws-analyzer/pull/18))`.
- Group the bullets under `### Added` (new commands, arguments, file types, services), `### Changed` (output,
  defaults or behaviour that's different), `### Fixed`, `### Removed`, in that order, and leave out empty groups.
- A change that can break a notebook goes first under Changed, starts with `**Breaking**:` and says what to change:
  a renamed or removed command or argument, a data method that returns something else, a raised `boto3>=` floor
  or Python floor.
- Leave out what users never see: tests, CI, Dependabot updates to the dev pins, screenshots, refactors, internal
  names (`_capture`, `_later`), and docs edits other than a new guide.

## 4. Pick the version and bump it

`$ARGUMENTS` may name one (`patch`, `minor`, `major` or `0.2.0`). Before 1.0, the rules are:

| Bump | When | Example |
|---|---|---|
| `minor` | anything under Added or Removed, or anything **Breaking** | 0.1.0 → 0.2.0 |
| `patch` | only Fixed, and Changed that's a fix or a wording change (prices, messages) | 0.1.0 → 0.1.1 |
| `major` | only when the user says the API is stable | 0.x → 1.0.0 |

`status` prints the bump its rules suggest. If the user's choice doesn't fit the entries (a `patch` with
something **Breaking**), say so and ask. Then:

```bash
.venv/bin/python .claude/skills/release/release.py bump <minor|patch|major|0.2.0>
```

It moves the Unreleased entries under `## [<version>] - <today>`, leaves an empty Unreleased above them, updates
the compare links at the bottom and sets `__version__`. It refuses a version that isn't newer than the last tag,
one the changelog already has, or an empty Unreleased.

## 5. Check and open the release pull request

1. Run `/check`. It has to pass, `package` included: that builds the wheel with the new version and imports it
   with only boto3. `tests/test_package.py` checks the changelog has an entry for `__version__`.
2. `release.py notes` prints the entry the GitHub release will show (hard-wrapped lines joined, the full-diff
   link added). Read it once more as the user.
3. Commit only `CHANGELOG.md` and `src/aws_analyzer/__init__.py`, as `Release <version>`, push the branch and open
   the pull request with the notes as its body:

   ```bash
   git commit -m "Release <version>" -- CHANGELOG.md src/aws_analyzer/__init__.py
   git push -u origin release/v<version>
   gh pr create --title "Release <version>" --body-file <notes file in the scratchpad>
   gh pr checks <n> --watch
   ```

## 6. Confirm, merge and publish

Show the user the version (and why that bump), the release notes, the pull request link and its checks. Then ask
with AskUserQuestion: **Merge and publish <version> to PyPI** / **Change the notes first** / **Not now**. Go on only
on an explicit yes. On "not now", leave the pull request open and say how to finish later (`/release` again).

```bash
gh pr merge <n> --merge --delete-branch
sha=$(gh pr view <n> --json mergeCommit --jq .mergeCommit.oid)
.venv/bin/python .claude/skills/release/release.py notes <version> > <scratchpad>/notes.md
gh release create v<version> --target "$sha" --title "v<version>" --notes-file <scratchpad>/notes.md
```

Tag the merge commit (`--target "$sha"`), not `main`, so a pull request merged in between can't slip into the
release.

## 7. Watch it reach PyPI

```bash
gh run watch "$(gh run list --workflow release.yml --limit 1 --json databaseId --jq '.[0].databaseId')" --exit-status
```

Then install it in a fresh virtual environment in the scratchpad (`pip install --no-cache-dir
aws-analyzer==<version>`), import `aws_analyzer` from outside the repo and print `__version__`. PyPI's JSON API can
lag a few minutes behind pip.

If the workflow fails:

- **Build and check**: the tag doesn't match `__version__`, or the wheel doesn't build or import. Nothing was
  uploaded. Ask before deleting the release and tag (`gh release delete v<version> --cleanup-tag --yes`), fix it
  in a new pull request, and publish again.
- **Publish to PyPI**, "invalid-publisher": PyPI's trusted publisher must name owner `utkarsh5026`, repository
  `aws-analyzer`, workflow `release.yml` and environment `pypi`. The user fixes that on pypi.org; then re-run the
  failed job (`gh run rerun <id> --failed`).
- **Publish to PyPI**, "file already exists": that version is on PyPI for good. Release the next patch version
  instead.

Finally `git switch main && git pull --ff-only`.

## Report

The version and why, the release and PyPI links, the result of the clean install, and the notes as published.
