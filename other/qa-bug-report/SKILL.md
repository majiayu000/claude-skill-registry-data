---
name: qa-bug-report
version: 1.0.0
description: Write a bug report a developer can reproduce and fix without asking a single follow-up question.
author: matrixx0070
tags: [qa, bug-report, repro, severity, triage]
capabilities: []
---

## When to use

When you've found a defect and need to hand it off so it actually gets fixed. A good report is a reproduction recipe plus enough context to triage priority. The test of quality: could a developer who's never seen the feature reproduce it from your report alone?

**Not for:** logging a vague "it's broken" note to yourself, feature requests (that's a change, not a bug), or questions about intended behavior (ask first — an unconfirmed expectation is not a bug). If you can't reproduce it, say so explicitly rather than filing noise.

## Method

1. **Reproduce it yourself first.** Confirm the steps are deterministic. Decision point: if it's intermittent, capture frequency ("3 of 10 attempts") and any pattern — don't pretend it's reliable.
2. **Write a one-line title** that names the symptom + context: "Checkout: applying expired code still discounts total." Searchable, specific.
3. **List minimal numbered repro steps** — the fewest steps that trigger it, starting from a known state (URL, account, data). Strip anything not required.
4. **State expected vs. actual** as two separate lines. The gap between them IS the bug. Never merge them into prose.
5. **Attach evidence:** screenshot/video, console/network log, request ID, timestamp. Include build/version and environment.
6. **Assign severity by impact, not annoyance** — decision point: data loss / money / security / total blocker → Critical; major function broken with no workaround → High; degraded with workaround → Medium; cosmetic → Low. Keep severity (impact) separate from priority (business urgency).

## Example

```
Title: Cart: quantity field accepts negative values, produces negative total
Env: staging build 4.2.1, Chrome 141, account qa-user-7
Steps:
  1. Add any item to cart
  2. In quantity field, enter -3, press Update
Expected: input rejected, quantity stays >= 1
Actual: total becomes -$59.97; checkout button remains enabled
Severity: High (money path, no client-side guard)
Evidence: screenshot cart-neg.png, network POST /cart/update req-id 8f2a
```

## Pitfalls

- **Merging expected and actual** into one sentence — the reader can't tell what should happen.
- **Non-minimal steps** — 12 steps when 3 reproduce it; the noise hides the trigger.
- **Severity by emotion** — flagging a typo Critical, or burying data loss as Medium.
- **No environment/build** — "works on my machine" starts here; always pin version + env.

## Output format

```
Title: <area>: <symptom in one line>
Environment: <build/version, OS/browser, account/role>
Preconditions: <starting state, test data>
Steps to reproduce:
  1. ...
  2. ...
Expected result: <one line>
Actual result: <one line>
Severity: <Critical/High/Medium/Low> — <impact rationale>
Frequency: <always | N of M>
Evidence: <screenshot/log/request-id/timestamp>
```
