---
name: add-port-adapter
description: Add or extend a driven port and its adapter in agent-office's hexagonal core — storage/persistence, OS integration, clock/scheduling, external services, a new notification channel. Use whenever the core needs something new from the outside world.
---

# Add a driven port and adapter

Rules: `ARCHITECTURE.md` (ports are additive; only the composition root knows concrete classes), `TESTING.md` (TDD; contract suites are mandatory).

1. **Can an existing port do it?** Check `packages/core/src/ports/driven.ts` first. Prefer a **new, narrow** port over growing an existing one, and never change an existing method's signature.
2. **Red: contract suite.** Add `xxxContract(name, make)` in `packages/core/test/contracts/`. It describes the behavior every implementation must have: round trips, errors as domain errors (`ValidationError`, …), idempotency and isolation.
3. **Fake.** Add a fake or recording implementation to `packages/core/test/fakes/index.ts` and run it through the contract in `packages/core/test/fakes.test.ts`.
4. **Use case.** Write a failing test in `core/src/application/*.test.ts` using the fake, then implement it so it depends on the port only. Wire it into `createOffice` (`OfficeDeps`) if it's office-wide.
5. **Real adapter.**
   - Node: `packages/adapters/src/<area>/`. Electron: `packages/desktop/src/main/adapters/electron-*.ts`.
   - Run the same contract suite against it, using temp dirs and never real user files.
6. **Wire it** in `packages/desktop/src/main/composition.ts` (Electron objects come in through `Shell`, built in `index.ts`). Extend `composition.test.ts`.
7. `make arch` (the dependency rule) and `make check`. For Electron adapters, also `make build test-ui`.
