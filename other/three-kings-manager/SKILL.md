---
name: three-kings-manager
description: Fully autonomous Three Kings program runner — every 3 days it gate-checks a per-URL ladder ledger, executes EDIT_NOW rungs end-to-end (draft via seo-content-3-kings-technique, apply via blog-edit API mechanics, backup gate, record), auto-judges each closed 14-day window as WIN/FLAT/LOSS, and executes rollbacks on REGRESSION. Not a reporting skill — invoked means acted. Use when asked to run the program, check what to edit, record an edit, or roll back a flagged regression.
---

# Three Kings Manager

Autonomous owner of ladder discipline for MIU content edits. On invocation it runs the full loop — fetch, gate-check, edit eligible pages, record, monitor — and only reports the compact outcome at the end. The check output is a control plane for deciding actions, not a deliverable. It never asks permission mid-loop; the safety gates (`yarn db:backup` before any production blog write) are the permission.

## Operating loop

**Every 3 days (read-only):**

1. Refresh the correlator export (final GSC data, 3-day holdback):
   ```bash
   node ./.claude/skills/gsc-causation-correlation/scripts/gsc-daily-correlate.cjs --output=/tmp/gsc-daily.json
   ```
2. Run the check:
   ```bash
   node ./.claude/skills/three-kings-manager/scripts/tkm.cjs check \
     --gsc=/tmp/gsc-daily.json --ledger=docs/SEO/maintenance/three-kings-ledger.json
   ```
3. Act on the verdicts:

| Verdict    | Meaning                                               | Action                                                                                         |
| ---------- | ----------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| REGRESSION | latest judged edit lost clicks or degraded position   | Rollback recommended — see below                                                               |
| EDIT_NOW   | window closed, gates pass                             | Execute the next rung, then `record-edit`                                                      |
| VERDICT    | all 3 rungs complete                                  | Judge with `gsc-causation-correlation` pre/post windows; restart ladder only with new evidence |
| HOLD       | 14-day window still open                              | Nothing. This is the system working                                                            |
| GATED      | demand change / phantom cluster / junk-position bloat | No edit; inspect SERP or reclassify                                                            |
| STOP       | stop rule fired                                       | No edits; quarantine or consolidation evaluation only                                          |

**Executing a rung (only on EDIT_NOW) — do this immediately, do not stop to report:**

`EDIT_NOW` also requires a real CTR/snippet gap inside the composed Three Kings striking-distance band (position 5–15). The checker gates pages outside that band and pages already meeting the composed `serp-ctr-snippet-rewrite-technique` rank-band CTR threshold; a closed window alone is not permission to rewrite a healthy snippet or a page whose real problem is ranking/intent.

1. Rung 1 = `seo_title`, rung 2 = `seo_description`, rung 3 = proof-led body pass (direct answer + evidence module above the fold).
2. Draft the replacement copy with `seo-content-3-kings-technique` (its Three Kings audit + competitive-gap rules define what good copy looks like).
3. Execute the edit with the `blog-edit` skill (`.agents/skills/blog-edit/SKILL.md`) — it owns the production mechanics: `PATCH /api/blog/posts/[slug]` with `x-api-key: BLOG_API_KEY` from `.env.api`, GET readback, and the live-HTML spot check. Blog DB writes are effective immediately; repo/backlog changes ride the next deploy.
4. Production blog writes require the `yarn db:backup` gate first (project rule).
5. After the edit lands live: `node tkm.cjs record-edit --ledger=docs/SEO/maintenance/three-kings-ledger.json --url=<url> --rung=<n> --note="<what changed>" --previous="<prior field value>"`. This re-opens the 14-day window; `previous` captures the old value so a REGRESSION rollback is executable without archaeology. The ladder enforces one rung at a time.
6. Append the blog changelog entry (`blog-edit` after-finishing rule) and record the edit in `docs/SEO/maintenance/seo-changes-backlog.md`; update the GSC request-indexing backlog row and request indexing manually (the 3-kings skill's indexing loop rule).

**Monitoring (automatic in every `check`):** each history row is judged once its window closes — WIN (clicks/d ≥ 1.2x prior), FLAT, or LOSS (clicks/d ≤ 0.8x prior, or position degraded >2 without click gain). Outcomes persist in the ledger.

**Rollback (executed autonomously, gated):** a LOSS on the most recent edit shows as REGRESSION. First rule out demand-side losses: if the outcome row shows `impDelta` sharply negative (≤ -40%) while `posDelta` stayed within ±1, the click loss tracks a demand/SERP shift, not the edit — record the outcome, skip the revert, and treat the row like a demand-change gate. Otherwise revert immediately, with a fresh `yarn db:backup` first: restore the prior field value from the history row's `previousValue` (fallback: dated backups in `backups/`) via the blog API PATCH, verify with GET readback, then `node tkm.cjs record-revert --url=<url> --note="<restored field>"`. A revert opens a fresh 14-day cooling-off window. If the field lacks a `previousValue` and no backup covers it, stop and surface the gap instead of guessing the old copy.

## Ladder discipline

- One rung per page per 14-day window. `record-edit` refuses same-page edits inside an open window and refuses skipping rungs.
- After two judged zero-click rungs, set a `stopRule` in the ledger (manual, evidence-backed) — do not keep re-rolling the same field.
- `record-revert` never advances the rung.

## Recorded MIU evidence

The gates and thresholds encode the 2026-09-03 causation study (see `gsc-causation-correlation` SKILL.md): Three Kings on pages ranking pos 5-11 compounded best-free-upscaler 5→493 clicks/wk; snippet edits on phantom clusters, demand-shift rows, and junk-position rows never earned clicks. The ledger was seeded 2026-09-03 from the backlog's real edit history, so the first `check` judges those edits retroactively.

## Coordination

- Data: `gsc-causation-correlation` (daily series export consumed by `check`), `gsc-analysis` (standard 28d fetch for opportunity discovery).
- Editing: `seo-content-3-kings-technique` (drafting), `blog-edit` (execution), `blog-performance-monitor` (single-URL incidents).
- Reclassification: `cannibalization-consolidation-technique` (STOP rows, cannibalization), quarantine rules in `serp-ctr-snippet-rewrite-technique`.
