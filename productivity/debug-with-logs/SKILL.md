---
name: debug-with-logs
description: Add strategic logging and use logs for debugging issues. Use when debugging production issues, implementing observability, adding tracing, or.
---

# Debug with Logs

Add strategic logging statements and use log analysis techniques to debug issues effectively. This skill covers logging best practices, log levels, structured logging, and debugging workflows.

## When to Use This Skill

Use this skill when you need to:

- Debug production issues
- Trace execution flow
- Understand system behavior
- Implement observability
- Add logging to new code
- Analyze existing logs
- Troubleshoot intermittent bugs

**Trigger phrases**: "debug with logs", "add logging", "trace execution", "log analysis", "debug production", "add observability"

## What This Skill Does

### Log Levels

| Level | Use Case | Example |
|-------|----------|---------|
| DEBUG | Detailed diagnostic info | Variable values, loop iterations |
| INFO | General operational events | Request received, task completed |
| WARNING | Potential issues | Deprecated API, slow query |
| ERROR | Errors that need attention | Failed operation, exception |
| CRITICAL | System-breaking errors | Database down, out of memory |

## Instructions

### Step 1: Identify Debug Points

Determine where to add logs:

```
Entry Points:
- Function entry with parameters
- API endpoint handlers
- Event listeners
- Background job starts

Exit Points:
- Function return with result
- API response sent
- Task completion
- Error handling

Decision Points:
- Conditional branches
- Loop iterations
- External API calls
- Database queries
```

### Step 2: Add Strategic Logging

#### Python

```python
import logging
import json
import time
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def log_function_call(func):
    """Decorator to log function entry and exit."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"Entering {func.__name__} with args={args}, kwargs={kwargs}")
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.debug(f"Exiting {func.__name__} with result={result} (took {duration:.3f}s)")
            return result
        except Exception as e:
            logger.error(f"Exception in {func.__name__}: {e}", exc_info=True)
            raise
    return wrapper

@log_function_call
def process_order(order_id: str, items: list) -> dict:
    """Process an order with detailed logging."""
    logger.info(f"Processing order {order_id} with {len(items)} items")

    # Log decision points
    if not items:
        logger.warning(f"Order {order_id} has no items")
        return {"status": "empty"}

    total = 0
    for i, item in enumerate(items):
        logger.debug(f"Processing item {i+1}/{len(items)}: {item}")
        total += item.get("price", 0)

    logger.info(f"Order {order_id} total: ${total}")
    return {"status": "processed", "total": total}
```

#### JavaScript/TypeScript

```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: 'debug',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'app.log' })
  ]
});

function logFunctionCall<T extends (...args: any[]) => any>(
  fn: T,
  fnName: string
): T {
  return ((...args: Parameters<T>): ReturnType<T> => {
    logger.debug(`Entering ${fnName}`, { args });
    const startTime = Date.now();

    try {
      const result = fn(...args);
      const duration = Date.now() - startTime;
      logger.debug(`Exiting ${fnName}`, { result, duration: `${duration}ms` });
      return result;
    } catch (error) {
      logger.error(`Exception in ${fnName}`, { error });
      throw error;
    }
  }) as T;
}

async function processOrder(orderId: string, items: Item[]): Promise<OrderResult> {
  logger.info('Processing order', { orderId, itemCount: items.length });

  if (!items.length) {
    logger.warn('Order has no items', { orderId });
    return { status: 'empty' };
  }

  let total = 0;
  for (const [index, item] of items.entries()) {
    logger.debug(`Processing item`, { index: index + 1, total: items.length, item });
    total += item.price ?? 0;
  }

  logger.info('Order processed', { orderId, total });
  return { status: 'processed', total };
}
```

#### Java

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class OrderService {
    private static final Logger logger = LoggerFactory.getLogger(OrderService.class);

    public OrderResult processOrder(String orderId, List<Item> items) {
        logger.info("Processing order {} with {} items", orderId, items.size());

        if (items.isEmpty()) {
            logger.warn("Order {} has no items", orderId);
            return new OrderResult("empty", 0);
        }

        double total = 0;
        for (int i = 0; i < items.size(); i++) {
            Item item = items.get(i);
            logger.debug("Processing item {}/{}: {}", i + 1, items.size(), item);
            total += item.getPrice();
        }

        logger.info("Order {} processed with total: ${}", orderId, total);
        return new OrderResult("processed", total);
    }
}
```

### Step 3: Use Structured Logging

Structured logs are easier to search and analyze:

```python
import json
import logging

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

    def log(self, level: str, message: str, **context):
        """Log with structured context."""
        log_entry = {
            "message": message,
            **context
        }
        getattr(self.logger, level)(json.dumps(log_entry))

    def info(self, message: str, **context):
        self.log("info", message, **context)

    def error(self, message: str, **context):
        self.log("error", message, **context)

