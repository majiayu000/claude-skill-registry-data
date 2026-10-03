---
name: payload-cms-security
description: Harden Payload CMS deployments against access-control and upload-related issues. Covers collection and field-level access functions, hook safety, file upload validation, GraphQL and REST surface, admin UI exposure, and multi-tenant isolation strategies. Invoke before shipping a Payload app to production, opening admin to non-developers, or after a Payload version upgrade.
---

# Payload CMS Security

Payload (v2 / v3) gives you a powerful headless CMS in a Node app, but its security depends almost entirely on the **access functions you write per collection and per field**. Defaults are reasonable but not strict — production-readiness requires intentional config.

## When to invoke

- Shipping a Payload app to production
- Opening the admin UI to non-developer team members or clients
- After a Payload major version upgrade (v2 → v3)
- Adding a new collection, especially user-generated or multi-tenant data
- Investigating a "user X saw user Y's data" incident

## Step 1 — Lock the admin UI

By default the admin is at `/admin` on the same origin as the app. That is a permanent target.

Three layers of defense, use at least two:

1. **Zero Trust / IP allowlist in front** — put `/admin` behind SSO with Cloudflare Access, Tailscale, or a VPN. The admin should not be reachable from the open internet for most projects. See [`cloudflare-hardening`](../cloudflare-hardening/SKILL.md).
2. **Rate limit auth endpoints** — `/api/users/login` and friends. Cloudflare Rate Limit or `express-rate-limit` on the Express app.
3. **Strong auth for admin users** — long passphrases, MFA where supported (Payload v3 has plugins for this), no shared accounts.

Optional but worth it: move `/admin` to an unguessable path via `routes.admin`. Not strong security, but cuts noise:

```ts
// payload.config.ts
export default buildConfig({
  routes: { admin: '/cms-' + process.env.ADMIN_PATH_SUFFIX },
  ...
});
```

## Step 2 — Access control per collection

Every collection has `access` functions that decide who can `create`, `read`, `update`, `delete`. Defaults often allow logged-in users more than intended.

```ts
// collections/Invoices.ts
import type { CollectionConfig } from 'payload/types';

const isAdmin = ({ req: { user } }) => user?.role === 'admin';
const isOwnerOrAdmin = ({ req: { user } }) => {
  if (!user) return false;
  if (user.role === 'admin') return true;
  // Restrict to documents where ownerId equals the requesting user
  return { ownerId: { equals: user.id } };
};

export const Invoices: CollectionConfig = {
  slug: 'invoices',
  access: {
    create: ({ req: { user } }) => Boolean(user),
    read: isOwnerOrAdmin,
    update: isOwnerOrAdmin,
    delete: isAdmin,
  },
  fields: [/* ... */],
};
```

Patterns:

- **Return `true`/`false` for unconditional access.** Easy to reason about.
- **Return a `Where` filter for row-level restrictions.** Payload applies it to every query — the requester only sees / mutates matching rows.
- **Always check `user` for null** before reading properties. Unauthenticated requests pass `user: undefined`.
- **Default deny** for `delete` on most collections. Public APIs almost never want delete.

## Step 3 — Field-level access

Some fields are sensitive even within a collection a user can read.

```ts
fields: [
  { name: 'email', type: 'email' },
  {
    name: 'internalNotes',
    type: 'textarea',
    access: {
      read: ({ req: { user } }) => user?.role === 'admin',
      update: ({ req: { user } }) => user?.role === 'admin',
    },
  },
  {
    name: 'passwordResetToken',
    type: 'text',
    access: {
      read: () => false,            // never returned
      update: () => false,          // only set by hooks
    },
  },
],
```

Field access is your protection against RSC over-fetch (see [`nextjs-security`](../nextjs-security/SKILL.md)) and accidental API leakage.

## Step 4 — Hook safety

`beforeChange`, `afterRead`, `beforeRead` hooks run with elevated context. They can leak or modify data in ways the access functions cannot prevent.

```ts
hooks: {
  // Strip sensitive fields before returning to non-admins
  afterRead: [({ doc, req: { user } }) => {
    if (user?.role !== 'admin') {
      delete doc.internalNotes;
      delete doc.auditLog;
    }
    return doc;
  }],

  // Force ownerId server-side; never trust client to set it
  beforeChange: [({ data, req: { user }, operation }) => {
    if (operation === 'create' && user) {
      data.ownerId = user.id;
    }
    return data;
  }],
}
```

Anti-patterns in hooks:

- Calling `payload.find()` without passing `req` — runs with full privileges, bypasses RLS-like access functions
- `afterRead` that fetches related data without checking the caller's access to those related collections
- `beforeChange` that trusts client-provided IDs (use the session user instead)
- Logging the whole document on every change — captures PII into logs

## Step 5 — File uploads

If a collection has `upload: true`, every authenticated `create` writes a file to disk or S3. The combination of (a) user-supplied filename, (b) user-supplied MIME, and (c) the server later serving these files is the classic "upload PHP, hit URL" attack — even though Payload itself doesn't execute PHP, an attacker can target the storage layer.

