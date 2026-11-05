---
name: specwright-release
description: "Opt-in release tagging for Specwright projects (release.enabled): bumps the version files as a tracked task in a change, and after the change is on main publishes the annotated tag and the GitHub release through scripts/release.sh. Backfills an older untagged version on request. Triggers: 'release', 'tag', 'publish v0.5.0', 'backfill a tag', or specwright-finish, specwright-pr watch and specwright-roadmap close offering a release."
metadata:
  version: 0.11.0
---

# Specwright Release

The script lives in `${CLAUDE_SKILL_DIR}/scripts/` (in other harnesses: the `scripts/` folder next to this SKILL.md); below, `scripts/release.sh` means that path. Run it with `bash` (Git Bash on Windows) from the code checkout, as `bash scripts/release.sh [--dir <repo>] <sub>`. It prints one JSON document. Exit 0 = done, 1 = stop (show its `message`), 2 = usage error, 3 = a git or `gh` network call failed or was refused.

Acts only with `release.enabled: true` in `openspec/specwright.yaml`; otherwise do nothing and mention no release.

```yaml
release:
  enabled: false                      # opt in
  version_files:                      # path or glob -> regex; the first is the primary
    VERSION: '^(\d+\.\d+\.\d+)$'
  tag: "v{version}"
  github_release: true                # also create the GitHub release from the tag's message
  auto: false                         # true = callers publish without asking
```

`release.enabled` with `pr.merge_method: rebase` is refused: a rebase rewrites the release commit.

## bump

A tracked task in the change's last task group, committed by the orchestrator through `specwright-commit`: `bash scripts/release.sh bump --to <version>` rewrites every version file and commits nothing. Verify with `bash scripts/release.sh check`, which reports the target version when all files agree.

Two changes can bump to the same version, and main's history then shows it once. `bash scripts/release.sh check --main <ref>` also compares a bumped branch with `<ref>`'s version and refuses (`version_not_ahead_of_main`) one that is not greater: bump again with a greater target. A branch that did not bump, or a `<ref>` with no readable version, passes. With `release.enabled` true, `specwright-pr` **ship** (`--main origin/<main>`, after a fenced fetch of main, before any push) and **watch** (before it reports ready and before the merge), and `specwright-finish` before a local merge (`--main <main>`), run it.

## Release notes

