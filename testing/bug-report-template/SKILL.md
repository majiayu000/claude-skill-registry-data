---
name: bug-report-template
description: "Builds a well-formed bug (defect) report from raw observation notes - fills in summary, environment, steps to reproduce, expected vs actual, and severity rationale - and validates that each field has the load-bearing content reviewers and engineers need to triage. Also converts a single test-failure record (JUnit XML, Allure JSON, pytest log, Playwright report) into a classified, ready-to-file bug spec, and provides the adversarial review checklist that gates a report before it enters the tracker (required fields, single-description title test, severity-priority independence, reproduction quality). Use when a stakeholder reports a problem informally, when a CI failure artefact needs to become a triageable report, or when a drafted report needs a pre-filing quality audit."
---

# bug-report-template

## Overview

A well-formed bug report is the input contract for triage, repro, and
fix. Industry consensus from Mozilla's long-standing bug-writing
guide ([mozilla-bug-writing][moz]) and the ISO/IEC/IEEE 29119-3:2021
incident-report format converges on the same eight fields:

[moz]: https://bugzilla.mozilla.org/page.cgi?id=bug-writing.html

| Field             | Purpose                                                      |
|-------------------|--------------------------------------------------------------|
| **Summary**       | Triage line - describes the problem, not the cause.         |
| **Environment**   | OS, build, browser/runtime version, locale, device.         |
| **Steps to Reproduce** | Numbered, deterministic, copy-pasteable.              |
| **Expected**      | What should have happened.                                  |
| **Actual**        | What did happen (verbatim error message if any).            |
| **Severity**      | Impact on users (intrinsic to the bug).                     |
| **Priority**      | Order of fix relative to other bugs (extrinsic, business).  |
| **Reproducibility** | Always / Sometimes / Once / Unable.                       |

> **Terminology note:** ISTQB distinguishes **error** (human action),
> **defect / fault / bug** (imperfection in a work product), and
> **failure** (deviation from delivered service). This skill uses
> "bug" and "defect" interchangeably with "fault" reserved for the
> code-level imperfection. Reports describe **failures** and the
> reporter's hypothesis about the underlying **defect**.

The skill is a workflow that takes raw input (a chat message, a voice
memo transcription, a copy-pasted error) and produces a filled
template - refusing to leave any required field blank.

## When to use

- A stakeholder describes a problem informally and wants it tracked.
- The team is migrating triage to a structured tracker (Linear,
  Jira, GitHub Issues) and needs a per-template template.
- A support ticket lacks the structure engineering needs.
- You're preparing a postmortem for an incident-tier bug and need a
  clean baseline report to anchor the timeline.

If the team already has a working bug template in their tracker, this
skill is **not** for replacing it - it's for **filling** it correctly.
Adapt the field set below to the team's existing template.

## How to use

1. Extract verbatim errors, the UI surface, environment details, and the
   reporter's expected-vs-actual from the raw input (Step 1); flag any gap
   instead of fabricating.
2. Draft a Summary under 60 chars that names the surface and the observable
   behavior, not the fix (Step 2).
3. Write numbered, deterministic, self-contained Steps to Reproduce, quantifying
   the rate for intermittent bugs (Step 3).
4. State Expected and Actual separately, pasting the verbatim error or a
   screenshot for Actual (Step 4).
5. Score Severity and Priority independently, then Reproducibility (Steps 5-6).
6. Assemble the fields into the Output format template, leaving `[GAP]` markers
   on any field the reporter did not supply.

## Step 1 - Extract raw evidence

From the input (chat message, error log, screenshot caption, voice
memo), extract:

- **Verbatim error messages** (with quotation marks).
- **The exact UI surface** (URL or screen name) where the issue was
  observed.
- **Any environmental details** the reporter mentioned (OS, browser,
  app version).
- **What the reporter expected** vs. **what they observed** - 
  separately. Often the reporter conflates these; tease them apart.

If any of these is missing, **flag the gap** rather than fabricating;
the gap is a triage signal in itself.

## Step 2 - Draft the Summary

Per Mozilla's guidance, summaries should be **under 60 characters**
and describe the **problem, not the solution** ([mozilla-bug-writing][moz]).

