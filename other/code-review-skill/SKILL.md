---
description: Full code review — type safety, naming, security, project standards, and form validation coverage. Use after significant changes before considering a task done.
disable-model-invocation: true
argument-hint: <scope, e.g. "apps/backend/admin-api/src/modules" or "recent changes">
---

# Code Review: $ARGUMENTS

## Files to review

!`git diff --name-only HEAD~1 2>/dev/null | grep -E '\.(ts|html)$' || find $ARGUMENTS -name "*.ts" -o -name "*.html" 2>/dev/null | head -30`

## Blockers (must fix before merge)

- `any` type used anywhere
- Hardcoded secret, API key, tenant/client ID, or connection string
- Auth bypass via query param, header, or env flag
- Empty `catch` block
- Unused variables or imports
- `HttpClient` injected directly into an Angular component instead of via `ApiClientService`
- `localStorage` used for a token
- `alert()` or `confirm()` in frontend code
- Reliance on native HTML form validation attributes instead of Angular `Validators`
- AJV or Zod used anywhere on the backend — `class-validator` only
- DTO defined as a plain interface instead of a `class-validator`-decorated class
- `as` cast used to silence a type error
- `@ts-ignore` or `@ts-expect-error`
- Angular `Validators` failure shown as a toast instead of an inline field error
- Server 400/409/500 shown as an inline field error instead of `serverError`/toast
- `class-validator` DTO missing a decorator on a field that's required in the Prisma model
- DTO `@MaxLength`/`@Min` not matching the Prisma `@db.VarChar(N)`/type constraint
- `@unique` field returning 400 on duplicate instead of 409
- TypeScript errors present in the package
- Prisma model using `@default(uuid())` or a scalar list field (`String[]`) — unsupported/inconsistent on this MySQL project

## Warnings (should fix)

- Class method missing an explicit access modifier
- Constructor dependency not `private readonly`
- Async function missing error handling
- `unknown` narrowed without a type guard
- Hardcoded API URL or port number
- Missing loading, error, or empty state on a frontend data page
- Backend service missing `/health` or `/health/ready`
- List query missing Prisma `select`

## Naming check

| Element | Expected convention |
|---|---|
| Variables / functions / methods | `camelCase` |
| Classes | `PascalCase` |
| Interfaces | `PascalCase`, no `I` prefix except accepted domain-entity interfaces |
| Module / controller / DTO files | `kebab-case` |
| DB tables / columns | `snake_case` |
| Prisma model names | `PascalCase` singular |
| Angular components | `PascalCase` class, `kebab-case` filename |
| Angular constants | `UPPER_SNAKE_CASE` |

## Security spot-check

- MSAL Bearer validation via `AzureAuthGuard`, consistently applied
- `@nestjs/throttler` rate limiting on sensitive routes
- Helmet registered in every service's `main.ts`
- `class-validator` + global `ValidationPipe` validates before controller logic
- No PII in logs

## TypeCheck command

```bash
pnpm --filter <package-name> typecheck
```

A review is not complete if type errors are present.

## Output format

**Blockers:** [list with file + line]
**Warnings:** [list with file + line]
**Suggestions:** [list]
**Verdict:** Pass / Needs fixes
