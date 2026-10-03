---
name: marathon-cleanup
description: >
  Audit active PDDA marathon plans and bundles, reconcile every lane against canonical project docs,
  frontmatter and status tables, GitHub issue and PR state, landed commits, tests, and CHANGELOG
  evidence, then archive only verified-complete task docs and fully complete marathons. Use when asked
  to clean up, reconcile, retire, archive, or sweep completed marathon files under PROJECT/2-WORKING,
  especially after marathon lanes merge. Defaults to report-only and requires explicit confirmation
  before moving files or changing lifecycle records.
---

# Marathon cleanup

Reconcile marathon execution artifacts with PDDA lifecycle state. A move is the final bookkeeping
step, never the evidence that work completed.

## Guardrails

- Read `ROUTER.md`, `AGENTS.md`, `GUIDING-PRINCIPLES.md`, the RELEASES DB (`releases roadmap list`), `PROJECT/PDDA.md`, and the
  candidate marathon in full before classifying it.
- Default to audit-only. Do not edit, move, close issues, create commits, or change ROADMAP or
  CHANGELOG until the operator confirms the exact proposed move set.
- Never classify from a closed issue, checked box, frontmatter word, commit message, or changelog
  entry alone. Require converging durable evidence and no contradiction.
- Preserve unrelated dirty-worktree changes. Stop if a candidate or lifecycle ledger has overlapping
  edits that cannot be safely merged.
- Use `git mv` for approved repo moves. Never delete marathon files or rewrite history.
- Treat unavailable GitHub state as `UNKNOWN`, not complete.

## 1. Inventory marathon candidates

Inspect only active execution artifacts under `PROJECT/2-WORKING`:

```bash
find PROJECT/2-WORKING -maxdepth 1 \
  \( -type f -o -type d \) \
  \( -name 'MARATHON-*.md' -o -name 'MARATHON-*' \) \
  -print | LC_ALL=C sort
```

Include hand-authored and generated marathon plans plus execution bundle directories. Classify
generated HQ rollups, triage reports, examples, snapshots, and docs that merely mention marathons as
`NOT-EXECUTION-DOC`; do not archive them through this workflow.

For each candidate, extract lane IDs from frontmatter (`lanes`), wave/lane tables, issue links,
phase briefs, and bundle YAML. Resolve each lane to its canonical `GH-<n>-*.md` document when one
exists. Report duplicate or contradictory mappings rather than choosing silently.

## 2. Build an evidence record per lane

Collect these signals without changing state:

| Signal | What to verify | Weight |
|---|---|---|
| Canonical PDDA doc | Location, terminal frontmatter, exact Status table, acceptance/QA state, explicit remaining work | Primary scope record |
| Marathon plan or brief | Bounded lane scope, terminal lane result, reviewer verdict, branch/PR/commit references | Scope and execution record |
| GitHub issue | Open/closed state, close reason, linked PRs, comments that narrow or preserve remaining scope | Corroboration; closed alone is insufficient |
| Delivery | Merged PR or commit is reachable from the intended target branch; changed paths match the lane | Required for implementation lanes |
| Verification | Recorded tests/gates passed for the shipped scope; no unresolved failed gate | Required |
| CHANGELOG | Dated entry names the issue/scope and delivery outcome | Provenance corroboration |

Useful read-only probes:

```bash
gh issue view <n> --json number,title,state,stateReason,closedAt,url,comments
gh pr list --state all --search '<n>' --json number,title,state,mergedAt,mergeCommit,url
git log --all --decorate --oneline --grep='GH-<n>\|#<n>'
git merge-base --is-ancestor <commit> development
rg -n "GH-<n>|#<n>" CHANGELOG.md PROJECT
```

Use the actual target branch from repo policy or the marathon contract in place of `development`
when they differ. Verify a referenced commit exists before running `merge-base`.

## 3. Classify every lane

Assign exactly one result:

