---
name: js
description: Use for Vite+React+TanStack Query frontends on Bun/Cloudflare Workers with shadcn/Tailwind—provides dev console bridge, tmux layout, dense/no-motion UI defaults, and Justfile/CI parity.
---

# JS (Vite/React/TanStack/Bun/Workers)

## Overview
Agent-ready workflow for the preferred JS stack: Vite + React + TanStack Query + Tailwind/shadcn UI on Bun with a Cloudflare Worker backend. Focus: dev console bridge to pipe FE logs to backend logs, tmux layout for servers/logs, dense/no-animation UI defaults, and Justfile/CI parity.

## When to Use
- Building or debugging this stack.
- Need frontend logs visible without browser console.
- Spinning up a fresh dev env for agents with tmux panes and predictable commands.
- Want square, animation-free, dense UI baseline.

## Core Pattern
- **Commands (keep CI aligned)**: `pnpm install --frozen-lockfile`; `pnpm format:check`; `pnpm lint`; `pnpm test -- --runInBand`; `pnpm dev`.
- **Dev console bridge (dev-only)**: in `src/dev/console-bridge.ts`, wrap `console` methods, POST to `/__dev/fe-logs` when `import.meta.env.DEV`, guard recursion/online state.
- **Worker receiver**: CF Worker route `/__dev/fe-logs` logs to backend console with timestamp/prefix; dev-only.
- **tmux layout**: session with panes for Vite (`bun run dev --host 0.0.0.0 --port 5173`), Wrangler (`bunx wrangler dev --local`), backend log tail, frontend log tail (Vite log to file). Start layout before debugging.
- **UI defaults**: square corners, animations off, dense spacing, mobile-first grid. Tailwind base: `* { border-radius: 0; animation: none; transition: none; } :root { color-scheme: light; }`.
- **TypeScript style**: split type/value imports; data-first funcs; `satisfies` over `as`; prefer `const T extends` for inference; throw typed errors; TSDoc on exports; tests with vitest close to code.
- **React + TanStack Query**: options-first hooks, explicit `enabled`, reuse query options/helpers, manage cache on identity change, add type tests where useful.

## Verification
- Trigger `console.error('boom')` in dev → appears in backend log tail as `[FE ...] boom`.
- `curl -X POST http://localhost:8787/__dev/fe-logs -d '{"level":"info","ts":0,"msg":"hello"}' -H 'Content-Type: application/json'` → shows in backend logs.
- View at 360px width → layout remains readable, no overflow; no animations.

## Quick Reference
- Start dev: `pnpm dev` (or `bun run dev --host 0.0.0.0 --port 5173`) + `bunx wrangler dev --local`
- Logs: ensure Vite writes to file (`--logFile logs/frontend.log`); tail in tmux panes.
- Bridge file: `src/dev/console-bridge.ts`; import in `main.tsx` only in dev.
- Worker endpoint: `/__dev/fe-logs` dev-only.
- UI base: radius 0, animations off, dense spacing.

## Red Flags
- Bridge enabled in production (missing dev guard).
- Using browser console instead of bridging logs.
- tmux panes pointing at wrong cwd; missing Justfile parity with CI.
- Animations/rounded defaults left on; UI not dense/mobile-first.
