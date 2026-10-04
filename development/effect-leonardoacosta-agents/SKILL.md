---
name: effect
description: Effect 4.0 framework conventions for Bun-based TypeScript services, including composition, typed errors, layers, runtime boundaries, and verification.
metadata:
  category: Framework
  level: framework
  engineer: api-engineer
  gate: bun typecheck
  bundles:
    - skill: drizzle
      category: DB
    - skill: bun
      category: Service
allowed-tools: Read, Glob, Grep
---


# Effect

Use this skill when a Bun service uses Effect as its application framework. Prefer the target
repository's local instructions for exact package versions and commands.

- Model expected failures with typed errors rather than unchecked exceptions.
- Build dependencies as explicit layers and provide them at the application boundary.
- Keep promise, callback, and request-framework interop at narrow adapter boundaries.
- Use scoped resources for connections, handles, and subscriptions that require cleanup.
- Run the repository's formatter and linter before `bun typecheck` and its focused tests.
