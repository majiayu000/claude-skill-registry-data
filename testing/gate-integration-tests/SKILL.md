---
name: gate-integration-tests
description: Gate 4 (e2e half) — test/e2e/ contains describeModule<T> tests using the hub-sdk client, hitting real APIs (and the same suite under direct/docker/hub). Use after Gate 3, before running tests.
---

# Gate 4b: e2e tests

End-to-end tests live in `test/e2e/`. The one file pattern (`<name>.test.ts` + `constants.ts`) is invoked by three runners — direct (in-process), docker (containerized), and hub (full stack) — using `describeModule<T>` from `@zerobias-org/module-test-client`. There is no `test/integration/` directory anymore.

The generator scaffolds:

- `test/e2e/<name>.test.ts` — a `describeModule<T>` skeleton with TODOs
- `test/e2e/constants.ts` — env-var-backed constants (the only place in the module that reads `process.env`)

This gate is about turning the scaffolded skeleton into a real test suite.

## What to check

```bash
# 1. e2e test files exist (generator scaffolds at least one)
ls test/e2e/*.test.ts >/dev/null 2>&1 \
  || { echo "✗ no test/e2e/*.test.ts files"; exit 1; }

# 2. constants.ts is the sole process.env reader
test -f test/e2e/constants.ts \
  || { echo "✗ test/e2e/constants.ts missing"; exit 1; }
grep -rn "process\.env" test/e2e/ | grep -v "constants.ts:" \
  && { echo "✗ process.env outside constants.ts"; exit 1; }

# 3. test files use describeModule<T> from module-test-client
grep -hrnE "import \{ describeModule" test/e2e/*.test.ts \
  | grep -q "from '@zerobias-org/module-test-client'" \
  || { echo "✗ describeModule not imported from @zerobias-org/module-test-client"; exit 1; }

# 4. Module type imported from hub-sdk/generated as a type-only import
grep -rnE "import type \{ [A-Z][a-zA-Z]+ \} from '\.\./\.\./hub-sdk/generated/api/index\.js'" test/e2e/ \
  >/dev/null \
  || echo "warn: module type not imported from hub-sdk/generated/api/index.js"

# 5. CoreError deserializer wired (3rd arg to describeModule)
grep -rn "CoreError\.deserialize" test/e2e/ >/dev/null \
  || echo "warn: pass CoreError.deserialize as the 3rd arg to describeModule for proper error types"

# 6. ESM relative imports
grep -rnE "from '\.\.?\/[^']*'" test/e2e/ | grep -v "\.js'" \
  && { echo "✗ test/e2e/ imports missing .js extension"; exit 1; }

# 7. nock is NOT used in e2e (these hit real APIs)
grep -rn "from 'nock'" test/e2e/ \
  && { echo "✗ nock in test/e2e/ — e2e tests hit real APIs"; exit 1; }

# 8. No dotenv anywhere
grep -rn "from 'dotenv'" test/ src/ 2>/dev/null \
  && { echo "✗ dotenv import found"; exit 1; }

# 9. No legacy test/integration/ directory
test -d test/integration \
  && { echo "✗ test/integration/ exists — move tests to test/e2e/ and delete"; exit 1; }

# 10. Skips are env-driven, not hardcoded
grep -rn "this\.skip()" test/e2e/ | head
# Skips should be inside `if (!ENV_CONST) this.skip();` style guards in constants-driven tests.
```

## describeModule<T> shape

```typescript
import { expect, assert } from 'chai';
import { CoreError, IllegalArgumentError, NotFoundError }
  from '@zerobias-org/types-core-js';
import { describeModule } from '@zerobias-org/module-test-client';
import type { <Class> } from '../../hub-sdk/generated/api/index.js';
import { <Tag>Api } from '../../hub-sdk/generated/api/index.js';
import { ORG_NAME, TEAM_NAME } from './constants.js';

describeModule<<Class>>('<Class> Module', (client) => {

  describe('<Tag>Api.<operation>', () => {
    it('does the happy path', async function () {
      if (!ORG_NAME) this.skip();
      const result = await client.get<Tag>Api().<operation>(ORG_NAME);
      expect(result).to.be.an('array');
    });

    it('rejects with NotFoundError on a missing target', async function () {
      try {
        await client.get<Tag>Api().<operation>('definitely-not-a-real-org');
        assert.fail('should have thrown');
      } catch (e) {
        expect(e).to.be.instanceOf(NotFoundError);
      }
    });
  });

}, (data) => CoreError.deserialize(data));
```

Three things to keep right:

1. **`describeModule<T>`** — the module type comes from `hub-sdk/generated/api/index.js`, type-only import.
2. **`client.get<Tag>Api()`** — never construct the client yourself; the wrapper handles direct/docker/hub differences.
3. **`CoreError.deserialize`** — the third argument. Without it, errors thrown over the wire (docker/hub modes) deserialize as plain objects, not `NotFoundError` etc.

## constants.ts

The only place in the module that reads `process.env`:

```typescript
export const ORG_NAME = process.env.GITHUB_ORG ?? 'zerobias-com';
export const TEAM_NAME = process.env.GITHUB_TEAM ?? '';
```

Every constant gets a sensible default or an empty string. Tests that need a non-empty value skip with `this.skip()` when the constant is empty. That's how the same file passes against a developer slot with everything provisioned and a slot with only minimal fixtures.

Wire actual values via `zbb env set <NAME> <value> --slot local`. Credentials go through `zbb secret create`, not env. See `@.claude/skills/environment-files/SKILL.md`.

## Pass criteria

- At least one `test/e2e/*.test.ts` exists
- `test/e2e/constants.ts` exists and is the only `process.env` reader in the module
- Tests import `describeModule` from `@zerobias-org/module-test-client`
- Module type comes from `../../hub-sdk/generated/api/index.js` (type-only import)
- `CoreError.deserialize` is passed as the third arg to `describeModule`
- No nock, no dotenv, no `test/integration/` directory
- Tests skip gracefully when their required constants are empty
- All relative imports end in `.js`

## On failure

- **`Cannot find module '@zerobias-org/module-test-client'`** — devDependency missing or wrong version. The generator pins `"@zerobias-org/module-test-client": "1.0.3"`; sync to that.
- **e2e fails in `zbb testDirect` but spec is correct** — credentials or env not set on the slot. `zbb env list --slot local`, `zbb secret list --slot local`.
- **e2e passes direct but fails docker** — usually means the `<Class>Impl` reads something at startup that isn't set in the container. Either move the read into `connect()` or set the env on the slot.
- **All e2e tests skip** — `constants.ts` defaults are empty and no env is set. Run `zbb env list --slot local` and populate.

## Related

- @.claude/skills/integration-testing/SKILL.md — full e2e test patterns
- @.claude/skills/environment-files/SKILL.md — constants.ts + zbb env/secret
- @.claude/skills/test-fixtures/SKILL.md — test data organization
- @.claude/skills/gate-test-execution/SKILL.md — running and verifying
