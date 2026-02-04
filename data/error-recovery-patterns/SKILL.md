---
name: error-recovery-patterns
description: Error recovery and failure handling patterns for distributed systems including rollback strategies, circuit breakers, retry logic with exponential backoff, graceful degradation, and compensating transactions. Activates when task execution fails, timeouts occur, external services fail, database transactions fail, or cascade failure risks are detected. Use when recovering from failures, preventing data corruption, implementing resilience patterns, or handling partial system failures.
---

# Error Recovery Patterns

## Overview

When systems fail, how you recover determines the difference between a minor hiccup and a catastrophic outage. This skill provides systematic approaches to error recovery, failure handling, and resilience patterns.

**When to use this skill:**
- Task execution fails with errors
- Timeouts or external service failures detected
- Database transaction failures occur
- Risk of cascading failures across systems
- Need to maintain data consistency during failures
- Implementing resilience for distributed systems

---

## Quick Diagnosis Framework

### 1. Classify the Failure

**Transient vs Permanent:**
- **Transient**: Temporary issue, likely to succeed on retry (network blip, timeout, rate limit)
- **Permanent**: Fundamental issue, won't succeed without intervention (invalid input, missing resource, configuration error)

**Recoverable vs Fatal:**
- **Recoverable**: Can restore to consistent state (retry, rollback, compensating transaction)
- **Fatal**: Cannot recover automatically (data corruption, invariant violation, critical dependency failure)

**Scope:**
- **Local**: Single operation failure
- **Distributed**: Multiple service failure
- **Cascading**: Failure spreading across system boundaries

### 2. Select Recovery Strategy

| Failure Type | Recovery Strategy | Pattern to Use |
|--------------|------------------|----------------|
| Transient + Recoverable | Retry with backoff | Exponential backoff, jitter |
| Transient + Service failure | Circuit breaker | Open/half-open/closed states |
| Permanent + Recoverable | Rollback or compensate | Transaction rollback, saga pattern |
| Permanent + Fatal | Fail gracefully | Graceful degradation, fallback |
| Distributed + Transient | Retry with timeout | Distributed timeout, bulkhead |
| Distributed + Permanent | Compensating transaction | Saga pattern, event sourcing |
| Cascading risk | Prevent cascade | Circuit breaker, rate limiting |

---

## Core Recovery Patterns

### Pattern 1: Retry with Exponential Backoff

**When to use:**
- Transient failures (network timeouts, temporary service unavailability)
- Rate limiting (429 responses)
- Database connection pool exhaustion

**Implementation approach:**
```python
# Exponential backoff with jitter
def retry_with_backoff(func, max_retries=5, base_delay=1, max_delay=60):
    """
    Retry with exponential backoff and jitter.

    Args:
        func: Function to retry
        max_retries: Maximum retry attempts (default 5)
        base_delay: Initial delay in seconds (default 1)
        max_delay: Maximum delay in seconds (default 60)
    """
    for attempt in range(max_retries):
        try:
            return func()
        except TransientError as e:
            if attempt == max_retries - 1:
                raise  # Final attempt, re-raise

            # Exponential backoff: 1s, 2s, 4s, 8s, 16s...
            delay = min(base_delay * (2 ** attempt), max_delay)

            # Add jitter (±25%) to prevent thundering herd
            jitter = delay * 0.25 * (2 * random.random() - 1)
            actual_delay = delay + jitter

            logger.warning(f"Transient error on attempt {attempt + 1}, "
                         f"retrying in {actual_delay:.2f}s: {e}")
            time.sleep(actual_delay)
```

**Key principles:**
- **Exponential backoff**: Double delay each retry (1s → 2s → 4s → 8s)
- **Max delay cap**: Prevent excessive wait times (typically 60s)
- **Jitter**: Add randomness (±25%) to prevent thundering herd problem
- **Max retries**: Limit attempts (typically 3-5) to prevent infinite loops
- **Idempotency**: Ensure retries are safe (use idempotency keys)

