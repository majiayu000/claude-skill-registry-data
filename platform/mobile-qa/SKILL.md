---
name: mobile-qa
description: "Routes selected-device mobile QA to a compatible original native testing skill with owner device and evidence policy."
---

# Native Mobile QA

Use for native Android/iOS behavior. Mobile web layouts belong to
`responsive-breakpoint-check`; browser flows belong to `playwright-visual-qa`.
Load and follow the complete original native testing skill that covers the
selected platform and target. For Android emulator feature flows, the exposed
provider is `test-android-apps:android-emulator-qa`; performance investigations
use `test-android-apps:android-performance`. Keep the native plugin's original
instructions, scripts and update path intact. This adapter does not reproduce
the author's test loop.

An Android emulator provider does not establish physical-device or iOS support.
Those routes require an explicitly compatible original provider exposed by the
host. If a matching provider or device capability is missing, the route is
unavailable: report SKIP or BLOCKED with the missing platform or capability,
use the host's official plugin setup to install or enable the matching provider,
then refresh session exposure. Do not counterfeit a missing workflow with a
local summary or claim that a package proves a live connection.

## Owner Device And Runtime Policy

- Identify the app/build, exact device or emulator, synthetic fixture, and
  expected state before actions. Prefer a disposable emulator for setup tests.
  Do not select a physical device implicitly, reset user data, change accounts,
  install profiles, or operate unrelated apps.
- Discover only the capability needed by the selected original workflow.
  Mobile MCP is optional; the native provider may use established adb or
  simulator tooling when compatible. Missing devices/platform support are
  SKIP or BLOCKED with a reason, not a passing app test.
- Before activating a third-party server, verify its pinned source, advisory
  fixes, telemetry controls and actual action surface. Keep unsafe URL schemes
  disabled. Do not expose arbitrary shell, package installation, file transfer,
  account changes or unrelated device operations by default.
- Check each batch subcommand against the same allowed operations and target.
  A batch entry point can bypass a filter of top-level tool names; exclude it
  unless its nested operations are equally constrained.

## Owner Evidence And Cleanup Policy

- Require expected state versus observed state, including accessibility or
  screenshot evidence where needed. Successful clicks alone do not prove
  that an app passes; preserve the original safe logs and command results.
- Stop only emulator/server processes created for this task. Preserve existing
  devices, apps, SDKs, accounts and host settings.

Use synthetic photos, input text and provider errors. Never type real secrets
into fixtures or collect personal notifications, photos or account screens.
Keep screenshots, logs, device identifiers and MCP configuration outside public
repositories. Report source build, target, actions, expected versus observed
state, raw artifact paths, actual command exit codes, and remaining gaps.

Verify keyboard/input, gallery/permission, and provider-error recovery flows on
their actual app builds before claiming project acceptance. A generic emulator
smoke test proves only that tested device/tool path.
