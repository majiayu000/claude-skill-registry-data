---
name: no-catch-all-layer
description: Use when creating, naming or extending a layer in an OSDD codebase (any stack), or deciding where a piece of code belongs. Never name a layer after its position in the architecture (core, common, shared, utils, transverse) rather than the one thing it owns — a positional name refuses no file, so every unplaced piece of code lands there until the layer is the application.
---

# no-catch-all-layer

`skills/laravel-conventions` §10 point 5 (and its stack equivalents) covers *how* a layer-package
decomposition is scaffolded; this is the rule that keeps whatever gets scaffolded from collapsing back
into one folder everything depends on. Triggers on naming a new layer, "où je mets ce code", "je le mets
dans le socle/common", and on a layer nothing seems to be outside of.

## When
Creating an OSDD layer (functional, technical, or a module), naming one, or choosing where a class
goes that doesn't obviously belong to the feature at hand.

## Steps

### 1. A layer is named for what it owns, not where it sits
1. **Every layer is named after one business domain or one named infrastructure concern.** Banned as
   a layer name, in any stack: `core`, `common`, `shared`, `base`, `socle`, `transverse`, `utils`,
   `tools`, `helpers`, `misc`, `framework` — and their translations. Each names a position, not a
   responsibility.
2. **A positional name is not a boundary.** A layer called `billing` refuses a session-handling class
   by its name alone; a layer called `transverse` refuses nothing, because nothing is outside
   "transverse". The name is the only thing stopping a file from landing in the wrong layer — remove
   it and the boundary is gone even though the folder still exists.
3. **The placement question: would a second module need this?** No → the module itself, nowhere
   else. Yes, and it's business → a shared functional layer, named for the domain. Yes, and it's
   infrastructure → its own named technical layer (`authentication`, `object-storage`, `tenancy`), one
   concern per layer. Answering "common" to this question means the owner hasn't been identified yet.
4. **Shared functional domains and product modules sit on opposite sides of a dependency direction,
   not two flavours of the same folder.** Filing them as peers turns a dependency rule into a naming
   preference, and the rule erodes without anyone deciding to break it.
5. **`technical/` names a bucket of layers, not a layer.** A single `technical/common` merges
   authentication, events and storage into one package every layer imports — the same mistake as a
   business-side catch-all, one level down. Split infrastructure by concern the same way domains are
   split by domain.

### 2. Why a catch-all layer is expensive, not just untidy
1. **It inverts the dependency graph.** Everything depends on it, so it can never be versioned,
   tested or extracted on its own, and a change inside it has the whole application as its blast
   radius — the bounded blast radius OSDD exists for is gone while the directory structure still
   claims otherwise.
2. **It hollows out the domains it was supposed to support.** Once it answers everything, the
   functional layers degrade to models and migrations with no behaviour, and the business rules end
   up in the one place that knows about every domain — a god class at layer scale (`skills/code-baseline`).
3. **It only grows.** Code lands there because it had nowhere else to go, and the next contributor
   reads a precedent, not a mistake.
4. **It defeats review.** "Which domains does this touch?" is answerable by reading a layer name — it
   stops being answerable for a layer that owns everything.

### 3. Hold the boundary with a tool, not with review
1. **The drift arrives one import at a time, over months, and no reviewer catches all of them.**
   Enforce the direction mechanically: a dependency checker (`deptrac`, or the stack's equivalent)
   declaring which layer may see which — infrastructure never sees business, a module never sees
   another module.
2. **An architecture test asserts the discovery itself**, not only the direction: every directory
   holding layers is a declared bucket, and every layer is attributed to exactly one. A bucket left
   out of that declaration yields zero layers for itself, which reads like a healthy repository while
   silently exempting everything inside it from the rule.
3. Both checks are cheap and fail on the commit that breaks the rule, not on the quarter someone
   noticed.

### 4. An existing catch-all is a remnant being dissolved, never a destination
1. **Nothing new is ever added to it.** A domain with no layer yet gets one; dropping it into the
   catch-all "for now" is how the dissolution loses ground every story until the layer outlives every
   plan to remove it.
2. **Pick the next extraction by incoming coupling** — how much the rest of the catch-all still
   depends on the piece being pulled out. A piece nothing inside it depends on leaves cleanly; one it
   depends on needs that dependency inverted first, or the extraction just relocates the cycle.
3. Don't start the dissolution as a drive-by inside an unrelated feature branch: name it as its own
   piece of work, extract the one piece the current change already touches if it leaves cleanly, and
   keep going from there.

## Output / checkpoint
Every layer's directory name states the one domain or concern it owns; nothing in the tree is named
for its position. A dependency checker and an architecture test both exist and both fail on a
violation, rather than the rule living only in review comments.

## Guardrails
- Scaffolding `core`/`common`/`shared` on day one "for the plumbing" is not a temporary convenience —
  there is no later sorting-out, that layer is the final destination.
- Renaming a catch-all (`socle` → `shared`) changes nothing; both names accept every file. Split it,
  don't rename it.
- A technical layer deciding a business rule (when an order ships, who may be invited) rather than
  merely exposing a shared type has crossed back into being a catch-all, whatever it's called.
- "Just one shared helper" is never one — see `skills/laravel-no-superficial-factorisation` (or the
  stack equivalent) for why "used twice" isn't a reason to cross the boundary.

## Origin
Mined from the org catalogue's `global` plugin, `no-catch-all-layer` (commit shipping 2026-09-21, a
new-file addition to the `global` and `laravel` plugins covering OSDD layer naming and multi-tenant
data residency). Mechanism kept: the positional-vs-responsibility naming test, the placement question,
the functional/module/technical dependency-direction split, the dissolution doctrine for an existing
catch-all (never a destination, ordered by incoming coupling), and enforcing the boundary with a
dependency checker plus an architecture test rather than through review alone. The naming bans are
generic (folder-naming words any stack could reach for) so nothing needed genericising under rule C.
`deptrac` is kept by name — it's a public open-source tool, not an internal one. Left out: nothing —
the source skill was itself already stack-agnostic and already anonymous. Prose rewritten throughout;
no text copied from the source file.
