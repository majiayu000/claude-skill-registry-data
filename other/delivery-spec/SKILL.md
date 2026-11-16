---
name: delivery-spec
description: Use when writing, splitting or checking the spec for one change before it is implemented — a feature or a fix, what it names as contracts, and the behaviour its tests are written from. Owns the spec's sections and which of them exist only where the project has them, the shorter form a fix takes, contracts limited to what other code depends on, the sign that one spec is several, behaviour stated as what each path leaves behind, an optional note in words on how to see a change that shows only in a running process, a step the person must take written as the command they run, the spec's claims about today's system checked before any code is written, and which sections are frozen once the spec is ready — the goal, the scope and the contracts, a fix's symptom — and which may be refined during the work, and the status it carries from draft to implemented, set by the change itself so the mainline reads implemented only once it has landed. Not why a design was chosen — that is the project's own decision record, which a spec points at. - Also when asked for a definition of done, what a spec should say about tests, how large a spec may be, whether a spec should name internal functions and types, how to write up a bug before fixing it, or whether an implementer may change what a spec says.
user-invocable: false
---

# Delivery — Spec

A spec says what one change delivers and what must be true once it is done: what the change adds,
what other code will rely on, and the behaviour its tests are written from. It is written before the
code, with the person who wants the change, and it is short enough to review in one sitting. It is not
a second copy of the code, and it does not carry the reasons for a design.

## When to use vs. neighbours

- Why a design was chosen, and what was rejected → the project's decision record; a spec points at
  the section it implements and restates none of it.
- Whether a new service is hexagonal or flat → `architecture-choice`.
- How the tests written from a spec are written — layers, substitution, assert strength, a defect's
  failing test → `test-principles`.
- The commit or merge message of the change → `git-commit-message`, in the `pyhouse-git` plugin, where
  installed.
- What implementing a ready spec may change besides its own code, and how an edit to what is frozen is
  caught → `delivery-change-contract`.
- What a change breaks, read from its diff once it exists → `/pyhouse-universal:change-review`, not a
  spec.

## Template(s)

A spec is one Markdown file per change, in the directory the project keeps them in. Section headings
may be in the project's language, worded as the project's earlier specs word them; which sections
exist, and their order, are what the template fixes — never an earlier spec's.
A section the template marks as conditional is left out entirely where its condition does not hold —
never kept with "none" under it.

### A feature

```markdown
# <the key the project's specs use>. <What the change delivers, in one line>

Status: draft

## Goal

<One paragraph: what exists once this change is done that does not exist now.>

## Source

<Only where the project keeps decision records: the record and section this spec implements.>

## In scope / out of scope

- In: <…>
- Out: <… — and the spec that takes it, where one does>
- Code: <the packages or layers this change adds or touches — never its files or the classes in them>

## Depends on

<Only where another spec must be done first: that spec.>

## Contracts

<Only where the change adds or changes something other code depends on — a table or schema, a
message or payload, a function another component calls, an HTTP or command-line surface, a setting's
or metric's name — each with its exact name and shape.>

## Behaviour and failures

<What the change does on its main path, and what invalid input, a repeat or a dependency that fails or
answers late leaves behind, and, where the change holds state, a restart or a partial write — those
the change has.>

## Settings and metrics

<Only where the change adds or changes one: its name, its meaning, and whether it is required.>

## How to see it working

<Only where the change shows only in a running process: what to do to it and what shows it working,
in words.>

## Steps for the person

<Only where the change needs a step an agent may not take: each as the command or script the person
runs, and whether it comes before the change lands or after it.>
```

### A fix

```markdown
# <the key the project's specs use>. Fix: <the symptom, in one line>

Status: draft

## Symptom

<What was observed, where, and how to reproduce it.>

## Cause

<The code that produces it, and why — and how that was established.>

## Regression test

<The test `test-principles` *A defect's test* asks for; where no test can reach the defect, the check
that would have caught it.>

## Steps for the person

<Only where the fix needs a step an agent may not take: each as the command or script the person
runs, and whether it comes before the fix lands or after it.>
```

## Rules

### What a spec holds

1. **One spec is one change a person can review in one sitting.** It is measured by a sign, not a
   line count: where the work has to be cut into parts implemented one after another, each part is its
   own spec, ordered by **Depends on**.
2. **A fix takes the short form; anything else takes the full one.** A fix states the symptom, its
   cause and the regression test `test-principles` asks for. A change that adds behaviour, a surface or
   a schema is a feature, however small, and takes every section whose condition holds.
