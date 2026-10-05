---
name: plan-writing-gherkin-criteria
description: >-
  Guides writing Given/When/Then acceptance scenarios that describe observable behaviour and can actually fail.
when_to_use: >-
  Use when authoring or reviewing the acceptance criteria in a plan's prd.md.
---

# Writing Gherkin Criteria

A scenario states a condition that could fail. That is the whole test of a good one.

## The Three Clauses Do Different Work

- **Given** — the state before, and only what matters. Setup that no clause depends on is noise, and noise is where
  wrong assumptions hide.
- **When** — one action. Two actions means two scenarios, or a scenario that cannot say which action caused the result.
- **Then** — one observable outcome. Observable means someone or something outside the system can see it.

## Observable, Not Internal

`Then the cache is warmed` describes an implementation. It will be marked complete by whoever wrote the cache, and it
will keep passing after the cache is removed.

`Then the second request returns without contacting the upstream service` describes behaviour. It survives the rewrite,
and it fails when the behaviour goes away — which is the only thing it was for.

## Falsifiability Is the Filter

Ask: what would this look like if it were false? A scenario with no answer is not an acceptance criterion. It is a
statement of intent that has been formatted like one.

`Then the interface is intuitive` has no failing case. `Then a first-time user completes checkout without opening help`
does.

## One Scenario, One Claim

A scenario asserting several things fails as a unit and reports nothing about which part broke. Splitting costs a few
lines and buys a diagnosis.

## Stable Identifiers

Each scenario carries an identifier that does not change when the text is edited or the list is reordered. Delivery
items cite it, reviews record against it, and other implementations match on it.

Renumbering scenarios silently breaks every reference to them, and nothing reports the break — the citations still
parse, they just point somewhere else now.

## Write Them Before the Technical Shape

Criteria written after the design describe the design. Written before, they constrain it, which is the entire reason to
write them down rather than assume them.
