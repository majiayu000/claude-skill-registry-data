---
name: backend-api-patterns
description: Backend and API implementation patterns for scalability, security, and maintainability. Use when building APIs, services, and backend infrastructure.
---

This skill provides backend and API implementation patterns for building robust, scalable services.

## When to Invoke This Skill

Automatically activate for:
- API endpoint implementation
- Database operations and queries
- Authentication and authorization
- Caching and performance optimization
- Service architecture design

## API Design Patterns

### Consistent Response Structure

```typescript
// Standard API response envelope
interface ApiResponse<T> {
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
  };
  meta?: {
    pagination?: {
      page: number;
      pageSize: number;
      total: number;
      totalPages: number;
    };
    timestamp?: string;
    requestId?: string;
  };
}

// Success response helper
function success<T>(data: T, meta?: ApiResponse<T>['meta']): ApiResponse<T> {
  return { data, meta };
}

// Error response helper
function error(
  code: string,
  message: string,
  details?: Record<string, unknown>
): ApiResponse<never> {
  return { error: { code, message, details } };
}

// Paginated response helper
function paginated<T>(
  data: T[],
  page: number,
  pageSize: number,
  total: number
): ApiResponse<T[]> {
  return {
    data,
    meta: {
      pagination: {
        page,
        pageSize,
        total,
        totalPages: Math.ceil(total / pageSize),
      },
    },
  };
}
```

### Route Handler Pattern

```typescript
// Generic handler wrapper with error handling
type Handler<T> = (
  req: Request,
  context: { params: Record<string, string> }
) => Promise<T>;

function createHandler<T>(handler: Handler<T>) {
  return async (req: Request, context: { params: Record<string, string> }) => {
    const requestId = crypto.randomUUID();

    try {
      const result = await handler(req, context);
      return Response.json(success(result, { requestId }));
    } catch (err) {
      if (err instanceof AppError) {
        return Response.json(
          error(err.code, err.message),
          { status: err.statusCode }
        );
      }

      console.error(`[${requestId}] Unexpected error:`, err);
      return Response.json(
        error('INTERNAL_ERROR', 'An unexpected error occurred'),
        { status: 500 }
      );
    }
  };
}

// Usage
export const GET = createHandler(async (req, { params }) => {
  const user = await userService.findById(params.id);
  if (!user) throw new NotFoundError('User', params.id);
  return user;
});
```

## Service Layer Pattern

### Repository Pattern

```typescript
interface Repository<T, ID = string> {
  findById(id: ID): Promise<T | null>;
  findMany(options: FindOptions<T>): Promise<T[]>;
  count(filter?: Partial<T>): Promise<number>;
  create(data: CreateInput<T>): Promise<T>;
  update(id: ID, data: UpdateInput<T>): Promise<T>;
  delete(id: ID): Promise<void>;
}

interface FindOptions<T> {
  filter?: Partial<T>;
  orderBy?: keyof T;
  orderDir?: 'asc' | 'desc';
  limit?: number;
  offset?: number;
}

type CreateInput<T> = Omit<T, 'id' | 'createdAt' | 'updatedAt'>;
type UpdateInput<T> = Partial<Omit<T, 'id' | 'createdAt' | 'updatedAt'>>;

// Implementation
class UserRepository implements Repository<User> {
  constructor(private db: Database) {}

  async findById(id: string): Promise<User | null> {
    return this.db.query.users.findFirst({
      where: eq(users.id, id),
    });
  }

  async findMany(options: FindOptions<User>): Promise<User[]> {
    const { filter, orderBy, orderDir = 'asc', limit, offset } = options;

    return this.db.query.users.findMany({
      where: filter ? this.buildWhere(filter) : undefined,
      orderBy: orderBy ? (orderDir === 'asc' ? asc : desc)(users[orderBy]) : undefined,
      limit,
      offset,
    });
  }

  // ... other methods
}
```

### Service with Business Logic