| Result | Rule | Parent marathon eligible? |
|---|---|---|
| `VERIFIED-COMPLETE` | Entire canonical task scope is terminal, delivered, verified, and consistent | Yes; task doc may move |
| `VERIFIED-MARATHON-SLICE` | This marathon's explicitly bounded slice is delivered and verified, while separately stated issue scope remains | Yes; task doc stays active |
| `OPEN` | Acceptance work remains or issue/doc says active | No |
| `BLOCKED` | Work is parked, failed, awaiting review, unmerged, or gate-failed | No |
| `AMBIGUOUS` | Evidence is missing or too weak | No |
| `CONFLICT` | Durable sources disagree about completion, target, or scope | No |

`VERIFIED-COMPLETE` requires all of the following:

1. The canonical doc explicitly records the completed outcome and has no in-scope next action.
2. Implementation is merged/reachable on the intended target branch, or a docs/research lane records
   its required durable artifact.
3. The lane's acceptance criteria and relevant gates have positive verification evidence.
4. GitHub state and CHANGELOG do not contradict the local outcome. An open issue requires an explicit
   reason; otherwise classify `CONFLICT`.

Use `VERIFIED-MARATHON-SLICE` only when the plan defined the slice before or during execution and the
canonical doc clearly separates remaining issue work. Do not retroactively narrow scope to make a
marathon look complete.

## 4. Decide task-doc and marathon moves separately

A canonical `GH-*.md` task doc may move from `2-WORKING` to `3-COMPLETED` only when its result is
`VERIFIED-COMPLETE`. Before proposing the move, require a PDDA terminal lead word such as `Complete`,
`Shipped`, `Fixed`, `Closed`, `Merged`, `Resolved`, or `Landed`, and reconcile its Status table.

The parent marathon may move only when:

- every lane is `VERIFIED-COMPLETE` or `VERIFIED-MARATHON-SLICE`;
- no wave, lane, review, merge, gate, or operator action remains;
- the marathon's own status can truthfully become terminal;
- all sibling bundle files describe the same terminal outcome;
- the destination does not already exist; and
- relative links will remain valid or are included in the proposed edit set.

An open issue does not block a completed marathon slice by itself. It does block moving that issue's
canonical task doc unless the entire issue is complete and the open state is being explicitly
reconciled.

## 5. Report before mutation

Return one table per marathon with lane result, canonical doc, GitHub state, delivery proof,
verification proof, CHANGELOG proof, contradictions, and proposed action. End with one exact move
set, for example:

```text
git mv PROJECT/2-WORKING/GH-123-EXAMPLE.md PROJECT/3-COMPLETED/
git mv PROJECT/2-WORKING/MARATHON-PLAN-YYYY-MM-DD.md PROJECT/3-COMPLETED/
```

Also list required content edits and ledger updates. Ask for explicit confirmation of that set. If
any lane is not eligible, leave the marathon in place and state the smallest evidence or work needed.

## 6. Apply a confirmed cleanup

After confirmation, execute in this order:

1. Re-check `git status`, GitHub state, target-branch reachability, and destination absence.
2. Update eligible task docs to terminal frontmatter and an evidence-backed Status row; preserve
   issue links and outcome detail.
3. Update the marathon plan and every file in its bundle to the verified terminal outcome. Do not
   leave `not yet fired`, `ready`, or an outstanding next action inside `3-COMPLETED`.
4. Use `git mv` for eligible task docs, then the fully complete marathon file or directory.
5. Update ROADMAP pointers and state in place. Keep it a pointer ledger; do not copy execution detail.
6. Add a concise dated CHANGELOG entry naming the verified outcome and moved artifacts.
7. Run `utils/pdda/pdda.sh run`. Run relevant link or repo validation when links or code changed.
8. Report moves, evidence, validation output, and anything deliberately left active.

If validation fails, do not claim completion. Repair only changes in the confirmed cleanup scope; if
the failure is unrelated, report it precisely without altering unrelated user work.

