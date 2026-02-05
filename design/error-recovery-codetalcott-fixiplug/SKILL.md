---
name: "error-recovery"
description: "Master error handling and recovery patterns for robust agent workflows. Learn retry strategies, timeout handling, optimistic updates with rollback, circuit breakers, and graceful degradation. Essential for production-ready agents."
tags:
  - "error-handling"
  - "retry-logic"
  - "timeout"
  - "circuit-breaker"
  - "resilience"
  - "fallback"
  - "graceful-degradation"
  - "production-ready"
version: "1.0.0"
level: "advanced"
author: "FixiPlug Team"
references:
  - "stateTrackerPlugin"
  - "agentCommands"
  - "fixiAgentPlugin"
  - "tablePlugin"
  - "formSchemaPlugin"
---

# Error Handling and Recovery Skill

## Overview

Building robust agents requires **anticipating and handling failures** gracefully. This skill teaches you proven error recovery patterns for network errors, timeouts, validation failures, and race conditions.

**Key Principle**: Expect failures, handle them elegantly, recover automatically when possible.

**What You'll Master**:
1. **Retry with Exponential Backoff** - Retry failed operations with increasing delays
2. **Timeout Handling** - Detect and recover from hung operations
3. **Optimistic Updates with Rollback** - Update UI immediately, rollback on error
4. **Circuit Breaker Pattern** - Stop calling failing services
5. **Graceful Degradation** - Provide fallback functionality
6. **Error State Management** - Track and communicate errors to users

---

## Pattern 1: Retry with Exponential Backoff

**Goal**: Retry failed operations with increasing delays to avoid overwhelming servers

### Basic Implementation

```javascript
async function retryWithBackoff(operation, options = {}) {
  const {
    maxRetries = 3,
    initialDelay = 1000,
    maxDelay = 10000,
    backoffMultiplier = 2,
    retryableErrors = ['NetworkError', 'TimeoutError', '503', '504']
  } = options;

  let delay = initialDelay;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      // Track retry state
      await fixiplug.dispatch('api:setState', {
        state: 'retrying',
        data: {
          attempt,
          maxRetries,
          nextDelay: delay
        }
      });

      // Execute operation
      const result = await operation();

      // Success - clear retry state
      await fixiplug.dispatch('api:setState', {
        state: 'success',
        data: { retriesUsed: attempt - 1 }
      });

      return result;

    } catch (error) {
      console.error(`Attempt ${attempt} failed:`, error);

      // Check if error is retryable
      const isRetryable = retryableErrors.some(pattern =>
        error.message.includes(pattern) ||
        error.statusCode?.toString().includes(pattern)
      );

      if (!isRetryable) {
        // Non-retryable error - fail immediately
        await fixiplug.dispatch('api:setState', {
          state: 'error',
          data: { error: error.message, retryable: false }
        });
        throw error;
      }

      // Last attempt failed
      if (attempt === maxRetries) {
        await fixiplug.dispatch('api:setState', {
          state: 'max-retries-exceeded',
          data: {
            error: error.message,
            attempts: maxRetries
          }
        });
        throw new Error(`Operation failed after ${maxRetries} retries: ${error.message}`);
      }

      // Wait before next retry
      console.log(`Retrying in ${delay}ms...`);
      await new Promise(resolve => setTimeout(resolve, delay));

      // Increase delay (exponential backoff)
      delay = Math.min(delay * backoffMultiplier, maxDelay);
    }
  }
}
```

### Usage Example: Retry Table Load

```javascript
async function loadTableWithRetry(endpoint) {
  return await retryWithBackoff(async () => {
    // Inject table
    await fixiplug.dispatch('api:injectFxHtml', {
      html: `<div fx-table fx-action="${endpoint}" fx-trigger="load"></div>`,
      selector: '#app'
    });

    // Wait for success
    return await fixiplug.dispatch('api:waitForState', {
      state: 'table-ready',
      timeout: 5000
    });
  }, {
    maxRetries: 3,
    initialDelay: 1000,
    backoffMultiplier: 2
  });
}

// Usage
try {
  await loadTableWithRetry('/api/products/');
  console.log('Table loaded successfully');
} catch (error) {
  console.error('Failed to load table:', error);
  // Show error UI
}
```

