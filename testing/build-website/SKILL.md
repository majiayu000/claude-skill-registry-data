---
name: build-website
description: Build, serve, and test the Too Many Cooks documentation website (Eleventy + Playwright)
argument-hint: "[build|dev|test|clean]"
disable-model-invocation: true
allowed-tools: Bash
---

# Website (Eleventy + Playwright)

Build and test the Too Many Cooks documentation site at `website/`.

## Commands

**build** — Full production build:
```bash
cd website && npm run build
```

**dev** — Start the dev server with live reload:
```bash
cd website && npm run dev
```
Serves at `http://localhost:8080`.

**test** — Run Playwright E2E tests:
```bash
cd website && npm test
```

**clean** — Remove generated files:
```bash
cd website && npm run clean
```

**No args** — Default to `build` then `test`.

## Prerequisites

Playwright must be installed first:
```bash
cd website && npm ci && npx playwright install --with-deps chromium
```
