---
name: "Core Browser Automation"
description: "General-purpose patterns for reliable browser automation (selectors, waiting, scrolling, overlays, HITL)."
tools:
  - playwright
---

## Selector Strategy (Stability First)
- **Priority 1**: `data-testid`, `data-test`, `data-cy`, `id` (if stable).
- **Priority 2**: Accessible roles with names (e.g., `getByRole('button', { name: 'Submit' })`).
- **Priority 3**: Text content (e.g., `getByText('Submit')`) - use with caution if text is dynamic.
- **Avoid**: Brittle CSS selectors (e.g., `div > div:nth-child(3)`), XPath, or selectors tied to visual layout.

## Waiting Strategy (No Flaky Sleeps)
- **Explicit Waits**: Wait for elements to be **attached**, **visible**, and **enabled** before interacting.
- **State Changes**: Wait for clear UI signals (spinners disappearing, success messages appearing).
- **Bounded Polling**: If no clear signal exists, use a loop with a short sleep (1-2s) and a max retry count.
- **Avoid**: Long blind sleeps (e.g., `sleep(5000)`).

## Scroll Strategy
- **Window vs. Container**: Determine if the scrollbar belongs to the `window` or a specific container element.
- **Incremental Scan**: Scroll in small chunks (e.g., half viewport) to trigger lazy-loading or reveal elements.
- **Check after Scroll**: Re-evaluate the page state after scrolling (elements might become visible).

## Handling Overlays & Modals
- **Detection**: Watch for common overlay selectors (dialogs, cookie banners, "interstitial" layers).
- **Dismissal**: Look for "Close", "X", "Accept", "Reject", "No thanks" buttons.
- **Click Intercepted**: If a click fails due to an overlay, find the overlay, dismiss it, and retry the click.

## Frames & Iframes
- **Detection**: If an element is not found, check if it resides within an `iframe`.
- **Switching**: Switch context to the iframe before querying elements inside it.

## Human-in-the-Loop (HITL) Policy
- **Auth**: Stop for Login/SSO/MFA/CAPTCHA. Ask user to complete and type "Done".
- **Irreversible Actions**: **ALWAYS** ask for explicit confirmation before clicking:
  - Submit / Complete / Finish
  - Attest / Certify
  - Approve / Confirm / Yes
  - Send / Pay
- **Ambiguity**: If unsure if an action is irreversible, ASK first.

## Recovery Rules
- **Element not found**:
  - Check for iframes.
  - Check for shadow DOM.
  - Check if the element is behind an overlay.
  - Scroll to bring it into view.
- **Click intercepted**:
  - Identify the obscuring element.
  - Dismiss it (if it's a modal/banner).
  - Wait for it to disappear (if it's a toast/spinner).
- **Stale element**:
  - Re-query the element from the DOM before interacting.
