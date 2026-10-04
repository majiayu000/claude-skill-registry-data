---
name: macos-screen-capture-lifecycle
description: "Use when building or diagnosing macOS ScreenCaptureKit consent, stream ownership, teardown, restart, privacy, or runtime proof; not camera capture."
license: "MIT"
metadata:
  author: "coryparrry"
  version: "0.1.0"
  last-updated: "2026-08-30"
  last-reviewed: "2026-08-30"
  apple-docs-reviewed: "2026-08-30"
---

# macOS Screen Capture Lifecycle

Treat capture as a user-consented, stateful resource. Completion means the exact executable can start, deliver, stop, drain, release, and—when promised—restart without stale work.

## Route the work

First identify the caller's executable path, bundle ID, signature, PID, launch method, deployment target, current lifecycle owner, and failing stage. Do not infer TCC state from another build, process, checkbox, or compilation.

- For one frame, prefer `SCScreenshotManager` with a narrow fresh filter when it is available for the deployment target; otherwise use a tested, bounded one-frame `SCStream` path or raise the deployment floor deliberately.
- For `SCStream`, callbacks, teardown, restart, permission diagnosis, or runtime checks, read [references/stream-lifecycle.md](references/stream-lifecycle.md).
- Before changing APIs or review dates, read [references/apple-documentation.md](references/apple-documentation.md) and query Xcode `DocumentationSearch` for the exact symbols.

## Non-negotiable invariants

- Explain capture and prompt only from clear user action. Permission is not consent for unrelated capture.
- Never reset TCC, modify its database, open System Settings, relaunch processes, or restart capture services without authorization.
- Use one serialized lifecycle owner. Retain stream, delegate, outputs, and queues for their registration lifetime.
- Attach outputs before start; roll back partial setup. Give callbacks a generation so old work cannot mutate a new session.
- Teardown is idempotent and transition-aware: a stop requested during asynchronous start is recorded, start completion settles exactly once, any successful start is then stopped exactly once, and only afterward are outputs removed, queues fenced from outside them, accepted work drained/cancelled, and ownership released.
- Route caller stop and `stream(_:didStopWithError:)` through the same teardown. Treat `userStopped` as intentional; retries are bounded, cancellable, and never used for missing consent.
- Minimize source and duration. Do not log pixels, OCR, titles, thumbnails, filter contents, or user text.

Validate the real launch path: consent states, first valid frame, cancellation during transitions, no post-teardown work, repeated cycles without multiplied callbacks or resource growth, source loss, bounded recovery, and app quit. A shared system daemon remaining alive is not proof the app still captures.

Update `last-updated` for material changes, `last-reviewed` after substantive review, and `apple-docs-reviewed` only after checking Apple sources.

## Review

- Last updated: 2026-08-30
- Last reviewed: 2026-08-30
- Apple documentation reviewed: 2026-08-30

Scope/evidence: ScreenCaptureKit consent, stream ownership, teardown, and restart guidance was checked with Xcode MCP `DocumentationSearch`.

[Apple documentation evidence](references/apple-documentation.md)
