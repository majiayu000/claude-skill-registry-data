---
name: pr-review
description: Reviews pull requests for correctness, security, performance, and adherence to project conventions.
---

# PR Review Skill

When reviewing a pull request, perform the following checks systematically. Do not skip any section.

## 1. Breaking Changes

- Identify any changes to public APIs, exported types, or interfaces
- Flag removed or renamed functions, classes, or configuration options
- Check for database schema changes that could affect existing data
- Verify backward compatibility or confirm that breaking changes are documented in the PR description
- Check if the version bump (major/minor/patch) matches the scope of changes

## 2. Test Coverage

- Verify that new code paths have corresponding unit tests
- Check that modified code has updated tests reflecting the change
- Look for edge cases that are not covered (null inputs, empty collections, boundary values)
- Confirm integration tests exist for new API endpoints, database operations, or external service calls
- Flag any tests that were removed without clear justification

## 3. Security (OWASP Top 10)

- **Injection**: Check for unsanitized user input in SQL queries, shell commands, or templates
- **Broken Auth**: Verify authentication checks on new endpoints; confirm tokens are validated
- **Sensitive Data**: Ensure no secrets, API keys, or PII are logged or exposed in responses
- **XXE/Deserialization**: Check for unsafe parsing of XML or untrusted serialized data
- **Access Control**: Verify authorization checks; confirm users cannot access other users' data
- **Misconfiguration**: Check for debug modes, verbose error messages, or permissive CORS in production
- **XSS**: Verify all user-supplied content is escaped before rendering in HTML
- **Dependencies**: Check if new dependencies have known vulnerabilities

## 4. Conventional Commits

- Verify commit messages follow the format: `type(scope): description`
- Check that the type matches the change (feat, fix, refactor, docs, test, chore, perf)
- Ensure commit messages are clear, imperative mood, and under 72 characters
- Flag squash-worthy fixup commits (e.g., "fix typo", "address review comments")

## 5. Performance

- Flag N+1 query patterns in database access code
- Check for unnecessary re-renders, re-computations, or memory allocations in hot paths
- Identify missing database indexes for new query patterns
- Look for blocking operations in async contexts
- Check for unbounded collection growth (missing pagination, limits, or size caps)
- Verify caching strategies where appropriate

## 6. Error Handling

- Confirm all error paths return meaningful error messages (without leaking internals)
- Check that exceptions are caught at appropriate levels, not swallowed silently
- Verify that external service calls have timeouts, retries, and circuit breaker patterns
- Ensure validation errors are returned as 400-level responses, not 500s
- Check for proper cleanup in error paths (resource release, transaction rollback)

## 7. Documentation

- Verify public API changes are reflected in API docs, JSDoc/docstrings, or README
- Check that complex business logic has inline comments explaining the rationale
- Confirm changelog is updated for user-facing changes
- Verify migration guides exist for breaking changes

## Output Format

Provide feedback organized by severity:

- **Blockers**: Issues that must be fixed before merge (security, correctness, data loss)
- **Suggestions**: Improvements that would strengthen the code (performance, readability)
- **Nits**: Minor style or preference issues (naming, formatting)
