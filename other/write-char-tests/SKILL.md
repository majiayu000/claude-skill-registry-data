---
name: write-char-tests
description: >
  Writes characterization tests (HTTP slice tests) for a given domain before an architecture
  refactoring. Captures the observable HTTP behaviour of all controllers in the domain so that
  any regression introduced during the refactoring is immediately detected.
  Trigger on: "écris les char tests pour X", "write-char-tests sur X",
  "je veux les characterization tests de X avant refacto",
  "prépare le filet de sécurité pour X", "characterize X avant fix-debt".
---

## Purpose

Generate `.characterization.spec.ts` files that freeze the current HTTP output of a domain's
controllers. These tests follow the **characterization test** pattern (Michael Feathers,
_Working Effectively with Legacy Code_): they do not assert correctness — they capture what
the system currently does, so that refactoring cannot silently change observable behaviour.

For the full rationale and conventions, read:
`apps/idf-young-documentation/docs/coding-standards/testing-strategy.md`

---

## Step 1 — Identify the domain scope

Determine which `*-api` library (or libraries) to cover:

| Input                                     | Action                                       |
| ----------------------------------------- | -------------------------------------------- |
| User provides a domain name (e.g. "tips") | Locate `libs/<domain>/<domain>-api/src/`     |
| User provides a directory path            | Use it directly                              |
| `fix-debt` triggered this skill           | Use the same scope as the `fix-debt` session |

Read the `project.json` to confirm the library name and exported paths.

---

## Step 2 — Discover all controllers in scope

Scan the `*-api/src/` directory for `*.controller.ts` files. For each controller:

1. Read the file to extract:
   - The route prefix (`@Controller('...')`)
   - Every HTTP method handler (`@Get`, `@Post`, `@Put`, `@Patch`, `@Delete`) with its path
   - The return type or view class used
   - The service method called
2. List all endpoints in a summary table before writing any code:

```
## Endpoints found — tips-api

| Method | Route           | Controller method  | Return type      |
| ------ | --------------- | ------------------ | ---------------- |
| GET    | /tips           | search()           | TipView[]        |
| GET    | /tips/:id       | findOne()          | TipView          |
| POST   | /tips           | create()           | TipView          |
| DELETE | /tips/:id       | delete()           | void             |
```

Wait for the user to confirm ("go", "ok", "oui", or equivalent) before proceeding.

---

## Step 3 — Identify dependencies to mock

For each controller, find:

1. The **repository class(es)** injected into the service — these are the only dependencies
   to mock (the DB is intentionally absent, see testing-strategy.md)
2. The **module class** used to bootstrap the `TestingModule`
3. The **auth guard** class (typically `AuthorizationsGuard`) to override

Read the service file and the module file to confirm injection tokens.

---

## Step 4 — Write the fixtures

For each entity returned by the repository mock, create a minimal but realistic TypeScript
fixture object. Place fixtures inline in the test file (do not create separate fixture files
unless there are more than 3).

Fixture naming convention: `{entityName}Fixture` (e.g. `tipEntityFixture`).

The fixture must contain **all fields that are mapped to the view** — check the `.view.ts` or
`.view.interface.ts` to ensure no field is omitted.

---

## Step 5 — Write the test file

Create `{domain}.characterization.spec.ts` at the root of `*-api/src/`:

```typescript
import { ClassSerializerInterceptor, INestApplication } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { Test } from '@nestjs/testing';

import { AuthorizationsGuard } from '@idf-subventionjeunes-web/commons-api';
import { Ok } from '@idf-subventionjeunes-web/commons-domains';
import * as request from 'supertest';

import { TipsSqlRepository } from './infrastructure/sql/tips.repository';
// Import the feature module, the repository, and the auth guard
import { TipsModule } from './tips.module';

// --- Fixtures ---
const tipEntityFixture = {
  tip_id: 'tip-id-1',
  tip_title: 'Tip title',
  // ... all mapped fields
};

describe('{Domain} — characterization', () => {
  let app: INestApplication;

  const mockRepo = {
    search: jest.fn(),
    findOne: jest.fn(),
    // ... all methods used by the service
  };

  beforeAll(async () => {
    const moduleRef = await Test.createTestingModule({
      imports: [TipsModule],
    })
      .overrideProvider(TipsSqlRepository)
      .useValue(mockRepo)
      .overrideGuard(AuthorizationsGuard)
      .useValue({ canActivate: () => true })
      .compile();

    app = moduleRef.createNestApplication();
    app.useGlobalInterceptors(new ClassSerializerInterceptor(app.get(Reflector)));
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  // One describe per controller route
  describe('GET /tips/:id', () => {
    it('returns 200 with the tip — matches snapshot', async () => {
      mockRepo.findOne.mockResolvedValue(Ok(tipEntityFixture));

      const response = await request(app.getHttpServer()).get('/tips/tip-id-1');

      expect(response.status).toBe(200);
      expect(response.body).toMatchSnapshot();
    });

    it('returns 404 when tip not found — matches snapshot', async () => {
      mockRepo.findOne.mockResolvedValue(Err(new UnknownTipError()));

      const response = await request(app.getHttpServer()).get('/tips/unknown');

      expect(response.status).toBe(404);
      expect(response.body).toMatchSnapshot();
    });
  });

  // Repeat for every endpoint
});
```

### Rules for the test body

- **One `it` per success case per endpoint** — mock the repo to return `Ok(fixture)`, assert
  status and `toMatchSnapshot()` on the body
- **One `it` per error case per endpoint** — mock the repo to return `Err(...)`, assert the
  expected HTTP status and `toMatchSnapshot()` on the body
- Never hardcode expected field values (e.g. `expect(body.title).toBe('...')`) — use
  `toMatchSnapshot()` exclusively
- Always reset mocks in `beforeEach` if the `describe` block contains multiple `it`s that
  set different mock return values
- **Never use section-divider comments** (e.g. `// ---... GET /tips/:id ...---`) inside or
  outside `describe` blocks — the `describe` label is self-documenting and these banners add
  visual noise without value

---

## Step 6 — Run the tests and generate the snapshots

```bash
pnpm exec nx test <domain>-api --testPathPattern=characterization
```

The first run generates the `.snap` file. Confirm all tests pass (green). If a test fails
due to a module configuration issue (missing provider, circular dep), fix it before proceeding.

---

## Step 7 — Commit

The following files must be committed together:

- `libs/<domain>/<domain>-api/src/{domain}.characterization.spec.ts`
- `libs/<domain>/<domain>-api/src/__snapshots__/{domain}.characterization.spec.ts.snap`

Suggested commit message:

```
test(IDF-XXX): add characterization tests for {domain}-api before architecture refactoring
```

---

## Constraints

- **Never run `jest --updateSnapshot`** after the initial generation unless the behaviour change
  is intentional and reviewed. A snapshot diff during a refactoring is a bug signal.
- **Never use a real DB** in these tests. The DB is intentionally absent — see testing-strategy.md.
- **Never test auth logic** in these tests. Override the guard unconditionally.
- **Never assert individual field values** — always use `toMatchSnapshot()` so the full
  response shape is captured.
- If the module has complex imports that fail to bootstrap in isolation (e.g. circular deps or
  global config modules), use `overrideModule` or `useValue` overrides to stub them — but do
  not simplify the module structure just for the test.
