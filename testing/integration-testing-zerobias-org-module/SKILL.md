---
name: integration-testing
description: e2e test patterns for ESM/gradle Hub modules — describeModule<T> + hub-sdk. Use when writing test/e2e/*.test.ts files.
---

# e2e tests

e2e tests live in `test/e2e/`. They hit the **real** API through the typed client emitted into `hub-sdk/generated/`, and the same file runs under three modes:

| Mode    | Client behind `client`       | Driver                              | Purpose                                  |
|---------|------------------------------|-------------------------------------|------------------------------------------|
| direct  | `<Class>Impl` in-process     | `zbb testDirect` / `:testDirect`    | Quickest, no container — proves impl works |
| docker  | `<Class>Client` → container  | `zbb testDocker` / `:testDocker`    | Proves the packaged container works      |
| hub     | `<Class>Client` → Hub Server | `zbb testHub` (currently blocked)   | Proves the full Hub plane                |

You write the test **once** with `describeModule<T>`; the runner picks the impl behind `client`.

## Canonical shape

```typescript
import { expect, assert } from 'chai';
import {
  CoreError, NotFoundError, InvalidCredentialsError, IllegalArgumentError,
} from '@zerobias-org/types-core-js';
import { describeModule } from '@zerobias-org/module-test-client';
import type { <Class> } from '../../hub-sdk/generated/api/index.js';
import { <Tag>Api } from '../../hub-sdk/generated/api/index.js';
import { ORG_NAME, TEAM_NAME } from './constants.js';

describeModule<<Class>>('<Class> Module', (client) => {

  describe('<Tag>Api.list<Resource>', () => {
    it('lists resources for an org', async function () {
      if (!ORG_NAME) this.skip();
      const result = await client.get<Tag>Api().list<Resource>(ORG_NAME);
      expect(result).to.be.an('array');
    });

    it('rejects NotFoundError for an unknown org', async () => {
      try {
        await client.get<Tag>Api().list<Resource>('definitely-not-an-org');
        assert.fail('should have thrown');
      } catch (e) {
        expect(e).to.be.instanceOf(NotFoundError);
      }
    });
  });

}, (data) => CoreError.deserialize(data));
```

Five things must be right:

1. **`describeModule<T>` imported from `@zerobias-org/module-test-client`** — never reach for `mocha`'s `describe` directly.
2. **Module type `<Class>` is a type-only import** from `hub-sdk/generated/api/index.js`. The generator template already does this.
3. **Tag APIs are value imports** from the same path (`<Tag>Api`). The test fetches them via `client.get<Tag>Api()`.
4. **`CoreError.deserialize` is the third argument** to `describeModule`. Without it, errors thrown across the wire in docker/hub mode arrive as plain objects instead of `NotFoundError` etc.
5. **All env-driven values come from `./constants.js`** — never `process.env` in the test body.

## constants.ts

`test/e2e/constants.ts` is the only place in the module that reads `process.env`:

```typescript
export const ORG_NAME    = process.env.GITHUB_ORG       ?? 'zerobias-com';
export const TEAM_NAME   = process.env.GITHUB_TEAM      ?? '';
export const REPO_OWNER  = process.env.GITHUB_REPO_OWNER ?? '';
export const REPO_NAME   = process.env.GITHUB_REPO_NAME  ?? '';
```

Each constant gets a default or an empty string. Tests that require a non-empty value skip with `this.skip()`. That's the design pattern: same test file passes everywhere, regardless of which fixtures a particular slot has.

```typescript
it('inspects the configured repo', async function () {
  if (!REPO_OWNER || !REPO_NAME) this.skip();
  // ... real test
});
```

Set values via `zbb env set <NAME> <value> --slot local`. See `@.claude/skills/environment-files/SKILL.md` for the credential side (`zbb secret create`).

## Connection coverage

Connection lifecycle is covered by `describeModule<T>` itself — the wrapper calls `connect()` before each test using credentials pulled from the slot's secret. You generally don't need an explicit `ConnectionTest.test.ts` in `test/e2e/`. If a module wants to assert specific connect-time behavior (e.g. token refresh), do it as a normal test in the main e2e file.

Unit tests *do* have a `ConnectionTest.test.ts` because they exercise the lifecycle methods directly with nock mocks. e2e doesn't need that.

## Logging

`@zerobias-org/logger` works the same way as in unit tests:

```typescript
import { LoggerEngine } from '@zerobias-org/logger';
const logger = LoggerEngine.root().get('<Tag>Test');

logger.debug('list<Resource>(%s)', ORG_NAME);
const result = await client.get<Tag>Api().list<Resource>(ORG_NAME);
logger.debug('→ %s', JSON.stringify(result, null, 2));
```

Visible when `LOG_LEVEL=debug` is set on the slot. Helpful for diagnosing mapper drift; remove or tone down once mappers are stable.

## Suite-level setup / teardown

If a test needs to **create** state before running (e.g. a temporary repo), use `before` / `after` hooks inside `describeModule`:

```typescript
describeModule<<Class>>('<Class> Module', (client) => {
  let tempId: string;

  before(async function () {
    if (!REPO_OWNER) this.skip();
    const created = await client.get<Tag>Api().create<Resource>({ name: 'tmp-e2e' });
    tempId = created.id;
  });

  after(async () => {
    if (tempId) await client.get<Tag>Api().delete<Resource>(tempId);
  });

  // ... tests
});
```

Hooks share the same `client` and the same skip semantics.

## When direct passes but docker doesn't

The most common cause is the container reading something at startup that isn't in the slot's env. Either:

- Move the read into `connect()` so the container picks it up at request time, or
- Set the env on the slot via `zbb env set …`

`zbb testDocker` builds the image from `dist/` and runs it; if the impl works in `testDirect` but fails in `testDocker`, the gap is almost always environment, not logic.

## When all tests skip

Either no env is set on the slot, or `constants.ts` defaults are empty. `zbb env list --slot local` to confirm; `zbb env set <NAME> <value>` to fix.

## What to avoid

- **No `dotenv` import anywhere** — gone. zbb manages env state.
- **No `test/integration/` directory** — gone. e2e is one layout.
- **No raw `process.env`** outside `constants.ts`.
- **No nock in e2e** — these tests hit real APIs. nock belongs in `test/unit/`.
- **No client construction inside the test** — `client` comes from `describeModule`. Calling `new<Class>()` yourself defeats the multi-mode plumbing.
- **No `import * as nock`** (it's only in unit tests anyway, but worth saying explicitly).

## Validation

```bash
test -f test/e2e/constants.ts \
  && grep -q "describeModule" test/e2e/*.test.ts \
  && echo "✓ e2e layout"

grep -rn "process\.env" test/e2e/ | grep -v "/constants.ts:" \
  && echo "✗ process.env outside constants.ts"

grep -rn "from 'nock'" test/e2e/ \
  && echo "✗ nock in e2e"

test -d test/integration \
  && echo "✗ test/integration/ exists — delete it"

grep -rn "CoreError\.deserialize" test/e2e/ >/dev/null \
  || echo "warn: pass CoreError.deserialize as 3rd arg to describeModule"

grep -rnE "from '\.\.?\/[^']*'" test/e2e/ | grep -v "\.js'" \
  && echo "✗ ESM imports missing .js extension"
```

## Running

```bash
zbb testDirect --slot local       # in-process — start here
zbb testDocker --slot local       # container — validate packaging
# zbb testHub --slot local        # full stack — currently blocked
```

`zbb testDirect` and `zbb testDocker` proxy directly to the underlying gradle tasks.

## Related

- @.claude/skills/testing-core/SKILL.md — cross-cutting principles
- @.claude/skills/environment-files/SKILL.md — `zbb env` / `zbb secret`
- @.claude/skills/error-handling/SKILL.md — core errors to assert against
- @.claude/skills/gate-integration-tests/SKILL.md — Gate 4b checklist
- @.claude/skills/gate-test-execution/SKILL.md — Gate 5
