---
name: cc-electron-project-standard
description: Use when an Electron application needs work on main/preload/renderer boundaries, contextBridge IPC, sender validation, sandbox and navigation policy, native modules, lifecycle or desktop packaging. A Node HTTP service without Electron is outside this specialty.
---

# Electron application engineering

Identify the owning application and its main, preload and renderer entry points. JavaScript/TypeScript does not imply a browser-only or service-only role.

1. Read the actual Electron/Node/Chromium version, lock, packaging tool and supported platforms. Keep the project's existing module and build conventions.
2. Define a narrow typed bridge: one operation per channel, validated arguments and stable results. Authorize the actual sender/frame in main before any privileged effect.
3. Check `contextIsolation`, sandbox, Node integration, preload contents, protocol/CSP, navigation and new-window behavior together. An isolated renderer still sends untrusted IPC input.
4. Own listeners, handlers, windows, workers and native resources through startup/shutdown. Check native-module ABI/rebuild and ASAR/resource paths against the packaged application.
5. Use [practice](references/practice.md) and the [closed minimal example](examples/minimal/README.md), including its main/preload/renderer contract and explicit faulty variant.
6. Follow [verification](references/verification.md): rejected sender/input tests precede process/UI tests, platform bundles, upgrades and signing.

Deliver process boundaries, bridge contract, security decisions, actual verification and platform gaps. Node handler tests do not prove Electron sandbox activation or a signed application.

## Engineering practices

Read the [local engineering decisions](references/engineering-practices.md) for this task and follow their links to relevant shared principles. Apply levels and exceptions against actual project contracts; product frontend/backend labels do not constrain language or role.
