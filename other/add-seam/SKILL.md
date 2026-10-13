---
name: add-seam
description: Put an integration that will change at scale behind one interface (a new provider, store or transport), so a later swap is a new implementation and not new callers. Use when adding a third-party integration or infrastructure piece that could plausibly be replaced as the product grows.
argument-hint: <concern>
---

# Add a seam

The README's "Scaling path" lists every seam: what's there now, what it becomes, where
the interface is, and the skill that swaps it. A seam is worth it only for something
that will change at scale; everything else is plain code.

1. **The interface**, in the one place every caller reaches it: a shared concern in
   `packages/nest-common/src/<concern>.ts` (like `storage.ts`, `crypto.ts`), one
   service's in that service (like `apps/notifications/src/channels/sms/sms-transport.ts`),
   Python in `apps/ai/app/`. The smallest set of methods the callers need, in the repo's
   terms, not the provider's.
2. **The first implementation** in its own file, the provider's SDK imported only there.
   Chosen from env in one factory (the module that provides it), so callers never name
   the provider.
3. **Its header comment** says what the interface is for, what implements it today, and
   how to swap it: the files to add, the env to set, the tests to extend. The existing
   seams' headers are the model.
4. **A local stand-in** that speaks the real protocol, for tests and local development
   (Mailpit, `packages/fake-stripe`, the fake push server), refused in production at
   boot.
5. **Tests** against the interface: a contract test the next implementation reuses, and
   integration tests through the stand-in.
6. **Docs.** A row in the README's "Scaling path" table, and a
   `.claude/skills/swap-<concern>/SKILL.md` like the others (interface, today's
   implementation, how to add one, what to test, `disable-model-invocation: true`),
   listed in `docs/README.md`'s runbooks.
7. **Boundaries.** If the provider's SDK must stay inside the adapter, a
   dependency-cruiser rule in `.dependency-cruiser.cjs` enforces it.

## Done when

- `bun run lint` and `bun run check-types` pass, and the tests pass against the
  stand-in (`bun run test:integration`).
- Nothing outside the adapter imports the provider (`Grep` for its package name).
- The `reviewer` agent reports nothing blocking.
