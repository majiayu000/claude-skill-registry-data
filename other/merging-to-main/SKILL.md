---
name: merging-to-main
description: Keyword-gated by name. Merge a ready branch to main via PR.
argument-hint: "[--force] [--force-merge-active-branch]"
version: 2.0.0
allowed-tools: ["Read","Write","Edit","Bash","Grep","Glob","Agent","Skill","AskUserQuestion","TaskCreate","TaskUpdate","TaskGet","TaskList"]
---

# Merging to Main

## Overview

Merge a work or feature branch to main via PR, gated by local validation — GitHub Actions is not in
the loop. `merge-assemble` computes the gates and
directives (`d0`-`d8`). What follows is what it cannot precompute: your judgment calls, plus the
steps depending on live PR/merge state.

**Announce at start:** "I'm using the coordinator:merging-to-main skill to merge this branch to main."

On a PowerShell host, invoke the `.exe` launcher by absolute path through the call operator
(Shape W) — ladder and shapes: `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`.
Compute and apply are one verb — `brief` was removed (K-114): `merge-assemble apply [--session-id <id>] [--force] [--decisions-file <path>]`, resolved per that ladder. Resolve every `judgment_points[]` entry it returns, via `--decisions-file`, before its gated directive(s) proceed. `--force` bypasses only the node ceremony hard-gate (`d0`).

**First Officer Doctrine:** EM may refuse to merge and alert the PM on a branch with known issues.

---

## Step 1: Test Suite Gate

Pre-authorized Tier-U ceremony — grant first: `tier-u-grant-cli grant ceremony
"merging-to-main implicit Tier-U grant for the pre-merge unscoped project test suite" --ceremony
merging-to-main`.

`d0` (`node --test tests/plugin-ecosystem/run.js`, halt-on-fail) runs first, then detect and run
the project's own test runner (`pnpm test`/`npm test`, `pytest`/`python3 -m pytest`, `/validate`, or
project-specific from `CLAUDE.md`/`package.json`). **This is the most expensive step in the whole
ceremony** — a machine-wide event (magnitude: `python3 coordinator/tests/_spawn_budget.py`). Fail on either →
halt: _"Test suite failed. Fix first, or use `/merging-to-main --force` to bypass for hotfixes."_

**`--force`** (skill flag, distinct from `apply`'s): skips this step including the Tier-U grant and
`d0`. Log: _"Force-merge requested — test suite gate bypassed."_

---

## Step 2: Pre-flight

Commit only paths this session touched, on the commit invocation itself (detail: wiki).

On a work/feature branch → continue. On main with unpushed commits ahead of `origin/main` →
auto-recover via `merge-recovery-and-tag-cut recovery-branch` (cuts a fresh `work/<host>/<date>`
branch off the pre-sync state, pushes, resets main, prints `BRANCH=<name>`), then continue there. On main with nothing unpushed → abort:
_"Already on main with nothing to merge. Switch to a work or feature branch first."_

Resolve the branch via `coordinator-current-branch`, decide unpushed state with `coordinator-invoke push.outstanding '{}'`, and push with `--set-upstream` when it reports commits ahead.

---

## Step 3: Release Surface (your call)

`d6`/`d3`/`d5`/`d1`/`d2` are directives (illegal-path scan, coverage gate, portability sweep,
tag-prefix resolution, release-tag cut). Judgment:

**Ship verdict (`ship_verdict`).** EM stages one line, PM confirms or overrides; don't merge on
`hold`/`split` without PM redirect. `/staff-session vp-product` gives a structured second opinion.

```markdown
**Ship verdict:** [ship | ship-behind-flag | hold | split | spike-only] — [one-sentence rationale]
```

| Verdict | Meaning |
|---|---|
| ship | AC satisfied/waived, evidence supports merge |
| ship-behind-flag | Ready but gated — name the flag |
| hold | Don't merge — name the concern |
| split | Two changes land separately — name them |
| spike-only | Informative only, don't merge |

**Release-note framing.** Prefer the latest `state/week-changelog/*-pending-release.md`
accumulator; absent, draft inline by impact (Added/Changed/Fixed/Deps/Internal; template: wiki).
When a tag is being cut, run `merge-release-notes-derive missed-releases <tag> $ENTRY_PATHS` first:
each entry it names shipped in an earlier release that never flipped, so leave it out of these notes.
Prepend to a repo-root `CHANGELOG.md` if one exists, committed before Step 5. `tasks/`/`tmp/`-only
merges get an "Internal" line only.

**Demo path** (user-visible merges) — append a Demo Path section (template: wiki) to the PR body.

**Version-bump (`version_bump_final`).** `version_bump` is a proposal only — confirm/override
before `d2` fires (mode detail: wiki).

**Portability (`portability_disposition`).** Empty sweep report continues silently; non-empty needs
a per-finding PM disposition (options: wiki). Not a merge blocker;
`COORDINATOR_OVERRIDE_PORTABILITY=1` skips it for a one-off.

---

## Step 4: UE-specific checks (`project_type: game-dev`, `project_subtypes: unreal`)

Otherwise skip. Detection table (all five checks): wiki. UBT and reverse-drift gates have live
producers — non-zero halts with remediation (or the matching `COORDINATOR_OVERRIDE_*`). Plugin-
version-matrix, structural-index-schema, and install-path touches need eyeball diff-path
classification — no producer yet
<!-- engine-gap: field=merge.touched_path_classes producer=unknown memo=engine-gap-markers-name-a-memo-that-was-never-filed.md -->.
A schema bump needs `schema-migration-auditor` dispatched, the Staff Engineer review before merge.

---

## Step 5: Create PR

Compose the PR body via `merge-gate-and-pr pr-body --ship-verdict "$SHIP_VERDICT" --summary
"$SUMMARY" --release-notes "$RELEASE_NOTES" --verification "$VERIFICATION" --risk "$RISK" --links
"$LINKS" --commit-range main..HEAD` (`d4`), then `gh pr create --base main --head "$BRANCH" --title
"$TITLE" --body "$BODY"`. Pass `--release-notes` and `--demo-path` without headings of their own,
release-note version headings at `###` or lower. Exit 2 `unrecognized arguments` (older engine):
rerun without `--summary`, `--verification`, `--risk`, `--links`.

If a version bump was suggested but not yet PM-confirmed, surface it in the PR body: _"Suggested
bump: patch ({old} → {new}) — confirm before tagging."_

---

## Step 6: Local Validation Confirmation

Step 1's local run is the gate — confirm it passed on the exact head being merged (re-run
`/validate` if commits landed since). A failure blocks merge — _"Validation failed
on {test}. Fix and re-run `/merging-to-main`, or investigate via `coordinator:systematic-debugging`."_

