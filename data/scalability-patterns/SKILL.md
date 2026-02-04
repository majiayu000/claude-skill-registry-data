---
name: scalability-patterns
description: Master scalability patterns with load balancing, caching, database scaling, microservices, and horizontal scaling strategies.
---

# Scalability Patterns

Implement scalability patterns to handle growth, improve performance, and maintain reliability under increasing load.

## When to Use This Skill

- Performance bottlenecks
- User growth
- Data volume increase
- High traffic events
- Geographic expansion
- Cost optimization
- Architecture modernization
- SLA requirements

## Core Concepts

### 1. Horizontal vs Vertical Scaling

```markdown
**Vertical Scaling (Scale Up):**
- Add more CPU, RAM to existing server
- Limits: Hardware ceiling, single point of failure
- Use case: Databases, legacy apps

**Horizontal Scaling (Scale Out):**
- Add more servers
- Benefits: No limit, fault tolerance
- Requires: Stateless design, load balancing
- Use case: Web servers, app servers

**Recommendation:** Design for horizontal scaling
```

### 2. Caching Strategies

```markdown
## Cache Architecture

**Cache-Aside (Lazy Loading):**
```
1. App checks cache
2. If miss, read from DB
3. Write to cache
4. Return data
```

**Write-Through:**
```
1. App writes to cache
2. Cache writes to DB
3. Return success
```

**Write-Behind:**
```
1. App writes to cache
2. Return success immediately
3. Cache async writes to DB (eventual consistency)
```

**Use Cases:**
- CDN: Static assets (images, CSS, JS)
- Redis: Session data, API responses
- Browser cache: User-specific data
- Application cache: Configuration, reference data

**Example - Redis Caching:**
```javascript
async function getUser(userId) {
  // Try cache first
  let user = await redis.get(`user:${userId}`);
  
  if (!user) {
    // Cache miss - get from database
    user = await database.query('SELECT * FROM users WHERE id = ?', [userId]);
    // Store in cache (TTL: 1 hour)
    await redis.setex(`user:${userId}`, 3600, JSON.stringify(user));
  }
  
  return JSON.parse(user);
}
```
```

### 3. Database Scaling

```markdown
## Database Scaling Strategies

**Read Replicas:**
- Master: Write operations
- Replicas: Read operations
- Reduces load on master
- Eventual consistency

**Sharding (Horizontal Partitioning):**
- Split data across multiple databases
- Shard key (e.g., user_id % num_shards)
- Challenges: Joins, resharding

**Vertical Partitioning:**
- Split tables by columns
- Separate hot/cold data
- Example: User profile vs user activity logs

**CQRS (Command Query Responsibility Segregation):**
- Separate read and write models
- Optimized for different use cases
- Event sourcing integration
```

### 4. Load Balancing

```markdown
## Load Balancer Strategies

**Round Robin:**
Server 1 → Server 2 → Server 3 → Server 1...

**Least Connections:**
Route to server with fewest active connections

**IP Hash:**
Route based on client IP (sticky sessions)

**Weighted:**
More requests to more powerful servers

**Health Checks:**
- Monitor server health
- Remove unhealthy servers
- Automatic failover

**Example Architecture:**
```
Internet → CloudFlare CDN
         → AWS ALB (Application Load Balancer)
            → Auto Scaling Group
               → EC2 Instance 1
               → EC2 Instance 2
               → EC2 Instance 3
```
```

## Best Practices

1. **Stateless design** - Store state externally (Redis, DB)
2. **Async processing** - Use message queues for heavy tasks
3. **Cache aggressively** - Multiple cache layers
4. **Database optimization** - Indexes, query optimization
5. **Monitor metrics** - CPU, memory, response time, error rate
6. **Auto-scaling** - Scale based on metrics
7. **Graceful degradation** - Reduce functionality vs complete failure
8. **Load testing** - Identify bottlenecks before production

## Resources

- **Scalability Rules**: Martin Abbott
- **High Performance Browser Networking**: Ilya Grigorik
