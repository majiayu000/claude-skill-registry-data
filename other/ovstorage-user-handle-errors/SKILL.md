---
name: ovstorage-user-handle-errors
description: Use when an ovstorage tool returns ok false and you need to interpret the envelope error and choose the next action.
license: CC-BY-4.0
version: "0.1.0"
author: NVIDIA Omniverse
tags: [ovstorage, errors, mcp]
tools: [Read]
compatibility: Requires ovstorage MCP tools or equivalent result-envelope output.
---

# Reading Envelope Errors

**Goal:** When a tool call fails, understand what went wrong and what
to do next.

**When to use this:** Any time you get `ok: false` from a tool. Bookmark
this — it's the cross-cutting primer the other runbooks reference.

## Anatomy of an error envelope

```json
{
  "v": "0.1",
  "ok": false,
  "operation": "ovstorage_read",
  "resource": "s3://my-bucket/missing.bin",
  "error": {
    "code": "NotFound",
    "message": "NotFound: object missing at s3://my-bucket/missing.bin",
    "retryable": false,
    "next_action": "Add a matching connection to ovstorage.toml and restart the host."
  }
}
```

The fields you care about, in order of usefulness:

### 1. `error.code` — the canonical reason

A stable string identifying the failure category. Pin your branching
on this, not on `error.message`. Common codes:

| Code | Meaning |
|---|---|
| `NotFound` | Address doesn't exist |
| `AlreadyExists` | Destination is taken (write with `if_dest: {"kind": "fail"}`) |
| `PermissionDenied` | Auth allows the call but not on this resource |
| `AuthRequired` / `CredentialExpired` | Connection needs auth refresh |
| `NoRoute` / `NotConfigured` | No backend serves this address and no anonymous fallback is granted for its scheme |
| `Unsupported` | Backend exists but doesn't support this op |
| `PreconditionFailed` | A write-side `if_match` / `if_dest` precondition failed before anything was committed |
| `ObjectModified` | The object changed *during* a call already under way, or a read's `if_match` failed |
| `ResourceExhausted` | Hit a cap (`max_bytes`, quota, rate) |
| `InvalidArgument` | The arguments you passed are wrong |
| `Transient` / `BrokerUnavailable` / `ResourceExhausted` / `DeadlineExceeded` | Backend hiccup, cap, or throttling; retry-friendly |
| `Cancelled` | The call was cancelled (Ctrl+C, timeout, etc.) |

Full list and meanings: see `ErrorCode` in
[`docs/public/agent/mcp-tools.md`](../../docs/public/agent/mcp-tools.md).

### 2. `error.retryable` — should you try again

A boolean. `true` means a blind retry with the same arguments might
succeed. Today only these codes are retryable: `Transient`,
`BrokerUnavailable`, `ResourceExhausted`, `DeadlineExceeded`,
`CacheLockContention`, `AuthorizationLeaseExpired`.

When `retryable: true`:
- Retry with exponential backoff (e.g., 1s, 2s, 4s) up to 3-5 attempts
- If still failing, surface to the user — don't loop forever

When `retryable: false`: do **not** retry the same call. Either the
input is wrong (fix it), the resource doesn't exist (different
recovery), or the operation isn't supported (use a different one).

### 3. `error.next_action` — the recovery hint

A human-readable string suggesting what to do next. Present at
high-value error sites (auth failures, missing config, no-route). When
present, it's the most actionable signal — it tells you the *specific*
call to make.

`next_action` is **not** present on every error. If absent, fall back
to `error.code` and the table above.

### 4. `error.message` — for logging / surfacing to humans

Human-readable. Signed-URL query params and bearer tokens are
redacted, and a failed object-storage request surfaces the provider's
error code (for example `AuthenticationFailed`) rather than its
response body. Two paths are carved out of that: a provider's
*credential* endpoint, whose response text can still reach the
message, and per-entry queue batch failures, which carry the
provider's own free-form failure message. So treat `error.message` as
sensitive whenever you forward it off-host. Use it for logs and for
messages you show the user, **not** for branching logic.

## Decision tree

```
Is `error.retryable` true?
├─ yes → retry with backoff (3-5 attempts)
└─ no
   ├─ Is `error.next_action` present?
   │  ├─ yes → do what it says
   │  └─ no → branch on `error.code`:
   │       ├─ NotFound / AlreadyExists → input-shaped; agent decides
   │       ├─ PermissionDenied / AuthRequired → surface to user
   │       ├─ InvalidArgument → review your tool-call arguments
   │       ├─ Unsupported → check ovstorage_capabilities; choose a different op
   │       └─ Internal / IntegrityFailure / etc. → surface to user
```

## MCP-specific note

Every error envelope is also reflected as `isError: true` on the MCP
`CallToolResult`. Both signals say the same thing — your client
library may surface them separately. Trust whichever is more natural;
they're never inconsistent.

## What NOT to do

- **Don't pattern-match on `error.message` text.** It's for humans. The text varies; the code doesn't.
- **Don't retry on non-retryable codes.** A blind retry of `PermissionDenied` won't suddenly succeed.
- **Don't fabricate `next_action` recovery steps when the field is absent.** If you don't know what to do, surface the error rather than guess.

## See also

- [ovstorage-user-getting-started](../ovstorage-user-getting-started/SKILL.md) — run `ovstorage_doctor` to investigate config-related errors
- [`docs/public/agent/envelope.md`](../../docs/public/agent/envelope.md) — envelope v=0.1 contract
- [`docs/public/agent/mcp-tools.md`](../../docs/public/agent/mcp-tools.md) — per-tool error specifics
