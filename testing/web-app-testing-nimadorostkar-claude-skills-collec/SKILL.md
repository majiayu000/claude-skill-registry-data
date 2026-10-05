---
name: web-app-testing
description: Use when testing a web application interactively — verifying a feature, reproducing a bug, or checking a flow in a real browser. Covers systematic exploration, console and network inspection, and reporting what you find.
metadata:
  category: testing
  version: 1.0.0
  tags: [testing, browser, manual-testing, debugging, qa]
---

# Web Application Testing

## Purpose

Verify a web application by driving it, systematically. Automated tests confirm what someone thought to check; interactive testing finds what nobody thought of, which is where the interesting bugs are.

## When to Use

- Verifying a feature works before shipping.
- Reproducing a reported bug.
- Exploring a flow for defects that automated tests would not catch.
- Checking a fix in a real browser.

## Capabilities

- Systematic exploration of a feature's state space.
- Console and network inspection during the flow.
- Boundary and error-path probing.
- Cross-viewport and cross-browser checks.
- Clear, reproducible defect reports.

## Inputs

- The feature or flow, and what it is meant to do.
- The environment and any test credentials.
- The bug report, if reproducing.

## Outputs

- A verdict: works, or a list of defects.
- For each defect: steps, expected, actual, evidence (screenshot, console error, failing request).
- Notes on what was checked, so gaps are visible.

## Workflow

1. **Walk the happy path first** — Confirm the feature does what it claims for a normal user with normal data. If this fails, stop; there is nothing else to test yet.
2. **Open the console and the network tab before you start** — A 500 that the UI silently swallows, or a console error on every keystroke, is invisible if you are only looking at the page.
3. **Probe the boundaries** — Empty input, maximum length, special characters, a name with an apostrophe, a quantity of zero, a quantity of -1. The interesting bugs live here.
4. **Break the network** — Throttle it, then take it offline mid-request. What does the user see? A spinner forever is a defect.
5. **Test the back button and refresh** — Mid-flow. Multi-step forms and payment flows break here constantly.
6. **Check the second viewport** — At least one mobile width. Layouts break at breakpoints, and nobody looks.

## Best Practices

- The console is the cheapest bug detector available and the least used. An error there during a flow that "works" is a defect that has not surfaced yet.
- Test what happens when the user does the reasonable-but-unexpected thing: double-clicking submit, opening two tabs, pressing back after paying.
- A defect report without steps to reproduce is a complaint. Include the exact input, the exact URL, and the exact browser.
- Check the network tab for requests that should not be there: an API called four times on one page load, a request firing on every keystroke without debouncing.
- Verify against the requirement, not against your assumption about the requirement. Read what it was supposed to do.
- Note what you did *not* test. An untested area that is assumed tested is worse than a known gap.

## Examples

**A systematic pass over one feature:**

```text
Feature: refund an order (admin)

Happy path
  [PASS] Full refund on a paid order succeeds; the order shows "Refunded".
  [PASS] Partial refund reduces the balance and shows the remaining amount.

Boundaries
  [PASS] Refund of 0 is rejected with a clear message.
  [FAIL] Refund exceeding the order total is accepted by the UI. The API
         returns 422, but the UI shows a success toast and the row does not
         update. The user believes the refund succeeded.
         Steps: order ord_01HX (total $42) -> Refund -> enter 500 -> Submit.
         Expected: an inline error stating the maximum refundable amount.
         Actual: green "Refund issued" toast; no state change.
         Console: POST /refunds 422 (Unprocessable Content) — error swallowed
         in the .catch() at RefundModal.tsx:88.

Error paths
  [FAIL] With the network offline, Submit spins indefinitely. No timeout, no
         error state. The user cannot tell whether the money moved.

Interaction
  [FAIL] Double-clicking Submit issues two POSTs. The second returns 409
         (idempotency held), so no double refund occurs — but the UI shows
         an unexplained error on the second response. The button is not
         disabled during the request.

Not tested
  - Multi-currency orders (no test data available in this environment).
  - Refunds on orders older than 90 days (gateway restriction; needs a stub).
```

Three real defects, none of which an automated test suite was checking for, and all found in under fifteen minutes by being systematic rather than clever.

## Notes

- The "success toast on a failed request" bug is extremely common and is invisible to anyone not watching the network tab. It is the strongest argument for having devtools open the entire time.
- A submit button that is not disabled during its request will be double-clicked by a real user, and the idempotency key is what saves you. Verify both the button and the key.
- When you find a defect worth keeping, write the automated test for it. Interactive testing finds bugs; automation stops them coming back.