```typescript
class UserService {
  constructor(
    private userRepo: Repository<User>,
    private cache: Cache,
    private eventBus: EventBus
  ) {}

  async getUser(id: string): Promise<User> {
    // Check cache first
    const cached = await this.cache.get<User>(`user:${id}`);
    if (cached) return cached;

    // Fetch from database
    const user = await this.userRepo.findById(id);
    if (!user) throw new NotFoundError('User', id);

    // Cache for future requests
    await this.cache.set(`user:${id}`, user, { ttl: 3600 });

    return user;
  }

  async createUser(input: CreateUserInput): Promise<User> {
    // Validate
    const existing = await this.userRepo.findMany({
      filter: { email: input.email },
      limit: 1,
    });
    if (existing.length > 0) {
      throw new ValidationError('Email already exists', { email: 'Already in use' });
    }

    // Hash password
    const hashedPassword = await hashPassword(input.password);

    // Create user
    const user = await this.userRepo.create({
      ...input,
      password: hashedPassword,
    });

    // Emit event for side effects
    await this.eventBus.emit('user.created', { userId: user.id });

    return user;
  }

  async updateUser(id: string, input: UpdateUserInput): Promise<User> {
    const user = await this.userRepo.update(id, input);

    // Invalidate cache
    await this.cache.delete(`user:${id}`);

    return user;
  }
}
```

## Authentication Patterns

### JWT with Refresh Tokens

```typescript
interface TokenPair {
  accessToken: string;   // Short-lived: 15 minutes
  refreshToken: string;  // Long-lived: 7 days
}

interface TokenPayload {
  sub: string;           // User ID
  email: string;
  roles: string[];
  type: 'access' | 'refresh';
}

class AuthService {
  constructor(
    private userRepo: Repository<User>,
    private tokenRepo: Repository<RefreshToken>,
    private jwtSecret: string
  ) {}

  async login(email: string, password: string): Promise<TokenPair> {
    const user = await this.userRepo.findMany({
      filter: { email },
      limit: 1,
    });

    if (!user[0] || !await verifyPassword(password, user[0].password)) {
      throw new UnauthorizedError('Invalid credentials');
    }

    return this.generateTokenPair(user[0]);
  }

  async refresh(refreshToken: string): Promise<TokenPair> {
    // Verify token
    const payload = this.verifyToken(refreshToken);
    if (payload.type !== 'refresh') {
      throw new UnauthorizedError('Invalid token type');
    }

    // Check if token is revoked
    const stored = await this.tokenRepo.findById(refreshToken);
    if (!stored || stored.revoked) {
      throw new UnauthorizedError('Token revoked');
    }

    // Get user and generate new tokens
    const user = await this.userRepo.findById(payload.sub);
    if (!user) throw new UnauthorizedError('User not found');

    // Revoke old refresh token
    await this.tokenRepo.update(refreshToken, { revoked: true });

    return this.generateTokenPair(user);
  }

  private generateTokenPair(user: User): TokenPair {
    const accessToken = jwt.sign(
      { sub: user.id, email: user.email, roles: user.roles, type: 'access' },
      this.jwtSecret,
      { expiresIn: '15m' }
    );

    const refreshToken = jwt.sign(
      { sub: user.id, type: 'refresh' },
      this.jwtSecret,
      { expiresIn: '7d' }
    );

    return { accessToken, refreshToken };
  }

  private verifyToken(token: string): TokenPayload {
    try {
      return jwt.verify(token, this.jwtSecret) as TokenPayload;
    } catch {
      throw new UnauthorizedError('Invalid or expired token');
    }
  }
}
```

### Middleware Pattern

```typescript
type Middleware = (req: Request, next: () => Promise<Response>) => Promise<Response>;

// Auth middleware
function authMiddleware(requiredRoles?: string[]): Middleware {
  return async (req, next) => {
    const token = req.headers.get('Authorization')?.replace('Bearer ', '');

    if (!token) {
      return Response.json(
        error('UNAUTHORIZED', 'No token provided'),
        { status: 401 }
      );
    }

    try {
      const payload = verifyToken(token);

      if (requiredRoles?.length && !requiredRoles.some(r => payload.roles.includes(r))) {
        return Response.json(
          error('FORBIDDEN', 'Insufficient permissions'),
          { status: 403 }
        );
      }

      // Attach user to request context
      (req as any).user = payload;

      return next();
    } catch {
      return Response.json(
        error('UNAUTHORIZED', 'Invalid or expired token'),
        { status: 401 }
      );
    }
  };
}

// Rate limiting middleware
function rateLimitMiddleware(limit: number, windowMs: number): Middleware {
  const requests = new Map<string, { count: number; resetAt: number }>();

  return async (req, next) => {
    const ip = req.headers.get('x-forwarded-for') || 'unknown';
    const now = Date.now();

    const record = requests.get(ip);

    if (!record || record.resetAt < now) {
      requests.set(ip, { count: 1, resetAt: now + windowMs });
      return next();
    }

    if (record.count >= limit) {
      return Response.json(
        error('RATE_LIMITED', 'Too many requests'),
        { status: 429 }
      );
    }

    record.count++;
    return next();
  };
}
```

