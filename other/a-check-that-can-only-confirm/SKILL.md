---
name: a-check-that-can-only-confirm
description: "[flow-learned] Design guards, tests, lint rules and verification scripts so they are capable of failing: every check gets a mutant that must make it fire, a mutant that must leave it silent, a mutant that removes its input, and an asserted non-zero count of what it examined. Use this whenever writing or changing anything that walks, greps, scans or asserts across a codebase — a repo-wide test, a claim guard, an identity roster, a seeding check, a CI gate — including when the request is only 'add a test for this' or 'make sure nothing else broke'. A check that passes because it reached nothing looks exactly like a check that passes because the code is correct, so consult this before trusting any green result."
status: promoted
promoted: '2026-09-11'
---

# A Check That Can Only Confirm

## Contract

Iron law: a check that cannot fail is not a check — prove it can fire, prove it can stay silent, and prove it reached its input. Applies whenever a guard, test, lint rule, roster walk or scan is written or changed. Returns, per check: a must-fire mutant, a must-stay-silent mutant built from a correct input that resembles the incorrect one, an input-removal mutant, an asserted non-zero count of what was examined, and one run against a real full-size input — each one executed, not just written. Permitted skips: none; a check shipped without the three mutants is unverified.

## Why a green result proves less than it looks

A guard has two failure modes and only one is loud. Reporting the wrong answer gets noticed. Reaching nothing does not: zero offending files and zero files examined produce the same green. That happens when the matcher is narrower than intended — matching a number only when a unit follows it, handling two of the four spellings a symbol is imported under — so the input the guard exists for never enters it, and nothing in the output says so.

## Write three mutants, not one

- **Must-fire** — an input the check exists to reject. This is the one everyone writes, and on its own it is satisfied by a matcher that fires on almost anything.
- **Must-stay-silent** — a *correct* input built to resemble the incorrect one as closely as you can. Without it, over-matching stays invisible until the check blocks real work, and the fix under that pressure is to exclude one more case, which just moves the false positive.
- **Input-removal** — delete an entry from the roster, empty the directory it walks, rename the symbol it starts from. The check must now fail. This is the mutant that catches a narrowed matcher, because matching nothing and having nothing to match are indistinguishable from the outside.

## Make silence say something

Assert and print a count of what the check examined, beside the count of what it found: `assert examined > 0` before `assert not offending`. A run reporting "examined 0 entries, 0 problems" is reporting a defect in itself; without the first number it reads as a pass.

## Run it against a real artifact

Fixtures are built from the same understanding that built the matcher, so they inherit its blind spot. Run the check once over a production-sized input — the whole repository, a full export, a real transcript — and reconcile its examined count against an independent enumeration before believing it.

## What to avoid

- **Inferring intent from neighbouring text.** Suppressing a match because a nearby line looks like a denial suppresses the wrong ones. Parse the structure instead of adding another exclusion.
- **Accepting a stand-in for the type under test.** A list supports indexing and `len`, so a test passing lists where the code takes a buffer never constructs the type it claims to cover.
- **Treating a value that parsed as a value that answers the question.** Assert the value's identity, not that parsing succeeded: that the number found is the one the check is about, from the field the check names.

## Verification

- [ ] A must-fire and a must-stay-silent mutant, both executed.
- [ ] An input-removal mutant that makes the check fail.
- [ ] A non-zero examined count, asserted and reported.
- [ ] One run against a real, full-size input.
