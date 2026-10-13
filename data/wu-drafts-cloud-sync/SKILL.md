---
name: wu-drafts-cloud-sync
description: Implement or review WU-DRAFT-001 My Documents for WriteUrdu using the existing METRICS_DB D1 database. Add authenticated writing_documents CRUD, Save to my account, cross-device restore, throttled sync and revision conflict handling while preserving localStorage autosave/history.
---

# WriteUrdu My Documents — local-first account persistence

Read first:

1. `specs/WU-DRAFT-001-cross-device-cloud-drafts.md`
2. `specs/WU-AUTH-001-social-authentication-foundation.md`
3. `specs/WU-ACCOUNT-001-account-document-platform-boundary.md`
4. `docs/WU-AUTH-DRAFTS-IMPLEMENTATION-PLAN-2026-08-13.md`
5. current `js/editor-tools.js` and writer bootstrap code
6. current migrations and `METRICS_DB` consumers.

## Core rule

**Account-backed documents extend local drafts; they never replace them.**

The existing browser-local autosave stays on the critical path and remains immediate/offline-safe.

Do not map the local ~650 ms save debounce to D1 writes.

## Database decision

Use the existing WriteUrdu D1 database:

```text
env.METRICS_DB
```

Do not create `WRITE_URDU_DB`, `ACCOUNT_DB` or another D1 database.

Expected domain layout:

```text
METRICS_DB
├── telemetry tables
├── share-artifact tables
├── Auth.js tables
└── writing_documents
```

Document code accesses `writing_documents` only. It obtains identity through `getSession()` from the auth wrapper.

## Step 1 — verify prerequisite state

Before coding:

- AUTH-A and AUTH-B must be stable;
- `getSession()` returns stable `session.user.id`;
- Google sign-in/local-writing preservation proof is green;
- inspect current migration sequence;
- capture current D1 table inventory;
- run existing product/telemetry/share baseline.

Do not proceed on an unexplained red baseline.

## Step 2 — additive document migration

Create the next numbered migration for:

```text
writing_documents
- id
- user_id
- editor_kind
- title
- content
- plain_text
- format_version
- revision
- created_at
- updated_at
```

Indexes:

```text
(user_id, updated_at DESC)
(user_id, id)
```

Initial guards:

- title <= 160 chars;
- content <= 750 KB UTF-8;
- editor kinds: basic/rich/keyboard;
- max 100 account-backed documents/user unless spec changes.

Migration rules:

- additive only;
- never edit applied migrations;
- never drop/rename telemetry/share/Auth.js tables;
- capture before/after table inventory;
- run existing telemetry/share/auth regressions after migration.

## Step 3 — authenticated API first

Expected routes:

```text
GET    /api/documents
POST   /api/documents
GET    /api/documents/:id
PATCH  /api/documents/:id
DELETE /api/documents/:id
```

Every handler:

- requires `DOCUMENTS_ENABLED=true`;
- calls project `getSession()`;
- uses `session.user.id` as owner;
- uses `env.METRICS_DB`;
- uses parameterized SQL;
- returns `Cache-Control: no-store`;
- validates limits server-side;
- never logs content;
- never trusts client-supplied `user_id`.

Do not query Auth.js `accounts`/`sessions` tables directly for authorization.

## Step 4 — optimistic concurrency

PATCH requires client's last known `revision`.

Equivalent update:

```sql
UPDATE writing_documents
SET title = ?, content = ?, plain_text = ?, revision = revision + 1, updated_at = ?
WHERE id = ? AND user_id = ? AND revision = ?
```

No matching row because revision moved => `409 Conflict`.

No silent last-write-wins and no automatic merge.

## Step 5 — basic writer pilot

Integrate through one shared account-persistence client/module, not transliteration code.

First remote action is explicit:

```text
Save to my account
```

Signing in alone uploads nothing.

Keep local account metadata separate from existing draft payload:

```text
documentId
lastSyncedRevision
lastSyncedSignature
syncState/error
```

Never store OAuth/session tokens or provider identity in localStorage.

## Step 6 — remote sync cadence

For an already account-backed document:

- local save continues normally;
- local signature change marks remote state dirty;
- remote write occurs roughly 20–30 seconds later;
- explicit save may sync immediately;
- safe visibility-change sync is optional;
- D1/API failure never blocks local save.

No per-keystroke network calls.

## Step 7 — truthful status

Represent local and account state independently:

```text
Saved on this device
Saved to your account
Saving to your account…
Account save paused — your local draft is safe
This document changed on another device
```

Never imply remote success when only localStorage succeeded.

## Step 8 — My Documents

Build a focused noindex `/my-documents` route:

- recent list;
- title/preview/editor kind/modified time;
- open in correct editor;
- rename;
- delete with confirmation;
- copy/recovery action;
- empty state linking to writing.

List endpoint should not transfer every full document body.

## Step 9 — safe restore

Use existing editor adapter/handoff mechanisms.

Rules:

- no document text in URLs;
- rich content remains rich;
- a different non-empty local draft is not silently replaced;
- preserve local work/history or ask before replacement;
- remote revision metadata is updated correctly after open.

## Step 10 — rich + keyboard

Extend the same client/API through existing adapters.

Verify:

- rich HTML formatting survives exact round-trip;
- Urdu/RTL characters survive unchanged;
- keyboard editor round-trip works;
- local history remains independent.

## Step 11 — conflict UX

On 409 offer:

1. Open account version.
2. Keep this device as a new copy.
3. Optional explicit Replace account version after fresh revision + confirmation.

Default preserves data.

## Shared-D1 safety

The physical database is shared; product domains are not.

Documents module must not:

- update telemetry rollups/events;
- update share artifacts;
- modify Auth.js account/session records;
- join provider account/email fields into document authorization.

Telemetry/share/auth code must not begin reading document content.

Avoid a generic all-table DAO.

## Tests

Server:

- unauthenticated CRUD => 401;
- disabled documents => safe unavailable;
- user A cannot list/get/update/delete user B's document;
- invalid kind/oversize/quota rejected;
- list omits full bodies;
- stale revision => 409;
- hard delete removes row;
- no content logging;
- migration preserves telemetry/share/Auth.js tables.

Browser/product:

- signed-out local autosave still works;
- sign-in uploads nothing automatically;
- explicit Save to my account creates one document;
- local save remains immediate during API/D1 failure;
- remote writes are throttled;
- second browser/device restore works;
- rich formatting and Urdu/RTL survive;
- conflict is surfaced;
- remote open does not silently destroy local work.

Run the full existing WriteUrdu suite after focused tests.

## Rollback

Set:

```text
DOCUMENTS_ENABLED=false
```

Local drafts/history continue. Existing remote rows and all shared-database tables remain intact.

Do not drop `writing_documents` as normal rollback.

## Stop conditions

Stop and fix if:

- implementation requires another D1 database;
- document migration touches existing table definitions;
- cloud API becomes required for typing;
- sign-in uploads historical local drafts;
- any document query is not scoped by session user ID;
- remote writes mirror the local debounce;
- rich/Urdu content is corrupted;
- conflict resolution silently overwrites unseen changes.
