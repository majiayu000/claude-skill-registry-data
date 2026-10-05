---
name: production-readiness
description: Pre-publish checklist beyond `zbb gate`. Use before opening a release PR or merging to main.
---

# Production readiness

`zbb gate` proves the module **builds, tests, and packages cleanly**. This skill covers what's *not* in the gate but matters before the module hits production: security, observability, documentation, and the "did we leave a footgun" check.

## What `:gate` already checks

If `gate-stamp.json` is committed and `:gateCheck` is green, all of these are already validated:

- `:bundleSpec`, `:generate*` (Gates 1–2)
- `:compile`, `:lint` (Gate 3)
- `:test` (unit + integration in-process — Gate 4a + part of 5)
- `:testDirect` (e2e direct — Gate 5)
- `:testDocker` (e2e docker — Gate 5 for connectors)
- `:buildImage` (Gate 6)
- `gate-stamp.json` itself (Gate 6 / CI's check)

Don't repeat those here. This skill is for the *gaps*.

## Security

- [ ] No plaintext credentials in `src/`, `test/`, fixtures, or README
- [ ] No API tokens, OAuth secrets, or PAT-style strings checked in (scan with `git secrets` or a sweep for `[A-Za-z0-9_]{32,}` strings near "token"/"key"/"secret")
- [ ] No PII in sanitized fixtures — names, emails, phone numbers, addresses replaced with `example.com`-style placeholders (see `@.claude/skills/test-fixtures/SKILL.md`)
- [ ] Error messages don't leak header values, auth tokens, or upstream stack traces
- [ ] `connectionProfile.yml` references the right core profile (`tokenProfile`, `oauthClientProfile`, `basicConnection`, etc.) and doesn't add a custom field that duplicates one already in core
- [ ] OAuth flows: `connectionState.yml` extends `baseConnectionState` and tracks `expiresIn` correctly (the platform's cron uses it for refresh)

## Error handling

- [ ] Producers map HTTP responses to **named** `@zerobias-org/types-core-js` errors:
  - 401 → `InvalidCredentialsError`
  - 403 → `UnauthorizedError`
  - 404 → `NotFoundError`
  - 429 → `RateLimitExceededError`
  - other → `UnexpectedError` with the upstream's status + message
- [ ] No `throw new Error(...)` in `src/` — always a named core type
- [ ] No swallowed errors (try/catch with no rethrow or log)

## Observability

- [ ] No `console.log` / `console.error` in `src/` — use `LoggerEngine.root().get('<Name>')` from `@zerobias-org/logger`
- [ ] Logger names match the module / producer (`getLogger('GithubReposProducer')`, not `'console'`)
- [ ] Debug logging is opt-in via slot `LOG_LEVEL=debug`; default is silent
- [ ] Mapper runtime validation pass already done (see `@.claude/skills/mapper-runtime/SKILL.md`) — any temp `[TEMP-RAW-API]` debug logs removed

## Code quality (beyond `:lint`)

- [ ] No `// @ts-ignore` / `// @ts-expect-error` without a linked bug or comment
- [ ] No `// eslint-disable-next-line` without a one-line reason
- [ ] No commented-out blocks of code
- [ ] No `TODO` / `FIXME` referring to *this PR's* work (move to follow-up issue or finish it)
- [ ] No `!` non-null assertion in `src/` unless the safety is obvious from the surrounding code

## Documentation

- [ ] `README.md` covers:
  - How to obtain credentials (link to the vendor's docs)
  - What scopes / permissions the integration needs
  - At least one operation example with the factory + `connect()`
  - How to run the test modes locally (`zbb test / testDirect / testDocker`)
- [ ] `api.yml` operations have human-readable descriptions sourced from vendor docs (linked, not paraphrased from memory)
- [ ] If the module needs special env vars beyond `zbb env set`, they're listed in the README

## API surface stability

- [ ] No breaking change to an existing operation without a major version bump
- [ ] Schema renames flagged (existing modules may consume the old name)
- [ ] Removed operations require deprecation notice in CHANGELOG (when applicable)

## Performance and resource use

- [ ] No infinite retries on a 4xx
- [ ] Reasonable timeouts on the HTTP client (default to `30000ms` unless the vendor's SLA suggests otherwise)
- [ ] Pagination doesn't accumulate the entire result set in memory if it can stream
- [ ] No N+1 calls in producer methods that should be a single bulk request

## Pre-publish sanity sweep

```bash
cd package/<vendor>/[<suite>/]<service>

# Logger discipline
grep -rn "console\.\(log\|error\|warn\)" src/ \
  && echo "✗ console.* in src/"

# Logger import
grep -rn "from '@zerobias-org/logger'" src/ \
  || echo "warn: no logger imported in src/ (acceptable for tiny utility modules)"

# Error discipline
grep -rn "throw new Error(" src/ \
  && echo "✗ raw Error throws — use core error types"

# Temp debug leftovers
grep -rn "TEMP-RAW-API\|TODO:\|FIXME:\|XXX:" src/ test/ \
  && echo "warn: leftover dev markers"

# Credential leak sweep (heuristic — not exhaustive)
grep -rnE "(api[_-]?key|secret|password|token)\s*[:=]\s*['\"][A-Za-z0-9_-]{16,}" src/ test/ \
  && echo "✗ possible credential leak"

# Docs
grep -q "connect" README.md && grep -q "zbb test" README.md \
  || echo "warn: README missing connect or zbb test instructions"
```

## Sign-off

The module is ready for production when:

- `gate-stamp.json` is committed and `:gateCheck` is green
- Every box above is checked
- The PR description explains *what changed* + *why*, not *how* (the code already shows how)
- A reviewer who hasn't worked on this module can follow the README and connect successfully

## Related

- @.claude/skills/security/SKILL.md — auth flow patterns
- @.claude/skills/error-handling/SKILL.md — which core error to throw
- @.claude/skills/documentation/SKILL.md — what README should cover
- @.claude/skills/readme-template/SKILL.md — README structure
- @.claude/skills/gate-build/SKILL.md — Gate 6 (`zbb gate` + stamp)
- @.claude/skills/completion-checklist/SKILL.md — pre-PR checklist