**When NOT to use:**
- Permanent failures (invalid input, missing resources)
- User-interactive operations (don't make users wait)
- Write operations without idempotency guarantees

---

### Pattern 2: Circuit Breaker

**When to use:**
- Repeated failures to external service
- Protecting downstream services from overload
- Preventing cascading failures
- Fast-failing when service is known to be down

**Implementation approach:**
```python
class CircuitBreaker:
    """
    Circuit breaker pattern with three states:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Failures exceeded threshold, requests fail fast
    - HALF_OPEN: Testing if service recovered
    """
    def __init__(self, failure_threshold=5, timeout=60, success_threshold=2):
        self.failure_threshold = failure_threshold  # Failures before opening
        self.timeout = timeout  # Seconds before trying again (half-open)
        self.success_threshold = success_threshold  # Successes to close

        self.failure_count = 0
        self.success_count = 0
        self.state = "CLOSED"
        self.opened_at = None

    def call(self, func):
        """Execute function through circuit breaker."""
        if self.state == "OPEN":
            # Check if timeout elapsed
            if time.time() - self.opened_at >= self.timeout:
                self.state = "HALF_OPEN"
                self.success_count = 0
                logger.info("Circuit breaker entering HALF_OPEN state")
            else:
                raise CircuitBreakerOpenError("Circuit breaker is OPEN")

        try:
            result = func()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        """Handle successful call."""
        self.failure_count = 0

        if self.state == "HALF_OPEN":
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = "CLOSED"
                logger.info("Circuit breaker CLOSED (service recovered)")

    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1

        if self.state == "HALF_OPEN":
            # Failure in half-open state, reopen circuit
            self.state = "OPEN"
            self.opened_at = time.time()
            logger.warning("Circuit breaker OPEN (half-open test failed)")

        elif self.failure_count >= self.failure_threshold:
            # Threshold exceeded, open circuit
            self.state = "OPEN"
            self.opened_at = time.time()
            logger.error(f"Circuit breaker OPEN ({self.failure_count} failures)")
```

**Key principles:**
- **CLOSED state**: Normal operation, track failures
- **OPEN state**: Fast-fail without calling service (save resources)
- **HALF_OPEN state**: Test if service recovered (limited requests)
- **Failure threshold**: Open after N consecutive failures (typically 5-10)
- **Timeout**: Try again after N seconds (typically 30-60s)
- **Success threshold**: Close after N successes in half-open (typically 2-3)

**Monitoring:**
- Track state transitions (CLOSED → OPEN is critical alert)
- Monitor failure rate before opening
- Alert on circuit breaker open events
- Dashboard: show circuit breaker states across services

---

### Pattern 3: Transaction Rollback

**When to use:**
- Database transaction failures
- Multi-step operations where consistency required
- ACID transactions (single database)
- Failures during data modification

**Implementation approach:**
```python
def transfer_funds(from_account, to_account, amount):
    """
    Transfer funds with automatic rollback on failure.
    Demonstrates transaction rollback pattern.
    """
    with db.transaction():  # Automatically rolls back on exception
        try:
            # Step 1: Debit source account
            from_balance = db.get_balance(from_account)
            if from_balance < amount:
                raise InsufficientFundsError(f"Balance {from_balance} < {amount}")

            db.debit(from_account, amount)
            logger.info(f"Debited {amount} from {from_account}")

            # Step 2: Credit destination account
            db.credit(to_account, amount)
            logger.info(f"Credited {amount} to {to_account}")

            # Step 3: Record transaction
            db.record_transaction(from_account, to_account, amount, timestamp=now())
            logger.info(f"Recorded transaction {from_account} → {to_account}")

            # All steps succeeded, commit
            return TransactionResult(success=True, transaction_id=...)

        except Exception as e:
            # Any failure triggers automatic rollback
            logger.error(f"Transaction failed, rolling back: {e}")
            # with statement handles rollback automatically
            raise TransactionFailedError(f"Transfer failed: {e}") from e
```

**Key principles:**
- **All-or-nothing**: Either all steps succeed or none do
- **Automatic rollback**: Use database transaction context managers
- **Idempotency**: Safe to retry entire transaction
- **Logging**: Log each step for debugging rolled-back transactions
- **Isolation**: Prevent dirty reads during transaction

**When NOT to use:**
- Distributed systems (multiple databases) - use saga pattern instead
- Long-running operations (locks held too long)
- Operations with external side effects (APIs, file writes)

---

### Pattern 4: Compensating Transaction (Saga Pattern)

**When to use:**
- Distributed systems (multiple services/databases)
- Long-running business processes
- Cannot use traditional transactions (no ACID across services)
- Need eventual consistency

**Implementation approach:**
```python
class BookingWorkflow:
    """
    Hotel booking saga with compensating transactions.
    Steps: Reserve hotel → Charge payment → Send confirmation
    Compensations: Cancel reservation ← Refund payment ← Cancel email
    """
    def execute(self, booking_request):
        """Execute saga with automatic compensation on failure."""
        executed_steps = []

        try:
            # Step 1: Reserve hotel room
            reservation = self.hotel_service.reserve_room(
                booking_request.hotel_id,
                booking_request.dates
            )
            executed_steps.append(("reserve_room", reservation.id))
            logger.info(f"Reserved room {reservation.id}")

            # Step 2: Charge payment
            payment = self.payment_service.charge(
                booking_request.card,
                booking_request.amount
            )
            executed_steps.append(("charge_payment", payment.id))
            logger.info(f"Charged payment {payment.id}")

            # Step 3: Send confirmation email
            email = self.email_service.send_confirmation(
                booking_request.email,
                reservation,
                payment
            )
            executed_steps.append(("send_email", email.id))
            logger.info(f"Sent confirmation {email.id}")

            # All steps succeeded
            return BookingResult(success=True, reservation_id=reservation.id)

        except Exception as e:
            # Failure occurred, compensate executed steps in reverse order
            logger.error(f"Booking failed at step {len(executed_steps)}, "
                        f"compensating: {e}")

            self._compensate(executed_steps)

            raise BookingFailedError(f"Booking failed: {e}") from e

    def _compensate(self, executed_steps):
        """Execute compensating transactions in reverse order."""
        for step_name, step_id in reversed(executed_steps):
            try:
                if step_name == "reserve_room":
                    self.hotel_service.cancel_reservation(step_id)
                    logger.info(f"Compensated: cancelled reservation {step_id}")

                elif step_name == "charge_payment":
                    self.payment_service.refund(step_id)
                    logger.info(f"Compensated: refunded payment {step_id}")

                elif step_name == "send_email":
                    self.email_service.send_cancellation(step_id)
                    logger.info(f"Compensated: sent cancellation {step_id}")

            except Exception as comp_error:
                # Compensation failed - critical error requiring manual intervention
                logger.critical(f"COMPENSATION FAILED for {step_name} {step_id}: "
                              f"{comp_error}")
                # Alert operations team
                self.alert_service.critical_alert(
                    f"Manual intervention required: compensation failed",
                    details={"step": step_name, "id": step_id, "error": comp_error}
                )
```

**Key principles:**
- **Forward steps**: Execute business logic steps sequentially
- **Track execution**: Record each completed step for compensation
- **Reverse compensation**: Undo steps in reverse order on failure
- **Semantic compensation**: Cancel reservation, refund payment (not database rollback)
- **Idempotent compensations**: Safe to retry compensation
- **Handle compensation failures**: Critical alerts for manual intervention

**Saga orchestration patterns:**
- **Orchestration**: Central coordinator (shown above)
- **Choreography**: Services coordinate via events (more decoupled)

---

### Pattern 5: Graceful Degradation

**When to use:**
- Non-critical service failures
- Maintaining core functionality during partial outages
- User experience over complete accuracy
- Fallback to cached/simplified responses

**Implementation approach:**
```python
def get_user_recommendations(user_id):
    """
    Get personalized recommendations with graceful degradation.
    Fallback chain: ML model → collaborative filtering → popular items
    """
    try:
        # Primary: ML-based personalized recommendations
        recommendations = ml_service.get_recommendations(user_id, timeout=2.0)
        logger.info(f"Returned ML recommendations for user {user_id}")
        return recommendations

    except (TimeoutError, ServiceUnavailableError) as e:
        logger.warning(f"ML service unavailable, falling back to collaborative: {e}")

        try:
            # Fallback 1: Collaborative filtering (faster, simpler)
            recommendations = collab_filter_service.get_similar_users_items(
                user_id,
                timeout=1.0
            )
            logger.info(f"Returned collaborative filtering for user {user_id}")
            return recommendations

        except (TimeoutError, ServiceUnavailableError) as e2:
            logger.warning(f"Collaborative filtering failed, falling back to popular: {e2}")

            try:
                # Fallback 2: Popular items (cached, always available)
                recommendations = cache.get_popular_items(category=user.category)
                logger.info(f"Returned popular items for user {user_id}")
                return recommendations

            except Exception as e3:
                # Final fallback: Empty recommendations (degraded but functional)
                logger.error(f"All recommendation sources failed, returning empty: {e3}")
                return []  # Graceful degradation: site still works, just no recommendations
```

**Key principles:**
- **Fallback chain**: Primary → Fallback 1 → Fallback 2 → Minimal functionality
- **Decreasing quality**: Each fallback is simpler/less accurate but faster/more reliable
- **Always functional**: Never completely fail (return empty/cached data)
- **Timeouts**: Use aggressive timeouts (1-2s) to fail fast and try fallback
- **Monitoring**: Track fallback rate (high rate = investigate primary service)

**Fallback strategies:**
- **Cached data**: Stale but available
- **Simplified logic**: Faster, less accurate algorithm
- **Default values**: Reasonable defaults (popular items, average values)
- **Degraded UI**: Hide non-critical features

---

## Data Consistency Strategies

### Strategy 1: Immediate Consistency (Single Database)

**Pattern**: Use database transactions for ACID guarantees

**When to use:**
- Single database operations
- Strong consistency required
- Operations must be atomic

**Implementation**: Transaction rollback pattern (see Pattern 3 above)

---

### Strategy 2: Eventual Consistency (Distributed Systems)

**Pattern**: Accept temporary inconsistency, guarantee eventual convergence

**When to use:**
- Distributed systems (multiple databases/services)
- High availability more important than immediate consistency
- Can tolerate temporary stale data

**Implementation:**
```python
# Step 1: Write to primary database (source of truth)
db.create_order(order_id, user_id, items, total)

# Step 2: Publish event for eventual consistency
event_bus.publish(OrderCreatedEvent(
    order_id=order_id,
    user_id=user_id,
    items=items,
    total=total,
    timestamp=now()
))

# Other services consume event asynchronously:
# - Inventory service decrements stock
# - Analytics service records purchase
# - Email service sends confirmation
# Each service eventually becomes consistent
```

**Key principles:**
- **Source of truth**: One service owns the data
- **Event-driven**: Publish events for others to react
- **Idempotent consumers**: Handle duplicate events safely
- **Monitoring**: Track lag between write and propagation
- **Conflict resolution**: Define merge strategy for concurrent updates

---

### Strategy 3: Causal Consistency

**Pattern**: Preserve cause-effect relationships while allowing other operations to be reordered

**When to use:**
- Social media feeds (comment after post)
- Collaborative editing (see your own changes)
- Chat applications (messages in order per conversation)

**Implementation**: Use vector clocks or logical timestamps to track causality

---

## Failure Prevention Patterns

### Bulkhead Pattern

**Purpose**: Isolate failures to prevent cascade

**Implementation:**
- **Connection pools**: Separate pools per service (failure in service A doesn't exhaust pool for service B)
- **Thread pools**: Separate threads per operation type
- **Resource limits**: CPU/memory limits per service (cgroups, Docker limits)

---

### Timeout Pattern

**Purpose**: Prevent indefinite waiting

**Implementation:**
```python
# Set aggressive timeouts
response = requests.get(
    external_api_url,
    timeout=(3.0, 10.0)  # (connection timeout, read timeout)
)

# Async with timeout
async with asyncio.timeout(5.0):
    result = await long_running_operation()
```

**Guidelines:**
- **Connection timeout**: 1-3s (how long to establish connection)
- **Read timeout**: 5-10s (how long to wait for response)
- **User-facing**: 2-5s max (prevent frustration)
- **Background jobs**: 30-60s (allow more time)

---

### Rate Limiting

**Purpose**: Prevent overload from excessive requests

**Implementation:**
- **Client-side**: Throttle requests to prevent hitting limits
- **Server-side**: Reject requests above threshold
- **Adaptive**: Reduce rate during degraded performance

---

## Monitoring & Alerting for Recovery

### Key Metrics

1. **Error rate**: Percentage of failed requests (alert if >1%)
2. **Retry rate**: How often retries happen (high rate = transient failures)
3. **Circuit breaker state**: Alert when circuits open
4. **Recovery time**: How long to recover from failure (MTTR)
5. **Compensation rate**: How often sagas compensate (should be low)

### Alerting Strategy

**Symptom-based alerts** (what users experience):
- High error rate (>1% for 5 minutes)
- High latency (p99 > 1s)
- Circuit breaker open

**Cause-based logging** (for debugging):
- Which specific operation failed
- Transient vs permanent failure
- Retry attempts and outcomes
- Compensation steps executed

---

## Testing Recovery Patterns

### Chaos Engineering

**Inject failures in test/staging:**
- Kill random services
- Introduce network latency
- Cause database timeouts
- Fill disk space
- Exhaust connection pools

**Verify:**
- System recovers automatically
- No data corruption
- Appropriate fallbacks triggered
- Monitoring alerts fire correctly

### Recovery Testing Checklist

- [ ] Retry logic works (verified with network failures)
- [ ] Circuit breaker opens/closes correctly
- [ ] Transaction rollback prevents partial writes
- [ ] Saga compensation executes in correct order
- [ ] Graceful degradation provides minimal functionality
- [ ] Timeouts prevent indefinite hangs
- [ ] Monitoring captures recovery events
- [ ] Alerts fire for critical failures

---

## Decision Framework

### When task fails, ask:

1. **Is failure transient or permanent?**
   - Transient → Retry with exponential backoff
   - Permanent → Don't retry, log error

2. **Is system distributed?**
   - Single database → Transaction rollback
   - Multiple services → Saga pattern

3. **Is service external/unreliable?**
   - Yes → Circuit breaker + fallback
   - No → Standard retry

4. **Can I degrade gracefully?**
   - Yes → Fallback chain (ML → simple → cached → empty)
   - No → Fast fail with error message

5. **What consistency guarantees needed?**
   - Strong (financial) → ACID transactions
   - Eventual (social) → Event-driven updates
   - Causal (chat) → Vector clocks

---

## Common Anti-Patterns

### ❌ Retry Forever
**Problem**: Infinite retry loop exhausts resources
**Solution**: Max retries (3-5), exponential backoff, circuit breaker

### ❌ No Jitter
**Problem**: Thundering herd (all clients retry simultaneously)
**Solution**: Add jitter (±25% randomness) to backoff

### ❌ Retry Non-Idempotent Operations
**Problem**: Duplicate charges, duplicate emails
**Solution**: Use idempotency keys, check before retrying

### ❌ Ignore Compensation Failures
**Problem**: Half-completed saga leaves inconsistent state
**Solution**: Alert operations team, manual intervention required

### ❌ No Timeouts
**Problem**: Indefinite hangs consume resources
**Solution**: Set timeouts on all external calls (3-10s)

### ❌ Synchronous Saga
**Problem**: Long-running saga blocks user
**Solution**: Asynchronous saga (immediate response, poll for completion)

---

## Real-World Examples

### Example 1: Payment Processing Failure
**Scenario**: Credit card charge fails during checkout

**Recovery strategy**:
1. Classify: Transient (network) or permanent (declined card)?
2. If transient: Retry with exponential backoff (3 attempts)
3. If permanent: Show user error, don't retry
4. If retry exhausted: Circuit breaker opens, use backup payment processor

### Example 2: Microservice Dependency Down
**Scenario**: Recommendation service unavailable

**Recovery strategy**:
1. Circuit breaker opens after 5 failures
2. Fast-fail for next 60 seconds (don't call service)
3. Graceful degradation: Show cached popular items
4. After 60s: Half-open state, test if service recovered
5. If recovered: Close circuit, resume normal operation

### Example 3: Database Transaction Failure
**Scenario**: Transfer between accounts fails mid-transaction

**Recovery strategy**:
1. Transaction rollback: Undo debit from source account
2. Log failure for investigation
3. Return error to user: "Transfer failed, please try again"
4. User retries: Idempotent (check if already processed)

---

## Summary Checklist

When implementing error recovery:

- [ ] **Classify failure**: Transient vs permanent, recoverable vs fatal
- [ ] **Select pattern**: Retry, circuit breaker, rollback, saga, or graceful degradation
- [ ] **Implement idempotency**: Use keys to prevent duplicate operations
- [ ] **Add timeouts**: Prevent indefinite hangs (3-10s)
- [ ] **Monitor recovery**: Track error rates, retry rates, circuit breaker states
- [ ] **Test failures**: Chaos engineering, inject faults, verify recovery
- [ ] **Alert on critical**: Circuit open, compensation failures, high error rates
- [ ] **Document runbooks**: How to manually intervene when automation fails

**Remember**: The goal is to recover automatically when possible, fail gracefully when not, and always maintain data consistency.
