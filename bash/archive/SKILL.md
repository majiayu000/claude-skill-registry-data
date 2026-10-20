---
name: archive
owner: baseline
description: Phase 10.5 — move the slug's workflow artifacts (intake, scout, research, spec, approvals, swarm state, security reports, rendered diagrams) to docs/archive/<YYYY-MM-DD>/<slug>/. Runs before /commit so the committed tree is clean of work-in-flight files. workflow.json stays live and gets archived as the first step of /commit.
---

# archive — Phase 10.5

Invoked after `/document` and before `/commit`. Pillar 4 of seed.md ("no historical data — moved to archive") happens here.

The archival *bundle* is planned at spec time — the spec's slug determines which files travel together. This skill is the executor.

## Prereq

`workflow.json` must have `document` in `completed` OR in `exceptions`. Otherwise stop and say which phase is missing.

## Steps

1. Read `.claude/state/workflow.json` to get the slug (derive from `request`, or from any `docs/specs/*.md` that was produced — whichever is present).
2. **Render the per-phase timing table FIRST** (before the move, while the consent tokens are still in `.claude/state/`):
   ```
   node .claude/hooks/lib/timing.mjs render <slug>
   ```
   It reads the `phase_timer` stamps at `.claude/state/timing/<slug>.jsonl` plus consent-token mtimes (`spec_approvals/<slug>.approval`, `commit_consent`) and writes a per-phase model-time-vs-human-wait table to `<bundle>/timing.md`. The table is *born in the bundle* (it creates the bundle dir). It must run before Step 4 because the archive script moves `spec_approvals/<slug>.approval` into the bundle — render it first or the approve-direction gate's human-wait reads `n/a`. Best-effort — a missing/sparse timing log yields a header-only table, never an error.

3. **Verify the spec's declared delta against the landed diff with `verifyAndApplyDelta`, then apply only what it confirms** (gated by `memory.architecture_map.enabled`; skip the whole of Steps 3 and 5.5 when false). This is what keeps `docs/system/` true to what is on disk instead of drifting the moment the next cycle ships.

   **It must run before Step 4, for the same reason Step 2 does.** `archive.sh` moves `docs/specs/<slug>.md` into the bundle; after that `resolveSpecPath` returns `null`, the `## System delta` table is never read, and every array below comes back empty — which is byte-identical to a spec that declared nothing. Verify first, or a real drift archives silently green. The `specMissing` field exists to make that failure loud if the order is ever changed back: when it is `true`, the empty arrays mean *the table was not read*, not *the table was clean*.

   ```
   node .claude/skills/workspace/cli.mjs delta --slug <slug> --touched '["path/one.mjs","path/two.mjs"]' --json   # wraps workspace/delta.mjs -> verifyAndApplyDelta
   ```

   **Pass the paths as one quoted argument, never as bare space-separated words.** Both a quoted JSON array (above) and a quoted comma-separated list (`--touched 'a.mjs,b.mjs'`) parse. The repo's default shell is zsh, which does not word-split an unquoted `$VAR`, so a variable holding N paths arrives as a *single* argument containing spaces and matches no anchor. `verifyAndApplyDelta` reports that case as `inputEmpty: true`, distinct from an honest "nothing matched" — but a single quoted argument is immune to word-splitting in both zsh and bash, so pass one and the distinction never has to be read.

   The signature previously named the comma form while this paragraph instructed the array form in bold, and only the comma form parsed. Measured 2026-08-13 on one spec and tree: the array gave confirmed 0 / drift 6, the comma list gave confirmed 6 / drift 0, and `inputEmpty` was `false` both times — so the field that separates malformed input from an honest no-match was defeated by following the instruction. Accepting both forms is what closed it.

   Scope the list to the **governed surface** (`memory.architecture_map.governed_surface`) — its roots, its code extensions, minus its excluded segments and trees. Corpus files under `docs/system/` are the model itself, not governed surface, so a relocation of the corpus contributes no touched paths.

   Read the arrays before moving on. Each names a different thing the operator owes an answer to:

   | Field | Meaning | What to do |
   |---|---|---|
   | `specMissing` | the spec could not be read at all, so no row was ever parsed | the arrays below are not evidence. Check the step order and the slug before believing them |
   | `confirmed` / `applied` | the spec declared it and the diff proves it; the anchor, digest and shard landed | nothing — this is the success path |
   | `drift` | the spec declared it and the diff does **not** confirm it | the row is wrong or the work did not land. Nothing was written for it. Fix the spec or the code |
   | `unclaimed` | the landing touched a governed path no row claims and no element anchors | a coverage gap. Declare it in a `## System delta` row, or accept it deliberately |
   | `skippedGlob` | applied, but glob-anchored, so it earned no digest | expected for a family anchor; a *file* anchor here means the element is unwitnessed |

   Only confirmed rows are written. A declared row the diff cannot confirm applies **nothing** — no anchor appended, no shard, no digest — which is what makes this step evidence rather than a re-stamp. There is no bulk-refresh path: re-stamping untouched elements would make the model permanently green and launder the drift the digest exists to catch.

3.9. **Snapshot the corpus before anything moves.**

   ```
   node .claude/skills/archive/reverify-guard.mjs capture <slug>
   ```

   This must run BEFORE Step 4, for the same reason Steps 2 and 3 do: after the move there is no pre-archive state left to compare against, and `check` would then have nothing to prove a skip with and would re-verify every time.

