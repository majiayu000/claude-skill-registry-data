---
name: logging-observability-standards
description: When setting up telemetry, debugging distributed systems, or standardizing application output.
version: 2.0.0
category: architecture
tags: [architecture, observability, logging, backend]
skill_type: architecture
author: skiLLM
license: MIT
compatible_agents: [claude-code, cursor, copilot, codex]
estimated_context_tokens: 2000
dangerous: false
requires_review: false
security_level: review-required
dependencies: [error-handling-architecture]
triggers: [logging, observability, debugging, monitoring, tracing]
permissions:
  filesystem: { read: true, write: true }
  network: { outbound: true }
  shell: { execute: false }
input_requirements: [backend service, logging infrastructure]
output_contract: [structured json logs, correlation ids, no sensitive data leaked]
failure_conditions: [plaintext logs, no trace context, pii in logs]
last_updated: 2026-05-15
---

# Logging & Observability Standards

## Purpose
Logs are the black box recorder of your system. When failures happen at 2 AM in production, logs are your only witness. This skill ensures application state and failures are highly searchable, machine-readable, and traceable across system boundaries WITHOUT leaking sensitive user data.

## When to use
- Bootstrapping a new backend microservice or monolithic API
- Refactoring code filled with disorganized `console.log` or `print` statements
- Designing a system that spans multiple services/functions
- Setting up monitoring, alerting, and debugging infrastructure

## When NOT to use
- Application performance monitoring (APM) - related but different concern
- Security incident response (use SIEM/security tools)
- User analytics (different use case, different tool)

## Inputs required
- Backend service with multiple endpoints/functions
- Logging infrastructure (ELK, DataDog, Grafana Loki, CloudWatch, etc.)
- Understanding of structured logging concepts

## Workflow
1. **Implement Structured Logging**: Configure logger to output NDJSON (Newline Delimited JSON) instead of plain text
2. **Inject Context**: Attach a `correlation_id` (or `trace_id`) at HTTP entry point and pass through all downstream calls
3. **Standardize Levels**: ERROR (system broken), WARN (unexpected but recovered), INFO (lifecycle), DEBUG (verbose tracing)
4. **Sanitize Data**: Implement redaction middleware to mask credentials, tokens, and PII before logs hit the stream
5. **Add Request Context**: Log request duration, status code, user context (anonymized), and performance metrics
6. **Trace Async Flows**: Pass correlation ID through event handlers, message queues, and inter-service calls
7. **Monitor Log Health**: Alert on high ERROR rates, unexpected patterns, or missing correlation IDs

## Rules
- MUST output JSON in production environments (not plain text)
- MUST include Request ID/Correlation ID in all HTTP requests
- MUST NEVER log raw passwords, session tokens, or financial data
- MUST log full stack traces for ERROR level (for debugging)
- MUST log only message and context for WARN/INFO (not verbose)
- MUST redact/sanitize any PII before log emission
- MUST include timestamps in UTC
- MUST standardize key names across all logs

## Anti-patterns
- **String Concatenation**: `logger.info("User " + userId + " failed to login")` (unqueryable)
- **Logging Expected Errors as ERROR**: Logging validation failure as ERROR (use INFO/WARN)
- **Silent Catching**: Catching exception without logging the stack trace
- **No Context**: Logs with no request/correlation ID (impossible to trace)
- **Unstructured Logs**: Plain text logs without JSON structure
- **Missing Timestamps**: Logs without UTC timestamps (ordering problems)
- **Over-Logging**: Logging every line of execution (noise, storage cost)

## Failure conditions
- Logs are plain text (not JSON)
- No correlation ID tracking
- PII or credentials in logs
- Missing stack traces on ERROR logs
- No way to correlate logs across services

## Validation checklist
- [ ] Logger outputs NDJSON (each line is valid JSON)
- [ ] Correlation ID/Trace ID included in all requests
- [ ] ERROR logs include full stack traces
- [ ] INFO/WARN logs are concise (no excessive detail)
- [ ] All timestamps in UTC
- [ ] No passwords, tokens, or PII in logs
- [ ] Request duration/latency logged
- [ ] Correlation ID passed through async/inter-service calls
- [ ] Redaction middleware configured and working
- [ ] Log levels used correctly (ERROR for failures, INFO for lifecycle)
- [ ] Searchable by correlation ID (verified in log aggregator)
- [ ] Sampling/retention policy defined (cost management)

## Output format
- **Log structure**: JSON with consistent keys: timestamp, level, message, correlationId, userId (anonymized), duration, error, stack
- **Log format**: NDJSON (one valid JSON object per line)
- **Timestamps**: UTC ISO 8601 format
- **Levels**: ERROR, WARN, INFO, DEBUG
- **Middleware**: Automatic request ID generation, redaction on output

## Security considerations
- All PII (names, emails, phone numbers) MUST be redacted or anonymized
- Tokens, API keys, passwords MUST NEVER appear in logs
- Credit card data MUST NEVER appear in logs
- Database connection strings MUST be redacted
- User IDs may appear but real names MUST NOT
- Logs MUST be encrypted in transit and at rest

## Agent execution notes
- Agent MAY: Add structured logging, implement correlation IDs, add redaction middleware, configure log rotation
- Agent MUST NEVER: Log passwords/tokens, use plain text logs, leave PII unredacted, omit stack traces
- Agent MUST ASK: Before adding new log messages that might contain PII, before changing log levels
- Agent MUST VALIDATE: Logs are JSON, correlation IDs flow through system, no PII present

## Example

**❌ Anti-pattern (String concatenation, no context, no redaction):**
```javascript
// BAD: Unstructured, concatenated
console.log('User ' + req.user.id + ' logged in at ' + new Date());

// BAD: No correlation ID
logger.info('Processing order');
logger.info('Order processed');

// BAD: Leaking PII and secrets
logger.error('Failed to connect: ' + process.env.DB_PASSWORD);
logger.info('User email: ' + user.email + ' password hash: ' + user.passwordHash);

// BAD: Expected error logged as ERROR
try {
  const user = await User.findById(userId);
} catch (e) {
  logger.error('User not found'); // WRONG level
}
```

**✅ Correct pattern (Structured JSON, correlation IDs, redacted):**
```javascript
// CORRECT: Structured JSON with context
logger.info('User login successful', {
  userId: 'user_123', // Anonymized or hashed
  correlationId: req.id,
  duration: Date.now() - req.startTime,
  timestamp: new Date().toISOString()
});

// CORRECT: Correlation ID flows through system
const requestId = req.headers['x-request-id'] || uuid();
req.correlationId = requestId;

// Pass to downstream calls
await orderService.process(order, { correlationId: requestId });

// CORRECT: Redaction middleware
logger.addRedaction([
  process.env.DB_PASSWORD,
  /\d{4}-\d{4}-\d{4}-\d{4}/, // Credit card pattern
  /@\w+\.\w+/, // Email pattern
]);

// CORRECT: Proper error logging with stack trace
try {
  const user = await User.findById(userId);
} catch (error) {
  logger.warn('User not found', {
    userId,
    correlationId: req.correlationId,
    message: error.message
    // Stack trace logged by error handler, not here
  });
}

// CORRECT: Full context on errors
logger.error('Database connection failed', {
  error: error.message, // Not the password!
  code: error.code,
  stack: error.stack,
  correlationId: req.correlationId,
  timestamp: new Date().toISOString(),
  severity: 'critical'
});
```
