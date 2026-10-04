---
name: jade-recipe-1.5-1.6-string-isempty
description: >-
  Replaces the pre-Java-6 emptiness idiom s.length() == 0 with s.isEmpty()
  on String receivers only. Agent-mode recipe: the shard contract names the
  files to edit; this document defines the transform and its invariants.
mode: agent
arguments: [--shard-json]
---
# jade-recipe-1.5-1.6-string-isempty — length() == 0 → isEmpty()

`java.lang.String.isEmpty()` was added in Java 6 (`Returns true if, and only if,
length() is 0`). Java 5 has no such method, so the idiom `s.length() == 0` is the
only way to express it on 1.5. On 1.6 the direct call is clearer and is what the
Oracle javadoc points at.

## Scope of one task

You receive a shard contract. Edit **only** the files listed in `editable_files`.
`read_only_context` is there for you to read when you need to resolve a receiver's
type — never modify it.

## Transform

For each site in `entry_points`:

1. Read the flagged line and locate the `<receiver>.length() == 0` expression.
2. **Resolve the static type of `<receiver>`.** This is the whole job — the pattern
   cannot do it, which is why this recipe is agent mode.
   - local variable → find its declaration in the same method
   - field → find the field declaration in the class
   - parameter → read the method signature
   - method call result → read the called method's return type
3. **Only if the receiver is a `String`**, rewrite:
   `receiver.length() == 0` → `receiver.isEmpty()`
   Preserve any surrounding negation exactly: `!(s.length() == 0)` becomes `!s.isEmpty()`.
4. Remove the `// JADE-FLAG:STRING_ISEMPTY_ADOPTION` comment for that site.

## When NOT to transform

Report `SKIPPED` for the site and leave the code untouched when the receiver is:

- `StringBuffer` or `StringBuilder` — neither has `isEmpty()` in Java 6.
  A known case in this codebase is `HTTPIO.java`, where `type` is a `StringBuffer`
  parameter. Rewriting it would not compile.
- a collection, array, or any type you could not resolve with certainty.

Uncertainty is a `SKIPPED`, never a guess. If you rewrote the site but are not
certain the semantics are identical, report `NEEDS_REVIEW` rather than `FIXED`.

## Invariants

- No edit outside `editable_files`.
- No public signature changes — this rule is `body-local`; every edit stays inside
  a method body or a field initializer.
- No new imports: `isEmpty()` is a method on `String`, nothing to import.

## Status to report

| status | when |
|---|---|
| `FIXED` | receiver proven to be `String`, rewritten |
| `SKIPPED` | receiver is not a `String`, or type could not be resolved |
| `NEEDS_REVIEW` | rewritten, but semantics not certain |
| `FAILED` | file unreadable, or the flagged expression is not present |
