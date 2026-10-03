---
name: monorepo-metro
description: React Native and Expo in monorepos. Use for Invalid hook call or duplicate react-native in a workspace app, Metro not resolving workspace packages, EAS failing only in the monorepo, hoisting and lockfile strategy.
user-invocable: false
---

# React Native in a monorepo

## First, delete the folklore

Modern expo/metro-config configures Metro for monorepos automatically. If the repo carries a hand-written `metro.config.js` full of `watchFolders`, `nodeModulesPaths`, `extraNodeModules` or `disableHierarchicalLookup` copied from an old blog post, that config is now the most likely cause of the problem, not the fix. Strip it down to the default Expo config, run `npx expo start --clear` once, and re-test before debugging anything else.

The problems that remain after that are real, and they are all below.

## Singletons, the actual monorepo disease

react, react-native and the native-module packages must resolve to exactly one copy for the app. Two copies produce the classic signatures:

- "Invalid hook call" with a perfectly valid component
- "Tried to register two views with the same name"
- A native module that works in one workspace app and crashes in another

Diagnose with the package manager, not by staring at code: `npm ls react-native` (or `yarn why react-native`, `pnpm why react-native`) from the repo root. More than one resolved version, or the same version in two physical locations, confirms it.

Fix at the root: pin the singletons with the root manifest's override mechanism (`overrides` for npm, `resolutions` for yarn, pnpm's overrides). Then reinstall from the root and re-run the check. If the lockfile seems to hold onto stale resolutions after the override, a full reinstall of node_modules is legitimate here; this is the deliberate-upgrade case, not build-error cache thrashing.

## Hoisting strategies decide your failure mode

- npm and yarn hoist: a package you forgot to declare still resolves because a sibling declared it. Everything works locally and then fails on EAS or on a colleague's machine with a different install order. The bug is the undeclared dependency, not the machine.
- pnpm and bun isolate: undeclared dependencies fail immediately and loudly. More friction on day one, dramatically fewer ghosts later.

Whichever the repo uses, the rule is the same: every workspace package declares what it imports. Hoisting merely changes when you find out.

## Native code and config plugins in shared packages

JS-only shared packages are free. The moment a shared package carries native code or a config plugin, remember that natives are built per app: the app's own package.json must carry the dependency (so autolinking and prebuild see it), not just the shared package's. Symptoms of getting this wrong: the module exists in JS, and the native side throws "module not found" only in release or only in one app.

## EAS builds from a monorepo

- The lockfile that matters is the root one; EAS installs from the repo root and builds the app in its workspace directory.
- "Works locally, fails on EAS" in a monorepo is almost always hoisting (an undeclared dependency that local hoisting hid) or a file referenced outside the workspace that is not committed.
- Keep one SDK/react-native version pair across apps in the workspace if at all possible. Two apps on two RN versions in one workspace is a supported-in-theory, painful-in-practice setup; if a version split is unavoidable, treat it as temporary and plan the convergence.

## When Metro acts haunted

Symptoms like "module disappeared after I moved a file" or imports resolving to stale copies: one `npx expo start --clear` after dependency-graph surgery is legitimate. Running it before every start is a ritual that hides a real problem; if cold cache is the only thing that makes the app build, the resolution problem above is still unsolved.
