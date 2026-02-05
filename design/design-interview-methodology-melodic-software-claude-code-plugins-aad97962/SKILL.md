---
name: design-interview-methodology
description: 4-step framework for system design interviews. Use when preparing for technical interviews, practicing whiteboard design, or structuring architectural discussions. Covers requirements gathering, high-level design, deep dives, and wrap-up.
allowed-tools: Read, Glob, Grep
---

# Design Interview Methodology

This skill provides a structured framework for approaching system design interviews and architectural discussions.

## When to Use This Skill

**Keywords:** system design interview, whiteboard design, architecture discussion, technical interview, design framework

**Use this skill when:**

- Preparing for a system design interview
- Structuring a whiteboard architectural session
- Teaching others how to approach design problems
- Practicing with design exercises
- Leading architectural discussions with stakeholders

## The 4-Step Framework

System design interviews typically last 45-60 minutes. This framework ensures you cover all bases while demonstrating structured thinking.

| Step | Time | Purpose |
| ---- | ---- | ------- |
| **1. Requirements** | 5-10 min | Clarify scope, constraints, scale |
| **2. High-Level Design** | 10-15 min | Draw major components and data flow |
| **3. Deep Dive** | 15-20 min | Detail 1-2 critical components |
| **4. Wrap-Up** | 5-10 min | Trade-offs, bottlenecks, improvements |

## Step 1: Requirements Gathering (5-10 minutes)

**Goal:** Understand what to build and constraints before designing.

### Functional Requirements

Ask about core functionality:

- "What are the primary use cases?"
- "What should users be able to do?"
- "What are the must-have vs. nice-to-have features?"

### Non-Functional Requirements (NFRs)

Clarify quality attributes:

| Category | Questions to Ask |
| -------- | ---------------- |
| **Scale** | How many users? DAU/MAU? Read/write ratio? |
| **Performance** | Latency requirements? Throughput targets? |
| **Availability** | Uptime requirements? (99.9% = 8.76 hours downtime/year) |
| **Consistency** | Strong or eventual consistency? |
| **Durability** | Data loss tolerance? Backup requirements? |

### Back-of-Envelope Estimation

Quick calculations to inform design:

```text
Example: Design a URL shortener

Users: 100M monthly active
Writes: 100M URLs/month = ~40 writes/second
Reads: 10:1 ratio = 400 reads/second
Storage: 100M * 500 bytes = 50GB/month = 600GB/year
```

**Detailed estimation techniques:** See `estimation-techniques` skill.

### Requirements Checklist

Before proceeding to design:

- [ ] Core use cases identified
- [ ] Scale understood (users, data, requests)
- [ ] Read/write ratio known
- [ ] Latency/throughput targets set
- [ ] Consistency requirements clear
- [ ] Availability targets established

## Step 2: High-Level Design (10-15 minutes)

**Goal:** Draw the major components and show data flow.

### Start with the Obvious

Begin with the simplest architecture that could work:

```text
Client --> API Gateway --> Service --> Database
```

Then add complexity as needed based on requirements.

### Core Components to Consider

| Component | When to Include |
| --------- | --------------- |
| **Load Balancer** | Multiple servers, horizontal scaling |
| **API Gateway** | Authentication, rate limiting, routing |
| **CDN** | Static content, global users |
| **Cache** | Read-heavy, latency-sensitive |
| **Message Queue** | Async processing, decoupling |
| **Database** | Persistent storage (SQL vs NoSQL decision) |
| **Search** | Full-text search, complex queries |
| **Object Storage** | Large files, media content |

### Data Flow Narration

Walk through the system explaining each step:

```text
"When a user creates a short URL:
1. Request hits the load balancer
2. API Gateway validates the request and checks rate limits
3. Service generates a unique short code
4. Short code and URL are stored in the database
5. Cache is updated for fast reads
6. Response returns the shortened URL"
```

### API Design

Sketch key API endpoints:

```text
POST /urls          - Create short URL
GET  /{shortCode}   - Redirect to long URL
GET  /urls/{id}/stats - Get click analytics
```

### Database Schema Sketch

Show key tables/collections:

```text
URLs table:
- id: primary key
- short_code: indexed, unique
- long_url: original URL
- user_id: foreign key
- created_at: timestamp
- expires_at: nullable timestamp
```

## Step 3: Deep Dive (15-20 minutes)

**Goal:** Demonstrate depth on 1-2 critical components.

### How to Choose What to Deep Dive

Let the interviewer guide, or choose based on:

1. **Most complex component** - Shows technical depth
2. **Most critical for requirements** - Shows understanding
3. **Your strength area** - Play to your expertise

### Common Deep Dive Topics

| Topic | What to Cover |
| ----- | ------------- |
| **Database scaling** | Sharding strategy, replication, indexes |
| **Caching** | Cache strategy, invalidation, hit ratio |
| **Data consistency** | Conflict resolution, distributed transactions |
| **Search** | Indexing, ranking, query optimization |
| **Messaging** | Delivery guarantees, ordering, dead letters |
| **Rate limiting** | Algorithm choice, distributed implementation |

