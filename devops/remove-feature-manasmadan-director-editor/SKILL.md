---
name: remove-feature
description: Remove an optional feature a product doesn't need (Director and the AI service, file uploads, Google sign-in, captcha) completely - code, tables, env, copy, docs and tests - without breaking a running deployment. Use when the user wants to drop a feature from their product, not merely leave it switched off.
argument-hint: <feature>
disable-model-invocation: true
---

# Remove a feature

Every optional feature is off until its variables are set (`apps/api/src/features.ts`),
so an unused one costs code, not runtime. Remove it when the product will never use it
and the code is in the way. Work on a branch; the change is large and goes through
review like any other.

## Find everything it touches

Start from its names: `git grep -n -i "<feature>"` for its module names, env variables,
error codes, events, queues and i18n namespaces. The table is where each one lives:

| Feature | Its code and config |
|---|---|
| Director and the AI service | `apps/ai`, `packages/ai-client`, `apps/api/src/modules/{ai,director,live,shorts}`, `packages/contracts/src/api/{director,shorts}.ts`, `packages/client/src/api/{director,shorts}`, `apps/web/src/modules/{director,shorts}` and their routes, `packages/fake-google`, `ai.prisma`, the `ai-director` and `ai-review` queues, `AI_*`, `DIRECTOR_*`, `GOOGLE_*` other than `GOOGLE_CLIENT_*`, `YOUTUBE_*`, `LIVE_*`, the `ai` and `ai-worker` chart services and image, CI's `python` job, `docs/director.md`, `docs/python-services.md` |
| File uploads | `apps/api/src/modules/files`, `apps/worker/src/files`, `packages/nest-common/src/storage.ts`, `packages/contracts/src/files.ts` and `api/files.ts`, `files.prisma`, the `files` queue, `S3_*`, `FILE_SCANNER`, `CLAMAV_URL`, RustFS and ClamAV in `docker-compose.yml` and the charts, `avatar.spec.ts` |
| Google sign-in | `socialProviders` in `apps/api/src/auth/auth.ts`, `GOOGLE_CLIENT_*`, the Google button in the auth pages, `google.spec.ts` |
| Captcha | `apps/web/src/components/captcha.tsx`, the captcha plugin in `apps/api/src/auth/auth-plugins.ts`, `TURNSTILE_*`, the Turnstile widget in `infra/tofu/modules/cloudflare`, `captcha.spec.ts`, `captcha.integration.test.ts` |

## Remove it, in this order

1. **Clients first**: its pages, components, hooks and routes in `apps/web` and
   `packages/client`; its entries in `APP_PATHS` and navigation.
2. **The API and services**: the module and its registration in `app.module.ts` and
   `src/rpc/router.ts`; its contract files and their entries in
   `packages/contracts/src/api/index.ts`; its switch in `features.ts` and `FEATURES`
   (`packages/contracts/src/api/system.ts`); processors, queues in
   `packages/jobs/src/queues.ts` and routes in `eventSubscribers`; error codes only it
   throws.
3. **Events.** Stop emitting its events, but leave their names in
   `packages/contracts/src/events.ts` and the audit labels in i18n: the audit log still
   shows past entries, and the events-compat check refuses a removed event.
4. **The database, expand then contract.** The release that removes the code keeps the
   tables: the previous release still runs against the schema during the rollout and
   after a rollback. Drop the tables, grants and functions in a later release's
   migration, once nothing running reads them (the db-change skill), and remove the
   models from `packages/db/prisma/schema/` in that same change.
5. **Env and deploy**: its variables from each `src/env.ts`, `.env.example`,
   `docs/environment.md`, the chart values and the Secret templates in
   `docs/new-project.md`; its chart services, add-ons, images (`docker-bake.hcl`, the
   workflows' image lists) and compose services. Tell the user which SOPS keys to delete
   (you don't edit those files).
6. **Copy.** Its i18n keys, except the audit labels above.
7. **Docs and runbooks**: the README (the feature list, "What's inside", "Scaling path"
   rows and their `swap-*` skills if the seam goes too), `docs/README.md`, the doc that
   covers it, the relevant `CLAUDE.md` files and rules.
8. **Tests**: its unit, integration and e2e tests go with the code; tests of other
   features that used it as a fixture move to something that stays. Every remaining
   file stays at 100%; if one drops, the remaining code lacks tests (the write-tests
   skill).
9. **Dependencies** only it used: `bun remove <pkg> --cwd <workspace>` (the user
   approves dependency changes); knip lists what's left unused.

## Done when

- `git grep -n -i "<feature>"` finds only the kept event names, audit labels and the
  later migration's plan.
- `bun run lint` (knip finds no unused files, exports or dependencies),
  `bun run check-types`, `bun run test`, `bun run test:integration`, `bun run test:e2e`,
  `bun run charts:check` pass, and `bun run gen` leaves no diff.
- The `reviewer` agent, and `docs-sync` for the docs, report nothing blocking.