3. **A spec states what, never why.** Where the project keeps decision records, the reasons live there
   and the spec names the section it implements. Where a spec and a decision disagree, the decision
   wins and the spec is corrected — by the person, not by whoever is implementing it.
4. **Contracts hold only what other code depends on** — a table or schema, a message or payload, a
   function another component calls, an HTTP or command-line surface, a setting's or metric's name —
   with exact names and shapes. A name used inside one component is left out: the implementation lays
   it down, and a spec that fixes internal names and types becomes a second copy of the code that
   drifts from it with every change. The test for each entry: would anything outside the component
   that implements it — other code, a stored row, a dashboard, an operator's command — break if its
   name or shape changed? If not, it is internal. So is a function placed in a shared package that only
   this change calls, and so is the order of steps inside the component's work: **Behaviour and
   failures** says what those steps leave behind, not how they run. An earlier spec that names
   internals is no precedent.
5. **Behaviour and failures is the list the tests are written from.** It names the main path and the
   paths the tests must cover — what invalid input, a repeat or a failing dependency leaves behind,
   and, where the change holds state, a restart or a partial write — so they are decided before the
   code and not discovered in it. Each entry is a result a test can assert: "errors are handled" is
   not one, "a payload with no `id` is rejected and nothing is stored" is. The level each test takes is
   `test-principles`'.
6. **How to see it working is a hint, not a check.** It exists only where the change shows only in a
   running process — a request answered, a message consumed, a log line written — and says in words
   what to do to the process and what shows the change working. It names no command and no environment
   to start: whoever checks the change works those out from the project.
7. **A step the person must take is written as theirs, as the command they run.** Anything an agent
   may not do — handling a secret, deleting from an environment the person has not said is the agent's
   to change, an action needing an account it does not hold — goes into **Steps for the person**. Where
   the step edits what an agent may not read, such as a file of secrets, the command is a script the
   agent writes: it adds only what is missing, prints the names it touched and never their values, and
   can be run twice; what it prints is what shows the step done.

### Checked before code, frozen after

8. **What the spec says about today's system is checked while it is written, before any code
   exists.** A fix's cause is reproduced, or read in the code that produces it; where neither is
   possible, the spec says why. A feature's statements about what already exists — the code it extends
   or calls, the schema and the data it assumes, the decision records it implements — are set against
   the code, the data and the records themselves. A statement that fails its check is corrected with
   the person, then checked again. A check reads; one that writes to an environment, costs money or
   calls a real external system runs only once the person agrees, told what it touches, and without
   that agreement it is not run, and is reported as not run. Whether an environment is anyone else's is
   theirs to say.
9. **A spec is ready only once the person has accepted it and its statements have passed their
   check.** Its status says so, and until then it is a draft that no implementation starts from.
10. **A ready spec's goal, scope and contracts change only with the person's consent.** **Goal**,
    **In scope / out of scope** and **Contracts** are frozen, and so is a fix's **Symptom**: whoever
    implements the spec stops and asks before changing what the change does, what it leaves alone or
    what other code relies on, and never rewrites them to match what was built. The scope's **Code**
    line says where the work is expected, not a limit: code elsewhere is free
    (`delivery-change-contract` rule 1) unless it changes a contract. A cause that turns out
    wrong goes back to the person too, since the fix it implies is a different one. A change the person
    agrees to is recorded in the spec, with its reason. **Behaviour and failures** and **How to see it
    working** may be refined during the work, the edit visible in the diff — a refinement that drops a
    path or changes what **Goal** promises is a change of scope, and asks first.
11. **A spec is implemented once its change is, and the change says so.** Its status moves from `draft`
    to `ready` to `implemented`, and `implemented` is set in a commit of the change that implements it.
    The mainline then reads `implemented` only for a change that has landed: a spec still `ready` there
    has not, whether or not work on it began. An implemented spec is not implemented again; a further
    change to what it delivered is a spec of its own. Where the project keeps an index of its specs, a
    new spec gets its row when it is written, and the row changes with the status, in the same change;
    where it keeps none, none is made — the status lines are the index.

## Hard stops

- Asked to record why a design was chosen, or which alternatives were rejected → stop; that is the
  project's decision record, and the spec points at it.
- Asked to write the code, the tests or the commit for a spec → stop, this skill writes only the spec;
  implementing a ready spec is `/pyhouse-delivery:implement`, under `delivery-change-contract`, and
  tests are `test-principles`.