| Anti-pattern                                       | Better                                              |
|----------------------------------------------------|-----------------------------------------------------|
| `Need to add cookies banner`                       | `Cookie consent banner missing on /pricing`         |
| `Fix the login form`                               | `Login form rejects valid email with apostrophe`    |
| `Bug in checkout`                                  | `Checkout returns 500 when shipping address is empty` |

A good summary names the **surface** (URL/screen) and the **observable
behavior** (what's wrong).

## Step 3 - Build the Steps to Reproduce

Per [mozilla-bug-writing][moz], reproduction steps must be:

- **Numbered** in execution order.
- **Specific** - exact buttons, exact URLs, exact input values.
- **Deterministic** - no "around step 5 it sometimes...".
- **Self-contained** - start from a known state (logged out, fresh
  browser session).

Example contrasting good vs. bad:

```
Bad:
1. Go to the site and try to check out.

Good:
1. Open https://example.com/ in Firefox 128 (private window).
2. Click "Add to cart" on the first product card.
3. Click the cart icon (top right).
4. Click "Checkout".
5. Leave the shipping address fields empty.
6. Click "Place order".
```

If the bug is **intermittent**, document the reproduction rate ("8 out
of 20 attempts on macOS Sonoma 14.4 / Firefox 128") - quantify the
rate, don't guess.

## Step 4 - Separate Expected from Actual

Mozilla's example pattern ([mozilla-bug-writing][moz]):

```
Expected: My Inbox displays correctly.
Actual:   The page shows "Your browser does not support cookies
          (error -91)".
```

Reject blurry phrasings like "it doesn't work" or "page displays
incorrectly" - they push the cost of investigation onto the engineer
instead of the reporter.

For UI bugs, attach a screenshot as the **Actual** body. For backend
bugs, paste the exact error message + status code. If a stack trace
is available, capture it verbatim as input for hypothesis extraction.

## Step 5 - Pick Severity (intrinsic) and Priority (extrinsic)

Score two independent fields: **Severity** (what the defect does to the user
when it manifests) and **Priority** (when the team plans to fix it relative to
other work). They are not the same axis - a Critical-severity bug for a
non-paying user can be P2, and a Minor-severity bug on the marketing homepage
can be P0 the day before launch. Score severity from impact; let the PM /
engineering decide priority from business context.

Use the classification scales in
[references/severity-and-priority-scales.md](references/severity-and-priority-scales.md).

## Step 6 - Score Reproducibility

Per [mozilla-bug-writing][moz]:

- **Always** - every attempt reproduces.
- **Sometimes** - quantify the rate (`12/20`, `~30%`).
- **Once** - observed once; cannot reproduce despite trying.
- **Unable** - reporter could not reproduce after the initial sighting.

A `Once` or `Unable` bug is **not** a candidate for fix-then-close - 
it's a candidate for adding monitoring or extending the test suite to
catch it next time.

## Output format

```markdown
## <Summary, <60 chars, problem-not-solution>

**Severity:** Critical | Major | Moderate | Minor
**Priority:** P0 | P1 | P2 | P3
**Reproducibility:** Always | Sometimes (X/Y) | Once | Unable

### Environment

- **App / Build:** <name + version + commit SHA if known>
- **OS:** <macOS 14.4 / Windows 11 23H2 / Ubuntu 24.04 / iOS 18.0>
- **Browser / Runtime:** <Firefox 128 / Chrome 130 / Node 22.5.0 / Python 3.12>
- **Locale / Timezone:** <en-US / UTC+0> (only when relevant)
- **Device / Viewport:** <iPhone 13 / 1280x800 desktop> (only when relevant)

### Steps to reproduce

1. <step>
2. <step>
3. ...

### Expected

<one sentence - what should have happened>

### Actual

<verbatim error / observed behavior; attach screenshot or log>

### Notes

<optional: any context the reporter mentioned that doesn't fit elsewhere - recent changes, why they were doing this, what they tried>
```

## Worked example - from a Slack message

Input:

> "hey, the checkout flow is broken on mobile - i hit the place order button and nothing happens. tried twice. firefox on my phone."

The skill identifies missing fields and produces a draft with **gap
flags** for the missing data:

```markdown
## Place order button does nothing on mobile checkout

**Severity:** Major (feature unusable; needs reporter confirmation)
**Priority:** P1 (until severity is confirmed)
**Reproducibility:** Sometimes (2 attempts confirmed by reporter)

### Environment

- **App / Build:** [GAP - confirm the build / version]
- **OS:** [GAP - "my phone" - confirm iOS or Android + version]
- **Browser:** Firefox (mobile)
- **Locale / Timezone:** [GAP - only if business-logic-relevant]
- **Device:** [GAP - confirm phone model]

### Steps to reproduce

1. [GAP - confirm starting URL or screen]
2. Add a product to the cart.
3. Navigate to checkout.
4. Tap "Place order".
5. Observe: nothing happens.

### Expected

Tapping "Place order" submits the order and navigates to the
confirmation screen.

### Actual

Tapping "Place order" produces no visible response (no nav, no error,
no spinner).

### Notes

Reporter tried twice. Returning to reporter for the gaps before triage.
```

The `[GAP]` markers force the reporter to fill them in, rather than
the engineer triaging on incomplete data.

**Variant - from a stack-trace dump.** Given an automated alert with the full
production stack trace, the skill drafts the report with **Steps to Reproduce**
marked `Unable - production crash (no manual repro yet)` and the **Actual**
field populated with the verbatim trace, flagged for hypothesis extraction.

## From a CI failure record

A test failure produces structured data (XML, JSON, HTML) with everything a
triager needs - assertion, stack, test name, environment. This workflow
ingests that record and emits a ready-to-file bug spec instead of starting
from prose.

### F1 - Ingest the failure record

Inputs are auto-detected by extension:

| Format | Source | Schema reference |
|---|---|---|
| JUnit XML | pytest, JUnit, surefire, Playwright | `<testsuites>/<testsuite>/<testcase>/<failure>` per the de-facto schema (Apache Ant) at [llg.cubic.org/docs/junit/](https://llg.cubic.org/docs/junit/) |
| Allure JSON | Allure framework (any language) | per-test JSON in `allure-results/`; schema at [docs.qameta.io/allure-report](https://docs.qameta.io/allure-report/) |
| pytest `--tb=short` log | pytest stdout/stderr | line-oriented; regex-driven |
| Playwright HTML report | Playwright trace | `report.json` inside the HTML bundle |
| TestNG XML | TestNG | similar to JUnit; per [testng.org](https://testng.org/) |

Parser bodies and per-format field shapes live in
[references/parsers.md](references/parsers.md). `parse_junit(path)` returns
one dict per failing testcase; Allure's first-class `severity` / `feature` /
`suite` labels are harvested when present.

### F2 - Extract classification fields

For each failure, propose values for the bug report:

| Field | Source | Default if unknown |
|---|---|---|
| Title | First line of `failure.message` truncated to 100 chars | "Test failure: {test_name}" |
| Body | Markdown with test name, stack, env, links | (always present) |
| Severity | Allure `severity` label OR inferred from assertion class (`AssertionError` → Medium; `TimeoutError` → High; `ConnectionError` → High) | Medium |
| Priority | Match severity by default; production-runner = bump | Medium |
| Defect type (IEEE 1044) | Inferred from stack location: tests/* → Test specification; app/* → Code (implementation) | Code |
| Component | Allure `feature` / `suite` label OR top-of-stack module | (none) |

Severity inference rules (heuristic, reviewer confirms):

```python
SEVERITY_FROM_ERROR = {
    "AssertionError":   "medium",
    "TimeoutError":     "high",
    "ConnectionError":  "high",
    "OutOfMemoryError": "critical",
    "SecurityException": "critical",
}

def infer_severity(failure_type, message):
    if failure_type in SEVERITY_FROM_ERROR:
        return SEVERITY_FROM_ERROR[failure_type]
    if "production" in message.lower() or "p0" in message.lower():
        return "high"
    return "medium"
```

Inference is heuristic - severity / type from exception class is
approximate, and root cause (ISTQB CTAL-TA) requires human investigation:
leave that field blank for the triager, and always label classification
fields "proposed - triager confirms".

### F3 - Render, dedupe, file

`render_body(failure, env)` emits a standard Markdown block consumed
verbatim by every tracker - test name, assertion, stack, environment,
artefact links, a proposed-classification table, reproduction (commit +
command), and dupe history. Full template:
[references/spec-template.md](references/spec-template.md).

Before filing, **search the tracker for open bugs with a matching title /
test name** - if duplicates exist, attach a comment instead of creating a
new bug. Then emit the tracker-agnostic spec and hand it to the
`bug-tracker-workflow` skill (qa-defect-management) to file on Jira,
Linear, GitHub Issues, or Azure DevOps:

```yaml
bug_spec:
  title: "Test failure: checkout fails with promo X"
  body: |
    ## Test failure
    ...
  severity: high
  priority: p2
  labels: [bug, type:regression, component:checkout]
  defect_type: Code
  component: checkout
  reproduction:
    commit: "abc123"
    command: "pytest tests/checkout/test_promo.py::test_stacked"
    environment:
      branch: main
      ci_run: "https://github.com/.../runs/123"
```

After filing: capture the new bug's URL, append a comment to the CI run
linking the bug, and update a per-test "known failure" register so
subsequent runs can correlate.

Caveats: JUnit XML is an informal Ant convention and some runners emit
non-standard variants - parse gracefully; tests that crash before the
runner catches them (segfault) produce no JUnit output - pair with CI
step-failure detection; each tracker has its own search semantics, so
dedup false negatives are possible.

## Review checklist

Before any report - hand-written or auto-filed - enters the tracker, audit
it. Auto-filed bugs need the audit *especially*. Output: per-finding
pass/fail plus a single verdict (`pass`, `block`, `pass-with-caveats`).

1. **Required fields.** Title, severity, priority, initial lifecycle state
   (`New`), reproduction steps (commit + command + observation),
   environment. Proposed fields: defect type (IEEE 1044), root-cause
   hypothesis, component. Any missing required field = BLOCK. `TBD` in a
   required field = blank = BLOCK.
2. **Title quality (single-description test).** Distinguishable (not
   "checkout broken"), behavioural (states what fails, not "fix this"),
   concrete verbs, single-clause (no "and" joining two failures). Failures
   = BLOCK + coach with a suggested rewrite.
3. **Severity-priority consistency.** Both populated independently.
   Critical severity + Low priority (or Trivial + Immediate) demands
   justification - rare but legitimate. Severity always equal to priority =
   flag as suspicious (likely auto-equated). Scales in
   [references/severity-and-priority-scales.md](references/severity-and-priority-scales.md);
   deeper classification rules in `severity-vs-priority-reference`
   (qa-defect-management).
4. **Reproduction quality.** Must include a commit SHA (not "Production" -
   that isn't a commit), a runnable command, a one-line observation, and
   expected vs actual. Missing any = BLOCK.
5. **Classification sanity.** If the from-CI-failure workflow proposed
   classification fields: defect type matches stack location; severity
   proposal consistent with assertion class (AssertionError → Critical
   without justification is suspect); component matches the code path.
   Treat Allure severity tags as advisory, not authoritative.
   Inconsistencies = caveat, shown but flagged.

Never auto-fill missing fields during review - only flag and recommend;
never mark "pass" with a missing required field or a repro without a
pinned commit. Severity / priority calibration stays judgmental - the
triager arbitrates disagreements.

## Anti-patterns

| Anti-pattern                                                | Why it fails                                                | Fix |
|-------------------------------------------------------------|-------------------------------------------------------------|-----|
| Filing without environment fields                           | Engineer cannot reproduce; bug bounces back to reporter.    | Force the GAP markers in the template; refuse to file without them. |
| Combining multiple unrelated symptoms in one bug            | Triage rate-limits - one of the symptoms gets fixed, the bug closes, and the others get lost. | Split into separate bugs; cross-link if related. |
| Severity = Priority shorthand ("Critical = P0")              | Confuses intrinsic impact with business prioritization.    | Score them independently; let the PM/engineering decide priority. |
| `Always` reproducibility on first observation               | The reporter may have triggered a one-off race condition.   | Verify "Always" with at least 5 deterministic repros before claiming it. |
| Hand-copying an assertion into the bug instead of parsing the artefact | Stack truncation, escaping errors.                        | Always parse the structured failure record (section F1). |
| One bug per test failure with no deduplication              | Tracker fills with the same flake filed N times.            | Always search for an open match before filing (section F3). |

## References

- [references/severity-and-priority-scales.md](references/severity-and-priority-scales.md) -
  the Severity and Priority classification scales used in Step 5.
- [mozilla-bug-writing][moz] - Mozilla's bug-writing guide;
  practitioner-emergent canonical for summary / steps / expected /
  actual structure.
- ISO/IEC/IEEE 29119-3:2021 - incident-report content (cite by
  stable standard ID; spec is paywalled at iso.org).
