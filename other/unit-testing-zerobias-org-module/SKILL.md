---
name: unit-testing
description: Unit test patterns for ESM/gradle Hub modules. Use when writing test/unit/*.test.ts files.
---

# Unit tests

Unit tests live in `test/unit/`. They mock HTTP with nock, run without credentials, work offline, and finish fast. `zbb test --slot local` runs them.

## Shape of a unit test file

```typescript
import { expect, assert } from 'chai';
import nock from 'nock';
import { Email, NotFoundError, InvalidCredentialsError }
  from '@zerobias-org/types-core-js';
import { new<Class> } from '../../src/index.js';

describe('<Tag>Producer', () => {
  afterEach(() => nock.cleanAll());

  describe('get<Resource>', () => {
    it('should retrieve a <resource> by id', async () => {
      nock('https://api.example.com')
        .get('/<resource>/123')
        .reply(200, { id: '123', name: 'Foo' });

      const api = new<Class>();
      await api.connect({ apiToken: 'x' });
      const result = await api.get<Tag>Api().get<Resource>('123');

      expect(result).to.have.property('id', '123');
      expect(nock.pendingMocks()).to.be.empty;
    });

    it('should throw NotFoundError when the <resource> does not exist', async () => {
      nock('https://api.example.com')
        .get('/<resource>/999')
        .reply(404, { error: 'not_found' });

      const api = new<Class>();
      await api.connect({ apiToken: 'x' });

      try {
        await api.get<Tag>Api().get<Resource>('999');
        assert.fail('should have thrown');
      } catch (e) {
        expect(e).to.be.instanceOf(NotFoundError);
      }
    });
  });
});
```

Notes baked into the shape above:

- **`import nock from 'nock'`** — default import for nock 14 / ESM. The `import * as nock` form does not work.
- **`from '../../src/index.js'`** — relative imports always end in `.js`, even though the source is `.ts`.
- **`afterEach(() => nock.cleanAll())`** — prevents cross-test mock leakage. Use this at suite level or inside each `describe()`.
- **`nock.pendingMocks()`** — at the end of a test, this should be empty. If it's not, a mock you set up wasn't consumed, which usually means the producer URL didn't match.
- **Use core error types** — `NotFoundError`, `InvalidCredentialsError`, `RateLimitExceededError`, `UnexpectedError`. Plain `Error` assertions don't lock in the producer's error mapping.

## Optional `test/unit/Common.ts`

When most tests share the same setup (connect + mocks), factor it out:

```typescript
import nock from 'nock';
import { new<Class> } from '../../src/index.js';
import type { <Class> } from '../../src/index.js';

export async function newConnectedClient(): Promise<<Class>> {
  nock('https://api.example.com')
    .post('/auth/login')
    .reply(200, { accessToken: 'test-token' });

  const api = new<Class>();
  await api.connect({ apiToken: 'test-token' });
  return api;
}
```

`Common.ts` is conventional but not auto-scaffolded. Only add it when the duplication is real. Never read `process.env` from it.

## Connection tests

Every connector module should have `test/unit/ConnectionTest.test.ts` covering:

- happy connect (200 → state set, `isConnected()` true)
- failed connect (401 → `InvalidCredentialsError`)
- `isConnected()` false before `connect()`
- `disconnect()` clears state, `isConnected()` becomes false
- `metadata()` returns a shape with `status`

This is the minimum that proves the lifecycle methods aren't lying.

## Producer tests

One file per `<Tag>Api` from the generated interface. For each operation:

- happy path with a representative response body
- one error path (404, 429, or 401 as appropriate)
- if the operation paginates: a multi-page test that verifies all pages are consumed

For mappers, the test should assert against shaped data, not just type:

```typescript
expect(result).to.deep.equal({
  id: '123',
  email: 'a@example.com',
  createdAt: new Date('2025-01-01T00:00:00Z'),
});
```

Use `deep.equal` (not just property checks) when the mapper has many fields — that catches missing fields *and* wrong field names in one assertion.

## Fixtures

Real, sanitized API responses live in `test/unit/fixtures/` (gitignored or committed as appropriate). Strip all PII before committing:

| Real           | Sanitized            |
|----------------|----------------------|
| `j.doe@google.com` | `user@example.com` |
| `Jane Doe`     | `Jane Doe`           |
| `4111 1111 …`  | `4111111111111111`   |
| API keys       | `test-token-xxx`     |
| Stripe IDs     | `cus_test_xxx`       |

Import them as plain objects:

```typescript
import userFixture from './fixtures/user-123.json' with { type: 'json' };

nock('https://api.example.com')
  .get('/users/123')
  .reply(200, userFixture);
```

(For modules where `import X from 'foo.json'` doesn't work under tsx/esm, use `await import` or read the file via `node:fs` — but the assertion clause stays the same.)

## What to avoid

- **`jest.mock`, `sinon`, `fetch-mock`, `msw`** — only nock. Mock at the HTTP boundary, not at the class boundary.
- **Mocking the module's own internal `Client` class** — that hides the bug you're trying to catch. Mock the upstream API instead.
- **Asserting against `typeof`** — `expect(typeof x.id).to.equal('string')` is too weak. Use `expect(x.id).to.equal('expected-id')` or `expect(x.id).to.be.instanceOf(UUID)`.
- **Tests that pass without `nock.cleanAll()`** — they'll still pass, then suddenly fail in CI when test order changes. Add the cleanup.

## Validation

```bash
ls test/unit/*.test.ts >/dev/null && echo "✓ unit tests present"

grep -hn "import nock" test/unit/*.test.ts
# Each match should be `import nock from 'nock';` — no `* as nock`.

grep -hnE "from '\.\.?\/[^']*'" test/unit/ | grep -v "\.js'"
# Should print nothing.

grep -hnE "jest\.mock|from 'sinon'|fetch-mock|from 'msw'" test/unit/
# Should print nothing.

grep -hn "process\.env" test/unit/
# Should print nothing.

grep -hn "nock\.cleanAll" test/unit/*.test.ts
# Should print at least one match (afterEach hook).
```

## Related

- @.claude/skills/testing-core/SKILL.md — cross-cutting principles
- @.claude/skills/nock-mocking/SKILL.md — nock-specific patterns
- @.claude/skills/test-fixtures/SKILL.md — fixture organization
- @.claude/skills/error-handling/SKILL.md — which error to throw
- @.claude/skills/gate-unit-tests/SKILL.md — Gate 4a checklist
