---
name: gate-unit-tests
description: Gate 4 (unit half) — test/unit/ contains nock-mocked tests covering happy and error paths for every producer. Use after Gate 3, before running tests.
---

# Gate 4a: Unit tests

Unit tests live in `test/unit/` and mock HTTP with nock. They must run cleanly without any network, credentials, or external state. `zbb test --slot local` invokes them.

The generator scaffolds `test/unit/.gitkeep` only — the actual test files are written during this gate. `test/unit/Common.ts` is conventional but not auto-scaffolded.

## What to check

```bash
# 1. Unit test files exist
ls test/unit/*.test.ts >/dev/null 2>&1 \
  || { echo "✗ no test/unit/*.test.ts files"; exit 1; }

FILES=$(ls test/unit/*.test.ts | wc -l)
echo "✓ $FILES unit test file(s)"

# 2. Test structure
DESCRIBES=$(grep -hcE "^\s*describe\(" test/unit/*.test.ts | awk '{s+=$1} END {print s}')
ITS=$(grep -hcE "^\s*it\(" test/unit/*.test.ts | awk '{s+=$1} END {print s}')
[ "$DESCRIBES" -ge 1 ] && [ "$ITS" -ge 3 ] \
  || { echo "✗ need at least 1 describe and 3 it cases (found $DESCRIBES describe / $ITS it)"; exit 1; }

# 3. nock 14 ESM default import — `import nock from 'nock'` (not `import * as nock`)
grep -rn "import \* as nock" test/unit/ \
  && { echo "✗ wildcard nock import (nock 14 needs default import)"; exit 1; }
grep -rn "^import nock from 'nock';" test/unit/ >/dev/null \
  || echo "warn: no nock import found — confirm tests don't hit the network"

# 4. No forbidden mock libraries
grep -hnE "jest\.mock|from ['\"]sinon['\"]|fetch-mock|from ['\"]msw['\"]" test/unit/ \
  && { echo "✗ forbidden mock library — only nock is allowed"; exit 1; }

# 5. No env or credentials in unit tests
grep -rn "process\.env" test/unit/ 2>/dev/null \
  && { echo "✗ process.env in unit tests — unit tests run with no env"; exit 1; }
grep -rn "from 'dotenv'" test/unit/ 2>/dev/null \
  && { echo "✗ dotenv import — unit tests don't use .env"; exit 1; }

# 6. No real-API surface in unit imports
grep -rnE "from 'axios'|new XMLHttpRequest" test/unit/ 2>/dev/null
# Should print nothing. Producers consume axios internally; tests intercept via nock.

# 7. nock cleanup hook present
grep -rn "nock\.cleanAll\|nock\.restore" test/unit/ >/dev/null \
  || echo "warn: no nock.cleanAll() — add an afterEach() to prevent test cross-talk"

# 8. ESM imports — relative imports end in .js
grep -rnE "from '\.\.?\/[^']*'" test/unit/ | grep -v "\.js'" \
  && { echo "✗ test/unit/ imports missing .js extension"; exit 1; }

# 9. Tests target the real exports
grep -rnE "from '\.\.?\/(\.\.?\/)*src/index\.js'" test/unit/ >/dev/null \
  || echo "warn: tests don't import the module factory from src/index.js"

# 10. Error scenarios present (401/404/429/etc.)
grep -rnE "InvalidCredentialsError|NoSuchObjectError|RateLimitExceededError|UnexpectedError" test/unit/ >/dev/null \
  || echo "warn: no core-error assertions — add at least one error-path test per producer"
```

## Pass criteria

- At least one file under `test/unit/*.test.ts` and at least 3 `it()` cases total
- nock imported as default (`import nock from 'nock';`) — nock 14 / ESM
- No forbidden mock libraries (jest.mock, sinon, fetch-mock, msw)
- No `process.env`, no `dotenv` — unit tests are hermetic
- Tests import from `src/index.js` (or, when justified, from internal source files)
- Relative imports end in `.js`
- nock cleanup hook present
- At least one error-path test per producer

## Suggested file layout

```
test/unit/
├── ConnectionTest.test.ts        # connect/disconnect/isConnected/metadata
├── <Tag1>ProducerTest.test.ts    # per-tag tests
├── <Tag2>ProducerTest.test.ts
└── fixtures/
    ├── <tag1>.json
    └── <tag2>.json
```

`test/unit/Common.ts` is conventional but not required. When present, it builds an in-process connected client with nock mocks already in place, so individual tests stay small. See `@.claude/skills/unit-testing/SKILL.md` for the canonical shape.

## Running locally

```bash
zbb test --slot local
```

Runs mocha against `test/**/*.test.ts` under `tsx/esm` (configured in `.mocharc.json`). Unit tests should pass with no shell env set.

## On failure

- `nock.restore()`/`disable*Connect` interference between test files — call `nock.cleanAll()` in `afterEach()` and `nock.enableNetConnect()` only when you genuinely need outgoing traffic
- "Got 404 against `https://…`" with a stack trace but no useful matcher — your nock URL doesn't match the producer's URL. Print `nock.pendingMocks()` and `nock.activeMocks()` in `afterEach()` to debug
- Test imports break with `Cannot find module './Foo'` — relative import missing `.js`
- "TypeError: nock is not a function" — wildcard import; switch to `import nock from 'nock'`

## Related

- @.claude/skills/unit-testing/SKILL.md — unit test patterns
- @.claude/skills/nock-mocking/SKILL.md — nock 14 ESM-default-import patterns
- @.claude/skills/testing-core/SKILL.md — general testing principles
- @.claude/skills/test-fixtures/SKILL.md — fixture organization
- @.claude/skills/gate-test-execution/SKILL.md — running and verifying
