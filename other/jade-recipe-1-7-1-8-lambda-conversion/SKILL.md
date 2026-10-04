---
name: jade-recipe-1.7-1.8-lambda-conversion
description: >-
  Converts anonymous single-abstract-method (SAM) inner classes to Java 8
  lambda expressions. Agent-mode recipe: the shard contract names the
  files and flagged sites; this document defines the transform, the
  non-convertible categories that must be SKIPPED, and the invariants.
mode: agent
arguments: [--shard-json]
---
# jade-recipe-1.7-1.8-lambda-conversion — anonymous SAM class -> lambda

Java SE 8 (JEP 126) lets an anonymous inner class that implements exactly one
abstract method be replaced by a lambda expression. This recipe is agent mode
because deciding whether a given flagged site is convertible needs real
judgment — reading the anonymous class body, the interface/superclass it
implements or extends, and how the instance is used — not just regex.

## Scope of one task

You receive a shard contract. Edit **only** the files listed in
`editable_files`. `read_only_context` is there for you to read when you need
to resolve an interface's method count, a superclass's fields, or a
`JADE-FLAG:LAMBDA_CONVERSION` site's surrounding method — never modify it.
`entry_points` names the flagged sites (file + line) inside your
`editable_files` to process.

## Transform

For each flagged site in `entry_points`:

1. Read the flagged line and locate the `new <Type>(<args>) { ... }`
   anonymous class expression the flag marks.
2. **Identify what `<Type>` is** — an interface or a concrete/abstract class —
   and how many abstract methods it declares (for an interface) or how many
   methods the anonymous body overrides (for a class).
3. **Only if it is a true single-abstract-method case**, rewrite the
   anonymous class to a lambda:
   - `new Runnable() { public void run() { BODY } }` -> `() -> { BODY }`
   - `new Thread() { public void run() { BODY } }` -> `new Thread(() -> { BODY })`
     (the constructor argument form — `Thread` itself is a class, but its
     single-method `Runnable`-shaped override is the well-known convertible
     idiom used throughout this codebase)
   - `new ActionListener() { public void actionPerformed(ActionEvent e) { BODY } }`
     -> `(ActionEvent e) -> { BODY }` (and the analogous form for any other
     genuine single-method listener interface: `ItemListener`, `ChangeListener`,
     `Callable<V>`, `Comparable<T>`, a JADE-declared single-method interface
     such as `InChannel.Dispatcher` or `ConnectionFactory`, etc.)
   - Preserve the method body, parameter names, and any generic type
     arguments on `<Type>` exactly.
4. Remove the `// JADE-FLAG:LAMBDA_CONVERSION` comment for that site on
   success.

## When NOT to transform (report SKIPPED)

Leave the code untouched and report `SKIPPED` for the site when `<Type>` or
the anonymous body is any of:

- **A field.** The anonymous class declares its own instance field(s) —
  lambdas have no instance state of their own beyond captured locals.
- **Multiple methods.** The anonymous class overrides more than one method
  from its interface/superclass (e.g. a `MouseAdapter`/`WindowAdapter`
  override that implements just one of several available callbacks is still
  a multi-method type — not convertible even though only one is used here).
- **A `this`-qualified self-reference.** The body refers to the anonymous
  class's own instance via a qualified `this` (e.g. `Outer.this` is fine —
  that is the *enclosing* instance and lambdas keep that working identically
  — but a bare, unqualified `this` meaning the anonymous class itself does
  not carry over to a lambda, which has no `this` of its own).
- **A multi-abstract-method interface**, or an abstract **class** with more
  than one abstract method (`AbsoluteCounterValueProvider` in this codebase
  is one such case — it is an abstract class, not an interface, so it is
  never convertible regardless of how many methods are overridden).
- **An extends-by-name of a concrete class** whose constructor does
  meaningful work beyond the default (e.g. `new RemoteDFRequester(remoteDF, s) { ... }`,
  `new OneShotBehaviour(this) { ... }`) — the constructor call itself is not
  representable as a lambda.

For a SKIPPED site, insert `// JADE-MODERNIZATION-DEFERRED:LAMBDA_CONVERSION <reason>`
in place of the flag comment, naming which of the categories above applied.

If you converted a site but are not fully certain the captured-variable
semantics or method resolution are identical, report `NEEDS_REVIEW` instead
of `FIXED` — never guess.

## Invariants

- No edit outside `editable_files`.
- No public signature changes — this rule is `body-local`; every edit stays
  confined to the expression that creates the anonymous class (a local
  variable initializer, a field initializer, or a method-call argument). The
  enclosing field/local/parameter's declared type and every method signature
  in the file are untouched.
- No new imports needed — a lambda targeting an existing interface requires
  nothing beyond what the anonymous class already used.

## Status to report

| status | when |
|---|---|
| `FIXED` | genuine SAM case, rewritten to a lambda |
| `SKIPPED` | field state, multiple methods, unqualified `this`, multi-abstract-method type, or meaningful-constructor class extension |
| `NEEDS_REVIEW` | rewritten, but capture/resolution semantics not certain |
| `FAILED` | file unreadable, or the flagged expression is not present |
