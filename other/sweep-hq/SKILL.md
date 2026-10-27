---
name: sweep-hq
description: >
  Find orphaned CommCare HQ apps in the ACE domain and soft-delete the ones you approve. Needs a
  live-set from sweep-live-set.
disable-model-invocation: false
---

# sweep-hq

Find CommCare HQ applications in the ACE-owned domain (`connect-ace-prod`) that no current opp references and triage them. HQ apps soft-delete via `doc_type` mutation (restorable via HQ admin UI's "deleted applications" list); ACE drives this through the `commcare_delete_app` Playwright atom. Builds and multimedia remain documented gaps — no upstream delete API exists.

## Inputs

- Live-set file path from `sweep-live-set`.
- `ACE_HQ_DOMAIN` from `.env` (defaults to `connect-ace-prod`).
- `ACE_HQ_BASE_URL` (e.g. `https://www.commcarehq.org`).
- `mode` — `recommend` (default) | `execute`. In `recommend` the skill is **report-only**: diff/score/render + return the recommended-action list; **no mutations**. In `execute` it soft-deletes only `approvedIds`. The human-confirmation gate between the two is the orchestrator's job — see `agents/sweep.md § Human-confirmation gate`.
- `approvedIds` (`execute` mode only) — the exact app ids the human approved in chat. Mutate nothing outside this set.

## Products

- `ACE/_sweep/<timestamp>/hq-orphans.md` — human-readable triage report.
- `ACE/_sweep/<timestamp>/hq-orphans.yaml` — machine-readable `OrphanReport`.
- For approved orphan apps: `commcare_delete_app({ domain, app_id })` calls.

## Process

1. **Read the live-set** via `drive_read_file`.
2. **List HQ inventory:** `commcare_list_apps({ domain: ACE_HQ_DOMAIN })`. Returns `[{ id, name, doc_type }]` for every Application in the domain (soft-deleted apps are filtered server-side).
3. **Diff:** for each app whose `id` is NOT in `liveSet.identifiers.commcareAppIds`, mark as orphan candidate.
4. **Score:** call `scoreHqApp(item, ACE_HQ_DOMAIN)` from `lib/sweep-fingerprint.ts`. Returns high if the domain matches and name has Learn/Deliver/CRISPR pattern; medium for unrecognized names in the ACE domain; low for apps in a different domain (defensive — caller shouldn't normally pass these in).
5. **Build the `OrphanReport`** with `system: 'hq'`. Single Actionable section — orphan apps are soft-deletable.
6. **Render** + write `hq-orphans.md` and `.yaml` to the sweep folder.
7. **Recommend — stop here in `mode: recommend`.** Return the structured recommended-action list (orphan apps to soft-delete — each with id, name, confidence, and the reversibility note "90-day restorable via HQ admin UI") plus the report Drive link, to the orchestrator. **Perform no mutations.** Do not try to prompt the human from this skill — a dispatched subagent can't reach them; the orchestrator runs the confirmation gate (see `agents/sweep.md § Human-confirmation gate`).

## Execute phase (`mode: execute` only)

Runs only when the orchestrator re-dispatches with `mode: execute` + `approvedIds` (the app ids the human approved in chat). For each **approved** orphan app, call `commcare_delete_app({ domain: ACE_HQ_DOMAIN, app_id })`. The atom POSTs to HQ's `delete_app` web view, which soft-deletes by mutating `doc_type` to `<original>-Deleted` and creating a `DeleteApplicationRecord` for restore. Mutate nothing outside `approvedIds`; return the per-item result.

## Restoration

HQ apps are restorable for 90 days after soft-delete via the admin UI's deleted-applications list (`/a/<domain>/apps/deleted/`) or by calling `undo_delete_app/<record_id>/`. The sweep atom does NOT return the record id (the redirect response doesn't expose it), so restoration is a manual operation via the HQ web UI.

## Failure modes

- **Live-set path doesn't resolve:** abort with "Run `sweep-live-set` first."
- **`commcare_list_apps` returns 401 / session redirect:** the existing PlaywrightSession retry handles this transparently; if the retry also fails, surface a clear "Connect/HQ session expired — run /ace:connect-login" message.
- **`commcare_delete_app` returns 403:** the account lacks edit permission on the app — surface as a per-item failure, don't halt the batch.
- **An app is already soft-deleted** (very unlikely since `commcare_list_apps` filters them out, but possible if a race occurs): the second delete returns 302 to dashboard same as the first — treat as success (no-op).

## Implementation notes for agents

- HQ apps soft-delete is at `POST /a/<domain>/apps/delete_app/<app_id>/`. The view is CSRF-protected (`@no_conflict_require_POST` + `@require_can_edit_apps`); the `commcare_delete_app` atom handles the CSRF dance via the existing PlaywrightSession cookie jar.
- API key auth is sufficient for `commcare_list_apps` (CCHQ's TaskPie resource has `allow_session_auth=True`, so session cookies work too — we use session cookies to keep the auth path uniform with `commcare_delete_app`).
- HQ builds and multimedia have **no upstream delete API**. They are NOT surfaced in this skill's report; the human is expected to know that builds accumulate per release-build cycle and aren't cleanable from ACE.

## Related skills

- `sweep-live-set` produces the live-set this skill diffs against.
