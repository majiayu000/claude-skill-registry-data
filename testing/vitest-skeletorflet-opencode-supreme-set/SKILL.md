---
name: vitest
description: Vite integration, ESM support, describe/it/expect, mocking (vi.mock), snapshot testing, coverage, watch mode, CI config.
---

## vitest

Blazing fast unit testing with Vite.

### Setup and config
- Vite integration: zero-config for Vite projects
- vitest.config.ts: customize test behavior
- Global setup and teardown
- Environment: node, jsdom, happy-dom

### Test structure
- describe, it, test blocks
- expect assertions with matchers
- beforeEach, afterEach, beforeAll, afterAll
- Test filtering with .only, .skip, .todo

### Mocking
- vi.mock for module-level mocking
- vi.spyOn for function spies
- vi.fn for fake implementations
- vi.useFakeTimers for time control

### Advanced
- Snapshot testing with toMatchSnapshot
- Coverage reports with c8/istanbul
- Watch mode with --ui
- CI: --reporter=junit, --reporter=json
