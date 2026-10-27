---
name: sweep-connect
description: >
  Find orphaned Connect programs, opportunities, payment units, and invites; deactivate or delete
  the safe ones. Needs a live-set from sweep-live-set.
disable-model-invocation: false
---

# sweep-connect

Find Connect artifacts (programs, opportunities, payment units, FLW invites) that no current opp references, score them, and present them for triage. Connect's upstream API is uneven: opportunity deactivate is available, unaccepted FLW invite delete is available, but programs and payment units have no upstream delete path. This skill deactivates opportunities and deletes unaccepted invites **in its execute pass, after the orchestrator's per-system human-confirmation gate** (see `agents/sweep.md § Human-confirmation gate`); programs and PUs surface in a "upstream-gap — delete via Connect admin UI" section.

## Inputs

- Live-set file path from `sweep-live-set` skill output.
- `ACE_CONNECT_BASE_URL` from `.env` (e.g. `https://connect.dimagi.com`).
- `mode` — `recommend` (default) | `execute`. In `recommend` the skill is **report-only**: diff/score/render + return the recommended-action list; **no mutations**. In `execute` it mutates only `approvedIds`. The human-confirmation gate between the two is the orchestrator's job — see `agents/sweep.md § Human-confirmation gate`.
- `approvedIds` (`execute` mode only) — the exact ids the human approved in chat. Mutate nothing outside this set.

## Products

- `ACE/_sweep/<timestamp>/connect-orphans.md` — human-readable triage report.
- `ACE/_sweep/<timestamp>/connect-orphans.yaml` — machine-readable `OrphanReport`.
- For approved orphan opportunities: `connect_update_opportunity({active: false})` calls.

## Process

