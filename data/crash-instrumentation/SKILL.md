---
name: crash-instrumentation
description: Set up crash instrumentation with actionable context. Use when configuring crash capture, error boundaries, or breadcrumb strategies.
triggers:
  - "breadcrumb strategy"
  - "capture crashes"
  - "crash context"
  - "crash reporting"
  - "debug crashes"
  - "error boundaries"
priority: 1
---

# Crash Instrumentation

Capture crashes with the context needed to debug them.

## Core Principle

A crash report without context is useless. Every crash should include:

| Context | Why | Example |
|---------|-----|---------|
| `screen` | Where it happened | "CheckoutScreen" |
| `job_name` | What user was doing | "checkout" |
| `job_step` | Where in the flow | "payment" |
| `breadcrumbs` | What led here | Last 20 user actions |
| `app_version` | Release correlation | "1.2.3" |
| `user_segment` | Who's affected | "premium", "trial" |

## Breadcrumb Strategy

Breadcrumbs are the trail leading to a crash. Capture:

| Category | What to Log | Example |
|----------|-------------|---------|
| `navigation` | Screen transitions | "HomeScreen → CartScreen" |
| `user` | Taps, inputs, gestures | "Tapped checkout button" |
| `network` | API calls (not payloads) | "POST /api/orders started" |
| `state` | Key state changes | "Cart updated: 3 items" |
| `error` | Non-fatal errors | "Retry #2 for payment" |

**Limit:** Keep last 20-50 breadcrumbs. More is noise.

## Error Boundaries

Catch errors before they crash the app:

```swift
// iOS - capture context before crash
func captureError(_ error: Error, screen: String, job: String?) {
    Observability.captureError(error, context: [
        "screen": screen,
        "job_name": job ?? "unknown",
        "session_duration": sessionDuration(),
        "memory_pressure": memoryPressure()
    ])
}
```

```kotlin
// Android - uncaught exception handler
Thread.setDefaultUncaughtExceptionHandler { thread, throwable ->
    Observability.captureError(throwable, mapOf(
        "thread" to thread.name,
        "screen" to currentScreen,
        "job_name" to currentJob
    ))
    previousHandler?.uncaughtException(thread, throwable)
}
```

## What NOT to Attach

| Don't | Why |
|-------|-----|
| Full stack traces in breadcrumbs | Redundant, SDK captures this |
| User input text | PII risk |
| Full request/response bodies | Size limits, PII |
| Entire app state | Unbounded, noise |

## Crash Types to Handle

| Platform | Type | Instrumentation |
|----------|------|-----------------|
| iOS | `EXC_BAD_ACCESS` | Breadcrumbs, memory context |
| iOS | `SIGKILL` (watchdog) | Background task tracking |
| Android | `ANR` | Main thread breadcrumbs |
| Android | `OutOfMemoryError` | Memory tracking |
| React Native | JS exceptions | Error boundaries |

## Implementation

See `references/crash-reporting.md` for:
- Platform-specific crash capture setup
- Breadcrumb implementation patterns
- Vendor SDK configuration

See `skills/symbolication-setup` for readable stack traces.
