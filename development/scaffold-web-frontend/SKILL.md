---
name: scaffold-web-frontend
description: >-
  Load this skill when starting or scaffolding a new web frontend (SvelteKit or React + Vite):
  creating the source layout, $lib/api client boundary, test folders, and .gitignore. Trigger when
  the user says "start/scaffold a Svelte app", "scaffold a React app", or sets up a fresh frontend
  repo. For the backend use scaffold-python-service.
compatibility: >-
  Requires `bun` on PATH (or Node.js 20+ with npm) and network access to the npm registry for the
  first install. Vite, Vitest, and Playwright arrive as project dev dependencies, not from a
  global install; Playwright additionally downloads browser binaries on first run. `git` is needed
  only to initialise the repo.
---

# Scaffold a Web Frontend

Bun + Vite. SvelteKit and React share the same layout conventions; only the framework files differ.

```
frontend/
├── src/
│   ├── lib/
│   │   ├── api/            # centralized API client — the only place fetch is called
│   │   ├── components/     # presentational components (PascalCase)
│   │   ├── stores/         # SvelteKit only — shared state, updated from API responses
│   │   └── types.ts
│   ├── routes/             # SvelteKit routes  (React: src/routes or React Router config)
│   └── app.html / main.tsx
├── tests/
│   ├── unit/
│   ├── component/
│   └── e2e/
├── package.json
├── tsconfig.json
├── vite.config.ts
└── .gitignore
```

## Initial Config

- `package.json` scripts for dev/build/test/lint/typecheck — see `ceh-web-frontend:environment`.
- `tsconfig.json` with `strict: true`; ESLint + Prettier configured.
- Components are presentational; all `fetch` goes through `src/lib/api`.

## Agent instruction file

Claude Code reads `CLAUDE.md`, **not** `AGENTS.md`. If the repo already has an `AGENTS.md` for
other coding agents, do not duplicate it — create a `CLAUDE.md` that imports it, so both tools
read one source:

```markdown
@AGENTS.md
```

Add any Claude-specific instructions below the import. A symlink also works, but on Windows it
needs Administrator or Developer Mode, so prefer the import. If there is no `AGENTS.md`, just
write `CLAUDE.md` directly.

## .gitignore

```
node_modules/
.svelte-kit/
dist/
build/
.env
.env.*
!.env.example
.DS_Store
```
