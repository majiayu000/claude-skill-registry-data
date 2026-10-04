---
name: artefact-discipline-check
description: Routes a change through the correct workflow when the change touches a generated artefact or a protected branch. Use before hand-editing a file that is produced by a generator (build outputs, schema dumps, taxonomies, doc portals, scorecards, lockfiles). Use before pushing directly to, force-pushing, or `reset --hard`ing a protected branch (the default branch, release branches, long-lived integration branches). Use when CI flags generated-artefact drift or a protected-branch operation. The workflow redirects to "edit source, run the generator, commit both halves" or "open a PR through the documented merge mechanism", never to "hand-edit the artefact" or "force-push past the check".
derives_from: ../../governance/artefact-and-branch-discipline.md
---

# Artefact and Branch Discipline: Check

## Overview

Two related disciplines protect a project's audit trail: generated artefacts are read-only (the generator is the canonical statement of how the artefact derives from the source), and protected branches are append-only (the branch is the canonical statement of what the project's history looks like). This skill runs the routing workflow from the canonical rule [`governance/artefact-and-branch-discipline.md`](../../governance/artefact-and-branch-discipline.md) so a change about to take the forbidden path (hand-edit the artefact; force-push past the check) is caught and redirected at the moment of decision.

The rule is the source of truth for normative content (what counts as generated, what counts as protected, what the exception paths look like, framework alignment). This skill is the workflow wrapper: identify the trigger, classify the artefact or branch, route to the correct action.

## When to Use

- Before opening an editor on a file at the top of which sits a "Do not hand-edit; regenerate via X" notice, or any file your project's `## Boundaries` section names as generated.
- Before running `git push` directly to the default branch, a release branch, or a long-lived integration branch the project treats as protected.
- Before running `git push --force` or `--force-with-lease` against any shared branch.
- Before running `git reset --hard` over uncommitted work, especially work that did not originate with you.
- Before merging a change into the protected branch without going through the project's PR mechanism.
- When CI reports generator-output drift (a `--check` mode failure), or when branch protection refuses a push.
- When a lockfile (`package-lock.json`, `poetry.lock`, `Cargo.lock`, `go.sum`) is about to be hand-edited to resolve a conflict instead of regenerated with the package manager.

## Process

The routing workflow from the canonical rule, executed in order:

1. **Identify the trigger surface.** Two distinct surfaces; the routing differs.
   - **Generated artefact surface**: about to modify a file produced by running a command against other files (build outputs, schema dumps, taxonomies, doc portals, scorecards, lockfiles, generated tests, generated fixtures).
   - **Protected branch surface**: about to push to, force-push to, rewrite history of, or merge directly into a branch whose history other people (or other automation) depend on.

2. **For the generated-artefact surface, classify the file.** If the project's `## Boundaries` (or equivalent) lists the file as generated, or if the file's top-of-file notice says "Do not hand-edit; regenerate via X", or if running the generator's `--check` mode against the file would flag any divergence, the file is generated.

