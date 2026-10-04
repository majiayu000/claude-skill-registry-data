---
name: fill-the-gaps
description: Complete work in progress that the user left incomplete on purpose. Use when the tree holds bare signatures, empty modules, pseudo code, deleted code, or `AI TODO` / `AI FIXME` / `AI NOTE` markers.
disable-model-invocation: true
argument-hint: "lock_definitions: y | n = y, lock_names: y | n = y"
arguments: [lock_definitions, lock_names]
---

# Filling the gaps

The user gave you work in progress. It is incomplete, and it can be broken. This is correct. The user writes the code that says what the software must be, and you write the code that makes it run.

## The tree is the specification

The user speaks to you in these forms:

| Form | Means |
| :-- | :-- |
| A signature with no body | Build this. The name and the types are the contract. |
| An empty class or module | This concept exists. Find its parts. |
| Pseudo code | The steps are correct. Write them in the language. |
| Deleted code and a comment | The old solution is dead. Do not bring it back. |
| A marker | Read the marker. |

- ALWAYS read the full diff, and then every file that the diff touches, before the first edit.
- NEVER repair the tree back to its last working state. Broken is the input, not the fault.
- NEVER add a feature that no gap asks for.

## Markers

A marker starts with `AI`. The prefix means the line speaks to you.

- `AI TODO` — the code is absent. Write it.
- `AI FIXME` — the code is present and wrong. Replace it.
- `AI NOTE` — a constraint on the work near it. It is not work by itself.

- ALWAYS delete a marker when you satisfy it.
- NEVER act on a `TODO` or a `FIXME` without the `AI` prefix.

## The two locks

Read both locks before the first edit. The default of each one is `y`.

| Lock | `y` says |
| :-- | :-- |
| `lock_definitions` | The set of definitions is closed. Add none. |
| `lock_names` | The names are frozen. Rename none. |

## lock_definitions

- IF `lock_definitions` is `y`, THEN write no new function, no new class, and no new method. Put the work in the definitions that the tree already holds.
- IF a call has no definition, because the user deleted it or never wrote it, THEN delete the call and each line that serves only the call. NEVER write the absent definition.
- ALWAYS do that work again with the builtin types and the builtin functions of the language, or with a library that the repository already imports.
- ALWAYS name, in your answer, each call that you deleted, and what does the work now.
- IF the work cannot run without one new definition, THEN stop. Name it, say why the builtins are not enough, and wait.
- IF `lock_definitions` is `n`, THEN write the definitions that the gaps ask for, and no more.

<good-examples>
- The tree calls `Money(amount)`, and no `Money` exists. The call goes, and the amount stays a `Decimal`.
- A deleted `retry_on_error` decorator sits above a function. The decorator line goes, and a `for` loop with three attempts takes its place.
</good-examples>

<bad-examples>
- You write `class Money:` to make the call run. The user deleted that class on purpose.
- You keep the call and write a marker above it. The code still fails.
</bad-examples>

## lock_names

- IF `lock_names` is `y`, THEN keep the name of each class, each function, and each method. This holds also for a name that you find wrong.
- IF a name is wrong, THEN say which name, propose one replacement in one line, and wait. NEVER apply it first.
- IF `lock_names` is `n`, THEN correct the name, correct each caller in the same turn, and name each change in your answer.

The lock covers a name of the user. A local variable that you write is yours in both modes.

A deletion is not a rename. IF `lock_definitions` is `y`, and it asks you to delete a call, THEN delete it. `lock_names` does not stop a deletion.
