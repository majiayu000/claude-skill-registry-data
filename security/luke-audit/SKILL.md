---
name: luke-audit
description: >
  Compliance audit of the Luke codebase against architectural constraints in
  CLAUDE.md. Finds violations of stack rules, AppConfig misuse, auth/crypto
  issues, RBAC drift, pricing/collection errors, storage misuse, NAV patterns,
  frontend shadcn violations, and dev pattern failures.
  Use after vibe coding sessions or before releases.
  Scoping: default = diff vs merge-base. /luke-audit apps/web | --since <ref> | --full
argument-hint: '[--full|--since <ref>|<path> [--since <ref>]]'
context: fork
agent: Explore
background: false
disallowed-tools: Edit, Write, NotebookEdit
---

# Luke Architecture Audit

Read-only. Do NOT modify any file.
Find violations of the architectural constraints in CLAUDE.md.
Report findings with proposed fixes — never apply them.

**Read `.claude/skills/luke-shared/audit-protocol.md` first** and apply it in
full: diff scoping (§1), baseline suppression (§2), the mandatory "Promotion
to rule" section (§3), `lessons.md` as a check input (§4), and the
constraint/heuristic classification (§8).

**Scope of this skill: application architecture.** Platform state — exact
versions, dependency alignment, Node/pnpm/Docker lifecycle, package-manager
policy, toolchain health — belongs to `/luke-deps`
(`.claude/skills/luke-shared/governance-map.md`). Consume a platform finding
when it explains an application finding; never maintain a second checklist for
it. Several checks that used to live here now have a deterministic owner in
`tools/scripts/check-platform-integrity.ts`.

Then read these files:

- `CLAUDE.md` (project root)
- `lessons.md` (project root) — the part routed to this skill, per protocol §4
- `packages/core/src/schemas/config.ts` (AppConfigRegistry)
- `packages/core/src/schemas/rbac.ts` (sectionEnum, SECTION_TO_PERMISSION, SECTION_ACCESS_DEFAULTS)
- `packages/core/src/auth/permissions.ts` (RESOURCES, ROLE_PERMISSIONS)
- `packages/core/src/storage/config.ts` (`isValidBucket()` — the authoritative bucket list)
- `packages/core/src/schemas/pricing.ts` (`PRICING_CURRENCIES` — the authoritative currency list)

These source files are the single source of truth for enum-like checks below —
never assume a hardcoded count or list from this skill file.

**Accepted ADRs are normative architecture**, not documentation
(`governance-map.md` §4). Read the ADR files that bear on the scope directly
from `docs/decisions/` — the generated index is for navigation and is **not**
proof that no other ADR exists, because ADRs have been missing from it. Load
only what the scope touches, not the whole directory.

Code that contradicts an Accepted ADR is reported as `ADR/CODE CONFLICT` with
the evidence, and the user decides. Never conclude from the contradiction alone
that the ADR is stale, and never reinterpret one to fit the implementation.

**Invocation arguments:** $ARGUMENTS

Resolve the invocation arguments above per `audit-protocol.md` §1 **before**
running any git scope derivation. The whole bound value is the scope selector
here — this skill takes no mode. If it is empty, use the protocol default —
diff vs merge-base, not the whole monorepo. If it carries an explicit selector,
that selector wins and the default is never derived.

---

## Check Areas

Three areas, one single pass. See the fan-out note in `../luke-shared/audit-protocol.md` §6.

### 1 — Stack, Config & Env

**Stack constraints:**

- Raw SQL inconsistent with the raw-SQL policy in `CLAUDE.md` (Stack
  Constraints → Raw SQL). **CONSTRAINT** against that policy, which is the
  normative source and carries its own exception classes — read it, do not
  restate it here. Raw SQL that the policy permits is not a finding; raw SQL
  whose justification is absent or contradicted is. Unusual-but-permitted SQL
  is an investigation trigger, not an automatic violation (protocol §8)
- `$queryRawUnsafe` / `$executeRawUnsafe` anywhere in application code — the
  policy names the tagged-template form as the only sanctioned one
- `any` type without explanatory comment on same line
- `// @ts-ignore` or `// @ts-expect-error` without explanation
- `console.log/warn/error/info` in `apps/api/src/` (must use Pino) or `apps/web/src/` (must use `lib/debug.ts`). Exception: `apps/api/prisma/` scripts.

**AppConfig system:**

- `process.env.*` in `apps/` or `packages/core/` outside these allowed files:
  `packages/core/src/runtime/env.ts`, `apps/*/next.config.*`
- AppConfig keys used in `prisma.appConfig.findUnique/upsert` that are NOT in `AppConfigRegistry`
- Sensitive keys (`password`, `pass`, `secret`, `token`) read with `decrypt: false`

**Env policy:**

- An app's `.env` or `.env.*` variables outside that app's permitted list in CLAUDE.md "Env Policy",
  or an API variable matching `FORBIDDEN_ENV_PATTERNS` (`apps/api/src/server.ts`); the web list may
  hold `NEXTAUTH_*`, and compose interpolation variables are out of scope

**Dev patterns:**

- `user.role === 'admin'` or `user.role === 'editor'` inline instead of `hasPermission()`
- `console.*` leaking through (covered above)
- An explicit `onDelete:` on every `@relation`, and an index led by every FK's columns, are enforced by P13 in `tools/scripts/check-platform-integrity.ts`; review what it cannot see: a `Cascade` without the justifying comment rule 6 asks for
- Missing `@@index` on commonly filtered columns (`isActive`, `navVendorId`, `brandId`, `seasonId`, `vendorId`) in `packages/db/prisma/*.prisma`. **CONSTRAINT**: CLAUDE.md rule 8 says so — enforce it as written. Its breadth is decided: the owner kept the rule as it is (`docs/LUKE_MONOREPO_AUDIT_2026-08-30.md`, Appendix Z.7), so do not raise it as `NEEDS DECISION`

