---
name: deprecation-and-migration
description: >
  Safe deprecation of features and migration between versions. Use
  when removing features, changing APIs, or migrating data schemas.
  Covers deprecation notices, migration guides, and sunset timelines.
version: 1.0.0
permissions:
  - fs.read
  - fs.write
  - shell.exec
triggers:
  - context: "deprecating a feature"
  - context: "removing an API endpoint"
  - context: "migrating data schemas"
  - command: "/ship"
platforms:
  - claude-code
  - cursor
  - gemini-cli
  - copilot
  - codex
  - opencode
  - windsurf
  - kiro
dependencies:
  - git-workflow-and-versioning@^1.0.0
author: codehands-core
signed: true
tier: 2
---

## Overview

Deprecation is making a promise: "this will be removed, here's what to use instead, and here's how much time you have." This skill ensures deprecated features have clear notices, migration paths, and respectful timelines.

## When to Use

- When removing a feature or API endpoint
- When changing a public API signature (breaking change)
- When migrating database schemas
- When replacing one library/tool with another
- NOT for internal-only changes with no external consumers

## Process

### 1. Deprecation Notice

Before removing anything, add a deprecation notice:
```typescript
/**
 * @deprecated Use `newFunction()` instead. Will be removed in v3.0.0.
 */
function oldFunction() { ... }
```

### 2. Migration Guide

Write a migration guide:
```markdown
## Migrating from v1 to v2

### Breaking Changes
1. `oldFunction()` removed → use `newFunction()`
2. `/api/v1/users` removed → use `/api/v2/users`

### Step-by-Step
1. Update import: `import { newFunction } from 'package'`
2. Replace all calls to `oldFunction(a, b)` with `newFunction({ a, b })`
3. Run tests to verify
```

### 3. Sunset Timeline

- **Deprecation notice**: v2.0 (current release)
- **Last supported version**: v2.x (minimum 1 major version)
- **Removal**: v3.0 (never remove in a minor/patch version)

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Nobody uses this feature" | If you don't have usage metrics, you don't know. Add deprecation logging first, then decide. |
| "We can just remove it" | Removing without notice breaks consumers. Even internal consumers. Deprecate first. |

## Red Flags

- Removing features without deprecation notice
- Breaking changes in minor/patch versions
- No migration guide for breaking changes
- No usage metrics before deciding to deprecate

## Verification

- [ ] Deprecation notice with replacement and removal version
- [ ] Migration guide written
- [ ] Breaking changes in CHANGELOG
- [ ] Major version bump for breaking changes (semver)

## See Also

- `codehands:git-workflow-and-versioning` — Semver for breaking changes
- `codehands:documentation-and-adrs` — ADR for deprecation decision
