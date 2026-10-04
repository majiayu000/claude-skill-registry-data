---
name: jade-recipe-11-17-wrapper-valueof
description: >-
  Replaces primitive wrapper constructor calls with the corresponding valueOf
  factory. JEP 390 (JDK 16) deprecated those constructors for removal. Agent-mode
  recipe: the shard contract names the files; this document defines the transform
  and the identity-sensitive sites it must refuse to touch.
mode: agent
arguments: [--shard-json]
---
# jade-recipe-11-17-wrapper-valueof — the wrapper constructors are on the way out

JEP 390 designated the primitive wrapper classes as value-based and deprecated
their constructors for removal. The JDK 16 release note is explicit:
"Programmers are strongly discouraged from calling the wrapper class
constructors, which are now deprecated for removal."

Nothing is broken on JDK 17 — the code compiles and runs. What the rule buys is
that this is JADE's largest terminally-deprecated surface: 144 sites confirmed
by javac itself (`-Xlint:removal -Xmaxwarns 100000`), spread over 52 files.

## Scope of one task

You receive a shard contract. This rule is `blast_class: body-local`
(`parallel_safe: true`), planned into 12 shards. Edit only that shard's
`editable_files`; `read_only_context` is read-only.

## The transform

```
new Boolean(x)   ->  Boolean.valueOf(x)
new Integer(x)   ->  Integer.valueOf(x)
new Long(x)      ->  Long.valueOf(x)
new Double(x)    ->  Double.valueOf(x)
new Float(x)     ->  Float.valueOf(x)
new Character(c) ->  Character.valueOf(c)
```

Both the primitive and the `String` overloads are covered — `Integer.valueOf(String)`
and `Long.valueOf(String)` exist and parse identically. Fully-qualified receivers
(`new java.lang.Long(...)`) keep their qualification: `java.lang.Long.valueOf(...)`.

The static type of the expression is unchanged, so no field type, method
signature or return type moves. That is what makes this body-local.

## The one thing that can go wrong

`valueOf` may return a cached, shared instance where the constructor always
returned a fresh one. `Boolean.valueOf` always returns `Boolean.TRUE` or
`Boolean.FALSE`; `Integer.valueOf`, `Long.valueOf`, `Short.valueOf` and
`Byte.valueOf` intern -128..127; `Character.valueOf` interns 0..127.

Before converting a site, check what happens to the resulting object:

- compared with `==` or `!=` against another wrapper
- used as a `synchronized` monitor
- used as a key in an `IdentityHashMap`, or passed to `System.identityHashCode`
- relied on for `wait`/`notify`

Any of those makes the conversion a behaviour change. Leave the site as it is,
keep its `// JADE-FLAG:` marker, and report it in the shard result. Converting
an identity-sensitive site is worse than leaving a deprecation warning.

`.equals` comparison, `.intValue()`/`.booleanValue()` unwrapping, storage in a
collection, and use as a method argument are all safe.

## What the agent may not do

- Do not "simplify" further by removing the boxing altogether (`new Integer(x)`
  -> `x`). Autoboxing has different overload-resolution behaviour and this rule
  is not a refactor.
- Do not edit a site inside a comment or a string literal. The scanner's line
  filter is prefix-based and its population (147) is three larger than javac's
  live count (144); the difference is code sitting inside block comments such as
  `MMCanvas.java:427-469`. Check with `java_source.is_live_code()` before every
  edit.
- Do not touch `#PJAVA_INCLUDE`, `#DOTNET_INCLUDE` or `#MIDP_EXCLUDE` blocks.
  They are comment text, not code.

## Verification

Recompiling in `jade-ant:17` with `-Xlint:removal -Xmaxwarns 100000` reports zero
`[removal] ... in Boolean/Integer/Long/Double/Float/Character has been deprecated
and marked for removal` warnings, down from 144. Any site deliberately left
behind is named in the shard result with its reason. The build exits 0 and all
consumers PASS.
