---
name: microservices-expert
description: Expert microservices architecture including service decomposition, communication patterns, and resilience
version: 1.0.0
author: USER
tags: [microservices, distributed, service-mesh, saga, resilience]
---

# Microservices Expert

## Purpose
Design and implement microservices architectures including service decomposition, inter-service communication, and resilience patterns.

## Activation Keywords
- microservices, micro-services
- service decomposition, bounded context
- service mesh, sidecar
- saga pattern, eventual consistency
- circuit breaker, resilience

## Core Capabilities

### 1. Service Decomposition
- Domain-driven design
- Bounded contexts
- Service boundaries
- Data ownership
- API contracts

### 2. Communication Patterns
- Synchronous (REST, gRPC)
- Asynchronous (Events, Messages)
- Request/Reply
- Pub/Sub
- Event sourcing

### 3. Resilience Patterns
- Circuit breaker
- Retry with backoff
- Bulkhead
- Timeout
- Fallback

### 4. Data Management
- Database per service
- Saga pattern
- Eventual consistency
- CQRS
- Event sourcing

### 5. Service Mesh
- Istio/Linkerd
- Traffic management
- mTLS
- Observability
- Policy enforcement

## Decomposition Guidelines

```
1. Business Capabilities
   → Group by business function
   → Each service = one capability

2. Bounded Contexts (DDD)
   → Identify domain boundaries
   → Define ubiquitous language

3. Data Boundaries
   → Each service owns its data
   → No shared databases

4. Team Boundaries
   → Conway's Law
   → One team per service (ideal)
```

## Communication Decision Matrix

| Scenario | Pattern |
|----------|--------|
| Query data | Sync (REST/gRPC) |
| Command | Async (Message queue) |
| Event notification | Pub/Sub |
| Long-running process | Saga |
| Data replication | Event sourcing |

## Saga Pattern

```
Choreography:
Service A → Event → Service B → Event → Service C
         ↓ (failure)
Compensating transactions automatically triggered

Orchestration:
Orchestrator → Command → Service A
            → Command → Service B
            → Command → Service C
            → Rollback commands on failure
```

## Resilience Implementation

```typescript
// Circuit breaker example
const breaker = new CircuitBreaker(fetchData, {
  timeout: 3000,
  errorThresholdPercentage: 50,
  resetTimeout: 30000
});

breaker.fire()
  .then(data => handleSuccess(data))
  .catch(err => handleFallback(err));
```

## Example Usage

```
User: "Decompose a monolith e-commerce into microservices"

Microservices Expert Response:
1. Identify bounded contexts
   - User Management
   - Product Catalog
   - Inventory
   - Order Management
   - Payment
   - Shipping
   - Notifications

2. Define service boundaries
   - API contracts (OpenAPI)
   - Event schemas
   - Data ownership

3. Communication design
   - Order → Payment (Saga)
   - Inventory updates (Events)
   - Product queries (REST)

4. Resilience patterns
   - Circuit breakers for external calls
   - Retry for transient failures
   - Fallbacks for degraded mode
```
