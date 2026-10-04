---
description: "E2E test flow design and review. Use when adding a new E2E test, analysing the impact of changes on existing tests, or introducing a Docker E2E flow."
---

# E2E Test Flow — Design and Review Skill

This skill exists to prevent the failure mode of "debugging by gut feel
and breaking existing tests along the way". Always walk through this
checklist before writing code.

---

## 1. Preflight Checklist (before you touch code)

**Verify every item below before adding a new E2E test or modifying an
existing one.**

### 1-1. Baseline

- [ ] Run `npm run test:e2e` and confirm every existing test passes
- [ ] If any test is failing, identify the cause BEFORE making changes
- [ ] "It's broken now, I'll fix it later" is prohibited. Start from a
      green state every time.

### 1-2. Understand the flow

The current E2E stack runs in this order:

```
global-setup.ts
  → generate random secretPath
  → write .test-output/test-config.json
  → clean test.db
  → start dev server (port 3001)

playwright webServer
  → wait for Next.js to be ready

auth.setup.ts
  → visit /baan-admin/{secretPath}/login
  → log in → save auth-state.json

spec files
  → run authenticated tests using auth-state.json

global-teardown.ts
  → stop dev server
  → clean test.db
```

Plan your change only after you fully understand this flow.

### 1-3. Classify every touched file

Mark each file you intend to touch as one of the following:

| Class | Description | Principle |
|-------|-------------|-----------|
| **Existing file** | A file the current tests depend on | Minimal change. No regressions. |
| **New file** | A file you are adding this round | Design freely. |

If you are modifying an existing file, do the impact analysis in
Section 2 first.

### 1-4. Map the env vars you depend on

List every environment variable the test stack relies on:

```
DATABASE_URL          → must point at data/test.db
PORT                  → 3001
NEXT_TEST_DIST_DIR    → .next-test (required to avoid colliding with .next)
SECRET_PATH           → generated dynamically by global-setup
```

When adding a new env var, always set a safe default that keeps the
existing dev-environment tests working.

---

## 2. Impact Analysis for Shared Infrastructure Changes

The files below **affect every E2E test**. Analyse the blast radius
before changing any of them.

### playwright.config.ts

- Scope: **all E2E tests**
- A change here ripples through every spec
- Be especially careful when touching `webServer.command`

**Prohibited pattern:**
```typescript
// Do not flip Turbopack ↔ webpack casually.
// Switching without identifying the root cause masks other problems.
command: 'next dev --webpack'  // "just trying it" is prohibited
```

### tests/e2e/auth.setup.ts

- Scope: **all authenticated tests**
- A login-flow change breaks every authenticated spec
- Only additive changes are allowed
- Env var defaults must preserve the previous behaviour

### tests/e2e/global-setup.ts / global-teardown.ts

- Scope: **test-run start and end**
- Responsible for secretPath generation, dev server startup, and
  test.db lifecycle
- A change here can cascade: auth.setup and everything after it will
  fail
- **Deleting or commenting out these files is absolutely prohibited**

### next.config.ts

- Scope: **both dev environment and production build**
- Touches both E2E test dev server and production builds
- Do not change it just for a test. Reconsider whether it is truly
  necessary.

### Test-only API routes (`/api/test/*`)

- Must be guarded by BOTH `NODE_ENV !== 'production'` AND a secret
  token
- They are load-bearing for test reliability; changing their
  interface breaks existing specs.

---

## 3. Checklist for Adding a Docker E2E Flow

Procedure for running a Docker-based E2E alongside the dev E2E without
disturbing it.

### 3-1. Files you MUST NOT change

- [ ] `playwright.config.ts` — do not modify
- [ ] `tests/e2e/global-setup.ts` — do not modify
- [ ] `tests/e2e/global-teardown.ts` — do not modify
- [ ] `tests/e2e/auth.setup.ts` — additive changes only

### 3-2. Files you MUST create fresh

- [ ] `playwright.docker.config.ts` — Docker-specific config
- [ ] `tests/e2e-docker/global-setup.ts` — Docker-specific setup
- [ ] `tests/e2e-docker/global-teardown.ts` — Docker-specific teardown

