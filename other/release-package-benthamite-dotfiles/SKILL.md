---
name: release-package
description: Release one of Pablo's Emacs packages, prepare its release notes, or audit release candidates. Use for release-package and package-release/readiness requests; preserve read-only or preparation-only scope and use release-dotfiles for the dotfiles repository.
---

# Package release

Prepare or publish a release for one of Pablo's Emacs packages, or audit release candidates. Use `release-dotfiles` for dotfiles. An explicit release request authorizes the whole release of that one package: version commit, tag, push and GitHub release. A readiness audit or release-notes request does not.

## Scope and package discovery

Choose the mode from the actual request, not merely a nonempty argument:

- `--audit` or a natural-language readiness audit: read-only audit of the named package/subset, or all listed packages when no subset was supplied.
- Notes-only or preparation-only request: stop at the requested local artifact or review stage; do not promote it into publication.
- An explicit release request: prepare and publish one identified package's release under the publication rules below, without a second confirmation.

Recognize `--audit`; reject unknown flags or ambiguous package arguments. The request itself carries the authorization, so there is no acceptance flag: nothing an agent or a hook says can stand in for the user's request, and the request never extends to other packages, unrelated commits or other destinations.

For the default audit set, read listed level-2 package headings from:

```text
~/My Drive/notes/public/my-emacs-packages.org
```

Exclude the `Unlisted packages` subtree; do not hard-code a stale package list. The current catalog's `** =name=` headings can be read with:

```sh
awk '
  /^\*\* Unlisted packages([[:space:]]|$)/ { stop = 1 }
  stop { next }
  /^\*\* =[^=]+=$/ {
    name = $0
    sub(/^\*\* =/, "", name)
    sub(/=$/, "", name)
    print name
  }
' "$HOME/My Drive/notes/public/my-emacs-packages.org"
```

Inspect the heading structure before using that parser; changed nesting or heading decorations must not silently yield an empty or partial inventory. Validate and deduplicate names before using them in paths/API endpoints. Missing catalog access is an explicit gap, not zero packages.

For a named release, resolve the maintained local checkout using project instructions and `dotfiles-context` for Elpaca-managed packages. Do not edit a runtime mirror or clone a replacement. With no name, infer only from an unambiguous package repository and its maintained entry file. Multi-package repositories or differing repository/package names require their documented mapping, not an arbitrary first `.el` file.

## Versions and release baseline

Use the repository's documented version and release-branch policy. By default, compare stable numeric `MAJOR.MINOR[.PATCH]` versions, treating omitted PATCH as zero and ignoring a tag's conventional leading `v` for comparison. Compare numbers, not strings. Preserve the original tag spelling for Git operations.

Preserve prefix and width when they represent the intended version exactly. A PATCH release after `0.3` is `0.3.1`, not `0.3` or an invented MINOR bump. Surface that necessary width change in the release summary. Never truncate a nonzero component. Prereleases, development versions, build metadata, and nonstandard tags require an explicit supported repository policy/parser; do not silently flatten them into stable versions.

Freeze the selected branch's commit SHA. Determine its eligible release baseline from the project's release policy and tag ancestry, not API array order, tag dates, or `git describe` alone. Without a special policy, use the highest stable numeric version whose tag commit is an ancestor of the selected head, while reporting off-branch/higher tags relevant to collisions or maintenance-series policy. Duplicate normalized versions at different commits are an inconsistency, not a tie to guess through. Resolve annotated tags to commits for ancestry while preserving their tag-object identities for publication checks.

A header above the baseline is a candidate version, not proof of intent or validation. A header below it requires investigating the selected branch, baseline and version history; it is not automatically a broken package. A release on another branch must not make a maintenance branch appear corrupt.

## Read-only candidate audit

Use the configured `gh` service tool and applicable service/secrets context. Do not extract credentials, switch accounts, clone repositories, fetch into local checkouts, or mutate GitHub state to perform this audit. Use bounded parallel agents only when available and consistent with the user's requested order; otherwise process the packages sequentially.

