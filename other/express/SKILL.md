---
name: express
description: >
  Hotfix fast lane (GH-267/GH-516) for an explicit `/express`, "express this hotfix",
  or "express GH-N" request. Carries a critical, risk-bounded fix, registered
  regression suite, releases-ledger updates, born-complete PDDA doc, CHANGELOG,
  landing, and reconciliation in one operator-authorized motion. Requires a
  task clone branched from origin/development (carrying <= 2 local commits) with the
  canonical pre-push gate installed, authenticated gh, and the root releases ledger. The
  driver commits and fast-forward pushes directly to development, verifies the
  commit and issue closure, then reconciles with `wave_reconcile --commit`.
  Supports --dry-run across commands, contextual subsystem tolerance (--allow-multi-subsystem
  or <= 30 insertions across <= 2 files), an explicit `resume` subcommand to recover
  interrupted runs, and central telemetry mirroring (~/.config/xyz/events/).
  Refuses shared/stale clones, diverged branches, > 2 commits, unsafe Git/Bash/kernel surfaces,
  oversized diffs, generated-artifact hand edits, missing/red suites, and closed or unresolved
  issues. Do not use for Costly or one-way-door changes.
---

# /express — hotfix fast lane through the whole paper trail

One verb, one motion: the fix, its regression suite, the ledger writes, the
born-complete capture doc, the CHANGELOG entry, the landing, and the
reconciliation — all before the operator's coffee cools. The guardrails are the
skill; the speed is a side effect.

---

## Recite this — verbatim, as the first thing in your first response

> **Express Discipline:**
> 1. **Verify clone & pre-flight bounds (Phases 0–2).** Require a task clone off `origin/development` ($\le 2$ local commits, canonical pre-push gate installed via `githooks/install.sh --check`); enforce strict subsystem bounds ($\le 4$ files / $\le 150$ insertions) and hard refusals on kernel, coordination, or shared Bash surfaces.
> 2. **Validate issue & registered regression suite (Phases 3–4).** Confirm the tracking issue is OPEN; verify that a dedicated regression suite exists (`test/gh<N>-<slug>.sh`) and is registered in `validate.sh TESTS` (hotfix without a registered suite is refused).
> 3. **Generate born-complete docs & append changelog (Phase 5).** Scaffold capture doc in `PROJECT/2-WORKING/` with Status, Acceptance, Merge evidence, and Lessons Learned present from birth; append the entry to `CHANGELOG.md` in the same motion.
> 4. **Execute qualified gate & dial-in releases ledger (Phases 6–7).** Register roadmap issue in `releases.db` and dial into active release (`releases next`); execute regression suite green, prove tree identity, and re-snapshot tree to prevent drift.
> 5. **Direct fast-forward landing & 3-push reconciliation (Phases 8–11).** Commit qualified paths (`Closes #N`), direct push fast-forward to `origin/development` (`XYZ_SKIP_PREPUSH=1`), verify remote issue closure, ship release evidence, and execute clean-tree `wave_reconcile --commit`.
>
> **Overall Goal:** Critical, risk-bounded hotfix implemented, tested, ledger-tracked, landed directly to development, and reconciled with a complete paper trail in one single, unpaused motion with zero bypassed safety invariants.

Then begin work.

---

**Design provenance:** proposed on #259 (comment 5434441831, v2), filed as
#267, upgraded in #516 (True Direct-Push Mode, commit-driven reconciliation,
branch flexibility, recovery subcommand, dry-run, and central telemetry):
re-use the releases verbs, `wave_reconcile`, the pre-push gate, and `.tick`
events rather than building parallel machinery. Where jog pauses at each
landing boundary by default (orchestrator outer review), express inlines those
same predicates — base branch, diff size, gate receipts — as pre-flight
refusals, because a pause would defeat the reason /express exists. That is the
foundational difference, and it is the only one.

## Procedure

Run the driver; it enforces the order. Do not hand-perform steps the driver owns.

