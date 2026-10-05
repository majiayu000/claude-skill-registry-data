---
name: testing-core
description: Cross-cutting testing principles for ESM/gradle Hub modules. Use when writing any test, unit or e2e.
---

# Testing core

Principles that apply to both `test/unit/` (nock-mocked) and `test/e2e/` (`describeModule<T>`). Specifics for each live in `unit-testing` and `integration-testing`.

## The split

| Layer        | Lives in         | Network | Credentials       | Runs via                                |
|--------------|------------------|---------|-------------------|-----------------------------------------|
| Unit         | `test/unit/`     | nock    | none              | `zbb test --slot local`                 |
| e2e direct   | `test/e2e/`      | real    | `zbb secret` / `zbb env` | `zbb testDirect --slot local`    |
| e2e docker   | `test/e2e/`      | real    | same              | `zbb testDocker --slot local`           |

The **same `test/e2e/<name>.test.ts`** runs under all three e2e modes. That's the whole point of `describeModule<T>` — the client wrapper varies, the test body doesn't.

## What every test must do

1. **Pass deterministically** — no flakes, no "retry usually fixes it". If a test is flaky, it's broken.
2. **Cover the success path AND at least one error path** — `NotFoundError`, `InvalidCredentialsError`, `RateLimitExceededError`, whichever applies. Use the core error types from `@zerobias-org/types-core-js`.
3. **Use chai** — `mocha + chai` is the framework. `expect(…).to.…` everywhere.
4. **Use ESM imports** — relative imports end in `.js`. Package imports do not.
5. **Skip cleanly** — only at suite level (`before(function () { if (!hasFoo) this.skip(); })`) or test level for known-limited environments (`it('does X', function () { if (!X_AVAILABLE) this.skip(); })`). Never `it.skip(...)` or `describe.skip(...)` as a way to dodge work — that's gone.

## What every test must NOT do

- **Touch the network unmocked from `test/unit/`** — nock should intercept; if it doesn't, fix the mock or the producer URL.
- **Read `process.env` from a test file** — for unit tests, env is irrelevant; for e2e, only `test/e2e/constants.ts` reads it. Everything else imports from there.
- **Hardcode values that should be env-driven** — IDs, organizations, repo names belong in `constants.ts` with sensible defaults.
- **Use mocking libraries other than nock** — no `jest.mock`, no `sinon`, no `fetch-mock`, no `msw`. Only nock, only for unit tests.
- **Modify generated files** — `generated/` and `hub-sdk/generated/` are codegen output. The fix is always in `api.yml` + `:generate`.
- **Skip individual unit tests** — unit tests must always pass. If one's failing, fix the impl or the mock. Skipping is reserved for e2e with missing fixtures.

## Naming & structure

```
test/unit/
├── ConnectionTest.test.ts          # connect/disconnect/isConnected/metadata
├── <Tag1>ProducerTest.test.ts      # per-tag tests
├── <Tag2>ProducerTest.test.ts
└── fixtures/                       # optional, gitignored fixture data
    └── <tag1>.json

test/e2e/
├── constants.ts                    # the only process.env reader in the module
└── <name>.test.ts                  # describeModule<T> skeleton
```

Mocha discovers `**/*.test.ts`. The `.test.ts` suffix is the convention; the generator already uses it.

## Test names: "should …" + behavior

```typescript
// good
it('should retrieve a user by id', async () => { … });
it('should throw NotFoundError when the user does not exist', async () => { … });

// not good
it('test get user', async () => { … });
it('works', async () => { … });
```

Each test name reads as a sentence describing one behavior. Use multiple `it()` cases per `describe()` rather than asserting many unrelated things in one big test.

## Arrange / Act / Assert

Blank lines separate the three phases — no `// Arrange` / `// Act` / `// Assert` comments:

```typescript
it('should get user by id', async () => {
  const userId = 'test-123';

  const result = await userApi.get(userId);

  expect(result).to.have.property('id', userId);
});
```

Comments are reserved for non-obvious things: an API quirk you're testing, an encoding edge case, a known shape difference between docker and direct mode.

## Error assertions: name the core error

```typescript
import { NotFoundError, InvalidCredentialsError, RateLimitExceededError }
  from '@zerobias-org/types-core-js';

try {
  await api.getMissing('id');
  assert.fail('should have thrown');
} catch (e) {
  expect(e).to.be.instanceOf(NotFoundError);
}
```

Generic `expect(e).to.be.instanceOf(Error)` is not enough — the producer is expected to map HTTP failures into specific core error types, and the test exists to lock that mapping in.

## Debug logging in e2e

`@zerobias-org/logger` is the new logger:

```typescript
import { LoggerEngine } from '@zerobias-org/logger';
const logger = LoggerEngine.root().get('<TestName>');

logger.debug('userApi.get(%s)', userId);
const result = await userApi.get(userId);
logger.debug('→ %s', JSON.stringify(result, null, 2));
```

Visible when the slot sets `LOG_LEVEL=debug` (e.g. `zbb env set LOG_LEVEL debug --slot local`). Useful for diagnosing mapper drift; remove the logs once mappers are stable to keep test output clean (or scope to `:debug`).

## Running

```bash
# from the module dir
zbb test       --slot local         # unit tests
zbb testDirect --slot local         # e2e direct (in-process)
zbb testDocker --slot local         # e2e docker (container)
```

CI never runs tests — it validates `gate-stamp.json`, which is what `zbb gate` (run locally) produces. So "running tests in CI" isn't a thing; you commit the stamp.

## Related

- @.claude/skills/unit-testing/SKILL.md — unit test patterns
- @.claude/skills/integration-testing/SKILL.md — e2e patterns
- @.claude/skills/nock-mocking/SKILL.md — nock 14 default-import patterns
- @.claude/skills/test-fixtures/SKILL.md — fixture organization
- @.claude/skills/environment-files/SKILL.md — zbb env / secret
- @.claude/skills/error-handling/SKILL.md — which core error to throw
- @.claude/skills/code-comments/SKILL.md — when comments add value
