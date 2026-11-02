---
name: write-tests
description: Write or improve automated tests that can catch real defects in any language. Use this whenever you add or change tests, including unit, API, integration and browser tests, whenever a feature or bug fix needs test coverage, or whenever someone asks you to raise coverage. It prevents tests that pass without checking anything.
---

# Write tests

A test is only useful if it fails when the code is wrong. Tests that repeat the
implementation or mock everything raise the coverage number and catch nothing.

## When to use

Any time you add or change a test. To find what is missing in an existing suite,
start with `audit-test-suite`.

## Steps

1. **Read the code and a neighbouring test.** Use the project's framework, helpers
   and naming. Do not add a test framework or a mocking library unprompted.

2. **List what could go wrong.** Before you write code, go through this list and
   keep every item that applies:

   - Caller has no credentials, or belongs to someone else
   - Input is empty, wrong type, at the limit, or one past the limit
   - Item is missing, or already exists
   - Dependency times out, errors or returns bad data
   - The same request arrives twice, or two arrive at once
   - Time boundary: exactly at the limit, and one unit either side
   - State is wrong for this action, such as cancelling something finished
   - A secret or private field could appear in output
   - Existing users or existing data could change

3. **Choose the level.** Use the highest level that stays fast and repeatable.

   | Behaviour | Level |
   | --- | --- |
   | Pure rule: dates, parsing, limits | Unit test with a table of inputs |
   | API, permissions, persistence | Real handler, real schema, test database |
   | Third-party service | Real client code, stubbed at the network |
   | Multi-step business flow | One ordered scenario through real entry points |
   | UI behaviour | Browser test against a local app |
   | Files, processes, OS behaviour | Real OS, on each platform you ship |

4. **Keep your own code real.** Fake only what you do not control: third-party
   APIs, the clock and platform services. Never mock the function under test or
   your own modules. Import the real code, never a copy.

5. **Make fakes strict.** An unexpected call must fail the test. A fake that
   answers anything can hide a wrong URL or an unwanted write. It must also keep
   the behaviour your code relies on, such as transactions and foreign keys.

6. **Write the test.** Each case sets up its data, does one action, then checks
   the result. See the example for your language in the next section.

7. **Assert the outcome, not only the response.**

   - Compare exact values.
   - Read back stored state after a write.
   - After a denied or failed call, confirm that nothing changed.
   - Count side effects: one email, one charge, zero model calls.
   - Plant a canary secret, then search the output for it.

8. **Prove that the test can fail.** Break the code on purpose, such as by removing
   the check. Run the test and confirm that it fails **with the expected message**.
   Restore the code and confirm that it passes. If it still passes while the code
   is broken, the test is worthless, so fix it.

9. **Confirm it runs in CI.** Find the script or job that executes this file. New
   files outside the configured pattern are silently never run.

10. **Finish.** Follow `verify-and-report`.

## Examples

Open only your language. Each folder has a small API and a complete test, covering
permissions, limits, audit records, secrets, replays and concurrency.

| Language | Guide | Test file |
| --- | --- | --- |
| JavaScript, TypeScript | `references/javascript.md` | `examples/javascript/app-test.mjs` |
| Python | `references/python.md` | `examples/python/test_app.py` |
| Go | `references/go.md` | `examples/go/app_test.go` |

For another language, read the closest example and translate it to the project's
test framework.

## Permission matrix

For each protected operation:

| Caller | Expected | Also check |
| --- | --- | --- |
| No credentials, or forged ones | 401 | Nothing changed |
| Valid user, someone else's resource | 404 | Nothing changed, same body as missing |
| Member without the required role | 403 | Nothing changed |
| Owner | 2xx | Stored value is correct |

Use 404 when the caller should not learn that the item exists. Follow the project's
convention if it differs. Run the matrix over a list of endpoints, so that a new
endpoint is one new row.

## Timing rules

- Pass the clock in, and use fixed timestamps for date rules.
- Do not use a sleep to wait for work to finish. Wait for a condition.
- A deadline only guards against a hang, so make it generous.

## Stop and ask when

- The code cannot be tested without a large redesign.
- A correct test fails and the expected behaviour is unclear.
- Testing would need real credentials or a production system.

## Common mistakes

| Tempting move | Why it fails | Do this instead |
| --- | --- | --- |
| `assert result is not None` | Passes on almost anything | Assert the exact value |
| Mock the database and repository | Proves only the mock | Use a real test database |
| Copy the implementation's logic into the test | Same bug on both sides | Use known literal values |
| Change the expected value to pass | Hides the defect | Find out why it differs |
| Check only the response | Misses storage bugs | Read back the stored state |
| Test only success | Misses most real incidents | Use the list in step 2 |
| Assert on source code text | Breaks on a move, misses behaviour | Run the behaviour |
| Snapshot a huge output | Reviewers approve noise | Assert the fields that matter |

## Checklist

- [ ] It failed for the right reason when the code was broken.
- [ ] It runs real code through a real entry point.
- [ ] Unexpected external calls fail the test.
- [ ] Denied calls are covered, and they changed nothing.
- [ ] Limits are tested on both sides.
- [ ] Side effects are counted.
- [ ] It does not depend on timing, order or leftover state.
- [ ] CI runs it.

## Report

```markdown
Tests added: <file: what each case proves>
Failure proof: <what you broke, and the failure message>
Runs in CI through: <script or job>
Not covered: <known gaps>
```
