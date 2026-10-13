---
name: wu-auth-add-provider
description: Add an approved OAuth identity provider to the existing WriteUrdu Auth.js foundation after it is stable. Keep identity scopes minimal, preserve the existing METRICS_DB-backed session system, and never auto-link accounts by email.
references:
  - google
  - facebook
---

# WriteUrdu — add an OAuth provider

Use only after `WU-AUTH-001` AUTH-A/AUTH-B is stable.

Read:

- `specs/WU-AUTH-001-social-authentication-foundation.md`;
- `specs/WU-ACCOUNT-001-account-document-platform-boundary.md`;
- current `functions/lib/auth.mjs`;
- matching provider reference in this directory;
- current Auth.js provider source/docs.

## Provider order

1. Google first.
2. Facebook after Google + first My Documents cross-device restore is stable.

Do not add providers merely because Auth.js supports them.

## Platform invariants

Adding a provider must not require:

- another session system;
- another D1 database;
- another users table;
- editor changes;
- document schema changes;
- a new auth framework.

The existing foundation remains:

```text
Auth.js
→ D1Adapter(env.METRICS_DB)
→ existing shared WriteUrdu D1 database
```

Provider-specific work belongs only in provider configuration/construction and sign-in UX.

## Implementation steps

### 1. Verify current provider API

Check current Auth.js provider export/config and provider developer-console requirements. Do not copy old callback/scope examples blindly.

### 2. Register provider externally

Use canonical production callback under `write-urdu.com`. Preview callbacks are added only when deliberately supported.

Never place client secrets in source/docs/issues/logs.

### 3. Configure Cloudflare secrets

Google:

```text
GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET
```

Facebook:

```text
FACEBOOK_CLIENT_ID
FACEBOOK_CLIENT_SECRET
```

No D1 configuration change is needed: continue using existing `METRICS_DB`.

### 4. Update only the auth boundary

Only `functions/lib/auth.mjs` (or the established single project-owned auth module) imports provider code.

Provider appears only when its complete config is ready.

Auth readiness is provider-neutral: at least one complete provider may make auth ready.

### 5. Identity scopes only

Do not request:

- Google Drive/Gmail/Contacts/Calendar;
- Facebook posting/Page/friends/ads/business permissions;
- provider storage/data access unrelated to sign-in.

Any scope expansion is a separate feature.

### 6. Sign-in UI

Render provider buttons only when configured.

Use current Auth.js CSRF-safe sign-in behavior and the existing same-origin callback contract.

### 7. Account-linking safety

Do not merge two provider identities merely because email strings match.

Cloud documents remain authorized by stable `session.user.id`, never provider/email.

A future Connected Accounts feature requires separate explicit security/recovery design.

### 8. Regression

For each provider verify:

- complete pair => provider available;
- incomplete pair => provider excluded;
- one broken provider does not disable another valid provider;
- `/api/me` still exposes stable user ID;
- Auth.js continues using `METRICS_DB`;
- no new D1 binding/database is introduced;
- My Documents authorization remains by user ID;
- anonymous editor remains usable.

Production smoke:

- OAuth callback;
- expected provider row in Auth.js `accounts` table;
- session works;
- sign-out works;
- existing provider regression passes;
- existing telemetry/share endpoints remain healthy.

## Facebook gate

Before Facebook ships, this Google flow must already be stable:

```text
write locally
→ Google sign in
→ Save to my account
→ second browser/device
→ restore/edit
```

Do not use provider expansion to mask persistence bugs.

## Out of scope

- email/password;
- account linking;
- provider APIs beyond identity;
- social posting;
- changing `writing_documents`;
- changing transliteration/editor behavior;
- creating another D1 database.
