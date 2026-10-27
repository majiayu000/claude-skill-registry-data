---
name: "scalability"
description: 'Design scalable systems with horizontal scaling, load balancing, caching, message queues, and stateless services. Use when planning system capacity, implementing load balancers, adding message queues for async processing, or designing stateless microservices architecture.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
---

# Scalability

> **Purpose**: Design systems that handle growth in users, data, and traffic. 
> **Approaches**: Horizontal scaling, load balancing, caching, async processing, stateless services.

---

## When to Use This Skill

- Planning system capacity and scaling strategy
- Implementing load balancing or auto-scaling
- Adding message queues for async processing
- Designing stateless microservices
- Configuring database read replicas or sharding

## Prerequisites

- Basic understanding of distributed systems
- Cloud platform access

## Decision Tree

```
Scaling concern?
+- Current bottleneck?
| +- Single server at capacity? -> Horizontal scaling (add instances)
| +- Database overloaded? -> Read replicas + connection pooling
| +- Too many synchronous calls? -> Message queue (async processing)
| - Repeated expensive queries? -> Caching layer (Redis/CDN)
+- Architecture decision?
| +- Stateful servers? -> Make stateless (externalize session/state)
| +- Monolith too large? -> Extract bounded contexts to services
| - Need global reach? -> CDN + multi-region deployment
- Data scaling?
 +- Read-heavy? -> Read replicas + cache
 +- Write-heavy? -> Sharding or partitioning
 - Both? -> CQRS pattern (separate read/write models)
```

## Horizontal vs Vertical Scaling

| Approach | Description | When to Use |
|----------|-------------|-------------|
| **Vertical** | Bigger server (more CPU/RAM) | Quick fix, limited by hardware |
| **Horizontal** | More servers | Long-term, unlimited growth |

**Prefer horizontal scaling** - Add more instances rather than bigger servers.

---

## Stateless Services

```csharp
// [FAIL] Stateful (doesn't scale)
public class OrderController : ControllerBase
{
 private static Dictionary<int, Order> _orders = new(); // Shared state!
 
 [HttpPost]
 public IActionResult CreateOrder(Order order)
 {
 _orders[order.Id] = order; // Lost on restart or different instance
 return Ok();
 }
}

// [PASS] Stateless (scales horizontally)
public class OrderController : ControllerBase
{
 private readonly IOrderRepository _repository;
 
 [HttpPost]
 public async Task<IActionResult> CreateOrder(Order order)
 {
 await _repository.SaveAsync(order); // Persisted to database
 return Ok();
 }
}
```

---

## Load Balancing

```yaml
# NGINX load balancer config
upstream api_servers {
 least_conn; # Route to server with fewest connections
 server api1:5000;
 server api2:5000;
 server api3:5000;
}

server {
 listen 80;
 location / {
 proxy_pass http://api_servers;
 proxy_set_header Host $host;
 proxy_set_header X-Real-IP $remote_addr;
 }
}
```

**Strategies**:
- **Round Robin** - Distribute evenly
- **Least Connections** - Route to least busy
- **IP Hash** - Same client -> same server

---

## Caching Strategy

```csharp
// Cache frequently accessed data
public class ProductService
{
 private readonly IDistributedCache _cache;
 private readonly IProductRepository _repo;
 
 public async Task<Product> GetProductAsync(int id)
 {
 var cacheKey = $"product:{id}";
 var cached = await _cache.GetStringAsync(cacheKey);
 
 if (cached != null)
 return JsonSerializer.Deserialize<Product>(cached);
 
 var product = await _repo.GetByIdAsync(id);
 await _cache.SetStringAsync(cacheKey, 
 JsonSerializer.Serialize(product),
 new DistributedCacheEntryOptions
 {
 AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10)
 });
 
 return product;
 }
}
```

---

## Message Queues (Async Processing)

```csharp
using RabbitMQ.Client;

// Producer - Queue heavy operations
public class OrderService
{
 private readonly IConnection _connection;
 
 public async Task<Order> CreateOrderAsync(OrderDto orderDto)
 {
 var order = await _repository.CreateAsync(orderDto);
 
 // Queue email and inventory update (don't block)
 await _queue.PublishAsync("order.created", new
 {
 OrderId = order.Id,
 CustomerEmail = order.CustomerEmail
 });
 
 return order;
 }
}

// Consumer - Process in background
public class OrderProcessor : BackgroundService
{
 protected override async Task ExecuteAsync(CancellationToken stoppingToken)
 {
 await _queue.SubscribeAsync("order.created", async message =>
 {
 await _emailService.SendOrderConfirmationAsync(message.OrderId);
 await _inventoryService.UpdateStockAsync(message.OrderId);
 });
 }
}
```

