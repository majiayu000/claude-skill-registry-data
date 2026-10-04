---
name: ui-qa
description: "Routes UI validation to native mobile, browser, accessibility or responsive QA."
---

# UI QA Router

Use this skill for validation, debugging, and review of UI work.

Original author providers must be exposed by the current-session catalog. Read
their complete skills and prerequisites; retain reviewed upstream and native
plugin ownership.
Bible's local QA policies define the requested evidence and scope separately.
Missing native skills, tools or connections remain unresolved dependencies;
report official setup and pending exposure instead of assuming availability.

## Routing

- Requested UX critique, technical UI audit, final polish or error/edge-case
  hardening -> `impeccable.impeccable`, selecting its corresponding original
  `critique`, `audit`, `polish` or `harden` reference. Use Operate mode for app UI.
- Native Android/iOS app behavior on a device or emulator -> `mobile-qa`
- Visual fidelity, screenshot comparison, UI regression -> `playwright-visual-qa`
- Desktop/tablet/mobile web layout verification -> `responsive-breakpoint-check`
- Keyboard, focus, semantics, contrast, or ARIA review ->
  `accessibility-ui-review`
- Rendered frontend testing / debugging ->
  `build-web-apps:frontend-testing-debugging`
- React / Next.js perf review -> `build-web-apps:react-best-practices`
- Engineering review for UI changes -> `superpowers.requesting-code-review`,
  with rendered QA evidence when the requested review depends on visual behavior.

## Rule

For business apps, choose relevant evidence from `ui-business-apps`: task
completion and state behavior as well as the rendered screen. A static visual
review does not prove working filters, permissions, save behavior or chart data.
Report checks that ran and the precise unresolved interaction or runtime gap.
If evidence research is needed, select `ui-research`; if implementation is
requested, select `ui-build`. Reuse an established route on follow-up turns.
