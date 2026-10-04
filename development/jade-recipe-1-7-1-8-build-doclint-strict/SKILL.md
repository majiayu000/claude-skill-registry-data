---
name: jade-recipe-1.7-1.8-build-doclint-strict
description: >-
  Adds -Xdoclint:none to Ant <javadoc> elements so the JDK 8 javadoc tool's
  default-on DocLint checker does not turn pre-existing malformed Javadoc
  comments into build failures. Agent-mode recipe: verifying the fix means
  actually running `ant doc` under the JDK 8 Docker image.
mode: agent
arguments: [--shard-json]
---
# jade-recipe-1.7-1.8-build-doclint-strict — DocLint opt-out for javadoc

Starting with JDK 8, the `javadoc` tool runs its bundled DocLint checker by
default. A malformed HTML comment or a missing tag that previously produced
at most a warning can now fail the `javadoc` build outright, unless
`-Xdoclint:none` (or a narrower `-Xdoclint:<group>` selection) is passed.

## Scope of one task

You receive a shard contract naming `src/jade/build.xml` and the flagged
`<javadoc>` elements inside the `doc` target. Edit **only** the files listed
in `editable_files`.

## Transform

For each flagged `<javadoc .../>` element:

1. Confirm it does not already carry an `additionalparam` (or nested
   `<arg value="-Xdoclint..."/>`) mentioning `Xdoclint`.
2. Add `additionalparam="-Xdoclint:none"` to the element's attribute list.
   Do not otherwise reformat the element — this file has very long
   attribute lines; keep the diff to the one added attribute.
3. Remove the `// JADE-FLAG:BUILD_DOCLINT_STRICT` marker comment for that
   element.
4. **Verify by actually building.** This is a build-tooling rule, not a
   source-code one — the only real evidence is running
   `ant doc` under the JDK 8 Docker image (see the shard's `verify_command`)
   and confirming it completes without a DocLint-caused failure. Do not mark
   a site `FIXED` from static inspection alone.

## When NOT to transform (report SKIPPED)

- The element already carries `-Xdoclint:none` or an equivalent narrower
  `-Xdoclint:<group>` selection — `SKIPPED`, not a duplicate edit.

## Invariants

- No edit outside `editable_files`.
- No public signature changes — this rule is `body-local`; each fix is one
  added attribute on one `<javadoc>` element, independent of every other
  build target.
- Do not touch the `<javac>` source/target attributes or any other target in
  this file — those belong to other rules.

## Status to report

| status | when |
|---|---|
| `FIXED` | attribute added, `ant doc` verified to complete under JDK 8 |
| `SKIPPED` | the element already opts out of DocLint |
| `NEEDS_REVIEW` | attribute added but `ant doc` still fails for a reason unrelated to DocLint (report the actual error) |
| `FAILED` | file unreadable, or the flagged element is not present |
