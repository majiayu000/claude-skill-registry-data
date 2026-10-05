---
name: microservices-patterns
type: reference
description: "Provides microservices design patterns for service decomposition, API gateway, circuit breakers, saga orchestration, and inter-service communication. Use when designing or implementing microservices architecture."
paths: ["**/docker-compose*", "**/k8s/**", "**/services/**"]
effort: 4
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
user-invocable: true
when_to_use: "When designing microservices architecture, implementing service communication, or decomposing monoliths"
---

# Microservices Patterns

Service decomposition, communication, resilience, and orchestration patterns.

## Service Decomposition

| Pattern | Description | Use When |
|---------|-------------|----------|
| Domain-Driven | Align services with bounded contexts | Complex business domains |
| Data-Ownership | Service owns its data store | Data isolation required |
| Team-Aligned | One service per team | Large organizations |

## Communication Patterns

### Sync: HTTP/gRPC
\`\`\`yaml
# API Gateway routing
routes:
  - match: { prefix: /orders }
    route: { cluster: order-service }
  - match: { prefix: /users }
    route: { cluster: user-service }
\`\`\`

### Async: Message Queue
\`\`\`
Producer → Exchange → Queue → Consumer
         (Topic)   (DLQ on failure)
\`\`\`

Use async for: event propagation, eventual consistency, load leveling.

## Resilience Patterns

### Circuit Breaker
\`\`\`typescript
// Example with opossum
const breaker = new CircuitBreaker(fetchUserProfile, {
  timeout: 3000,
  errorThresholdPercentage: 50,
  resetTimeout: 30000,
});
\`\`\`

### Retry with Backoff
\`\`\`typescript
async function retryWithBackoff(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try { return await fn(); }
    catch (e) { await sleep(Math.pow(2, i) * 1000); }
  }
  throw new Error('Max retries exceeded');
}
\`\`\`

## Data Patterns

| Pattern | Consistency | Complexity | Use When |
|---------|-------------|------------|----------|
| Saga (orchestration) | Eventual | High | Complex multi-service transactions |
| Saga (choreography) | Eventual | Medium | Simple event chains |
| Event sourcing | Eventual | High | Audit trail, time travel |
| Shared database | Strong | Low | Anti-pattern, avoid |

## API Gateway

Tools: Kong, AWS API Gateway, Envoy, NGINX.

Responsibilities: routing, auth, rate limiting, request transformation, load balancing.

## Observability Stack

- Distributed tracing: Jaeger / Tempo
- Metrics: Prometheus + Grafana
- Logs: ELK / Loki
- Service mesh: Istio / Linkerd (adds mTLS, traffic management)

## Related Skills

- `backend-architect` — single-service architecture
- `event-sourcing-architect` — event sourcing patterns
- `kubernetes-architect` — deployment patterns
- `deployment-engineer` — CI/CD for microservices
