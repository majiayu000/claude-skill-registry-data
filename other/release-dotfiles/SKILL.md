---
name: release-dotfiles
description: Deploy and release a new version of the dotfiles Emacs profile. Use when the user says `/release-dotfiles X.Y.Z`, asks to deploy profile X.Y.Z, cut/publish/prepare a dotfiles release, or bump the dotfiles version. The agent builds and tests the development profile first, hands it to the user, and releases the pinned version only after the user confirms. Do not use for standalone Emacs package releases; use release-package instead.
---

# Dotfiles profile deployment and release

Prepare, test and release `benthamite/dotfiles` version `NEW_VERSION`. Use
`dotfiles-context` for canonical source routing and paired configuration checks,
and `publish-dotfiles` for every dotfiles push. Reading this procedure does not
authorize its side effects.

## How the mechanism fits together

The user gives a version number, for example `/release-dotfiles 9.0.2`. The
skill owns everything from there in two phases with one stop between them.

**Phase 1: deploy the development profile.** The agent creates
`NEW_VERSION-dev` from a cooldown lockfile: the user's own packages at their
remote tip, third-party packages at the newest commit first observed at least
seven days ago (`bin/elpaca-cooldown`; every package runs unsandboxed, so
upstream HEAD is never built directly). It launches a GUI Emacs on the profile
with the reporter in `scripts/smoke-report.el`,
reads the plain-text report, fixes the root cause of every failure, and repeats
until the report is clean. When it is clean the reporter instance writes the
lockfile from its own Elpaca queue, so the pinned refs are exactly the checkouts
that passed. The agent then launches the dev profile for the user and stops.

**The stop.** The user works in the dev profile and comes back to the same
session. "Proceed" means release. A reported problem sends the skill back to
Phase 1.

**Phase 2: release the versioned profile.** The agent commits the frozen
lockfile as the release commit, reviews public text, tags, pushes and creates
the GitHub release. Nothing is tested again: the versioned profile pins what was
tested. No other layer tests profiles. `init-deploy-profile` in the `init`
package is a plain build command and must not be used for this flow.

## Modes and resumption

- A preparation request stays local: Phase 1 may run in full, but no package
  repo push beyond Step 1's scope, no tag, no branch push and no GitHub release
  without explicit publication authority.
- A release request may proceed only through the gates below.
- `--accept` skips the notes confirmation in Step 8. For a publication request it
  also approves pushing the reported clean, unpushed package repos in Step 1
  after their ownership and push destinations are verified. It does not expand a
  preparation request into publication, authorize unrelated repositories, or
  supply the user's dev-profile confirmation in Step 6.
- `--accept` never skips the user's test in Step 6 or either security-review
  layer in Step 10.

When resuming, identify the exact version, the dev profile directory, whether
the report is clean, the lockfile candidate and its digest, the approved notes,
and the completed gates. Do not repeat a lockfile commit, tag, push or release
creation merely because the session restarted. Reconcile any existing artifact
with the exact candidate before reusing it. A prior clean report applies only to
a dev profile whose recipes, checkouts and extras have not changed since.

# Phase 1: deploy and test `NEW_VERSION-dev`

## Step 0: resolve the repository, version and live Emacs

Confirm the canonical dotfiles checkout and its exact `origin` identity:

```bash
git remote get-url origin
git status --porcelain
```

Require the GitHub owner/repository to be exactly `benthamite/dotfiles`, not a
substring match. Use the existing canonical checkout if the current directory is
wrong; do not clone or modify the Elpaca dotfiles mirror.

Take `NEW_VERSION` from the user's argument. Require canonical
`MAJOR.MINOR.PATCH` (`^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$`), no
`v` prefix. If no version was given, ask for one; do not invent it. The dev
profile is `NEW_VERSION-dev` under `~/.config/emacs-profiles/`.

Resolve the live Emacs values of `init-current-profile`, `user-init-file`,
`paths-file-config`, `elpaca-sources-directory` and `init-master-lockfile-path`.
Require successful queries, valid strings and existing paths. The lockfile
destination must resolve to the canonical repo's `emacs/lockfile.el`. Do not
reconstruct paths from a profile label.

Inspect the dotfiles worktree and index before any release edit. Preserve
unrelated or concurrent changes, including files another session has staged.
Do not stash or commit them implicitly; commit your own changes by path.

## Step 1: check Elpaca source reproducibility

Start with one call that does the inventory below and reports only what needs
attention, including the CI state of own repositories:

```bash
bin/release-preflight --convert
```

