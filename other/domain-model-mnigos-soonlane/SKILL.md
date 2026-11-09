---
name: domain-model
description: Stress-tests plans and architecture against the Soonlane modules and packages, Effect ports and layers, ADRs, product docs and code reality, and maintains the UBIQUITOUS_LANGUAGE.md glossary. Use when adding a module or package, moving logic between domain/application/infrastructure/presentation, introducing a port, service or layer, naming or renaming domain concepts, resolving term conflicts, or checking a plan against the domain model.
---

# Domain Model

Use this skill to sharpen architecture and language before implementation.

## Sources

Read the relevant sources for the topic:

- `UBIQUITOUS_LANGUAGE.md`
- `CONTEXT.md` and `CONTEXT-MAP.md` when they exist
- `docs/decisions/*.md`
- `PRODUCT.md` when product behavior matters (decisions there are final)
- `ARCHITECTURE.md` for the package and module map and the server boundary
- The root `AGENTS.md` naming table and Effect layering rules
- Existing modules and at least 3 similar files before proposing folder or boundary changes

Use [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md) for context docs, [ADR-FORMAT.md](./ADR-FORMAT.md) for ADRs and [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md) for `UBIQUITOUS_LANGUAGE.md`.

## Flow

1. Identify the affected modules (see `ARCHITECTURE.md`) and packages, and which one owns the behavior.
2. Check context docs, glossary and ADRs for existing ownership, terms and decisions.
3. Compare the plan with current code behavior and the product docs.
4. Call out conflicts between language, ADRs, docs and code.
5. When the user asks to brainstorm, push back or establish a pattern, stay analysis-only until they explicitly say to proceed.
6. Ask one sharp question at a time only when code and docs cannot answer it.
7. Propose canonical terms for vague or overloaded language.
8. Keep `UBIQUITOUS_LANGUAGE.md` current: when a task introduces, renames or retires a domain term or UI label, update it in the same change (format in GLOSSARY-FORMAT.md). Update context docs only when the user asks.
9. Recommend `adr-authoring` only when the decision is hard to reverse, surprising without context, and based on a real trade-off.

## Soonlane Boundaries

- `packages/domain`: brands (`CalendarDate`, `UserId`) and constants shared by every workspace. No Effect, framework, ORM or RPC.
- `packages/contracts`: the oRPC contract and Zod schemas; the only API boundary between server, browser and the future desktop app.
- `packages/ui`: reusable, app-agnostic React primitives. No router, no data fetching, no domain types.
- `apps/web/src/modules/<module>/domain`: pure types, tagged errors (`*.errors.ts` with a `code` field) and helpers. No Effect services, framework, ORM or RPC imports.
- `application/`: ports (`*.port.ts`, a `Context.Service` without implementation) and services (`*.service.ts`, a `Context.Service` plus its `*Live` layer, methods via `Effect.fn('Service.method')`). Services orchestrate ports; they never touch Drizzle or HTTP directly.
- `infrastructure/`: adapters that implement ports. `*.repository.ts` runs every query through `Db.run` and never catches or translates errors; `*.layer.ts` wraps an external system as a Layer.
- `presentation/`: oRPC routers, raw HTTP handlers, middleware, components, hooks and helpers. Tagged errors become oRPC errors only in `platform/rpc/rpc.base.ts`.
- `platform/`: config, the composed `AppLive` and the single `ManagedRuntime`. A new `*Live` layer is wired in `app.layers.ts`.
- Cross-module use goes through another module's service or port; importing another module's `infrastructure/` should be flagged.
- Everything under `platform/`, `application/` and `infrastructure/` is server-only; browser code reaches it only through oRPC.

## Rules

- Use current repo architecture over generic DDD examples; there is no CQRS, event bus or outbox here.
- Apply structure selectively to the module whose ownership changes; do not reshape untouched modules.
- Promote code into a package only when a second consumer (another app, the desktop app, another package) needs it.
- Flag "task", "date", "due", "today" and "overdue" when they are used ambiguously; "today" is always the user's local calendar day.
- Do not create ADRs, tickets, commits or comments unless the user asks.
