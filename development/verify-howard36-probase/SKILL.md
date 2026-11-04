---
name: verify
description: Verify a change is done by running lint, the Prettier check, the test suites, and a production build. Use after finishing any code change and before opening a PR.
---

Run these checks from the repo root, in order, and stop at the first failure:

```
npm run lint
npx prettier . --check
npm test
npm run test:db && npm run test:integration
npm run build
```

- If Prettier reports unformatted files, run `npx prettier --write <files>` on just those files and re-run the check.
- If lint or build fails, fix the reported issue. `@typescript-eslint/no-floating-promises` is an error: add `.catch(...)` or `void` to un-awaited promises rather than disabling the rule.
- `npm run test:db` needs Docker. If Docker is unavailable, skip the integration step and say so explicitly in the report; do not point the tests at any other database.
- If a test fails, decide whether the test or the code is wrong before changing either, and say which in the report.
- Report the outcome faithfully: which checks passed, and the exact error output for any that failed.

Do not run `npm run dev:prod` or `npm run prod` as part of verification.