`--convert` makes own treeless clones blobless first, so the pushes this step
may need finish in seconds. Act on each flagged checkout as described below;
the rest of this step explains what the flags mean.

The dev profile clones every package from its remote, so a commit that exists
only in a local checkout is invisible to it and to the lockfile. Inventory each
distinct Git checkout under the live Elpaca source directory, including Git
worktrees whose `.git` is a file. Resolve real paths and deduplicate shared
checkouts. Inspect working-tree and staged changes with:

```bash
git -C "$PACKAGE_REPO" status --porcelain
```

The `sources/dotfiles` checkout is a read-only runtime mirror that the commit
hooks synchronize from the canonical repository. Check that it matches the
canonical committed source; never commit or push that mirror as an ordinary
package repo.

For other packages, distinguish detached HEAD, missing upstream, Git command
failure, behind/diverged history and genuine unpushed commits. Check upstream
existence separately before querying its range:

```bash
git -C "$PACKAGE_REPO" rev-parse --verify '@{upstream}'
git -C "$PACKAGE_REPO" log --oneline '@{upstream}..HEAD'
```

An arbitrary nonzero exit is not proof of a missing upstream. Fetch the relevant
remote refs before judging visibility. For a detached or upstream-less package,
verify whether its exact HEAD is reachable from the intended remote's advertised
branch/tag history. No upstream is not automatically a blocker, but an
unpublished or unverifiable commit is. A lockfile hash cannot preserve changes
that exist only in a dirty worktree.

Run every `git push` and `gh` command as its own tool call with a literal
target; the GitHub write guard rejects compound commands, pipes and
redirections.

Report dirty repos and clean-but-unpublished repos separately, with the exact
target and proposed action. In publication mode, `--accept` permits pushing the
reported clean package repos within its scope; otherwise obtain scoped
confirmation. Never infer a writable fork destination from an upstream URL.
Inspect outgoing changes before pushing and use `post-push-ci` after each push.
A failed push does not stop the inventory, but unresolved reproducibility or CI
failures block the release.

Untracked byte-compiled artifacts may be cleaned with `trash` only after
inspecting the exact candidates and confirming they are disposable generated
files. Identify candidates with:

```bash
git -C "$PACKAGE_REPO" ls-files --others --exclude-standard -z -- '*.elc'
```

Preserve NUL-delimited paths. Recheck status after cleanup. If `trash` is
unavailable, leave the files and report the blocked cleanup; do not substitute
destructive deletion.

For remaining dirty repos, ask which exact changes may be committed and pushed;
make both effects explicit. After approval, inspect the diffs, split logical
changes and stage only the agreed paths. Do not use a blanket `git add -A`
across work owned by concurrent sessions.

## Step 2: reconcile temporary Elpaca PR pins

Scan `emacs/config.org` for `awaiting PR merge` markers and legacy GitHub PR
URLs. Inspect each enclosing `use-package :ensure` recipe or explicit `elpaca`
order. A bare PR URL is a candidate, not proof of an active pin. A deliberate
`:ref` pin with an explanatory paragraph, such as a package whose upstream
deleted the file, is not a PR pin; leave it.

For each actual pin, query supported CLI fields:

```bash
gh pr view "$PR_URL" \
  --json state,mergedAt,baseRefName,headRepository,headRepositoryOwner,headRefName,url
```

Use `state == MERGED` / non-null `mergedAt`; `merged` and `baseRepository` are
not supported `gh pr view --json` fields. Derive the base owner/repo from the
returned PR URL and query its default branch:

```bash
gh repo view "$BASE_REPO" --json nameWithOwner,defaultBranchRef
```

- If the recipe no longer points to that PR head, report "comment only /
  already restored" and leave it unchanged.
- If the PR is open, retain and report the intentional pin.
- If it is closed without merge, obtain a decision before retaining or replacing
  abandoned code in a release.
- If merged, restore the base repo. Remove the branch only when the PR base is
  the repo's default branch; otherwise retain the base branch explicitly.

Preserve unrelated recipe options and comments. Remove the PR marker only where
it no longer describes a temporary pin. Keep one install recipe per package.
Commit only the recipe changes, as a separate logical change, with the tracked
`bin/check-config-org` evidence. The dev profile built in Step 4 is tangled from
the canonical `config.org`, so it picks these recipes up; the live session does
not need a reload for that.

## Step 3: recheck the dotfiles baseline

