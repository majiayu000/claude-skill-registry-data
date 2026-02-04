---
name: backend-development-patterns
description: API design, database patterns, REST/GraphQL, microservices architecture, and backend best practices
triggers: [api, backend, REST, GraphQL, database, microservices, server, endpoint, PostgreSQL, Supabase]
version: 1.0.0
agents: [senior-fullstack-developer, database-migration-specialist, solutions-architect]
context_levels:
  minimal: Core API patterns and database best practices
  detailed: Complete architecture patterns and examples
  full: Working code examples and templates
---

# Backend Development Patterns Skill

## Overview
This skill provides comprehensive backend development patterns including API design, database architecture, authentication, and scalable backend systems.

## When to Use This Skill
- Designing and implementing REST/GraphQL APIs
- Database schema design and optimization
- Backend service architecture
- Microservices patterns
- Data layer implementation

## Core API Design Principles (Level 1 - Always Loaded)

### REST API Best Practices

**URL Structure:**
```
✅ GOOD - Resource-oriented URLs
GET    /api/users           # List users
GET    /api/users/:id       # Get specific user
POST   /api/users           # Create user
PUT    /api/users/:id       # Update user (full replace)
PATCH  /api/users/:id       # Update user (partial)
DELETE /api/users/:id       # Delete user

# Nested resources
GET    /api/users/:id/orders      # Get user's orders
POST   /api/users/:id/orders      # Create order for user

❌ BAD - Verb-based URLs
GET    /api/getUser?id=123
POST   /api/createUser
POST   /api/updateUser
POST   /api/deleteUser
```

**HTTP Status Codes:**
```typescript
// Success responses
200 OK              // Successful GET, PUT, PATCH, DELETE
201 Created         // Successful POST
204 No Content      // Successful DELETE (no response body)

// Client errors
400 Bad Request     // Invalid input data
401 Unauthorized    // Missing or invalid authentication
403 Forbidden       // Valid auth but insufficient permissions
404 Not Found       // Resource doesn't exist
409 Conflict        // Resource conflict (e.g., duplicate email)
422 Unprocessable   // Validation errors

// Server errors
500 Internal Error  // Unexpected server error
503 Service Unavail // Temporary unavailability

// Example usage
app.post('/api/users', async (req, res) => {
  try {
    const user = await userService.create(req.body);
    res.status(201).json(user); // 201 Created
  } catch (error) {
    if (error instanceof ValidationError) {
      res.status(422).json({ error: error.message }); // 422 Validation
    } else if (error instanceof ConflictError) {
      res.status(409).json({ error: error.message }); // 409 Conflict
    } else {
      res.status(500).json({ error: 'Internal server error' }); // 500
    }
  }
});
```

**Request/Response Format:**
```typescript
// ✅ GOOD - Consistent response structure
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
  meta?: {
    timestamp: string;
    requestId: string;
  };
}

// Success response
{
  "success": true,
  "data": {
    "id": "123",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "meta": {
    "timestamp": "2025-01-15T10:30:00Z",
    "requestId": "req_abc123"
  }
}

// Error response
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": {
      "field": "email",
      "value": "invalid-email"
    }
  },
  "meta": {
    "timestamp": "2025-01-15T10:30:00Z",
    "requestId": "req_abc123"
  }
}
```

### Database Design Patterns

**Schema Design Best Practices:**
```sql
-- ✅ GOOD - Proper constraints and indexes

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Index frequently queried fields
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Foreign key relationships
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  total DECIMAL(10, 2) NOT NULL CHECK (total >= 0),
  status VARCHAR(50) NOT NULL DEFAULT 'pending',
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);

-- ❌ BAD - No constraints, poor naming
CREATE TABLE user_table (
  id INT,
  mail VARCHAR(1000),
  data TEXT
);
```

**Query Optimization:**
```typescript
// ✅ GOOD - Efficient query with specific fields
async function getUserOrders(userId: string) {
  return db.query(`
    SELECT
      o.id,
      o.total,
      o.status,
      o.created_at
    FROM orders o
    WHERE o.user_id = $1
    ORDER BY o.created_at DESC
    LIMIT 20
  `, [userId]);
}

// ❌ BAD - SELECT * and no limit
async function getUserOrders(userId: string) {
  return db.query(`
    SELECT * FROM orders WHERE user_id = $1
  `, [userId]);
}

// ✅ GOOD - Avoid N+1 queries with JOIN
async function getUsersWithOrders() {
  const result = await db.query(`
    SELECT
      u.id as user_id,
      u.name,
      u.email,
      json_agg(
        json_build_object(
          'id', o.id,
          'total', o.total,
          'status', o.status
        )
      ) as orders
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
    GROUP BY u.id, u.name, u.email
  `);

  return result.rows;
}
```

