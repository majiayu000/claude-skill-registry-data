---
name: full-patrol
description: Suki's full patrol for a queue of independent PRs. Each warrior walks her own route to the end, and Suki inspects every route before the human signs off. Use for autopilot-full, "autopilot this queue", "full autopilot", one owner per PR, or a batch of independent PRs to drive to merge-ready with full autonomy while the operator clicks every merge.
---

# Suki's full patrol

On a full patrol every warrior walks her own route from the gate to the far wall, and no two routes overlap. Suki does not walk the routes for them. She sends her own inspectors to check each one, and only then does she report it clear to the captain, who gives the final word. You own the verdicts, never the PRs. One owner carries each PR from build to merge-ready. Nothing merges until your formation, which never wrote the code, has proven the code that lands and the operator has clicked the merge.

A verdict covers one patch, and green CI covers one head. Step 4 runs a full formation once, and again only for a major change. The patch-id rule in `safe-landing` can carry a lane's result to a new head, and every new head needs its own green CI.

Prove behavior with the project's verify skill (see `vital-signs`), or with Claude Code's `run` skill when the repo has none.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

## Steps

1. **The operator's gates come first.** The grant covers only the queue's items, so items the operator names as theirs and PRs outside the queue stop at merge-ready. A request to state the plan is not a go. On the operator's go, write the full program objective into the standing orders and restate it in your todolist, so it stands across turns until the queue is done. Before the first owner starts, tell the operator the size of the program: the number of owners, the verifier lanes in the first round, and the ceiling of two fix-forwards per PR from step 4. A program of more than three owners waits for the operator's go on that size, unless the operator's request already named it.
2. **Spawn one owner per PR, and keep its work where a replacement can find it.** Resolve the forge once for the program. GitHub CLI (`gh`) is the default. If `command -v origin` succeeds and Origin can resolve the repository, use `origin pr` for every PR operation. Otherwise stay on `gh` and record the fallback. Never require Graphite (`gt`). Each owner is a background subagent, dispatched as `team-avatar:appa` with Appa's model from the avatar-setup sheet, in its own worktree. It builds, opens its PR per `yip-yip`, proves the change on the real artifact, drives it to green per `long-flight`, and hands the PR off at merge-ready once steps 4 and 5 clear it. No owner runs the merge. Where the runtime lets a subagent spawn one, an owner may dispatch its own workers and reviewers. Where it cannot, it does that work itself with the same review separation.

   Open the PR early so CI and bots run alongside the work. The code is ready only after the `purify` pass and the `clear-water` pass, so the full formation runs on finished code. Then rebase onto current trunk and report the code-ready head before self-proof, so verification runs on the base the patch lands on. Report every later head, and report merge-ready once self-proof, CI, and `long-flight` are done. Fix rounds stay on that base unless trunk conflicts or breaks CI, because each rebase restarts CI. Run the repo's checks for the touched paths on the committed head before the code-ready push and before any later push that needs a verifier.

   Assume the owner's session dies. Soon after starting, the owner pushes and starts a decision trail with `battle-map` in the program's store at `${CLAUDE_CONFIG_DIR:-~/.claude}/orchestrate/<slug>/` (on Codex, `${CODEX_HOME:-~/.codex}/orchestrate/<slug>/`), then pushes after every unit worth keeping. Whoever spawns a subagent records its id, its state, and a stuck-after runtime from past runs of its kind in that store, so the root can probe it if the parent dies. An owner force-pushes only its own branch, with `--force-with-lease` pinned to the SHA it last pushed or took over. On any push it did not make, it stops and reports to the root.
