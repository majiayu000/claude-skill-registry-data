---
name: afk-codebase-design
description: money-tracker.online's own half of the codebase-design skill - its house idiom, seams, dependency examples, test layout and risk-high interfaces. Shadows the shared base of the same name; read that base for the vocabulary and the rules.
---

# AFK codebase design in money-tracker.online

**Read `.ai/skills/afk-codebase-design/SKILL.md` first.** That file is the shared half, kept identical by hand across the repositories that use this pipeline (ADR 0021 retired the renderer): the vocabulary (module, interface, depth, seam, adapter, leverage, locality), the five rules, the dependency-category skeleton, the design-it-twice procedure and the done-when. `afk-triage`, `afk-to-tickets` and `afk-architecture-review` read that path literally, so those terms are guaranteed to be the same everywhere.

This file is the other half: what is true only here. It shadows the shared file by name in the cockpit's registry - `.ai/cezar/skills` is scanned before `.ai/skills` and the first of a name wins - so an agent that loads the skill by name gets **this** file and must read the shared one alongside it. Neither half is complete on its own.

## The house idiom: ports passed in, never looked up

This repo's seams are **narrow structural types passed as arguments**, not modules reached through an import. `LedgerBatchPorts` (`src/server/ledger/batch.ts`) is the shape to copy: the batch logic names exactly what it needs, and the caller supplies it.

Two conventions come with it:

- **Time is a dependency.** `src/server/clock.ts` exists so that no module reads the wall clock directly. A function whose result depends on "now" takes it as an argument.
- **Name the port for the role, not the vendor.** `PolarClient` (`src/server/billing/polar-client.ts`) is the exception that proves it - it is named for the vendor because it models that vendor's API surface, and everything above it speaks in roles.

**There is no DI container.** Dependencies are plain object literals passed as arguments. Do not introduce a framework-level injection mechanism.

## Money is the load-bearing constraint

`docs/MONEY.md` is not background reading. Money in this repo has rules about representation, rounding and currency that a plausible-looking change breaks silently, and SDLC.md lists money among the `risk-high` areas for that reason. Read it before touching any amount, and prefer the existing helpers in `src/lib/money/` to arithmetic you write yourself.

CODE_REVIEW.md makes this mechanical: **a money-touching write path needs its own test.**

## Dependency categories (where to put the seam)

| Category             | Example in money-tracker.online                                                                                                       | Test with                                           |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| In-process           | enum tuples (`src/lib/enums.ts`), money types and arithmetic (`src/lib/money/`), i18n catalogue loading (`src/lib/i18n/catalogue.ts`) | the real code                                       |
| Local, substitutable | the D1 handle, R2, KV, the clock (`src/server/clock.ts`)                                                                              | an injected fake; the clock takes an explicit value |
| Remote you own       | the task queue (`TaskMessage`, `src/server/queue/messages.ts`)                                                                        | the zod envelope plus a handler called directly     |
| True external        | Polar (`PolarClient`), email delivery (`NotificationEmailEnqueuer`, `src/server/notify/email.ts`)                                     | the port, filled with a stub                        |

## Seams money-tracker.online already has

Build on these before inventing new ones.

| Seam                                                                                          | What varies across it                                                                         |
| --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `TenantScope` (`src/server/repos/scope.ts`) / `TenantRepository` (`src/server/repos/base.ts`) | the database handle. **Not** the tenant filter - that boundary is the subject of ADR 0002     |
| `LimitResolver` (`src/server/repos/base.ts`)                                                  | how a plan limit is resolved, without the repository knowing about plans                      |
| `LedgerBatchPorts` (`src/server/ledger/batch.ts`)                                             | everything a ledger batch needs, named explicitly                                             |
| `ParserRegistry` (`src/server/import/registry.ts`)                                            | a statement format is one registered parser                                                   |
| `PolarClient` (`src/server/billing/polar-client.ts`)                                          | the payment provider                                                                          |
| `NotificationEmailEnqueuer` (`src/server/notify/email.ts`)                                    | how a notification becomes a queued email                                                     |
| `TaskMessage` (`src/server/queue/messages.ts`)                                                | a job kind is one member of the zod envelope plus its handler in `src/server/queue/handlers/` |
| `CatalogueLoader` (`src/lib/i18n/catalogue.ts`)                                               | where translation catalogues come from                                                        |

## Where the tests go

Four Vitest projects, and they are not interchangeable:

- `ui` - jsdom, for components.
- `server` - plain Node, for `src/server/**` with bindings passed in.
- `workerd` - the real Workers runtime, for what genuinely needs it.
- `tooling` - policy outside `src/**`: scripts, hooks, config.

Choosing `workerd` when `server` would do makes a slow test that hides a missing seam. Reach for it only when the behaviour under test _is_ the runtime.

## What is risk-high here

From SDLC.md: **auth, sessions, data scoping, money, schema migrations, shared contract surfaces, or broad cross-cutting edits.** When signals conflict, pick the higher label and say why. `qaGate` is on: a PR carrying `needs-qa` does not merge without `qa-approved`.

Layering rules that are blockers in CODE_REVIEW.md, and so constrain where a seam may go:

- Every query goes through the tenant-scoped base repository. **A new repository function needs its tenant-isolation case.**
- A server function validates its input with Zod at the boundary **and parses it a second time in the handler**. Both are required; removing either is a blocker.
- `components/ui` holds React Aria primitives that never fetch and never import from the server.
- A money-touching write path has its own test.

## Design it twice: which interfaces

Run the design-it-twice procedure from the shared file when a new or changed interface touches the tenant repository base, a ledger or money path, a D1 migration, the queue envelope or auth.
