---
name: vsa
description: >
  Vertical Slice Architecture guardian, two modes. PLACE mode: decide where a new class, event,
  DTO, or module belongs under VSA rules, or design a new module/slice map from scratch. AUDIT
  mode: scan for slice-isolation violations (cross-slice imports, cross-module coupling, misplaced
  events) and prescribe the move that fixes each. Use whenever the user says "VSA", "which slice",
  "where does this class go", "slice isolation", "organize the slices", "cross-slice import",
  "should this move to module root", or asks how to structure a feature in a slice-based codebase.
---

# VSA — Slice Placement & Isolation

The architecture in one breath: **group by feature slice, not file type; slices never import each other; modules talk only through database state and events; the scheduler is the only orchestrator.**

Default mode is **place**; the words "audit", "scan", "violations", "leak" select **audit**.

## The Rules (both modes enforce these)

1. **Slice = one user story.** Every class serving that story — controller, service, job, listener — lives in the same folder. Namespace: `App\{Module}\{Slice}\{ClassName}`.
2. **No type folders.** `Actions/`, `Jobs/`, `Listeners/`, `Http/Controllers/` are banned; the moment one appears, slicing has failed.
3. **No cross-slice imports.** A slice never `use`s or dispatches a class from another slice.
4. **Shared within a module → module root.** A class, DTO, or enum used by 2+ slices of the same module moves to `app/{Module}/` — never defined in one slice and imported by another.
5. **Events are the seams.**
   - Slice must trigger a sibling slice → fire a module-internal event at the **module root**; the receiving slice registers a listener. Never a direct call or job dispatch across the boundary.
   - Event consumed by 2+ modules → `App\Shared\Events\`.
   - An event never lives inside a slice folder.
6. **Modules never import each other's classes.** Cross-module effects flow through database state (status fields another module's scheduler picks up) or shared events. Models used by many modules live in `App\Shared\`.
7. **The scheduler orchestrates.** Module A writes state; the scheduler detects it and triggers Module B. No module calls another.

## Mode PLACE

Given a new class, feature, or whole module:

1. Name the user story. One story → one slice; two stories → two slices, even if they share a screen.
2. Walk the decision ladder: used by one slice → in the slice · by 2+ slices, one module → module root · by 2+ modules → `Shared/` · event → rule 5 placement.
3. For a new module, design the map with aggregate-root thinking before folders: **trigger → state written → who consumes it**. Deliver a table (slice → story → classes) plus the module's status-field contract (values written, consumed by whom).
4. Verify against reality: read the existing tree first; place new code the way its neighbors are placed. If existing structure already violates the rules, flag it — do not imitate a violation.

The rules are stack-agnostic — folder-per-slice with event seams works in any framework; only the namespace idiom changes.

## Mode AUDIT

Sweep the module (or whole app) for each violation class, with grep evidence:

1. Cross-slice `use`/dispatch statements.
2. Cross-module class imports (anything not via `Shared/` or events).
3. Direct cross-module job dispatches or method calls.
4. Events defined inside slice folders.
5. DTOs/enums defined in one slice, imported by another.
6. Type folders reappearing.
7. Orchestration outside the scheduler (module A directly triggering module B).

### Output — per violation

`file:line` → rule broken → **the concrete move that fixes it** ("move `ParsedRowDto` to `app/Ingestion/`, update 3 imports"; "replace the direct dispatch with a `CsvUploadParsedEvent` at module root + listener in the receiving slice"). Ranked: cross-module coupling first (breaks the architecture), cosmetic placement last. End with the isolation verdict per module: clean / leaking.

Audit is read-only; apply moves only on request, each move followed by a green full suite.
