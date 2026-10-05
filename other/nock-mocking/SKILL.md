---
name: nock-mocking
description: Nock 14 HTTP mocking patterns for ESM unit tests. Use when intercepting HTTP in test/unit/ or writing reusable mock fixtures.
---

# Nock for ESM unit tests

`nock` is the only HTTP-mocking library used in this repo's unit tests. Under nock 14 + ESM + `tsx/esm`, the import is `default`, not `* as`:

```typescript
import nock from 'nock';     // YES
// import * as nock from 'nock';   // NO — gives "nock is not a function"
```

This file documents the patterns that come up regularly. The unit-testing skill covers the surrounding test structure; this file is just about nock.

## Cleanup hook

Set this at the top of every unit test file (or once in `Common.ts`):

```typescript
import nock from 'nock';

afterEach(() => {
  nock.cleanAll();
});
```

Without it, an unconsumed mock from one test will satisfy a later test's request and you'll never notice.

## Basic GET

```typescript
nock('https://api.example.com')
  .get('/users/123')
  .reply(200, { id: '123', name: 'Jane' });

const user = await api.getUsersApi().getUser('123');
expect(user.id).to.equal('123');
expect(nock.pendingMocks()).to.be.empty;       // mock was consumed
```

`nock.pendingMocks()` empty at the end of the test is the strongest possible signal that the producer hit exactly the URL you mocked.

## POST with body matcher

```typescript
nock('https://api.example.com')
  .post('/users', { name: 'Jane', email: 'j@example.com' })
  .reply(201, { id: 'u_1', name: 'Jane', email: 'j@example.com' });

const created = await api.getUsersApi().createUser({
  name: 'Jane',
  email: 'j@example.com',
});
```

Match a partial body with a function:

```typescript
nock('https://api.example.com')
  .post('/events', (body) => body.kind === 'login')
  .reply(204);
```

## Query strings

Nock is exact-matching unless you tell it otherwise:

```typescript
nock('https://api.example.com')
  .get('/users')
  .query({ page: 1, per_page: 50 })
  .reply(200, []);

// allow any query:
nock('https://api.example.com')
  .get('/users')
  .query(true)
  .reply(200, []);
```

## Headers

If the producer must send a particular header, scope the mock to it:

```typescript
nock('https://api.example.com', {
  reqheaders: { authorization: /^Bearer .+/ },
})
  .get('/me')
  .reply(200, { id: 'u_1' });
```

Use this sparingly — header assertions are useful for auth tests but become a maintenance burden everywhere else.

## Error responses

```typescript
nock('https://api.example.com')
  .get('/users/999')
  .reply(404, { error: 'not_found' });

try {
  await api.getUsersApi().getUser('999');
  assert.fail('should have thrown');
} catch (e) {
  expect(e).to.be.instanceOf(NotFoundError);
}
```

Use the **core error types** from `@zerobias-org/types-core-js` — `NotFoundError`, `InvalidCredentialsError`, `RateLimitExceededError`, `UnexpectedError`. Asserting against generic `Error` is too loose to lock in producer behavior.

## Multiple sequential responses

For pagination tests:

```typescript
nock('https://api.example.com')
  .get('/users').query({ page: 1 }).reply(200, [{ id: 'u_1' }], { Link: '<...>; rel="next"' })
  .get('/users').query({ page: 2 }).reply(200, [{ id: 'u_2' }]);

const users = await api.getUsersApi().listUsers();
expect(users).to.have.length(2);
```

Or `.times(N)` for the same mock used N times:

```typescript
nock('https://api.example.com')
  .get('/me')
  .times(3)
  .reply(200, { id: 'u_1' });
```

## Reusable fixture helpers

When a mock appears in many tests, factor it:

```typescript
// test/unit/fixtures/userMocks.ts
import nock from 'nock';
import userFixture from './user-123.json' with { type: 'json' };

export function mockGetUser(id = '123') {
  return nock('https://api.example.com')
    .get(`/users/${id}`)
    .reply(200, userFixture);
}
```

Tests use them as:

```typescript
import { mockGetUser } from './fixtures/userMocks.js';

it('reads a user', async () => {
  mockGetUser();
  const u = await api.getUsersApi().getUser('123');
  expect(u.id).to.equal(userFixture.id);
});
```

## Debugging unmatched requests

When a test fails with a real HTTP error rather than a nock match, the producer hit a URL no mock covered. To find what it hit:

```typescript
nock.emitter.on('no match', (req) => {
  // eslint-disable-next-line no-console
  console.error('nock no-match:', req.method, req.path, req.headers);
});
```

(Or just rely on `nock.pendingMocks()` and the failed-test stack trace — for most cases that's enough.)

## What not to do

- **`import * as nock from 'nock'`** — nock 14 default-import only. The wildcard form silently breaks.
- **`nock.disableNetConnect()`** as a global default — fine in CI, but it makes local debugging awkward when you want to compare against the real API. Prefer `nock.cleanAll()` after each test.
- **Mocking inside `before()` once for the whole suite** — when a test mutates the mock state, the next test inherits a half-consumed mock. Mock fresh in each `it()` or each `beforeEach()`.
- **Asserting on `nock.isDone()`** — it's true only if *every* mock you set up was consumed *and* nock is in record mode. Use `expect(nock.pendingMocks()).to.be.empty;` instead — more precise, fails cleanly.

## Validation

```bash
# default import everywhere
! grep -rn "import \* as nock" test/unit/

# every test file (or common.ts) cleans up
grep -rn "nock\.cleanAll" test/unit/ >/dev/null \
  || echo "warn: add afterEach(() => nock.cleanAll())"

# only nock, no other mock libs
grep -rnE "jest\.mock|from 'sinon'|fetch-mock|from 'msw'" test/unit/ \
  && echo "✗ non-nock mock library"
```

## Related

- @.claude/skills/unit-testing/SKILL.md — unit test structure
- @.claude/skills/test-fixtures/SKILL.md — fixture organization
- @.claude/skills/testing-core/SKILL.md — chai assertion patterns + core error types
- @.claude/skills/error-handling/SKILL.md — which core error to throw on which HTTP status