3. **Run owners in parallel off trunk, never stacked,** so each PR lands on its own. When the work is sequenced or coupled, use `shield-wall` instead.
4. **Verify with one full formation.** A full `kyoshi-formation` runs once, at the code-ready head. Another full formation runs only for new behavior, a redesign, or a large new diff. A rebase, a merge-conflict resolution, or a minor fix gets a single verifier at the new head. Fan out independent verifiers at the code-ready SHA on Suki's model. They re-run the gates, prove the load-bearing behavior live on the real surface through the verify skill, and audit the diff. Toph takes the diff audit with `earth-rumble`. The verdict is not clean without the live lane, and not before you audit the receipts in the merge-ready report, because no lane trusts a claim it has not checked.

   Send every proven finding, whatever a lane labeled it, to the owner in one fix-forward, with a red test across every site that has the same defect. A defect that trunk shows without the PR is recorded against trunk and does not gate the PR. One the PR copies or newly reaches is the PR's own. Never push a fix yourself, because each branch has one writer. Replace a stuck owner instead.

   Brief every review lane to report what the diff breaks, not everything wrong in the files it touches. Ask for no mutation or fuzz campaign unless the operator asked for one. Two fix-forwards per PR is the ceiling. When a blocking finding survives the second, stop work on that PR. Report it blocked with the finding and its evidence, and let the operator choose another round, a narrower PR, or closing it.
5. **The operator merges only what you verified, tested on the trunk it lands on.** Green CI alone never authorizes a merge. Your clean verdict is a precondition for the operator's click, never a substitute for it. Once the formation's lanes have started, merge prep rebases onto current trunk, reports the new head, and waits for green CI.

   Right before the hand-off, fetch trunk and ask whether its changes can affect the patch, because rebasing for every trunk move never ends.
   - Rebase and wait for CI when the code that would land was never tested, as with a conflict, a file both sides changed, or a change to which checks run for the PR.
   - A lockfile both sides changed needs no rebase when a frozen install passes on the merge result and the packages the PR changes resolve there as on the head. That install tests the lockfile that would land. A failing install means the rebase must repair it.
   - When trunk changed a caller of the patch or something the patch depends on (code it calls, a dependency version), run the patch's checks on the merge result and hand off on a pass.
   - Otherwise hand off.
   - If trunk would force a third rebase past merge prep, hold and report to the root, which sequences the colliding work.

   The owner presents the merge-ready PR to the operator with its verdict and pinned head SHA, then returns. A fresh owner takes the next item, per the dispatch rules in `avatar-mode`. If trunk moves again before the operator merges, the patch-id rule in `safe-landing` governs re-verification.
6. **Run the root layer.** Anything that loosens a gate, such as a raised budget or an allowlist entry, needs a verifier's proof and then your fresh countersign, because the owner is the one who wants green. Under a grant that covers approvals, that countersign is the approval, and the owner's record of it points at your countersign for a lane to check. A disabled or soft-failed check always comes out, because it stops guarding every case. Never give or bypass an approval the forge enforces, because no countersign covers it.

   On the operator's go, arm an hourly audit tick as a real `/loop` in dynamic mode, which schedules its own wake-up rather than blocking on a sleep. Keep it until no delegated work is left, because long runs drift and agents stall silently. Each tick does this:
   - Re-read this skill from disk under the installed plugin, and re-read the standing objective.
   - Fix drift, such as an unreported head or an unrecorded agent, by having its owner record it. Drift is a gap in the record, not a stall.
   - Probe every agent, down to the leaf lanes, and judge each by its side effects (pushes, trail rows, ledger rows). Status text and summaries can hide a stuck child.
   - Call an agent stuck when it errors, cannot start turns, or shows nothing new past its stuck-after runtime. An owner that has neither pushed nor written a trail row by the first tick is stuck too. One waiting on you or the operator is not stuck, so answer it.
   - Replace a stuck agent at once, without waiting for its stop to land.
   - End a tick that changed something for the operator by catching them up per `iceberg-wake`. A tick that changed nothing stays quiet.
7. **Stand down at once on the operator's stop.** A hold reaches every owner as a zero-writes order. Each reports where it stands and keeps its brief until the operator releases it.

## Reply

Catch the operator up per `iceberg-wake`. Cover each PR's state and verdict, what is merge-ready for the operator's click, countersigns and why, and open operator gates. Link each PR as `https://github.com/<owner>/<repo>/pull/<number>` and link the trails.
