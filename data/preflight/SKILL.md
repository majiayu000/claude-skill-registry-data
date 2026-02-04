---
name: preflight
description: Pre-PR check for common issues - run before pushing to catch problems early
---

# Preflight

Run this before creating a PR to catch common issues in changed files.

## Instructions

1. Run `git diff main --name-only` to get list of changed files
2. For each changed file, run the checks below
3. Report issues with `file:line` references
4. Group by category for readability

## Checks

### TypeScript Strict

- [ ] No `any` types - find proper type or use `unknown`
- [ ] No `@ts-ignore` or `@ts-expect-error` without explanation
- [ ] Local interfaces use `Props` not `ComponentNameProps`
- [ ] Type check passes (use `make types` if available, else `pnpm tsc --noEmit`)

```bash
# Check if 'types' target is available in make output
make 2>/dev/null | grep -q 'types' && make types || pnpm tsc --noEmit
```

### React Patterns

- [ ] `'use client'` only where actually needed (hooks, browser APIs, event handlers)
- [ ] Browser-only libs use `dynamic(() => import(...), { ssr: false })`
- [ ] No `console.log` left in code (use proper logging or remove)

### Route Structure

- [ ] Routes have `loading.tsx` with skeleton
- [ ] Routes have `error.tsx` with reset button
- [ ] Page components are server components unless they need client features

### Data Fetching

- [ ] Prisma queries use `select` to specify fields (not bare `findMany()`)
- [ ] No N+1 patterns (queries inside loops)
- [ ] tRPC routers return flat structures

### Validation

- [ ] Zod schemas in `validations/` not inline in components

### Environment Variables

- [ ] No `process.env.*` outside `constants/` directory
- [ ] New env vars added to `.env.example`
- [ ] `NEXT_PUBLIC_` prefix only for client-safe values
- [ ] Server-only secrets not accessed in client components

### Imports

- [ ] Use `@/` path alias (no `../../../` climbs)
- [ ] Barrel exports updated when adding new files

### Dead Code

- [ ] No unused imports
- [ ] No unused variables or parameters
- [ ] No unused functions or components
- [ ] No commented-out code blocks (delete or restore)
- [ ] No unreachable code after return/throw

### Security

- [ ] No hardcoded secrets or API keys
- [ ] No `dangerouslySetInnerHTML` without sanitization
- [ ] No raw SQL queries (use parameterized/Prisma)
- [ ] No sensitive data in console.log or error messages
- [ ] User input validated before use

### Dependency Vulnerabilities

Quick audit check (not full analysis - use `/audit` for that):

```bash
pnpm audit 2>/dev/null | head -20
```

- [ ] No critical/high vulnerabilities in **direct** dependencies
- Transitive/dev-only vulnerabilities: note but don't block (run `/audit` for full analysis)

### Git Hygiene

- [ ] No merge conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
- [ ] No `.only` or `.skip` left in test files
- [ ] No `debugger` statements
- [ ] No `.env.local` or other local config committed
- [ ] No large binary files that shouldn't be in git

### Performance

- [ ] Large objects/arrays use `useMemo` if recreated each render
- [ ] Images have explicit `width` and `height` (prevents layout shift)
- [ ] No synchronous heavy operations in render path
- [ ] Lists over 100 items paginated or virtualized
- [ ] No `useEffect` without dependency array

### Styling

- [ ] Theme-aware colors (`text-muted-foreground`) not hardcoded (`text-gray-500`)
- [ ] Images use `<Image>` from `next/image`

### Dates

- [ ] Use `formatInTimeZone` from `date-fns-tz`, not `format` from `date-fns`
- [ ] Display dates in `facilityTimezone`, store in UTC

### Accessibility

- [ ] Images have `alt` attributes
- [ ] Interactive elements have proper `aria-*` attributes
- [ ] Form inputs have associated labels

### Code Style

- [ ] No semicolons
- [ ] Files end with single newline
- [ ] Empty lines have no whitespace
- [ ] No trailing whitespace

## Output Format

```markdown
## Preflight Report

> Note: Not running test suites (vitest/playwright) - assuming you've run them or will before pushing. CI is the backstop.

### TypeScript (2 issues)
- app/users/page.tsx:15 - `any` type used, consider `User[]`
- components/modal.tsx:8 - uses `UserModalProps` instead of `Props`

### Route Structure (1 issue)
- app/bookings/ - missing loading.tsx

### Imports (1 issue)
- lib/utils.ts:3 - relative import `../../components`, use `@/components`

### Passed
- React Patterns
- Data Fetching
- Validation
- Styling
- Dates
- Accessibility
- Code Style
```

## Severity

Report issues but don't block. Developer decides what to fix. Some checks are style preferences, others are bugs waiting to happen.

**Must fix:** Security issues, merge conflict markers, hardcoded secrets, `.only`/`.skip` in tests
**Should fix:** `any` types, missing error boundaries, N+1 queries, timezone bugs, unused code, performance issues
**Nice to fix:** Naming conventions, import style, semicolons
