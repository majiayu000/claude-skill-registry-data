---
name: architecture-guide
description: Comprehensive software architecture and system design guide covering design patterns, distributed systems, scalability, microservices, and architectural principles. Use when designing systems, solving architecture problems, or learning design patterns.
sasmp_version: "1.3.0"
bonded_agent: 06-architecture-specialist
bond_type: PRIMARY_BOND
eqhm_enabled: true
---

# Architecture & System Design Guide

Master software architecture, system design, and building scalable distributed systems.

## Quick Start

### Monolithic Architecture
```
┌─────────────────────────────────────┐
│          Application Layer          │
├─────────────────────────────────────┤
│  Authentication │ API │ Business    │
├─────────────────────────────────────┤
│          Database Layer             │
└─────────────────────────────────────┘
```

### Microservices Architecture
```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Auth Service │  │ Order Service │  │ User Service │
└──────────────┘  └──────────────┘  └──────────────┘
        │                │                  │
        └────────────────┴──────────────────┘
                    │
            ┌───────────────────┐
            │  API Gateway      │
            └───────────────────┘
            │
        ┌───┴───┐
        │Client │
        └───────┘
```

## Design Patterns

### Creational Patterns
```javascript
// Singleton Pattern
class Database {
  static instance = null;

  static getInstance() {
    if (!Database.instance) {
      Database.instance = new Database();
    }
    return Database.instance;
  }
}

// Factory Pattern
class UserFactory {
  createUser(type) {
    if (type === 'admin') return new AdminUser();
    if (type === 'regular') return new RegularUser();
  }
}

// Builder Pattern
class UserBuilder {
  constructor(name) {
    this.name = name;
  }

  setEmail(email) {
    this.email = email;
    return this;
  }

  setRole(role) {
    this.role = role;
    return this;
  }

  build() {
    return new User(this);
  }
}
```

### Structural Patterns
```javascript
// Adapter Pattern
class OldAPI {
  getData() { return { data: [] }; }
}

class APIAdapter {
  constructor(oldAPI) {
    this.oldAPI = oldAPI;
  }

  getAPIv2Format() {
    return { response: this.oldAPI.getData() };
  }
}

// Decorator Pattern
class Coffee {
  cost() { return 5; }
}

class MilkDecorator {
  constructor(coffee) {
    this.coffee = coffee;
  }

  cost() { return this.coffee.cost() + 2; }
}
```

### Behavioral Patterns
```javascript
// Observer Pattern
class EventEmitter {
  constructor() {
    this.listeners = {};
  }

  on(event, callback) {
    this.listeners[event] = this.listeners[event] || [];
    this.listeners[event].push(callback);
  }

  emit(event, data) {
    if (this.listeners[event]) {
      this.listeners[event].forEach(cb => cb(data));
    }
  }
}

// Strategy Pattern
class PaymentProcessor {
  constructor(strategy) {
    this.strategy = strategy;
  }

  process(amount) {
    return this.strategy.process(amount);
  }
}

class CreditCardStrategy {
  process(amount) { return `Processing credit card: $${amount}`; }
}

class PayPalStrategy {
  process(amount) { return `Processing PayPal: $${amount}`; }
}
```

## Architectural Patterns

### Layered Architecture (N-Tier)
```
┌─────────────────────┐
│  Presentation Layer │
├─────────────────────┤
│  Business Logic     │
├─────────────────────┤
│  Persistence Layer  │
├─────────────────────┤
│  Database           │
└─────────────────────┘
```
- Simple, familiar structure
- Easy to organize code
- Can become monolithic

### Event-Driven Architecture
```
┌──────────────────┐
│  Event Producer  │
└────────┬─────────┘
         │ (Message Broker)
     ┌───┴────┬────────┐
┌────▼────┐ ┌▼─────┐ ┌▼──────┐
│Consumer1│ │Cons2 │ │Cons3  │
└─────────┘ └──────┘ └───────┘
```
- Decoupled systems
- Real-time processing
- Complexity in event management

### Microservices Architecture
- **Advantages**: Independent scaling, language flexibility
- **Challenges**: Distributed systems, testing, DevOps
- **Best For**: Large teams, complex domains

## Scalability Concepts

### Horizontal vs Vertical Scaling
```
Vertical Scaling:          Horizontal Scaling:
┌──────────┐              ┌──────────┐
│Server    │              │Server 1  │
│16GB RAM  │              │4GB RAM   │
│4 CPUs    │   ──────>    ├──────────┤
└──────────┘              │Server 2  │
                          │4GB RAM   │
                          ├──────────┤
                          │Server 3  │
                          │4GB RAM   │
                          └──────────┘
```

