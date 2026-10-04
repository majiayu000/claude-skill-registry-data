---
name: snaap-api
description: >
  Use when adding or changing any endpoint on the snaap-backend Express + MongoDB API. Covers REST
  conventions, the error envelope, validation, RBAC and the existing HomepageSection shape.
---
# Snaap API conventions

**Extend, don't fork.** Reuse existing resources. The `/homepage-sections` resource already exists
with admin CRUD; confirm its real schema before changing it:

```
{ sectionKey, enabled, title, subtitle, order,
  items: [{ title, subtitle, image, iconKey, ctaLabel, ctaLink, category, search }] }
```

**Authorization:** every write route is gated by `requireAdmin` placed BELOW the public GET routes
— authorization, not just authentication. `GET /api/admin/customers` is currently mis-ordered
above the guard; fix it, don't copy the pattern. Add an audit-log entry (who / what / when /
previous value) on every write.

**Validation:** validate `req.body` / `req.query` at the boundary; guard against NoSQL injection
and mass assignment. Validate upload type and size.

**Responses:** a consistent error envelope; consistent `page` / `limit` pagination with a total
count; ETag / caching where the resource is cacheable.

**Migrations:** reversible, dry-run first, references checked (orders / reviews / section items)
before soft-deleting; never drop documents; never run destructive commands.

**Secrets:** env var NAMES only in code and docs. `helmet` and `express-rate-limit` are installed —
wire them into `server.js`. Never commit `.env`.
