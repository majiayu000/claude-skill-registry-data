---
name: aiwf-react-coding
description: Use for React components, hooks, state, accessibility, rendering behavior, builds, and browser UI validation.
---

# AIWF React Coding

## Core Rule

Work from the app's actual React stack. Inspect package manager, React version, framework, build tool, routing, styling system, and test setup before editing components. Visible UI changes need browser or screenshot validation when practical.

## Workflow

1. Inspect `package.json`, lockfile, `vite.config.*`, Next/Remix config, `tsconfig`, component folders, state management, test config, and existing design system.
2. Confirm whether the app is React-only, React with TypeScript, Next.js server/client components, Electron, or another runtime.
3. Patch components with stable state and effects. Avoid broad rewrites of architecture, package manager, or styling approach.
4. Validate accessibility basics: labels, roles, focus order, keyboard behavior, disabled/loading states, and error states.
5. Run the repo-native lint/test/build and visually inspect changed screens when the UI changes.

## React Guardrails

- Follow the Rules of Hooks. Do not call hooks conditionally or inside loops, callbacks, or non-component helpers.
- Keep effects for synchronization with external systems. Avoid using `useEffect` as a general state derivation tool when render-time derivation works.
- Preserve server/client boundaries in framework apps. Do not add browser-only APIs to server components.
- Keep component props typed and stable. Add `aiwf-typescript-coding` for TS/TSX type changes.
- Avoid introducing global state for local UI state.
- Prevent layout shift from loading, empty, and error states.

## Validation Defaults

Prefer existing commands. Useful fallbacks:

```powershell
npm run lint
npm test
npm run build
npm run dev
```

Use `pnpm`, `yarn`, or `bun` when the lockfile shows that manager. For visible changes, use a browser screenshot or Playwright check when available.

## Primary Source Anchors

- React documentation: https://react.dev/
- React Learn: https://react.dev/learn
- React API reference: https://react.dev/reference/react

React framework rules vary by router and build tool. Verify the local framework docs or project conventions when those rules matter.