---

## Pattern 2: Timeout Handling

**Goal**: Detect and recover from operations that hang indefinitely

### Timeout Wrapper

```javascript
async function withTimeout(promise, timeoutMs, operationName = 'Operation') {
  let timeoutId;

  const timeoutPromise = new Promise((_, reject) => {
    timeoutId = setTimeout(() => {
      reject(new Error(`${operationName} timed out after ${timeoutMs}ms`));
    }, timeoutMs);
  });

  try {
    // Track timeout state
    await fixiplug.dispatch('api:setState', {
      state: 'operation-started',
      data: {
        operation: operationName,
        timeout: timeoutMs,
        startTime: Date.now()
      }
    });

    // Race: operation vs timeout
    const result = await Promise.race([promise, timeoutPromise]);

    // Success
    await fixiplug.dispatch('api:setState', {
      state: 'operation-completed',
      data: {
        operation: operationName,
        duration: Date.now() - Date.now()
      }
    });

    return result;

  } catch (error) {
    if (error.message.includes('timed out')) {
      // Timeout occurred
      await fixiplug.dispatch('api:setState', {
        state: 'operation-timeout',
        data: {
          operation: operationName,
          timeout: timeoutMs
        }
      });
    }
    throw error;

  } finally {
    clearTimeout(timeoutId);
  }
}
```

### Usage Example: Form Submission with Timeout

```javascript
async function submitFormWithTimeout(form, data) {
  try {
    // Validate
    const validation = await withTimeout(
      fixiplug.dispatch('api:validateFormData', { form, data }),
      3000,
      'Form Validation'
    );

    if (!validation.valid) {
      throw new Error('Validation failed: ' + JSON.stringify(validation.errors));
    }

    // Fill form
    await withTimeout(
      fixiplug.dispatch('agent:fillForm', { form, data }),
      5000,
      'Form Fill'
    );

    // Submit
    await withTimeout(
      fixiplug.dispatch('agent:clickButton', { text: 'Submit' }),
      10000,
      'Form Submission'
    );

    // Wait for success
    await withTimeout(
      fixiplug.dispatch('api:waitForState', { state: 'form-submitted' }),
      5000,
      'Submission Confirmation'
    );

    console.log('Form submitted successfully');

  } catch (error) {
    if (error.message.includes('timed out')) {
      console.error('Operation timed out:', error.message);

      // Retry or show error to user
      const retry = confirm('Operation timed out. Retry?');
      if (retry) {
        return await submitFormWithTimeout(form, data);
      }
    } else {
      console.error('Submission failed:', error);
    }

    throw error;
  }
}
```

---

## Pattern 3: Optimistic Updates with Rollback

**Goal**: Update UI immediately for responsiveness, rollback if server rejects

### Optimistic Update Pattern

```javascript
async function optimisticUpdate(operation, uiUpdate, rollback) {
  // 1. Save current state
  const previousState = await fixiplug.dispatch('api:getCurrentState');

  try {
    // 2. Apply optimistic UI update immediately
    await fixiplug.dispatch('api:setState', {
      state: 'optimistic-update',
      data: { previousState: previousState.data }
    });

    await uiUpdate();

    console.log('UI updated optimistically');

    // 3. Perform actual operation (async)
    const result = await operation();

    // 4. Confirm success
    await fixiplug.dispatch('api:setState', {
      state: 'update-confirmed',
      data: { result }
    });

    console.log('Server confirmed update');

    return result;

  } catch (error) {
    console.error('Optimistic update failed:', error);

    // 5. Rollback UI to previous state
    await fixiplug.dispatch('api:setState', {
      state: 'rollback',
      data: { error: error.message }
    });

    await rollback(previousState);

    console.log('UI rolled back to previous state');

    // 6. Show error to user
    await fixiplug.dispatch('api:setState', {
      state: 'update-failed',
      data: { error: error.message }
    });

    throw error;
  }
}
```

