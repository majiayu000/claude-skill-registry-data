---
name: code-standards
description: >
  The binding, numbered definition of good code for this codebase. Generation agents read it
  BEFORE writing any code; review skills cite violations by rule id (CS-n). Use whenever the user
  says "code standards", "what is good code", "coding rules", or before generating application
  code in any pipeline step.
---

# Code Standards

Every rule here is checkable by reading the code — no vibes. Generators comply; reviewers cite CS-n. A rule that can't be verified by inspection doesn't belong in this file.

## Naming

- **CS-1** Class names carry their type suffix: `Controller`, `Job`, `Service`, `Event`, `Listener`, `Factory`.
- **CS-2** Queued classes carry the `Job` suffix; trigger-listeners are named `{Verb}On{Event}Listener`.
- **CS-3** Service primary methods are intent-named (`check`, `create`, `process`, `store`) — `handle()` is reserved for framework contracts.
- **CS-4** Enum cases are `ALL_CAPS_SNAKE_CASE`.
- **CS-5** A name states what comes out, not how it works (`priorComposites`, not `loopAndFilterList`).

## Structure

- **CS-6** Guard clauses and early returns over nested conditionals; no `else` after a return.
- **CS-7** A self-contained block of 4+ lines (input → transform → one output) becomes an intent-named private method.
- **CS-8** Never extract: guard clauses, single statements, or blocks mutating 2+ enclosing-scope locals — over-extraction reads worse than inline code.
- **CS-9** One responsibility per class; a method reads top-to-bottom at one level of abstraction.
- **CS-10** Paired classes (sibling drivers, mirrored paths) stay symmetric: same shape, same extractions.

## Comments

- **CS-11** No inline what-comments — the code self-explains through names; a comment restating the next line is deleted.
- **CS-12** A genuine why (race condition, idempotency gate, security rationale, external quirk) lives in the method PHPDoc, never inline.
- **CS-13** Commented-out code never ships.

## Simplicity

- **CS-14** No interface with a single implementation — unless a swap requirement exists today, in which case use the driver pattern.
- **CS-15** No config entry for a value that never changes; constants live where they're used.
- **CS-16** Framework feature over hand-rolled equivalent: if Laravel ships it (validation, throttling, casting, scheduling), use it.
- **CS-17** Fewest files that work — no scaffolding, folders, or base classes "for later".

## Framework Idiom

- **CS-18** Validation lives in FormRequests, never inline in controllers.
- **CS-19** Authorization lives in Policies/Gates, never inline role checks scattered in controllers or views.
- **CS-20** Relationships via Eloquent (`hasMany`, `belongsTo`), not manual joins; no raw SQL with user input.
- **CS-21** Slow or external work (mail, HTTP, image processing) is queued, never inline in a request.

## Data Safety

- **CS-22** Every trust boundary (user input, webhook payload, CSV cell, query param) validates before use; mass assignment stays guarded.
- **CS-23** Multi-write operations wrap in one transaction; partial writes are a bug.
- **CS-24** Any new query path eager-loads its relations — an N+1 is a defect, not a style issue.

## Errors & Tests

- **CS-25** No swallowed exceptions, no empty catch — fail loud or handle for real.
- **CS-26** Every behavior change ships with a test named by the behavior it proves.
- **CS-27** A bug fix starts with a red regression test (see red-first skill); no fix commits without one.

## Placement

- **CS-28** Class placement follows the vsa skill's rules — slice-first, events as seams; not restated here.

## Formatting

- **CS-29** PSR-12 compliance, enforced by Pint (`vendor/bin/pint`) — formatting is the tool's job; never hand-format against it, never argue style Pint already settles.
- **CS-30** Static analysis must pass: PHPStan — Larastan in Laravel projects (`vendor/bin/phpstan analyse`). New code introduces zero new errors at the project's configured level; never fix an error by adding a baseline entry or `@phpstan-ignore` without a PHPDoc why.

## Consumers

- Generation agents (task-backend, task-frontend, tuhin twin) read this file before writing code.
- The review skill cites CS-n in findings; readability-sweep enforces CS-1..13 mechanically.
- If this file conflicts with a target project's `docs/conventions.md`, the project wins — flag the delta instead of silently following either.
