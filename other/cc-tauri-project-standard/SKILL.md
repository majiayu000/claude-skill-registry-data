---
name: cc-tauri-project-standard
description: Use when a Tauri application needs work on Rust commands, WebView IPC contracts, capabilities and permissions, managed state, desktop lifecycle, platform builds or release boundaries. A plain Rust library without Tauri is outside this specialty.
---

# Tauri application engineering

Locate the owning web application and `src-tauri` crate. Treat UI and Rust core as application roles, regardless of the product supplying this skill.

1. Read the actual Tauri/API/plugin versions, Cargo and JavaScript locks, configuration and supported platforms. Keep v1 and v2 permission models distinct; preserve the existing toolchain.
2. Map each invoke to its Rust command, validated input, public result/error and resource owner. Keep filesystem/process authority in the core and expose narrow operations.
3. Check command registration, app-command permission generation, capabilities, window/WebView labels and remote origins together. Permissions do not validate application-specific input.
4. Define managed-state lifetimes, bounded blocking work, cancellation and shutdown. Review locks held across suspension and event listener cleanup.
5. Use the [practice checklist](references/practice.md) and [minimal application](examples/minimal/README.md). They include the local command contract needed without another skill package.
6. Follow [verification boundaries](references/verification.md): test rejected input before effects, then verify actual WebView/permission activation, target bundles and signing in their own environments.

Deliver the affected UI/core roots, invoke contract, authority decisions, actual commands/results and unverified platforms. Source or unit checks alone do not establish a working desktop release.

## Engineering practices

Read the [local engineering decisions](references/engineering-practices.md) for this task and follow their links to relevant shared principles. Apply levels and exceptions against actual project contracts; product frontend/backend labels do not constrain language or role.
