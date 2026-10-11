---
name: stride-denial-of-service
description: Generate Denial of Service threats for a system, repo, architecture, or data flow. Use when Codex needs to identify how attackers could exhaust resources, block workflows, amplify load, starve dependencies, or otherwise reduce availability or degrade service quality.
---

# STRIDE Denial Of Service

## Overview

Use this skill to generate threat ideas specifically in the Denial of Service category of STRIDE. Focus on availability loss, resource exhaustion, queue buildup, lock contention, retry storms, dependency saturation, and operational degradation.

Prefer threats tied to actual bottlenecks, amplification points, and failure cascades over generic "the system could go down" statements.

## Workflow

### 1. Establish the modeling scope

Choose one concrete slice first:

- one API path
- one background job or worker pool
- one storage or cache dependency
- one external integration
- one multi-step workflow with retries or fan-out

### 2. Identify critical resources and chokepoints

Look for:

- CPU, memory, disk, network, file descriptors, threads, worker slots
- databases, caches, queues, object stores, and third-party APIs
- rate limits, batch jobs, import pipelines, and scheduled tasks
- locks, transactions, contention points, and serial bottlenecks
- expensive queries, large payloads, or unbounded loops

### 3. Generate Denial of Service threats

Generate threats around:

- request floods or expensive-request abuse
- queue flooding or dead-letter buildup
- retry storms and cascading failures
- large uploads, decompression bombs, or oversized payloads
- cache stampedes or thundering herds
- lock contention, hot partitions, or single-tenant noisy-neighbor effects
- external dependency slowness propagating into core workflows
- admin or reporting jobs starving production traffic

### 4. Stress availability assumptions

For each chokepoint, ask:

- What happens if this component gets 10x or 100x more work?
- What prevents a single actor or tenant from monopolizing shared resources?
- Are retries bounded and jittered?
- Is work admission controlled with limits, quotas, backpressure, or circuit breakers?
- Can low-cost attacker input trigger high-cost backend work?

### 5. Deliver concise threats

For each threat, capture:

- threat title
- component or boundary affected
- availability scenario
- likely impact
- why the system may be vulnerable
- suggested mitigations or validation questions

## Output Rules

Default to a short list of concrete Denial of Service threats.

Do not drift into general performance tuning unless the issue affects attacker-driven or failure-driven availability loss.

## Example Requests

- Generate Denial of Service threats for this API.
- Review this repo and identify resource-exhaustion and retry-storm risks.
- Use this architecture to find where one tenant could degrade shared availability.
