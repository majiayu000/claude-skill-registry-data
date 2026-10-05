---
name: exploratory-testing
description: >-
  Guides session-based exploratory testing of a running interface or API: framing charters, choosing tours, citing a
  specification, contract, or design for every expected result, telling a defect from a gap, and staying
  non-destructive.
when_to_use: >-
  Use when exploring a live web interface or API for correctness, edge-case, and consistency defects, or when judging
  whether an exploratory finding is grounded.
compatibility: Requires a running surface reachable from a real browser or request client, and its specifications.
---

# Exploratory Testing

[Exploratory and Usability Review](../../../repo-governance/workflows/quality/exploratory-usability-review.md) owns the
sequence: declared tasks, one bounded pass, and a terminal result. Enumerated Coverage and Usability Probes and
Completeness own the sweeps that enumerate instead of sampling; Evidence Safety and Accessibility owns what a capture
may hold; and [API Testing](../../../repo-governance/development/api-testing.md) owns the direct request an API change
needs. This skill covers the tester's judgement inside that pass.

## Frame Each Charter as a Mission

A charter names what to explore, with which resources or constraints, and what kind of information or risk it should
reveal. For example: explore the discount field on checkout, with expired, stacked, and malformed codes, to reveal
pricing and validation defects.

A charter as broad as "explore checkout" finds whatever lies on top. One that lists clicks is a script and cannot
discover that a path was impossible to find. The workflow's declared tasks are these charters, frozen before the pass
starts. Anything found outside a charter is still recorded, marked as outside it.

## Vary the Angle With Tours

| Tour                                                      | Tends to find                         |
| --------------------------------------------------------- | ------------------------------------- |
| the primary journeys, in varied order                     | defects in the flows people depend on |
| a record's lifecycle: create, change, store, show, remove | values altered or lost between steps  |
| hostile input: invalid, boundary, oversized, out of order | validation and error-handling defects |
| one action repeated, quickly and many times               | state and timing defects              |
| the least-used settings and corners                       | paths nobody tested                   |
| the same view across viewport, locale, and theme          | text and layout defects under change  |

Against an API, the same tours become operations called in varied order, a resource's lifecycle, malformed requests,
repeated and concurrent calls, the ends of pagination, and requests with credentials missing or expired.

## Cover the Product, Not the Screens

So coverage is not an accident, check the charter set touches each element of the product: its structure, what each
function computes, the data at its limits, its interfaces to other systems, the platforms it runs on, the operations
real users perform, and time, such as expiry, ordering, and races.

## Cite Every Expected Result

Each expected result names its source: a scenario in the specification, a clause of the contract, an approved design, or
an independent computation. When no source exists, record an open question, not a defect. When live behaviour
contradicts an existing scenario, the scenario wins, and the defect quotes it.

## Defect or Gap

Behaviour that is correct, intended, reproducible, and owned by the target, yet protected by no scenario, is a
specification gap. Propose a scenario, written as [Writing Gherkin Criteria](../plan-writing-gherkin-criteria/SKILL.md)
teaches, for its owner to confirm; never write it into the specification directly. Edge cases such as empty results,
boundaries, and recovery are the richest source. When it is unclear whether behaviour is intended, record a question.
Behaviour a third party or the browser owns is neither.

## Stay Non-Destructive

Observe; never attack.

- **Allowed:** navigating, filling forms with obviously synthetic data, reading responses and headers, safe read
  requests, and a single malformed read to see the error shape.
- **Only with authorization for this run:** any state-changing action, such as a deletion, a purchase, or an API write,
  using synthetic data, a test account, and cleanup. Without it, stop at the confirmation step or request boundary and
  record the flow as not exercised because it changes state.
- **Never:** injection beyond one reflective probe, fuzzing at volume, guessing credentials, generating load, touching
  another account's data, or using a discovered bypass. Confirming that an unauthenticated request is refused is
  allowed; exploiting a gap is not.

Redact every credential in a captured request.

## Keep the Lenses Apart

The exploratory lens runs first and the usability lens second, as the workflow orders. Give the usability attempt to a
reviewer who never read the specification, which a first-time user lacks; with none available, label that lens
spec-aware.