### 3-3. Resources to keep separate

| Resource | dev E2E | Docker E2E |
|---------|---------|------------|
| Port | 3001 | 3002 (or another free port) |
| DB file | `data/test.db` | `data/test-docker.db` |
| test-config | `.test-output/test-config.json` | `.test-output/docker-test-config.json` |
| auth-state | `.test-output/auth-state.json` | `.test-output/docker-auth-state.json` |
| Build dir | `.next-test` | `.next-docker-test` |

### 3-4. Conditions for sharing auth.setup.ts

You may share `auth.setup.ts` only if ALL of the following hold:

- [ ] The change is purely additive (no existing code deleted or
      modified)
- [ ] Env var defaults preserve the original behaviour
- [ ] `npm run test:e2e` still passes for the existing dev E2E flow
      after your change

**Example of env-var defaults:**
```typescript
// Use Docker E2E settings if present, otherwise fall back to the dev
// E2E defaults so existing tests keep working unchanged.
const configPath = process.env.TEST_CONFIG_PATH ?? '.test-output/test-config.json';
const authStatePath = process.env.AUTH_STATE_PATH ?? '.test-output/auth-state.json';
```

### 3-5. Do not touch build caches

- Do not delete `.next-test` or `.next` from setup / teardown
- Next.js manages its own cache. Test code interfering with it leads
  to unpredictable behaviour.

---

## 4. Debugging Checklist for auth.setup Failures

**"Redirected to the setup page" is the most common failure mode.
Investigate in this order.**

### Step 1: Check the setup API

```bash
curl -s http://localhost:3001/baan-admin/api/setup
# Must return 200 with valid JSON.
# 401 / 404 means the DB is not readable.
```

### Step 2: Check `hasUsers()`

If the login page's Server Component calls `hasUsers()`:

- Verify it reads the same DB as the API route
- Verify `DATABASE_URL` is correctly propagated in the Server
  Component's context
- Verify the env is passed in when the dev server is spawned

### Step 3: Confirm `DATABASE_URL` consistency

```typescript
// Example spawn from global-setup.ts
devServer = spawn('node', [...], {
    env: {
        ...process.env,
        DATABASE_URL: 'file:data/test.db',  // same value the API route sees
        PORT: '3001',
    },
});
```

When the API route and the Server Component see different databases,
`hasUsers()` returns inconsistent results.

### Step 4: Check `getAdminUrlPath()`

If the layout reads `secretPath`:

- If it reads from the DB, make sure `DATABASE_URL` points at the
  correct DB
- Make sure `.test-output/test-config.json`'s secretPath matches the
  value in the DB

### Step 5: Turbopack ↔ webpack is a last resort

- Switching bundlers without addressing the root cause achieves
  nothing
- "Just try it" is prohibited. Identify the root cause first.
- If you do switch, verify the impact on every existing test.

---

## 5. Minimise-Change Principle

**When extending the test infrastructure for a new feature, minimise
changes to existing parts.**

### Baseline policy

1. **Prefer adding a new file over modifying an existing one**
2. **When you must share, protect the existing behaviour via env var
   defaults**
3. **Run `npm run test:e2e` both before and after the change** to
   confirm no regression

### Approval flow for changes

```
Is a change needed?
  → YES: Is it a change to an existing file?
      → YES: perform impact analysis (Section 2)
           → additive changes only
           → preserve existing behaviour via env var defaults
           → verify with npm run test:e2e after the change
      → NO: design freely
```

### Things you must NOT do

- Flip `playwright.config.ts` `webServer.command` "just to try"
- Delete `.next-test` from setup scripts
- Rewrite `global-setup.ts` "for optimisation"
- Add code on top of already-failing spec files
- Replace `auth.setup.ts`'s existing logic with a different
  implementation

---

## Quick Reference

```bash
# Run the full existing E2E suite
npm run test:e2e

# Run a single spec (reuse the existing server)
npm run test:e2e:quick -- posts

# Run the Docker E2E (once added)
npx playwright test --config playwright.docker.config.ts
```

**Goal of this skill:** plan every change to the E2E infrastructure
deliberately, and eliminate the "code, run, fix, repeat" style.
