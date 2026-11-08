---
name: mdcp-self-check
description: Run before saying a coding task is done, and when something fails. Self-check (build, types, tests, scanners), defense review (OWASP 2025 abuse cases), and a self-debug loop that stops after three failed attempts and reports. Use for "check your work", "is it safe", "debug this", "why does it fail".
---

# Self-check, defense and self-debug

## 1. Self-check (before "done")
Run what the project has and record each result as pass, fail or not run:
1. `npx tsc --noEmit`, lint, tests, `npm run build`
2. `npm audit --omit=dev`; `gitleaks detect` and `semgrep --config auto` if installed
3. `git diff`: no secrets, no unrelated edits, no leftover debug output
4. The requested behavior, exercised once (run it, call the route, open the page)

## 2. Defense review
For every new route, action or form, answer each with evidence from the code or a test:
- Who may call it, and is ownership of the object checked? (A01)
- Is input validated and output minimal? (A05, data leakage)
- What happens on timeout, bad input, missing record, two requests at once? (A10)
- Is it rate-limited, and is it logged without secrets? (A07, A09)
- Does it add a dependency, and has that dependency been reviewed? (A03)
Full list: `master-developer/references/security-check.md`, `web-analysis-shield.md`, `exploit-sandbox.md`. Test only your own code.

## 3. Self-debug
1. Reproduce with a failing test or exact steps. Read the whole error.
2. Form one hypothesis, find the root cause, grep every caller before touching shared code.
3. Fix once, in the shared place. Re-run the failing test, then the suite and build.
4. A fix that does not work gets reverted, then try a different approach. After three failed attempts, stop and report: error, what was tried, what was learned, suggested next step.
5. Add a regression test.

## 4. Report
End with: what changed, results of section 1 (including "not run"), open risks, shortcuts taken. Never write "100% secure" or "no bugs".