### Repository Pattern

```typescript
// Generic repository interface
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  findAll(options?: FindOptions): Promise<T[]>;
  create(data: Partial<T>): Promise<T>;
  update(id: string, data: Partial<T>): Promise<T>;
  delete(id: string): Promise<boolean>;
}

// Implementation for User entity
class UserRepository implements Repository<User> {
  constructor(private db: Database) {}

  async findById(id: string): Promise<User | null> {
    const result = await this.db.query(
      'SELECT * FROM users WHERE id = $1',
      [id]
    );
    return result.rows[0] ? this.mapToUser(result.rows[0]) : null;
  }

  async findByEmail(email: string): Promise<User | null> {
    const result = await this.db.query(
      'SELECT * FROM users WHERE email = $1',
      [email]
    );
    return result.rows[0] ? this.mapToUser(result.rows[0]) : null;
  }

  async create(data: CreateUserDto): Promise<User> {
    const result = await this.db.query(
      `INSERT INTO users (email, name, password_hash)
       VALUES ($1, $2, $3)
       RETURNING *`,
      [data.email, data.name, data.passwordHash]
    );
    return this.mapToUser(result.rows[0]);
  }

  async update(id: string, data: Partial<User>): Promise<User> {
    const updates: string[] = [];
    const values: any[] = [];
    let paramCount = 1;

    Object.entries(data).forEach(([key, value]) => {
      updates.push(`${key} = $${paramCount}`);
      values.push(value);
      paramCount++;
    });

    values.push(id);

    const result = await this.db.query(
      `UPDATE users
       SET ${updates.join(', ')}, updated_at = NOW()
       WHERE id = $${paramCount}
       RETURNING *`,
      values
    );

    return this.mapToUser(result.rows[0]);
  }

  private mapToUser(row: any): User {
    return {
      id: row.id,
      email: row.email,
      name: row.name,
      createdAt: row.created_at,
      updatedAt: row.updated_at,
    };
  }
}
```

### Service Layer Pattern

```typescript
// Business logic layer
class UserService {
  constructor(
    private userRepo: UserRepository,
    private emailService: EmailService,
    private cacheService: CacheService,
    private logger: Logger
  ) {}

  async createUser(dto: CreateUserDto): Promise<User> {
    // 1. Validate input
    this.validateUserDto(dto);

    // 2. Check for duplicates
    const existing = await this.userRepo.findByEmail(dto.email);
    if (existing) {
      throw new ConflictError('Email already registered');
    }

    // 3. Hash password
    const passwordHash = await bcrypt.hash(dto.password, 12);

    // 4. Create user
    const user = await this.userRepo.create({
      email: dto.email,
      name: dto.name,
      passwordHash,
    });

    // 5. Send welcome email (async, don't block)
    this.emailService.sendWelcomeEmail(user.email)
      .catch(err => this.logger.error('Failed to send welcome email', err));

    // 6. Invalidate cache
    await this.cacheService.delete(`users:all`);

    // 7. Log event
    this.logger.info('User created', { userId: user.id });

    return user;
  }

  async getUserById(id: string): Promise<User> {
    // Try cache first
    const cacheKey = `user:${id}`;
    const cached = await this.cacheService.get<User>(cacheKey);

    if (cached) {
      return cached;
    }

    // Fetch from database
    const user = await this.userRepo.findById(id);

    if (!user) {
      throw new NotFoundError('User not found');
    }

    // Cache for 5 minutes
    await this.cacheService.set(cacheKey, user, 300);

    return user;
  }

  private validateUserDto(dto: CreateUserDto): void {
    if (!validator.isEmail(dto.email)) {
      throw new ValidationError('Invalid email format');
    }

    if (dto.password.length < 8) {
      throw new ValidationError('Password must be at least 8 characters');
    }

    if (dto.name.trim().length < 2) {
      throw new ValidationError('Name must be at least 2 characters');
    }
  }
}
```

## Authentication & Authorization