---

### 2 — Auth, Crypto, RBAC & Sections

**Auth & crypto:**

- Import of `secrets.server`, `getMasterKey`, `deriveSecret`, `getApiJwtSecret` from `@luke/core` directly (must be `@luke/core/server`)
- Crypto utilities imported in client-side files (no `typeof window` guard)

**RBAC:**

- A write to RBAC keys that bypasses `saveConfig`/`saveConfigs`/`deleteConfig` and is NOT followed by
  `invalidateRbacCache()` after it commits
- `requirePermission` presence is enforced by `.semgrep/rules/procedure-requires-permission.yml`;
  review what it cannot see: a `selfProcedure` handler that breaks its contract in
  `apps/api/src/lib/trpc.ts`, a `nosemgrep: luke-procedure-requires-permission` whose reason does
  not hold, a permission that does not match the operation
- tRPC read-only procedures using `requirePermission('entity:update')` instead of `entity:read`
- Missing `withAuditLog` or `logAudit()` on procedures named `create`, `update`, `delete`, `remove`, `restore`, `unlink`

**Section system — cross-reference these three sources:**

- `sectionEnum` in `packages/core/src/schemas/rbac.ts`
- `SECTION_TO_PERMISSION` in same file
- `SECTION_ACCESS_DEFAULTS` in same file

Check:

1. Every `sectionEnum` value has an entry in `SECTION_TO_PERMISSION`
2. Every `sectionEnum` value has an entry in `SECTION_ACCESS_DEFAULTS` for all 3 roles
3. Every `SECTION_TO_PERMISSION` value maps to a valid `resource:action` in `VALID_RESOURCE_ACTIONS`
4. Any frontend route/nav item referencing a section string not in `sectionEnum`

**LDAP:**

- Auth strategy hardcoded instead of reading `auth.strategy` from AppConfig
- LDAP config written to AppConfig without `ldapConfigSchema` validation

**Multi-table writes:**

- Prisma write operations on 2+ related tables NOT wrapped in `prisma.$transaction()`
- `prisma.$transaction([...])` array syntax where operations depend on each other's results (should use callback syntax)

---

### 3 — Domain Logic, Storage & Frontend

**Pricing:**

- tRPC mutations for pricing parameter sets accessible to `editor` role (admin-only)
- Currency values not in `PRICING_CURRENCIES` (see `packages/core/src/schemas/pricing.ts`)
- Pricing calculations not scoped to both `brandId` and `seasonId`

**Collection Layout:**

- Collection progress as a hardcoded value or ordering instead of the catalog-backed `phaseId`
- Gender values as free strings instead of `COLLECTION_GENDER`; strategy or line-status options built
  from the default constants instead of the `CollectionCatalogItem` catalog
- Column visibility allowing more toggleable columns than `COLLECTION_COLUMNS_MAX_VISIBLE` outside
  fullscreen
- `skuBudget` on a Row or `skuForecast` on a Group (inverted)
- Collection row picture URLs constructed manually instead of `buildCollectionRowPictureUploadUrl()`

**Storage:**

- File handling outside an `IStorageProvider` implementation
- Bucket names not accepted by `isValidBucket()` in `packages/core/src/storage/config.ts`
- `/upload/` or `/api/uploads/` paths constructed manually
- `enableProxy` hardcoded instead of reading from config

**NAV sync:**

- NAV table names built without `sanitizeCompany()`
- Any import from `apps/api` inside `packages/nav`
- NAV sync requests built with `pool.request()` instead of `createSyncRequest()`
- NAV + local upsert NOT in `prisma.$transaction()`
- Sync touching `isActive` or enriched fields on local entities

**Frontend (apps/web/src only):**

- Direct `@radix-ui/` imports bypassing shadcn
- `style={{` for visual styling
- className via string concatenation instead of `cn()`
- Hex/rgb/hsl colors hardcoded instead of CSS variables
- Tailwind arbitrary values without justifying comment
- Hardcoded `localhost:3001` or absolute API URLs
- `globalThis.confirm(` or `window.confirm(` instead of `<ConfirmDialog>`

---

## Report Format

```
## Luke Audit Report
Scanned: <path or 'full monorepo'>
Date: <today>

### Summary
| Area                    | HIGH | MEDIUM | LOW | Status   |
|-------------------------|------|--------|-----|----------|
| Stack & Config & Env    |  N   |   N    |  N  | ✅/⚠️/🔴 |
| Auth & RBAC & Sections  |  N   |   N    |  N  | ✅/⚠️/🔴 |
| Domain & Storage & UI   |  N   |   N    |  N  | ✅/⚠️/🔴 |

✅ clean  ⚠️ LOW only  🔴 HIGH or MEDIUM present

Suppressed by baseline: N

### Findings

#### [AREA]

**[HIGH/MEDIUM]** — <title>
File: `path/to/file.ts:line`
Problem: <why this violates the constraint and what risk it creates>
Fix:
\`\`\`ts
// proposed fix
\`\`\`

**[LOW]** — <title> — `file.ts:line`
Fix: <one-line fix>

### Promotion to rule
<mandatory section — see §3 of the shared protocol>
```

### Rules

- HIGH: security, data corruption, broken auth/access control
- MEDIUM: architectural drift that compounds over time
- LOW: style inconsistency, minor deviation
- Max 25 findings — prioritize HIGH and MEDIUM
- If area is clean: `✅ No findings`
- Do NOT suggest refactors outside CLAUDE.md constraints
