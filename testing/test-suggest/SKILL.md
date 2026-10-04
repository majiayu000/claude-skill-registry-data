---
name: test-suggest
description: Propose specific, actionable test cases for a target module — without writing the actual test code. Use this skill whenever the user wants to know "what should I test", "what test cases would catch real bugs in X", "I have a finding from test-assessment, what tests would close that gap", "suggest tests for this file", or wants to think through coverage before writing. Pairs with the test-assessment skill (which finds gaps); writing the test code itself happens as a normal follow-up task once the suggestions are reviewed. This skill stops at suggestions — if the user wants code generated, redirect them. Trigger even on casual phrasings ("what should I test in auth.ts", "give me test ideas for this module").
license: MIT
---

# Test Suggestion

Take a target — a finding from a test-assessment report, or a specific source file — and produce a prioritized, actionable list of test cases worth writing. The output is what to test and why, not the test code itself.

## What this skill does (and doesn't)

**Does:** Read the target source, recognize its branches and failure modes, learn the repo's existing test conventions, and produce a structured list of test cases ranked by importance. Each suggestion includes name, setup, action, assertion, rationale, and which test file it belongs in.

**Does not:** Write the test code. Run tests. Modify the target. Refactor untestable code. Writing the code is outside this skill's scope — if the user asks for code, complete the suggestion output first, then write the code as a normal follow-up task (not via this skill): "I can suggest the cases, but writing them is the next stage. Want me to write the code for case 1 once you've reviewed the list?"

## Core principle

A good suggestion specifies enough that someone could write the test without re-reading the source. A bad suggestion is vague ("test the happy path") or tautological ("test that it returns the right type" — TypeScript already does that). Each suggestion must be tied to a failure mode that would actually happen if the test didn't exist.

## Workflow

Do these in order. The earlier phases set context the later phases need.

### Phase 1: Understand the request

Determine input shape:

**Mode A — Pasted finding from test-assessment.** The user gives you something like:
> "Auth primitives have no unit tests — lib/password.ts, lib/auth-rate-limit.ts, lib/mfa-cookie.ts only proven via Playwright."

Multiple targets in one finding. Suggest cases for each, but group output by target file.

**Mode B — Direct target.** "Suggest tests for lib/password.ts" — single file, deeper coverage.

**Mode C — Vague request.** "What should I test?" — ask for a target before proceeding. Don't guess.

### Phase 2: Inspect the target

Run `scripts/inspect_target.sh <file>` to get a quick structural summary: exports, imports, branch count, throw sites, async-ness, line count.

Then read the source directly. Don't suggest from signatures alone — you need the implementation to know what can actually go wrong. Pay attention to:

- **Branches** — every `if`, `switch`, ternary, early `return`, error path
- **Throws and rejects** — what error states does the code declare?
- **Side effects** — DB writes, network calls, file system, mutations of arguments
- **Boundary inputs** — empty strings, zero, null, negative numbers, very large inputs, malformed shapes
- **Assumptions** — anything the code relies on that a caller might violate (env vars, ordering, prior state)
- **Security-relevant invariants** — auth checks, tenant isolation, secret handling, redaction

If the source is over ~300 lines, read it in chunks and form suggestions per logical section rather than trying to hold the whole thing in context.

### Phase 3: Learn the repo's test conventions

Before suggesting anything, look at how this repo writes tests. Read 2-3 existing test files in the same area (or, failing that, the most recent test files in `tests/` or wherever they live).

Note:
- **Framework** — Jest, Vitest, node:test, Pytest, RSpec, Go testing, PHPUnit, etc.
- **Assertion style** — `expect(x).toBe(y)`, `assert.strictEqual(x, y)`, `x.should.equal(y)`, etc.
- **Test naming convention** — `it('does X')` vs `test('does X')` vs `test_does_x`
- **Setup/teardown style** — `beforeEach` blocks, fixture functions, factory helpers
- **Mocking style** — Jest auto-mocks, `vi.mock`, manual stubs, `MagicMock`, fake-prisma harnesses, etc.
- **File location** — alongside source (`foo.test.ts`), in `tests/` subdir, in `__tests__/`
- **Fixture patterns** — sample data files, factory functions, shared setup

Suggestions must match these conventions. A Jest-style suggestion in a node:test repo means the test won't even run.

### Phase 4: Check existing coverage

Find any existing tests for this target. Look in:
- `<dir>/<name>.test.<ext>`
- `tests/<name>.test.<ext>`
- `__tests__/<name>.test.<ext>`
- Any test file that imports the target

