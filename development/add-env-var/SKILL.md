---
name: add-env-var
description: Add, rename or remove an environment variable or setting for any service, locally and in every deployed environment. Use when code needs a new setting, a secret, a provider key or a feature switch.
argument-hint: <NAME> <service>
---

# Add an environment variable

A variable lives in up to six places, and all of them change together.

1. **Validate it** where the service reads it, with a type and bounds:
   - a Nest service: its `src/env.ts` (t3-env, zod). One several services share:
     a fragment in `packages/nest-common/src/env.ts`, spread into each;
   - web: `apps/web/src/env.ts` (server-only; the browser gets nothing);
   - ai: a field in `apps/ai/app/settings.py` with `alias="<NAME>"` and a constraint;
   - mobile: build-time in `apps/mobile/app.config.ts`, runtime `EXPO_PUBLIC_*` in
     `src/lib/config.ts` (public: never a secret).
   Import `env`; never read `process.env` elsewhere.
2. **A feature switch?** Optional features are on only when their variables are set:
   add it to `features` in `apps/api/src/features.ts` (both-or-neither for pairs) and
   to `FEATURES` in `packages/contracts/src/api/system.ts`, so disabled procedures answer
   `FEATURE_DISABLED` and clients hide the UI.
3. **Production guard.** A test-only value (a fake URL, a loopback address, a local
   stand-in) is refused at boot when `NODE_ENV=production`, next to the existing guards
   at the end of the service's `src/env.ts`.
4. **`.env.example`**, in its section, with a comment saying what it does and what
   switches on. A secret gets `change-me` so `bun run setup` generates it
   (`packages/testing/src/secrets.ts` knows the formats); an optional one stays empty.
   Tests run with these values, never `.env`.
5. **`docs/environment.md`**: a row in the service's table (name, who reads it, default,
   what it does).
6. **Deployed.** A plain setting: the service's `env` in
   `deploy/charts/stack/values.yaml`, or per environment in
   `deploy/environments/<env>/stack.yaml`. A secret: the service's SOPS Secret
   (`deploy/environments/<env>/secrets/<service>.sops.yaml`; the user edits it with
   `sops`, you never decrypt it), and its line in the templates in
   `docs/new-project.md` and the list in `deploy/README.md`.

Locally: `bun run setup` adds the new key to `.env` (the doctor fails until then);
`bun run env:set NAME=value` sets it. Never read `.env`.

Removing one: delete it from all of the above in one change; the doctor then reports it
as stale in existing `.env` files, and `bun run env:unset NAME` deletes it.

## Done when

- `bun run check-types` and `bun run test` pass (every suite runs with `.env.example`'s
  values, so a required variable missing there fails them).
- The service starts with the example value (`bun dev`, in the background) and refuses
  a bad one with a readable message.
- `bun run charts:check` passes if `deploy/` changed.
- The `docs-sync` agent reports nothing out of date; the `security-reviewer` agent for a
  secret.
