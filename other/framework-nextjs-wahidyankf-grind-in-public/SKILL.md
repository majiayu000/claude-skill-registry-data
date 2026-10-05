---
name: framework-nextjs
description: >-
  Guides Next.js work under the Next.js standard: deciding server or client before writing a component, declaring cache
  behaviour before a fetch, treating each server action as a public endpoint, and testing at each framework boundary.
when_to_use: >-
  Use when adding or changing a Next.js route, layout, server component, server action, or route handler, before the
  first test of the change.
compatibility: Requires a Next.js application with its type check, lint, unit, and browser test targets.
---

# Next.js Framework

Every Next.js rule is owned by
[Next.js Standards](../../../repo-governance/development/quality/stacks/nextjs-standards.md), which builds on
[React Standards](../../../repo-governance/development/quality/stacks/react-standards.md). State, effects, and
browser-side data follow [React Framework](../framework-react/SKILL.md), component building follows Developing Frontend
UI, and [Programming TypeScript](../programming-typescript/SKILL.md) carries the language procedure. This skill adds
only the judgement of placing work across the server and client boundary. Where a sentence here seems to state a rule,
the standard decides.

## Start From What the Project Records

Read the version line and hosting choice recorded under [Version, Hosting, and Examples][version-hosting-and-examples].
Framework defaults differ between major lines, so check the recorded line's documentation, not memory, before relying on
one.

Run the type check, lint, and unit targets on the untouched tree. A gate already failing is handled under
[Preexisting Error Resolution](../../../repo-governance/principles/root-cause-orientation.md).

## Decide Server or Client Before Writing

| The component needs                                     | Place it                                                  |
| ------------------------------------------------------- | --------------------------------------------------------- |
| data, a secret, or a server-only module                 | a server component                                        |
| state, an effect, an event handler, or a browser API    | a client component at the smallest interactive leaf       |
| both                                                    | a server parent that fetches, passing a client leaf props |
| server-rendered content inside an interactive container | the container as a client component, content as children  |

A client boundary drawn high in the tree ships everything below it to the browser. When a component needs to move to the
client, first try splitting off the interactive part.

## Declare the Cache Before the Fetch

Before writing a fetch, decide whether its data is per-request, revalidated on an interval, or revalidated by tag, and
write that declaration with it. Then find every mutation that changes the same data and confirm it revalidates the same
path or tag. A page showing old data after a save usually lacks that pairing.

## Treat Each Server Action as an Endpoint

Write the refusal tests first: an unauthenticated call, an unauthorized one, and each invalid input the schema rejects.
Only then write the success case. An action is reachable by anyone who can send a request, whether or not a form in the
application calls it, so a test that only exercises the form proves nothing about the endpoint.

## Test at Each Framework Boundary

| Under test                             | Test as                                               |
| -------------------------------------- | ----------------------------------------------------- |
| a domain function                      | a plain unit test                                     |
| a server action or route handler       | a function call with its outbound boundaries replaced |
| a client component, hook, or data flow | a component test, as the React skills set             |
| routing, streaming, and loading states | an end-to-end journey in a real browser               |

Browser journeys follow Writing Browser End-to-End Tests. Layers follow
[Test Boundaries and Gates](../../../repo-governance/development/quality-gates.md).

## Before Handing Off

- the type check, lint, and unit targets passed, and the affected journeys passed in a real browser;
- each new client boundary sits on the smallest interactive leaf;
- every new fetch declares its caching, and every mutation revalidates what it changed;
- every new server action has its refusal tests; and
- each recorded red failed on an assertion about the missing behaviour.

[version-hosting-and-examples]:
  ../../../repo-governance/development/quality/stacks/nextjs-standards/001-version-hosting-and-examples.md