```bash
# 0. From the task clone carrying the fix (SOP §4 clone, <= 2 commits ahead, hooks installed):
python3 utils/py/express.py check --issue <N> --suite test/gh<N>-<slug>.sh   # steps 0–4
python3 utils/py/express.py docs  --issue <N> --suite test/gh<N>-<slug>.sh --summary "<one line>"  # step 5
python3 utils/py/express.py ledger --issue <N>                               # step 6
python3 utils/py/express.py land  --issue <N> --suite test/gh<N>-<slug>.sh   # steps 7–11
# or the whole motion at once:
python3 utils/py/express.py run --issue <N> --suite test/gh<N>-<slug>.sh --summary "<one line>"

# Inspect what would happen without modifying disk, DB, or git state:
python3 utils/py/express.py run --issue <N> --suite test/gh<N>-<slug>.sh --summary "<one line>" --dry-run

# Recover/resume an interrupted express run (e.g. dropped network or post-push closeout fault).
# --suite names the registered suite the landing ran: resume validates the COMMITTED receipt
# (read from HEAD, never the working tree) against it and never runs a suite or writes evidence
# (GH-592). With no committed valid receipt it refuses BEFORE closing the issue or shipping and
# prints the recovery recipe below.
python3 utils/py/express.py resume --issue <N> --suite test/gh<N>-<slug>.sh [--sha <SHA>]

# Recovery recipe when resume refuses. Run in a FRESH disposable full clone. Every inspection fails
# closed: `set -euo pipefail` is active (not a comment), cleanliness is asserted with git's own exit
# codes (never by an empty-stdout test), and snap() aborts on the first failing command.
set -euo pipefail
SHA=<SHA>; N=<N>; SUITE=test/gh<N>-<slug>.sh
git checkout "$SHA"
git diff-index --quiet HEAD -- && [ "$(git ls-files --others --exclude-standard | wc -c)" -eq 0 ]   # 1. clean baseline
LOG=$(mktemp -t express-recovery)                                                                 # 2. log OUTSIDE the tree
snap(){ git rev-parse HEAD && git status --porcelain && git remote -v && git config --list --local | shasum -a 256; }
BEFORE=$(snap) || { echo "identity inspection failed"; exit 1; }; printf '%s\n' "$BEFORE" >"$LOG"
set +e; bash "$SUITE" >>"$LOG" 2>&1; RC=$?; set -e; echo "rc=$RC" >>"$LOG"                     # 3. record rc at once
AFTER=$(snap) || { echo "identity inspection failed"; exit 1; }; printf '%s\n' "$AFTER" >>"$LOG"
[ "$BEFORE" = "$AFTER" ] || { echo "VOID: identity drifted during the suite — no receipt"; exit 1; }  # 4.
git checkout development && git diff-index --quiet HEAD --                                       # 5. same helper, actual rc
python3 -c "import sys; sys.path.insert(0,'utils/py'); import express; print(express.write_receipt('.', '$SHA', $N, '$SUITE', $RC))"
cp "$LOG" TESTS-RESULTS/*+GH-"$N"-express/recovery-run.log                                       # 6. retain the run
git add TESTS-RESULTS && git commit -m "chore(express): recovery receipt GH-$N (commit $SHA)" && git push origin development
python3 utils/py/express.py resume --issue "$N" --suite "$SUITE" --sha "$SHA"                    # 7.
```

Before landing, `cmd_land` qualifies the change, resolves the exact owned full issue
URL, and invokes `roadmap update --gid OWNED_ROW --accepted-start` (schema009 must
already be deliberately installed). It then requalifies against the existing
driver-projection allowlist before snapshots/testing. Dry-run previews only;
registration via `ledger` is not admission. Interrupted/repeated land preserves
one effective start; receipt-based `resume` never starts work after landing.


