---
name: root-cause-five-whys
description: "1."
---

# Root Cause Analysis: Five Whys (Verbose)

## The Five Whys Process

### Example 1: Database Outage

```
1. What happened?
   API returning 500 errors, database unavailable

2. Why?
   New query deployed without timeout,
   connection pool exhausted

3. Why?
   Query wrote infinite loop,
   connections never released

4. Why?
   Code review didn't catch infinite loop,
   no static analysis

5. Why?
   No automated testing in CI/CD,
   manual review only

Root Cause: Lack of automated code analysis and testing
Solution: Implement static analysis (linting) + unit tests in CI
```

### Example 2: Data Inconsistency

```
1. What happened?
   Customer balance showed $100, actual balance $200

2. Why?
   Two updates applied out of order
   (debit before credit)

3. Why?
   No ordering guarantee in async queue

4. Why?
   Queue implemented as simple FIFO,
   retries re-enqueued randomly

5. Why?
   No message deduplication or ordering,
   system designed without considering retries

Root Cause: Async queue lacks message ordering and deduplication
Solution: Use ordered queue (Kafka, RabbitMQ with ordering)
```

## Effective vs Ineffective RCAs

### ❌ Ineffective: Stops at Individual

```
Q: What happened?
A: API crashed

Q: Why?
A: Engineer deployed bad code

Q: Why?
A: Engineer made a mistake

Analysis ends.
Prevention: Nothing (can't prevent mistakes)
Result: Same incident repeats in 3 months
```

### ✅ Effective: Focuses on System

```
Q: What happened?
A: API crashed due to code bug

Q: Why?
A: Code review didn't catch bug

Q: Why?
A: No automated testing in CI/CD

Q: Why?
A: Testing infrastructure wasn't set up

Q: Why?
A: No resources allocated for testing

Root Cause: Organizational resource allocation
Prevention: Budget for testing infrastructure
Result: Similar bugs caught automatically
```

## Five Whys Facilitator Guide

**Role:** Don't solve, facilitate discussion

**Do:**
- Ask open-ended questions
- Let participants explain fully
- Dig deeper on vague answers
- Challenge assumptions

**Don't:**
- Propose solutions too early
- Judge/blame anyone
- Settle for first answer
- Move too fast

### Red Flag Answers

❌ "Engineer made a mistake"  
→ Ask: "How can the system prevent this mistake?"

❌ "Miscommunication"  
→ Ask: "Why wasn't the information clear?"

❌ "Bad luck"  
→ Ask: "What about the design made us susceptible?"

## Ishikawa (Fishbone) Diagram

Instead of just "5 Whys", map contributing factors:

```
                     Root Cause
                         |
      ┌─────────┬─────────┼─────────┬─────────┐
      |         |         |         |         |
    Process  People   Systems   Tools    Data
      |         |         |         |         |
   - Retry    - Training  - No      - No      - No
     logic    - Comms      testing   static    validation
               - Support  - No       analysis
                 hours     monitoring
                          
                    ↓ All lead to
                 
                Root Cause:
            Lack of automation
              & safeguards
```

## Real-World Examples

### Incident: Payment Processing Failure

```
Timeline: Payment authorization occasionally failed (0.1% rate)

Level 1 Why: Authorization service returning 500 errors
Level 2 Why: Database connections timing out
Level 3 Why: Database query had no timeout specified
Level 4 Why: Code didn't specify timeout in connection config
Level 5 Why: Default connection timeout was infinite (legacy config)

Root Cause: Legacy configuration with unsafe defaults
Solution: Add timeout to all database connections, update defaults

Prevention: Configuration validation, automated tests for timeouts
```

### Incident: Data Loss

```
Timeline: 1000 user records deleted unexpectedly

Level 1 Why: Database delete command executed
Level 2 Why: Batch deletion script ran without filters
Level 3 Why: Script had WHERE clause but it evaluated to TRUE
Level 4 Why: WHERE clause checked wrong database column
Level 5 Why: No schema validation, no schema versioning

Root Cause: Lack of schema versioning and migration testing
Solution: Implement migration testing, run on staging first
Prevention: All migrations tested on production-like data
```

## Documenting RCA Results

```markdown
# Root Cause Analysis: Order Processing Failure

## Timeline
- 14:00: Failure began
- 14:05: Detected
- 14:10: Mitigated
- 14:15: Resolved

## Five Whys

1. **What happened?**
   50% of orders failed processing

2. **Why?**
   Payment API was unavailable

3. **Why?**
   Payment service exceeded rate limits

4. **Why?**
   No circuit breaker, kept hammering API

5. **Why?**
   Application designed without circuit breaker pattern

## Root Cause
Lack of circuit breaker in payment integration

## Prevention Measures
- [ ] Implement circuit breaker library
- [ ] Add exponential backoff
- [ ] Monitor payment API health
- [ ] Add integration tests
- [ ] Document failure modes

## Timeline to Complete
- Week 1: Implement circuit breaker
- Week 2: Deploy and test
- Week 3: Monitor for recurrence
```

## Common RCA Mistakes

❌ "The system failed" (too vague)  
✅ "Query timeout not set" (specific)

❌ Stopping after 3 whys (too shallow)  
✅ Continue until "system design" or "process"

❌ Assigning blame  
✅ Focus on systems and processes

❌ Proposing solution before RCA  
✅ Complete RCA, then brainstorm solutions

## Success Indicators

✅ Root cause is about system, not individual  
✅ Solution is preventable (not "engineer won't make mistake")  
✅ Team learns something (not obvious)  
✅ Similar incidents should be prevented by solution  
✅ Everyone agrees on root cause
