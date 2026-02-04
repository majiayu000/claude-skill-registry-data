---
name: fvtt-error-handling
description: This skill should be used when adding error handling to catch blocks, standardizing error handling across a codebase, or ensuring proper UX with user messages vs technical logs. Covers NotificationOptions, Hooks.onError, and preventing console noise.
---

# Foundry VTT Error Handling Patterns

**Domain:** Foundry VTT V12/V13 Error Handling
**Status:** Production-Ready (Verified against V13 API)
**Last Updated:** 2025-12-31

---

## Overview

This skill provides **production-ready error handling patterns** for Foundry VTT modules, using the documented V13 APIs: `NotificationOptions` and `Hooks.onError`.

### When to Use This Skill

- Adding error handling to catch blocks in Foundry modules
- Standardizing error handling across a codebase
- Ensuring proper UX (user messages vs technical logs)
- Preventing console noise and double-logging
- Enabling ecosystem compatibility (other modules can listen to your errors)

### Core Principle

**Always separate error funnel from user notification:**

- **Error funnel** (`Hooks.onError`): Logs stack traces, triggers ecosystem hooks, provides structured data
- **User notification** (`ui.notifications.*`): Clean, sanitized messages with full UX control

**Why separation matters:**
1. `Hooks.onError` mutates `error.message` when `msg` is provided (see Foundry GitHub #6669)
2. `clean: true` only works in NotificationOptions, not Hooks.onError
3. User sees only your controlled message, not technical details
4. Explicit control over console logging (`console: false` prevents double-logging)

---

## Quick Reference: Four Error Patterns

| Pattern | Error Funnel | User Notification | Use Case |
|---------|--------------|-------------------|----------|
| **User-facing** | Hooks.onError (`notify: null`) | ui.notifications.error | Unexpected failures |
| **Expected validation** | _(none)_ | ui.notifications.warn | User input errors |
| **Developer-only** | Hooks.onError (`notify: null`) | _(none)_ | Diagnostic logging |
| **High-frequency** | Throttled Hooks.onError | Throttled ui.notifications.warn | Render loops, hooks |

---

## Pattern 1: User-Facing Failures

**Use for:** Unexpected errors, operations that failed, critical failures

```javascript
} catch (err) {
  // Preserve original error as cause when wrapping non-Errors
  const error = err instanceof Error ? err : new Error(String(err), { cause: err });

  // Error funnel: stack traces + ecosystem hooks (no UI)
  Hooks.onError(`YourModule.${contextDescription}`, error, {
    msg: "[YourModule]",
    log: "error",
    notify: null,  // No UI from hook
    data: { contextDescription, userFacingDescription }  // Structured context
  });

  // Fully controlled user message (sanitized, no console - already logged)
  ui.notifications.error(`[YourModule] ${userFacingDescription}`, {
    clean: true,
    console: false  // Hooks.onError already logged
  });
}
```

**Key points:**
- User sees only `userFacingDescription` (no technical details leaked)
- Stack trace logged via Hooks.onError (full Error object)
- Ecosystem visibility (other modules can listen to `Hooks.on("error", ...)`)
- Structured `data` for debugging and hook subscribers
- Explicit `console: false` prevents double-logging

---

## Pattern 2: Expected Validation / Recoverable Issues

**Use for:** User input errors, missing data, expected validation failures

```javascript
} catch (err) {
  const message = `[YourModule] ${userFacingDescription}`;
  ui.notifications.warn(message, {
    clean: true,
    console: false  // Expected failures - no console noise
  });
}
```

**Key points:**
- Uses `warn` severity (not `error`) for expected cases
- Simpler than Hooks.onError (no error funnel needed for routine validation)
- `console: false` avoids noise for common user-driven failures
- **Optional**: Gate console logging behind debug flag:
  ```javascript
  console: game.settings.get("your-module", "enableProfiling")
  ```

---

## Pattern 3: Developer-Only Errors

**Use for:** Diagnostic logging, internal errors that don't need user notification

```javascript
} catch (err) {
  const error = err instanceof Error ? err : new Error(String(err), { cause: err });
  Hooks.onError(`YourModule.${contextDescription}`, error, {
    msg: "[YourModule]",
    log: "error",
    notify: null,  // Log only, no UI spam
    data: { contextDescription }  // Structured context for debugging
  });
}
```

**Key points:**
- Uses error funnel (consistency) but no notification
- Stack traces logged for developers
- No UI spam for internal diagnostics
- **Alternative**: Use `console.error(...)` for truly isolated cases (but lose ecosystem hooks)

---

## Pattern 4: High-Frequency Errors

**Use for:** Render loops, hooks, event handlers that might error repeatedly

```javascript
// Module-scoped throttle (outside class/function)
const errorThrottles = new Map();

// In catch block:
} catch (err) {
  const throttleKey = contextDescription;
  const lastError = errorThrottles.get(throttleKey) || 0;

  // Throttle: 5 second window per context
  if (Date.now() - lastError > 5000) {
    const error = err instanceof Error ? err : new Error(String(err), { cause: err });

    // Error funnel (no UI)
    Hooks.onError(`YourModule.${contextDescription}`, error, {
      msg: "[YourModule]",
      log: "warn",
      notify: null,  // No UI from hook
      data: { contextDescription, userFacingDescription }
    });

    // Separate controlled notification (console: false prevents double-logging)
    ui.notifications.warn(`[YourModule] ${userFacingDescription}`, {
      clean: true,
      console: false  // Already logged via Hooks.onError
    });

    errorThrottles.set(throttleKey, Date.now());
  }
}
```

**Key points:**
- Throttles to prevent notification queue flood
- Module-scoped Map prevents spam across multiple instances
- Uses `warn` severity for non-critical repeated errors
- Separates error funnel (logs only) from user notification
- Explicit `console: false` prevents double-logging

---

## Decision Tree: Classifying Errors

**Ask these questions:**

1. **Is this unexpected?** (system failure, unhandled case, critical error)
   → **Pattern 1**: User-facing failures

2. **Is this expected validation?** (user input error, missing required data)
   → **Pattern 2**: Expected validation

3. **Is this diagnostic-only?** (internal state, no user impact)
   → **Pattern 3**: Developer-only

4. **Could this fire repeatedly?** (render loop, hook, event handler)
   → **Pattern 4**: High-frequency throttled

---

## Foundry-Specific Gotchas

### 1. `Hooks.onError` Mutates Error Objects

**Critical**: `Hooks.onError` modifies `error.message` when `msg` is provided:

```javascript
// Internal Foundry implementation (from GitHub #6669):
if (msg) err.message = `${msg}: ${err.message}`;
```

**This is why we separate funnel from notification:**
- Error funnel gets the Error object (stack traces preserved)
- User notification uses clean string (no mutation affects UX)

**Always normalize to Error objects:**
```javascript
const error = err instanceof Error ? err : new Error(String(err), { cause: err });
```

### 2. `console` Default Behavior Not Documented

**Issue**: Foundry V13 docs don't explicitly state the default value for `NotificationOptions.console`.

**Evidence**: API examples show `{ console: false }` to suppress logging, implying default is `true`.

**Best practice**: Be explicit to prevent double-logging and future-proof against default changes:
```javascript
ui.notifications.error(message, {
  clean: true,
  console: false  // Explicit is better than implicit
});
```

### 3. `notify` String Values Are Undocumented

**Issue**: `Hooks.onError` accepts `notify: null | string`, but valid string values aren't enumerated in V13 API docs.

**Your assumption**: `notify` accepts `"error"`, `"warn"`, `"info"` (like `ui.notifications.*` methods)

**Reality**: Likely correct but NOT explicitly documented.

**Best practice**: Use `notify: null` + separate `ui.notifications.*` for full control:
```javascript
// Avoid relying on undocumented notify strings
Hooks.onError(..., { notify: null });  // Error funnel only
ui.notifications.error(...);           // Separate notification
```

### 4. `clean: true` Only Works in NotificationOptions

**Issue**: `{ clean: true }` sanitizes untrusted input, but ONLY in `ui.notifications.*`.

**Does NOT work in `Hooks.onError`**: The `msg` parameter is NOT sanitized by Hooks.onError.

**Best practice**:
- Keep `msg` in Hooks.onError generic (module prefix only): `msg: "[YourModule]"`
- Put user/document data in separate `ui.notifications.*` call with `{ clean: true }`

```javascript
// ❌ Bad - untrusted data in Hooks.onError msg
Hooks.onError(..., { msg: `[Module] ${userInput}` });  // Not sanitized!

// ✅ Good - untrusted data in ui.notifications with clean: true
Hooks.onError(..., { msg: "[Module]", notify: null });
ui.notifications.error(`[Module] ${userInput}`, { clean: true });
```

### 5. `{ cause: err }` Has Excellent Support

**Good news**: Error `cause` parameter (ES2022) is widely supported:
- Available since September 2021 (4+ years)
- Foundry V13 minimum: Chromium 122, Firefox 127, Electron 33+
- **Safe to use** in all Foundry V13+ environments

**Usage**:
```javascript
const error = err instanceof Error ? err : new Error(String(err), { cause: err });
```

Preserves original error context for debugging in modern browsers.

---

## Implementation Checklist

When adding error handling to your module:

### 1. Audit All Catch Blocks
```bash
grep -r "} catch" scripts/
```

### 2. Classify Each Error
- [ ] Unexpected failure? → Pattern 1 (user-facing)
- [ ] Expected validation? → Pattern 2 (expected validation)
- [ ] Diagnostic only? → Pattern 3 (developer-only)
- [ ] High-frequency? → Pattern 4 (throttled)

### 3. Replace Patterns
- [ ] `console.log` → `console.error` or Hooks.onError (minimum fix)
- [ ] Manual notification + console → Hooks.onError (`notify: null`) + ui.notifications.*
- [ ] Expected failures → `ui.notifications.warn` with `console: false`
- [ ] Use `{ clean: true }` on ui.notifications.* for user/document data
- [ ] **Default to `console: false`** (prevents noise + double-logging)
- [ ] **Never** put untrusted strings in Hooks.onError `msg` (it's a prefix only)
- [ ] **Always** separate error funnel from user notification
- [ ] Preserve original error: `new Error(String(err), { cause: err })`
- [ ] Add structured `data` to Hooks.onError for debugging
- [ ] Throttle errors in render loops/hooks (prevent UI spam)

### 4. Test Error Paths
- [ ] Verify user-facing errors show clean message (no technical details leaked)
- [ ] Verify stack traces in console (Error objects via Hooks.onError)
- [ ] Verify `warn` severity used for expected validation errors
- [ ] Check that diagnostic errors don't spam UI (Hooks.onError with `notify: null`)
- [ ] Test throttling for high-frequency error paths (5 second window)
- [ ] Verify no double-logging (Hooks.onError + ui.notifications with `console: false`)
- [ ] Verify structured `data` appears in error hooks for debugging

---

## Verification Notes

**Verified against Foundry V13 API** (2025-12-31):

### ✅ Documented and Correct

- **`NotificationOptions.console`**: Optional boolean - "Whether to log the message to the console"
- **`NotificationOptions.clean`**: Optional boolean - "Whether to clean the provided message string as untrusted user input"
- **`Hooks.onError` signature**:
  ```typescript
  static onError(
    location: string,
    error: Error,
    options?: {
      data?: object;
      log?: null | string;
      msg?: string;
      notify?: null | string;
    }
  ): void
  ```
- **All four parameters documented**:
  - `msg`: String - "A message which should prefix the resulting error or notification"
  - `log`: null | string - "The level at which to log the error to console (if at all)"
  - `notify`: null | string - "The level at which to spawn a notification in the UI (if at all)"
  - `data`: object - "Additional data to pass to the hook subscribers"
- **Notification types**: `"info"`, `"warn"`, `"error"` (all documented)
- **`notify: null`**: Explicitly documented as valid (suppresses UI notification)
- **`{ cause: err }`**: Excellent browser support (ES2022, 4+ years available)

### ⚠️ Undocumented Behaviors

- `console` default value not explicitly stated (defensive `console: false` recommended)
- `notify` string values not enumerated (use `notify: null` + separate notifications)
- `Hooks.onError` mutates `error.message` (normalize to Error objects, separate funnel from notification)

---

## Benefits of This Approach

- **Foundry-native**: Uses only documented NotificationOptions and Hooks.onError APIs
- **Full UX control**: Always separates error funnel from user message (no technical leaks)
- **Stack traces**: Error objects via Hooks.onError include full stack traces in console
- **Preserves context**: `{ cause: err }` retains original error when wrapping non-Errors
- **Structured debugging**: `data` parameter provides context to hook subscribers and debugging
- **Ecosystem-compatible**: Error funnel allows other modules to listen to your errors
- **Better UX**: Severity discipline (warn vs error) + throttling prevents notification spam
- **Sanitization**: `{ clean: true }` on ui.notifications.* prevents XSS from error messages
- **No double-logging**: Explicit `console: false` prevents duplicate entries
- **Reduced console noise**: Expected validation errors don't clutter console by default
- **Consistent pattern**: All errors use same "funnel + notification" approach
- **Robust throttling**: Module-scoped Map prevents spam across multiple instances
- **Future-proof**: Uses only documented Foundry V13 error handling mechanisms

---

## Optional Enhancement: Localization

For published modules, consider localizing error messages:

```javascript
const message = game.i18n.format("YOUR_MODULE.Error.FailedToAddItem", {
  error: err.message
});
ui.notifications.error(message, { clean: true, console: false });
```

**Note**: If using `game.i18n.format`, the `format` function returns a sanitized string, so `clean: true` may be redundant (but harmless).

---

## References

### Foundry V13 API Documentation
- [NotificationOptions Interface](https://foundryvtt.com/api/interfaces/foundry.NotificationOptions.html)
- [Hooks.onError Method](https://foundryvtt.com/api/classes/foundry.helpers.Hooks.html)
- [Notifications Class](https://foundryvtt.com/api/classes/foundry.applications.ui.Notifications.html)

### GitHub Issues
- [Hooks.onError Implementation #6669](https://github.com/foundryvtt/foundryvtt/issues/6669) - Documents error.message mutation behavior

### Browser APIs
- [Error.cause - MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error/cause)
- [Can I Use: Error.cause](https://caniuse.com/mdn-javascript_builtins_error_cause)

### Related Skills
- `foundry-vtt-performance-safe-updates` - Multi-client update safety patterns
- `foundry-vtt-dialog-compat` - DialogV2 Shadow DOM patterns
- `foundry-vtt-version-compat` - API compatibility layer patterns

---

## Example: Real-World Usage

```javascript
// In blades-alternate-actor-sheet.js
import { queueUpdate } from "./lib/update-queue.js";

async _onItemCreate(event) {
  event.preventDefault();
  const itemType = event.currentTarget.dataset.itemType;

  try {
    // Attempt to create item
    const itemData = {
      name: `New ${itemType}`,
      type: itemType,
      system: {}
    };

    await queueUpdate(async () => {
      await this.actor.createEmbeddedDocuments("Item", [itemData]);
    });

    ui.notifications.info(`[BitD-Alt] Created new ${itemType}`);

  } catch (err) {
    // Pattern 1: User-facing failure
    const error = err instanceof Error ? err : new Error(String(err), { cause: err });

    Hooks.onError("BitD-Alt.ItemCreate", error, {
      msg: "[BitD-Alt]",
      log: "error",
      notify: null,
      data: { itemType, actorId: this.actor.id }
    });

    ui.notifications.error(`[BitD-Alt] Failed to create ${itemType}`, {
      clean: true,
      console: false
    });
  }
}
```

---

**Last Updated:** 2025-12-31
**Status:** Production-Ready (Verified against Foundry V13 API)
**Maintainer:** Claude Code (BitD Alternate Sheets)
