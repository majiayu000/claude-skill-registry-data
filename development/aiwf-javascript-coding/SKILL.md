---
name: aiwf-javascript-coding
description: Use for JavaScript runtime targets, modules, async behavior, DOM APIs, security, browser or Node validation.
---

# AIWF JavaScript Coding

## Core Rule

Start by identifying the JavaScript runtime and module system. Browser, Node, Electron, service worker, extension, and bundled frontend code have different APIs and compatibility rules. Do not add TypeScript syntax to JavaScript files unless the toolchain explicitly supports it.

## Workflow

1. Inspect `package.json`, lockfile, Node version files, bundler config, Babel/SWC config, ESLint config, test setup, and target browsers/runtimes.
2. Confirm ESM/CommonJS boundaries and generated/bundled output before changing imports, exports, or package metadata.
3. Patch async behavior carefully: promise rejection, cancellation, cleanup, event listener removal, timers, and backpressure.
4. Keep DOM, storage, network, and worker APIs behind the right runtime checks.
5. Validate with lint/test/build and runtime smoke where practical.

## JavaScript Guardrails

- Avoid unhandled promises and swallowed errors. Preserve meaningful error reporting.
- Keep user input, HTML insertion, URL construction, and local storage handling security-aware. Add `aiwf-security-guardrails` for XSS, tokens, auth, or public exposure.
- Do not mutate shared state in ways that break React or framework render assumptions.
- Do not mix CJS and ESM by guesswork. Follow the package's `"type"`, bundler config, and existing imports.
- Avoid broad dependency upgrades or package-manager switches just to use one feature.
- For browser code, verify target support or transpilation before using newer ECMAScript or Web APIs.

## Validation Defaults

Prefer existing commands. Useful fallbacks:

```powershell
npm run lint
npm test
npm run build
node <script.js>
```

Use `pnpm`, `yarn`, or `bun` when the lockfile shows that manager.

## Primary Source Anchors

- ECMAScript specification: https://tc39.es/ecma262/
- ECMA-262 standard page: https://ecma-international.org/publications-and-standards/standards/ecma-262/
- MDN JavaScript documentation: https://developer.mozilla.org/en-US/docs/Web/JavaScript

Verify runtime support before relying on current ECMAScript or Web Platform features.
