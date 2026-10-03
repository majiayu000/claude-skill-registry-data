---
name: browser-automation-router
description: Choose the narrowest reliable browser surface across Codex Browser, signed-in Chrome, Playwright CLI, and platform scripts. Use for browser automation, logged-in workflows, UI inspection, screenshots, form filling, publish previews, or frontend QA.
---

# Browser Automation Router

Choose the narrowest reliable browser surface before acting.

## Route Order

1. Prefer a purpose-built connector, API, or CLI when it fully supports the requested read or write action.
2. Use Codex's in-app Browser for public pages, localhost, visual review, annotations, downloads, and isolated sign-in state.
3. Use the Codex Chrome extension when the task requires the user's existing Chrome profile, signed-in session, open tabs, or extensions.
4. Use `$playwright` for deterministic terminal/CI runs, repeatable regression suites, tracing, or unattended batch execution.
5. Use a platform-specific automation script only when it exposes a tested batch/export contract that the native browser surface does not replace.
6. Use Computer Use only for browser-external desktop UI or a browser flow unsupported by the Browser/Chrome surfaces.

## Native Browser Rule

- Do not maintain custom JavaScript snippets, selectors, browser launchers, cookie importers, or profile-path logic for ordinary interactive browser work.
- Follow the installed Browser or Chrome plugin skill and its live documentation. Do not copy its internal bootstrap code into this repository.
- Prefer visible page state, snapshots, semantic locators, normal clicks/fills, and screenshots.
- Use page evaluation only when a high-level read-only operation cannot obtain the evidence. Never use it to inspect cookies, local storage, passwords, tokens, or profile files.
- Reuse the current browser binding or claimed tab during the task; do not create duplicate sessions without a reason.

## Fail-Closed Capability Gate

The native route requires Codex Desktop with the Browser or Chrome plugin available in the current task.

- Capability floor: Codex Desktop release dated `2026-06-11` or later for the Browser/Chrome Developer mode used by this routing policy.
- OpenAI does not publish a stable numeric desktop build floor for this feature. Treat the release date plus live plugin availability as the minimum contract.
- The in-app Browser has its own browser state. It does not inherit the user's Chrome profile.
- Chrome profile reuse requires the Codex Chrome extension and user-approved access to the intended tab/account.
- Plan, workspace policy, region, and rollout state may still disable a surface on a nominally new enough app.
- If the required plugin is absent or disabled, report the missing capability and select an explicit Playwright/platform-script fallback. Do not pretend the native route ran.

## Write Gates

- Keep navigation and read-only extraction separate from publish, comment, follow, like, bookmark, delete, account-switch, or settings changes.
- Confirm the active account and exact write action immediately before execution.
- Stop on captcha, unexpected login, wrong account, permission prompts, ambiguous targets, or changed page state.
- Never commit credentials, cookies, login state, QR payloads, or local Chrome profile paths.

## Evidence

Return the selected surface, capability check, target account boundary, actions performed, screenshots or output artifacts, blocked steps, and fallback used. Do not claim success from planned actions alone.
