---
name: setup-agent-code-style-strict
description: >-
  Add TypeScript strict-mode code-style rules to AGENTS.md. The rule text ships
  inside this skill, so write it from here, not from memory. Use when the user
  asks for strict-mode style rules. Not for Deno projects (use
  setup-agent-code-style-deno).
---

## Purpose
Integrates TypeScript strict mode coding standards into AGENTS.md.

## Prerequisites
- AGENTS.md must exist in project root
- Project uses TypeScript with strict mode

## Injection Location
Add code style rules to AGENTS.md after the "Project tooling Stack" section, before "Architecture".

## Code Style Rules (to inject)

```markdown
## Code Style (TypeScript Strict Mode)

### General Principles
- NO FALLBACKS/HACKS WITHOUT EXPLICIT REQUEST. "FAIL FAST, FAIL CLEARLY."
- USE TYPED CONSTANTS/ENUMS INSTEAD OF MAGIC NUMBERS/STRINGS
- FUNCTIONS ≤100 LINES; BREAK COMPLEX LOGIC INTO HELPERS
- TREAT LINTER/COMPILER WARNINGS AS ERRORS
- MAIN/EXPORTED FUNCTIONS FIRST, AUXILIARIES LAST
- PARAMETER STYLE: `{ REQUIRED, OPTIONAL = "DEFAULT" }`
- DOCUMENT ALL FILES AND FUNCTIONS WITH TSDOC
- TESTABILITY IS MORE IMPORTANT THAN PERFORMANCE AND ENCAPSULATION
- CODE ORDER IN FILES: imports, constants, types, interfaces, classes, main, public functions, private functions, tests

### TypeScript
- Strict mode (`strict: true`)
- Avoid nested ternary operators; prefer `if/else` chains or `switch` for multiple conditions
- Interfaces > types for objects
- Union types over enums for simple cases
- Pass all class dependencies via constructors or factory methods
- Pass dependencies for specific method calls via method parameters
- Prioritize pure functions for business logic; separate state mutation from logic
- Enforce immutability: use `readonly`, `Readonly<T>`, and `ReadonlyArray<T>`
- Avoid `any`; use `unknown` for truly unknown types
- Use utility types (`Partial`, `Pick`, etc.)
- Don't use index files to import modules
- Use strong inline type style for parameters:

```ts
export async function fetchData(
  {
    url,
    method = 'GET',
    retries = 3,
    requestData,
  }: Readonly<{
    url: string;
    method?: 'GET' | 'POST';
    retries?: number;
    requestData: RequestData;
  }>
): Promise<readonly ResponseData[]> {
  // ...
}
```

### Testing
- Don't change prod code to pass tests
- Unit tests for pure functions
- Integration tests for interactions
- E2E for critical flows
- Given-When-Then test names
- Test errors/edge cases; mock dependencies
- Target 60% coverage
- Keep a test pyramid (~70% unit, ~25% integration, ≤5% e2e)
- Behavior-first tests; avoid locking to internals
- Co-locate tests next to source (*.test.ts); keep fixtures in __fixtures__
- Fail fast on unhandledRejection/console.error
- Deterministic time/IDs/randomness; no wall-clock dependencies
- Use fake timers deliberately; avoid arbitrary sleeps
- Include negative paths (validation, auth, limits, idempotency, duplicate updates)
- Split unit/integration in CI; publish coverage reports

### File Organization
- Feature-based folders
- Separate concerns: services, adapters, utils, types, tests
- Shallow structure (≤3 levels)
- Consistent naming

### Documentation
- TSDoc for public APIs (params, returns, exceptions, examples)
- English comments only
- Intent/invariants when code unclear; no redundant comments
- Document complex logic/architecture
- Updated READMEs; inline comments for non-obvious code

### Performance
- Avoid synchronous heavy CPU on request path; offload to workers
- Use caches for repeated computations where safe
- Apply circuit breakers/timeouts for external I/O

### Security
- Input validation/sanitization
- Secure secrets via env vars; never hardcode tokens/keys
- Avoid logging secrets/PII; scrub identifiers in error logs
- Limit file sizes/types for uploads; scan where applicable
- Keep dependencies updated regularly
```

## Workflow
- [ ] Read project AGENTS.md
- [ ] Locate "Architecture" section
- [ ] Insert code style rules before "Architecture"
- [ ] Verify proper markdown formatting
- [ ] No duplicate sections
