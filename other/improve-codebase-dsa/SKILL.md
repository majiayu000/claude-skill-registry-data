---
name: improve-codebase-dsa
description: Scan a codebase for representation opportunities — data structures and state that permit invalid combinations and would be simpler as a state machine, discriminated union, or dispatch map — present them as a visual HTML report, then grill whichever one you pick. The representation counterpart to improve-codebase-architecture (module depth) and improve-codebase-colocation (placement). Use when scattered booleans and nullable flags encode state implicitly, duplicated branching begs a map or registry, a shape is re-guessed across call sites, or async/lifecycle flags allow stale or contradictory state. Read-only — proposes, never migrates.
disable-model-invocation: true
---

# Improve Codebase DSA

Surface representation friction and propose **re-representations** — changes that make invalid states unrepresentable. Data structures, state, control flow, algorithms, ownership. The aim is fewer reachable-but-wrong states and simpler code that follows.

This is the representation axis of the `improve-codebase-*` family. Its two siblings answer different questions — send findings to the right one instead of solving them here:

- **Placement** ("when this changes, how many places must I edit?") → `improve-codebase-colocation`.
- **Module depth / seams** ("is this interface as wide as its implementation?") → `improve-codebase-architecture`.
- **Representation** ("can I construct a value the domain forbids?") → this skill.

A discriminated union sometimes deepens a module, so this overlaps architecture at the edges. Stay on the representation question; hand depth-only findings to architecture.

## Vocabulary

Use these terms exactly in every suggestion — don't drift into "flag," "type," "refactor," "cleaner."

- **representation** — how a state is encoded in data and types.
- **invalid state** — a combination the current representation permits but the domain forbids (`isLoading: true` with `error` set).
- **make invalid states unrepresentable** — the organizing principle: choose a representation in which the wrong combinations cannot be constructed.
- **state machine** — explicit states plus the transitions between them, replacing a spread of booleans.
- **discriminated union** (tagged union) — one variant per case, a tag naming the case; each variant carries only its own fields. Replaces optional-field soup and re-guessed shapes.
- **dispatch map** (registry) — data-driven branching (a keyed map, table, or reducer) replacing duplicated `switch`/`if`.
- **the right collection** — a `Set`, `Map`, or index replacing repeated linear scans.
- **the illegal-state test** — the gate, analogous to architecture's deletion test: *can I construct a value of this type that the domain says can't exist?* A "yes" is the signal you want. A "no" means the representation is already tight — leave it.

## Process

### 1. Explore

**Scope before you scan — YAGNI.** A re-representation pays off where state is churned and reasoned about, so weight the parts of the codebase that recently changed. Decide *where* to look before you look:

- If the user named a direction — a module, a state model, a bug class — take it, and skip the inference below.
- Otherwise, walk back a good stretch of history (`git log --oneline`) for the hot spots — the files that keep coming up — and let those pull your attention first. If the changes are scattered, widen the net.

Then spawn a sub-agent to walk the codebase. Don't follow rigid heuristics — read for friction and apply the **illegal-state test** to anything that smells loose. Each signal carries the tag you'll use in the report:

- **`boolean-soup`** — multiple booleans or nullable fields on one entity that permit invalid combinations → a state machine or union.
- **`optional-soup`** — optional fields that are really "present in state A, absent in state B" → a discriminated union keyed on the state.
- **`shape-guessing`** — the same object shape re-checked or re-narrowed at many call sites → one shared typed model.
- **`branch-duplication`** — the same `switch`/`if`-ladder on one tag duplicated across the codebase → a dispatch map, registry, or reducer.
- **`scan-in-loop`** — repeated linear scans, `find()`-in-a-loop, or re-derived lookups → the right collection or an index.
- **`stale-state`** — lifecycle, async, or concurrency flags (`isLoading` + `error` + `data`) whose representation allows stale or contradictory combinations → a single status union.

**Do not force an abstraction.** Prefer boring local code when it is already clear. Reject anything that only wins on stylistic consistency, hypothetical extensibility, minor line-count, or that merely moves existing branching behind a new type without removing an invalid state. If the illegal-state test comes back "no," it's a skip.

### 2. Present candidates as an HTML report

Write a self-contained HTML file to the OS temp directory so nothing lands in the repo. Resolve the temp dir from `$TMPDIR`, falling back to `/tmp` (or `%TEMP%` on Windows), and write to `<tmpdir>/dsa-review-<timestamp>.html` so each run gets a fresh file. Open it — `open` (macOS) / `xdg-open` (Linux) / `start` (Windows) — and tell the user the absolute path.

The report uses **Tailwind via CDN** and **Mermaid via CDN**. The workhorse diagram is a **state matrix** — the boolean truth table with invalid rows struck out, collapsing into a union of the few valid states. See [HTML-REPORT.md](HTML-REPORT.md) for the scaffold, diagram patterns, and styling.

Each candidate is one card carrying the full evidence, so the user can judge it without opening the code:

- **Title** — names the re-representation (e.g. "Collapse the upload flags into an `UploadState` union").
- **Badge row** — strength (`Strong`, `Worth exploring`, `Speculative`) plus the signal tag from step 1.
- **Files** — `file:line` references, `font-mono text-sm`.
- **Invalid states today** — the crux: which forbidden combinations the current representation permits.
- **Problem** — one sentence.
- **Solution** — one sentence naming the proposed representation.
- **Wins** — bullets in the vocabulary above, ≤6 words each.
- **Before / After diagram** — the centrepiece (state matrix, state machine, or union split).
- **Migration & risk** — one line: smallest credible scope, and the regression risk of the re-representation.

Do NOT propose the final types yet. After the file is written, ask the user: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, call the Skill tool with `grilling` to walk the decision tree with them:

- **The exact shape** — the variants of the union or the states and transitions of the machine; which fields belong to which variant.
- **The call sites** — which re-guesses and branches collapse once the representation is tight; where the new type is constructed.
- **Migration** — a re-representation is behavior-preserving: the same states, encoded so the wrong ones can't exist. Name what changes at the boundary (serialization, persisted shapes, API contracts) and what must be back-filled.
- **Tests** — which existing tests survive unchanged, which get simpler, and what new validation the tighter type still needs.

Settle side effects inline. If the re-representation names a concept not yet in the domain language, add it (run `/domain-modeling` if the project keeps a `CONTEXT.md`). If the user rejects the candidate with a load-bearing reason a future audit would need — "these flags are independent on purpose" — offer to record it as an ADR so the next pass doesn't re-suggest it. Skip ephemeral or self-evident reasons.

**Stop at the locked shape.** This skill is read-only: it proposes the representation and hands the migration to a separate implementation pass. A move is a move — don't change behavior on the way.