4. Run the archive script (move-only; it never touches the already-rendered `timing.md`):
   ```
   .claude/skills/archive/archive.sh <slug>
   ```
   The script moves (`git mv` if repo is git, else `mv`) these artifacts — whichever exist — to `docs/archive/<YYYY-MM-DD>/<slug>/`:

   | Source | Target in bundle |
   |---|---|
   | `docs/intake/<slug>.md` | `intake.md` |
   | `docs/brief/<slug>.md` | `brief.md` |
   | `docs/brd/<slug>.md` | `brd.md` |
   | `docs/scout/<slug>.md` | `scout.md` |
   | `docs/research/<slug>.md` | `research.md` |
   | `docs/specs/<slug>.md` | `spec.md` |
   | `docs/specs/_rendered/<slug>/` | `spec-rendered/` |
   | `docs/security/<slug>-*.md` | `security.md` (concatenated if multiple) |
   | `.claude/state/spec_approvals/<slug>.approval` | `spec.approved` |
   | `.claude/state/swarm/<slug>.json` | `swarm.json` |
   | `.claude/state/swarm_approvals/<slug>.approval` | `swarm.approved` |
   | *(generated by Step 2 above, not moved)* | `timing.md` (per-phase model-vs-human-wait table) |

   Note that `docs/specs/<slug>.md` leaves its source location here. Anything that needs to read the spec runs before this step, not after — that is why Step 3 sits where it does.

5. **Do NOT move `workflow.json`.** `/commit` archives it as its first step so the phase ordering is preserved until the end.

5.5. **Gate on corpus health, and repair nothing** (same flag gate as Step 3; skip when false):

   ```
   node .claude/skills/system-reconcile/cli.mjs report --gate --json
   ```

   **A non-zero exit fails the phase.** Do not read the JSON and decide; the exit code is the verdict. Six of the seven sections gate — `stale`, `dangling`, `duplicateAnchors`, `orphanShards`, `unillustrated`, `missingKind` — and a breach names the section and the offending members. `gaps` is reported and never gates, because unanchored files pre-date this rule and blocking on them would fail every workflow until each one is anchored.

   The gate also fails when the report **could not be produced**. Seven empty arrays are what a clean corpus, an opted-out project and a crashed read all return, so emptiness alone is not health — `reconcileForGate` carries the discriminator that tells them apart (security review 2026-08-07, MEDIUM #2, deferred until this gate needed it).

   Until 2026-08-25 this step only printed, and that is precisely how a degraded corpus write reached a commit: it surfaced the breach and left the decision to a reader. A blocking rule nobody is obliged to act on is advice, so it is now an exit code.

   **Still no repair path.** `docs/system/` SHALL be byte-identical between Step 3 completing and the workflow ending — Step 3 is the corpus's single writer on the primary tree, and `/system-reconcile` exposes no apply path a workflow phase can reach. A repair the gate demands is a human-confirmed invocation of `/system-reconcile`, never an automatic follow-up to archiving.

   Ordering is load-bearing: Step 3 re-stamps the digest of every element whose anchor this landing touched, so a `stale` breach here is a real drift rather than the workflow's own edit awaiting its stamp.

5.7. **Re-verify when the archive invalidated the binding verdict.**

   `/integrate` stamped `.claude/state/last_test_result` at Phase 9. Step 4 has just changed the tree, and `/commit` will stage that change, so the verdict no longer covers what is about to be committed. Measured 2026-08-26: the `discard-ledger-audit-allowance` bundle re-fitted the `tdd-quickfix` envelope from 39,105 to 38,227 tokens and turned CI red on the commit that had just landed.

   ```
   node .claude/skills/archive/reverify-guard.mjs check <slug>
   ```

   Exit **3** — no per-track fitted envelope moved, no archived `spec.md` appeared or changed, and no new artifact filename entered a bundle. Those three are what the live-tree checks read; the digest covers them and deliberately omits bundle count and bundle paths, which move on every archive. Keep the existing stamp, say so in the Step 7 report, and continue. Exit **0** (changed, missing snapshot, unreadable tree, or any error) — re-run `project.json → test.cmd` and re-stamp `last_test_result` in the canonical four-line format, exactly as `/integrate` Step 2 does. A FAIL here is a real failure: do NOT record the phase, write `harness_state` `{state: "yielded", slug, reason: "post-archive verify FAIL"}` (marker delete first), and surface the output.

   The guard only ever skips on a positive match. Everything else re-verifies, because a verdict that does not cover the tree being committed is worth nothing.

6. Append `"archive"` to `workflow.json → completed`.
7. Tell the user: "Archived to `docs/archive/<date>/<slug>/`. Ready for `/grant-commit` → `/commit`." Include any non-empty `drift` or `unclaimed` from Step 3 and the Step 5.5 report — an unread gap report is the same as no gap report. A `specMissing: true` from Step 3 is reported too, and it invalidates the other arrays rather than joining them. Say which way Step 5.7 went — re-verified and green, or skipped and why — so a reader can tell a verdict that covers this tree from one that predates it.

## Constraints

- **Never archive a workflow in-flight.** If the user runs `/archive` before the workflow is done (integrate/document not complete), refuse and tell them which phase is missing.
- **Never delete artifacts.** Move-only. If a target file already exists in the bundle (re-run), refuse and tell the user to pick a new archive date or remove the conflict.
- **Idempotent on partial failure**: if the script moves 3 of 5 files and then fails, re-running continues from where it stopped (the moved files are gone from source, the un-moved are still at source).