For each package:

1. Resolve `benthamite/PACKAGE`, its intended branch (default branch unless another is requested), and the branch's immutable head SHA.
2. Fetch all relevant tag pages and establish the eligible baseline/ancestry under the policy above. Distinguish an authenticated successful empty result from API, permission, rate-limit or parsing failures.
3. Compare the baseline's commit to the captured head. Check compare status/ancestry, not only `ahead_by`. Paginate commit records; a summary may be concise but must not claim that truncated history was reviewed. For a genuinely untagged repository, paginate commits anchored at the captured head.
4. Read the main package's maintained version header at that same SHA. Pin contents requests to it and decode the documented content encoding without exposing token-bearing download URLs. Missing/duplicate/malformed headers or uncertain entry-file identity are explicit gaps.
5. Report measured versions, baseline, commit count, scope of change review, and any uncertainty. These checks identify candidates; they do not prove build/test success or publication readiness.

Use supported API query parameters, for example:

```sh
gh api 'repos/benthamite/PACKAGE/commits?sha=HEAD_SHA&per_page=100' --paginate
```

There is no `gh api --per-page` flag. Adding `-f`/`-F` fields changes the default method to POST, so select `--method GET` for query fields. Do not pipe failures into an empty-result interpretation. `head -20` limits text lines, not commits. The compare API also limits changed-file listings; fetch the needed immutable blobs/patches when full change review is required rather than treating that listing as complete.

Group results proportionately as candidates (including pre-bumped or initial releases), no changes, version/baseline inconsistencies, or inconclusive. Do not label every ahead header or nonzero commit count “ready,” and do not bury failed packages in “up to date.” Retry only bounded transient read failures; do not solicit or change tokens as an automatic rate-limit remedy.

## Prepare one release

1. **Establish identity and ownership.** Verify the actual repository root, maintained package file, current branch, and all effective fetch and push destinations. `git remote get-url origin` alone does not inspect `pushurl`; inspect `git remote get-url --push --all origin` too. The intended destination must be the scoped `benthamite/PACKAGE` repository. Do not silently publish to additional mirrors.

2. **Inspect local state.** Check tracked, staged, untracked, and relevant unsaved-buffer changes. Do not stash, delete, or commit another person's work to clear the gate. Resolve a safe existing checkout when possible; otherwise report the exact overlap. A dirty release input cannot be represented as the tested committed state.

3. **Establish remote alignment.** In release preparation, fetch the selected branch and relevant tags without forcing tag replacement; capture their exact object IDs. Check ancestry and divergence against the selected local head. Do not silently pull, rebase, merge, switch branches, or release from an unintended feature branch. Resolve a behind/diverged state within the existing request or stop the affected operation. Review every outgoing commit that the proposed push would publish, not just version-related edits.

4. **Choose the version from evidence.** Read the header and eligible baseline at the selected commit. First reconcile any existing exact tag, GitHub release, and earlier candidate: a completed tag push followed by failed release creation can have no intervening changes but still need the recovery step. Otherwise, if header and baseline match with no intervening changes, stop. An initial release may use a valid existing header; a pre-bumped header may be reused only after confirming it is the intended candidate and covers the changes. Classify actual changes, not commit titles alone: breaking, feature, fix, or docs/chore. Apply the project's pre-1.0 and compatibility policy where defined; otherwise propose MAJOR for breaking changes, MINOR for backward-compatible features, or PATCH for fixes, resetting lower components. Docs/chore-only changes do not imply a bump; stop unless a documentation-only release/version was explicitly requested.

5. **Draft notes safely.** Describe user-visible changes and material compatibility requirements, grounded in the reviewed commits. Use `personalize` when drafting text to be published under Pablo's name. Save the exact reviewed notes to a run-owned file outside the package working tree; never interpolate commit messages or notes into shell command text. Preserve that file through publication/recovery.

