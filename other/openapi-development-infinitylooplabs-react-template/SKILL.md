---
name: openapi-development
description: Generate and remove OpenAPI hook/config wiring for a backend domain in the React template.
metadata:
  short-description: OpenAPI integration workflow
---

# OpenAPI Development

## When to use
- Adding a new OpenAPI domain integration (instance, config, reducers/middlewares, env key wiring).
- Removing an existing OpenAPI domain integration from the template project.

## Quick start
0) Add integration:
   - `ill addOpenApiConfig auth`
   - or `ill addOpenApiConfig --name auth`
1) Generate hooks for this domain:
   - `npm run hooks:auth`
2) Remove integration when needed:
   - `ill removeOpenApiConfig auth`
   - or `ill removeOpenApiConfig --name auth`

## What CLI adds (`addOpenApiConfig`)
- Backend env constant in `app/constants/app/index.ts`:
  - `BACKEND_<NAME_SCREAMING_SNAKE>_URL`
- Axios wiring in `app/application/api/axios.ts`:
  - backend URL import usage
  - axios instance `${name}_instance`
  - request/response interceptors
- RTK instance file:
  - copies `_template/openapi-config/app/application/api/rtk/instances/sample.ts`
  - renames to `app/application/api/rtk/instances/${name}.ts`
- OpenAPI generator config:
  - copies `_template/openapi-config/openapi-config-sample.cjs`
  - renames to `openapi-config-${name}.cjs`
- `package.json` script:
  - adds `"hooks:${name}": "... openapi-config-${name}.cjs"`
- Store generated wiring:
  - inserts import + middleware in `app/application/store/generated/middlewares.ts`
  - inserts import + reducer in `app/application/store/generated/reducers.ts`

## What CLI removes (`removeOpenApiConfig`)
- Removes all lines injected by `addOpenApiConfig` in:
  - `app/constants/app/index.ts`
  - `app/application/api/axios.ts`
  - `package.json`
  - `app/application/store/generated/middlewares.ts`
  - `app/application/store/generated/reducers.ts`
- Deletes generated files:
  - `app/features/generated/hooks/${name}.ts`
  - `app/application/api/rtk/instances/${name}.ts`
  - `openapi-config-${name}.cjs`

## Naming rules
- Input is expected in lowercase domain style (`auth`, `drafts`, `billing`).
- CLI also derives:
  - `${nameScreamingSnake}` for env constant names
  - `${Name}`/`${name}` forms for injected code

## Final checks
- `npm run hooks:${name}` exists in `package.json` after add.
- New `openapi-config-${name}.cjs` and `${name}.ts` RTK instance are present after add.
- Store generated files include `${name}` reducer/middleware lines after add.
- After remove, all injected lines/files are gone.
