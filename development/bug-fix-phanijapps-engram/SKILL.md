---
name: bug-fix
description: Use this skill when the user wants to fix a bug -- a deviation between current behavior and intended behavior in code that already exists. Triggers on "fix bug", "fix this bug", "diagnose and fix", "investigate this regression", "this is broken". Do NOT use for new features (use `new-spec`) or for refactors that don't fix incorrect behavior.
---

# Skill: bug-fix

Fix a defect in the smallest, most root-causing way. The discipline is
universal: reproduce before fixing, write the failing test first,
falsify rival hypotheses before asserting a cause, identify root vs
symptom, close the coverage gap that let it through, minimum diff,
commit body documents why.

## When to invoke

Even a one-line fix benefits from walking this discipline; it forces
the question "is this fixing the cause or hiding it?"

For multi-file changes that go beyond fixing one defect — refactors,
new features triggered by discovering the bug — stop and use
`new-spec` instead. This skill is for bug fixes, not opportunistic
restructuring.

## Procedure

1. **Reproduce first.** Don't write a fix until you have one of: a
   failing test, documented manual reproduction steps that fail
   reliably, or a captured error / stack trace / log signature. No
   reproduction = no fix; you might be fixing the wrong thing.

2. **Write the failing test (red).** It should pin the *observable
   contract being violated*, not the current implementation. Push
   back on these failure modes:
   - **Mock-shape assertion.** `expect(mock).toHaveBeenCalledWith(...)`
     when the observable contract is a returned value or state
     change. Test the contract, not the implementation. (See
     `quality-engineer`'s "mock-shape assertions" check.)
   - **Test passes for the wrong reason.** Run the test against the
     unfixed code; confirm it fails *because of* the bug, not
     because the setup is wrong.

3. **List candidate causes, then falsify each.** Before asserting a
   root cause, name 2-3 plausible causes — not just the first one
   that comes to mind. For each, write Expected / Actual / Verdict:
   what you'd observe *if* that cause were true, what a probe (a log,
   a breakpoint, a one-off experiment) actually shows, and whether
   that rules the cause in or out. For example:
   - *Cause A: input arrives unsorted.* Expected: log shows
     out-of-order keys. Actual: keys are sorted. **Verdict: ruled
     out.**
   - *Cause B: cache returns a stale entry.* Expected: second call
     skips the loader. Actual: loader never runs on the repro.
     **Verdict: ruled in.**

   Fixating on the first plausible cause is how you fix the wrong
   thing; making yourself name rivals and kill them with evidence
   keeps you honest. One survivor that the evidence supports becomes
   the root cause you assert in step 4.

4. **Identify root cause before writing the fix.** Write down a
   one-line answer to each:
   - **Where is the defect actually?** In the called function, the
     caller, their shared assumption, or upstream of both? A null
     that crashes in `parse()` may originate in the loader that
     should never have produced null.
   - **When did it start?** `git log` and `git blame` on the
     affected code. For regression-shaped bugs the commit that
     broke it often tells you why; even for non-regressions, the
     commit messages surrounding the affected lines surface the
     original intent and context.
   - **Could the same class of bug exist elsewhere?** Grep for
     similar patterns — same function called from other sites, same
     assumption made elsewhere. If yes, decide whether the fix's
     scope widens or whether you file follow-up tickets and add an
     explicit non-goal ("fix here only").
   - **Why wasn't it caught?** Which test, assertion, or guard
     should have caught this and didn't — or never existed? Name the
     specific coverage gap (an untested branch, a contract no test
     pinned, an input class no fixture covered). The regression test
     in step 7 closes *that* gap, not just the one input you observed.

5. **Minimum fix.** Write the smallest change that turns the failing
   test green. Refuse to fix adjacent issues in the same PR; note
   them for follow-up. (Echoes `adversarial-reviewer`'s scope check
   — out-of-scope changes are a Blocker until justified or extracted.)

6. **Verify root vs symptom.** Look at the diff and ask: does this
   address what step 4 identified, or does it mask the symptom?
   Common symptom-only anti-patterns to refuse:
   - **Catch-all exception handlers** that swallow the bug instead
     of making the failing call not throw.
   - **Defensive checks at every call site** when the invariant
     should hold upstream. Twelve `if (x == null) return` callers
     of a function that should never return null is masking, not
     fixing.
   - **Retries around flaky code** when the right fix is to make
     the code deterministic.
   - **Feature flags that disable the broken path** instead of
     fixing it. Flags are for staged rollout, not for hiding bugs.

   If the failing test from step 2 still passes under a symptom-only
   fix, you wrote the wrong test — go back to step 2 and sharpen it.

7. **Regression test stays.** The failing test from step 2 is the
   regression test. It lives in the suite; it must pin the real
   invariant so it catches this bug if it recurs — and it should
   close the coverage gap named in step 4, pinning the invariant
   that was missing rather than only the one input you observed.
   Don't delete it after the fix lands.

8. **Commit body documents the root cause.** Conventional commit
   subject (`fix(<scope>): <subject>`) plus a body explaining what
   was wrong (the observable bug), why it was wrong (the root cause
   from step 4), and why the fix takes the shape it does. The diff
   shows *what*; the commit body shows *why*. Future readers care
   more about the latter.

9. **Loop back to the tracker (if any).** Comment the PR URL on the
   ticket and apply the next transition. The mechanism is
   adopter-specific (Jira MCP, Linear CLI, `gh issue comment`, etc.);
   the obligation — keeping the ticket synced — is universal.

## Anti-patterns to refuse

- **Fixing forward without a reproduction.** The obvious fix is
  wrong about a third of the time, and you can't tell which third
  until the test fails red first.
- **Fixing the bug plus adjacent cleanup in one PR.** Each cleanup
  is its own PR with its own justification. Bug-fix PRs are for
  fixing bugs.
- **Adjusting the spec or the test to match the buggy behavior.**
  If the spec and the fix disagree, one of them is wrong — surface
  that explicitly before continuing, don't paper over it.
- **Closing as "not reproducible"** without trying hard enough.
  Document what was tried, on what version, with what data, before
  giving up. "Couldn't reproduce on my machine" is a hypothesis
  worth testing, not a closing condition.
