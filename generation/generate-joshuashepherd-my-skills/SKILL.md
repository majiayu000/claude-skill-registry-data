---
name: generate
description: Regenerate a specific layer (schemas, services, routes, hooks, ui) or all layers. Use after schema changes or when generated code is out of date.
user-invocable: true
allowed-tools: Bash, Read, Grep
---

Regenerate code for the specified layer: $0

Valid arguments: schemas, services, routes, hooks, ui, all

Map to commands:
- schemas -> `pnpm generate:schemas`
- services -> `pnpm generate:services`
- routes -> `pnpm generate:routes`
- hooks -> `pnpm generate:hooks`
- ui -> `pnpm generate:ui`
- all -> run all five in order: schemas, services, routes, hooks, ui

After generation, run the corresponding layer validation to confirm success:
- schemas -> `pnpm contracts:check`
- services -> `pnpm services:check`
- routes -> `pnpm routes:check`
- hooks -> `pnpm hooks:check`
- ui -> `pnpm ui:check`
- all -> run `pnpm validate:all`

If $0 is empty, ask which layer to regenerate.