### Usage Example: Optimistic Table Cell Update

```javascript
async function updateCellOptimistically(rowId, column, newValue) {
  // Find the cell element
  const cell = document.querySelector(`tr[data-row-id="${rowId}"] td[data-column="${column}"]`);
  const oldValue = cell.getAttribute('data-value');

  await optimisticUpdate(
    // Operation: send PATCH to server
    async () => {
      const response = await fetch(`/api/products/${rowId}/`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ column, value: newValue })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Update failed');
      }

      return await response.json();
    },

    // UI Update: change cell immediately
    async () => {
      cell.textContent = newValue;
      cell.setAttribute('data-value', newValue);
      cell.classList.add('optimistic-update');
    },

    // Rollback: restore old value
    async (previousState) => {
      cell.textContent = oldValue;
      cell.setAttribute('data-value', oldValue);
      cell.classList.remove('optimistic-update');
      cell.classList.add('update-failed');

      // Remove error class after 2s
      setTimeout(() => cell.classList.remove('update-failed'), 2000);
    }
  );
}

// Usage
try {
  await updateCellOptimistically(1, 'price', 999.99);
} catch (error) {
  console.error('Cell update failed and rolled back');
}
```

---

## Pattern 4: Circuit Breaker

**Goal**: Stop calling a failing service to prevent cascading failures

### Circuit Breaker Implementation

```javascript
class CircuitBreaker {
  constructor(options = {}) {
    this.failureThreshold = options.failureThreshold || 5;
    this.resetTimeout = options.resetTimeout || 60000; // 1 minute
    this.monitoringPeriod = options.monitoringPeriod || 10000; // 10 seconds

    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
    this.failures = 0;
    this.lastFailureTime = null;
    this.successCount = 0;
  }

  async execute(operation, fallback) {
    // Check circuit state
    if (this.state === 'OPEN') {
      // Circuit is open - check if we should try again
      if (Date.now() - this.lastFailureTime > this.resetTimeout) {
        console.log('Circuit breaker entering HALF_OPEN state');
        this.state = 'HALF_OPEN';
        this.successCount = 0;
      } else {
        console.log('Circuit breaker is OPEN - using fallback');

        await fixiplug.dispatch('api:setState', {
          state: 'circuit-open',
          data: {
            failures: this.failures,
            lastFailure: this.lastFailureTime
          }
        });

        return await fallback();
      }
    }

    try {
      // Execute operation
      const result = await operation();

      // Success
      this.onSuccess();

      return result;

    } catch (error) {
      // Failure
      this.onFailure();

      if (this.state === 'OPEN') {
        console.log('Circuit breaker is now OPEN - using fallback');
        return await fallback();
      }

      throw error;
    }
  }

  onSuccess() {
    this.failures = 0;

    if (this.state === 'HALF_OPEN') {
      this.successCount++;

      // After 3 successes in HALF_OPEN, close the circuit
      if (this.successCount >= 3) {
        console.log('Circuit breaker closing (recovered)');
        this.state = 'CLOSED';

        fixiplug.dispatch('api:setState', {
          state: 'circuit-closed',
          data: { message: 'Service recovered' }
        });
      }
    }
  }

  onFailure() {
    this.failures++;
    this.lastFailureTime = Date.now();

    if (this.failures >= this.failureThreshold) {
      console.log(`Circuit breaker opening after ${this.failures} failures`);
      this.state = 'OPEN';

      fixiplug.dispatch('api:setState', {
        state: 'circuit-opened',
        data: {
          failures: this.failures,
          threshold: this.failureThreshold
        }
      });
    }
  }
}
```

### Usage Example: Protected API Calls

