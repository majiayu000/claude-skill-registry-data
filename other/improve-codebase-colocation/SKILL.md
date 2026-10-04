---
name: improve-codebase-colocation
description: Find placement and organization opportunities in a codebase, measured against the colocation-first conventions. Use when the user wants to improve code organization, colocate a feature scattered across technical folders (src/services, src/model, src/hooks, src/store), pull route-specific code back under its route, kill barrels, fix premature promotion to shared modules, rename vague *.utils.ts files, or make a codebase more colocated and AI-navigable. This is the audit counterpart to colocation-first (which places code as you write it).
disable-model-invocation: true
---

# Improve Codebase Colocation

Surface placement friction and propose **colocation moves** — relocations that pull code which changes together into one place. The audit counterpart to `colocation-first`: that skill places code as you write it; this one finds code already in the wrong place.

> The colocation vocabulary — route-owned module, module interface file, `internal/`, barrel, promotion, deletion test, concept-vs-bucket — and the worked premium-ads example live in colocation-first's [`references/route-owned-modules.md`](../colocation-first/references/route-owned-modules.md) and [`references/glossary.md`](../colocation-first/references/glossary.md). That is the single source of truth: read it before grilling a move (step 3), and don't restate or drift from it here.

## The question every candidate answers

> When this feature changes, how many places must I understand and edit?

Surface a **candidate** when that number exceeds **one** because of *where code lives* — not how deep its modules are. Depth belongs to the sibling skill `improve-codebase-architecture`; don't re-litigate it here.

## 1. Explore

Map the route tree and the shared roots (`src/services`, `src/model`, `src/hooks`, `src/store`, `src/components`, `src/lib`, `src/modules`) first. An Explore sub-agent walks the tree without flooding context.

Hunt these signals — most are greppable. Each carries the tag you'll use in the report:

- **`scattered-feature`** — one concept split across `src/services/X`, `src/model/X`, `src/hooks/useX`, `src/store/X`. Changes-together not living-together; strongest signal in a root-by-kind layout.
- **`technical-bucket`** — `_components/`, `_services/`, `_hooks/`, `_model/`, `_utils/` under a route, or those same buckets pushed one level deeper inside a `_<domain>/`.
- **`premature-promotion`** — a `src/modules` / `src/services` module imported by exactly one route → belongs under that route.
- **`barrel`** — an `index.ts` / `export *` hub that blurs seams and slows jump-to-file.
- **`vague-suffix`** — `*.utils.ts`, `*.helpers.ts`, `*.service.ts`, `*.domain.ts`; the concept needs a sharper name.
- **`cross-route-import`** — a route reaching into another route's private `_<domain>/`; a promotion signal, never a license to import internals.
- **`bloated-route`** — many files directly under a route instead of behind one `_<domain>/`.
- **`internal-misuse`** — `internal/` created for a single file, or absent while raw API/response shapes leak into a module's public surface.

**Filter false positives with the deletion test and the promotion rule.** A `src/lib/*` adapter or a `src/components/ui/*` used by many routes is correctly shared — leave it. One caller = colocate; two+ routes = legitimately shared. Present real reuse, never hypothetical.

## 2. Present candidates as an HTML report

Write a self-contained HTML file to the OS temp dir so nothing lands in the repo: resolve `$TMPDIR` (fall back to `/tmp`, or `%TEMP%` on Windows) and write `<tmpdir>/colocation-review-<timestamp>.html`. Open it (`open` / `xdg-open` / `start`) and tell the user the absolute path.

Each candidate card carries: **Files**, **Problem** (one sentence), **Solution** (one sentence), **Wins** (bullets in colocation vocabulary), its **signal tag** from step 1, a **before/after file-tree diagram** (scattered tree → one colocated `_<domain>/` tree), and a **strength** badge (`Strong`, `Worth exploring`, `Speculative`). End with a **Top recommendation** section. See [HTML-REPORT.md](HTML-REPORT.md) for the scaffold, diagram patterns, and styling.

Then stop. Do not move any files. Ask the user: "Which of these would you like to explore?"

## 3. Grill the chosen move

Once the user picks a candidate, walk it with them before touching files:

- **Colocation or promotion?** One route owns it → under the route. Two+ routes → `src/modules/<domain>/`.
- **What's the shape?** Domain-first folder name; which file becomes the module interface file; what hides in `internal/` — and whether there's enough to justify `internal/` at all.
- **What moves?** Which files relocate, which imports rewrite, which barrels die, which vague names sharpen.
- **Does the deletion test hold** for the resulting folder?

Settle side effects inline: if the move surfaces a cross-route dependency, decide whether it's a promotion before any file moves.

## 4. Execute the move

Once the shape is locked, perform the relocation — mechanical and safe. See [RELOCATION.md](RELOCATION.md) for order of operations, import rewriting, barrel removal, and verification. **A move is a move: don't change behavior on the way.**