```ts
{
  slug: 'media',
  upload: {
    mimeTypes: ['image/jpeg', 'image/png', 'image/webp', 'application/pdf'],
    staticDir: 'media',
    imageSizes: [/* defined sizes — Payload re-encodes images */],
    adminThumbnail: 'thumbnail',
  },
  access: {
    create: ({ req: { user } }) => Boolean(user),
    read: () => true,             // typically public
    delete: isOwnerOrAdmin,
  },
}
```

Hardening:

- **Restrict `mimeTypes`** to a strict allowlist. Do not accept `application/octet-stream` or `*/*`.
- **Server-side validate** with `file-type` against the actual bytes — MIME from the client is advisory.
- **Strip EXIF / metadata** from images (PII leak via geotags is common).
- **Re-encode images** through sharp / Payload's image processing — defangs polyglot files and clears most embedded payloads.
- **Cap file size** explicitly (`limits.fileSize`).
- **Store with a server-generated name**, never the user-supplied name on disk.
- **Serve from a separate domain / Cloudflare Pages / R2** with proper `Content-Disposition` headers and no script execution.

## Step 6 — GraphQL / REST surface

Payload exposes both REST and GraphQL automatically. Anything reachable is in scope.

- **GraphQL introspection** is on by default — turn off in production unless you have a reason to keep it:

  ```ts
  graphQL: { disable: process.env.NODE_ENV === 'production' ? false : false }
  // Or restrict the playground:
  graphQL: { disablePlaygroundInProduction: true }
  ```

- **`depthLimit` and complexity limits** — protect against deeply nested query DoS. Payload + `graphql-depth-limit` or `graphql-query-complexity`.
- **Disable unused collections from the API** entirely:

  ```ts
  { slug: 'audit-logs', admin: { hidden: true }, graphQL: false }
  ```

- **REST endpoints** respect the same access functions, but custom endpoints (`endpoints: [...]`) are not auto-protected — you write the auth check yourself.

## Step 7 — Authentication settings

```ts
// payload.config.ts
const config = buildConfig({
  cookiePrefix: 'app',
  csrf: ['https://example.com'],     // allowed origins for CSRF protection
  cors: ['https://example.com'],     // strict — not '*'

  // For your auth-enabled collection (often Users)
  // In the collection:
  auth: {
    tokenExpiration: 3600,          // 1h — match your session policy
    maxLoginAttempts: 5,
    lockTime: 600 * 1000,           // 10 min lockout
    cookies: {
      sameSite: 'Lax',
      secure: true,
      domain: 'example.com',
    },
  },
});
```

See [`auth-hardening`](../auth-hardening/SKILL.md) for the broader auth strategy.

## Step 8 — Multi-tenant collections

If one Payload instance serves multiple tenants (common SaaS pattern), tenant isolation is a top concern. Three approaches, from simplest to strongest:

1. **`tenantId` field + access filter** — every document has a tenant, every access function filters by the requesting user's tenant. Single-DB simplicity, but a missed access function leaks across tenants.
2. **Postgres RLS** under Payload — the database enforces isolation even if the app makes a mistake. See [`postgres-hardening`](../postgres-hardening/SKILL.md).
3. **Separate database per tenant** — strongest isolation, highest operational cost.

For most apps, (1) with disciplined code review is fine. For regulated data, add (2).

## Step 9 — Secrets and env

Payload reads from `.env` typically. Standard rules apply (see [`secret-hygiene`](../secret-hygiene/SKILL.md)).

Payload-specific notes:

- **`PAYLOAD_SECRET`** is used for JWT signing. Rotating it invalidates all sessions — schedule rotations for low-traffic windows.
- **Database URL** ends up in process env; ensure `process.env` is not leaked via debug routes or error pages.
- **S3 credentials** for media storage: scope the IAM policy to the specific bucket and operations needed (no `s3:*`).

## Step 10 — Update discipline

- Pin Payload to a patch version, watch the [Payload security advisories](https://github.com/payloadcms/payload/security/advisories) feed
- Test upgrades on staging before prod
- Database migrations: Payload's auto-migration works for additive changes; manual review for column drops or type changes

## Audit checklist

Before public launch:

- [ ] Admin path is behind SSO / Access / VPN, not on the open internet
- [ ] Every collection has explicit `access` for create/read/update/delete
- [ ] Sensitive fields have field-level access
- [ ] Hooks pass `req` to `payload.find/update/delete` (so access functions apply)
- [ ] File uploads have strict `mimeTypes` and server-side validation
- [ ] GraphQL introspection disabled in production (or you have a reason)
- [ ] CORS / CSRF lists are strict, no `*`
- [ ] `cookies.secure: true`, `sameSite: 'Lax'` or stricter
- [ ] `PAYLOAD_SECRET` is at least 32 random chars, in env, not committed
- [ ] No `payload.find()` calls in user-reachable code paths without `req`
- [ ] Tenant isolation strategy documented and reviewed

## What this skill will not do

- Help bypass Payload access controls on systems you do not own
- Endorse `access: { read: () => true }` on collections holding personal data
- Replace a Payload-specific security audit for high-stakes deployments
