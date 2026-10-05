---
name: testing_qa
description: Test strategy with actual test infrastructure - integrity gate, test battery, k6 load tests, fixtures.
when_to_use:
  - Adding features or endpoints
  - Refactoring workflows
  - Bug fixes
  - Performance validation
  - Pre-release quality gate
---

# Testing and QA (RESTO BOT)

## Testing layers

### 1. Integrity gate (CI)

- Validates all 54 workflow JSON files in `project/workflows/`
- Checks naming conventions, structure, required fields
- Runs in `integrity-gate.yml` workflow

### 2. Unit tests

- Python tests: `project/tests/` (pytest)
- Pure logic: parsers, validators, mapping functions

### 3. Contract tests

- `/v1` routes: auth, status codes, response shape
- Smoke tests: `project/scripts/smoke_security.sh`
- Gateway behavior: rate limits, method filtering

### 4. Integration tests

- Docker-compose test stack hitting gateway -> n8n
- Test harness: `project/.github/workflows/test-harness.yml`

### 5. Migration tests

- Apply migrations twice; ensure no errors (idempotency)
- Verify schema_migrations tracking

### 6. Load tests

- k6 scripts for throughput validation
- Target: SLO_INBOUND_TO_OUTBOX_P95_MS=2000ms

## Fixtures

- Sample inbound payloads in `project/tests/fixtures/`:
  - WhatsApp webhook (text, audio, image)
  - Instagram webhook
  - Messenger webhook
  - Valid auth, invalid auth, replayed event (idempotency)
  - Large payload boundary

## CI test matrix

```text
integrity-gate -> lint -> python-tests -> integration-tests
  -> docker-build -> security-scan -> frontend-lint
  -> test-harness -> ci-summary
```

## Key files

- `project/tests/` (pytest test suite)
- `project/workflows/` (54 workflow JSON files for integrity gate)
- `project/scripts/smoke_security.sh` (smoke tests)
- `project/.github/workflows/test-harness.yml`
- `project/.github/workflows/integrity-gate.yml`

## Required output

- Test plan + minimal test suite additions
- Smoke tests covering the critical path
- Regression note in PATCHLOG
