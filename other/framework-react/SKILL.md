---
name: framework-react
description: >-
  Guides React state, effects, and data work under the React standard: finding each value's narrowest home, deciding
  whether an effect is needed at all, keeping server data in the query cache, and testing hooks and data flows.
when_to_use: >-
  Use when adding or changing React state, an effect, a custom hook, or server data fetching and mutation, before the
  first test of the change. Component building belongs to the frontend UI skill.
compatibility: Requires a React project with its type check, lint, and component test targets.
---

# React Framework

Every React rule is owned by [React Standards](../../../repo-governance/development/quality/stacks/react-standards.md),
typing by [TypeScript Standards](../../../repo-governance/development/quality/stacks/typescript-standards.md), and
[Programming TypeScript](../programming-typescript/SKILL.md) carries the language procedure. This skill covers state,
effects, and data only. Building components, their variants, accessibility, and tokens belongs to Developing Frontend
UI; when a change does both, use both. Where a sentence here seems to state a rule, the standard decides.

## Start From What the Project Records

Read the store, query, and form choices recorded under the standard's
[Library Decisions](../../../repo-governance/development/quality/stacks/react-standards/001-library-decisions.md). When
the change needs a library that is not recorded, raise it as a decision rather than adding one quietly.

Run the type check, lint, and component tests on the untouched tree. A gate already failing is handled under
[Preexisting Error Resolution](../../../repo-governance/principles/root-cause-orientation.md).

## Find the Value's Home Before Declaring It

Ask of each new value, in order, and stop at the first yes:

| Question                                                            | Home                                      |
| ------------------------------------------------------------------- | ----------------------------------------- |
| can it be computed from props, state, or cached data?               | a value computed during render, not state |
| does a server own it?                                               | the query cache                           |
| does only one component read or change it?                          | that component's state or reducer         |
| do a parent and its near children share it?                         | the parent, passed down as props          |
| does a distant part of the tree need it, and does it change often?  | the recorded store                        |
| does a distant part of the tree need it, and does it rarely change? | context                                   |

A value that later needs a wider home moves one step at a time, with the tests proving each move.

## Question Every Effect

Most effects are not needed. Before writing one, check:

- a value derived from others is computed during render;
- a response to a user action runs in that action's event handler;
- server data comes from the query cache, which already handles ordering, cancellation, and stale responses; and
- resetting state when an identity changes uses a key on the component, not an effect that clears it.

An effect that survives these checks synchronizes with one external system, such as a subscription or a browser
interface. Write its cleanup in the same change, and test that unmounting or changing a dependency releases what it
started.

## Keep Server Data in the Cache

Give each query a key built from everything that changes its result, so two different requests never share an entry.
After a mutation, invalidate or update exactly the entries whose data it changed; a stale screen after a save usually
means a missed key. Loading and error states come from the cache, never from state flags kept beside it.

## Test at the Hook and Data Boundary

A custom hook is tested through a small component or a hook renderer that uses it as a component would. The domain
function it adapts is tested on its own, as a plain function. A data flow is tested with a fresh query cache per test
and the network replaced at the request boundary, so a test proves what the user sees on success, on failure, and while
loading. Each failure path gets its own test, and assertions stay on what renders, as the standard's tests section sets.
Layers follow [Test Boundaries and Gates](../../../repo-governance/development/quality-gates.md).

## Measure Before Memoizing

Add memoization only after a profile shows a render cost that matters, and keep the measurement in the change. A
memoized value whose dependencies change on every render costs more than it saves.

## Before Handing Off

- the type check, lint with the hooks rules, and component tests all passed;
- each new value sits in the narrowest home the table gives, and no server data was copied into state;
- every effect names its one external system and its cleanup is tested; and
- each recorded red failed on an assertion about the missing behaviour.
