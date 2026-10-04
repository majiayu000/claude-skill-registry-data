---
name: browser-use
description: Drive a real browser to QA a running app. Screenshots, clicks, forms, evidence. Use when there is no Playwright suite, or when a human flow must be walked.
---

# Browser use

## Trigger

Need to test a running web app by actually using it. No smoke suite, or the suite does not cover this flow.

Navigate, click, fill, screenshot, assert. Use the harness browser.

## How to drive the browser

Pick the door the runner actually has, in this order:

1. A first-party browser tool on this harness (Grok Bot browserUse, Grok Build browser, Claude computer use).
2. Headed Playwright against the given URL, if Playwright is already in the checkout.
3. Stop and say the harness has no browser.

Do not invent a headless stack. Do not scrape cookies out of a profile to skip login.

## Workflow

1. Resolve the target URL (dispatched, or local app for the repo). Confirm it is up before clicking.
2. Walk the flow as a user. One path. Screenshot each meaningful step.
3. Assert what the user would see: copy, state, error, navigation.
4. If login or 2FA is required, stop and hand that step to a human. Never ask for a password in chat. Never read `.env`.
5. Report. Repro, screenshots, what broke, what was fine.

## Guardrails

- Report only. Do not patch product code.
- Prefer a real click over injecting JS.
- Deterministic waits for visible state, not sleep.
- Stay on the dispatched flow. Do not wander the whole site.
- Never merge.

## Output

- Flow walked
- Screenshots of evidence
- Failures with repro steps
- Anything that could not be tested (auth wall, downed app)
