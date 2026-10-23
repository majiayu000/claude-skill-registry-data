---
name: php-patterns
description: "Use when writing or reviewing pure PHP at the language level, whatever the framework: typing, error handling, OOP patterns, comparison and array semantics, time/money/text values, dependencies, the execution surface, the test runner. The framework layer above it is skills/laravel-conventions."
---

# php-patterns

Step 6 of the pipeline (`WORKFLOW.md`), upstream of the Laravel layer: the language itself, before
the Eloquent/Laravel conventions that stack on top (see `gimli`, `morpheus`). Every rule below holds in a
repo with **nothing installed** (`CONVENTIONS.md`, rule A).

**Boundary with the framework layer** (audit, 2026-08-06): `skills/laravel-conventions` now holds it, mined
from an org catalogue of 45
skills on the framework layer — routing, tests, config, control flow, package choices, CRUD via the REST
API. **Where it's installed, it is the authority there.** This block stays deliberately below it: the PHP
language itself, on any framework. Don't add a Laravel rule here.

**An applied override is recorded, not hidden.** Where the framework layer or an installed org catalogue
decides a case this block also speaks to — §1.1 is the standing example — write what the governing rule
requires, and leave one short neutral trace addressed to whoever can decide (a line in the PR description, the
task summary or an ADR): which rule was overridden, by what, and that it is a resolved case. Never phrase it
as "a conflict between mentis and the house rules" to a non-technical stakeholder — that framing reads as
broken even when the case is a normal, resolved one, and has already caused a real project to get abandoned
and restarted over nothing. Raise one specific, named question to the decider only when no rule anywhere
actually resolves the case.

## When
As soon as PHP is written or reviewed, on any framework: this block is the common base, the Laravel
conventions apply on top of it, not instead of it.

## Steps

**Read only the sections the task actually touches.** The rules live one file per section under
`references/`; loading all six for a change that renames a method is waste, and a section read is a
section that has to be applied. If you are reviewing a whole diff, pick the rows whose trigger the diff
meets, not the whole table.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Typing | a signature, a property or a closed set of values is typed | [`01-typing.md`](./references/01-typing.md) |
| 2 | Error handling | a failure is raised, caught, converted or reported | [`02-error-handling.md`](./references/02-error-handling.md) |
| 3 | OOP and structure | a class, an interface, a trait or a static is introduced | [`03-oop-and-structure.md`](./references/03-oop-and-structure.md) |
| 4 | Comparison, arrays and the standard library | a comparison, a possibly-absent value, or an array transformation is written | [`04-comparison-arrays-stdlib.md`](./references/04-comparison-arrays-stdlib.md) |
| 5 | Time, numbers and text | a date, a money amount, a numeric input or non-ASCII text is handled | [`05-time-numbers-text.md`](./references/05-time-numbers-text.md) |
| 6 | Dependencies, the execution surface and the test runner | a package is added or updated, a statement, shell command or include path is built outside a framework layer, or the test runner is configured | [`06-dependencies-execution-tests.md`](./references/06-dependencies-execution-tests.md) |

## Output / checkpoint
Code compliant with the six sections above, checked on top of the applicable Laravel conventions
through `gate` (7) and `review` (8, `gimli`). **On framework-free PHP those two steps have no framework layer
to lean on**: the checkpoint is then the six sections above plus whatever test runner the project
actually has, and "no static analyser installed" is a finding to report rather than a checkpoint to skip
silently — §1.11 is the reason the analyser is worth asking for in the first place.

## Guardrails
No comments in the code produced (team rule, all repos). This block has no deep internal
production experience behind it (the operator is new to PHP, as noted on `gimli`): if a rule here
diverges from a real need observed in the field, fix this block rather than treating it as settled.
Never restate what a formatter already enforces — brace placement, line length, keyword casing and import
order are Pint/PHP-CS-Fixer's job, and a rule here that a formatter could apply is a rule in the wrong
place. `declare(strict_types=1)` is in §1.1 because it is the one PSR-12 item that changes runtime
behaviour, and it is overridden on Laravel (§1.1 says how).

## Origin
Sourced from PHP-FIG (PSR-12 style, the base PSRs), the official PHP documentation (types, enums,
`readonly`, `match`, comparison and array semantics, `DateTimeImmutable`, the multi-byte and cryptographic
functions) and established modern PHP market practice. The full provenance, the source stamps and the
refresh log are in [`references/origin.md`](./references/origin.md). Read it when checking whether a rule
is still current, not when applying one.
