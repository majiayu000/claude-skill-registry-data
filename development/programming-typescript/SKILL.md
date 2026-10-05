---
name: programming-typescript
description: >-
  Guides the procedure for writing or changing TypeScript: loading the TypeScript standard first, driving each increment
  test-first, finding which rule a decision falls under, and confirming the gates before handing off.
when_to_use: >-
  Use when writing, changing, or reviewing TypeScript code, before the first edit, alongside the language-agnostic
  application skill.
compatibility: Requires a TypeScript project with type check, lint, format, and unit test targets.
---

# Programming TypeScript

[TypeScript Standards](../../../repo-governance/development/quality/stacks/typescript-standards.md) owns every
TypeScript rule, strict typing included. This skill restates none of them. It carries the procedure for applying that
standard, and the judgement of noticing which rule a decision falls under.
[developing-applications](../developing-applications/SKILL.md) covers the language-agnostic judgement, and
[Red, Green, Refactor](../../../repo-governance/workflows/quality/red-green-refactor.md) owns the test-first cycle.

## Before the First Edit

1. **Read the standard.** Read TypeScript Standards in full, plus
   [React Standards](../../../repo-governance/development/quality/stacks/react-standards.md) or
   [Next.js Standards](../../../repo-governance/development/quality/stacks/nextjs-standards.md) when the code uses them.
2. **Compare the project's configuration with it.** A relaxed compiler option or a lint rule switched off is a finding
   to raise, not a baseline to copy into new code.
3. **Read the tests that cover the code** before interpreting or changing it.
4. **List the increments,** each one observable behaviour, simplest first, including every expected failure path.

## Drive Each Increment Test-First

Run each increment through Red, Green, Refactor at the narrowest target that can prove it, usually a unit test with its
operating-system-facing dependencies injected. Run the type check as part of each green, not only at the end: a type
error discovered after several cycles tends to force a redesign of work already written.

When the compiler rejects a change, fix the code. The standard lists what never silences a type error, and reaching for
one of those means the design, not the checker, needs attention.

## Notice Which Rule Applies

These moments recur. Each points at the part of the standard that decides it:

| While writing, you meet                                               | Apply, in TypeScript Standards |
| --------------------------------------------------------------------- | ------------------------------ |
| data arriving from a request, file, storage, or the environment       | Typing Rules, on validation    |
| a value whose shape is not known yet                                  | Typing Rules, on `any`         |
| two flags or optional fields that must never be set together          | Typing Rules, on unions        |
| two identifiers or quantities of the same primitive that must not mix | Typing Rules, on branded types |
| a call that can fail during normal operation                          | Expected Failures Are Returned |
| a promise started without being awaited or returned                   | Expected Failures Are Returned |
| a business decision taking shape inside an effectful function         | Typing Rules, on code shape    |

To decide between a returned failure and an exception, ask whether a caller in normal operation would need to handle it.
If it would, the failure is expected, and it gets its own test.

## Before Handing Off

- The type check, lint, and format gates pass, and then the fast gate from
  [Test Boundaries and Gates](../../../repo-governance/development/quality-gates.md).
- Every increment carries its red, green, and refactor records.
- The diff has been read once against the Typing Rules section, looking for what no linter sees, such as a failure
  thrown where callers should expect it.
- No compiler option, lint rule, or coverage exclusion was relaxed to let the change pass.
