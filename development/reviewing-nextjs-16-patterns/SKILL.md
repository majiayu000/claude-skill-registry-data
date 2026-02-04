---
name: reviewing-nextjs-16-patterns
description: Review code for Next.js 16 compliance - security patterns, caching, breaking changes. Use when reviewing Next.js code, preparing for migration, or auditing for violations.
allowed-tools: Read, Glob, Grep, TodoWrite
version: 1.0.0
review: true
---

# Next.js 16 Patterns Review

Comprehensive review for Next.js 16 compliance covering security vulnerabilities, caching patterns, breaking changes, and migration readiness.

## Review Process

For comprehensive security review patterns, use the reviewing-security skill from the review plugin. For dependency auditing, use the reviewing-dependencies skill from the review plugin.

### 1. Security Audit

**CVE-2025-29927 - Server Action Authentication**

Check all Server Actions for proper authentication:

```bash
# Find all Server Actions
grep -r "use server" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx"
```

For each Server Action verify:

- [ ] Authentication check at function start
- [ ] Authorization validation before data access
- [ ] No reliance on client-side validation only
- [ ] Proper error handling without leaking sensitive data

**Middleware Security**

```bash
# Find middleware files
find . -name "middleware.ts" -o -name "middleware.js"
```

Verify:

- [ ] Authentication logic present in middleware
- [ ] Protected routes defined in config.matcher
- [ ] No authentication logic removed in Next.js 16 migration
- [ ] Proper redirect handling for unauthorized access

**Server Component Data Access**

```bash
# Find async Server Components
grep -r "export default async function" app/
```

Check each Server Component:

- [ ] Session validation before data queries
- [ ] User context verified before personalized data
- [ ] No direct database queries without auth checks
- [ ] Proper error boundaries for auth failures

### 2. Caching Patterns

**use cache Adoption**

```bash
# Find fetch calls that should use cache
grep -r "fetch(" --include="*.ts" --include="*.tsx"
# Find functions that should be cached
grep -r "export async function" --include="*.ts"
```

Verify:

- [ ] `use cache` directive for cacheable functions
- [ ] Proper cache tags with `cacheTag()` for revalidation
- [ ] Cache lifecycle control with `cacheLife()`
- [ ] No unstable_cache in new code
- [ ] fetch() caching replaced with use cache

**Cache Lifecycle Configuration**

Check for proper cache profiles:

- [ ] `cacheLife('seconds')` for rapidly changing data
- [ ] `cacheLife('minutes')` for moderate update frequency
- [ ] `cacheLife('hours')` for stable content
- [ ] `cacheLife('days')` for rarely changing data
- [ ] `cacheLife('weeks')` for static content
- [ ] Custom profiles defined in next.config.js if needed

**Revalidation Strategy**

```bash
# Find revalidation calls
grep -r "revalidateTag\|revalidatePath" --include="*.ts" --include="*.tsx"
```

Verify:

- [ ] revalidateTag() matches cacheTag() definitions
- [ ] revalidatePath() used for page-level invalidation
- [ ] No orphaned cache tags
- [ ] Proper error handling in revalidation

### 3. Breaking Changes

**Async Request APIs**

```bash
# Find synchronous API usage
grep -r "cookies()\|headers()\|params\|searchParams" --include="*.ts" --include="*.tsx"
```

Check for required async usage:

- [ ] `await cookies()` in Server Components/Actions
- [ ] `await headers()` in Server Components/Actions
- [ ] `await params` in page/layout/route components
- [ ] `await searchParams` in page components
- [ ] React.use() wrapper in Client Components if needed

**Middleware to Proxy Migration**

```bash
# Check for removed middleware patterns
grep -r "NextResponse.rewrite\|NextResponse.redirect" middleware.ts
```

Verify migration:

- [ ] Simple rewrites moved to next.config.js redirects/rewrites
- [ ] Complex logic converted to Middleware Proxies
- [ ] Authentication logic preserved
- [ ] Header manipulation handled correctly

**Route Handler Changes**

```bash
# Find route handlers
find app -name "route.ts" -o -name "route.js"
```

Check each route handler:

- [ ] Dynamic functions require dynamic = 'force-dynamic'
- [ ] No synchronous cookies()/headers() calls
- [ ] Proper TypeScript types for request/params
- [ ] Error handling updated for new patterns

**generateStaticParams Changes**

```bash
# Find static param generation
grep -r "generateStaticParams" --include="*.ts" --include="*.tsx"
```

Verify:

- [ ] Returns array of param objects (not nested)
- [ ] Works with new async params
- [ ] Proper TypeScript types
- [ ] No deprecated patterns

### 4. Migration Verification

**Dependency Updates**

Check package.json:

- [ ] next: ^16.0.0 or higher
- [ ] react: ^19.0.0 or higher
- [ ] react-dom: ^19.0.0 or higher
- [ ] @types/react: ^19.0.0 (if using TypeScript)
- [ ] @types/react-dom: ^19.0.0 (if using TypeScript)

**Configuration Updates**

Check next.config.js:

- [ ] experimental.dynamicIO enabled if using dynamic APIs
- [ ] staleTimes configured if controlling client-side cache
- [ ] Custom cacheLife profiles defined if needed
- [ ] TypeScript config updated for async params

**Build Validation**

Run and verify:

```bash
npm run build
```

- [ ] No deprecation warnings
- [ ] No type errors
- [ ] No runtime errors in build
- [ ] Static generation works correctly
- [ ] Dynamic routes render properly

**Runtime Testing**

- [ ] Authentication flows work correctly
- [ ] Protected routes require login
- [ ] Server Actions validate permissions
- [ ] Cache invalidation triggers updates
- [ ] Dynamic content updates appropriately
- [ ] Static content serves from cache

## Violation Severity

**Critical**

- Missing authentication in Server Actions (CVE-2025-29927)
- Synchronous cookies()/headers() calls
- Security middleware removed or broken

**High**

- Missing cache directives on expensive operations
- Incorrect async params usage
- Broken revalidation strategy

**Medium**

- Using deprecated unstable_cache
- Middleware patterns that should be proxies
- Missing cache lifecycle configuration

**Nitpick**

- Suboptimal cache profiles
- Missing cache tags for fine-grained invalidation
- Legacy fetch caching patterns

## Best Practices

1. **Run security audit first** - Critical vulnerabilities take priority
2. **Group related violations** - Fix all async API issues together
3. **Test incrementally** - Verify each category before moving on
4. **Document decisions** - Record why certain patterns were chosen
5. **Update documentation** - Keep project docs current with Next.js 16 patterns