### JWT Authentication
```typescript
import jwt from 'jsonwebtoken';

interface JwtPayload {
  userId: string;
  email: string;
  role: string;
}

class AuthService {
  private readonly JWT_SECRET = process.env.JWT_SECRET!;
  private readonly JWT_EXPIRES_IN = '1h';
  private readonly REFRESH_TOKEN_EXPIRES_IN = '7d';

  generateAccessToken(user: User): string {
    const payload: JwtPayload = {
      userId: user.id,
      email: user.email,
      role: user.role,
    };

    return jwt.sign(payload, this.JWT_SECRET, {
      expiresIn: this.JWT_EXPIRES_IN,
      algorithm: 'HS256',
    });
  }

  generateRefreshToken(user: User): string {
    return jwt.sign(
      { userId: user.id },
      this.JWT_SECRET,
      { expiresIn: this.REFRESH_TOKEN_EXPIRES_IN }
    );
  }

  verifyToken(token: string): JwtPayload {
    try {
      return jwt.verify(token, this.JWT_SECRET) as JwtPayload;
    } catch (error) {
      throw new UnauthorizedError('Invalid or expired token');
    }
  }
}

// Middleware
function authenticateJWT(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;

  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing authentication token' });
  }

  const token = authHeader.substring(7);

  try {
    const payload = authService.verifyToken(token);
    req.user = payload;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
}

// Authorization middleware
function requireRole(...roles: string[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }

    next();
  };
}

// Usage
app.get('/api/admin/users', authenticateJWT, requireRole('admin'), async (req, res) => {
  // Only authenticated admins can access
  const users = await userService.getAllUsers();
  res.json(users);
});
```

## API Versioning

```typescript
// URL-based versioning
app.use('/api/v1', v1Routes);
app.use('/api/v2', v2Routes);

// v1 route (old)
v1Router.get('/users/:id', async (req, res) => {
  const user = await userService.getUser(req.params.id);
  res.json(user); // Old response format
});

// v2 route (new - includes additional fields)
v2Router.get('/users/:id', async (req, res) => {
  const user = await userService.getUser(req.params.id);
  const enriched = await userService.enrichUserData(user);
  res.json(enriched); // New response format with more data
});
```

## Pagination & Filtering

```typescript
// Query parameters for pagination
interface PaginationParams {
  page: number;
  limit: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
  filters?: Record<string, any>;
}

async function getUsers(params: PaginationParams) {
  const { page = 1, limit = 20, sortBy = 'created_at', sortOrder = 'desc' } = params;

  const offset = (page - 1) * limit;

  const result = await db.query(`
    SELECT * FROM users
    WHERE email LIKE $1
    ORDER BY ${sortBy} ${sortOrder}
    LIMIT $2 OFFSET $3
  `, [`%${params.filters?.email || ''}%`, limit, offset]);

  const countResult = await db.query('SELECT COUNT(*) FROM users');
  const total = parseInt(countResult.rows[0].count);

  return {
    data: result.rows,
    pagination: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
      hasNext: page * limit < total,
      hasPrev: page > 1,
    },
  };
}

// API endpoint
app.get('/api/users', async (req, res) => {
  const result = await getUsers({
    page: parseInt(req.query.page as string) || 1,
    limit: parseInt(req.query.limit as string) || 20,
    sortBy: req.query.sortBy as string,
    sortOrder: req.query.sortOrder as 'asc' | 'desc',
    filters: req.query.filters as any,
  });

  res.json(result);
});
```

## Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

// Global rate limit
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: 'Too many requests, please try again later',
  standardHeaders: true,
  legacyHeaders: false,
});

app.use('/api/', limiter);

// Strict limit for authentication endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // Only 5 login attempts per 15 minutes
  skipSuccessfulRequests: true,
});

app.post('/api/auth/login', authLimiter, loginHandler);
```

## Detailed Patterns (Level 2 - Load on Request)

See companion files:
- `graphql-patterns.md` - GraphQL schema design and resolvers
- `microservices-patterns.md` - Service communication and orchestration
- `caching-strategies.md` - Redis patterns and cache invalidation

## Code Examples (Level 3 - Load When Needed)

See examples directory:
- `examples/rest-api-complete.ts` - Full REST API implementation
- `examples/graphql-server.ts` - Complete GraphQL setup
- `examples/auth-flow-complete.ts` - Authentication implementation

## Integration with Agents

**senior-fullstack-developer:**
- Primary agent for backend implementation
- Uses these patterns for all API development
- References for database design

**database-migration-specialist:**
- Uses database patterns for schema design
- References optimization patterns

**solutions-architect:**
- Uses these patterns for system design
- Evaluates architecture decisions

---

*Version 1.0.0 | REST & GraphQL Ready | Scalable Patterns*
