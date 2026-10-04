---
name: jade-recipe-1.5-1.6-arrays-copyof-full
description: >-
  Replaces the full-array copy idiom System.arraycopy(a, 0, b, 0, a.length)
  with Java 6 Arrays.copyOf. Agent-mode recipe: the shard contract names the
  files to edit; this document defines the transform and its invariants.
mode: agent
arguments: [--shard-json]
---
# jade-recipe-1.5-1.6-arrays-copyof-full — full-array copy → Arrays.copyOf

The Oracle Java SE 6 collections changes page prints this exact idiom as the
"before" and `java.util.Arrays.copyOf` as the "after". The rule matches only the
full-array form, where both offsets are `0` and the length is the source array's
own `length`.

## Scope of one task

You receive a shard contract. Edit **only** the files listed in `editable_files`.
`read_only_context` is for reading, never for editing.

## Transform

For each site in `entry_points`:

1. Confirm the call really is the full-array form:
   `System.arraycopy(src, 0, dest, 0, src.length)` — same identifier in `src` and
   in `src.length`, both offsets literal `0`.
2. Rewrite to `dest = java.util.Arrays.copyOf(src, src.length);`
   Use the fully qualified name rather than adding an import, so the edit stays
   inside the statement and cannot collide with an existing `Arrays` symbol.
3. Remove the `// JADE-FLAG:ARRAYS_COPYOF_FULL_ARRAY_COPY` comment for that site.

## When NOT to transform

Report `SKIPPED` and leave the code untouched when:

- `dest` is `final`, or is a field that must not be reassigned — `Arrays.copyOf`
  returns a **new array**, so it reassigns the reference instead of filling the
  existing one. If any other live reference points at the old `dest` array, the
  rewrite changes behaviour. Check the enclosing method before rewriting.
- `dest` and `src` are the same variable and the result is not reassigned.
- either argument is an expression rather than a plain identifier.

A behaviour change here is silent and hard to find. When the aliasing question
cannot be answered from the file plus `read_only_context`, report `SKIPPED`.

## Invariants

- No edit outside `editable_files`.
- No public signature changes — this rule is `body-local`.
- No new import statements; the fully qualified call is deliberate.

## Status to report

| status | when |
|---|---|
| `FIXED` | full-array form confirmed, no aliasing risk, rewritten |
| `SKIPPED` | aliasing risk, non-identifier arguments, or form not confirmed |
| `NEEDS_REVIEW` | rewritten, but the aliasing analysis was not conclusive |
| `FAILED` | file unreadable, or the flagged call is not present |
