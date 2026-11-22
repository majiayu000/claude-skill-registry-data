---
name: visual-regression
description: Catch unintended visual changes by comparing screenshots against a baseline. Use after any change to a web UI, before calling it done, and whenever a change claims to be visual-only. Web UI only; needs a browser. Only invoke via the orcinus router.
license: MIT
user-invocable: false
---

# VISUAL-REGRESSION — did the look change, and was it supposed to?

Unit tests cannot see the page. A change that passes every test can still break the layout, hide a button, or change a colour. Visual regression testing catches that: capture what the page looked like before, capture it after, and compare the pixels. A difference the brief did not ask for is a finding, even if the tests pass.

## Rules

- Baseline first. Capture a baseline screenshot of each page and state before the change, in a fixed viewport, with animations disabled. Without a baseline there is nothing to compare against.
- Mask what moves. Dates, times, random IDs, and loading spinners change every run — mask them or the diff is noise.
- Compare pixels, not opinions. Record the percentage of differing pixels and save the diff image. A diff above the threshold is a finding.
- Review the diff image. Look at it yourself, or show it to the user. Do not auto-approve a diff, and never update the baseline to make a diff disappear without a human confirming the new look is intended.
- Never report "no visual change" without a comparison run.
- A check that did not run is never reported as passed.

## Steps, in order

### 1. Baseline

Serve the page (use the `webapp-testing` skill's `with_server.py` helper to manage the server). With Playwright, capture a screenshot of each page and state the change touches, at a fixed viewport (for example 1280x720), with animations disabled. Store baselines under `tests/visual/baseline/` and commit them. Record the viewport, the browser, and the Playwright version.

### 2. Change and re-capture

Make the change. Re-capture the same pages and states into `tests/visual/current/` (git-ignored). Do not overwrite the baseline.

### 3. Compare

Compare each current screenshot against its baseline, pixel by pixel. Record the percentage of differing pixels and save a diff image that highlights the changed areas. Use a threshold (for example, at most 0.1% differing pixels); anything above it is a finding.

### 4. Review and classify

Look at the diff image. Classify each difference as intended (asked for in the brief) or unintended. An unintended difference is a finding: fix the code, not the baseline.

### 5. Update the baseline only on confirmation

Update a baseline only after the user confirms in writing that the new look is intended. Record who confirmed it and when. Then re-run the comparison — it must show no diff above the threshold.

## Report

Return the report in this form:

- Pages and states captured, with viewport, browser, and Playwright version.
- For each page: baseline path, current path, diff percentage, diff image path.
- Classification of each difference (intended / unintended).
- Verdict: PASS (no diff above the threshold, or all diffs intended and confirmed) or FAIL (an unintended diff above the threshold).
- Baseline updates, with who confirmed each one and when.

## Scope

Web UI only. This skill needs a browser (Playwright + Chromium). It does not test logic, data, or API behaviour — that is what unit, E2E, and mutation testing are for.

## Sources

Method, in our own words, using Playwright (microsoft/playwright, Apache-2.0, licence verified from the primary LICENSE file) as-is. No code was copied from Playwright.
