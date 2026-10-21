---
name: sprint-oracle
owner: baseline
description: The sprint completeness oracle — a mechanical, exit-code-driven check that every feature in a sprint manifest is provably complete across three dimensions (a done-record reference, resolvable edge tests, and a resolvable wiring test). Fails loud with a per-feature gap list naming the missing dimension. Read-only. Use to gate a sprint before it is called done (Slice A of the sprint-mode epic), or any time you want a completeness reading.
disable-model-invocation: true
---

# sprint-oracle — mechanical completeness gate for a sprint

`sprint-oracle` reads a sprint manifest (authored by `sprint-plan`), scans the test tree for the `@sprint-feature` / `@kind` tags, and reports whether every feature is complete. It is the answer to "the final system ships incomplete": a sprint is not done until the oracle exits 0. Read-only — it reports, it never edits.

## What it checks (per feature)

A feature is complete only when all three hold:

1. **done-record** — `done_record` is non-empty (the feature traces to a spec AC).
2. **edge** — at least one name in `edge_tests` resolves to a test tagged `// @sprint-feature:<id> @kind:edge`.
3. **wiring** — `wiring_test` resolves to a test tagged `// @sprint-feature:<id> @kind:wiring`.

"Resolves" means: the named test exists in a scanned `.mjs` file **and** its tag's feature id and kind match. A test tagged `@kind:happy` never satisfies an edge or wiring requirement — the happy path does not count as completion.

## Exit codes (fail loud, fail distinct)

| Code | Meaning |
|---|---|
| `0` | every feature complete (or the manifest has zero features — vacuously complete) |
| `2` | gaps found — at least one feature is missing a dimension; a per-feature gap list is printed to stderr |
| `1` | operational error — the manifest could not be read or parsed (distinct from a completeness gap) |

A gap is `{feature, dimension, detail}` where `dimension` is one of `done-record` / `edge` / `wiring`, and `detail` names the unresolved test(s).

## How to use

```
node .claude/skills/sprint-oracle/oracle.mjs <manifest-path> [test-root]
```

`test-root` defaults to `tests`. The CLI prints each gap as `GAP <feature>: <dimension> — <detail>` and exits with the code above. For programmatic use, import `runOracle({manifestPath, testRoot})` → `{code, gaps, error?}`.

Example gap output:

```
GAP search: edge — no resolvable @kind:edge test among [search_empty_query]
GAP search: wiring — wiring_test 'search_end_to_end' does not resolve to a @kind:wiring test
```

## The honest limit

No script can prove a test is *semantically* an edge case or a true end-to-end exercise. The oracle verifies that the manifest's claims **resolve** to tagged tests — it trades unbounded gameability for mechanical checkability. That is a deliberate, documented bound (see the locked Q3 decision in the `mvp-sprint-parallel-cycles` spec): far better than today's no-record-of-done, and crisp enough to grep.

## Constraints

- Read-only. The oracle never writes; it reports an exit code + a gap list.
- Mechanical only. It does not judge test quality — it resolves references against tags.
- Pairs with `sprint-plan` (which authors the manifest + validates its shape). Keep authoring and gating separate.