Require that `emacs/config.org`, `emacs/extras/` and `emacs/lockfile.el` have no
uncommitted changes of yours. Other files may carry another session's work;
leave them alone. Fetch `origin`, and inspect the configured upstream and
ahead/behind counts. Treat fetch/query failures as failures, not "already
synchronized". Resolve a behind, diverged, detached or incorrectly targeted
branch before continuing. Being ahead is normal: the release publishes the
branch in Phase 2. Recheck the Elpaca dotfiles mirror against the committed
source.

## Step 4: create the dev profile

1. Confirm no Emacs runs with `--init-directory` pointing at the dev profile
   directory (`ps -axo pid,command`; `pgrep -f` can miss it). Ask the user to
   quit one that does. Trash any existing directory of that name after
   inspecting it: Elpaca skips cloning when a source directory exists, so a
   stale profile tests old checkouts.
2. Write the cooldown lockfile to the temporary workspace outside Drive:

   ```bash
   bin/elpaca-cooldown plan --out "$COOLDOWN_LOCKFILE" --report "$COOLDOWN_REPORT"
   ```

   Add `--drop PACKAGE` for every package whose recipe changed in Step 2 (a new
   repository, branch or pin): its old ref may not exist in the new remote, so
   it is left out and builds from the recipe in `config.org`. Add
   `--take-now PACKAGE` only when the user asked for a specific upstream commit
   before its cooldown ends, for example an urgent upstream fix; never add it
   to make a build pass. Read the report. `held` packages keep the previous
   release's ref and the report says why: "no observation is old enough yet" is
   normal while the observation log is young, while a rewritten or diverged
   history needs the user's decision. A remote that cannot be read fails the
   plan; do not fall back to an unpinned build. Packages whose `config.org`
   recipe carries a `:ref` or `:tag` are listed as "pinned in config.org" at
   that pin, because Elpaca honours it over the lockfile; an abbreviated
   commit the previous lockfile does not record fails the plan until the pin
   is written in full.
3. Create and tangle the profile from the live session without prompts, then
   install the cooldown lockfile as the profile's `lockfile.el` before anything
   launches it:

   ```bash
   emacsclient -e '(let ((dir (init-create-profile "'"$NEW_VERSION"'-dev" t))) (with-current-buffer (find-file-noselect paths-file-config) (init-build-profile dir)) dir)'
   cp -- "$COOLDOWN_LOCKFILE" "$HOME/.config/emacs-profiles/$NEW_VERSION-dev/lockfile.el"
   ```

   Do not call `init-deploy-profile`: it pulls, prompts and is meant for
   interactive use. Check that the profile's `lockfile.el` is byte-identical to
   `$COOLDOWN_LOCKFILE`, that its `init.el` carries every recipe changed in
   Step 2, and that `.current-profile` still names the live profile (creation
   alone does not launch).

## Step 5: build it until it builds

1. Launch a separate GUI Emacs on the profile, the way the user does, with the
   reporter loaded after init. Give it a report path and a lockfile path in a
   uniquely named temporary workspace outside Drive:

   ```bash
   INIT_TEST_INSTANCE=1 \
   SMOKE_REPORT_FILE="$REPORT" SMOKE_LOCKFILE_FILE="$LOCKFILE_CANDIDATE" \
     /Applications/Emacs.app/Contents/MacOS/Emacs \
     --init-directory="$HOME/.config/emacs-profiles/$NEW_VERSION-dev" \
     -l "$SKILL_DIR/scripts/smoke-report.el"
   ```

   Run it in the background and wait until the process exits: the reporter
   quits the instance itself right after writing the final report, so never
   signal it. It also finishes on a profile whose packages were already built,
   where Elpaca completes before `-l` loads the reporter. The report then reads
   `state: final`; an exit without that line is a crash to diagnose.
   A fresh profile clones and compiles several hundred packages; allow well
   over ten minutes before treating silence as a hang, and read the
   in-progress counts in the report rather than guessing. Do not use `--batch`:
   a batch Emacs exits at the first process-sentinel error and hides every other
   failure.
2. If the report lists a failed package, read its Elpaca log there. A dependent
   of a failed package fails with "Failed dependencies"; find the first failure.
   An unknown ref means an unpushed commit; "exists. Skipping clone" followed by
   a checkout error means a stale or shared checkout; "Unable to find main elisp
   file" after a successful clone means the recipe's `:files` no longer match
   upstream, so check whether upstream moved or deleted the file and pin,
   re-point or drop the package. Fix the root cause in the canonical source
   (`config.org`, an extra, or the package repo), commit it with the applicable
   evidence, and push package repos within Step 1's authority.
