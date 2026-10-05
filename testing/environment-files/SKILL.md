---
name: environment-files
description: Test env vars and credentials for ESM/gradle Hub modules. Use when wiring e2e test constants or managing per-slot secrets.
---

# Test env vars & credentials

zbb owns env state for test modes. There is no `.env` file in the new module's workflow and no `dotenv` dependency. Credentials are stored as zbb secrets; environment variables are set per-slot. Both are injected into `process.env` when zbb runs `test`, `testDirect`, or `testDocker`.

## Where env vars come from

| Source                        | Lives at                                    | Visible to                                 |
|-------------------------------|---------------------------------------------|--------------------------------------------|
| `zbb env set <NAME> <value>`  | `~/.zbb/slots/<slot>/env.yml`               | All zbb test modes for that slot           |
| `zbb secret create <name>`    | `~/.zbb/slots/<slot>/state/secrets/<name>.yml` | `zbb test*` only; never echoed to stdout |
| Shell environment             | the shell that invoked `zbb`               | passes through unchanged                   |

The slot directory is per-user and gitignored. Nothing about test credentials ever lands inside the module's working tree.

```bash
cd package/<vendor>/[<suite>/]<service>

# Plain env var
zbb env set GITHUB_ORG zerobias-com --slot local
zbb env list --slot local
zbb env get GITHUB_ORG --slot local

# Secret (prompts; value never goes through args)
zbb secret create github-pat \
  --module @zerobias-org/module-<vendor>-[<suite>-]<service> \
  --slot local
```

## The one place that reads `process.env`

The generator scaffolds `test/e2e/constants.ts` as the **sole** entry point for env access:

```typescript
/**
 * Test constants — resolved from slot environment.
 * Tests skip gracefully when required values are missing.
 */

export const ORGANIZATION_NAME = process.env.GITHUB_ORG ?? 'zerobias-com';
export const TEAM_NAME = process.env.GITHUB_TEAM ?? '';
export const REPO_OWNER = process.env.GITHUB_REPO_OWNER ?? '';
// ... env-backed constants
```

Each constant has a sensible default (or empty string when no useful default exists). Tests that need a non-empty value skip themselves:

```typescript
import { TEAM_NAME } from './constants.js';

it('lists members of the team', async function () {
  if (!TEAM_NAME) this.skip();
  const members = await client.getTeamsApi().listTeamMembers(TEAM_NAME);
  expect(members).to.be.an('array');
});
```

The skip pattern is intentional: the same `describeModule<T>` test file runs in three modes (direct / docker / hub) and on three machines (dev / qa / prod). Env-driven skips are how the suite stays green when a fixture isn't provisioned in a given slot.

## Naming convention

Env var names follow the pattern of the module:

```
<UPPERCASE_SERVICE>_<UPPERCASE_PURPOSE>
```

Examples:

```
GITHUB_ORG              # generic-ish; the module name implies github
GITHUB_TEAM
GITHUB_REPO_OWNER

JIRA_PROJECT_KEY
JIRA_ISSUE_TYPE

AWS_S3_TEST_BUCKET      # service-qualified when the module operates on AWS sub-services
```

Use the generator's `apiName` (uppercased) as the prefix when in doubt — the template prefills it:

```typescript
// e2e-constants.template.ts:
//   process.env.<%= apiName.toUpperCase() %>_SOME_ID ?? ''
```

## Forbidden: `process.env` outside `test/e2e/constants.ts`

| Where             | Allowed?                                   |
|-------------------|--------------------------------------------|
| `src/**`          | No. Configuration must flow through `ConnectionProfile`. |
| `test/unit/**`    | No. Unit tests use fixtures, not env vars. |
| `test/e2e/**` (except `constants.ts`) | No. Import from `./constants.js`. |
| `test/e2e/constants.ts` | Yes. The one place.                  |

This is the rule the audit grep enforces:

```bash
grep -rn "process\.env" src/ \
  && echo "✗ process.env in src/" || echo "✓ src clean"

grep -rn "process\.env" test/unit/ 2>/dev/null \
  && echo "✗ process.env in test/unit/" || echo "✓ unit tests clean"

grep -rn "process\.env" test/e2e/ | grep -v "/constants.ts:" \
  && echo "✗ process.env outside constants.ts" || echo "✓ e2e env access centralized"
```

## Credentials are secrets, not env

Credentials (API tokens, OAuth secrets, passwords) belong in `zbb secret create`, not `zbb env set`. The difference matters because:

- `zbb env list` prints values; `zbb secret list` doesn't.
- Secrets are tagged to a module (`--module @zerobias-org/module-…`) so the runtime injects them only when that module is under test.
- `describeModule<T>` knows how to pull secrets into the connection profile on each test mode.

A module that needs a secret declares it in `connectionProfile.yml`; zbb wires the secret value into the test's `ConnectionProfile` argument before `connect()` runs. Tests never read tokens out of `process.env` themselves.

## `.env` files (if you really need one locally)

Nothing in the canonical flow uses a `.env` file. If you keep one for personal convenience:

- It must be **gitignored** (the generator's `.gitignore` doesn't include it explicitly — add `.env` if you start using one)
- It must **not** be referenced from any committed file (no `dotenv` import, no `.mocharc.json` change)
- Use it only for shell-side helpers you run manually, e.g. `source .env && zbb env set …`

The generator does not scaffold a `.env`, a `.env.example`, or a `test-profiles/` directory. Don't recreate them.

## CI / publish flow

CI runs **no tests** — it validates the committed `gate-stamp.json`. So CI doesn't need credentials or env wiring. The `zbb gate` command that produces the stamp runs on the developer's machine with the developer's slot configured.

## Quick checks

```bash
# zbb env / secret state for this slot + module
zbb env list --slot local
zbb secret list --slot local | grep "$(jq -r .name package.json)"

# Constants file exists and only references process.env in this one place
test -f test/e2e/constants.ts && echo "✓ constants.ts" || echo "✗ no constants.ts"

# No dotenv anywhere (devDeps or imports)
grep -n '"dotenv"' package.json && echo "✗ dotenv in package.json" || echo "✓ no dotenv dep"
grep -rn "from 'dotenv'" src/ test/ 2>/dev/null && echo "✗ dotenv import" || echo "✓ no dotenv imports"
```

## Common issues

- **Test reads a value but it's always empty** — `zbb env set` was run on a different slot than the one passed to `zbb test*`. Use `zbb env list --slot local` to confirm.
- **`Cannot find module './constants'`** — missing `.js` extension on the import; ESM requires `from './constants.js'`.
- **Credentials show up in CI logs** — secrets stored via `zbb env set` instead of `zbb secret create`. Move them.
- **Test passes locally, fails in `zbb testDocker`** — the container only sees variables zbb declared, not your shell's. Re-set them with `zbb env set`.

## Related

- @.claude/skills/connection-profile/SKILL.md — what credentials a module accepts
- @.claude/skills/integration-testing/SKILL.md — how `test/e2e/` consumes these constants
- @.claude/skills/tool-requirements/SKILL.md — `zbb env` / `zbb secret` command reference