### Load Balancing
- **Round-robin**: Distribute equally
- **Least connections**: Route to least busy
- **IP hash**: Sticky sessions
- **Weighted**: Prefer certain servers

### Caching Strategies
```
Application -> L1 Cache (In-memory)
            -> L2 Cache (Redis)
            -> L3 Cache (CDN)
            -> Database
```

### Database Scaling
- **Read Replicas**: Multiple read-only copies
- **Sharding**: Horizontal partitioning
- **Replication**: Master-slave, multi-master

## Distributed Systems Concepts

### CAP Theorem
Choose 2 of 3:
- **Consistency**: All nodes see same data
- **Availability**: System always responds
- **Partition Tolerance**: Survives network failures

### Consensus Algorithms
- **Paxos**: Complex but proven
- **RAFT**: More understandable
- **Gossip**: Eventual consistency

### Distributed Transactions
- **Saga Pattern**: Long-running transactions
- **Two-Phase Commit**: ACID across systems
- **Event Sourcing**: Immutable event log

## API Design

### REST Principles
```
GET    /api/users              # List
GET    /api/users/:id          # Read
POST   /api/users              # Create
PUT    /api/users/:id          # Update
DELETE /api/users/:id          # Delete
```

### GraphQL Basics
```graphql
query {
  user(id: 1) {
    name
    email
    posts {
      title
      content
    }
  }
}
```

### gRPC
- Protocol buffers for serialization
- HTTP/2 for efficiency
- Strong typing and contract

## Data Modeling

### Normalization
- **1NF**: Atomic values
- **2NF**: Remove partial dependencies
- **3NF**: Remove transitive dependencies
- **BCNF**: Boyce-Codd Normal Form

### Denormalization Tradeoffs
- Faster reads, slower writes
- Redundant data
- Consistency challenges

## System Design Interview Patterns

### Approach
1. **Clarify Requirements**: Functional and non-functional
2. **Estimate Scale**: Users, QPS, storage
3. **Design High-Level**: Component diagram
4. **Dive Deep**: Pick critical components
5. **Discuss Tradeoffs**: Pros and cons

### Common Systems to Design
- **Twitter Feed**: Caching, fan-out, databases
- **Video Streaming**: CDN, encoding, playback
- **Messenger**: Real-time, consistency, scalability
- **Ride-sharing**: Geo-location, matching, payments

## Architecture Decision Records (ADR)

```markdown
# ADR 001: Use PostgreSQL for main database

## Context
We need a relational database for our data model.

## Decision
We will use PostgreSQL instead of MySQL.

## Consequences
- Excellent JSON support
- Better concurrency handling
- Steeper learning curve than MySQL
```

## Security Architecture

### Defense in Depth
```
┌──────────────────────────┐
│ Firewall                 │
├──────────────────────────┤
│ API Gateway / WAF        │
├──────────────────────────┤
│ Application Security     │
├──────────────────────────┤
│ Database Encryption      │
├──────────────────────────┤
│ Physical Security        │
└──────────────────────────┘
```

## Performance Architecture

### Optimization Levels
1. **Database**: Indexing, query optimization
2. **Application**: Caching, algorithms
3. **Infrastructure**: CDN, regional servers
4. **Protocol**: HTTP/2, compression

## Learning Resources

### Books
- "Designing Data-Intensive Applications" by Martin Kleppmann
- "Building Microservices" by Sam Newman
- "System Design Interview" by Alex Xu

### Online Resources
- System Design Primer GitHub
- Educative System Design courses
- Interview.io system design prep

### Practice
- Design familiar systems (Uber, Instagram)
- Whiteboard with peers
- Read production architecture docs

## Tools

### Diagramming
- **Draw.io**: Free diagramming
- **Lucidchart**: Professional diagrams
- **Excalidraw**: Quick sketches
- **Miro**: Collaborative whiteboarding

### Architecture Analysis
- **PlantUML**: Diagram as code
- **Structurizr**: Architecture as code
- **ArchiMate**: Standard notation

**Roadmap.sh Reference**: https://roadmap.sh/system-design

---

**Status**: ✅ Production Ready | **SASMP**: v1.3.0 | **Bonded Agent**: 06-architecture-specialist
