---
name: bug-report-writer
description: Use when writing or improving a bug report, defect ticket or Jira/GitHub issue from notes, screenshots, logs, a video description or a failed test, so developers can reproduce and fix it quickly.
---

# Bug Report Writer

## Overview

A good bug report lets a developer reproduce the problem on the first try. State exactly what happened, what should have happened, and how to make it happen again, with only the evidence that matters.

## Method

1. **Collect facts** from what the user provides: steps, screenshots, console or server logs, failing test output, environment.
2. **Reduce the steps** to the shortest path that triggers the bug. Remove steps that do not matter.
3. **Separate observation from guesses.** Facts go in the report; suspected causes go in a clearly labelled Notes line.
4. **Find missing essentials** (environment, build version, account type, data used). Ask for them, or mark them `Unknown`.
5. **Set severity and priority** with the table below.
6. **Write** using the format. Keep the title searchable.

## Format

```
Title: <Area>: <what goes wrong> when <condition>
       e.g. "Checkout: total ignores coupon when quantity is changed"

Environment: <app/build version, URL, browser/OS or device, account role, feature flags>
Severity: <Blocker | Critical | Major | Minor | Trivial>   Priority: <P1-P4>

Steps to reproduce:
1. ...
2. ...

Expected result: <what should happen, with the rule or spec reference if known>
Actual result: <what happens, exact error text>
Reproducibility: <Always | Intermittent (3 of 10 tries) | Once>

Evidence: <screenshot or video name, log excerpt (only relevant lines), request/response, test name>
Test data: <account, IDs, input values>
Notes: <suspected cause, workaround, first build where seen> (optional)
```

## Severity guide

| Severity | Meaning |
|---|---|
| Blocker | Stops testing or a release; no workaround |
| Critical | Core flow broken, data loss, security or payment issue |
| Major | Feature works incorrectly; workaround exists |
| Minor | Cosmetic or rare edge case with little impact |
| Trivial | Typo or tiny visual issue |

## Common mistakes

- Titles like "Bug in app" or "Not working".
- Steps that start in the middle ("go to the form" — which form, which user?).
- Pasting 500 lines of logs instead of the relevant 10.
- Mixing two bugs in one report.
- Presenting a guessed cause as fact.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
