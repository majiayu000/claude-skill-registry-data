---
name: release
description: Cut a release of the current repository, with a code review and a security review of everything since the last release, and the docs checked against the code, before anything ships. Use whenever cutting, shipping or publishing a release, bumping VERSION, tagging vX.Y.Z, or when Jason runs /bud:release. Claude Code only, since it runs Claude Code's code-review and security-review skills.
argument-hint: "[X.Y.Z]"
---

# Cut a release

Every release gets a code review and a security review of everything it ships,
and docs that say what the code does, before it ships. Jason picks the version and decides what a finding means; you
do the legwork and never cut the release past a finding he hasn't seen.

## 1. Find out how this repo releases

- Read the release section of `CLAUDE.md` (or `README.md`, `RELEASING.md`)
  and the release workflow in `.github/workflows/`. bud, for example, releases
  when a push to `main` changes `VERSION` (D80): the workflow checks it, runs
  the tests, pushes the `vX.Y.Z` tag and builds the release. Cloud sessions
  can't push tags, so a repo that needs a hand-pushed tag has to be released
  from Jason's machine: say so and stop.
- `git fetch origin main --tags`, then work from an up-to-date `main` with a
  clean tree. Uncommitted or unpushed work: stop and ask what goes in.
- The last release is the newest stable tag:
  `git tag --list 'v[0-9]*' --sort=-v:refname | grep -v -- - | head -1`
  (the `grep` drops prereleases like `nightly` or `-rc1`). No tag means the
  first release: everything is in it.

## 2. Say what's in it

List the commits in `<last tag>..origin/main` (`git log --oneline`) and
summarize them in a few lines, grouped by `feat`, `fix` and the rest. Nothing
since the last tag: there's nothing to release, so say so and stop.

## 3. Review it

Run both, on the whole range, not just the last commit:

1. The `code-review` skill (`/code-review`) at `high`, with the range as its
   target: `high <last tag>..origin/main`.
2. The `security-review` skill (`/security-review`) on the same range.

`code-review` takes the range as its target. `security-review` takes no
target: it reviews `origin/HEAD...HEAD`, which on `main` is empty, and a
cloud clone may have no `origin/HEAD` at all. Point it at the release, run it,
then put it back:

```sh
git update-ref refs/remotes/origin/release-base '<last tag>^{commit}'
git symbolic-ref refs/remotes/origin/HEAD refs/remotes/origin/release-base
# run security-review
git remote set-head origin main
git update-ref -d refs/remotes/origin/release-base
```

Fixes made in step 4 get their own `code-review` (their commits as the
range); a review of a fix's fix can stop at `low` once its findings are small.

If either skill isn't available (a surface other than Claude Code), say so
and stop: a release without both reviews isn't one this skill cuts.

## 4. Settle the findings with Jason

Show the findings from both reviews in one list, worst first, each with file,
line, what breaks and the fix. Then let him choose, per finding: fix it now,
ship with it (he says why), or stop the release.

- A fix is an ordinary change: follow `bud:code-style`, run the repo's checks
  (`just check` or what CI runs), commit, push to `main`, and review the
  fix's own diff with `code-review` before going on.
- A critical or high-severity security finding blocks the release until it's
  fixed or Jason explicitly ships with it.
- No findings: say so in one line and go on.

## 5. Check the docs against the code

Docs drift when code moves under them, so check every page, not only the ones
the release touched:

- **What to read:** the README, `docs/`, plan or design docs that describe the
  current state (bud's `BASE.md`, sections 0 to 7), and `CLAUDE.md` or
  `AGENTS.md`. Leave dated records alone: a decision log entry, a dated spec or
  plan, a changelog entry for an old release. They say what was true then.
- **How to check:** against the code and the built binary, never from memory.
  Commands and flags against each command's `-h` output, keys against the
  keymap code, config keys and defaults against the defaults in code, file
  trees against `ls`, counts ("seven languages", "three layouts") against what
  ships, and statuses or event names against the code that emits them. A doc
  that names a file, function or skill that no longer exists is wrong too.
- **What to fix:** anything that's wrong, missing for what this release adds,
  or describes something removed. Keep each page's voice and level of detail;
  don't rewrite what's accurate. Changes in behaviour the docs need but the
  code doesn't have are findings for Jason, not doc edits.
- **Then:** show Jason a short list of what was wrong, page by page, make the
  fixes as one `docs:` commit, run the repo's checks (some test the docs, like
  bud's `TestDocsCoverEveryKey`) and push to `main`. Nothing wrong: say so in
  one line and go on.

## 6. Pick the version

Propose the next version from the commits (semver: a breaking change bumps
major, a `feat` minor, only fixes patch), or take the one Jason passed, and
let him confirm it. It must be newer than the last tag.

## 7. Cut it

Do it the repo's way. For a `VERSION` file (bud): write the version, commit
`chore: release vX.Y.Z` with a body that records the reviews, and push `main`:

```text
chore: release v0.20.0

Reviewed v0.19.0..<sha>: code-review (2 findings, both fixed in <sha>),
security-review (none), docs (3 pages fixed in <sha>).
```

A finding Jason chose to ship with goes in that body too, with his reason.

## 8. Watch it land

Follow the release workflow run (GitHub's Actions tools: list the runs for
the push, then get the run) until it's done. Green: give Jason the release
link. Red: show the failing step and its log, and fix it the same way as a
finding. Never delete or move a tag, or re-run with the checks skipped, to
get it green.
