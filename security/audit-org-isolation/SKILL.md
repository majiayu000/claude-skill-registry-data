---
name: audit-org-isolation
description: Find Express route handlers that touch multi-tenant Prisma models without going through injectOrgFilter / injectWriteFilter. Use after adding new routes, before committing, and during security review.
---

# audit-org-isolation

Multi-tenant data isolation is the project's #1 security invariant. This skill greps for any handler that bypasses it.

## Background

The middleware `injectOrgFilter` (reads) and `injectWriteFilter` (writes) live at `apps/api/middleware/org-isolation.ts`. They append `organizationId = req.user.organizationId` to Prisma queries automatically. Any handler that talks to a multi-tenant model without these middlewares is a leak risk.

## Steps

1. **List multi-tenant models** by grepping `data/schema/prisma/schema.prisma` for `organizationId`.
2. **For each model**, grep `apps/api/routes/` for direct usage:
   ```
   prisma.<modelName>.find
   prisma.<modelName>.update
   prisma.<modelName>.delete
   prisma.<modelName>.create
   ```
3. **For each match**, check the surrounding handler:
   - Is the route mounted with `authenticateToken` + the org-isolation middleware?
   - OR does the handler explicitly include `organizationId: req.user.organizationId` in `where`?
4. **Flag violations** — handlers that touch a multi-tenant model with neither protection.
5. **Report** as a table:
   ```
   File:line          Model        Operation     Risk
   ```
6. **Do not fix automatically** — show the user the violations first. They may have intentional admin-only routes.

## Verification

- [ ] All multi-tenant models scanned
- [ ] Report grouped by file
- [ ] Each violation includes file:line for easy navigation

## Notes

- `WEBSITE_ADMIN` routes are allowed to bypass — flag them but mark as `[admin]`
- The `users` and `organizations` tables themselves have special rules — check existing patterns before flagging
- See [[Architecture/Org Isolation]] in the vault for full context
