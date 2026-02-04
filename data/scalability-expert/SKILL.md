---
name: scalability-expert
description: Expert scalability design including horizontal scaling, load balancing, database scaling, and capacity planning
version: 1.0.0
author: USER
tags: [scalability, scaling, load-balancing, sharding, capacity-planning]
---

# Scalability Expert

## Purpose
Design scalable systems including horizontal scaling, load balancing, database scaling, and capacity planning strategies.

## Activation Keywords
- scalability, scaling, scale
- load balancing, horizontal scaling
- sharding, partitioning
- capacity planning, growth
- traffic spike, handle load

## Core Capabilities

### 1. Scaling Strategies
- Horizontal vs vertical
- Auto-scaling
- Predictive scaling
- Scheduled scaling
- Manual scaling

### 2. Load Balancing
- Algorithm selection
- Health checks
- Session affinity
- Geographic routing
- Weighted routing

### 3. Database Scaling
- Read replicas
- Sharding strategies
- Caching layers
- Connection pooling
- Query optimization

### 4. Capacity Planning
- Traffic forecasting
- Resource estimation
- Cost projection
- Bottleneck prediction
- Growth modeling

### 5. Stateless Design
- Session externalization
- Shared nothing architecture
- Idempotent operations
- Cache distribution

## Scaling Decision Framework

```
1. Identify Bottleneck
   → CPU, Memory, I/O, Network?
   → Single component or systemic?

2. Choose Strategy
   → Vertical: Quick fix, has limits
   → Horizontal: Sustainable, complex

3. Implement
   → Stateless application tier
   → Database scaling
   → Cache layer

4. Monitor
   → Auto-scaling metrics
   → Capacity thresholds
   → Alert on saturation
```

## Load Balancing Algorithms

| Algorithm | Use Case |
|-----------|----------|
| Round Robin | Equal capacity servers |
| Least Connections | Varying request duration |
| IP Hash | Session affinity needed |
| Weighted | Unequal server capacity |
| Geographic | Multi-region |

## Database Scaling Patterns

```
Read Scaling:
Primary → Read Replica 1
       → Read Replica 2
       → Read Replica N

Write Scaling (Sharding):
Shard Key (user_id mod N)
  → Shard 0 (0-999)
  → Shard 1 (1000-1999)
  → Shard N

Caching Layer:
App → Cache (Redis Cluster) → Database
```

## Capacity Planning Formula

```
Required Capacity =
  (Peak Traffic × Growth Factor × Safety Margin)
  ÷ (Capacity per Instance × Target Utilization)

Example:
  Peak: 10,000 RPS
  Growth: 2x (annual)
  Safety: 1.5x
  Per Instance: 500 RPS
  Target Utilization: 70%

  = (10,000 × 2 × 1.5) ÷ (500 × 0.7)
  = 30,000 ÷ 350
  = 86 instances
```

## Auto-Scaling Configuration

```yaml
# Example auto-scaling policy
scalingPolicy:
  minInstances: 3
  maxInstances: 100
  metrics:
    - type: cpu
      target: 70%
      scaleUpCooldown: 3m
      scaleDownCooldown: 10m
    - type: requestsPerSecond
      target: 1000
  predictiveScaling:
    enabled: true
    lookAheadPeriod: 1h
```

## Example Usage

```
User: "Prepare system for 10x traffic increase"

Scalability Expert Response:
1. Current state analysis
   - Bottleneck identification
   - Single points of failure
   - Resource utilization

2. Application tier
   - Ensure stateless design
   - Configure auto-scaling
   - Add load balancer capacity

3. Database tier
   - Add read replicas
   - Consider sharding if needed
   - Optimize slow queries

4. Caching
   - Redis cluster sizing
   - Cache hit ratio targets
   - Warm-up strategy

5. Infrastructure
   - CDN capacity
   - Network bandwidth
   - DNS scaling

6. Monitoring
   - Capacity dashboards
   - Scaling event alerts
   - Cost projections
```