```javascript
const apiCircuitBreaker = new CircuitBreaker({
  failureThreshold: 5,
  resetTimeout: 60000
});

async function fetchProductsWithCircuitBreaker() {
  return await apiCircuitBreaker.execute(
    // Primary operation
    async () => {
      const response = await fetch('/api/products/');

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      return await response.json();
    },

    // Fallback when circuit is open
    async () => {
      console.log('Using cached data (circuit is open)');

      // Return cached data or empty state
      return {
        data: JSON.parse(localStorage.getItem('products_cache') || '[]'),
        cached: true
      };
    }
  );
}

// Usage
try {
  const products = await fetchProductsWithCircuitBreaker();

  if (products.cached) {
    console.log('Showing cached data');
  } else {
    console.log('Showing fresh data');
    localStorage.setItem('products_cache', JSON.stringify(products.data));
  }
} catch (error) {
  console.error('Failed to fetch products:', error);
}
```

---

## Pattern 5: Graceful Degradation

**Goal**: Provide reduced functionality when primary features fail

### Degradation Strategy

```javascript
async function loadDataWithDegradation(endpoint, options = {}) {
  const {
    enableSorting = true,
    enableSearch = true,
    enablePagination = true,
    fallbackData = []
  } = options;

  try {
    // Try full-featured load
    await fixiplug.dispatch('api:injectFxHtml', {
      html: `
        <div fx-table
             fx-action="${endpoint}"
             fx-trigger="load"
             ${enableSorting ? 'fx-table-sortable' : ''}
             ${enableSearch ? 'fx-table-search' : ''}
             ${enablePagination ? 'fx-page-size="20"' : ''}>
        </div>
      `,
      selector: '#app'
    });

    // Wait for load
    await withTimeout(
      fixiplug.dispatch('api:waitForState', { state: 'table-ready' }),
      5000,
      'Table Load'
    );

    console.log('Full-featured table loaded');

  } catch (error) {
    console.error('Full load failed, trying basic mode:', error);

    try {
      // Degrade: Load table without advanced features
      await fixiplug.dispatch('api:injectFxHtml', {
        html: `
          <div fx-table
               fx-action="${endpoint}"
               fx-trigger="load">
          </div>
        `,
        selector: '#app'
      });

      await withTimeout(
        fixiplug.dispatch('api:waitForState', { state: 'table-ready' }),
        5000,
        'Basic Table Load'
      );

      console.log('Basic table loaded (degraded mode)');

      await fixiplug.dispatch('api:setState', {
        state: 'degraded-mode',
        data: { message: 'Some features unavailable' }
      });

    } catch (secondError) {
      console.error('Basic load failed, using fallback data:', secondError);

      // Final fallback: Static data
      await fixiplug.dispatch('api:injectFxHtml', {
        html: `
          <div id="static-table">
            <p>Unable to load live data. Showing cached data:</p>
            <ul>
              ${fallbackData.map(item => `<li>${JSON.stringify(item)}</li>`).join('')}
            </ul>
          </div>
        `,
        selector: '#app'
      });

      await fixiplug.dispatch('api:setState', {
        state: 'offline-mode',
        data: { message: 'Showing cached data only' }
      });

      console.log('Showing static fallback data');
    }
  }
}
```

---

## Pattern 6: Error State Management

**Goal**: Track errors and communicate them to users effectively

### Error State Tracker

```javascript
class ErrorStateManager {
  constructor() {
    this.errors = [];
    this.maxErrors = 10;
  }

  async recordError(error, context = {}) {
    const errorRecord = {
      id: Date.now(),
      message: error.message,
      stack: error.stack,
      context,
      timestamp: new Date().toISOString(),
      recovered: false
    };

    this.errors.push(errorRecord);

    // Keep only recent errors
    if (this.errors.length > this.maxErrors) {
      this.errors.shift();
    }

    // Update state
    await fixiplug.dispatch('api:setState', {
      state: 'error',
      data: {
        error: errorRecord,
        recentErrors: this.errors.slice(-3)
      }
    });

    // Log to console
    console.error(`[Error ${errorRecord.id}]`, error);

    return errorRecord;
  }

  async markRecovered(errorId) {
    const error = this.errors.find(e => e.id === errorId);

    if (error) {
      error.recovered = true;
      error.recoveredAt = new Date().toISOString();

      await fixiplug.dispatch('api:setState', {
        state: 'error-recovered',
        data: { errorId, recoveredAt: error.recoveredAt }
      });
    }
  }

  getRecentErrors() {
    return this.errors.slice(-5);
  }

  hasUnrecoveredErrors() {
    return this.errors.some(e => !e.recovered);
  }
}

const errorManager = new ErrorStateManager();
```