---

## Database Scaling

### Read Replicas

```csharp
// Write to primary
builder.Services.AddDbContext<AppDbContext>(options =>
 options.UseNpgsql(builder.Configuration.GetConnectionString("Primary")));

// Read from replicas
builder.Services.AddDbContext<ReadDbContext>(options =>
 options.UseNpgsql(builder.Configuration.GetConnectionString("ReadReplica")));

public class UserService
{
 private readonly AppDbContext _writeDb;
 private readonly ReadDbContext _readDb;
 
 public async Task<User> GetUserAsync(int id) =>
 await _readDb.Users.FindAsync(id); // Read from replica
 
 public async Task CreateUserAsync(User user)
 {
 _writeDb.Users.Add(user);
 await _writeDb.SaveChangesAsync(); // Write to primary
 }
}
```

### Database Sharding

```csharp
// Shard by user ID
public class ShardedUserRepository
{
 private readonly List<AppDbContext> _shards;
 
 private AppDbContext GetShard(int userId)
 {
 var shardIndex = userId % _shards.Count;
 return _shards[shardIndex];
 }
 
 public async Task<User> GetUserAsync(int userId)
 {
 var shard = GetShard(userId);
 return await shard.Users.FindAsync(userId);
 }
}
```

---

## CDN for Static Assets

```csharp
// Use CDN for images, CSS, JS
<img src="https://cdn.myapp.com/images/logo.png" />
<link href="https://cdn.myapp.com/css/styles.css" rel="stylesheet" />

// Configure CDN
builder.Services.Configure<StaticFileOptions>(options =>
{
 options.OnPrepareResponse = ctx =>
 {
 ctx.Context.Response.Headers.Add("Cache-Control", "public,max-age=31536000");
 };
});
```

---

## Rate Limiting

```csharp
using AspNetCoreRateLimit;

builder.Services.Configure<IpRateLimitOptions>(options =>
{
 options.GeneralRules = new List<RateLimitRule>
 {
 new RateLimitRule
 {
 Endpoint = "*",
 Period = "1m",
 Limit = 100
 }
 };
});

app.UseIpRateLimiting();
```

---

## Autoscaling

```yaml
# Kubernetes HPA (Horizontal Pod Autoscaler)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
 name: api-autoscaler
spec:
 scaleTargetRef:
 apiVersion: apps/v1
 kind: Deployment
 name: api
 minReplicas: 2
 maxReplicas: 10
 metrics:
 - type: Resource
 resource:
 name: cpu
 target:
 type: Utilization
 averageUtilization: 70
```

---

## Best Practices

### [PASS] DO

- **Design stateless** - Store state in database/cache
- **Use load balancers** - Distribute traffic
- **Cache aggressively** - Reduce database load
- **Queue heavy operations** - Process asynchronously
- **Use read replicas** - Separate read/write load
- **Enable autoscaling** - Handle traffic spikes
- **Use CDN** - Serve static assets globally
- **Implement rate limiting** - Prevent abuse
- **Monitor metrics** - CPU, memory, request rate
- **Plan for failure** - Circuit breakers, retries

### [FAIL] DON'T

- **Store state in memory** - Breaks horizontal scaling
- **Single database instance** - Bottleneck
- **Synchronous heavy operations** - Use queues
- **Skip caching** - Database overload
- **Ignore connection pooling** - Connection exhaustion
- **Manual scaling only** - Use autoscaling
- **Serve static files from app** - Use CDN
- **No rate limiting** - Vulnerable to abuse

---

## Scalability Checklist

- [ ] Services are stateless
- [ ] Load balancer configured
- [ ] Caching implemented (Redis/Memory)
- [ ] Message queue for async processing
- [ ] Database read replicas configured
- [ ] CDN for static assets
- [ ] Rate limiting enabled
- [ ] Autoscaling configured
- [ ] Connection pooling enabled
- [ ] Monitoring and alerting set up

---

**See Also**: [Performance](../performance/SKILL.md) - [Database](../database/SKILL.md) - [Logging & Monitoring](../../development/logging-monitoring/SKILL.md)

**Last Updated**: January 13, 2026

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Session state lost after scaling | Use distributed cache (Redis) or JWT tokens for stateless sessions |
| Message queue backlog growing | Add consumer instances, implement dead-letter queues for poison messages |
| Database bottleneck with read replicas | Ensure read queries route to replicas and write queries to primary |