# Usage
logger = StructuredLogger(__name__)
logger.info("Order processed",
    order_id="ORD-123",
    customer_id="CUST-456",
    total=99.99,
    items_count=3
)

# Output:
# {"message": "Order processed", "order_id": "ORD-123", "customer_id": "CUST-456", "total": 99.99, "items_count": 3}
```

### Step 4: Debug Workflow

#### 1. Reproduce the Issue

```bash
# Run with debug logging enabled
DEBUG=* node app.js
# or
LOG_LEVEL=DEBUG python app.py
```

#### 2. Identify the Scope

```bash
# Filter logs by component
grep "OrderService" app.log

# Filter by time range
grep "2025-01-15T14:" app.log

# Filter by log level
grep "ERROR" app.log
```

#### 3. Trace Execution

```bash
# Find a specific request
grep "request_id=abc123" app.log

# Follow the flow
grep -E "(Entering|Exiting)" app.log | head -20
```

#### 4. Add Temporary Debug Logs

```python
# Add detailed logging to suspect area
def suspicious_function(data):
    logger.debug(f"Input data type: {type(data)}")
    logger.debug(f"Input data value: {data}")
    logger.debug(f"Input data keys: {data.keys() if hasattr(data, 'keys') else 'N/A'}")

    result = process(data)

    logger.debug(f"Result type: {type(result)}")
    logger.debug(f"Result value: {result}")

    return result
```

### Step 5: Production-Safe Debugging

```python
import os

class ConditionalLogger:
    """Logger that can enable verbose logging per-request."""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.verbose = os.getenv("VERBOSE_LOGGING", "false").lower() == "true"

    def debug(self, message: str, **context):
        """Only log debug in verbose mode."""
        if self.verbose:
            self.logger.debug(message, extra=context)

    def trace(self, message: str, request_id: str = None, **context):
        """Trace specific requests without enabling global debug."""
        traced_requests = os.getenv("TRACE_REQUESTS", "").split(",")
        if request_id in traced_requests:
            self.logger.info(f"[TRACE] {message}", extra=context)
```

### Step 6: Log Analysis Commands

```bash
# Count errors by type
grep "ERROR" app.log | cut -d: -f4 | sort | uniq -c | sort -rn

# Find slow operations
grep "duration" app.log | awk -F'"duration":' '{print $2}' | sort -n | tail -10

# Track error rate over time
grep "ERROR" app.log | cut -d' ' -f1 | cut -d'T' -f1 | uniq -c

# Find correlated logs
grep "correlation_id=abc123" app.log

# Tail with filtering
tail -f app.log | grep --line-buffered "ERROR\|WARN"
```

## Logging Best Practices

### Do's

```python
# Log with context
logger.info("User logged in", extra={"user_id": user_id, "ip": ip_address})

# Log exceptions with stack trace
try:
    process()
except Exception as e:
    logger.error("Processing failed", exc_info=True)

# Use appropriate levels
logger.debug("Cache hit for key: %s", key)      # Development
logger.info("Request processed in %dms", ms)    # Operations
logger.warning("Rate limit approaching: %d%%", pct)  # Attention
logger.error("Database connection failed: %s", err)  # Action needed
```

### Don'ts

```python
# Don't log sensitive data
logger.info(f"Password: {password}")  # NEVER!
logger.info(f"Token: {token}")  # NEVER!

# Don't log at wrong level
logger.error("Processing started")  # Should be INFO

# Don't use print for logging
print("Debug: " + str(data))  # Use logger instead

# Don't log too much in loops
for item in items:  # Could be millions
    logger.debug(f"Processing {item}")  # Log batch instead
```

## Debugging Checklist

- [ ] Identified the issue scope (which component/flow)
- [ ] Added entry/exit logs to suspect functions
- [ ] Added logs at decision points (if/else, loops)
- [ ] Added logs before/after external calls
- [ ] Included correlation IDs for request tracing
- [ ] Used appropriate log levels
- [ ] Avoided logging sensitive data
- [ ] Tested log output is useful
- [ ] Cleaned up verbose logs after debugging

## Quality Checklist

- [ ] Logs follow structured format
- [ ] Correlation IDs enable request tracing
- [ ] Log levels are appropriate
- [ ] No sensitive data in logs
- [ ] Logs are actionable
- [ ] Performance impact is minimal
- [ ] Log retention policy defined

## Related Skills

- `performance-review` - Performance analysis
- `security-review` - Security logging requirements
- `testing-review` - Test debugging

---

**Version**: 1.0.0
**Last Updated**: December 2025


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
