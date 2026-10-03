---
name: frontend-webapp-anatomy
description: Canonical folder structure and architecture pattern for React frontend apps under apps/web/ and apps/mfe/. No concrete reference implementation currently exists on disk — this is the pattern to follow when scaffolding the next one.
---

# Frontend Web App Anatomy

No concrete reference implementation currently exists in `apps/web/` or `apps/mfe/` — the
previous examples (`web1`, host/plain app; `mfe1`, Module Federation remote) were removed. Both
were scaffolded from the same `web` generator template — a remote just adds Module Federation
exposes/wiring on top. This doc captures the pattern they established; treat it as the spec for
the next app scaffolded, and update this doc to point at it once one exists.

## Folder structure

```
apps/{web|mfe}/{name}/
├── Dockerfile
├── nginx.conf                  ← SPA routing config for the built container
├── rsbuild.config.ts           ← Rsbuild bundler config (handles Module Federation for mfe/)
├── rstest.config.ts            ← Rstest test config
├── biome.json
├── AGENTS.md / README.md
├── helm/
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── values-prod.yaml
│   └── templates/
│       ├── deployment.yaml
│       └── ingress.yaml
├── public/
│   └── favicon.png
├── tests/
│   ├── index.test.tsx
│   ├── rstest.setup.ts
│   └── tsconfig.json
└── src/
    ├── index.tsx               ← entry point
    ├── bootstrap.tsx           ← app bootstrap (async import, required for MFE async loading)
    ├── App.tsx / App.css
    ├── env.d.ts                ← environment variable type declarations
    ├── router.tsx              ← React Router routes (host apps only; not present in a bare mfe remote)
    ├── shared/
    │   └── libs/
    │       └── apolloClient.ts ← Apollo Client singleton, points at Apollo Router
    └── modules/
        └── {feature}/
            ├── index.ts        ← module barrel export
            └── pages/
                └── {Feature}Page.tsx
```

## Architecture axioms

- All API calls go through `apolloClient` (Apollo Client → Apollo Router's supergraph
  gateway). Never call a gRPC server or a subgraph's GraphQL endpoint directly from the
  frontend.
- `apolloClient` reads its endpoint from a `PUBLIC_*` env var (e.g.
  `PUBLIC_GRAPHQL_URL`, loaded via `rsbuild.config.ts`'s `loadEnv()`), defaulting to
  `http://localhost:4000/graphql` for local dev.
- Module-based structure: each feature is a self-contained folder under `src/modules/{feature}/`
  with its own `index.ts` barrel and `pages/`. A module with just one page can skip the barrel
  and export the page directly — check an existing module (e.g. `modules/home`) before adding
  boilerplate a small module doesn't need.
- MFE apps (`apps/mfe/*`) use Module Federation via Rsbuild; `bootstrap.tsx` exists
  specifically so the app's real entry can be `import()`ed asynchronously, which Module
  Federation requires for shared-dependency negotiation to happen first.
- A host consumes a remote via `pluginModuleFederation({ remotes: { <remote>: ... } })` in the
  host's `rsbuild.config.ts`, pointed at the remote's exposed module (the remote's own
  `rsbuild.config.ts`'s `exposes`). The remote URL is a browser-side fetch (a `PUBLIC_*` env
  var), not something the host's own Node process resolves — check both sides'
  `rsbuild.config.ts` before assuming a new host/remote pair is wired the same way.

## Scaffolding — never build this by hand

```bash
bun run generate
# select: web (standalone React app) or mfe (Module Federation remote)
```

Host vs. remote role, and non-MF plain app vs. Module Federation, is inferred from where you
scaffold (`apps/web/` vs `apps/mfe/`) — the generator also assigns a free dev port
automatically.
