---
name: innozverse-testing-quality
description: Maintain code quality standards including linting, type checking, testing strategies, and code review practices. Use when preparing commits, reviewing code, or setting up quality checks.
---

# innozverse Testing & Quality Standards

Maintain high code quality across the innozverse project.

## Code Quality Checks

### Before Committing
```bash
pnpm lint        # Lint all code
pnpm typecheck   # Type check TypeScript
pnpm format      # Format with Prettier
pnpm build       # Ensure everything builds
```

### CI Checks (GitHub Actions)
- Linting (ESLint)
- Type checking (tsc)
- Building (Turbo)
- Tests (when implemented)

## Testing Strategy (To Be Implemented)

### Unit Tests
- **Packages**: Test shared utilities
- **API**: Test route handlers in isolation
- **Web**: Test components with React Testing Library

### Integration Tests
- **API**: End-to-end endpoint tests
- **Web**: Page-level tests with API mocking

### E2E Tests
- **Web**: Critical user flows
- **Mobile**: Key features on simulators

## Test Naming

```
<name>.test.ts         # Unit tests
<name>.integration.test.ts  # Integration tests
<name>.e2e.test.ts     # E2E tests
```

## Coverage Goals

- Critical paths: 80%+ coverage
- API endpoints: 100% coverage
- Shared utilities: 90%+ coverage

## Type Safety

- Enable TypeScript `strict` mode
- No `any` types without `// @ts-expect-error` comment
- Define all function return types
- Use Zod for runtime validation

## Linting Rules

- ESLint for TypeScript
- `flutter_lints` for Dart
- Prettier for formatting
- No unused variables
- No console.log in production

## Code Review Checklist

- [ ] Tests pass (when implemented)
- [ ] Linting passes
- [ ] Type checking passes
- [ ] No console.log or debugger statements
- [ ] Error handling present
- [ ] Environment variables documented
- [ ] Types exported from @innozverse/shared
- [ ] API endpoints versioned

## Git Hooks (Future)

- Pre-commit: Run lint + typecheck
- Pre-push: Run tests
- Commit message: Validate conventional commits

## Monitoring (Future)

- Sentry for error tracking
- Analytics for usage metrics
- Performance monitoring
- Uptime monitoring for API
