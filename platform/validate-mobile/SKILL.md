---
name: validate-mobile
description: Run a Maestro flow on an explicitly selected iOS or Android device and report behavioral evidence
argument-hint: "[flow-file-or-dir]"
user-invocable: true
---

# Validate Mobile

Invoke `mobile-flows-maestro` and run the flow in `$ARGUMENTS`.

Use the supplied path or discover the project's Maestro configuration. If more
than one unrelated flow is plausible, choose from the requested feature or ask
rather than running an arbitrary suite.

Determine the target platform from the flow, app configuration, and project
commands. Inspect booted iOS simulators with `xcrun simctl list devices booted`
and Android devices with `adb devices`; reject offline/unauthorized entries.
Use an already running compatible device when possible. If more than one is
available, select explicitly rather than relying on a default.

Verify flag placement with live help, then run the selected flow using the
current equivalent of:

```bash
maestro --device "$DEVICE_ID" test "$FLOW"
```

On failure, follow the skill's classification before changing the flow. Inspect
the failed step and relevant log tail. Retain a screenshot only when visual
evidence can distinguish the cause, and keep image payloads in a bounded visual
task when the host provides one.

Report the flow, platform, device, result, failed postcondition, and evidence.
