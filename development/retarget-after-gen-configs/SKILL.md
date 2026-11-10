---
name: retarget-after-gen-configs
description: Retarget hand-written Table and column names onto the last generated-config cache. Use when gen:configs tsc fails; when hand-written keys disagree with generated configs; or when the developer asks to retarget after regen.
---

Point the same live column or Table (same column ID or `tableId`) at the new generated key. The live spreadsheet is the source of truth; the four generated config files from the last successful regen are the cache; hand-written names follow identity in that cache.

Open [`docs/generated-data.md`](../../../packages/framework/docs/generated-data.md) now (reading by block, the one regen path), plus [`column-configs.md`](../../../packages/framework/docs/generated-data/column-configs.md) for sampled vs declared and [`config-sheet-floor.md`](../../../packages/framework/docs/generated-data/config-sheet-floor.md) for the floor. Leave regen-run permission, the floor report, and the untyped-column count with whoever ran `gen:configs`.

## Guardrails

**Retarget** identity literals: tests, Table-name groups, named Table/column calls, operators, endpoints, chores. Names only. Leave the live spreadsheet as it is. Leave generated literals as regen wrote them (floor included). Leave `gen:configs` unrun — the last successful regen is the cache.

Operator, endpoint, and chore logic stay as they are. A leftover pin stays a leftover `tsc` error: keep `IsExactly` / `assertType` / `assertNotType`.

## 1. Diff the cache

`git diff` the four generated config files from the regen that just ran. For every changed entry record column ID or `tableId`, old key, new key, and which traits moved. When you need the regenerated object, grep the Table key and read that object only.

Done when every generated hunk is attributed to an identity (same column ID or `tableId`, new key), a trait-only change (same key), an add/remove, or "cannot classify."

## 2. Collect `tsc` lines

Run `npm run tsc` if the regen output is not already in hand. Pair each diagnostic with the cache hunk that explains it.

Done when every `tsc` line is paired or marked unclassified. An unclassified error stays unpatched.

## 3. Classify

One tag per error: **identity** / **incidental trait** / **skipped pin** / **ask** / **unclassified**. Same column ID with a new key is identity even when `valueName` in that row also moved.

| Kind | Action |
| --- | --- |
| Same column ID, new key (header rename); same `tableId`, new Table key (Table rename) | **identity** — always retarget, including type-equality unions and `Object.keys` lists |
| New or vanished column ID on Test-Table fetch lists or complete-row bags | **identity** — follow regen |
| New or vanished key on a business-Table writable-key snapshot (e.g. Occupancy Terms `CompleteAppendBag` keyof) | **ask** |
| New Table added to a name group | **ask** |
| Same key, sampled trait changed | pin detector below |
| Trait-only diff whose assertion subject *is* the trait | **skipped pin** even if retargeting would make `tsc` green |
| Cannot classify from cache + `tsc` line | **unclassified** — leave unpatched |

**Pin detector** (sampled-trait change on an existing column ID). Open [`docs/testing.md`](../../../packages/framework/docs/testing.md#the-dev-fixtures-and-their-exemplar-columns)'s exemplar-columns section only for this step.

1. Documented exemplar → **skipped pin**.
2. Assertion subject is the trait (`ColumnIsFormula`, value name, empty-value-allowed, checkbox vs sampled boolean, writability-because-formula) → **skipped pin**.
3. Else read the test title and comments: would this spec still read the same if the trait flipped? Yes → **incidental trait**. No → **skipped pin**.
4. Unsure → **ask**. No third category.

Done when every paired error has exactly one tag, with column ID or `tableId` when the cache has one. Regenerated entries were grepped by Table key, not read as a whole file.

## 4. Retarget

Apply every **identity** and **incidental trait**. Open only the `describe` (or production call site) you are changing. Grep a Table key and read that generated object only.

Done when every allowed retarget is in the working tree and no pin, ask, unclassified error, or logic change was edited.

## 5. Exit

**Clean exit** when every error is classified, every allowed retarget is applied, and no pin/ask/unclassified remains: `npm run tsc`, then `npm test`, then the report.

**Stop exit** when any pin, ask, or unclassified remains: leave leftover `tsc` red. `npm test` is the clean-exit bar only. Classification succeeded. Report each leftover with the regenerated entry (header, column ID or `tableId`, trait that moved) so the developer can decide sheet vs wait.

## Report

Every item: tag (identity / incidental trait / skipped pin / ask), column ID or `tableId`, old key → new key or trait that moved. Unclassified items listed as left unpatched.