### Example Deep Dive: URL Shortener ID Generation

```text
Option 1: Auto-increment
  Pros: Simple, guaranteed unique
  Cons: Predictable, single point of failure, hard to scale

Option 2: UUID
  Pros: No coordination needed
  Cons: Too long (36 chars), not URL-friendly

Option 3: Base62 encoding of counter
  Pros: Short, URL-friendly
  Cons: Requires coordination for distributed systems

Option 4: Pre-generated IDs
  Pros: Fast, no runtime coordination
  Cons: ID exhaustion, more complex

Recommendation: Pre-generated ID ranges + Base62 encoding
- Each server gets a range of IDs
- IDs are Base62 encoded for short URLs
- Handles distributed scale without coordination per request
```

### Quantify Trade-offs

Always explain trade-offs with specifics:

- "This adds latency of ~5ms but improves reliability from 99% to 99.9%"
- "This uses 3x more storage but reduces query time from 100ms to 10ms"
- "This increases complexity but allows horizontal scaling to 10x traffic"

## Step 4: Wrap-Up (5-10 minutes)

**Goal:** Summarize, identify issues, and propose improvements.

### Identify Bottlenecks

Where will the system break first as scale increases?

```text
"The main bottleneck is the database. At 10x current scale:
- Write throughput becomes limiting
- Solution: Implement sharding by URL prefix
- Fallback: Read replicas for analytics queries"
```

### Discuss Trade-offs Made

Summarize key decisions and alternatives:

```text
"We chose eventual consistency for the redirect cache:
- Benefit: Lower latency, simpler architecture
- Cost: Up to 5 seconds of stale data possible
- Alternative: Strong consistency with higher latency"
```

### Propose Improvements

If you had more time, what would you add?

| Improvement | Benefit |
| ----------- | ------- |
| Analytics pipeline | Usage insights, business value |
| Abuse detection | Malware/spam URL protection |
| Geographic distribution | Lower latency globally |
| A/B testing capability | Feature experimentation |

### Handle Edge Cases

Mention edge cases you'd address:

- What if the database is down?
- What if a URL expires mid-redirect?
- What if a malicious user spams URL creation?
- What about duplicate long URLs?

## Common Pitfalls to Avoid

### 1. Jumping to Solution

**Problem:** Starting to design without understanding requirements.
**Fix:** Spend 5-10 minutes on requirements first.

### 2. Over-Engineering

**Problem:** Adding every component you know.
**Fix:** Start simple, add complexity only when justified by requirements.

### 3. Not Quantifying

**Problem:** Vague statements like "it's fast" or "it scales."
**Fix:** Use numbers: "handles 10K requests/second with p99 latency of 50ms."

### 4. Ignoring Trade-offs

**Problem:** Presenting only benefits of your design.
**Fix:** Actively discuss what you're sacrificing for each decision.

### 5. Silent Designing

**Problem:** Drawing without explaining.
**Fix:** Narrate your thought process constantly.

## Interview Signals: What Interviewers Look For

### Strong Signals

- Asks clarifying questions before designing
- Starts with requirements, not solutions
- Quantifies scale with back-of-envelope math
- Explains trade-offs for each decision
- Identifies bottlenecks proactively
- Acknowledges what they don't know

### Red Flags

- Jumps to favorite technology without justification
- Ignores scale/performance requirements
- Can't explain why a component is needed
- No consideration of failure scenarios
- Unable to identify trade-offs
- Defensive when challenged

## Time Management Tips

| Situation | Response |
| --------- | -------- |
| Running short on time | Skip to wrap-up, summarize trade-offs |
| Interviewer redirects | Follow their lead, they're guiding you |
| Stuck on a component | Acknowledge, move on, come back if time |
| Asked unknown technology | Explain your reasoning, ask about constraints |

## Practice Strategy

### Before the Interview

1. Study common design problems (see `design-problem-catalog` skill - Phase 4)
2. Practice back-of-envelope calculations (see `estimation-techniques` skill)
3. Know your quality attributes (see `quality-attributes-taxonomy` skill)
4. Time yourself on practice problems

### During Practice

- Set a 45-minute timer
- Practice on a whiteboard or paper (not IDE)
- Narrate your thoughts out loud
- Record yourself and review

## Related Skills

- `estimation-techniques` - Back-of-envelope calculations for scale
- `quality-attributes-taxonomy` - NFRs and the "-ilities"
- `cap-theorem` - Consistency/availability trade-offs (Phase 2)
- `design-problem-catalog` - Common interview problems (Phase 4)

## Related Commands

- `/sd:design <problem>` - Interactive design session (Phase 4)
- `/sd:estimate <scenario>` - Capacity calculations
- `/sd:explain <concept>` - Explain any concept

## Related Agents

- `system-design-interviewer` - Mock interview practice (Phase 4)
- `capacity-planner` - Back-of-envelope calculations
- `architecture-critic` - Challenge your designs (Phase 4)

---

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
