---
name: error-handling-architecture
description: When designing how a system recovers from and reports failures.
version: 2.0.0
category: backend
tags: [backend, errors, resilience, error-handling]
skill_type: architecture
author: skiLLM
license: MIT
compatible_agents: [claude-code, cursor, copilot, codex]
estimated_context_tokens: 1700
dangerous: false
requires_review: false
security_level: review-required
dependencies: [api-design-rest]
triggers: [error, exception, try-catch, error-handling, failure]
permissions:
  filesystem: { read: true, write: true }
  network: { outbound: false }
  shell: { execute: false }
input_requirements: [existing backend service, framework setup]
output_contract: [standardized error responses, no sensitive data leaked, proper logging]
failure_conditions: [silent exception catching, returning 200 for errors, leaking database details]
last_updated: 2026-05-15
---

# Error Handling Architecture

## Purpose
Uncaught exceptions crash servers. Leaked errors expose vulnerabilities. This skill creates a central, robust pipeline for capturing, categorizing, logging, and responding to failures without leaking sensitive data, ensuring system resilience and debugging capability.

## When to use
- Setting up a new backend service
- Refactoring code with excessive uncoordinated `try/catch` blocks
- Standardizing API error responses across a team
- Implementing a new microservice with shared error handling

## When NOT to use
- Client-side error handling (different context)
- Monitoring/alerting setup (separate concern, use Logging & Observability instead)
- Specific framework error documentation

## Inputs required
- Existing backend service codebase
- Framework error handling capabilities (Express middleware, Django signals, etc.)
- Logging infrastructure setup

## Workflow
1. **Define Error Classes**: Create base `AppError` class with `statusCode`, `isOperational` flag, and metadata
2. **Categorize Errors**: Distinguish Operational (bad input, network) from Programmer (null ptr, logic bug)
3. **Centralize Middleware**: Add framework-level error handler to catch ALL exceptions globally
4. **Log Appropriately**: Full stack for 5xx errors; metadata only for 4xx errors
5. **Sanitize Output**: Strip stack traces and internal details before sending to client
6. **Crash on Programmer Error**: Unhandled programmer errors MUST crash and restart the process
7. **Test Error Paths**: Verify error handling works for all failure scenarios

## Rules
- MUST NEVER silently swallow exceptions (`catch(e) {}`)
- MUST crash and restart process for unhandled Programmer Errors
- MUST standardize all HTTP error responses to RFC 7807 format
- MUST log full stack traces for 5xx errors
- MUST log only message and context for 4xx errors
- MUST sanitize all error responses (no DB details, SQL, stack traces)
- MUST NEVER throw string literals (always throw Error objects)
- MUST distinguish between Operational and Programmer errors

## Anti-patterns
- **Throwing Strings**: `throw "User not found"` (throw Error objects always)
- **Leaking DB Details**: Sending raw SQL constraint violation messages to client
- **Silent Catching**: `catch(e) {}` with no logging or action
- **200 OK for Errors**: HTTP 200 with `{ error: true }` payload
- **Generic Messages**: "Something went wrong" (unhelpful for debugging)
- **Unhandled Promises**: Async functions without catch handlers

## Failure conditions
- Unhandled exception occurs (process crashes without logging)
- Error response includes stack trace or internal details
- Silent exception swallowing (error never logged)
- HTTP 200 returned for failed requests
- Database constraint violation message sent to client

## Validation checklist
- [ ] All errors are Error objects (never strings)
- [ ] Global error middleware catches all exceptions
- [ ] Error responses use RFC 7807 format with `type`, `title`, `detail`, `status`
- [ ] Stack traces never sent to client
- [ ] Sensitive data (DB queries, credentials) never in error responses
- [ ] Operational errors return appropriate 4xx status codes
- [ ] Programmer errors crash and restart
- [ ] Full stack traces logged for 5xx errors
- [ ] Request context (user ID, correlation ID) included in logs
- [ ] No `catch(e) {}` blocks with no action

## Output format
- **Error Object**: Contains `statusCode`, `message`, `isOperational` flag, and optional `context`
- **Response Format**: RFC 7807 Problem Details JSON
- **Log Format**: Structured JSON with timestamp, level, context, stack trace (for 5xx)
- **Process Behavior**: Unhandled programmer errors crash; operational errors continue

## Security considerations
- Error messages MUST NOT leak internal architecture (DB names, file paths, versions)
- Stack traces MUST NEVER be sent to clients (log internally only)
- Database error messages MUST be wrapped (never expose raw constraints)
- Sensitive user data MUST NOT appear in error logs (sanitize before logging)
- Error pages MUST NOT reveal system information

## Agent execution notes
- Agent MAY: Create error classes, add global error middleware, sanitize responses, implement error logging
- Agent MUST NEVER: Throw strings, catch exceptions silently, leak stack traces, return 200 for errors
- Agent MUST ASK: Before changing error categorization, before modifying global error handler
- Agent MUST VALIDATE: All errors are Error objects, no stack traces in responses, proper categorization

## Example

**❌ Anti-pattern (Silent catching, leaking details, wrong status):**
```javascript
app.get('/users/:id', async (req, res) => {
  try {
    const user = await db.query(`SELECT * FROM users WHERE id = ${req.params.id}`);
    res.json(user);
  } catch(e) {
    // ANTI-PATTERN: silent catch
    res.json({ status: 'error', message: e.message }); // ANTI-PATTERN: 200 OK
    // ANTI-PATTERN: leaking SQL details
  }
});
```

**✅ Correct pattern (Centralized, sanitized, proper codes):**
```javascript
// 1. Define error class
class AppError extends Error {
  constructor(statusCode, message, isOperational = true) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = isOperational;
  }
}

// 2. Route handler
app.get('/users/:id', async (req, res, next) => {
  try {
    const user = await db.query('SELECT * FROM users WHERE id = ?', [req.params.id]);
    if (!user) {
      return next(new AppError(404, 'User not found'));
    }
    res.json(user);
  } catch (err) {
    next(err); // Pass to global handler
  }
});

// 3. Global error middleware
app.use((err, req, res, next) => {
  // Log with context
  logger[err.isOperational ? 'warn' : 'error']({
    message: err.message,
    statusCode: err.statusCode,
    stack: err.stack,
    requestId: req.id,
    userId: req.user?.id
  });
  
  // Crash on programmer error
  if (!err.isOperational) {
    process.exit(1);
  }
  
  // Sanitized response
  res.status(err.statusCode || 500).json({
    type: 'https://api.example.com/errors/app-error',
    title: err.statusCode === 404 ? 'Not Found' : 'Server Error',
    detail: err.isOperational ? err.message : 'Internal server error',
    status: err.statusCode || 500
  });
});
```
