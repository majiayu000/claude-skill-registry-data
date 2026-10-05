---
name: developing-frontend-ui
description: >-
  Guides building interface components test-first: listing each variant, state, and interaction as its own cycle,
  choosing which failing check starts it, and judging tokens, primitives, and logic placement as the component grows.
when_to_use: >-
  Use when building or changing React components, pages, or interactive states, before writing the component code.
compatibility: Requires a React project with component, accessibility, and browser test targets.
---

# Developing Frontend UI

This skill is scoped to React interfaces, and every rule it applies is owned elsewhere:
[React Standards](../../../repo-governance/development/quality/stacks/react-standards.md) for components, state, tests,
and browser security;
[TypeScript Standards](../../../repo-governance/development/quality/stacks/typescript-standards.md) for typing;
Accessibility and its modules; Design Tokens; Utility-First Styling where adopted; and
[Test-Driven Development](../../../repo-governance/development/tdd-policy.md). It carries only the procedure and
judgement of building a component under those rules.

## List the Increments Before the First Test

From the design and the acceptance criteria, list every variant, state, and interaction as a separate increment. For an
interactive component, consider default, hover, visible focus, active, disabled, loading, error, success, and empty.
Keep the ones the design or criteria name, and record the rest as not applicable.

Each increment gets one red, green, and refactor cycle, run as
[Red, Green, Refactor](../../../repo-governance/workflows/quality/red-green-refactor.md) sets out. A state discovered
halfway through a cycle is added to the list, never folded into the cycle in flight.

## Choose the Check That Fails First

| The increment is about                     | Start with a failing                                               |
| ------------------------------------------ | ------------------------------------------------------------------ |
| what renders for given props or a variant  | component test that finds elements by role, label, or visible text |
| a name, role, state, or keyboard behaviour | accessibility assertion in the component test                      |
| a flow that crosses components or pages    | end-to-end journey at the served origin                            |

Write the accessibility assertion before adding interactive states or roles. Appearance has no failing automated check
to start from: the real-browser check in Behaviour Change Verification confirms the visual result matches the design,
and contrast per theme follows Design Tokens. A red counts only when it fails on an assertion about the missing
behaviour; a render crash or a missing import is repaired first. The roles and keys each component type needs are in
Component Roles and Keys, and journeys follow
[End-to-End Testing](../../../repo-governance/development/end-to-end-testing.md).

## Keep Logic Out Before It Grows In

While making a test pass, watch for the component starting to branch on a business rule. Move that rule into a plain
function with its own unit test, and let a hook adapt it. When component state begins to mirror data a server owns, that
data belongs in the query cache instead. Both moves are cheap at the first branch and expensive at the fifth.

## Reach for the Role, Not the Value

Pick the token role that names the concept, not the value that looks right today. When no role fits, test the need
against the conditions in Design Tokens before adding one; failing them, it is a question for the design, not a local
value. Check contrast in every theme the component renders in, since a pair that passes in one proves nothing in the
other.

## Compose the Primitive Before Building One

Before building a control, look for the shared primitive the design names. Composing it inherits its roles, keys, and
states. A hand-built control has to reproduce every one of them, and a native element beats both where it serves.

## Refactor Against the User's View

During refactor, confirm the tests still act as a user does: no assertion on a class name, internal state, or instance
method. Confirm every state is reachable by keyboard and every target meets Forms and Targets.

## Before Handing Off

- the automated accessibility check passes in every interactive component's tests;
- the manual Release Check is still owed, since automation never replaces it; and
- each changed state and viewport has been seen in a real browser, per Behaviour Change Verification.