3. **For a generated artefact: redirect to the source-and-regenerate workflow.**
   - Edit the source the generator consumes (the `*.py` builder script's inputs, the `*.yml` schema, the per-document metadata, etc.).
   - Run the generator locally to refresh the artefact (the project's documented command; commonly `python3 tools/build-foo.py`, `npm run build`, or `make`).
   - Commit the source and the regenerated output together so the diff shows both halves; CI runs the generator in `--check` mode and fails on uncommitted drift.

4. **For a protected branch, classify the action.**
   - **Direct push to a protected branch**: prohibited.
   - **Force-push (`--force`, `--force-with-lease`) to a protected branch**: prohibited.
   - **`reset --hard` over uncommitted work that did not originate with you**: prohibited.
   - **Merging without going through the PR mechanism**: prohibited.
   - **Squash-merging when the project's convention is merge-commit (or vice versa)**: prohibited.
   - **Force-push to a feature branch you own, for legitimate rebasing or cleanup**: permitted.

5. **For a protected-branch operation: redirect to the PR mechanism.**
   - Develop the change on a feature branch named after the change.
   - Open a PR against the protected branch.
   - Wait for the required checks to pass.
   - Merge through the project's documented PR mechanism (squash, merge-commit, or rebase, per the project's convention).

6. **For a lockfile: redirect to the package manager.**
   - Run the package manager to update the lockfile (`npm install`, `poetry update`, `cargo update`, `go mod tidy`).
   - Commit the lockfile in the same commit as the dependency change.
   - Do not hand-edit the lockfile to resolve a merge conflict; re-run the package manager.

7. **If a genuine exception is required, follow the rule's exception protocol.**
   - For a generated artefact: document the technical reason the generator cannot be fixed in this PR; file a tracked issue with a remediation deadline; hand-edit the artefact with a comment marking the patch and linking the tracked issue; carry the documented exception link in the commit message.
   - For a protected branch: document the technical reason the force-push is necessary; obtain governance-authority approval; notify collaborators in advance; preserve the pre-rewrite ref under `refs/preservation/<short-reason>-<YYYY-MM-DD>/<original-ref-name>`; re-run the version-monotonicity audit after the rewrite.

## Red Flags

- "I will just edit the generated file directly; it is faster." The next regeneration silently overwrites the hand-edit; the divergence between source and artefact is invisible until then.
- "CI keeps flagging drift; let me regenerate in CI to make the check pass." This defeats the drift check by construction. See the gate-discipline rule: never weaken a gate to silence a failure.
- "I will strip the generator's `--check` job from CI; it is noisy." Same anti-pattern, blunter. The check exists because the drift it catches is real.
- "I will hand-fix the parts the generator got wrong." The fix is to the generator, not to the artefact.
- "Force-push to the protected branch is the fast path to undo the bad commit." The CI failure is signal; the force-push hides it. The fast path is the next commit, not the rewrite.
- "Direct push to the protected branch; the PR mechanism is overhead." The PR mechanism is the gate; merging around it is gate bypass.
- "I will demote the required check to optional just for this PR." Policy change subject to the same review as any other policy change; not a per-PR knob.
- "Hand-edited the lockfile to resolve the conflict; the package manager would have taken too long." The package manager is faster than the bug that the hand-edit will produce.

## Verification

The action is in the correct path when:

- For a generated-artefact change: the diff includes both the source-side change and the regenerated output; CI's `--check` mode passes on the committed result.
- For a protected-branch change: the change is on a feature branch; a PR is open against the protected branch; the required checks have passed; the merge will go through the documented mechanism.
- For a lockfile change: the lockfile is the package-manager-produced output, not a hand-edit; the dependency change and the lockfile change are in the same commit.
- For a documented exception: the exception entry exists, the deadline is set, the commit message links the exception, and the preservation ref (for a branch rewrite) is in place.

If any of these does not hold, the protocol is incomplete and the action is still in the forbidden path.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "It is just a one-line fix to the generated file." | A one-line hand-edit is overwritten by the next regeneration. The fix has to be in the source. |
| "Regenerating locally is slow; CI can do it." | Regenerating in CI defeats the drift check. The local cost is one command. |
| "Force-push is acceptable because no one else is on this branch." | Force-push to a protected branch breaks downstream branches and CI history. The branch's name and the project's intent are not enforcement; the protection settings are. |
| "The package manager is slower than just editing the lockfile." | The hand-edit produces a bug the lockfile-update would not. Time-to-correctness is what matters, not time-to-commit. |
| "The exception process is too much friction for a small change." | The friction is proportional to the residual risk of holding the gate open. Small changes that need the exception path were never small. |

## See Also

- Canonical rule [`governance/artefact-and-branch-discipline.md`](../../governance/artefact-and-branch-discipline.md): the full discipline, branch-protection settings, lockfile rules, long-lived integration branches, the version-monotonicity contract, exception-handling protocols, and framework alignment (NIST SSDF PO.3.2 / PS.1.1; CSA CCM CCC-01 to 04 / LOG-02 / LOG-04 / LOG-10 / AIS-04; ISO 27001 Annex A.8.32 / A.8.15 / A.5.4; SLSA v1.2 Source track, L2 and L4).
- Related skill [`gate-discipline-diagnose`](../gate-discipline-diagnose/SKILL.md): when the generator's `--check` mode fails or branch protection refuses a push, the fix is the artefact (or the action), not the gate.
- Related skill [`change-tracking-write-entry`](../change-tracking-write-entry/SKILL.md): an exception to either discipline (a documented hand-edit, a documented force-push) requires a CHANGELOG entry that records the exception link and the remediation deadline.
- Related skill [`action-before-explanation-of-inaction`](../action-before-explanation-of-inaction/SKILL.md): if branch protection blocks an operation, attempt the legitimate path (PR + merge through MCP or equivalent) and report the actual result; do not infer that "the branch is blocked because force-push is needed" without checking.
- Related skill [`skill-authoring-discipline`](../skill-authoring-discipline/SKILL.md): adding a new skill creates new artefacts in the pack; this skill confirms the generated-vs-source separation is respected (the pack README's skills tree is hand-maintained, not generated, so its update is normal; if a future pack switches to a generator for the tree, that boundary needs to be honoured).
