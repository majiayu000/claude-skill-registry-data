---
name: stack-install
description: Use to start a new Polyforms project, or to bring an existing project onto the @moifort/stack package (init, templates, Renovate, CI check, routines).
---

# Install the stack

## New project

```bash
mkdir <app> && cd <app> && git init
bunx @moifort/stack init --stacks backend,ios --set APP_TAGLINE="..."
bun install
```

Stacks: `backend`, `ios`, `ai`, `paid`, `admin`, `e2e`, `site`. `init` asks for every
placeholder the chosen stacks use that it cannot derive; derived ones (name, slug, bundle id,
repository) come from the folder name and can be overridden with `--set NAME=value`.

Then, in order, verifying each:
1. `bun run preflight` green.
2. `bun run ios:build` and `bun run ios:test` green (ios stack).
3. `bunx @moifort/stack bootstrap <app>` creates GitHub, Sentry, Renovate, GCP, and pushes
   the first commit; the Deploy workflow does the first deploy. It ends with the list of
   what needs the person.
4. Write the deployed function URL into `ios/<App>/Shared/APIClient.swift`.
5. Create or update the scheduled routines from `stack/routines/` (rule 16).
6. Fill `project-context.md`.

## Existing project

`init` never overwrites: it writes what is missing and lists what it kept. Then write a
batched plan, one batch per domain (CI, Terraform, Sentry, iOS shell, scripts), comparing each
kept file with its template and bringing the project in line batch by batch, each batch
verified and committed on its own.
