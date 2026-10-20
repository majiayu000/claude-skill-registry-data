---
name: sketch-design
description: >-
  Load this skill when the next change adds a type, module, or function other code will call, before
  its first test: sketch types, signatures, and module boundaries with no bodies, then check them.
  Trigger on a plan phase adding a module, "design this first", "sketch the types".
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Sketch design

Write the shape of the change before its code: the types, the signatures, and which module owns
which decision. The task is done when the sketch passes the four checks below and every failure is
either fixed in the sketch or named as accepted, and only then does implementation start.

## Procedure

1. **Name the domain in types.** Write the data types the feature needs, as the language's own
   type syntax with no function bodies. Make an illegal state unrepresentable where the language
   allows it: a tagged union over a struct of optional fields, a `Status` enum over a bare string,
   a parsed `EmailAddress` over `str`. Name each type in the words the user and the repo already
   use, never a synonym.
2. **Write the signatures.** Every function or method another module will call: name, parameter
   types, return type, and the errors it raises or returns. Leave bodies out. A body in the sketch
   pulls the review toward the code and away from the shape.
3. **Draw the boundaries.** For each module, one line: the decision it owns and hides (a file
   format, a retry policy, an ordering rule). A decision that two modules must both know is
   information leakage, so move it behind one of them now, while that costs an edit to the sketch.
4. **Run the checks** in Rules on the sketch and fix what fails.
5. **Show the sketch, then implement it.** Present it in the Output shape and continue to the code
   in the same turn. Wait for the user only when the sketch changes a public API, a stored data
   format, or anything else on the contract's one-way-door list.

## Rules

- **Check: illegal states.** For each type, name one value it can hold that the domain forbids.
  If one exists, tighten the type or say where it is validated, at the boundary, once.
- **Check: runs twice.** For each operation that writes (a database row, a file, a message, a
  payment), say what happens when it runs twice: on a retry, a double click, a redelivered message.
  Make it idempotent with a key or an upsert, or name why it can only ever run once.
- **Check: shared state.** For each value two requests, threads, or processes can touch, name who
  writes it. Build the per-request result apart from the shared value, then write it in one step,
  under a lock or a transaction, rather than mutating shared state as the work goes.
- **Check: smallest interface.** Count each module's public names. A module that exposes most of
  what it contains hides nothing, so merge it into its caller or cut the interface down.
- **One concern per file, named for it.** Place each new type and function in the file whose name
  already states its concern, or in a new file named for what it does, never in a catch-all
  (`utils`, `helpers`, `common`). Do not give one small function with one caller its own file. An
  agent finds code by Grep and Glob on names and reads a long file in chunks, so a mixed file costs
  context and makes an Edit match ambiguous, while a feature scattered across tiny files costs the
  same context in reads. An existing catch-all stays as it is: splitting it is a refactor nobody
  asked for.
- Keep the sketch to what this change needs. A type or parameter for a requirement nobody stated
  fails `ceh-coding-conduct:write-less-code` rung 1, sketch or not.

## Output

```markdown
**Types**

<type definitions in the target language, no bodies>

**Signatures**

<function and method signatures, with error types>

**Boundaries**

| Module | Owns and hides | Exposes |
| ------ | -------------- | ------- |

**Checks**

| Check              | Result                               |
| ------------------ | ------------------------------------ |
| Illegal states     | pass, or <value> → <fix or accepted> |
| Runs twice         | pass, or <operation> → <fix>         |
| Shared state       | pass, or <value> → <who writes, how> |
| Smallest interface | pass, or <module> → <names to cut>   |
```

## Stop conditions

- The sketch changes a public API, an endpoint, a config key, or a stored data format → stop and
  show the sketch for approval before any code.
- Two checks conflict, and fixing one breaks the other → present both options with a
  recommendation, and stop.
