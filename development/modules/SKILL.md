---
id: javascript.modules
name: JavaScript Modules
description: >
  Reviews JavaScript module boundaries, exports, barrels, side effects, circular dependencies, and CommonJS versus ES Module interoperability.
stack:
  - JavaScript
  - TypeScript
category: javascript
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - javascript modules
  - import export
  - commonjs
  - es modules
  - barrel files
  - circular dependencies
  - package exports
  - module boundaries
compatibility:
  runtime:
    browser: true
    node: true
---

# JavaScript Modules

## Purpose

Use this skill to review, refactor, or implement JavaScript module boundaries.

The goal is to keep imports and exports explicit, stable, tree-shakable, and easy to reason about.

This skill applies to ES Modules, CommonJS interoperability, barrel files, frontend code, Node.js code, shared libraries, scripts, and package entry points.

## When to Use

Use this skill when the task involves:

- `import` / `export`
- `require` / `module.exports`
- converting CommonJS to ES Modules
- converting ES Modules to CommonJS
- barrel files
- circular dependencies
- package entry points
- module boundaries
- tree-shaking problems
- path aliases
- side-effect imports
- dynamic imports
- public API design

## When Not to Use

Do not use this skill when:

- the task is only about business logic inside a function
- the change belongs to a framework-specific routing or lazy-loading skill
- the module system is fixed by the runtime and the request does not involve imports or exports
- the change would require broad package restructuring without explicit approval
- the task is only about TypeScript type definitions with no module boundary impact

## Do

Detect the active module system and keep module style consistent.

Prefer ES Modules in modern frontend and TypeScript code:

```js
import { formatUser } from "./format-user.js";

export function getDisplayName(user) {
  return formatUser(user);
}
```

Use CommonJS only when required by runtime or package contract:

```js
const { formatUser } = require("./format-user");

module.exports = {
  getDisplayName,
};
```

Prefer named exports for shared utilities.

Keep public API explicit with targeted exports.

Use barrel files carefully and avoid exporting internal helpers.

Prevent circular dependencies by moving shared helpers lower in the graph.

Avoid side effects in modules unless they are explicitly intentional.

Use dynamic imports for deferred loading when the boundary is justified.

Respect package exports and do not import private internal paths.

Keep module refactors small and reversible.

## Do Not

Avoid mixing `import` and `require` in the same file unless interoperability is required and justified.

Avoid default exports for shared utilities unless the project convention already requires them.

Avoid broad `export *` barrels that hide unstable internals.

Avoid import-time side effects.

Avoid importing from private package paths.

Avoid broad file moves when a narrow fix is sufficient.

## Review Checklist

- [ ] The module system is clear.
- [ ] Imports are consistent with the runtime.
- [ ] Public exports are intentional.
- [ ] Barrel files are safe and limited.
- [ ] There are no circular dependencies.
- [ ] Side effects are intentional.
- [ ] Package boundaries are respected.
- [ ] The diff is small and reversible.

## Expected Output

1. Detect the module system.
2. Keep module style consistent.
3. Make exports explicit.
4. Remove circular dependencies or side-effect ambiguity.
5. Keep the refactor focused.