## Database Patterns

### Query Optimization

```typescript
// Avoid N+1 queries with eager loading
async function getUsersWithOrders(): Promise<UserWithOrders[]> {
  // BAD: N+1 queries
  const users = await db.query.users.findMany();
  for (const user of users) {
    user.orders = await db.query.orders.findMany({
      where: eq(orders.userId, user.id),
    });
  }

  // GOOD: Single query with join
  return db.query.users.findMany({
    with: {
      orders: true,
    },
  });
}

// Pagination with cursor
async function paginateUsers(cursor?: string, limit = 20): Promise<{
  users: User[];
  nextCursor: string | null;
}> {
  const users = await db.query.users.findMany({
    where: cursor ? gt(users.id, cursor) : undefined,
    orderBy: asc(users.id),
    limit: limit + 1, // Fetch one extra to check for next page
  });

  const hasMore = users.length > limit;
  const data = hasMore ? users.slice(0, -1) : users;

  return {
    users: data,
    nextCursor: hasMore ? data[data.length - 1].id : null,
  };
}
```

### Transaction Pattern

```typescript
async function transferFunds(
  fromId: string,
  toId: string,
  amount: number
): Promise<void> {
  await db.transaction(async (tx) => {
    // Lock rows for update
    const from = await tx.query.accounts.findFirst({
      where: eq(accounts.id, fromId),
      for: 'update',
    });

    if (!from || from.balance < amount) {
      throw new ValidationError('Insufficient funds', {});
    }

    // Debit source account
    await tx.update(accounts)
      .set({ balance: from.balance - amount })
      .where(eq(accounts.id, fromId));

    // Credit destination account
    await tx.update(accounts)
      .set({ balance: sql`${accounts.balance} + ${amount}` })
      .where(eq(accounts.id, toId));

    // Log transaction
    await tx.insert(transactions).values({
      fromId,
      toId,
      amount,
      type: 'transfer',
    });
  });
}
```

## Caching Patterns

### Cache-Aside Pattern

```typescript
class CachedUserService {
  constructor(
    private userRepo: Repository<User>,
    private cache: Cache
  ) {}

  async getUser(id: string): Promise<User | null> {
    const cacheKey = `user:${id}`;

    // Try cache first
    const cached = await this.cache.get<User>(cacheKey);
    if (cached) return cached;

    // Fetch from database
    const user = await this.userRepo.findById(id);

    // Cache the result (including null to prevent cache stampede)
    if (user) {
      await this.cache.set(cacheKey, user, { ttl: 3600 });
    } else {
      await this.cache.set(cacheKey, null, { ttl: 60 }); // Short TTL for negative cache
    }

    return user;
  }

  async updateUser(id: string, data: UpdateUserInput): Promise<User> {
    const user = await this.userRepo.update(id, data);

    // Invalidate cache
    await this.cache.delete(`user:${id}`);

    return user;
  }
}
```

### Request Deduplication

```typescript
class RequestDeduplicator {
  private pending = new Map<string, Promise<unknown>>();

  async dedupe<T>(key: string, fetcher: () => Promise<T>): Promise<T> {
    // Return existing request if in flight
    const existing = this.pending.get(key);
    if (existing) return existing as Promise<T>;

    // Start new request
    const promise = fetcher().finally(() => {
      this.pending.delete(key);
    });

    this.pending.set(key, promise);
    return promise;
  }
}

// Usage
const deduplicator = new RequestDeduplicator();

async function getUser(id: string): Promise<User> {
  return deduplicator.dedupe(`user:${id}`, () => userRepo.findById(id));
}
```

## Best Practices Checklist

- [ ] Use consistent API response envelope
- [ ] Implement proper error hierarchy and handling
- [ ] Separate concerns: routes → services → repositories
- [ ] Use transactions for multi-step operations
- [ ] Implement caching with proper invalidation
- [ ] Avoid N+1 queries with eager loading
- [ ] Use cursor-based pagination for large datasets
- [ ] Implement rate limiting and request deduplication
- [ ] Validate inputs at API boundaries
- [ ] Log with structured data and request IDs
