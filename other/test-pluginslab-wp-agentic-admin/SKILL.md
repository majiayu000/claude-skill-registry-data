---
name: test
description: Run all tests (unit + ability) and lint
allowed-tools: "Bash(npm *), Bash(npx *), Bash(composer *)"
---

# Run All Tests

1. **Lint PHP**: `composer lint`
2. **Lint JS**: `npm run lint:js`
3. **Unit tests**: `npm test`
4. **Ability tests**: `npm run test:abilities -- --file tests/abilities/core-abilities.test.js`

Report results summary. If any step fails, show the errors and stop.
