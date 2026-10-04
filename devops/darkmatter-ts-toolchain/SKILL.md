---
name: darkmatter-ts-toolchain
description: 'The darkmatter TypeScript toolchain contract: Bun catalogs, Effect 4, effect-orpc, Postgres-first data, tsgo, Vitest, oxlint/oxfmt, changesets, Alchemy deploys, and required checks. Use when writing, fixing, building, or shipping TypeScript in a darkmatter repo. Use codebase-design for module boundaries and effect-typescript for deep Effect patterns.'
---

# Darkmatter TypeScript toolchain

Org-wide contract for TS repos (platform, nixmac-web, and friends). Align new
repos with the `darkmatter/template` catalog as the reference monorepo. The
stack is deliberate; substituting familiar defaults (npm, jest, wrangler, D1 as
the default database) creates a second convention and breaks CI.

Apply [codebase-design](../codebase-design/SKILL.md) for readability and module
boundaries. Toolchain checks support cohesive implementations and small public
interfaces; function length alone does not determine whether a helper belongs.

## Ops scripts — TypeScript, not bash

If the repo is TypeScript-only, utility and CI scripts are TypeScript
(`scripts/*.ts`, `bun scripts/ci.ts`). Do not add `.sh` files. See
[ADR-0012](../../docs/adr/0012-ops-scripts-in-typescript.md).

## Package management — Bun only

- Install: `bun install`; CI uses `bun install --frozen-lockfile`. If CI fails
  with "lockfile had changes, but lockfile is frozen", the lockfile is out of
  sync with a `package.json` — fix by running `bun install` locally and
  committing `bun.lock`; never delete the lockfile to "fix" it.
- Run scripts with `bun run <script>`; execute tools with `bun x <tool>`.
- Monorepos use Turbo + workspaces (`@repo/*` packages). Add shared code to a
  workspace package, not a relative `../../` import across apps.
- Shared dependency versions live in the root `workspaces.catalog`; package
  manifests use `catalog:` or `workspace:*` instead of repeating versions.

## Preferred stack defaults

Use these defaults unless the target repo has a documented exception:

| Area | Default |
| --- | --- |
| Runtime/package manager | Bun, workspace catalogs, Node >= 24 when Node is needed |
| Effect | Effect 4, `effect-solutions`, `@effect/tsgo`, `@effect/vitest`, `@effect/platform-bun` |
| Agents | `effect/unstable/ai` / effect-agent APIs before hand-rolled agent loops or duplicated contracts |
| Typed RPC | `effect-orpc@1.0.0-effect-v4.8` plus `@orpc/server`, `@orpc/client`, `@orpc/contract`, and `@orpc/shared` at `>=1.13`; load `effect-typescript` for usage rules |
| Data | Postgres first. Prefer Kysely + `pg` for query-heavy TypeScript, or Effect SQL Postgres for Effect-native database services. Do not pick D1 or sqlite as the default persistence layer. |
| Deploy | Alchemy-managed infrastructure, commonly Cloudflare Workers or AWS depending on the app |
| Web/UI | Vite or vite-plus, Vitest, React 19, Tailwind v4, shadcn/Radix, and the repo's shared UI package |
| Lint/format | oxlint with Effect/tsgo rules, oxfmt for formatting |

## Verify in this order

```bash
bun run typecheck   # tsgo -p tsconfig.json (NOT tsc)
bun run test        # vitest
bun run lint        # oxlint
bun run fmt:check   # oxfmt
```

Run the narrowest target that covers your change first (single test file,
single package), the repo-wide gates before handing off. All three must pass
on main; merge queues enforce required checks — prefer a PR over a direct
push even when your credentials technically bypass protection.

Test files are `<file>.test.ts` beside the source they cover; vitest picks
them up anywhere (`include: ["**/*.test.ts"]`). Do not add a `test/` or
`tests/` directory per package. The repo-root `tests/` exists only for
end-to-end tests that spawn the real server or span packages.

## Effect for meaningful I/O

Code with real I/O (network, DB, queues, retries) uses Effect — services,
Layers, typed errors, `Config` for configuration (named config files, with
env vars and flags as overrides: [ADR-0014](../../docs/adr/0014-named-config-files-over-flags-and-env.md)). Load the `effect-typescript` skill
for patterns. Plain async/await is fine for trivial glue; don't wrap a single
fetch in ceremony.

Convert a Promise-based driver to Effect at its adapter boundary and keep
internal operations in Effect. Own persistence, failure, and cleanup through
completion instead of returning success while work is still unobserved.

Keep database queries and decoding with the owning adapter. New app data starts
on Postgres unless a project-specific decision says otherwise. Use Kysely with
`pg` when the service is query-heavy; use Effect SQL Postgres when the repo is
already organizing persistence as Effect services and Layers. D1/sqlite are
valid only for narrow platform-local state, demos, or explicit edge constraints,
not as the default because they are easy to provision. Use existing typed query
tools when useful; parameterized SQL is also allowed with row validation and
behavioral query verification. A row generic does not validate data, and a
readability change does not require an ORM migration. See
[ADR-0015](../../docs/adr/0015-cohesive-modules.md).

## Deploys — Alchemy, never wrangler

- Infrastructure is code in `alchemy.run.ts`; `wrangler.toml` is prohibited.
- Deploy: `STAGE=prod bun run deploy` (per-app; check the app's README/run
  config for required env). Secrets come from `himitsu read <path>` at deploy
  time and SOPS for config — never hardcoded.
- Alchemy's config schema requires `SOPS_AGE_KEY` explicitly in env; it does
  NOT fall back to `~/.config/sops/age/keys.txt`:
  `SOPS_AGE_KEY=$(grep '^AGE-SECRET-KEY-' ~/.config/sops/age/keys.txt | head -1)`.
- Vite apps: `client` build must precede `ssr` build (hydration manifest).

## Releases

Changesets are the release source of truth: user-facing changes ship with a
`.changeset/*.md`; version bumps and changelogs are generated, not hand-edited.

## Style rules that surprise newcomers

- **Useful helpers:** extract when a name hides a meaningful decision or enables
  useful reuse. Inline pure forwarding wrappers; short or single-use helpers can
  still earn their place. Inspect existing lint diagnostics and fix unnecessary
  indirection rather than silently disabling a rule.
- **File limits:** retain configured limits; use 300 nonblank, noncomment lines
  when introducing one. Split by responsibility, or document a narrow increase
  or exception when the module is cohesive. Do not manufacture forwarding files
  to satisfy the counter.
- Conventional Commits, subject ≤50 chars; body only when the why isn't
  obvious.
- Fix problems at the source and remove obsolete compatibility paths. Keep
  explicit public re-exports and adapters that translate real external APIs;
  remove internal forwarding chains that add no useful contract.
