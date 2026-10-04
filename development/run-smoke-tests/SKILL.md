---
name: run-smoke-tests
description: Run Playwright smoke tests, debug failures, and verify fixes. Use for smoke, e2e, Playwright, or pre-ship browser verification.
---

# Run smoke tests

## Trigger

Need end-to-end smoke verification before or after changes.

## Workflow

1. Build prerequisites for the target app.
2. Run the relevant smoke suite or a focused test file.
3. If failing, inspect traces/logs and isolate the root cause.
4. Report the failure with evidence. Do not patch product code. Tech lead classifies. Bug implements.
5. If the suite is green, say so and stop.

## Example Commands

```bash
npm run smoketest
npm run smoketest -- path/to/test.spec.ts
npm run smoketest-no-compile -- path/to/test.spec.ts
```

If the repo uses a different script (`npm test`, `npx playwright test`, `make smoke`), use that. Do not invent a suite that is not in the checkout.

## Guardrails

- Prefer deterministic waits and assertions over brittle timeouts.
- Re-run a green result once when flake is suspected. Report flake evidence.
- Quarantine tests only when explicitly requested and documented.
- Never `--no-verify`. Never read `.env` or `.env.local`.

## Output

- Test results summary
- Root cause for each failure, with a repro
- Remaining flake risk (if any)

## Factory override

Report only. Do not implement the fix. Do not merge. Only the dispatched ticket or PR.