### Usage: Error Tracking in Workflow

```javascript
async function safeWorkflow() {
  try {
    // Step 1
    await performStep1();

    // Step 2
    await performStep2();

    // Step 3
    await performStep3();

  } catch (error) {
    // Record error with context
    const errorRecord = await errorManager.recordError(error, {
      workflow: 'safeWorkflow',
      step: 'performStep2',
      user: 'current-user'
    });

    // Try recovery
    try {
      await recoverFromError(errorRecord);

      // Mark as recovered
      await errorManager.markRecovered(errorRecord.id);

      console.log('Workflow recovered successfully');

    } catch (recoveryError) {
      // Recovery failed
      console.error('Recovery failed:', recoveryError);

      // Show error to user
      await showErrorUI(errorRecord);
    }
  }
}

async function showErrorUI(errorRecord) {
  await fixiplug.dispatch('api:injectFxHtml', {
    html: `
      <div class="error-banner">
        <strong>Error:</strong> ${errorRecord.message}
        <button onclick="retryOperation()">Retry</button>
        <button onclick="dismissError()">Dismiss</button>
      </div>
    `,
    selector: '#notifications',
    position: 'afterbegin'
  });
}
```

---

## Best Practices

### ✅ DO

1. **Always set timeouts for async operations**
```javascript
await withTimeout(operation(), 5000, 'Operation Name');
```

2. **Use exponential backoff for retries**
```javascript
await retryWithBackoff(operation, { maxRetries: 3, initialDelay: 1000 });
```

3. **Track error state for user communication**
```javascript
await errorManager.recordError(error, { context: 'form-submission' });
```

4. **Provide fallback data/functionality**
```javascript
return cachedData || defaultData || { message: 'No data available' };
```

5. **Use circuit breakers for external services**
```javascript
await circuitBreaker.execute(apiCall, fallback);
```

### ❌ DON'T

1. **Don't retry indefinitely**
```javascript
// Bad
while (true) {
  try { await operation(); break; } catch (e) { }
}

// Good
await retryWithBackoff(operation, { maxRetries: 3 });
```

2. **Don't ignore timeout errors**
```javascript
// Bad
try { await operation(); } catch (e) { }

// Good
try {
  await withTimeout(operation(), 5000);
} catch (e) {
  if (e.message.includes('timed out')) {
    // Handle timeout specifically
  }
}
```

3. **Don't let errors crash the app**
```javascript
// Bad
const data = await fetch('/api/data').then(r => r.json());

// Good
try {
  const data = await fetch('/api/data').then(r => r.json());
} catch (error) {
  await errorManager.recordError(error);
  return fallbackData;
}
```

4. **Don't retry non-retryable errors** (400, 401, 403, 404)
```javascript
const retryableErrors = ['NetworkError', '503', '504', 'TimeoutError'];
```

---

## Summary

This skill teaches you to:

1. **Retry with exponential backoff** - Automatically retry transient failures
2. **Handle timeouts** - Detect and recover from hung operations
3. **Optimistic updates** - Responsive UI with automatic rollback
4. **Circuit breakers** - Protect against cascading failures
5. **Graceful degradation** - Provide reduced functionality when needed
6. **Error state management** - Track and communicate errors effectively

**Remember**: Production agents must handle failures gracefully. Always implement retry logic, timeouts, and fallbacks.

