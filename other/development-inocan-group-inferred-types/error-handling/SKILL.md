---
name: error-handling
description: Handle errors consistently across frontend and backend. Use when implementing try/catch patterns, error boundaries, API error responses, or error reporting.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Error Handling Skill

Consistent error handling patterns for JavaScript applications.

## Core Principles

| Principle | Description |
|-----------|-------------|
| Fail Fast | Detect errors early, at system boundaries |
| Explicit Errors | Never swallow errors silently |
| Meaningful Messages | Errors should explain what went wrong and why |
| Graceful Degradation | Provide fallbacks when possible |
| Error Tracking | Log and report errors for observability |

## Error Categories

| Category | Where | Pattern |
|----------|-------|---------|
| Sync Errors | Component lifecycle | Error boundaries |
| Async Errors | Promises, fetch | try/catch, .catch() |
| Network Errors | API calls | Retry logic, offline queuing |
| Validation Errors | Form input, API | Field-level messages |
| System Errors | Uncaught exceptions | Global handlers |

## Pattern Quick Reference

### Synchronous Errors

```javascript
// Type guard with assertion
function assertDefined(value, message = 'Value is undefined') {
  if (value === undefined || value === null) {
    throw new Error(message);
  }
  return value;
}

// Defensive programming
function processUser(user) {
  assertDefined(user, 'User is required');
  assertDefined(user.id, 'User ID is required');
  // Safe to use user.id here
}
```

### Asynchronous Errors

```javascript
// Always handle promise rejections
async function fetchData() {
  try {
    const response = await fetch('/api/data');
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Fetch failed:', error);
    throw error; // Re-throw for caller to handle
  }
}
```

### Custom Error Classes

```javascript
// Typed errors with additional context
class ApiError extends Error {
  constructor(status, statusText, body = null) {
    super(`API Error: ${status} ${statusText}`);
    this.name = 'ApiError';
    this.status = status;
    this.body = body;
  }
}

class ValidationError extends Error {
  constructor(field, message) {
    super(`Validation: ${field} - ${message}`);
    this.name = 'ValidationError';
    this.field = field;
  }
}

// Usage
if (error instanceof ApiError && error.status === 401) {
  redirectToLogin();
}
```

### Error Boundaries (Components)

Use the `<error-boundary>` custom element to catch component errors:

```html
<error-boundary name="user-profile">
  <user-profile user-id="123"></user-profile>
  <template slot="fallback">
    <p>Could not load profile.</p>
  </template>
</error-boundary>
```

See: `/add-error-boundary` command for implementation.

### Global Error Handlers

```javascript
// Catch unhandled errors
window.onerror = function(message, source, lineno, colno, error) {
  reportError({
    type: 'uncaught',
    message,
    source,
    line: lineno,
    column: colno,
    stack: error?.stack
  });
  return false; // Allow default handling
};

// Catch unhandled promise rejections
window.onunhandledrejection = function(event) {
  reportError({
    type: 'unhandled-rejection',
    reason: event.reason
  });
};
```

### API Error Responses (Backend)

```javascript
// Consistent error response format
function errorResponse(res, status, type, message, details = null) {
  res.status(status).json({
    type,
    message,
    ...(details && { details })
  });
}

// Usage in route
app.post('/api/users', (req, res) => {
  const { email, password } = req.body;

  if (!email) {
    return errorResponse(res, 400, 'validation', 'Email is required', {
      field: 'email'
    });
  }

  // ...
});
```

## Error Flow Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  User Action    │────▶│  Error Handler  │────▶│  Error Report   │
│  (click, input) │     │  (try/catch)    │     │  (logging/API)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │  User Feedback  │
                        │  (toast/inline) │
                        └─────────────────┘
```

## User Feedback Patterns

| Error Type | Feedback | Example |
|------------|----------|---------|
| Validation | Inline field error | "Email is required" |
| Network | Toast notification | "Connection lost. Retrying..." |
| Auth | Redirect or modal | Redirect to login |
| Server | Generic message | "Something went wrong" |
| Not Found | 404 page or inline | "Resource not found" |

```javascript
// Centralized error display
function showError(error, options = {}) {
  const { type = 'toast', duration = 5000 } = options;

  if (type === 'inline' && options.container) {
    options.container.innerHTML = `
      <div class="error-message" role="alert">
        ${error.message}
      </div>
    `;
  } else {
    // Toast notification
    const toast = document.createElement('div');
    toast.className = 'toast toast--error';
    toast.setAttribute('role', 'alert');
    toast.textContent = error.message;
    document.body.appendChild(toast);

    setTimeout(() => toast.remove(), duration);
  }
}
```

## Detailed Implementation

For comprehensive patterns, see these related skills:

| Skill | Coverage |
|-------|----------|
| **observability** | Global handlers, error reporting, Web Vitals |
| **api-client** | API errors, retry logic, typed responses |
| **javascript-author** | Defensive patterns, type guards |
| **nodejs-backend** | Server error middleware, logging |
| **logging** | Structured error logging |

## Checklist

When implementing error handling:

**Frontend**
- [ ] Global `window.onerror` handler installed
- [ ] Unhandled promise rejections caught
- [ ] Error boundaries wrap risky components
- [ ] Async functions wrapped with try/catch
- [ ] User-friendly error messages shown
- [ ] Errors reported to monitoring service

**Backend**
- [ ] Consistent error response format
- [ ] Errors logged with context (request ID, user)
- [ ] Sensitive data not exposed in errors
- [ ] Validation errors return field-level details
- [ ] 5xx errors trigger alerts

**Both**
- [ ] Custom error classes for typed handling
- [ ] Errors re-thrown after logging (not swallowed)
- [ ] Stack traces available in development
- [ ] Generic messages in production

## Related Skills

- **validation** - JSON Schema validation with AJV, ValidationError patterns
- **observability** - Error tracking, performance monitoring
- **api-client** - Fetch error patterns, retry logic
- **javascript-author** - Defensive programming, type guards
- **nodejs-backend** - Server-side error handling
- **logging** - Structured error logging
