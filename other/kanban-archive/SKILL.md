---
name: kanban-archive
description: 'Close a PASS-reviewed feature or bug with kf archive. Features require a completion report and canonical docs; bugs update related docs only when needed. Use at review with current PASS reports or when completing closure in dones.'
---

# Kanban Phase 6 — Artifact (Autonomous)

Argument: `<feature_name>`.

Close the work item with traceable results and the appropriate documentation.

**Archive is the delivery gate, not just lifecycle bookkeeping.** `kf archive` is the post-delivery step: it refuses while a recorded `pr` is not verifiably merged (exit 1, no side effects, no `--force` escape), and a review-PASS item legitimately waits in `review` until its change lands — visible as "awaiting merge" in `kf status`/`kf doctor`. With no `pr` recorded, running archive *is* the human's delivery confirmation. Only then does it move to `dones`, sync canonical docs, close the issue, move the board and stamp `delivered` — all idempotent, so a re-run reconciles.

---

## 1. Prepare closure artifacts

```bash
kf status --change {feature_name}
kf status --change {feature_name} --json
```

Require current PASS testing and review reports. Read `kind` before choosing closure work:

- Feature: use `kf instruct feature-report --change {feature_name}` and write `phase-6-feature-report.md` in the review folder. Include actual changes, test/review evidence, documentation manifest, limitations and accepted follow-ups.
- Bug: no feature report or feature planning artifacts are required. Read the bug report and review result; confirm the verified fix, regression evidence and docs impact.

If already in dones, complete only missing closure work and validate; never reimplement.

## 2. Sync docs

For a feature, let `kf archive` copy requirement, UC index/files/diagram and test plan/current result into canonical docs. The requirement mirror under `docs/requirement/` was already written in Phase 1 — `kf archive` rewrites it from the Phase 1 artifact. Every canonical copy except the test result is stamped `status: archived`, and the UC index rows flip from `planned` to `implemented`. Do not manually copy the UC index/files, diagram or test plan before archive, and do not change approved source artifacts during closure.

### 2b. Reconcile superseded docs (feature, mandatory)

`docs/` must describe the system as it is after this feature, not as each older feature left it. Before `kf archive`, read [reconcile.md](reconcile.md) and follow it: find earlier canonical docs and `docs/workflow/*` that describe behavior this feature changes, mark contradicted snapshots with a `Superseded by` banner, bring workflow docs up to date, and record the result in the feature report's `## Docs Reconciled` section (`None — <reason>` when nothing is affected). Never rewrite another feature's snapshot body.

For a bug, update existing related feature docs only when the fix changes documented behavior or reveals inaccurate documentation. Use the feature/context named in the bug report; do not overwrite feature docs with bug-report content. Record bug ID, fix summary and regression reference in the project's changelog or change-history section (e.g. CHANGELOG.md) when one exists. If behavior is already documented correctly, leave docs as-is and record “No documentation update required” with the reason in the review report. Bug archive does not automatically create canonical feature docs.

## 3. Archive and validate

```bash
kf archive {feature_name}
kf validate --change {feature_name}
```

`kf archive` requires current PASS reports, verifies a recorded PR is merged (or takes the human's run as confirmation), runs the dones hook — which closes the issue and moves the board to `statusMap.dones` — moves review → dones, syncs canonical docs for a feature and stamps `delivered`/`deliveredAt` last. Bugs skip canonical docs. `kf stage ... dones` uses the same archive path, so the merge gate applies there too. If it refuses on an unmerged PR, the item is not done — merge the PR first. Validate after archive and check reported canonical destinations for a feature. Do not report completion if validation fails.

When refreshing an item already in dones, canonical docs may include later bug fixes. If the CLI reports changed canonical docs, preserve them with `--skip-specs`; do not use `--force` to restore an older snapshot without explicit user direction — a forced overwrite is recorded as a bypass.

## 4. Git handoff

```bash
git status
```

Archive runs after the feature's change has merged, so its output is a docs-only change on top of the default branch. Commit when the user requested it or project instructions explicitly require it, on its own branch and PR:

- Feature: `docs({context}): sync canonical docs for {feature_name}` — the canonical copies plus the docs reconciled in step 2b.
- Bug: `docs({context}): ...` for related docs updated in step 2, when any.

Include only this work item's changes, respect ignored .works directories and preserve unrelated working-tree changes. Otherwise report that changes are uncommitted.

---

## Done

Pipeline complete. Deliver the final report:

```text
## Pipeline Complete: {context}/{feature_name}
1. ✓ Confirm — requirement or bug triage
2. ✓ Plan — approved feature contract or lightweight bug contract
3. ✓ Implement — {M}/{M} tasks
4. ✓ Test — {N}/{N} passed
5. ✓ Review — PASS
6. ✓ Archive — kf archive, docs sync/update status, docs reconciled: {list or None}

Artifacts: .works/dones/{feature_name}_{timestamp}/
Feature canonical docs:
- docs/requirement/{context}/{feature_name}.md
- docs/use-cases/{context}/{feature_name}/README.md
- docs/use-cases/{context}/{feature_name}/UC-###(-<slug>).md (one file per use case)
- docs/use-cases/{context}/{feature_name}/diagram.md
- docs/testplan/{context}/{feature_name}.md
- docs/testplan/{context}/{feature_name}-result.md
```

For bugs, list only related docs actually updated, or state why none were needed. Report the commit SHA only if a commit was made.
