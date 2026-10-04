---
name: jade-recipe-1.7-1.8-build-rmic-deprecated
description: >-
  Documents (does not remove) the two <rmic> Ant task uses that are
  deprecated for removal starting with JDK 8 and removed outright in JDK 9+.
  Agent-mode recipe: the correct action on a 1.7->1.8 jump is a deferral
  marker plus a real build check, not deletion of a still-working task.
mode: agent
arguments: [--shard-json]
---
# jade-recipe-1.7-1.8-build-rmic-deprecated — rmic deferral

`rmic` (static RMI/JRMP stub generation) is deprecated for removal starting
with JDK 8, in favor of dynamic-proxy stubs (unnecessary since JDK 5), and is
removed outright in JDK 9+. It still runs — with a deprecation warning — on
JDK 8. For a 1.7 -> 1.8 jump this is technical debt to flag for the future,
not something to remove now: removing the two `<rmic>` calls would drop the
generated static stub classes that some deployments may still load
reflectively, which this recipe has no way to verify from the source tree
alone.

## Scope of one task

You receive a shard contract naming `src/jade/build.xml` and the two flagged
`<rmic .../>` elements inside the `jade` target. Edit **only** the files
listed in `editable_files`.

## Transform

For each flagged `<rmic classname="..." base="${build}"/>` element:

1. Leave the element itself untouched — do not delete it, do not add
   attributes to it. rmic still functions on JDK 8; this is a
   forward-looking deferral, not a JDK-8 breakage.
2. Replace the `// JADE-FLAG:BUILD_RMIC_DEPRECATED` marker comment with
   `// JADE-MODERNIZATION-DEFERRED:BUILD_RMIC_DEPRECATED rmic still works on JDK 8; deprecated for removal, will need dynamic-proxy stubs before a JDK 9+ jump`.
3. **Verify by actually building.** Run `ant jade` under the JDK 8 Docker
   image (see the shard's `verify_command`) and confirm the build still
   succeeds and both RMI stub classes are produced, with the expected
   JRMP-stub-deprecation warning present in the log — that warning is
   expected and is not a failure.

## When NOT to transform (report SKIPPED)

- The element has already been migrated away from `<rmic>` (e.g. converted
  to dynamic-proxy stubs) — `SKIPPED`, nothing to defer.

## Invariants

- No edit outside `editable_files`.
- No public signature changes — this rule is `body-local`; each fix is a
  comment swap next to one `<rmic>` element, independent of every other
  build target.
- Never delete or disable an `<rmic>` element under this rule — that is out
  of scope for a 1.7->1.8 jump (rmic removal only becomes a hard blocker at
  a future 8->9+ jump) and would need its own dedicated rule with real
  verification that no deployment depends on the generated static stubs.

## Status to report

| status | when |
|---|---|
| `FIXED` | deferral comment added, `ant jade` verified to still succeed under JDK 8 |
| `SKIPPED` | already migrated away from `<rmic>` |
| `NEEDS_REVIEW` | comment added but the build fails for an unrelated reason (report the actual error) |
| `FAILED` | file unreadable, or the flagged element is not present |
