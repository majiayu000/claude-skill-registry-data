---
name: typescript-conventions
description: Apply TypeScript conventions for composition, small single-purpose functions, tests for new functions, and formatter and import-alias discipline. Use when writing or reviewing TypeScript files.
license: MIT
compatibility: "Claude Code"
---

# TypeScript rules

- Keep `strict` mode enabled in `tsconfig.json`; never turn it off to make a build pass.
- Prefer composition over inheritance.
- Give every function one purpose and keep it near 30 lines or fewer.
- Add tests for every new exported function or changed contract and its edge cases. See `developer-os:testing-conventions` for how to write them.
- Follow the quote style and formatting the project's formatter enforces.
- Use the project's configured import alias instead of long relative paths.
