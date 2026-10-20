---
name: handoff
description: "Privately transfer a temporary workspace file between Manus execution devices with handoff.create and handoff.receive. Use when a file must move between Desktop Work Locally, another selected device, or a session runtime and no shared filesystem exists."
compatibility: opencode
---

# Handoff

Handoff copies one regular file through private temporary storage. It is an explicit transfer, not continuous synchronization.

## Send a file

1. Use `handoff.create` with a path relative to the current session workspace.
2. Return the `handoff_id`, file name, size, SHA-256, and expiry to the user.
3. Never expose or ask for an object key, storage URL, or access token.

## Receive a file

1. Use `handoff.inspect` when the ID or expected file is uncertain.
2. Use `handoff.receive` on the destination execution device. The destination is relative to that device's current workspace; omit it to use the original file name.
3. Prefer the original file name or another flat file name. Use a subdirectory only when the user requested that location; missing parent directories are created automatically, and newly created empty directories are rolled back if receive fails.
4. If the destination exists, report the conflict and ask for a different relative destination. Do not overwrite it.
5. Report the final local path only after size and SHA-256 verification and atomic placement succeed.

Handoffs are owner-only and temporary. A missing, expired, incomplete, or unauthorized ID is reported as unavailable without distinguishing the reason.
