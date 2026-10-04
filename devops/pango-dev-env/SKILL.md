---
name: pango-dev-env
description: "Invoke first for Pango backend-app development. Establish worktree, slot, test, store, and environment ownership before running the stack, tests, Artisan, Composer, npm, Tinker, or pgcli. Route detailed local and production work to the current project skills."
---

# Pango environment preflight

Use the repository `pango` CLI from the target worktree. The worktree selects
the branch, Compose project, slot lease, database, and test resources. Keep one
branch per worktree because switching branches under live resources can strand
them.

Load the project `pango-local-dev` skill for startup, current context, database,
logs, queues, tests, and service diagnosis. Treat current CLI help as the command
source of truth. Read `wiki/infrastructure/local-development.mdx` when setup or
environment background is needed instead of loading it for every focused test.

## Execution host

Follow the project's `AGENTS.md` and `pango-local-dev` for host selection.

For Charlie's local Shopify setup and manual review, run `pango-ready --help`
then use `pango-ready`. It rejects the E2E store and composes repository commands,
but it talks directly to local Docker Compose and is not the remote-development
path.

## Slot, store, and resource ownership

Before starting, switching, or tearing down a stack, run `pango dev list` and
follow this order:

1. Reuse the current worktree's lease.
2. Otherwise lease an available ordinary development slot through the supported
   `pango` flow.
3. If every ordinary slot is leased, report the active leases and wait. Never
   take another worktree's lease.

Shopify app and slot creation are persistent infrastructure changes. Run
`pango setup add-slot`, `pango app create`, `pango dev add-app`, or
`pango slot provision` only when Charlie explicitly asks after seeing the
existing pool.

Keep E2E infrastructure isolated. Never lease, repurpose, install, seed, or
modify an E2E app, slot, database, or store for ordinary development. An
unleased E2E app record is not an available development slot.

`charlie-pango-test.myshopify.com` is the ordinary development store.
`charlie-pango-e2e.myshopify.com` is reserved for E2E. State the target store
before opening a Shopify install URL.

Manage app stacks through `pango dev ...`. Confirm ownership before teardown.
Leave other worktrees and shared infrastructure untouched. Use raw Docker only
for read-only diagnosis; the branch-aware CLI owns lifecycle actions.

## Changed local secrets

Before starting the stack with a changed secret, prove the boundaries in order:

1. Check the stored value through the provider's safe authentication endpoint.
2. Check that the Pango command process sees a nonempty value without printing it.
3. After container creation, check the value's presence or length in both `web` and `worker` before exercising the application.

Commands launched through the `process` tool can resolve Homebrew fnox before the repository pin. Resolve secrets there through `mise exec -- fnox`; verify its version before an expensive run when profile inheritance is involved.

Container restarts retain their original environment. Attempt to apply a changed secret with one deliberate `pango dev down` followed by `pango dev run`, then confirm the new containers received it. If they did not, stop setup and report the environment injection boundary instead of repeating startup. Run Pango CLI commands sequentially because the `pango` alias may run `bun install`. Read the command result before accepting exit code zero as proof because a no-op can still exit successfully. After a full startup failure, identify the failed boundary before another full run.

## Verification

Verification is a question, not a stage. Run a check only when its failure could
reveal something about the changed contract.

1. For application behavior, run the smallest existing test that executes the
   changed path. If no test observes it, use the promised surface.
2. For UI behavior, inspect the rendered interaction. Typechecks and unit tests
   do not prove it.
3. For metrics, logging, telemetry, configuration, prose, and mechanical edits,
   use the narrow static or manual check that observes the change. Zero automated
   tests can be correct.
4. Use the full unit suite only when no focused target represents the risk. Do
   not run it merely to duplicate CI.
5. Use mockless E2E only when the claim crosses a real external boundary. Load
   `pango-e2e-mockless` first.

Before a baked test on local Docker, check for an active Buildx job:

```bash
docker buildx history ls --filter status=running --format '{{.Name}}'
```

If it prints a build, use a compatible warmed mounted test or wait. Do not start
another baked build on that daemon.

For a fast PHP loop, load the project `pango-pest-mounted` skill. Mounted mode is
valid only after this worktree and Docker host have a warmed exact image, and
only while dependency, runtime, local-library, Rust, Enigma, frontend, and portal
inputs remain unchanged.

Run checks expected to exceed 30 seconds through the `process` tool. Use a specific name, exact working directory, and terminal notifications. Keep progress in logs unless one targeted match needs attention. A green result stays valid until relevant code, fixtures, dependencies, or environment change.

## Branch preflight

Use focused tests and targeted hooks while the worktree is dirty. Treat
`pango check` as an optional local CI mirror, not a completion ritual. Run it
when a material or broad committed branch diff needs a full changed-range check,
or when the user explicitly asks to mimic CI. Skip it for a small follow up
already covered by focused tests and a targeted format or static check.

When the full check adds evidence, commit first because its Prek hooks validate
the committed range ending at `HEAD` and temporarily stash worktree edits.
Refresh the default branch with `git fetch origin master`, then run
`pango check origin/master`; `pango check master` may use a stale local branch.
If the check cannot start because a host tool is missing, report the tooling gap
and stop. Do not install application dependencies or improvise another check
path only to satisfy this step.

## Local setup and debugging gotchas

Manual dashboard access uses **Sign in through Shopify**. A fresh Shopify-created
local user has a random password and no reusable email-and-password login. For
automated browser review, follow `pango-debug` and remove its temporary password
and session afterward.

`pango dev run` migrates the leased database and regenerates Enigma entities.
If the slot database lacks its Store row, open the leased app's Shopify install
URL once so token exchange recreates the Store and OAuthAccount, then run
`pango db seed`. Verify the store and location prerequisites instead of adding
manual reference-data loaders.

Keep these observed failure mappings:

- A builder preview that reports unavailable or serves stale frontend code can
  mean the `frontend` service is down and the app fell back to baked assets.
  `web/public/hot` must contain the slot frontend origin. Check
  `pango dev logs frontend`.
- Portal inspection that differs from the builder preview means published portal
  assets may be stale. Run `pango dev portal-assets` after editing
  `returns-portal/` while the stack is up.
- `curl` returning `000` for a local HTTPS port can be an SNI mismatch. Use the
  tunnel URL or resolve the leased hostname to `127.0.0.1` with the port from
  `pango dev current`.
- In Tinker scripts, use fully qualified class names, raw strings for enum
  columns, and `Model::withoutEvents(...)` for domain-model fixture writes.
  Never kill Tinker during a transaction because it can leave row locks.
- Enigma entities use PostgreSQL integer types. After migrations that affect
  Enigma-read tables, run `pango db migrate`, then use `cargo check` in
  `crates/enigma` when validating the Rust consumer.

## Production routes

Skip local stack, slot, wiki, and `pango-ready` setup for production-only work.

- For production PostgreSQL data, load `pango-prod-data`. `pango prod query`
  owns the production target, AWS authentication, resource discovery, parameter
  binding, and output limits.
- For a multi-system production incident, load `pango-production-debugging`.
- For deployed PHP, jobs, Shopify Admin, queues, or DLQs, follow the production
  debugging route and its dedicated production tools.

Do not replace these paths with raw RDS Data API, ECS, queue, or token commands.
Refresh AWS only when the owning production workflow reports an expired session.
