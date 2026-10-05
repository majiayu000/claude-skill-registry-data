---
name: programming-javascript
description: >-
  Guides JavaScript work under the JavaScript standard: confirming the file is type-checked, typing through JSDoc,
  validating input the checker cannot see, and noticing floating promises and swallowed errors before handing off.
when_to_use: >-
  Use when writing, changing, or reviewing authored JavaScript, such as a script, tool, or module, before the first test
  of the change.
compatibility: Requires a JavaScript project with type check, lint, format, and unit test targets.
---

# JavaScript Programming

Every JavaScript rule is owned by
[JavaScript Standards](../../../repo-governance/development/quality/stacks/javascript-standards.md).
[Test-Driven Development](../../../repo-governance/development/tdd-policy.md) and
[Test Boundaries and Gates](../../../repo-governance/development/quality-gates.md) govern tests and gates,
[Red, Green, Refactor](../../../repo-governance/workflows/quality/red-green-refactor.md) runs each cycle, and
[Developing Applications](../developing-applications/SKILL.md) carries the judgement that holds in every language. This
skill adds only the procedure and judgement of applying them in JavaScript. Where a sentence here seems to state a rule,
the standard decides.

## Start From What the Project Records

1. **Find how the file is checked.** Read the compiler configuration and, under per-file checking, the top of the file.
   A file you are about to change that nobody checks is a finding to raise before you add to it.
2. **Compare the configuration with the standard.** A relaxed option or a lint rule switched off is not a baseline to
   copy into new code.
3. **Run the type check, lint, format check, and tests on the untouched tree.** A gate already failing is handled under
   [Preexisting Error Resolution](../../../repo-governance/principles/root-cause-orientation.md).
4. **List the increments,** each one observable behaviour, simplest first, including every expected failure path.

## Type Through JSDoc as You Write

Write the JSDoc for a function before its body: the parameter and return types, and the failures it can report. A
function whose types are hard to write usually takes a shape that is not yet decided, and settling it now is cheaper
than after several callers depend on it. Run the type check as part of each green, not only at the end.

When the checker rejects a change, fix the code. Reaching for an expected-error directive means the design needs
attention, and the directive, when truly warranted, carries the reason the standard asks for.

## Find the Input the Checker Cannot See

The checker trusts every JSDoc claim, so a type on data from outside is only as good as the check behind it. Look for:

| Where data enters                  | What to ask                                      |
| ---------------------------------- | ------------------------------------------------ |
| `JSON.parse` of a file or response | does a guard or schema run before the first use? |
| `process.env` or the command line  | is a missing or malformed value rejected early?  |
| a request body or query            | is the shape checked once, where it arrives?     |
| a dynamic `import()` or `require`  | is the loaded module's shape assumed?            |

Each answer that is no becomes an increment with a failing test for the bad input.

## Notice the Async and Error Slips

- A call returning a promise, written as a statement with nothing awaiting it, is a floating promise; the standard's
  Language Defaults decide what it becomes.
- A `catch` that logs and continues is a swallowed error unless the caller really does not need to know.
- A `throw` of a string or plain object loses the stack trace.
- A `forEach` with an `async` callback does not wait for anything; iterate with `for...of` and `await`, or collect the
  promises and await them together.

## Place a Test by What It Touches

A test that writes a file, reads the environment, or spawns a process belongs to the integration layer. To keep a
decision under unit test, pass in the text, the parsed value, or the setting, and let the entry point do the reading.

## Before Handing Off

- The type check, lint, and format gates pass, and then the fast gate.
- Every file changed is covered by the type check.
- Every input from outside passes a runtime check before use, with a test for the bad case.
- No promise floats and no error is swallowed.
- No compiler option, lint rule, or coverage exclusion was relaxed to let the change pass.
