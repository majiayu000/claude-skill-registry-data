---
name: architecture-skills
description: Master system design, architecture patterns, algorithms, data structures, and computer science fundamentals for building scalable systems.
sasmp_version: "1.3.0"
skill_type: atomic
version: "2.0.0"

parameters:
  scope:
    type: string
    enum: [component, service, system, enterprise]
    default: system
  style:
    type: string
    enum: [monolith, microservices, serverless, event-driven]
    default: microservices

validation_rules:
  - pattern: "^ADR-[0-9]{3}$"
    target: adr_ids
    message: ADR IDs must be ADR-NNN format
  - pattern: ".*Diagram$"
    target: diagram_files
    message: Diagram files should end with 'Diagram'

retry_config:
  max_attempts: 2
  backoff: linear
  initial_delay_ms: 1000

logging:
  on_entry: "[Architecture] Analyzing: {task}"
  on_success: "[Architecture] Decision recorded: {task}"
  on_error: "[Architecture] Analysis failed: {task}"

dependencies:
  agents:
    - system-architect
---

# System Architecture & Design Skills

## Big O Complexity Analysis

| Complexity | Name | Example |
|------------|------|---------|
| O(1) | Constant | Hash lookup |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | Array scan |
| O(n log n) | Linearithmic | Merge sort |
| O(n²) | Quadratic | Nested loops |
| O(2ⁿ) | Exponential | Power set |

## Common Data Structures

```python
# Time complexity comparison
class DataStructureGuide:
    """
    Array:      O(1) access, O(n) insert/delete
    LinkedList: O(n) access, O(1) insert/delete
    HashTable:  O(1) average, O(n) worst
    BST:        O(log n) balanced, O(n) worst
    Heap:       O(log n) insert/delete, O(1) min/max
    """

    @staticmethod
    def choose_structure(requirements: dict) -> str:
        if requirements.get("fast_lookup"):
            return "HashTable"
        if requirements.get("ordered"):
            return "BST or SortedArray"
        if requirements.get("priority"):
            return "Heap"
        return "Array"
```

## Design Patterns

```python
# Singleton with thread safety
from threading import Lock

class Singleton:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

# Factory Pattern
class ServiceFactory:
    _services = {}

    @classmethod
    def register(cls, name: str, service_class):
        cls._services[name] = service_class

    @classmethod
    def create(cls, name: str, **kwargs):
        service_class = cls._services.get(name)
        if not service_class:
            raise ValueError(f"Unknown service: {name}")
        return service_class(**kwargs)

# Strategy Pattern
from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass

class CreditCardPayment(PaymentStrategy):
    def pay(self, amount: float) -> bool:
        # Process credit card
        return True

class PayPalPayment(PaymentStrategy):
    def pay(self, amount: float) -> bool:
        # Process PayPal
        return True
```

## System Design Principles

```
SOLID Principles:
┌─────────────────────────────────────────────────┐
│ S - Single Responsibility                       │
│     → One class, one reason to change           │
│                                                 │
│ O - Open/Closed                                 │
│     → Open for extension, closed for change     │
│                                                 │
│ L - Liskov Substitution                         │
│     → Subtypes must be substitutable            │
│                                                 │
│ I - Interface Segregation                       │
│     → Many specific interfaces > one general    │
│                                                 │
│ D - Dependency Inversion                        │
│     → Depend on abstractions, not concretions   │
└─────────────────────────────────────────────────┘

Additional Principles:
DRY  - Don't Repeat Yourself
KISS - Keep It Simple, Stupid
YAGNI - You Aren't Gonna Need It
```

## Scalability Patterns