3. The report also lists every line of the `*Warnings*` buffer and every error
   line of `*Messages*`. A package can build under Elpaca and still break at
   load time, for example an upstream autoload cookie on a top-level form that
   reads an unbound variable ("Error loading ... autoloads: (void-variable
   ...)"). Treat each warning as a failure: read it, find the commit that
   introduced it, and fix the root cause or pin the package to the last good
   commit with the reason recorded in `config.org`. Do not reach for a newer
   upstream commit with `--take-now` to get a build through. Only a warning that was
   investigated and cannot be fixed or pinned away may be allowed, by
   relaunching with `SMOKE_ALLOW_WARNINGS=1` and naming it in the handover.
4. After a fix, rebuild what the fix affects. A recipe, ref or checkout change
   needs a trashed and recreated profile (repeat from Step 4). A change only to
   `config.org` code or to an extra needs a re-tangle of the dev profile and a
   fresh reporter run on the same directory. Repeat until the report shows zero
   failed packages, zero warnings and zero error messages. Do not hand a
   failing or warning profile to the user.
5. When the report is clean, the reporter writes `$LOCKFILE_CANDIDATE` from the
   tested instance's Elpaca queue and records `lockfile: PATH` in the report.
   Require that line; a `lockfile: not written` line names what is still wrong. Validate the candidate with the logic of
   `bin/check-lockfile` (one Lisp form, every entry with a `:source` string and
   a `:recipe` carrying a `:ref` string), compare its entry count with the
   previous lockfile, and check that every recipe changed in this release
   records the intended repository, branch and ref. Then confirm the build
   honoured the cooldown:

   ```bash
   bin/elpaca-cooldown verify-build --candidate "$COOLDOWN_LOCKFILE" --built "$LOCKFILE_CANDIDATE"
   ```

   A drifted ref is a failure: find why Elpaca checked out something else
   before continuing. The packages it lists as new were built at upstream HEAD
   without a cooldown; name them, and any `--take-now` package, in the Step 6
   handover so the user knows which code is fresh. Record the candidate's
   SHA-256 digest as `LOCKFILE_DIGEST`.
6. `INIT_TEST_INSTANCE=1` keeps the instance from claiming
   `~/.config/emacs-profiles/.current-profile` and the `active` link, which
   the commit hooks and `~/.emacs.d` rely on. Launch every test instance
   with it, and check afterwards that both still name the live profile.

## Step 6: hand the dev profile to the user and stop

The reporter instance has already quit itself. Launch the dev profile again
the same way, with `INIT_TEST_INSTANCE=1` but without the reporter, and leave
it open; the user closes it. Do not hand the user a command to run. Report
what was fixed during Step 5 and ask whether to proceed to the release of
`NEW_VERSION`. Then stop. `--accept` cannot supply this answer.

Include the unused-package report in the handover. Run
`bin/elpaca-cooldown unused` and relay its list: the third-party packages that
the package usage log has not seen loaded in 60 days. Every package runs
unsandboxed, so each one removed is one fewer upstream to trust. Present the
list as candidates for the user to choose from, never as a recommendation to
remove them all, and remove nothing in this release: a removal the user asks for
is a `config.org` change for the next one. When the command says the log is too
young, say so in one line and move on.

- "Proceed" continues to Phase 2.
- A reported problem is a Step 5 failure: fix the root cause, rebuild as Step 5
  item 3 requires, obtain a new clean report and a new lockfile candidate, and
  return to this step. Any change to `config.org` recipes, extras or package
  checkouts after the clean report invalidates `LOCKFILE_CANDIDATE`.

# Phase 2: release `NEW_VERSION`

## Step 7: freeze the candidate

Recheck that `LOCKFILE_CANDIDATE` still has `LOCKFILE_DIGEST`, and that
`config.org`, `emacs/extras/` and every package checkout are unchanged since the
clean report (compare HEADs and status against what Step 5 recorded). If
anything moved, return to Phase 1. Recheck the source-reproducibility gate:
every ref in the candidate must be reachable from its remote.

After a successful tag fetch, enumerate reachable tags:

```bash
git fetch --tags origin
git tag --merged HEAD --list --sort=-version:refname
```

Filter to exact canonical `MAJOR.MINOR.PATCH` names and take the highest as
`LATEST_TAG`. Require `NEW_VERSION` to be strictly higher and to collide with no
local or remote tag or release. Read every commit in `"$LATEST_TAG"..HEAD`; if
the range is empty and the lockfile is unchanged, report that there is nothing
to release. If the bump the user chose does not match the range (a breaking
change under a patch bump, for example), say so and let the user decide; do not
silently change the version.

## Step 8: draft and freeze release notes

