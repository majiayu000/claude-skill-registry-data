---
name: colocation-first
description: How to place, name, and organize files and modules in this codebase. Use whenever you create a new file, add a feature or sub-feature to a route, split a growing file, name a file or folder, or decide whether code should stay colocated under a route or move into a shared module. Apply this BEFORE writing new code or settling on a folder structure — even when the user never says "architecture" or "where should this go". This is the generative counterpart to the improve-codebase-colocation audit skill (which audits existing code for placement); reach for colocation-first whenever you are actively writing or placing code.
---

# Colocation First

One rule, applied before you write or place any code: **code that changes together lives together.** Before you create a file, name it, split a growing one, or pick a folder, ask: *when this feature changes, how many places must I understand and edit?* Drive that number toward **one**.

> Full naming tables, types-file rules, the worked premium-ads example, and the reasoning behind every rule live in [`references/route-owned-modules.md`](references/route-owned-modules.md) — the single source of truth. Read it when a detail isn't spelled out here. Term definitions (module, interface, seam, adapter, barrel, promotion, …) live in [`references/glossary.md`](references/glossary.md).

## Where does this code go?

Decide in this order:

1. **One route owns it** (the common case) → keep it under the route, behind **one** private, domain-named folder (search route → `_search/`).
2. **Two or more routes use it today** → promote to `src/modules/<domain>/`. Present reuse only, never hypothetical. A cross-route need is the promotion signal — never reach into another route's private folder to satisfy it.
3. **Plumbing** (transport, third-party wrapper, no domain meaning) → `src/lib/<thing>/` if shared, else the owning module's `internal/`.

Never exile route code to `src/modules` just to slim down `app/`. Understanding the route then means hopping away from it. A noisy route folder is fixed with a private `_<domain>/` subfolder, not by moving behavior away from what it serves.

## Name and group for the domain

- **Group by the concept that changes together** (`premium-ads/`, `search-results/`, `map-search/`) — never by technical kind (`_components/`, `_services/`, `_hooks/`, `_model/`), and never those same buckets pushed one level deeper (`_search/components/`).
- **Name domain-first:** `<domain-concept>[-specific-behavior][.<role>].ts`. Add a role suffix only when it carries real meaning: `.types.ts`, `.actions.ts`, `.server.ts` (pair with `import 'server-only';`), `.client.ts`, `.test.ts`, `-adapter.server.ts` / `-adapter.client.ts`.
- **Ban vague suffixes** — `.utils`, `.helpers`, `.service`, `.domain` — they hide ownership. Name the behavior instead: `select-premium-search-ads.ts`, not `premium.utils.ts`.

## Public surface and privacy

A **module interface file** is a domain-named file callers may import directly because it represents a stable capability — "public" to its route/module, not the whole app. It owns behavior or invariants, exposes a small intentional surface, and survives internal refactors without forcing caller changes.

Privacy is positional: root files are public, `internal/` files are private, and nothing imports another module's `internal/`. **Don't create `internal/` by default** — a single interface file with private functions is usually enough; reach for it only when enough hidden files justify the structure.

**No barrels.** No `index.ts`, no `export *`. Import directly from the interface file — it keeps jump-to-file fast, seams honest, and client code out of the server graph. A central file (`search.ts`) is allowed **only if it owns real behavior** (orchestration, composition, invariants), never as a re-export hub.

## Earn every folder and seam

Start flat — a module can be a single file. Add a folder or seam only when it gives callers a **smaller interface** *and* maintainers **better locality**. **Deletion test:** if removing the feature would mostly delete one folder, the folder earns its keep. If a structure only moves complexity around, drop it. Don't extract for a second caller, a deeper bucket, or a future that hasn't arrived yet.

## Before you commit a placement

- Lives next to its owner? Route-owned → `_<domain>/` under the route.
- Grouped by concept — not technical kind, nor those buckets pushed one level down?
- Name says what it owns, domain-first, with a role suffix only if it helps?
- About to write `index.ts` or `export *`? Stop.
- Extracting to `src/modules` for one caller? Stop — wait for the second route.
- New folder or `internal/`? Does the deletion test actually justify it yet?
- Need the tables, types-file rules, premium-ads shape, or rationale? → [`references/route-owned-modules.md`](references/route-owned-modules.md).
