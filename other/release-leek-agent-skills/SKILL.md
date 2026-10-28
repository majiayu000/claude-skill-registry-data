---
name: release
description: "Commit this session's work, bump the version, tag, push, and publish a GitHub release with grouped notes. Use when the user asks to release, cut, tag, or publish a version."
argument-hint: "[major|minor|patch] [summary] (both inferred from the commits when omitted)"
allowed-tools: "Bash(git status *) Bash(git diff *) Bash(git log *) Bash(git describe *) Bash(git tag *) Bash(git show *) Bash(git fetch *) Bash(git rev-list *) Bash(git add *) Bash(git commit *) Bash(git push *) Bash(gh auth status) Bash(gh release *)"
---

# Release

Cut one release from the current branch: every commit since the last tag, plus this
session's uncommitted work. One release, one version, one tag, one GitHub release page.

## Process

1. **Preflight.** Run `gh auth status`, `git fetch`, and `git describe --tags --abbrev=0`.
   Note the tag style (`v1.2.3` or `1.2.3`) from `git tag --sort=-v:refname | head -1` and
   keep it. If the branch is behind its remote (`git rev-list --count HEAD..@{u}` is not 0),
   stop: a release must not race someone else's push. No tag at all means a first release;
   read the version from the version file in step 4, or use `v0.1.0`. Done when you are
   authenticated, hold the last tag, and the branch is not behind.
2. **Commit this session's work.** Only files *you* created, edited, or deleted in this
   conversation; `git status --porcelain` lines you did not touch belong to a parallel
   session and stay out. Changes under `.claude/agent-memory/` are always yours too, whoever wrote them: they are the notes of agents with `memory: project`, not a parallel session's work in progress, so they ride along in your commit (`git add -- .claude/agent-memory`). `git add -- <new-path>` each new file, then
   `git commit --only -m "<type(scope): subject>" -- <path> …` (options before the `--`).
   Never `git add -A`, `git add .`, or `commit -a`. A file that mixes your hunks with
   foreign ones is left out and named in the report. Skip this step when there is nothing
   of yours to commit. Done when `git status --porcelain` shows none of your files.
3. **Choose the version.** `git log <last-tag>..HEAD --format='%h %s'`. No commits means
   nothing to release. When step 2 left changes out as not this session's, ask once which
   to commit (they are often the user's own earlier work): `AskUserQuestion` where
   available, `multiSelect: true` with one option per file (at most 4 per question, further
   questions for the rest); otherwise list them in chat and wait. Commit the picked ones as
   step 2 does and continue. Otherwise say so and stop. Bump from `$0` when given; otherwise from the
   subjects: `!` or `BREAKING CHANGE` → major (minor while still `0.x`), any `feat` → minor,
   anything else → patch. Done when the new version is stated with the rule that chose it.
4. **Bump the version file.** Find the one file whose version string equals the last tag:
   `.claude-plugin/marketplace.json`, `package.json`, `pyproject.toml`, `Cargo.toml`,
   `VERSION`, or whatever the repo uses. Replace exactly that string; assert it matched once.
   Commit it alone: `git commit --only -m "chore(release): <version>: <summary>" -- <file>`.
   The summary is `$1` when given, otherwise the headline change in six words or fewer,
   matching the style of earlier release commits. A repo with no version file is
   versioned by its tags alone; skip the commit. Done when `HEAD` is the release commit or
   there was nothing to bump.
5. **Tag and push.** A pushed tag cannot be taken back, so first draft the step 6 notes and
   ask the user to confirm (`AskUserQuestion` where available: one single-select question,
   **Tag and publish** first, its `preview` showing the version, the rule that chose the
   bump, and the drafted notes; otherwise show the same in chat and wait). Act only on a
   yes. Then `git tag -a <version> -m "<version>: <summary>"`, then
   `git push origin <branch> <version>` in one command. First check that the tag is free
   with `git tag -l <version>` (empty output means free); stop if it already exists. Never
   probe with a bare `git tag <version>`: that creates a lightweight tag instead of
   checking. Done when the push reports both refs.
6. **Publish** the confirmed notes. Write the notes from the diff, not from the subjects: one bullet per
   user-visible change, grouped under `##` headings by area (the scopes in the subjects
   are a good start), the release commit itself omitted, no attribution trailers.
   `--generate-notes` alone is too thin; use it only to append the compare link.
   `gh release create <version> --title "<version>: <summary>" --notes "$(cat <<'EOF' … EOF)"`.
   Done when `gh release view <version>` returns a URL.
7. **Report.** The release URL, the two commit subjects with short SHAs, and any files
   deliberately left out of step 2 and why. When step 4 bumped `.claude-plugin/marketplace.json`,
   also print the command that refreshes the installed Claude Code plugin, using that file's
   `name` and the plugin `name`: `claude plugin marketplace update <marketplace>` then
   `claude plugin update <plugin>@<marketplace>`. For this repo that is
   `claude plugin marketplace update leek-agent-skills && claude plugin update leek-skills@leek-agent-skills`.
   The running session keeps the previous plugin until it restarts.

## Guardrails

- Release the current branch as it stands. No branch switching, no amend, no rebase, no
  stash, no reset: a parallel session's uncommitted work is unrecoverable if discarded.
- Never force-push, and never move or delete a tag. A wrong version gets the next version.
- If the push in step 5 fails, leave the local tag in place and report the error; do not
  retry with different flags.
