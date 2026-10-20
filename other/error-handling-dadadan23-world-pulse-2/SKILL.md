---
name: "error-handling"
description: 'Implement robust error handling with exceptions, retry logic, circuit breakers, and graceful degradation. Use when designing error handling strategies, implementing retry policies, adding circuit breakers, configuring timeouts, or building health check endpoints.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
---

# Error Handling

> **Purpose**: Handle failures gracefully with logging, retries, and circuit breakers. 
> **Goal**: No silent failures, clear error messages, system resilience. 
> **Note**: For language-specific implementations, see [C# Development](../csharp/SKILL.md) or [Python Development](../python/SKILL.md).

---

## When to Use This Skill

- Designing error handling strategies
- Implementing retry policies with backoff
- Adding circuit breakers for external services
- Configuring request timeouts
- Building health check endpoints

## Prerequisites

- Understanding of exception hierarchies in target language
- Resilience library available

## Decision Tree

```
Handling an error?
+- Expected failure (validation, not-found)?
| - Return error result/status code, don't throw
+- Unexpected failure (network, I/O, timeout)?
| +- Transient? -> Retry with exponential backoff
| | - Still failing after retries? -> Circuit breaker
| - Permanent? -> Log + return error response
+- What to catch?
| +- Specific exception -> catch specific, handle specifically
| +- Base exception -> only at top-level boundaries
| - NEVER catch and swallow silently
+- Error response format?
| +- API? -> RFC 7807 Problem Details
| - UI? -> User-friendly message + log technical details
- Logging?
 - Always include: correlation ID, exception type, stack trace, context
```

## Exception Handling

### Custom Exception Types

**Define Specific Exceptions:**
```
Exception Hierarchy:
 AppException (base)
 +- ValidationException
 +- NotFoundException 
 +- UnauthorizedException
 +- ForbiddenException
 - ExternalServiceException
```

**Benefits:**
- Catch specific errors
- Provide context in exception
- Different handling per type
- Clear error messages

### Try-Catch-Finally Pattern

```
function processPayment(amount, paymentMethod):
 try:
 # Attempt operation
 validatePaymentMethod(paymentMethod)
 chargeResult = paymentGateway.charge(amount, paymentMethod)
 
 # Log success
 logger.info("Payment processed", {amount, paymentMethod})
 
 return chargeResult
 
 catch ValidationException as error:
 # Handle validation errors
 logger.warn("Invalid payment method", {error, paymentMethod})
 throw error
 
 catch NetworkException as error:
 # Handle network errors with retry
 logger.error("Payment gateway unavailable", {error})
 throw ExternalServiceException("Payment service temporarily unavailable")
 
 finally:
 # Always execute (cleanup resources)
 releasePaymentLock(paymentMethod)
```

### Global Error Handler

**Centralized Error Handling:**
```
# HTTP API Error Handler
function handleHttpError(error, request, response):
 # Log error with context
 logger.error("Request failed", {
 error: error.message,
 stack: error.stack,
 requestId: request.id,
 path: request.path,
 method: request.method
 })
 
 # Map exception to HTTP status
 statusCode = mapExceptionToStatusCode(error)
 
 # Return user-friendly response
 return response.status(statusCode).json({
 error: error.userMessage,
 requestId: request.id,
 timestamp: currentTime()
 })

function mapExceptionToStatusCode(error):
 if error is NotFoundException: return 404
 if error is ValidationException: return 400
 if error is UnauthorizedException: return 401
 if error is ForbiddenException: return 403
 if error is ExternalServiceException: return 503
 return 500 # Internal Server Error
```

---

## Common Error Handling Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| **Retry** | Transient failures | Network timeouts, rate limits |
| **Circuit Breaker** | Prevent cascading failures | External service calls |
| **Fallback** | Provide alternative | Default values, cached data |
| **Timeout** | Prevent hanging | Long-running operations |
| **Bulkhead** | Isolate resources | Separate thread pools per service |
| **Rate Limiting** | Protect from overload | API throttling |

---

## Error Handling Anti-Patterns

**[FAIL] Swallow Exceptions:**
```
try:
 riskyOperation()
catch:
 # Do nothing - ERROR! No one knows it failed
```

**[FAIL] Generic Catch-All:**
```
try:
 operation()
catch Exception:
 return null # Hides what went wrong
```

**[FAIL] Exception for Flow Control:**
```
try:
 user = database.findUser(id)
catch NotFoundException:
 # Using exceptions for normal flow - BAD
 user = createNewUser(id)
```

**[PASS] Proper Error Handling:**
```
try:
 user = database.findUser(id)
catch NotFoundException as error:
 logger.warn("User not found", {id})
 throw error # Re-throw, don't hide
catch DatabaseException as error:
 logger.error("Database error", {error, id})
 throw ServiceUnavailableException("User service temporarily unavailable")
```

---

## Resilience Patterns Summary

```
Resilience Stack (Apply Multiple Patterns):

 -------------------------------------
 | Rate Limiting (Protect your service)|
 -------------------------------------
 (down)
 -------------------------------------
 | Timeout (Prevent hanging) |
 -------------------------------------
 (down)
 -------------------------------------
 | Circuit Breaker (Fail fast) |
 -------------------------------------
 (down)
 -------------------------------------
 | Retry (Handle transient failures) |
 -------------------------------------
 (down)
 -------------------------------------
 | Fallback (Provide alternative) |
 -------------------------------------
```

---

## Resources

**Resilience Libraries:**
- **.NET**: Polly, Microsoft.Extensions.Resilience
- **Python**: tenacity, resilience4py
- **Node.js**: opossum (circuit breaker), async-retry
- **Java**: Resilience4j, Hystrix (deprecated)
- **Go**: go-resilience, go-retry

**Patterns:**
- [Microsoft Cloud Design Patterns](https://learn.microsoft.com/azure/architecture/patterns/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Release It! by Michael Nygard](https://pragprog.com/titles/mnee2/release-it-second-edition/)

---

**See Also**: [Skills.md](../../../../Skills.md) - [AGENTS.md](../../../../AGENTS.md)

**Last Updated**: January 27, 2026

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Retry storm overwhelming service | Add exponential backoff with jitter, set max retry count |
| Circuit breaker stuck open | Check half-open state configuration, verify health endpoint responds |
| Swallowed exceptions hiding bugs | Always log exceptions before fallback, use structured logging with stack traces |

## References

- [Retry Circuit Breaker](references/retry-circuit-breaker.md)
- [Fallback Logging Timeouts](references/fallback-logging-timeouts.md)