---

## Step 7: Merge

Pre-merge quiet check: `merge-gate-and-pr active-branch-guard --pr "$PR"` halts if the PR's newest
commit is younger than 300 seconds. Override with the skill's own `--force-merge-active-branch`.

Merge via `gh pr merge` (no `--delete-branch`), merge commit (never squash). The head branch is
deleted only when its remote tip is an ancestor of the base — a merged PR merges a snapshot, not
the branch's later pushes; otherwise keep it and report the tip and its unmerged-commit count. Recovery recipes for
"base branch policy prohibits" and "head not up to date": wiki. **Merge conflicts** — do not force
through; offer the PM merge-main-in-and-resolve (recommended) or rebase; stop and wait.

The PR requirement (0 approvals) and Step 1's local validation are the gates.

**IF `d2` CUT A RELEASE TAG, VERIFY IT CONTAINS THE RELEASE — HERE, BEFORE ANYTHING ELSE:**

    git fetch origin --tags && git rev-list --count <tag>..origin/main

**Non-zero means the tag does not contain the release and the publish is wrong.** Retarget it
against the merge commit `gh pr merge` produced and force-push with a pinned lease; do not proceed
to Step 8 until it reads 0.

`d2` fires in Step 3 but the merge lands here, so the tag can point at main without the branch;
nothing else catches it. Run the check every time. Why: wiki § Tag-contains-release guard.

Once the merge lands, trigger the SCIP rebuild best-effort in the background (never blocks): `"$_py"
"${CLAUDE_PLUGIN_ROOT:-<content-root>/coordinator}/bin/scip-rebuild-at-ceremony.py" --ceremony
merge-to-main` (§ Plugin-local `coordinator/bin/`, `resolve-coordinator-bin.md`).

---

## Step 8: Post-Merge Re-Verify Shared Infra

After a conflict-resolved or concurrently-edited merge, confirm each touched file still carries a
canonical phrase from your change at `HEAD`; missing → re-apply and push a follow-up commit.

---

## Step 9: Local Cleanup

Check out main (`COORDINATOR_OVERRIDE_BRANCH=1`), pull, delete the local branch. Clear any stray
worktree (`git worktree remove <path>`).

---

## Step 10: Completion-Log Status Flip

Runs when a release tag was cut (`d2` landed); skip otherwise. `mkdir -p
archive/release-notes/`, then `d7` (`merge-release-notes-derive flip-tags <tag> <sha> <date>
$ENTRY_PATHS`) flips every matching entry to the earliest release tag whose history contains it. Best-effort `git mv` the pending-release accumulator to `archive/release-notes/`, scoped-commit
`$ENTRY_PATHS` + accumulator + release notes file, push to main.

---

## Step 11: Report

```
## Merged to Main
- **PR:** {url}
- **Merge commit:** {sha}
- **Branch deleted:** {branch} (local + remote)
- **Now on:** main @ {sha}
```

`d8` (`orphan-branch-sweep --format text --severity-min warning`, non-`OK` lines) surfaces other
in-flight branches: _"Multiple work branches in flight — verify these don't carry work intended for
this PR."_

**Negative-spec — the auto-memory drain gate is gone from this ceremony, do not restore it.**
Why: wiki § Retired: auto-memory drain gate.

## Red Flags

**Never:** squash commits; push directly to main. Concurrent-writer caveat: cap commit sweeps at
~6 and accept a moving target — don't loop trying to converge.

## Integration

**Called by:** `coordinator:finishing-a-development-branch` (Option 1); PM/EM directly, never
`/workday-complete`.
