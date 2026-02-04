---
name: upgrading-to-prisma-6
description: Migrate from Prisma 5 to Prisma 6 handling breaking changes including Buffer to Uint8Array, implicit m-n PK changes, NotFoundError to P2025, and reserved keywords. Use when upgrading Prisma, encountering Prisma 6 type errors, or migrating legacy code.
allowed-tools: Read, Write, Edit, Grep, Glob
version: 1.0.0
---

# Prisma 6 Migration Guide

This skill guides you through upgrading from Prisma 5 to Prisma 6, handling all breaking changes systematically to prevent runtime failures and type errors.

---

<role>
This skill teaches Claude how to migrate Prisma 5 codebases to Prisma 6 following the official migration guide, addressing breaking changes in Buffer API, implicit many-to-many relationships, error handling, and reserved keywords.
</role>

<when-to-activate>
This skill activates when:
- User mentions "Prisma 6", "upgrade Prisma", "migrate to Prisma 6"
- Encountering Prisma 6 type errors related to Bytes fields
- Working with Prisma migrations or schema changes during upgrades
- User reports NotFoundError issues after upgrading
- Reserved keyword conflicts appear (`async`, `await`, `using`)
</when-to-activate>

<overview>
Prisma 6 introduces four critical breaking changes that require code updates:

1. **Buffer → Uint8Array**: Bytes fields now use Uint8Array instead of Buffer
2. **Implicit m-n PKs**: Many-to-many join tables now use compound primary keys
3. **NotFoundError → P2025**: Error class removed, use error code checking
4. **Reserved Keywords**: `async`, `await`, `using` are now reserved model/field names

Attempting to use Prisma 6 without these updates causes type errors, runtime failures, and migration issues.
</overview>

<workflow>
## Migration Workflow

**Phase 1: Pre-Migration Assessment**

1. Identify all Bytes fields in schema
   - Use Grep to find `@db.ByteA`, `Bytes` field types
   - List all files using Buffer operations on Bytes fields

2. Find implicit many-to-many relationships
   - Search schema for relation fields without explicit join tables
   - Identify models with `@relation` without `relationName`

3. Locate NotFoundError usage
   - Grep for `NotFoundError` imports and usage
   - Find error handling that checks error class

4. Check for reserved keywords
   - Search schema for models/fields named `async`, `await`, `using`

**Phase 2: Schema Migration**

1. Update reserved keywords in schema
   - Rename any models/fields using reserved words
   - Update all references in application code

2. Generate migration for implicit m-n changes
   - Run `npx prisma migrate dev --name v6-implicit-mn-pks`
   - Review generated SQL for compound primary key changes

**Phase 3: Code Migration**

1. Update Buffer → Uint8Array conversions
   - Replace `Buffer.from()` with TextEncoder
   - Replace `.toString()` with TextDecoder
   - Update type annotations from Buffer to Uint8Array

2. Update NotFoundError handling
   - Replace error class checks with P2025 code checks
   - Use `isPrismaClientKnownRequestError` type guard

3. Test all changes
   - Run existing tests
   - Verify Bytes field operations
   - Confirm error handling works correctly

**Phase 4: Validation**

1. Run TypeScript compiler
   - Verify no type errors remain
   - Check all Buffer references resolved

2. Run database migrations
   - Apply migrations to test database
   - Verify compound PKs created correctly

3. Runtime testing
   - Test Bytes field read/write operations
   - Verify error handling catches not-found cases
   - Confirm implicit m-n queries work
</workflow>

## Quick Reference

**Breaking Changes Summary:**

| Change | Before | After |
|--------|--------|-------|
| Buffer API | `Buffer.from()`, `.toString()` | `TextEncoder`, `TextDecoder` |
| Error Handling | `error instanceof NotFoundError` | `error.code === 'P2025'` |
| Implicit m-n PK | Auto-increment `id` | Compound PK `(A, B)` |
| Reserved Words | `async`, `await`, `using` allowed | Must use `@map()` |

**Migration Command:**
```bash
npx prisma migrate dev --name v6-upgrade
```

**Validation Commands:**
```bash
npx tsc --noEmit
npx prisma migrate status
npm test
```

<constraints>
## Migration Guidelines

**MUST:**
- Backup production database before migration
- Test migration in development/staging first
- Review auto-generated migration SQL
- Update all Buffer operations to TextEncoder/TextDecoder
- Replace all NotFoundError checks with P2025 code checks
- Run TypeScript compiler to verify no type errors

**SHOULD:**
- Create helper functions for common error checks
- Use `@map()` when renaming reserved keywords
- Document breaking changes in commit messages
- Update team documentation about Prisma 6 patterns

**NEVER:**
- Run migrations directly in production without testing
- Skip TypeScript compilation check
- Leave Buffer references in code (causes type errors)
- Use NotFoundError (removed in Prisma 6)
- Use `async`, `await`, `using` as model/field names without `@map()`
</constraints>

<validation>
## Post-Migration Validation

After completing migration:

1. **TypeScript Compilation:**
   - Run: `npx tsc --noEmit`
   - Expected: Zero type errors
   - If fails: Check remaining Buffer references, NotFoundError usage

2. **Database Migration Status:**
   - Run: `npx prisma migrate status`
   - Expected: All migrations applied
   - If fails: Apply pending migrations with `npx prisma migrate deploy`

3. **Runtime Testing:**
   - Test Bytes field write/read cycle
   - Verify error handling catches P2025 correctly
   - Test implicit m-n relationship queries
   - Confirm no runtime errors in production-like environment

4. **Performance Check:**
   - Verify query performance unchanged
   - Check connection pool behavior
   - Monitor error rates in logs

5. **Rollback Readiness:**
   - Document rollback steps
   - Keep Prisma 5 migration snapshot
   - Test rollback procedure in staging
</validation>

## References

For detailed migration guides and examples:

- **Breaking Changes Details**: See `references/breaking-changes.md` for complete API migration patterns, SQL examples, and edge cases
- **Migration Examples**: See `references/migration-examples.md` for real-world migration scenarios with before/after code
- **Migration Checklist**: See `references/migration-checklist.md` for step-by-step migration tasks
- **Troubleshooting Guide**: See `references/troubleshooting.md` for common migration issues and solutions

For framework-specific migration patterns:
- **Next.js Integration**: Consult Next.js plugin for App Router-specific Prisma 6 patterns
- **Serverless Deployment**: See CLIENT-serverless-config skill for Prisma 6 + Lambda/Vercel

For error handling patterns:
- **Error Code Reference**: See TRANSACTIONS-error-handling skill for comprehensive P-code handling