1. **Read the live-set** via `drive_read_file`. Parse YAML.
2. **List Connect inventory** using existing atoms, in BOTH configured
   orgs — the PM org (`connect_orgs.pm_org`) AND, when one is configured, the NM/holding
   org (`connect_orgs.nm_org`; null in self-managed mode), from `bash bin/ace-doctor --preflight --no-live`
   → `connect_orgs:`. Union the rows by opportunity `id`. A PM org's listing
   includes every opportunity on its programs, including those HELD by the
   NM org (Phase 4's PM→NM shape, where the PM table's
   `holding_organization_name` names the holder); the NM org's listing adds
   anything it holds on a program outside the PM org, which the PM listing
   cannot see. Both list layouts parse since ace#2506 (before it, the NM
   org's URL returned 0 rows). An NM-held opportunity is still acted on at
   the PM org's URL (`playbook/integrations/connect-api.md § PM→NM org-URL
   matrix`); pass the org it was LISTED at as `organization_slug` to the
   per-opportunity reads in step 4b. ACE programs
   also live in any org a previous configuration used; to sweep one, pass
   that org's slug explicitly (the operator names it — read it off the
   live-set opps' `connect.program.url`, never from memory):
   - `connect_list_programs`
   - `connect_list_opportunities` (per program)
   - `connect_list_invites` (per program — for unaccepted-invite cleanup tied to orphan opportunities)
   - Payment units are NOT listed standalone — they are implicit children of opportunities. When an opp is deactivated (or eventually hard-deleted), its PUs follow.
3. **Diff** each item's id against the corresponding live-set bucket:
   - programs → `liveSet.identifiers.connectProgramIds`
   - opportunities → `liveSet.identifiers.connectOpportunityIds`
   - invites (for orphan opportunities only) → no diff needed; every invite under an orphan opp is itself orphaned
4. **Score** each orphan via `scoreConnectItem(item, liveSet)` from `lib/sweep-fingerprint.ts`.
4b. **Opportunity health + demo-user invite hygiene (ace#953 / ace#938).** For each candidate opportunity, `connect_get_opportunity` and record `end_date` and `dashboard_read` (as `dashboardRead`) onto the `ConnectItemInfo` you pass to the scorer, then `connect_list_flw_invites({ organization_slug, opportunity_id, phone: '${ACE_E2E_PHONE}' })` and record whether the demo user holds access and in what state.

   - **`end_date === ''` is a DEFECT, not an orphan signal.** An opportunity with no end date **bricks the mobile app for every worker invited to it** — that is ace#938, where one poisoned opp was found the hard way and a hand sweep of the same org turned up **ten more** loaded landmines. `scoreConnectItem` now flags it `high` with a `MALFORMED:` signal. Note `undefined` (not read) is deliberately NOT malformed: the repair writes a date, so scoring an unread field as malformed would mutate healthy opportunities.
   - **`dashboard_read === 'setup_incomplete'` is NOT SWEEPABLE (ace#2083).** Connect never finished the opportunity's setup (no payment unit — `is_setup_complete`), so it is already inactive, every read 302s to the payment-unit wizard, and it still counts one `EXPECTED_OPP_BUDGET` in every program-ceiling sum on the org. `connect_update_opportunity({active: false})` removes nothing, Connect has no opportunity-delete API (requested as dimagi/commcare-connect#1611), and Connect's own `delete_stale_opportunities` task purges visit-free opportunities once they are six months old — which this cohort is by construction. `scoreConnectItem` flags it with `SETUP_INCOMPLETE_DISPOSITION` (`lib/sweep-fingerprint.ts`). Report it; never deactivate it and never count it as swept. The source of new ones is closed by `connect-opp-setup` Step 4.0.
   - **The demo-user rows are report-only, and split by state.** `match.status === 'accepted'` has **no ACE-side delete path at all** — Connect's delete view excludes accepted invites server-side, and `delete_opportunity()` exists only as a Celery task with no view, no REST, no atom. The escape is rotating `${ACE_E2E_PHONE}`. `match.claimed === false` (pending) is deletable **once ace#1159 lands** — that atom currently cannot be called because no atom returns the invite row id.

   **Cost note:** `connect_get_opportunity` is 2 HTTP GETs per opportunity, and `connect_list_opportunities` cannot substitute (the list page renders no date). `ai-demo-space` held 114 opportunities at ace#938 time, so an org-wide deep pass is ~340 requests. Scope it to live-set-diffed orphans plus a periodic full audit, or accept the cost — the hand sweep that found the ten landmines did the full pass successfully.

5. **Build the `OrphanReport`** with `system: 'connect'`. Partition the report into **five** sections:
   - **Actionable — repair:** malformed opportunities (empty `end_date`). This is a *repair*, not a deletion, and it is the highest-value output of this sweep.
   - **Actionable — deactivate/delete:** orphan opportunities (soft-deactivate) and unaccepted FLW invites (auto-delete). Never a `setup_incomplete` opportunity.
   - **Report-only — setup_incomplete (Connect auto-purges at 6 months, no delete API):** one row per `setup_incomplete` orphan with its id, name and `date_created` when known, and the line `Connect auto-purges visit-free opportunities at 6 months (delete_stale_opportunities); no delete API — ace#2083`. Give the count in the summary as its own number, never folded into the swept/deactivated total.
   - **Report-only — demo-user access:** one row per opportunity where `${ACE_E2E_PHONE}` holds access, annotated with its reason: `accepted → no upstream delete path; rotate ${ACE_E2E_PHONE}` or `pending → awaiting ace#1159`.
   - **Upstream-gap:** programs only — print Connect admin URLs (`<base_url>/a/<org_slug>/program/<id>/`) for manual deletion. There is no upstream delete view for programs.
6. **Render** via `renderOrphanReport()` from `lib/sweep-report.ts`. Write `connect-orphans.md` and `connect-orphans.yaml` to the sweep folder.
7. **Recommend — stop here in `mode: recommend`.** Return the structured recommended-action list (opportunities to deactivate — excluding every `setup_incomplete` one; unaccepted FLW invites to delete — each with id, name, confidence) plus the programs report-only list and the report Drive link, to the orchestrator. **Perform no mutations.** Do not try to prompt the human from this skill — a dispatched subagent can't reach them; the orchestrator runs the confirmation gate (see `agents/sweep.md § Human-confirmation gate`).

## Execute phase (`mode: execute` only)

