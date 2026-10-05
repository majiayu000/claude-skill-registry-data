---
name: padosoft-contract-changes
description: >-
  Use this skill when something other code depends on is about to change shape — a method or function
  signature, a parameter added, removed, reordered or retyped, a return type, an overridden method, an
  interface, an event payload, a schema, a response contract, a default value. Also when the user reports a
  signature-incompatibility error, a caller broken after a refactor, a child class that no longer matches
  its parent, a fixture failing after a schema was tightened, or asks how to change an API without breaking
  consumers. It gives the search that finds every dependent, the classification that says what is breaking,
  and the rule that the whole change lands together. Do not use it for designing an API from scratch, for
  versioning a public package, or for database migrations (padosoft-database-design covers those).
license: MIT
compatibility: >-
  Any language with callers and inheritance. The covariance rules are stated for languages that enforce
  substitutability; the search and staging procedure applies everywhere.
metadata:
  version: 0.3.0
  author: Padosoft
  summary: Changing a signature is editing everything that agreed to it.
  profiles: core
  scope: global
  repository: https://github.com/padosoft/skills
  keywords: refactoring, signature, breaking change, override, covariance, callers, contract, migration
---

# Contract changes

Changing a signature is not editing a function. It is editing **everything that agreed to it** — callers,
overrides, mocks, fixtures, serialised payloads, documentation — and the ones you do not find are the ones
that fail later, somewhere else, in a way that does not name you.

**The rule: find every dependent before you edit, classify what breaks, and land the whole change as one
coherent unit.**

---

## 1. Four kinds of dependent, and only one is obvious

| Dependent | Missed because |
|---|---|
| **Direct callers** | this is the one everybody greps for |
| **Overrides** in subclasses, traits, interface implementations | they do not *call* the method, so a call-site search never shows them |
| **Test doubles**: mocks, stubs, fakes, spies | they re-declare the signature to imitate it |
| **Frozen copies**: fixtures, recorded payloads, contract snapshots, generated clients, documentation | nothing links them to the source at all |

Search for all four, and use whatever the ecosystem gives you that understands *symbols* rather than text
before falling back to a text search:

```bash
# callers
rg -n "->\s*<method>\s*\(|::\s*<method>\s*\(|\b<method>\s*\(" src/ tests/
# overrides and re-declarations — the ones the caller search cannot see
rg -n "function\s+<method>\s*\(|def\s+<method>\s*\(|<method>\s*\(.*\)\s*[:{]" src/ tests/
# who extends or implements the declaring type
rg -n "extends\s+<Type>\b|implements\s+<Type>\b|: <Type>\b" src/ tests/
# frozen copies
rg -rn "<method>|<field>" fixtures/ __snapshots__/ docs/ openapi/
```

A dynamic call — a name built from a string, a template, a configured handler — is invisible to every
search above. If the codebase resolves anything by convention, §4 is about you.

## 2. Classify before you edit

| Change | Breaking? | What it costs |
|---|---|---|
| Add a parameter **with a default**, at the end | no | check the overrides: they need a compatible default |
| Add a parameter **without a default** | **yes** | update every caller, or add it with a default first and require it in a second step |
| Remove a parameter | **yes** | every caller, and every mock |
| **Reorder** parameters | **yes, and silently** | callers keep compiling and pass the wrong values — prefer named arguments, or do not |
| Narrow a parameter type | **yes** | every caller; and a subclass may only widen what it accepts |
| Widen a parameter type | on the parent only | subclasses may widen freely; the parent's callers keep working |
| Change the **return type** | **yes, for the hierarchy** | a subclass may narrow, never widen — and the error is often at load time, not call time |
| Change a default **value** | silently | nothing breaks; behaviour changes for every caller that omitted it |

The last row is the dangerous one, because nothing anywhere goes red.

And one trap the table above hides: **an optional trailing parameter is additive for callers and breaking
for implementers.** Adding `?T $x = null` to an interface method leaves every call site valid and makes
every existing implementation of that interface invalid — in a language that checks the declaration, the
class fails to load, before a line of its own code runs. If the interface is public API that other people
implement, the parameter is not the mechanism: add an optional capability interface, or carry the new fact
in an extension channel that already exists.

