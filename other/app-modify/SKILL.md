---
name: app-modify
description: >
  Edit a deployed, live CommCare app (fix a form, add or change a question) and ship it to its live
  opportunity, verifying Connect picked it up. Use when someone asks to change a live app. Needs
  Nova, HQ and opp ids.
---

# Modify a deployed app

Changes an app that is already deployed, and often already live on an opportunity: add or
reword a question, change logic, adjust a case property or a menu. The edit goes into the same
Nova app, the same HQ app id, and the same opportunity, so the partner never ends up with a second
app or a second opportunity. This skill composes the build skills in the order a live change needs
and adds the one check no build skill makes: **did the live opportunity actually get the new
version?**

The platform facts are in [`playbook/README.md`](../../playbook/README.md) (row "Edit a deployed app
and ship the new version"), [`commcare-api.md` § Changing a live app](../../playbook/integrations/commcare-api.md#changing-a-live-app--what-you-can-and-cannot-do)
and [`connect-api.md` § Changing a live opportunity](../../playbook/integrations/connect-api.md#changing-a-live-opportunity).
This skill does not restate them.

## Inputs

| Parameter | Used for | Resolver |
|---|---|---|
| `change_request` | what to change, verbatim from the requester | explicit arg |
| `nova_app_id` | the Nova app to edit (one per Learn / Deliver app) | explicit arg; default: run_state `phases.commcare-setup.products.apps.<learn\|deliver>.nova_app_id`; else the program context doc's Apps |
| `hq_domain`, `hq_app_id` | the HQ app the Nova app uploads into. Must be the SAME id that is live | explicit arg; default: run_state `phases.commcare-setup.products.apps.*`; else the context doc's Apps |
| `opportunity_id`, `program_org` | the live opportunity that serves the app, and its program's org (Connect URL org; see `connect-api.md` § Which Connect orgs ACE acts in) | explicit arg; default: run_state `phases.connect-setup.products.connect.opportunity.id` + `pm_org_slug`; else the context doc's Scope. Omit both when no opportunity uses the app yet |
| `server` | HQ cluster | explicit arg; default `ACE_HQ_DEFAULT_SERVER` |

The skill runs with no `run_state.yaml` when the ids are passed. Inside a run, the resolver
defaults apply and the result is written back to the run (step 10).

## Products

- A change record with before and after state (build ids, deliver units, payment units, marker diff):
  - inside a run, `<N>-<phase>/app-modify_<YYYYMMDD-HHMM>.md` in the run folder;
  - on a program project, a dated line in the context doc's Decisions plus the board task.
- A new released HQ build on the same `hq_app_id`.

## Terminology

Every string this skill puts in front of a reader follows
[`skills/_terminology.md`](../_terminology.md): **`Connect`, never `CommCare Connect`**, and
**US spelling, always** — program, enrollment, enroll, organization, behavior, center; never
programme, enrolment, organisation (owner, 2026-10-20: *"everything should be US spelling"*,
ace#3232). Identifiers (case properties, slugs, ids, config keys) keep their spelling.

## Process

1. **Confirm the approval.** This skill writes to a live partner object. The caller, at level 0,
   must already have shown the requester or owner the change, the before state and the intended
   after state, and got approval (`partner-on-connect-program § Changing a live program` step 3).
   A subagent cannot ask; if no approval is recorded in the dispatch, stop and return the proposal
   instead of editing.
2. **Record the before state.**
   - `commcare_list_apps` for the domain: confirm `hq_app_id` exists and note its latest released
     build.
   - `commcare_download_ccz` of that released build with `write_to_path`, keeping the returned
     `connect_markers` / `projected_connect_state`.
   - When `opportunity_id` is set, `connect_list_deliver_units` and `connect_list_payment_units`
     at `program_org`.
3. **Classify the change.** Does it touch Connect markers: forms, modules, `<learn:deliver>` /
   `learn_module` / `assessment` blocks, or deliver-unit slugs? Content-only edits (labels,
   hints, constraints inside an existing form) are low risk. Marker edits can add or drop deliver
   units, so say this in the proposal before step 4. A dropped deliver unit that holds a payment
   unit cannot be repaired from ACE, because there is no payment-unit update or delete atom.
4. **Edit the app in Nova.** Use `/nova:edit` with the change request, or the private-work atoms
   directly through `lib/nova-work.ts` (`begin_work` → edits → `save_work`). Its `save()` throws
   unless Nova saved, and an unsaved edit ships nowhere. Read the result back with `get_app`.
   Translate last: editing an English string demotes its translations
   (`nova-integration.md` § The per-language channel).
5. **Re-check the Connect markers** with `app-connect-coverage` on the edited Nova app (pass the
   Nova app id). It auto-fixes a missing marker before upload.
6. **Re-upload to the same HQ app.** Use the update-in-place path in `app-deploy` with the explicit
   `nova_app_id`, `hq_domain` and `hq_app_id`. Then confirm with `commcare_list_apps` that the
   app id is unchanged. A new id means a second app was created. Stop and report it; do not
   release it.
7. **Re-apply HQ settings** with `app-hq-settings` on the same HQ app id. A Nova re-upload drops
   the settings Nova can't set (camera-only capture, grid menus).
8. **Build, release and verify the release.**
   - `app-release` on the HQ app id.
   - `app-release-qa` on the new build, passing `--opportunity-id` when an opportunity uses the
     app. Its payment-integrity checks stay in force: the casedb preload audit (Step 4, `casedb_preloads`,
     ace#2006 — a pre-filled payment field lets a worker re-file a paid encounter) and the
     re-release invariants (Step 4.7: question `@id`s and `form_field_rules` targets still exist).
   - A QA failure halts here. The release is already live, so report it as a regression to fix
     forward; do not paper over it.
9. **Verify Connect picked it up.** This is the step that turns the playbook's UNVERIFIED residual
   into an observation. Skip it only when no opportunity uses the app.
   - Download the new released CCZ (`commcare_download_ccz`, `write_to_path`) and compare its
     `connect_markers` with step 2's.
   - Read `connect_list_deliver_units` and `connect_list_payment_units` again at `program_org`.
   - **Markers unchanged:** the deliver units should match step 2 exactly. Record "content-only
     re-release, deliver units unchanged".
   - **Markers changed:** if the deliver-unit list does not show the new or renamed unit, the
     opportunity has not re-synced. No atom triggers `Sync Deliver Units` on an opportunity
     whose units are already synced: the sync inside `connect_list_deliver_units` and
     `connect_create_payment_units` fires only when the form's checkbox list is empty. So hand
     the operator the opportunity wizard's `Sync Deliver Units` button at the program org's URL,
     then re-read. A new deliver unit needs its own payment unit (`connect-opp-modify`).
   - Whether workers' phones take the new build before their next visit is not observable from
     ACE. Say so in the record rather than implying it.
   - Append what you observed to [`connect-api.md` § Changing a live opportunity](../../playbook/integrations/connect-api.md#changing-a-live-opportunity)'s
     residual, through the shipping skill as a separate small PR. The residual stays open until
     someone observes it.
10. **Record the change.** Write the before and after (build ids, marker diff, deliver and payment
    units, QA verdict) to the record named in § Products. Inside a run, add a step entry under the
    phase that owns the app. Never flip a phase's status.

## MCP Tools Used

- Nova: `begin_work`, `save_work`, `get_app`, plus the edit atoms `/nova:edit` chooses (all via `lib/nova-work.ts`)
- ace-connect (HQ): `commcare_list_apps`, `commcare_download_ccz`, and through the composed skills `commcare_make_build`, `commcare_release_build`
- ace-connect (Connect): `connect_list_deliver_units`, `connect_list_payment_units`
- Composed skills: `app-connect-coverage`, `app-deploy`, `app-hq-settings`, `app-release`, `app-release-qa`

## Existing objects

- **`app-deploy` updates the HQ app in place.** That makes this skill possible, and it also means
  the re-upload becomes the live app's next build. Step 6 halts rather than release under a new id.
- **Deliver units are shared** across opportunities in the same holding org wired to the same
  released Deliver app (ace#573). A marker change affects every such opportunity. List them in
  the proposal (`connect_list_opportunities`).
- **A deliver unit that holds a payment unit cannot be dropped safely.** No atom updates or deletes
  a payment unit. Step 3 flags marker removals before any edit.
- **The Learn `passing_score` is not touched by an app edit** (it lives on the CommCareApp row,
  ace#1350). Changing it is `connect-opp-modify`.

## Mode Behavior

- **Auto:** runs steps 2–10 once approval is recorded in the dispatch; halts on any QA failure or a
  changed HQ app id.
- **Review:** presents the step 3 classification and the marker diff before step 4, and the step 9
  observation before closing.

## Dry-Run Behavior

When `--dry-run` is active, run steps 2–3 (reads only) and write the proposal to the change record.
Do not edit Nova, upload, release or call Connect write paths.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-10-18 | Initial version: the modify path for a deployed app, with a live check that the opportunity picked up the release (audit item 6) | ACE (build-vs-maintain audit) |
