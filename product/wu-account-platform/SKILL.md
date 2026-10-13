---
name: wu-account-platform
description: Orchestrate WriteUrdu account, My Documents and future collaboration work. Use the existing METRICS_DB D1 database, preserve anonymous/local writing, and route each implementation request to the smallest approved child slice. Do not infer profiles, teams or social graph from authentication.
---

# WriteUrdu account platform orchestrator

Read first:

1. `specs/WU-ACCOUNT-001-account-document-platform-boundary.md`
2. `specs/WU-AUTH-001-social-authentication-foundation.md`
3. `specs/WU-DRAFT-001-cross-device-cloud-drafts.md`
4. `docs/WU-AUTH-DRAFTS-IMPLEMENTATION-PLAN-2026-08-13.md`
5. `docs/WU-AUTH-INVOICECRAFTLY-REUSE-MAP-2026-08-19.md`

## Platform invariant

WriteUrdu remains an anonymous-first Urdu writing product.

Account work is introduced in layers:

```text
L0 anonymous/local writing
L1 optional identity
L2 My Documents
L3 minimal account preferences when needed
L4 private collaboration — separate discovery/spec
L5 teams — separate discovery/spec
L6 public profile/follow/feed — Hold
```

Never jump layers because the underlying database could support them.

## Database invariant

The initiative reuses the existing WriteUrdu D1 database:

```text
env.METRICS_DB
```

Do not create `ACCOUNT_DB`, `WRITE_URDU_DB` or another D1 database.

Logical domains inside the shared physical database:

```text
existing telemetry tables
existing share-artifact tables
Auth.js adapter tables
writing_documents
future approved tables only when corresponding features are approved
```

Isolation is through migrations, modules, APIs and authorization.

## Routing

### Authentication backend foundation

Use:

`.claude/skills/wu-auth-authjs-d1-foundation/SKILL.md`

when the task is about Auth.js packages, D1 adapter schema, `/api/auth/*`, `/api/me`, readiness, sessions or backend auth tests.

### Google/account shell

Use:

`.claude/skills/wu-auth-account-shell/SKILL.md`

when the task is about `/sign-in`, Google OAuth production callback, header account state, sign-out or preserving local writing through OAuth.

### My Documents

Use:

`.claude/skills/wu-drafts-cloud-sync/SKILL.md`

when the task is about `writing_documents`, `/api/documents*`, Save to my account, `/my-documents`, cross-device restore, sync cadence or revision conflicts.

### Additional provider

Use:

`.claude/skills/wu-auth-add-provider/SKILL.md`

only after the existing provider and account-value loop are stable.

### Profiles/collaboration/teams/followers

Do not implement from this skill. They require separate approved feature specs.

## Sequence gates

### AUTH-A gate

Must prove:

- no new D1 database;
- Auth.js uses `METRICS_DB`;
- migration is additive;
- existing telemetry/share behavior remains green;
- auth off leaves anonymous product unchanged;
- stable session user ID exists.

### AUTH-B gate

Must prove:

- real Google custom-domain sign-in;
- local writing survives sign-in/sign-out;
- `/api/me` works;
- existing shared-D1 features remain healthy.

### DOC-A/B gate

Must prove:

```text
write locally
→ explicitly Save to my account
→ second browser/device
→ sign in
→ open same document
→ continue writing
```

before expanding to Facebook or richer account identity.

## Shared-D1 rules

- Existing applied migrations are immutable.
- New auth/document schema uses new numbered migrations.
- Auth.js adapter owns its tables.
- Document module owns `writing_documents`.
- Telemetry/share modules stay in their domains.
- Product authorization is always `session.user.id`.
- No document content enters telemetry/auth logs or rows.
- Rollback is feature-flag based, not table dropping.

## Product guardrails

Do not:

- require login to type/write;
- automatically upload local history on sign-in;
- expose public profiles because a user account exists;
- add team/ACL tables in anticipation of future work;
- build a follower graph/feed;
- request Google Drive/Gmail or Facebook social permissions for identity;
- auto-link provider accounts by email;
- introduce a framework rewrite.

## Completion behavior

After any slice:

- update the owning spec with shipped evidence/status only when implementation actually exists;
- keep unrelated future layers unchanged;
- run the full WriteUrdu regression, including telemetry/share/product/SEO behavior;
- record any manual Cloudflare/provider configuration still required.
