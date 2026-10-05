---
name: package-boundary-guardian
description: Use when changing JS/TS package exports, startup/import cost, package size, public subpaths, dependency direction, optional peers, tree-shaking, or package-boundary tests.
---

# Package Boundary Guardian

Treat package shape as a tested contract from the beginning of a project.

## Workflow

1. Identify public entry points from `package.json` exports.
2. Identify forbidden dependency directions for each entry point.
3. Keep checks for:
   - export presence,
   - forbidden imports,
   - startup/import time,
   - reachable files/bytes,
   - `npm pack --dry-run` files and unpacked bytes,
   - optional peer isolation.

4. If ShapeShift Labs Evidence Kit is installed, run:

```sh
npx evidence-kit scope
npm run bench:startup:check
npm run bench:package:gates
npm run docs:perf:search -- package-boundary startup
```

Use the scope result to decide whether startup or package benchmarks need refresh.

## Rules

- Prefer subpath exports over root export growth.
- Keep optional integrations out of root imports.
- Do not hide package-size regressions behind functional tests.
- Record package-boundary source passes when external package shapes informed budgets or export layout.
- Record budget changes in an iteration note with the reason.