```yaml
# Horizontal vs Vertical Scaling
horizontal:
  approach: Add more servers
  pros:
    - Better fault tolerance
    - Theoretically unlimited
  cons:
    - Complexity
    - Data consistency challenges

vertical:
  approach: Increase server resources
  pros:
    - Simpler
    - No code changes
  cons:
    - Hardware limits
    - Single point of failure

# Caching Strategy (Cache-Aside)
cache_aside:
  read:
    1: Check cache
    2: If miss, read from DB
    3: Store in cache
    4: Return data
  write:
    1: Write to DB
    2: Invalidate cache

# Database Scaling
database:
  read_replicas:
    - Offload read traffic
    - Eventual consistency
  sharding:
    - Horizontal partitioning
    - Key-based routing
  partitioning:
    - Range or hash based
    - Within single database
```

## Distributed Systems

```
CAP Theorem:
┌─────────────────┐
│   Consistency   │ ← All nodes see same data
├─────────────────┤
│  Availability   │ ← Every request gets response
├─────────────────┤
│   Partition     │ ← System works despite network
│   Tolerance     │   failures
└─────────────────┘
→ Choose 2 of 3 (P is usually required)

CP Systems: MongoDB, Redis Cluster
AP Systems: Cassandra, DynamoDB
CA Systems: Traditional RDBMS (no partition tolerance)
```

## Architecture Decision Record

```markdown
# ADR-001: Use Event-Driven Architecture

## Status
Accepted

## Context
Our system needs to handle async workflows
and decouple services for scalability.

## Decision
Adopt event-driven architecture using Kafka
as the message broker.

## Consequences
### Positive
- Loose coupling between services
- Better scalability
- Async processing capability

### Negative
- Increased complexity
- Eventual consistency challenges
- Debugging is harder

## Alternatives Considered
- REST-based sync communication (rejected: tight coupling)
- RabbitMQ (rejected: Kafka better for our scale)
```

## System Design Template

```
┌─────────────────────────────────────────────────────────────┐
│ 1. REQUIREMENTS (5 min)                                     │
│    □ Functional: What does it do?                           │
│    □ Non-functional: Scale, latency, availability           │
│    □ Constraints: Budget, timeline, team                    │
├─────────────────────────────────────────────────────────────┤
│ 2. ESTIMATION (5 min)                                       │
│    □ Users: DAU, peak concurrent                            │
│    □ Storage: Data size, growth rate                        │
│    □ Bandwidth: Requests/sec, data transfer                 │
├─────────────────────────────────────────────────────────────┤
│ 3. HIGH-LEVEL DESIGN (10 min)                               │
│    □ Components: Services, databases, caches                │
│    □ Data flow: Read/write paths                            │
│    □ APIs: Endpoints, contracts                             │
├─────────────────────────────────────────────────────────────┤
│ 4. DEEP DIVE (15 min)                                       │
│    □ Database schema                                        │
│    □ Caching strategy                                       │
│    □ Scaling approach                                       │
├─────────────────────────────────────────────────────────────┤
│ 5. TRADE-OFFS (5 min)                                       │
│    □ Consistency vs Availability                            │
│    □ Cost vs Performance                                    │
│    □ Complexity vs Maintainability                          │
└─────────────────────────────────────────────────────────────┘
```

## Troubleshooting Guide

| Issue | Root Cause | Solution |
|-------|------------|----------|
| Cascading failure | No circuit breaker | Add Hystrix/Resilience4j |
| Inconsistent data | Race condition | Use distributed locks |
| Hot spots | Uneven sharding | Consistent hashing |
| High latency | N+1 queries | Batch or cache |

## Key Concepts Checklist

- [ ] Big O complexity analysis
- [ ] Data structure trade-offs
- [ ] Sorting and searching
- [ ] Graph algorithms
- [ ] Dynamic programming
- [ ] System design interviews
- [ ] Scalability patterns
- [ ] Database design
- [ ] Caching strategies
- [ ] Load balancing
- [ ] Microservices
- [ ] API design
- [ ] Security principles
- [ ] Performance optimization

---

**Source**: https://roadmap.sh
**Version**: 2.0.0
**Last Updated**: 2025-01-01