Apply the user's outgoing-prose conventions (`personalize` when publishing as
Pablo). Write user-facing descriptions rather than copying terse commit messages.
Group features, fixes and other changes; for a large range, summarize by theme
while accounting for the significant changes.

Keep notes in the same temporary workspace. Record the file as
`RELEASE_NOTES_FILE`. Present the previous/proposed versions, commit count,
package reproducibility/CI status, remaining PR pins, fixes made in Step 5 and
the notes; wait for explicit confirmation unless `--accept` applies. After
approval, freeze the content and record its SHA-256 digest. The exact same file
must be reviewed and passed to GitHub; do not retype a heredoc or publish
literal placeholders later.

## Step 9: write the lockfile and release commit

Copy `LOCKFILE_CANDIDATE` to the canonical `emacs/lockfile.el`, verify the copy
has `LOCKFILE_DIGEST`, and run the tracked check. Stage only that file and
commit by path so another session's staged files stay out of the release
commit:

```bash
cp -- "$LOCKFILE_CANDIDATE" emacs/lockfile.el
git add -- emacs/lockfile.el
claude/bin/elisp-check-evidence file:emacs/lockfile.el -- bin/check-lockfile
git commit --allow-empty -m "$NEW_VERSION" -- emacs/lockfile.el
```

Run the evidence wrapper as the only executable in its tool call, from the
repository root. Record the release candidate's exact commit ID as `CANDIDATE`.
Do not build or launch a `NEW_VERSION` profile locally: it would pin the same
refs the dev profile already exercised, and its only consumers are other
systems' deployments.

## Step 10: guarded publication review

Follow `publish-dotfiles`, including any due full-history audit, before creating
a new tag. A full-audit receipt requires successful status and
`full-audit-recorded:`, not merely a clean-looking review count.

```bash
bin/dotfiles-publish scan --mode release \
  --release-notes "$RELEASE_NOTES_FILE" \
  --tag "$NEW_VERSION"
```

Capture the printed run ID as `RUN_ID` and confirm the candidate equals
`CANDIDATE`. Continue review after exit 2; fail closed on scanner/setup failure.
Display and adjudicate every unit, including the release notes and exact tag
name. Do not record blanket clean verdicts. Check public text for private paths,
internal details and unapproved plans as well as credentials. Require a
successful, complete clean review.

If repair changes the candidate, return to Step 7 with the new state; a code fix
needs a new dev-profile report and lockfile candidate, not a reuse of the old
one. Never delete or move a preexisting/public tag. Clean up only this
workflow's own unpublished tag after verifying its exact identity and absence
from the remote.

## Step 11: tag, publish and create the release

Recheck `CANDIDATE`, `NEW_VERSION`, the notes digest and applicable authority.

1. Create a lightweight tag on the exact reviewed candidate:

   ```bash
   git tag "$NEW_VERSION" "$CANDIDATE"
   ```

2. Publish the branch and tag together:

   ```bash
   bin/dotfiles-publish push --run "$RUN_ID" --tag "$NEW_VERSION"
   ```

   Require success and verified remote refs. Follow `publish-dotfiles` for
   recovery, remote-tracking refresh and `post-push-ci`. Do not create the
   GitHub release unless the tagged candidate passes required CI. A code fix
   after publication requires a newly tested candidate and version, not moving
   the public tag.

3. Recheck that the notes file still has the approved digest, then create the
   release using that file:

   ```bash
   gh release create "$NEW_VERSION" \
     --repo benthamite/dotfiles \
     --title "$NEW_VERSION" \
     --verify-tag \
     --notes-file "$RELEASE_NOTES_FILE"
   ```

   If the request times out or returns an ambiguous failure, query the exact
   release before retrying. Do not duplicate, delete or replace a possibly
   successful release blindly.

## Step 12: verify and clean up

```bash
gh release view "$NEW_VERSION" --repo benthamite/dotfiles \
  --json tagName,body,url,isDraft,isPrerelease
git ls-remote --tags origin "refs/tags/$NEW_VERSION"
```

Verify the remote tag equals `CANDIDATE`, the release has the intended
publication state and its body matches the reviewed notes. A successful command
alone is not proof of those facts. Confirm `.current-profile` names the user's
live profile. Report the release URL, the dev profile the user is now running,
and any unresolved gate. Remove this workflow's temporary report, lockfile
candidate and notes only after verification or a deliberate abort; preserve them
for a pending resume.

For access, network or Emacs-query failures, diagnose the exact error and use
available authorized recovery paths. Do not label every 403 as rate limiting,
switch credentials speculatively or claim success with an unmeasured gate.
