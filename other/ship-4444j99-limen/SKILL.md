---
name: ship
description: Drive one change from implemented to LIVE-VERIFIED and merged — scoped gates, PR, required-checks merge, live-artifact proof, closeout predicates — with no status stalls in between. Use when asked to ship, land, or deliver a change end-to-end.
---

# Ship

One concern → one branch → merged into `main` → **proven live** — executed end-to-end without
pausing to report status (2026-07-04 censor precedent `friction-shallow-first`; the standing
autonomy grant in `CLAUDE.md` → Standing Autonomy). This skill COMPOSES the existing machinery —
it introduces no new predicate; every step names the script that owns it.

## Steps

1. **Isolate + implement.** Work in a git worktree on a topic branch cut from `origin/main`,
   named by intent (`feat/`, `fix/`, `heal/`, `chore/`, `docs/`, `refactor/` — CLAUDE.md → Merge &
   Branch Protocol). One concern per branch; stage explicitly with `git add <path>`, never `-A`.
   For a one-file docs append, use `scripts/ship-docs.sh <slug> "<msg>" <file…>` instead of steps
   2-4 — it is this whole skill in one command for the docs class.
2. **Gate scoped to the diff.** `bash scripts/verify-scoped.sh` — it maps changed paths to only
   the gates they implicate and names every skipped gate. Fix root-to-leaf and re-run until green.
   Never hand-run the full matrix for a scoped diff; never chase a gate the diff doesn't implicate.
3. **Push + PR.** Push the branch, `gh pr create` with the green gate run cited in the body.
4. **Merge on the predicate, not on memory.** `scripts/merge-policy.sh <PR#>`:
   - exit 0 CLEARED → `scripts/await-pr.sh <PR#> --merge` (the ONE sanctioned waiter — bounded,
     loud, single-instance; never a hand-rolled poll loop).
   - exit 2 HOLD → required checks still running; `await-pr.sh` waits them out within its deadline.
     Anything longer belongs to the beat's merge rung (`scripts/merge-drain.py` via
     `scripts/drain.sh`) — hand off and continue other lanes; never babysit.
   - exit 3 BLOCKED → repair the real conflict/check, then re-run. Never force.
   Read `logs/AUTONOMY_PAUSED` first — a merge-prohibiting marker stops this step (await-pr
   refuses on its own, but don't even arm it).
   Non-deploy verdicts count **required** checks only; advisory checks never hold a merge.
   Website-sensitive PRs require the full rollup green — merging IS the deploy.
5. **Prove it LIVE — the artifact, not the merge.** A merged PR is not a shipped change
   (2026-07-24 insights lineage: a redesign verified only on synthetic renders; the live surface
   never changed). For any user-visible/product-facing claim, run `python3 scripts/ship-gate.py`
   (reachable deployed URL, from `spec/ship-surfaces.json`) or the change's own probe
   (`scripts/probe-runtime-adapter.py`, `scripts/experience-audit.py`, `scripts/link-health.py` —
   whichever owns the surface). If the artifact needs regeneration after merge, regenerate and
   push it — the engine merging is not the profile changing.
6. **Close out.** `scripts/no-tasks-on-me.sh` and `scripts/credential-wall.py --check` both exit
   0; loose work committed; then the relay: what shipped, predicate verdicts as proof, one
   registry pointer for anything homed. No caveat tail. For a full session closeout, run
   `/closeout` — this step is its per-change instance.

## Gate

A change is SHIPPED only when: the implicated scoped gates are green, the PR is MERGED via
`merge-policy.sh`/`await-pr.sh`, the live artifact is verified (step 5 predicate exit 0 or a cited
probe), and the closeout predicates are green. Merged-but-not-live is NOT shipped — say so
plainly, with the failing probe output.
