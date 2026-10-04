---
name: api-gateway-designer
version: "2.0"
trigger: API gateway, microservice communication, API design, route patterns
description: Design and implement scalable API gateways, RESTful APIs, GraphQL endpoints, WebSocket handlers, and microservice communication patterns. Use when creating API routes, designing endpoints, implementing middleware, or setting up service mesh architectures.
---

# API Gateway Designer

## REST API Patterns

### Resource-Oriented Endpoints
```typescript
router.get('/api/users', requireAuth, async (req, res) => {
  const users = await userService.list(req.query);
  res.json({ data: users, meta: { total: users.length } });
});

router.post('/api/users', requireAuth, async (req, res) => {
  const user = await userService.create(req.body);
  res.status(201).json({ data: user });
});

router.get('/api/users/:id', requireAuth, async (req, res) => {
  const user = await userService.getById(req.params.id);
  if (!user) throw new NotFoundError('User not found');
  res.json({ data: user });
});
```

### Query Builder with Pagination
```typescript
class QueryBuilder<T> {
  build() {
    let q = db.select().from(this.table);
    if (this.query.filter) {
      q = q.where(and(...conditions));
    }
    q = q.limit(this.query.limit).offset((this.query.page - 1) * this.query.limit);
    return q;
  }
}
```

## GraphQL Schema

```typescript
builder.prismaObject('User', {
  fields: (t) => ({
    id: t.exposeID('id'),
    email: t.exposeString('email'),
    posts: t.relation('posts'),
  })
});

builder.queryType({
  fields: (t) => ({
    user: t.prismaField({
      type: 'User',
      args: { id: t.arg.id({ required: true }) },
      resolve: (query, _, args) => db.user.findUnique({ ...query, where: { id: args.id } })
    })
  })
});
```

## WebSocket Handler

```typescript
export class WebSocketManager {
  broadcast(channel: string, payload: unknown) {
    this.clients.forEach(client => {
      if (client.subscriptions.has(channel)) {
        client.send(JSON.stringify({ channel, payload }));
      }
    });
  }
}
```

## Middleware

```typescript
export const rateLimitMiddleware = async (req, res, next) => {
  try {
    await rateLimiter.consume(req.user?.id || req.ip);
    next();
  } catch {
    res.status(429).json({ error: 'Too many requests' });
  }
};
```

## Protocol

1. **Assess** — Understand the specific requirement and context
2. **Plan** — Determine the approach based on the guidance above
3. **Execute** — Apply the api gateway designer methodology
4. **Verify** — Validate the output against expected standards
5. **Report** — Document results and any issues encountered
