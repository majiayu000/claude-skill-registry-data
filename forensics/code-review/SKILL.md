---
name: code-review
description: Use when reviewing code you did not write in this task — a pull request, a teammate's branch, a diff, or another agent's output. Enforces risk-ordered reading, evidence-backed findings, and severity triage instead of a comment flood.
---

# Code Review

Goal: catch what matters, skip what doesn't, and never say "looks good"
about code you haven't actually read.

This is for reviewing OTHER work (a PR, a branch, another agent's output).
For checking your own work, use `verify-work`.

## Steps

1. **Understand the intent first.**
   What is this change supposed to do? Read the description/ticket/journal
   before the diff. A review without intent is just style-nitpicking.

2. **Read in risk order, not file order.**
   First: anything touching auth, money, data deletion, migrations, public
   APIs, concurrency. Then core logic. Then tests. Style last, if at all.
   Say which high-risk areas the diff touches — that's the review's spine.

3. **Hunt for the three killers:**
   - **Unintended behavior change** — does anything behave differently that
     the description doesn't mention?
   - **Weakened safety** — tests loosened/deleted, error handling removed,
     validation relaxed, exceptions swallowed?
   - **Hidden scope** — changes that have nothing to do with the stated
     intent, riding along unreviewed?

4. **Back every finding with evidence.**
   Point to the line, state the failure scenario ("if two requests hit this
   concurrently, X"). A finding you cannot ground in the code is a question,
   not a finding — ask it as one.

5. **Triage, don't flood.**
   Label each finding: **blocker** (breaks something / unsafe) /
   **should-fix** (real but not fatal) / **nit** (take or leave). Report the
   2-5 highest-impact spots first. Dozens of nits bury the one blocker —
   optimize for signal, not for looking thorough.

6. **Verify claims when stakes are high.**
   For a blocker-level suspicion, don't just assert — run the code or write
   a quick failing case if the environment allows. Evidence rules apply to
   reviews too.

7. **Conclude honestly.**
   End with one of: approve / approve-with-nits / needs-changes (list the
   blockers). "LGTM" on a diff you skimmed is a lie with good manners.

## Do not

- Do not review style before correctness.
- Do not demand rewrites to your personal taste — consistency with the
  existing codebase wins.
- Do not pass a diff you didn't fully read. If it's too big to review
  properly, say that — "split this" is a valid review outcome.
