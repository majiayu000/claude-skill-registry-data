---
name: hand-edited-catalogue-invariants
description: "Guard hand-edited data catalogues (seeded exercise/item lists, preset programs, skill/tech trees, title tables) with structural invariant tests — cross-reference existence, name uniqueness, enum-stored-as-String validity, prerequisite acyclicity — and mutation-prove each. Use when a catalogue is edited by hand, when a typo would fail silently rather than crash, or when a progression tree could soft-lock."
---

# Hand-edited catalogue invariants

Catalogues edited by hand (seed lists, preset programs, skill trees, title
tables) fail **silently**: no crash, no error, just wrong content shipped.
Behaviour tests pass on a broken catalogue because the rules are fine — it is
the *data* that is inconsistent. Assert the structure over the real data.

## The four invariants that actually catch bugs

1. **Cross-reference existence.** Every name one catalogue quotes from another
   must exist there. Critical when the reader auto-creates unknown names
   (a lenient import/resolve path): a typo then mints a near-duplicate row
   instead of failing, so nothing ever complains.

```kotlin
val missing = Programs.ALL.flatMap { p -> p.entries.filter { it.name !in catalogue } }
assertEquals(emptyList(), missing)   // list the offenders, don't just count
```

2. **Name uniqueness — case-insensitively** when lookups are. Two rows differing
   only by case both match; the loser is unreachable, and `forName(x).field`
   silently returns the wrong row's value.

3. **Enum-stored-as-String validity.** A `String` column holding an enum name
   compiles with any typo and throws at `valueOf` on read — the persisted-enum
   launch crash. Assert every value is in `Enum.entries.map { it.name }`.

4. **Prerequisite acyclicity** for any progression tree. A loop locks every
   member forever: each waits on another, and no play can open them. Invisible
   in-app; only a walk finds it. Dangling-reference and unlock-gating tests both
   **pass** on a cyclic graph — that is why this needs its own test.

```kotlin
// single nullable parent -> ancestor walk; ordered set so the message shows the path
val parentOf = ALL.associate { it.name to it.requires }
ALL.forEach { skill ->
    val seen = linkedSetOf(skill.name)
    var cursor = skill.requires
    while (cursor != null) {
        assertTrue("prerequisite loop: ${seen.joinToString(" -> ")} -> $cursor", cursor !in seen)
        seen += cursor; cursor = parentOf[cursor]
    }
}
```
Multiple parents -> DFS colouring instead. Acyclicity + the existence check
together imply every chain terminates at a real root, i.e. full reachability.

Also cheap and worth it: non-empty child lists, numeric fields `> 0`, scheduling
keys unique (two programs on one weekday makes "today" depend on list order),
and *domain* coherence — e.g. a load may only sit on an item that can carry one
(`weight > 0 ⇒ inherentlyWeighted || modifier says so`), otherwise the UI renders
an unexplained value.

## Mutation-prove every invariant

An invariant asserted over a constant list can trivially be vacuous. Break the
real data once per invariant and confirm the *matching* assertion fires:

- misspell one cross-reference → existence test names it
- duplicate one name → uniqueness test (expect collateral failures: one
  duplicate commonly breaks 3–4 tests, including value lookups)
- typo one enum string → enum test
- point a parent at its own child → loop test prints the path

Commit first, then revert each mutation with `git checkout -- <file>` in the same command (a `.bak`
copy can be deleted mid-run) and re-run the gate after; mutation mechanics are in
`gradle-mutation-proof-regression-test`.

## Traps

- **Read the accessors first.** The composed public list is often built from a
  `private` base list plus extras; test the public one or the test misses rows.
- **Confirm the test path is new** (`git log --oneline -1 -- <path>`) before
  `write` — overwriting an existing test file deletes cases with no compile error.
- **Capture gradle's real exit code** (`cmd > log; EXIT=$?`), not a pipeline's —
  piping through `sed` makes `&&` gate on `sed`'s status, so a red build can
  still commit.