Runs only when the orchestrator re-dispatches with `mode: execute` + `approvedIds` (the ids the human approved in chat). Mutate **only** those ids:

- **Malformed opportunities (repair)** → call `connect_update_opportunity` with `{ organization_slug, opportunity_id, end_date: <date> }`. **Two guards, both load-bearing:** (1) only ever FILL an empty `end_date` — never shorten an existing one; (2) if the opportunity is **in the live-set**, propose a FUTURE date so the repair cannot end a run that is still going. A past date is fine only for an orphan. The atom re-reads via `getOpportunity` on the 302, so the repair is verified rather than asserted.
- **Opportunities** → call `connect_update_opportunity` with `{ organization_slug, opportunity_id, active: false }`. If an approved id is `setup_incomplete`, do not call it: return it as `not-sweepable: setup_incomplete (Connect auto-purges at 6 months, no delete API)`, never as success.
- **Unaccepted FLW invites** → call `connect_delete_unaccepted_flw_invites({ organization_slug, opportunity_id, user_invite_ids: [...] })`. **This path is currently unreachable — see ace#1159:** no atom returns the invite row id. `connect_list_flw_invites` shipped (ace#824/#855, `b23303ff`) but its `FlwInviteRow` carries no id, and `connect_list_invites` is PROGRAM-scoped, not the FLW invite table. Until #1159 surfaces the `UserInvite` pk, report these rather than attempting the delete. Accepted invites in the list are silently skipped server-side; cascade-deletes associated `OpportunityAccess` rows.

Return the per-item result. Programs are never mutated (upstream gap — report-only).

## Failure modes

- **Live-set path doesn't resolve:** abort with "Run `sweep-live-set` first."
- **`connect_list_*` returns 401/403:** session is stale; recommend `/ace:connect-login` then retry.
- **An orphan opportunity is already inactive:** treat as success (no-op) — EXCEPT a `setup_incomplete` one, which is reported as not sweepable (above), because "already inactive" there means the sweep removed nothing that matters.

## Implementation notes for agents

- The Connect `delete_opportunity()` helper exists in `commcare_connect/opportunity/deletion.py` (used by Celery tasks) but no Django view exposes it. Its one caller is `delete_stale_opportunities` (`opportunity/tasks.py`, scheduled Mondays 02:00 by migration `0105_purge_stale_opportunities_periodic_task`): opportunities with `date_created` older than six months and no `UserVisit`. That is the only removal a `setup_incomplete` orphan gets. Building a connect-delete-opportunity atom (*not yet implemented*) requires an upstream PR — out of scope.
- **The accepted-invite gap is permanent until upstream moves, and ace#1159 does NOT close it.** The delete view filters `exclude(status=accepted)` server-side, so accepted invites are unreachable through it no matter what ids we obtain — and every successful Phase 6 run CLAIMS its tile, which makes the invite accepted. That is the dominant class of accumulated demo-user access. `delete_opportunity()` (the only thing that cascade-deletes `OpportunityAccess` for an accepted worker) has no view. So: #1159 unblocks the pending minority; the accepted majority needs an upstream Connect PR or a `${ACE_E2E_PHONE}` rotation. Do not let #1159 read as finishing this job.
- **Why the accumulation matters beyond tidiness:** the mobile opp-list endpoint filters `Opportunity.objects.filter(opportunityaccess__user=...)` with no `active=True` filter, so ACE's existing soft-deactivate does NOT remove device tiles. They accumulate per demo user forever. Phase 6's claim recipe scrolls to find its target tile among them on a FIXED budget (`speed 80` / `timeout 40000`), which has already produced two deterministic failures when the target sat 8+ tiles deep (ace#647). A fixed budget against an unbounded list degrades on a cadence.
- The Connect `delete_user_invites` HTML view at `/a/<org_slug>/opportunity/<opp_id>/delete_invites/` is `@csrf_exempt` and the atom `connect_delete_unaccepted_flw_invites` calls it directly. Accepted invites are silently skipped server-side, so the caller doesn't need to pre-filter — but doing so saves a server roundtrip.

## Related skills

- `sweep-live-set` produces the live-set this skill diffs against.
