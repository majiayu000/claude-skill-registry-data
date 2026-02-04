---
name: systems-computing
description: Understand computer systems from digital logic through operating systems, networks, databases, and distributed systems.
sasmp_version: "1.3.0"
bonded_agent: 05-systems-expert
bond_type: PRIMARY_BOND
---

# Systems Computing Skill

## Skill Metadata

```yaml
skill_config:
  version: "1.0.0"
  category: systems
  prerequisites: [cs-foundations]
  estimated_time: "10-12 weeks"
  difficulty: intermediate-advanced

  parameter_validation:
    domain:
      type: string
      enum: [cpu, memory, os, network, database, distributed]
      required: true
    scale:
      type: string
      enum: [single, cluster, global]
      default: single

  retry_config:
    max_attempts: 3
    backoff_strategy: exponential
    initial_delay_ms: 500

  observability:
    log_level: INFO
    metrics: [domain_usage, design_pattern_frequency]
```

---

## Quick Start

Master how modern computers actually work, from circuits to distributed systems.

### Digital Logic & CPU

**CPU Concepts**
- Instruction execution cycle
- Registers and cache hierarchy
- Pipelining
- Branch prediction

**Cache Memory**
- L1, L2, L3 hierarchy
- Temporal and spatial locality
- Cache lines and blocks

### Operating Systems

**Process Management**
- Process states and context switching
- Scheduling algorithms: FCFS, SJF, round-robin

**Memory Management**
- Virtual memory and paging
- Page tables and TLB
- Page replacement: LRU, optimal

**Concurrency**
- Race conditions and critical sections
- Mutual exclusion: locks, semaphores
- Deadlock: conditions, detection, recovery

### Networking

**OSI Model**
- Layer 1: Physical (signals, cables)
- Layer 2: Data Link (MAC, switching)
- Layer 3: Network (IP, routing)
- Layer 4: Transport (TCP, UDP)

**Protocols**
- HTTP/HTTPS: Web
- TCP: Reliable connection
- UDP: Fast connectionless
- DNS: Name resolution

### Distributed Systems

**CAP Theorem**
- Consistency: all nodes same data
- Availability: responds to requests
- Partition tolerance: survives splits
- Can guarantee only 2 of 3

**Consensus Algorithms**
- Paxos: proven consensus
- Raft: simpler consensus

---

## Troubleshooting

| Issue | Root Cause | Resolution |
|-------|------------|------------|
| High latency | Slow DB queries | Add indexes, cache |
| Memory exhaustion | Memory leak | Profile, fix leaks |
| Connection exhaustion | Pool too small | Increase pool size |
| Cascading failure | No circuit breaker | Add circuit breakers |

---

## Key Concepts

- **Latency**: Time to complete one task
- **Throughput**: Tasks completed per unit time
- **Scalability**: Performance with increasing load
- **Fault tolerance**: Reliability despite failures

---

## Interview Questions

- How do caches work?
- Explain virtual memory
- What is thrashing?
- Difference between TCP and UDP?
- How do transactions work?
- Design a system that scales to millions of users