## 3. The whole change lands together

Parent, every subclass, every caller, every mock, every fixture: **one commit, or one pull request whose
intermediate states nobody has to deploy.** Never merge a state where parent and child disagree — in a
language that checks substitutability, that is not a failing test, it is a class that will not load, and it
takes the whole module with it.

"I will fix the rest after" is how a refactor becomes an outage.

Then let the tools confirm it: static analysis catches signature incompatibility before any test runs, and
it is the cheapest check in the sequence. Run it **before** the suite, not after.

## 4. Convention-resolved dependents fail silently

When a framework wires things by naming convention — a handler resolved from a string, a listener looked up
by table name, a property whose name must match a key, a file whose path is computed — then a rename does
not produce an error. It produces **nothing**: the code is never called, and no exception is thrown.

```text
resolved = table + "EventService"   →  rename the class, and the hook simply stops firing
```

Two protections: a test that asserts the wiring resolves (not that the handler works — that it is *found*),
and a startup check that fails loudly when a declared name has no implementation.

## 5. The same rule, one level up

A signature is the smallest contract. Everything below is the same shape at a different altitude:

- **An event payload** other services deserialise. Adding a field is safe; removing or retyping one is not,
  and the consumers are in another repository.
- **A schema that gets tightened.** Validation that becomes stricter breaks the fixtures and the stored
  documents that were written under the looser rule — they must be migrated in the same change, or the
  tightening must be staged.
- **A stored contract.** Recorded requests, cached serialisations and snapshots were frozen under the old
  shape and will be read under the new one.
- **A template that includes a partial owned by another repository.** The include is a runtime
  dependency on that repository's current state: rename or remove the partial on one side and the page
  fails on the other, at request time, with nothing in either repository's tests to catch it. Use the
  conditional form of the include, or copy the partial and accept the duplication deliberately — and when
  a shared partial starts receiving a new variable, guard its presence until every consumer passes it.
- **A producer moving from synchronous to queued**, or the reverse: the contract that changes is the timing
  and the failure mode, and callers depend on both.

## 6. Staging a breaking change you cannot land at once

When the dependents are outside your reach:

1. **Add the new shape alongside the old**, with the old delegating to it.
2. **Make the old one warn** — a deprecation that names the replacement and is visible where the caller runs.
3. **Migrate the dependents**, tracking them against the list from §1.
4. **Remove the old one**, once the list is empty and long enough has passed for the slowest consumer.

Steps 2 and 4 are the ones that get skipped, in opposite ways: no warning, or no removal ever.

---

## Gotchas

- **A caller search proves nothing about overrides.** They are the dependents that never call you.
- **Reordering parameters of the same type is the quietest breaking change in software.** Everything still
  compiles.
- **Changing a default is a behaviour change for code nobody touched**, and it will be attributed to
  whatever ran next.
- **Mocks re-declare the contract**, so a suite can stay green against a signature that no longer exists.
- **Documentation and generated clients are dependents.** See **`padosoft-docs-match-code`**.
- **The error can arrive at load time**, far from the change, naming two classes and no line of yours.

## Checklist

- [ ] Callers, overrides, test doubles **and** frozen copies all searched
- [ ] Convention-resolved dependents considered; wiring asserted by a test
- [ ] Every change classified as breaking or not, including default-value changes
- [ ] Return-type change checked against every subclass in the hierarchy
- [ ] Parent, children, callers, mocks and fixtures in one coherent change
- [ ] Static analysis run **before** the test suite
- [ ] If staged: new shape added, old one deprecated with a named replacement, removal scheduled

## Final report

```
Contract: <symbol / event / schema>
Change: <what> → breaking: yes | no (why)
Dependents found: callers <n> · overrides <n> · doubles <n> · fixtures/docs <n>
Convention-resolved: none | <what, and the test that asserts it>
Landed: one change | staged (<step reached>, removal due <when>)
Static analysis: <tool> clean before tests: yes | no
```