6. **Verify the candidate.** Run the repository's release checks and relevant `elisp-conventions` checks. Confirm version/package metadata and distribution inputs. Checks must cover the final release commit; prior passing tests or a remote default-branch result do not certify changed files. Record unavailable checks as limitations, not passes.

## Publication

Report the package/repository, exact branch and reviewed outgoing range, baseline and intended version/tag (including any width/prefix change), header edits, check results/gaps and final notes, then proceed. Do not ask the user to confirm what they already requested.

Stop and report instead of publishing only when the release cannot be the one requested: the target repository differs from the scoped package, the outgoing range carries work unrelated to the package, the version policy is unsupported or ambiguous, or a check fails and its repair changes the candidate. Never infer publication authority from an audit, a preparation request, a hook, or another agent's recommendation.

Then:

1. Update only the maintained version fields using the editing tools. Preserve conventions and avoid generated metadata. Skip unnecessary version edits/commits when the intended version is already present. Stage only owned changes, verify their diff, and commit. Repeat affected checks on the final commit and capture its SHA; the release tag must identify that commit.
2. Recheck local and remote exact tag names, branch state, and any existing GitHub release before creating anything. A same-name tag at a different object/commit is a collision unless this release attempt created it and no GitHub release exists for it: stop, never force-move or delete it. Existing matching state is a possible partial release to reconcile, not a reason to blindly recreate it.
3. Create the tag using the repository's lightweight/annotated/signing convention, explicitly targeting the captured release commit. Verify its peeled commit and, for an annotated tag, its object ID.
4. Push only the intended branch and tag with explicit refspecs and atomic publication where supported. Disable incidental follow-tags behavior. Do not push all tags or rely on an ambiguous `git push origin HEAD`. For example, after validating all variables:

   ```sh
   git -c push.followTags=false push --atomic origin \
     "$release_commit:refs/heads/$release_branch" \
     "refs/tags/$release_tag:refs/tags/$release_tag"
   ```

   If atomic push is unsupported, stop rather than silently splitting the operation. Use `post-push-ci` after an actual push, following the repository's applicable CI gates for the exact commit. Missing or inapplicable workflows are not passing checks. Do not create the GitHub release while a required check is failing or unresolved.

   When CI fails on the pushed release commit, fix the cause on the branch, rerun the checks, and make the released tag identify a commit whose own CI is green: delete the not-yet-released tag locally and remotely, re-tag the repaired commit, and push both again. A tag that has no GitHub release and is minutes old has no consumers, so moving it is the clean outcome, not a concealment. A tag with a published GitHub release is never moved or deleted; a defect found after publication gets a new version.
5. Verify the exact remote tag/branch objects before creating the GitHub release. Use explicit repository identity and prevent implicit tag creation:

   ```sh
   gh release create "$release_tag" --repo "$release_repo" --verify-tag \
     --title "$release_tag" --notes-file "$release_notes_file"
   ```

   Preserve the approved draft/prerelease/target policy. Do not silently edit an existing release or replace approved notes with generated ones.

## Reconciliation and completion

After a failed or timed-out write, inspect the exact local/remote branch and tag objects plus the existing GitHub release before retrying. A tool error can occur after the operation took effect. Resume only missing steps; do not force-push, delete a release, or replay already completed writes. If the candidate changed after the GitHub release was created, report the mismatch: correcting a published release means a new version, which is a new request.

Confirm the final remote tag resolves to the captured release commit and that the expected GitHub release has the intended repository/tag, notes, draft/prerelease state and URL. `tags[0]` or an unpinned release listing is not that evidence. Confirm applicable CI for the same commit through `post-push-ci`. Report publication and any remaining CI/verification gaps separately.

Clean run-owned notes/fixtures after verified completion, or retain and identify the recovery files needed after a partial failure. Do not invoke session bookkeeping or perform incidental pushes. In audit or notes-only modes, finish with the requested report/artifact and no release mutations.