For each existing test, note what it covers. **Don't suggest cases that already exist.** If a function has 3 cases tested and 5 untested, suggest only the 5 missing ones — and acknowledge the existing 3 in the output ("Already covered: …").

### Phase 5: Design the test cases

This is the heart of the skill. For each untested behavior worth testing, draft a case using the rubric in `references/case-design.md`. Each case must specify:

- **Name** — the eventual test name, written as a behavior statement (`"returns 401 when authorization header is missing"` not `"test1"`)
- **Type** — unit / integration / contract / E2E (see `references/test-types.md` for choosing)
- **Setup** — the preconditions to establish (concretely — "stub `db.query` to throw `ConnectionError`", not "mock the database")
- **Action** — what to call and with what inputs
- **Assert** — what to verify (concretely — "response.status === 401 AND response body matches `{ error: 'unauthorized' }`")
- **Why** — the failure mode this catches. If you can't articulate what would break in production, the case is probably not worth writing.
- **Watch out for** — optional. Tricky bits: timing, async cleanup, shared state, etc.

### Phase 6: Determine test type per case

Not every case is a unit test. Match the type to what the case actually exercises:

- **Unit** — single function/class, dependencies stubbed, fast
- **Integration** — multiple modules together, real test DB, real I/O at module boundaries
- **Contract** — HTTP/gRPC handler invoked, real request/response shapes, internal deps stubbed
- **E2E** — full app running, browser or full request path, real services

If a case requires real Postgres to exercise it meaningfully (testing actual SQL behavior, transaction semantics, constraint failures), it's integration — don't pretend it's a unit test by mocking the entire query.

### Phase 7: Prioritize

Rank suggestions: **Must-have / Should-have / Nice-to-have**.

- **Must-have** — security boundaries, money handling, data deletion, the path that fails most often if the contract changes
- **Should-have** — main happy path of the feature, the most common error case
- **Nice-to-have** — edge cases that would be unusual in practice, defensive checks for "shouldn't happen" states

A user looking at the list should be able to say "I'll do the must-haves this week" without re-reading the rationale for each one. Aim for 3-7 must-haves max per target — if you have more, the priorities aren't sharp enough.

### Phase 8: Compose the output

Use `assets/suggestion-template.md`. Output structure:

1. **Header** — target file(s), framework detected, where new tests should live
2. **Already covered** — brief list of what existing tests handle (so the user knows you saw them)
3. **Suggestions** — numbered, grouped by must-have / should-have / nice-to-have
4. **Untestable as-written** — if anything in the target can't be unit-tested without refactoring (heavy module-level side effects, hardcoded singletons, no DI), call it out honestly. Don't suggest mocking-everything workarounds. See `references/untestable-code.md`.
5. **Next step** — one line: "I can generate code for any of these — say 'write case N' or 'write all must-haves'."

## Test type guidance

For deep dives, see:
- `references/case-design.md` — the rubric for designing good cases
- `references/test-types.md` — choosing unit vs integration vs contract vs E2E
- `references/untestable-code.md` — recognizing code that needs refactoring before testing
- `references/language-notes.md` — JS/TS, Python, PHP, Go, Ruby, Java, Rust conventions

## Sampling for large targets

If the target is over ~500 lines or has 20+ exports, don't try to suggest cases for everything. Instead:

1. Suggest cases for the 5-8 most-important exported behaviors (driven by risk, not by alphabetical order)
2. Tell the user explicitly: "I focused on the highest-leverage cases. Want me to expand to other functions?"
3. Don't pad the list with tautological cases just to hit a count

## Graceful degradation

If `inspect_target.sh` can't run (no shell, restricted env), do the inspection manually by reading the file. The output is the same; only the speed differs.

If you can't read the existing test files (permission, missing, etc.), note it in the output and suggest cases using the language's most common conventions, with a caveat: "Conventions assumed; verify against your existing tests before writing."

## When to redirect

The user wants code generation, not suggestions:
> "Just write the tests for me."

Reply: "I can suggest the cases first — that's what this skill does. After you review them, I can write the code for the ones you want as a follow-up task. Should I produce the suggestions, or skip straight to writing?"

The user wants assessment, not suggestions:
> "Are these tested?"

Reply: "Sounds like you want a coverage assessment first. The test-assessment skill finds gaps; this one suggests what to do about them. Want me to run an assessment, or do you have a specific target you want suggestions for?"

The user wants both ("assess and then suggest"):

Run test-assessment first, then offer suggestions for the top findings. Don't try to do both simultaneously — finish the assessment, present the report, then ask which findings to suggest cases for.
