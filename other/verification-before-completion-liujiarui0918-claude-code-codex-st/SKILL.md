---
name: verification-before-completion
description: Use BEFORE claiming any task complete. "Looks right" is not verification.
---

# Verification Before Completion

The gap between "I wrote the code" and "the code works" is where 80% of bugs ship. Closing that gap is non-negotiable.

## Iron Law

**A task is not complete until you have executed the verification command, read the output, and confirmed it matches expectations.**

Compiling is not verification. Type-checking is not verification. "Looks right" is not verification.

## What counts as verified

You must be able to point to:
1. The **command** you ran (or interaction you performed).
2. The **output** you observed.
3. The **expectation** that output satisfied.

Missing any of those three? Not verified.

## Red Flags

- "It should work."
- "I don't think anything else changed."
- "The diff looks right."
- "Tests probably pass."
- "I'll let CI catch it."
- Saying "done" without naming the verification step you took.

If any of these appear in your reasoning, you are about to ship an unverified change.

## Verification by task type

### Code changes (functions, modules)
- Run the relevant unit test(s). Read the green/red output.
- If no test exists, write one OR run an integration that exercises the path.
- If neither is possible, run the function with a real input in a REPL / script.

### API endpoints
- Hit the endpoint with `Invoke-RestMethod` / `curl` / Postman.
- Read the actual response body and status code.
- Verify both happy path AND at least one error case.

### UI changes
- Open the page. See the change with your eyes (or screenshot).
- Click the thing. Watch it do the thing.
- Resize / different state — the easy regressions live here.

### CLI / scripts
- Execute the script with realistic args.
- Inspect stdout, stderr, exit code, and any files it produced.
- Run it a second time if it's supposed to be idempotent.

### Test additions
- Run the test on the **broken** code first — it must fail.
- Then run on the fixed code — it must pass.
- A test that has never seen red is not a test, it's an assertion that always passes.

### Configuration / infra
- Reload / restart the affected service.
- Confirm the new config is actually in effect (env var dump, debug endpoint, log line).
- Trigger the behavior the config controls.

## The "I can't run it" exception

Sometimes you genuinely cannot execute (no env, no creds, sandboxed). In that case:
- **Say so explicitly**: "I cannot verify; here is what I would run and what output I'd expect."
- Hand off with that note so the human or next agent runs it.
- Do NOT mark the task complete. Mark it "pending verification."

## MUST checklist before declaring done

- [ ] Verification command identified
- [ ] Command executed
- [ ] Output read end-to-end (not just "exit 0")
- [ ] Output matches the expected behavior
- [ ] Side effects checked (files written? state changed? logs clean?)
- [ ] No new warnings/errors I'm ignoring

If any box is unchecked, the task is not done.

## Cross-references

- [[systematic-debugging]] Phase 4 — the verification step in bug-fix flow.
- [[requesting-code-review]] — self-review is *additional* to verification, not a substitute.
- [[finishing-a-development-branch]] — verification is gate 1 before branch options.
