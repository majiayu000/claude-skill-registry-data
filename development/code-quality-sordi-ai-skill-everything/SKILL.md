---
name: code-quality
description: Apply when writing or refactoring code. Generic rules to prevent the most common review comments — function length, naming, error handling, security, and tooling.
license: MIT
version: 1.1.0
tokens_target: 1800
triggers:
  - writing code
  - refactoring
  - review
loads_after: []
supersedes: []
---

# Sub-Skill: Code Quality & Common Mistakes
<!-- target: ~1800 tokens (real tiktoken count, see tools/render_readme_table.py) | 28 rules with severity classification -->

**Purpose:** Prevents the 20 % of mistakes that cause 80 % of review comments. Concrete rules from real projects — no boilerplate.

## Rule classification

- **MUST** — load-bearing. Violating causes bugs, security issues, or cross-team confusion. Never break.
- **SHOULD** — default behavior. Deviation needs a documented reason in the code or PR.
- **AVOID** — usually wrong; documented exception inline where needed.

**Where these rules don't strictly apply:** test fixtures, generated code (parser tables, codegen output, schema-derived types), CLI bootstrap scripts, framework adapters, and migration scripts may legitimately differ. The rules below apply to **production code paths** unless an inline exception says otherwise.

---

## Rules

### Functions & Logic

1. **SHOULD: Functions under ~30 lines.** Longer → split where practical. Reduces cognitive load.
2. **AVOID: Boolean as last argument.** `render(true)` is unreadable. Use enum or named-property: `render({ withHeader: true })`.
3. **SHOULD: Early return over nested if-blocks.** Nesting depth > 2 is a warning sign.
4. **SHOULD: No magic numbers.** `if (status === 3)` → `if (status === OrderStatus.SHIPPED)`.
5. **AVOID: Double negation.** `if (!isNotValid)` → `if (isValid)`.

### Variables & Naming

6. **SHOULD: Variable names describe content, not type.** `userList` instead of `arr`, `activeUserId` instead of `id`.
7. **SHOULD: Temporary variables for complex expressions.** `const isEligible = age >= 18 && !isBanned;` instead of cramming it all into an `if`.
8. **AVOID: Abbreviations except established ones** (`id`, `url`, `ctx`, `req`, `res`). `usr`, `cfg`, `tmp` → spell out.

### Error Handling

9. **MUST: Every `async` call needs `try/catch` or `.catch()`.** Unhandled promise rejections crash Node processes.
10. **MUST: Never silently swallow error objects.** `catch (e) {}` is forbidden. At minimum: `logger.warn(e)`.
11. **MUST: Error messages must include context.** `throw new Error('User not found: ' + userId)` not `throw new Error('Not found')`.
12. **SHOULD: Catch specific exception types, not broad categories.** Catch `ConnectionError` not `Exception`. Broad catches mask unrelated bugs and make debugging harder.
13. **SHOULD: Use exponential backoff with jitter for retry logic.** Never retry in a tight loop. Each retry should wait longer than the last with randomization to prevent thundering herds.
14. **MUST: Never retry non-idempotent operations without explicit safeguards.** A retried POST that creates a resource can produce duplicates. Use idempotency keys or check-before-retry patterns.
15. **SHOULD: Propagate errors with context rather than swallowing and re-raising generic exceptions.** Use `raise NewError("context") from original_error` to preserve the chain. Reference: ERR-2026-016.

### Imports & Dependencies

16. **SHOULD: No circular imports.** When in doubt: run `madge --circular src/`.
17. **SHOULD: External dependencies only in dedicated adapter files.** No direct `axios.get()` in business logic — always wrap through an interface.
18. **MUST: Remove `console.log` before commit.** Use a pre-commit hook or linter rule `no-console`. *Exception: debug helpers behind a build-time `__DEV__` flag.*

### Tests

19. **MUST: Every new function needs at least one happy-path test.** No merge without test coverage for new logic. *Exception: pure projection wrappers, single-line getters, and deprecated shims may rely on integration tests.*

### Performance

20. **MUST: No DB queries in loops (N+1 problem).** Instead of `for (item of items) { await db.find(item.id) }` → use a JOIN or `WHERE id IN (...)` query.
21. **MUST: Paginate large datasets.** Never `SELECT * FROM table` without `LIMIT`. API endpoints with lists need `?page=` and `?limit=`.
22. **SHOULD: New `WHERE` clauses need indexes.** Before every new query: is there a matching DB index? Without index → full table scan on growing data.
23. **SHOULD: Lazy loading for heavy operations.** Load data only when needed, not "just in case".

### Security

24. **MUST: Never use user input directly in queries.** Always use prepared statements or ORM query builders. Applies to SQL, NoSQL, shell commands, and template engines.
25. **MUST: New API endpoints need auth.** No endpoint without authentication and authorization — not even "internal" endpoints. *Exception: documented public-asset / health-check routes that explicitly opt out in code comments.*
26. **MUST: Never put secrets in code.** No API keys, passwords, or tokens in source code or comments. Always use environment variables.
27. **MUST: Validate and sanitize user input.** At the system boundary (API entry): check type, length, format. Never trust blindly.

### Tooling & Cross-Platform

28. **MUST: Always prefix `docker run -v` from Git Bash / MSYS on Windows with `MSYS_NO_PATHCONV=1`.** MSYS auto-converts unquoted Linux paths to Windows paths before passing them to `docker.exe`, mangling bind-mount arguments. Use `MSYS_NO_PATHCONV=1 docker run -v "C:/path:/repo" ...` with explicit Windows-style host paths. Reference: `ERR-2026-013`.

---

## Why This Sub-Skill Earns Stars

Without these rules, the agent produces code that works but immediately gets flagged in reviews. With these rules, it writes code that looks like it came from a senior developer — on the first try. The MUST/SHOULD/AVOID classification means rules are followed strictly where they matter (security, error handling) and pragmatically where context matters (function length, lazy loading).