What each phase asserts (all refusals and fired runs write `.tick/express/*` — a sibling of tick's coordination log, never inside it (GH-694) — and mirror to `~/.config/xyz/events/`):

0. **Tree of execution** — task branch based on origin/development with $\le 2$
   local commits (GH-516; $> 2$ refuses with `too-many-commits`; diverged branches
   refuse with `task-clone`), no scratch paths, and `bash githooks/install.sh --check`
   proves the canonical pre-push stub (`gate-unwired`; hooks do not travel, GH-549).
   Express never commits over peer work (GH-527). Hand-edits to ledger files or
   generated views are refused; only the driver's verbs may write them.
1. **Bounds** — ≤ 4 core files / ≤ 150 insertions, single subsystem (unless
   `--allow-multi-subsystem` is passed, or micro-diff tolerance applies: $\le 30$
   insertions across $\le 2$ files auto-passes, GH-516). Only the lane's OWN
   paperwork (`CHANGELOG.md` and the current issue's capture doc resolved by
   `capture_doc_path(root, issue)`) is exempt. Every other `PROJECT/**` path and
   operator .md edit (README, governance, skills) COUNTS (a gateless merge never
   rewrites policy unbounded).
   Defaults are operator-tunable via `--max-files` / `--max-insertions`; the
   refusals are never optional.
2. **Hard refusals** — frozen twins and shared Bash runtime (GH-308), any
   new/edited `.sh` under `utils/` or `relay-automation/` (GH-551),
   coordination-kernel and containment surfaces (AGENTS: at least Costly).
3. **Issue first** — the tracking issue exists and is OPEN. Closed => the work
   may already be landed; run the preflight probes instead of re-doing it.
4. **Suite** — the fix's regression suite exists AND is registered in
   `validate.sh` TESTS. A hotfix without its suite is a claim, not a fix.
5. **Docs born complete** — capture doc scaffolded in `2-WORKING` with Status,
   Acceptance, Merge evidence, and `## Lessons Learned (For Future Agents)`
   present from birth (highly recommended — since GH-693 the reconciler warns
   rather than refuses promotion when it is missing; fill it in anyway),
   plus the CHANGELOG entry appended in the same motion.
6. **Ledger** — `roadmap add` if the issue is unparked, then `manifest dial-in`
   against the active release (`releases next`) with an express reason. The
   adopted release/leaderboard projections and `ROADMAP-DASHBOARD.md` refresh
   in the same phase and are the only accepted driver outputs.
7. **Gate** — the fix's suite runs green, the tree is RE-SNAPSHOTTED afterwards
   by path and content (`tree-drift`: new paths and changed qualified bytes both
   refuse). Gate identity is re-proven after the suite, staging uses explicit
   pathspecs, and the direct push passes `XYZ_SKIP_PREPUSH=1`. That bypasses the
   FULL pre-push gate (`validate.sh`) by lane design (GH-267/GH-516) — it is not a
   duplicate of Step 7, which ran only the fix's registered suite. The receipt
   written in Step 9 says exactly that (`gate: express-suite`).
8. **Land** — one commit of exactly the qualified paths with `Closes #N`, then
   `git push origin HEAD:development`. A concurrent update refuses as a normal
   non-fast-forward; there is no force push and no PR. The closeout switches to clean,
   current `development` (ship/reconcile state never rides the task branch).
9. **Receipt, then ship with evidence** (GH-592) — from clean, current
   `development`, the driver writes `TESTS-RESULTS/<date>+GH-<N>-express/provenance.jsonl`
   (`commit` = the landing sha, `command` = the suite, the real `rc`,
   `gate: express-suite`) and then `manifest ship --gid <rel> --evidence "<sha>;
   registered suite <suite> green (express-suite, not the full gate); receipt <path>;
   direct development push"`. Ship precedes the issue close below, so the
   GH-205 shape (an issue closed while its manifest item is still dialed_in)
   can only arise if the ship persist itself fails — which exits non-zero with
   an `express-reconcile-failed` receipt and is what `resume` recovers.
10. **Close the issue** — the commit message says `Closes #<N>` and lands on the
    default branch; the driver verifies and closes explicitly if GitHub has not.
11. **Persist, reconcile cleanly, persist — fail closed.** The landing is
    three pushes total: (1) the hotfix land push (step 8), then from
    `development`, (2) the ship outputs are committed and pushed, and only
    then (3) `wave_reconcile.py --commit <sha> --gate` runs from the clean tree —
    `--gate` proves the receipt from step 9 is attributable to this landing (it
    proves attribution, not test success) and its stdout is printed; its
    outputs form the third commit and push. The ship commit (2) carries exactly
    the receipt file and nothing else under `TESTS-RESULTS/`. Every post-push fault exits
    non-zero with an `express-reconcile-failed` receipt; success prints only
    after every boundary.

## After the run

- Confirm the tail: `releases check` clean, `pdda.sh issue-doc-sync` 0 errors,
  capture doc promoted (or, under an OPEN umbrella, correctly left in
  `2-WORKING` with merge evidence — that is success, not failure).
- `standup` reports the weekly express count; a rising counter means the normal
  lane is too slow — fix the lane, don't normalize express.

## Non-goals

- No override flag: a refused run routes to the normal fresh-clone PR lane,
  full stop. An `--force` would make every guardrail negotiable.
- No Costly/one-way-door work, ever (see step 2 refusals).
- No force push (direct landing pushes fast-forward with Step 7 qualifying suite receipt and `XYZ_SKIP_PREPUSH=1`).
