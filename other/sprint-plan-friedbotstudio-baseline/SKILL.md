---
name: sprint-plan
owner: baseline
description: Decompose an MVP vision into a sprint manifest — a prioritized feature list where every feature carries explicit done-criteria (a done-record reference, named edge tests, and a wiring test). Produces the sprint manifest that `sprint-oracle` checks for completeness. Use when planning a sprint of parallel work (Slice A of the sprint-mode epic). Not a workflow phase; the manifest it writes is the completeness contract a sprint is held to.
disable-model-invocation: true
---

# sprint-plan — author a sprint manifest with per-feature done-criteria

`sprint-plan` turns an MVP vision into a **sprint manifest**: a prioritized list of features, each carrying the done-criteria that make "done" mechanically checkable. The manifest is the input contract for `sprint-oracle`, which fails a sprint until every feature meets its criteria. This is Slice A of the `mvp-sprint-parallel-cycles` epic — the completeness half of the parallel-sprint goal (a sprint can be fast yet provably not partial).

## What the manifest is

A JSON document (`template-manifest.json` is the shape). Each feature declares three done-criteria dimensions so completeness is a grep, not a judgment call:

- **`done_record`** — a reference proving the feature is specified (a spec AC id, e.g. `AC-012`). Non-empty.
- **`edge_tests`** — names of tests covering error / empty / edge states. A non-empty array.
- **`wiring_test`** — the name of one integration test exercising the feature end-to-end.

```json
{
  "sprint": "<sprint name>",
  "features": [
    {
      "id": "search",
      "priority": "P0",
      "done_record": "AC-012",
      "edge_tests": ["search_empty_query", "search_unicode"],
      "wiring_test": "search_end_to_end"
    }
  ]
}
```

## The test-tag convention (how `sprint-oracle` resolves the names)

A named test counts toward a feature only when the test file tags it. Immediately above the `test('<name>', …)` call, place:

```js
// @sprint-feature:<feature-id> @kind:edge|wiring|happy
test('<name>', () => { /* … */ });
```

`sprint-oracle` builds a map of `testName → {feature, kind}` from these tags and resolves each manifest reference against it. A test tagged `@kind:happy` does **not** satisfy an `edge` or `wiring` requirement — that is the deliberate, mechanical line (no script can prove a test is *semantically* an edge case; the tag is the author's crisp claim, and the oracle verifies the claim resolves).

## How to use

1. Decompose the MVP vision into features. Decide priority (`P0`/`P1`/…) per feature — scoping, not implementation.
2. For each feature, name its `done_record` (the spec AC it traces to), the `edge_tests` it must carry, and its `wiring_test`.
3. Write the manifest (default location: `.claude/state/sprint/<sprint>/manifest.json`, gitignored runtime state).
4. Validate the shape before handing it to the oracle:

   ```
   node .claude/skills/sprint-plan/validate-manifest.mjs validate <manifest-path>   # wraps validate-manifest.mjs -> validateManifest
   ```

   `validateManifest(obj)` returns `{valid, errors:[{feature, field, reason}]}` — it flags missing required fields per feature and duplicate feature ids. It checks **shape**, not completeness; completeness is `sprint-oracle`'s job.

## Constraints

- The manifest is a scoping artifact, not a design. `sprint-plan` decides *what* features and *which* done-criteria, never *how* a feature is built.
- Decisions live in main context (Article II). This skill is invoked there; it delegates nothing to a subagent.
- Completeness is enforced by `sprint-oracle`, not here — keep the two concerns separate.
