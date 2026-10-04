---
name: icaire-check-update
description: Check whether the ICAIRE workbench repo has an upstream or release update, pull it in safely, apply required local install changes, and verify the active skills and automations. Use when the user asks to update ICAIRE skills, check for ICAIRE workbench updates, keep ICAIRE skills current, or run the packaged update automation.
---

# ICAIRE Check Update

Use this skill to keep the local `icaire-workbench` checkout and active Codex
install current without clobbering teammate edits. The job is not complete when
updates are merely found or listed; apply safe updates, refresh repo-owned local
skills and automations, and verify the result.

This skill mirrors the packaged `icaire-check-update` automation. When both are
present, the automation handles the recurring daily check and this skill handles
manual on-demand updates.

## Contract

This skill guarantees:

- Check the tracked upstream and release tags before deciding there is an
  update.
- Prefer the newest release tag newer than the current checkout when releases
  exist.
- Preserve local edits, teammate customizations, and local commits.
- Read `CHANGELOG.md` after updating and apply every relevant `Agent update
  actions` section.
- Refresh installed ICAIRE skill symlinks from this repo when they are
  repo-owned symlinks.
- Refresh packaged ICAIRE automations from this repo when they are repo-owned
  installed copies.
- Do not overwrite copied local skills or locally customized automation
  definitions without preserving them first.
- Run the repo validator with active-install checks before reporting success.

## Workflow

1. Resolve the ICAIRE workbench repo:
   - use the current working directory if it is the `icaire-workbench` repo
   - otherwise use `~/projects/ICAIRE/icaire-workbench` when it exists
   - otherwise use `~/projects/ICAIRE/icaire-skills` when present and rename it
     to `~/projects/ICAIRE/icaire-workbench`
   - otherwise use `~/projects/icaire-skills` when present and rename it to
     `~/projects/ICAIRE/icaire-workbench`
   - otherwise ask the user for the repo path
2. Record the starting state:
   - `git status --short --branch`
   - `git rev-parse --abbrev-ref --symbolic-full-name @{u}`
   - `git rev-parse HEAD`
   - `git describe --tags --abbrev=0`, when a tag exists
3. Fetch upstream and tags:
   - `git fetch --prune --tags`
4. Decide the update source:
   - if release tags exist, identify the newest reachable release tag that is
     newer than the current checkout
   - otherwise compare `HEAD...@{u}` and use the tracked upstream branch
   - if there is no newer release and the branch is not behind upstream, report
     that no repo update was found, then still verify the active local install
5. Preserve local work before updating:
   - inspect `git status --short --branch`
   - if the worktree is dirty, create a clear local preservation commit for the
     user's edits before updating, unless the user explicitly says not to commit
   - if local commits exist, preserve them by rebasing rather than discarding
     them
6. Apply the update safely:
   - for upstream-branch updates, use `git pull --rebase --autostash`
   - for release-tag updates, rebase local commits onto the selected release or
     fast-forward to the release when there are no local commits
   - if conflicts occur, resolve only when intent is clear by keeping both
     upstream improvements and teammate-specific enhancements
   - if intent is unclear, stop and report the exact conflicted files and the
     suggested reconciliation
7. Read release notes:
   - compare the previous HEAD and final HEAD against `CHANGELOG.md`
   - identify every release entry that may have landed
   - read each relevant `Agent update actions` section before changing the
     active install
   - if no release entry covers the changed range, report that and continue
     with generic install refresh and verification
8. Refresh installed ICAIRE skills:
   - use `README.md` as the catalog source of truth
   - install general-purpose skills by default
   - keep any previously selected role-specific ICAIRE skill symlinks when they
     already point into this repo
   - create or refresh symlinks under `${CODEX_HOME:-$HOME/.codex}/skills`
   - remove stale repo-owned symlinks for skills no longer selected
   - do not overwrite non-symlink copied skills; back them up first or report
     the manual follow-up when preservation is unclear
9. Refresh packaged ICAIRE automations:
   - copy each `automations/*/automation.toml` template into
     `${CODEX_HOME:-$HOME/.codex}/automations/<automation-id>/automation.toml`
   - refresh repo-owned installed copies
   - preserve locally customized automation definitions before replacing them
   - never restore `icaire-ingest-granola`; Granola discovery is owned by the
     single machine-wide BigBrain router and ICAIRE contributes only its
     approved destination profile and ingestion policy
10. Apply every relevant changelog `Agent update actions` item:
    - install newly added skills
    - refresh changed skills
    - install or refresh added automations
    - remove stale repo-owned skills or automations when instructed
    - keep rollback copies outside the live Codex automation root
    - run required verification commands
11. Verify:
    - run `python3 tests/check_skills.py --active-install`
    - confirm `icaire-check-update` resolves in the active local skills root
      when this skill is present in the selected install set
    - confirm every packaged automation file exists under the active automation
      root and matches the packaged template
    - treat missing, stale, mismatched, or misplaced active install files as a
      failed update until they are refreshed or explicitly reported as blocked
    - inspect `git status --short --branch` after the update

## Guardrails

- Do not use `git reset --hard`, `git checkout --`, or destructive cleanup.
- Do not discard unrelated local edits.
- Do not claim an update was installed unless the local HEAD changed or the
  upstream/release comparison proved it was already current.
- Do not overwrite copied local skills or customized automations without
  preserving them first.
- Do not treat repo-template validation as active install validation. Codex can
  only use skills and automations under `${CODEX_HOME:-$HOME/.codex}`, so verify
  that root explicitly.
- Do not skip `CHANGELOG.md`; release entries are the source of truth for local
  install update actions.
- Do not run local BigBrain indexing, sync, or health checks against the ICAIRE
  brain as part of this repo update.

## Output

Report:

- repo path
- starting branch and upstream
- whether an update was found
- previous HEAD and final HEAD
- release version or upstream source applied
- changelog agent actions applied or skipped as not applicable
- teammate edits preserved or replayed
- conflicts resolved or blockers found
- refreshed skills
- refreshed automations
- verification commands and pass/fail status
- any unresolved manual follow-up
