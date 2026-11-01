---
name: chrome-local-automation
description: Connect app-specific browser skills to an already connected Chrome session through managed tabs and DOM automation. Use for reusable tab setup, click/readback helpers, and web workflow control; not for standalone CDP, background HTTP control, account login, or credential storage.
---

# Chrome local automation bridge

Use this Skill as the common bridge between Chrome and software-specific browser workflows. It assumes Chrome is already connected to the host automation runtime and keeps login, two-factor authentication, paid submissions, and account selection under explicit user control. It does not provide a standalone CDP server, HTTP bridge, or headless background controller.

## Establish the tab

1. Initialize or refresh the browser runtime and read its returned state before selecting a tab.
2. Prefer an existing tab passed by the user or a stable mention. Do not hard-code browser IDs or tab IDs that can change between sessions.
3. To create a test or workflow tab, use the connected Chrome target and open the exact URL, then immediately read back URL and page state.
4. If Chrome disappears from the runtime inventory, refresh once or reset the runtime only when no uncommitted task is in progress; do not switch to another browser profile automatically.

## Control and verify

- Use DOM roles, accessible names, text, and visible state as the primary route; do not rely on fixed pixel coordinates.
- After every click, submit, expand, upload, or navigation, read back the page state. Do not treat a click return alone as success.
- Save the request state and old result inventory before a non-reversible web action. Submit authorized actions only once; resume or reconcile after timeout instead of automatically resubmitting.
- Keep credentials, cookies, tokens, local storage contents, account IDs, and private page data out of scripts, logs, and packaged skills.
- When an app-specific workflow exists, let this bridge own tab setup and generic click/readback checks while the app skill owns domain selectors and business validation.

## Reusable helper

Import `scripts/chrome-bridge.mjs` only inside a browser automation runtime that supplies the `cua` object. The helper exposes:

- `ensureTab(cua, options)` for an existing mention/tab or a newly created managed tab.
- `assertPage(tab, expected)` for URL and readiness readback.
- `safeClick(tab, locator, label)` for a single visible click followed by a DOM snapshot.
- `describeTab(tab)` for a minimal state record.

This helper intentionally has no network credential handling and no protocol bypass. If managed-tab access is unavailable, stop and report the gap rather than claiming silent background control.
