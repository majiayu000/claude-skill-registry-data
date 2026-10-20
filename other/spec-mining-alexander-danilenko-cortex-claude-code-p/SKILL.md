---
name: spec-mining
description: "Apply this opinionated workflow when reverse-engineering legacy or undocumented systems: scope, explore the code, trace data flows, document in EARS format, flag uncertainties. For code archaeology, onboarding, and requirements extraction."
---

# Spec Mining

Extract a specification from a system that has no usable documentation, by reading the code that actually runs.

The discipline that makes the output trustworthy: **separate what you observed from what you inferred.** A reader will act on this document — rebuilding a service, planning a migration, onboarding — and a confident-sounding guess is worse than an acknowledged gap, because nobody goes back to check it.

## Approach

Work outside-in: entry points, then routes, then the services behind them, then the data layer. Following an actual request path teaches you the system's real structure, which is often not the structure its directory names advertise.

Read the tests too. They document intended behaviour and edge cases someone hit in production, and they are usually more honest than any comment or README in the repo.

Read the migration history as well. Migrations are dated and ordered, so they show how the schema arrived at its current shape — which columns were added under pressure, what was backfilled, what was renamed but never dropped. That sequence is often the only surviving record of why the data model looks the way it does.

Every observation cites its evidence — `src/auth/jwt.strategy.ts:42`. Without a location the reader can't verify a claim, and unverifiable claims are what make reverse-engineered specs rot.

## Writing observed requirements — EARS

EARS keeps requirements unambiguous by forcing the trigger and the state into the sentence, so "the system validates the token" can't hide _when_.

| Pattern     | Form                                       |
| ----------- | ------------------------------------------ |
| Ubiquitous  | The system shall [action].                 |
| Event       | When [trigger], the system shall [action]. |
| State       | While [state], the system shall [action].  |
| Conditional | While [state], when [trigger], shall …     |
| Optional    | Where [feature enabled], shall …           |

Number them by area so they can be referenced later — `OBS-AUTH-001`, `OBS-USER-002`:

```text
OBS-AUTH-001
While credentials are valid, when POST /auth/login is called, the system
shall return a JWT access token (15m) and a refresh token (7d).
Evidence: src/auth/auth.controller.ts:31, src/auth/auth.service.ts:88
```

## Uncertainties are a deliverable

Anything you could not determine from the code goes in its own section as a question, not a guess: what triggers a status transition, whether a delete is soft, which external system owns a field. This section is often the most valuable part of the document — it is the list of things a maintainer must be asked before anyone relies on the rest.

## Output

Save to `specs/{project_name}_reverse_spec.md`. Structure and section order: `references/specification-template.md`.