The notes of a release (the annotated tag's message, then the GitHub release body) come from the `## Release Notes` section of each change's archived `proposal.md`, read at the release commit. The section runs to the next `##` heading or the end of the file and holds a summary of at most 600 characters, then one or more of `### Added`, `### Changed`, `### Fixed` and `### Removed` (each at most once), each followed only by list items (`-`, `*` or `+` and a space; an indented line continues the item) of at most 500 characters. HTML comments and blank lines are ignored. Anything else (another heading, prose under a heading, no summary, no item) makes the section invalid.

```markdown
## Release Notes

One or two sentences saying what this release brings.

### Added

- New `--dry-run` flag on publish
```

An item that names no issue or PR (`#<n>` or `<owner>/<repo>#<n>` outside a code span) is listed with the change's PR appended, ` (#<pr>)`; with no PR known it is listed as written. The notes open with the release summary, then list `Added:`, `Changed:`, `Fixed:` and `Removed:` with every change's items in the changes' order (150 items at most, then `…and <n> more items`), and `Changes:` with one line per change that has no valid section.

The summary comes from the bumping change: the change in the release's range whose archived `tasks.md` has a ticked `release.sh bump --to <version>` task and a valid section; with none or several, the last change with a valid section. The bump task rewrites that summary to describe the whole release, not only its own change, and checks the section with `bash scripts/release.sh notes --proposal openspec/changes/<change>/proposal.md`. That subcommand reads one file, needs no repo, git or network and no `release.enabled`; it exits 0 with the summary and each item's line (an unreferenced item ends in the literal ` (#<pr>)`), 1 with `release_notes_invalid` and every error with its line (or `no_release_notes`), 2 when the file is missing. Run it again after every edit of the section.

A change whose section is invalid, or whose proposal is over 64 KB, falls back to its Why line under `Changes:`, and `status` and `publish` list it in `warnings` (the change and the first error) without stopping. A change with no section is listed as before.

## publish

Once the change is on main (callers: `specwright-finish`, `specwright-pr` **watch**, `specwright-roadmap` **close**):

**Run login.** Use the run login the caller handed over (`run login: <login>`). A publish the user started directly has none: take `github.login` from `openspec/specwright.yaml`, else run `bash <specwright-pr>/scripts/as.sh --resolve` once (it prints the active github.com account; exit 3 → stop and tell the user). Keep it for the whole run. "Origin on github.com" means its fetch URL, `git remote get-url origin` (after `insteadOf`; `github.com.` included), never the raw `remote.origin.url`: a shorthand such as `corp:acme/app` that expands to github.com is on github.com. With origin on github.com, every step below runs through `as.sh <run login>`, never unfenced; plain calls are only for an origin elsewhere.

1. Fetch main only, without tags: `bash <specwright-pr>/scripts/vcs.sh fetch-main --repo <code toplevel> --role code --no-tags --login <run login>` (it fences the fetch when origin is on github.com, else runs plain, and works on Git and on a colocated jj repo alike). Never `--tags`, and keep `--no-tags` (a clone with `remote.origin.tagOpt=--tags` fetches every tag otherwise): a local tag that differs from origin's (a lost push race) would fail the fetch before publish can report it. `release.sh` reads origin's tags itself (`ls-remote`) and fetches only the tag it publishes. Pass `--main <ref>` after a fetch, `<ref>` being the `ref` it printed (`origin/<main>` on Git, a commit id on jj), `--main <main>` otherwise. On jj a commit id names no branch, so also pass `--base <main>`, the GitHub base branch, to `status` and `publish` (`untagged` lists no PRs and takes no `--base`).
2. `bash <specwright-pr>/scripts/as.sh <run login> bash scripts/release.sh untagged --main <ref>` (it reads origin's tags; plain `bash scripts/release.sh untagged ...` only when origin is not on github.com) lists the versions after the latest published one that are not published, oldest first (none published: only the current version). Published means the tag is on origin (with no origin remote: a local tag); a version whose tag is local but not on origin (a failed push) is always listed, and a re-run pushes it. Publish each oldest first and stop at the first failure. `untagged --local` reads local tags only, with no network call and no login (`specwright-finish` in `finish: local`); its output says `"tags": "local"`, since a local tag may be missing on origin. Publish still reads origin.
3. `bash <specwright-pr>/scripts/as.sh <run login> bash scripts/release.sh publish --version <version> --main <ref>` (`--base <main>` too on jj) from the code repo, so every git and `gh` call inherits the fence; plain `bash scripts/release.sh publish ...` only when origin is not on github.com. It checks the remote, stops on a conflicting tag, creates the annotated tag, pushes only `refs/tags/<tag>` and creates the GitHub release. It is idempotent: a re-run resumes.
4. Store-backed: add `--store <store toplevel>` (and `--store-main <ref>`, `--store-prefix <P>`) to `status` and `publish`, so the notes come from the store's archive. Only the code repo is tagged.

The tagger is git's committer identity: the commit-identity rules of the project (CLAUDE.md/AGENTS.md) apply. The annotated release tag is the one Git write Specwright makes on a jj repo: `release.sh publish` creates it with Git and pushes only `refs/tags/<tag>`. Every other branch read and write goes through `vcs.sh`.

Report per version: `release v0.5.0: tag pushed at <sha>, GitHub release created`, or `release v0.5.0: already published`.

When `publish` creates the tag, its JSON has `warnings` (`[{"change", "error"}]`): report each change and its error next to the release line, for example `release v0.5.0: tag pushed at <sha>, GitHub release created; warning: add-x: line 12: unknown heading 'Security'`. The notes were derived from the archive, so the tag keeps the Why-line fallback for that change; nothing is rewritten. A re-run that finds the tag reports `warnings: []`.

## Stops

Show the error and tag nothing more. None is fixed by moving, deleting or forcing a tag.

| Exit | Error | Do |
|---|---|---|
| 1 | releases disabled | do nothing |
| 1 | `pr.merge_method` rebase, or a rebase-merged release commit | report the commit or settings; the user tags by hand or changes the merge method |
| 1 | version files disagree | the user fixes them by hand; run `check` |
| 1 | version not on main | publish after the release commit reaches main |
| 1 | tag exists at another commit | the user fixes it by hand |
| 1 | a lightweight tag at the release commit | the user replaces it by hand with an annotated tag, or deletes it |
| 1 | `push_url_mismatch`: origin pushes to another repository than it fetches from | the user fixes `remote.origin.pushurl`, or publishes from a remote whose URLs agree |
| 1 | `tag_mismatch`: the local tag and origin's are different tag objects (a lost push race) | the user deletes the local tag (`git tag -d <tag>`); a re-run fetches origin's |
| 1 | a `version_files` entry outside the repository, or a symlink | the user fixes `release.version_files` (list the file a link points to) |
| 1 | an older version is untagged | publish it first (`untagged` lists it) |
| 1 | `version_not_ahead_of_main`: the branch bumped to a version not greater than main's | rerun `bump --to` with a greater version, commit it, and ship or merge again |
| 3 | network or fence failure | report it; a re-run of publish resumes |
| 3 | `deadline_exceeded` or `response_too_large`: a `git` or `gh` network command ran past 120 s (300 s for the closed-PR read) or printed more than 32 MiB, and was stopped with everything it started | report the command the message names; nothing was retried, and a re-run of publish resumes. After a cut-off tag push or `gh release create` publish reads the result back: a tag on origin that is the local tag object at the release commit, or a release found, counts as done; otherwise the message says what is not done and that a re-run does it |
| 3 | `state: unknown` with `deadline_exceeded` or `response_too_large`: a tag push or `gh release create` was cut off and reading it back failed too | report that the tag's (or release's) state on origin is unknown; check it by hand (`git ls-remote --tags origin`, `gh release view`) before a re-run |

## Backfill

`publish --version <old>` for an older untagged version, only when the user asks.

## Never

Never delete or move a tag, use `--force` or `--tags`, push a branch, tag the store, or publish without `release.enabled`.
