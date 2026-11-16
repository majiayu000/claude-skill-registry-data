---
name: delivery-change-contract
description: Use when implementing a ready spec and about to change something other than the change's own code — a test written before the code, a test that existed before the change, a gap the spec left, the spec's goal or scope, a decision record, or a check that guards the repository such as the architecture test, the linter's configuration or CI. Owns the short list of what is frozen while a spec is implemented and changes only with the person's consent, that everything else is free and read by the review from the diff, that a new decision record or a stricter guarding rule is free, that an environment others use, a shared service or a secret is touched only with the person's consent asked once before the work, with credentials found or created rather than asked for piece by piece, the base commits a change is measured from, and catching an edit to what is frozen by a diff from them rather than by forbidding it. What a spec holds and which of its sections are frozen are `delivery-spec`'s; whether an edit to a test changed what it asserts is decided by the review that reads the diff. - Also when asked whether an implementer may edit a test, loosen the architecture test, touch code another component shares, or fill in a name the spec does not give.
---

# Delivery — Change contract

While a spec is implemented, a few artifacts are **frozen**: they change only by the person, or with
their consent. Everything else is free, and the review reads it in the diff. No tool can stop an edit —
a file changes through any command that can write — so freezing is not a ban: an edit to what is frozen
is caught by a diff from a fixed commit, and reaches the person as a stop.

## When to use vs. neighbours

- What a spec holds, and which of its sections are frozen once it is ready → `delivery-spec`.
- Whether a test is strong enough, at which level, and a fix's failing test → `test-principles`.
- Whether an edit to a test repaired its form or weakened its meaning →
  `/pyhouse-universal:change-review`, which classifies every such edit from the diff, and is told the
  tests' base so that a test written before the code counts as one that existed.
- The messages of the change's commits → `git-commit-message`, in the `pyhouse-git` plugin, where
  installed.
- How the branch lands and when its history is folded → `git-branching`, in the `pyhouse-git` plugin,
  where installed.

## What is frozen

- What the checks that guard the repository already enforce — the architecture test, the linter's and
  type checker's configuration, CI, hooks. A rule added that only makes one stricter is free; an
  exemption added to one, or a rule changed or removed, loosens it.
- The project's decision records as they stand. A new record is free, unless it supersedes or
  contradicts one that exists: that changes the old decision, and is the person's.
- What a test written for this change before its code asserts — a case, an expected value, a check.
  Its form — a typo, an import, a name the code settled — is free.
- The spec's sections `delivery-spec` rule 10 freezes.

## Rules

1. **What is not frozen is free, and needs nothing.** Code anywhere the change needs it, a test that
   existed before the change, a fixture — each is edited as the work asks, and the review reads it in
   the diff. Nothing is declared: the diff already says what changed.
2. **A frozen artifact is changed only by the person, or with their consent.** Whoever is implementing
   stops, says what they would change and why, and goes on only with the answer. The commit that makes
   an agreed change names the consent in its body; a change to the spec is also recorded in the spec,
   as `delivery-spec` asks.
3. **A gap is filled, not guessed silently and not stopped on.** Where the spec does not decide a name,
   a default or a case, it is filled the way the code around it and the decision records already do. A
   gap whose filling would change a contract other code depends on, or contradicts a decision, is the
   spec's scope, and frozen.
4. **An artifact the list does not name takes the standing of what it serves.** A fixture or a test
   helper follows the tests it serves; a file that guards other files follows the checks that guard the
   repository.
5. **The project names its paths; the list is this skill's.** Which directory holds the tests, which
   file is the architecture test, where CI lives — the project records them in its agent instructions.
   Where it records none, they are read from the repository, and the person is told the paths were not
   named.
6. **Every edit to what is frozen is measured from a base commit, by a diff anyone can recompute.** The
   spec's base is the commit at which it reads as ready on the change's branch; the tests' base is the
   commit holding the tests written before the code. The diff of the spec from its base, of the tests
   from theirs, and of the repository's guarding checks and decision records from where the branch left
   its mainline, is taken before the change is reviewed. An edit to a frozen artifact the person did not
   agree to is a stop; an addition the list leaves free is not, and the review reads it with the rest.
7. **A base commit stays as written until the change has been measured from it.** No later edit is
   folded into it before the diff and the review have read the change: an edit folded into the commit it
   changes is invisible to both. Once they have, the branch's history may be curated as the repository
   lands branches.
8. **Whoever made an edit does not judge what it did to a test.** Whether an edit kept what the test
   asserts or weakened it is decided by the review, from the diff, by someone who wrote neither the test
   nor the edit — and for a test written before the code, from the tests' base, where it already
   existed. A weakened assertion the person has not agreed to holds the change.
9. **An environment others use, a shared service and a secret are not the change's, and consent to
   them is asked once.** Whether an environment is anyone else's is the person's to say. Before the work
   starts, whoever implements asks in one question for everything the change's checks would touch there,
   naming every service a command starts, stops or recreates, read from the definition it runs — not
   only what it was meant to touch. The answer holds for the whole change; a command beyond it is asked
   again. A credential a check needs is found where the project keeps one for its checks — a test
   fixture, a seed, a documented local default — or created in an environment the change started
   itself; a file of secrets is never read (`delivery-spec` rule 7). What only the person can do
   reaches them once, as one script by that rule, never as a series of questions. A run the person
   refused or did not answer is not made, and is reported as not made.

## Hard stops

- Asked to write or check the spec itself, or to decide whether it is ready → stop, use
  `delivery-spec`.
- Asked whether the change is correct, or what it breaks → stop, use
  `/pyhouse-universal:change-review`.
