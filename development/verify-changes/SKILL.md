---
name: Verify Changes
description: Use this skill after implementing code to verify correctness before notifying the user.
---

# Verify Changes (QA Protocol)

Use this skill after code changes to meet the `AGENTS.md` “definition of done”.

## When to use

- After any change that can affect build/runtime behavior.
- Always after UI/interaction changes (run UI smoke).

## Standard checks (run from repo root)

Run these in order; if one fails, fix it before continuing:

1) Typecheck + minimal lint

```bash
npm run check
```

2) Backend tests (includes smoke)

```bash
npm test
```

3) Build bundle (catches bundler/runtime issues)

```bash
npm run build
```

## UI smoke (required when UI/interaction changed)

Pre-reqs:

1) Build the frontend:

```bash
npm run build
```

2) Start the backend serving `dist/` on `:4800`:

```bash
npm run backend:start
```

Then run:

```bash
npm run test:ui:smoke
```

## Notes

- If you only changed documentation, you can skip these commands.

