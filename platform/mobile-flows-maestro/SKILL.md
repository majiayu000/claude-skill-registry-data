---
name: mobile-flows-maestro
description: >-
  This skill should be used when Maestro is explicitly requested or already
  present and the task is to author, run, or debug iOS/Android Maestro flows;
  use Maestro MCP; or handle Maestro selectors, system UI, permissions,
  Keychain, JavaScript, waits, device state, flakiness, or CI. Evidence includes
  a .maestro directory or flow YAML with appId. Not for XCUITest, Appium, web,
  desktop, backend, or unit tests.
---

# Maestro Mobile Flows

Use Maestro's live surface as the source of truth. CLI flags come from the
installed `maestro --help` and subcommand help. Flow YAML and JavaScript come
from current Maestro documentation. When MCP is connected, inspect its actual
tool inventory instead of naming remembered tools.

## Choose the interface

Use MCP or Studio for interactive hierarchy inspection, authoring, and feedback.
Use the CLI for scriptable execution, exit codes, reports, artifacts, and CI.
Confirm that the installed version supports `maestro mcp`, then register it
through the active host's MCP mechanism.

Hierarchy and text are cheap; repeated image payloads are not. When a host
retains images in the long-lived conversation, keep screenshots in a bounded
visual task and return only its text finding.

## Select a device deliberately

Inspect booted iOS simulators and connected Android devices. Ignore
offline/unauthorized Android entries. When more than one compatible device is
available, target one explicitly with the installed CLI's syntax--currently
`maestro --device <serial-or-udid> test <flow>`. Do not silently choose a
platform, emulator, or physical device.

## Prefer observable selectors

Prefer visible text, then accessible identifiers or descriptions, then
coordinates. Maestro text matchers are regular expressions, so escape
metacharacters and disambiguate labels that can match multiple elements. An ID
works only when the app exposes it to the platform accessibility hierarchy;
inspect the live hierarchy rather than assuming a SwiftUI identifier, Android
resource ID, Compose tag, React Native testID, or Flutter key is visible.

## State and system surfaces

Configure supported iOS and Android permissions through `launchApp.permissions`
or `setPermissions`; use platform tools only for special cases current Maestro
cannot represent.

iOS app-state clearing does not necessarily clear Keychain. For independent
authentication flows, use the current `clearKeychain` command or
`launchApp.clearKeychain` and remember that it is iOS-only.

External authentication and other system-owned surfaces can be unstable in
unattended CI. Prefer a test-build-only bypass or seeded identity when
authentication itself is not under test. Keep a controlled integration test
when the real handoff is the requirement.

Biometric simulation changes across Xcode and device tooling. Check current
Maestro docs and `xcrun simctl help` before suggesting a command; do not preserve
old `simctl` syntax as doctrine.

## JavaScript is a separate file

`runScript` executes a JavaScript file relative to the flow. Keep scripts in the
uploaded flow directory for cloud execution.

Maestro JavaScript is not Node: do not assume `require`, ES modules, filesystem
access, or browser `fetch`. Use the HTTP and output interfaces documented by the
installed/current Maestro version.

```yaml
- runScript: scripts/health.js
- assertTrue: ${output.healthy}
```

## Wait for product behavior

Maestro assertions already retry for a default window. Use
`extendedWaitUntil` when a legitimate outcome exceeds that window, with a
timeout tied to expected product behavior rather than a blanket larger value.
A larger timeout proving successful establishes timing sensitivity, not its
cause.

On failure, classify before editing: app defect, selector problem, timing race,
test-state leak, or environment failure. Do not rewrite a flow merely to make
the current run pass.

Keep independently meaningful journeys separate when that improves diagnosis
or reuse. Combine steps that form one product outcome; do not split files to
satisfy a universal one-journey rule.

Load `references/maestro-gotchas.md` for CI, platform state, system surfaces,
and failure diagnosis.
