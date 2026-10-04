---
name: root-cause-classification
description: Structured approach to diagnosing bugs and classifying their root cause as code, data, environment, dependency, design, or process.
---
# Root Cause Classification

A structured approach to diagnosing bugs and classifying their root causes.

## Classification Taxonomy

Every bug falls into one of these categories. Choose the one that best describes the **fundamental cause**, not the symptom.

### code
Logic errors in the application code itself.
- Off-by-one errors
- Wrong conditional logic
- Missing null/nil checks
- Incorrect algorithm implementation
- Type errors or casting issues
- Missing error handling

### data
Issues with data quality, format, or schema.
- Corrupt or unexpected data in the database
- Schema migration issues
- Data format mismatches between systems
- Missing or stale cache entries
- Encoding/serialization errors

### env
Environment and infrastructure configuration.
- Missing or wrong environment variables
- Wrong credentials or expired tokens
- DNS/networking configuration
- Resource limits (memory, disk, connections)
- Version mismatches between environments

### user
Unexpected user behavior or edge cases.
- Input the system doesn't handle (special characters, extreme values)
- Workflow the design didn't anticipate
- Concurrent actions from the same user
- Browser/device-specific behavior

### external
Failures in third-party services or dependencies.
- API breaking changes upstream
- Dependency bugs
- Third-party service outages or rate limits
- SDK version incompatibilities

### race
Concurrency and timing issues.
- Race conditions between goroutines/threads
- Deadlocks
- Timing-dependent behavior
- Stale reads in distributed systems
- Double-submit / duplicate processing

### design
The design itself is flawed.
- Missing requirement in the original spec
- Incorrect assumption about user behavior
- Architecture doesn't handle the scale/pattern
- Feature interaction not considered

## Investigation Process

1. **Reproduce** — Can you consistently trigger the bug? What's the minimal reproduction?
2. **Isolate** — What component/layer is the bug in? Use logs, debugger, or tracing.
3. **Trace** — Follow the execution path from trigger to symptom. Where does it diverge from expected?
4. **Classify** — Based on the root cause, assign a classification.
5. **Assess** — Severity (low/medium/high/critical) and blast radius.
6. **Fix** — Design the fix. Does it address the root cause or just the symptom?

## Severity Guide

- **critical** — Data loss, security vulnerability, complete service outage
- **high** — Major feature broken, significant user impact, workaround difficult
- **medium** — Feature partially broken, workaround exists, limited user impact
- **low** — Minor inconvenience, cosmetic, edge case with easy workaround

## Frontmatter Fields

Add these to the bug spec:

```yaml
root_cause_class: code  # code, data, env, user, external, race, design
severity: medium        # low, medium, high, critical
```

## Pattern Recognition

After classifying several bugs, look for patterns:
- Cluster of `data` bugs → need better validation and migration testing
- Cluster of `env` bugs → need better config management and parity between environments
- Cluster of `race` bugs → need concurrency review, consider adding race detector to CI
- Cluster of `design` bugs → specs need more thorough edge case analysis
- Cluster of `external` bugs → need better resilience patterns (retries, circuit breakers, fallbacks)
