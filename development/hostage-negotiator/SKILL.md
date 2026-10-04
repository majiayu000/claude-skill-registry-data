---
name: hostage-negotiator
description: Keep a small requested change focused when optional refactors, architectural redesign, or unrelated cleanup threaten to expand its scope.
---

# Hostage Negotiator

> Release the button. The architecture stays.

## Establish the terms

Read supplied files, applicable project instructions and working-tree status together. Discover only missing paths; include hidden instruction files in that discovery so an incomplete inventory does not require another pass. Do not precede known-file reads with a separate directory listing. Search again for an unresolved dependency or instruction boundary. Use the project's runner.

For each supporting change, ask which acceptance condition fails without it. A small visible change can require state, error handling or security work; smallest diff is not the objective. Keep optional refactors separate, without creating a scope document for an ordinary edit. Ask when a missing product decision materially changes the implementation.

For stateful behavior, follow entry, completion and recovery through the existing owner. Preserve existing or specified return values, errors and cleanup, including cancellation. For a newly suppressed operation, assert the required suppression and state ownership without inventing an unspecified return-value contract. Reuse covered tests and add missing transitions at that boundary, not a parallel harness.

Assert observable contracts, not incidental counter increments or token values. For stale or failed work, capture contractual field values before release and compare afterward; retaining the owner object can alias in-place mutations. Preserve payload/error identity and snapshot mutable contents only when contractual. Do not invent exception-identity requirements for task cancellation.

Async regression checks must terminate even when the guarded behavior is broken: bound behavior-dependent waits and release or cancel controlled tasks in cleanup. Keep callback helpers separate from framework methods: an async `fail` or `run` on a unittest TestCase can break assertions or execution; use distinct names or composed support.

Without equivalent project support, optionally copy the [Python asyncio asset](assets/controlled_call.py) or [JavaScript Promise asset](assets/controlled_call.mjs) for the actual runtime into permitted test support. Read its complete usage block alongside application files: `sed -n '1,/^"""$/p' <python-asset>` or `sed -n '1,/^ \*\//p' <js-asset>`. These include limits and optional task lifecycle ownership to replace custom start/wait/drain plumbing; inspect implementation for trust, adaptation or unclear behavior. Assets do not replace application assertions or external-resource cleanup; no separate reference is needed.

## Deliver and stop

Run native tests in a dedicated shell command with its own results and process exit. A dedicated command need not be a separate model turn: when an edit succeeds, run the relevant test command immediately in the same tool interaction if sequencing is supported. Wait for the edit result first; do not test a failed or pending edit, run edits and tests concurrently, or replace a test exit with a later command exit. Inspect a failing test before choosing a fix. Keep before/after evidence separate; batching changes transport, not the checks or their order. Then combine remaining copy integrity (`cmp <asset> <copy>`), diff checks and scope status in one non-test call, preserving each needed exit. Inspect new code not already visible in your edit output; do not reprint a whole generated suite merely to confirm it exists. A later successful command is not test evidence; never recopy a helper to make its integrity check pass.

Review the diff against acceptance conditions, removing only your own unjustified additions. Reuse valid evidence; rerun only for changed relevant inputs, unresolved uncertainty or an explicit requirement.

Before claiming tests passed, locate their native identities/count and results, not just the shell exit or trailing diff/status. Missing evidence: first inspect an existing report tied to that command and inputs; observe a still-running process instead of restarting it. Otherwise rerun only the missing, safely repeatable check in scope, capturing its result and own exit. Never replay a deployment or side-effectful workflow merely to recover output. If evidence remains unavailable, say unverified. A later run is new evidence, not a repaired transcript; missing, undiscovered or skipped tests cannot support a pass.

When terminal capture is unreliable and local evidence files are permitted, use the [single-run native capture fallback](references/native-evidence.md); read retained results instead of rerunning solely for output.

Report decisive observations and limits, then stop when the requested behavior and checks are verified.

Preserve user changes and explicit requirements. Review does not authorize implementation; publishing and optional refactors require authorization. Keep humor optional.
