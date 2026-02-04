---
name: backend-bootstrapper
description: Bootstraps complete backend with Apso, including API setup, database configuration, and testing. Triggers when user needs to create backend, setup API, or initialize server.
---

# Backend Bootstrapper

I set up production-ready backends using Apso, giving you a fully functional REST API in minutes.

## What I Create

### 1. Apso Service Configuration
Complete `.apsorc` schema file with:
- All entities defined
- Relationships configured
- Validation rules
- Indexes optimized
- Multi-tenancy enabled

### 2. Generated NestJS Backend
Apso auto-generates:
- REST API with OpenAPI docs
- CRUD endpoints for all entities
- TypeORM models
- Database migrations
- Validation middleware
- Error handling
- Logging

### 3. Database Setup
- PostgreSQL database (local or AWS RDS)
- All tables created
- Relationships enforced
- Migrations ready
- Seed data (optional)

### 4. Development Environment
- Docker Compose for local database
- Environment variable configuration
- Development server running
- Hot reload enabled

### 5. API Documentation
- OpenAPI/Swagger documentation
- Interactive API testing UI
- Type definitions exported
- Example requests

## The Bootstrap Process

### Step 1: Validate Schema
I'll review the schema from `schema-architect` and:
- Check for missing fields
- Validate relationships
- Ensure multi-tenancy
- Add recommended indexes
- Suggest optimizations

### Step 2: Create Apso Project
```bash
# Install Apso CLI
npm install -g @apso/apso-cli

# Create new service
apso server new --name your-service-backend

# Navigate to project
cd your-service-backend
```

### Step 3: Configure Schema
I'll create the `.apsorc` file with your entities:

```json
{
  "service": "your-service-api",
  "version": "1.0.0",
  "database": {
    "provider": "postgresql",
    "host": "localhost",
    "port": 5432,
    "database": "your_service_db"
  },
  "auth": {
    "enabled": true,
    "provider": "better-auth"
  },
  "multiTenant": true,
  "entities": {
    // Your schema here
  }
}
```

### Step 4: Generate Code
```bash
# Generate NestJS backend
apso server scaffold

# This creates:
# src/
#   autogen/        ← Generated code (DON'T EDIT)
#   extensions/     ← Your custom code
#   common/         ← Shared utilities
#   main.ts         ← Entry point
```

### Step 5: Install Dependencies
```bash
npm install
```

### Step 6: Start Database
```bash
# Start PostgreSQL via Docker
npm run compose

# This starts:
# - PostgreSQL on port 5432
# - pgAdmin on port 5050 (optional)
```

### Step 7: Provision Database
```bash
# Create tables and run migrations
npm run provision

# This:
# - Creates all tables
# - Sets up foreign keys
# - Creates indexes
# - Runs seed data (if any)
```

### Step 8: Start Development Server
```bash
# Start backend server
npm run start:dev

# Server runs at:
# - API: http://localhost:3001
# - OpenAPI Docs: http://localhost:3001/api/docs
# - Health Check: http://localhost:3001/health
```

### Step 9: Verify & Test
I'll test all endpoints:

```bash
# Health check
curl http://localhost:3001/health

# Test CRUD endpoints
curl http://localhost:3001/organizations
curl http://localhost:3001/users
curl http://localhost:3001/projects
```

## Generated API Structure

For each entity, you get:

### Standard REST Endpoints

**List**
```
GET /entities
Query params: ?page=1&limit=10&sort=created_at&order=desc
Response: { data: [...], total: 100, page: 1, limit: 10 }
```

**Get by ID**
```
GET /entities/:id
Response: { id, ...fields }
```

**Create**
```
POST /entities
Body: { field1: value1, field2: value2 }
Response: { id, ...fields, created_at, updated_at }
```

**Update**
```
PUT /entities/:id
PATCH /entities/:id  (partial update)
Body: { field1: newValue }
Response: { id, ...fields, updated_at }
```

**Delete**
```
DELETE /entities/:id
Response: { success: true }
```

### Filtering & Querying

**Filter by field**
```
GET /entities?status=active
GET /entities?created_at_gte=2024-01-01
```

**Full-text search**
```
GET /entities?search=keyword
```

**Relations**
```
GET /entities?include=relations
GET /organizations/123/users  (nested route)
```

**Aggregations**
```
GET /entities/count
GET /entities/stats
```

## Automatic Features

### 1. Multi-Tenancy
Every request is automatically scoped to the organization:

```typescript
// Middleware adds organization context
@UseGuards(OrgGuard)
export class ProjectController {
  // All queries filtered by req.organizationId
  async findAll(@Req() req) {
    // Only returns projects for req.organizationId
  }
}
```

### 2. Validation
Input validation with class-validator:

```typescript
// Automatically validated
class CreateProjectDto {
  @IsString()
  @MinLength(3)
  @MaxLength(100)
  name: string;

  @IsEnum(['active', 'archived'])
  status: string;
}
```

### 3. Error Handling
Consistent error responses:

```json
{
  "statusCode": 400,
  "message": "Validation failed",
  "errors": [
    {
      "field": "name",
      "message": "name must be at least 3 characters"
    }
  ]
}
```

### 4. Logging
Structured logging with Winston:

```typescript
// Automatic logging of:
// - All requests
// - Errors
// - Database queries
// - Performance metrics
```

### 5. OpenAPI Documentation
Interactive docs at `/api/docs`:

- All endpoints documented
- Request/response schemas
- Try-it-out functionality
- Example requests

## File Structure

```
your-service-backend/
├── src/
│   ├── autogen/              ← ⚠️ NEVER MODIFY - Generated by Apso
│   │   ├── Organization/     ← Entity-specific modules
│   │   │   ├── Organization.entity.ts
│   │   │   ├── Organization.service.ts
│   │   │   ├── Organization.controller.ts
│   │   │   └── Organization.module.ts
│   │   ├── User/
│   │   ├── guards/           ← ⚠️ AUTO-GENERATED - Auth & scope guards
│   │   │   ├── auth.guard.ts     # AuthGuard for session validation
│   │   │   ├── scope.guard.ts    # ScopeGuard for multi-tenant data isolation
│   │   │   ├── guards.module.ts  # NestJS module for guards
│   │   │   └── index.ts          # Barrel exports
│   │   └── index.ts
│   │
│   ├── extensions/           ← ✅ YOUR CUSTOM CODE (safe to modify)
│   │   ├── Organization/
│   │   │   ├── Organization.controller.ts   (add custom endpoints)
│   │   │   └── Organization.service.ts      (add business logic)
│   │   ├── User/
│   │   ├── Project/
│   │   └── auth/             (Better Auth integration)
│   │
│   ├── common/               ← Shared utilities
│   │   ├── interceptors/
│   │   ├── decorators/
│   │   └── filters/
│   │
│   └── main.ts               ← App entry point
│
├── test/                     ← Tests
│   ├── unit/
│   └── e2e/
│
├── .apsorc                   ← Schema definition
├── docker-compose.yml        ← Local database
├── package.json
└── README.md
```

**Important:** Guards are now generated inside `src/autogen/guards/` to clearly indicate they are auto-generated. All files in `autogen/` are overwritten on every `apso server scaffold` run.

## Customization Options

### Adding Custom Endpoints

```typescript
// src/extensions/Project/Project.controller.ts
import { Controller, Post, Param } from '@nestjs/common';

@Controller('projects')
export class ProjectController {
  // Add custom endpoint
  @Post(':id/archive')
  async archive(@Param('id') id: string) {
    // Your custom logic
    return this.projectService.archive(id);
  }

  @Get(':id/statistics')
  async getStats(@Param('id') id: string) {
    // Custom aggregation
    return this.projectService.getStatistics(id);
  }
}
```

### Adding Business Logic

```typescript
// src/extensions/Project/Project.service.ts
import { Injectable } from '@nestjs/common';

@Injectable()
export class ProjectService {
  async archive(id: string) {
    // Complex business logic
    const project = await this.findOne(id);

    // Archive all tasks
    await this.taskService.archiveByProject(id);

    // Update project status
    return this.update(id, { status: 'archived' });
  }
}
```

### Adding Middleware

```typescript
// src/common/interceptors/logging.interceptor.ts
@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler) {
    const req = context.switchToHttp().getRequest();
    const { method, url } = req;

    console.log(`${method} ${url}`);

    return next.handle();
  }
}
```

## Environment Configuration

I'll create `.env` files:

```bash
# .env (local development)
NODE_ENV=development
PORT=3001

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_service_db
DB_USER=postgres
DB_PASSWORD=postgres

# Better Auth
AUTH_SECRET=your-secret-key-here
AUTH_URL=http://localhost:3001

# AWS (for production)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

## Testing

I'll set up testing structure:

```typescript
// test/e2e/project.e2e-spec.ts
describe('ProjectController (e2e)', () => {
  let app: INestApplication;

  beforeEach(async () => {
    const moduleFixture = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  it('/projects (GET)', () => {
    return request(app.getHttpServer())
      .get('/projects')
      .expect(200)
      .expect((res) => {
        expect(res.body.data).toBeInstanceOf(Array);
      });
  });

  it('/projects (POST)', () => {
    return request(app.getHttpServer())
      .post('/projects')
      .send({ name: 'Test Project', organization_id: '...' })
      .expect(201)
      .expect((res) => {
        expect(res.body.name).toBe('Test Project');
      });
  });
});
```

## Verification Checklist

Before marking bootstrap as complete, I verify:

- ✅ Server starts without errors
- ✅ Database connection successful
- ✅ All tables created
- ✅ OpenAPI docs accessible
- ✅ CRUD endpoints work for all entities
- ✅ Multi-tenancy filtering active
- ✅ Validation works on create/update
- ✅ Error handling returns proper responses
- ✅ Environment variables configured
- ✅ Docker Compose running

## Common Issues & Solutions

**Issue:** "Cannot connect to database"
**Fix:** Ensure `npm run compose` is running and ports aren't conflicting

**Issue:** "Module not found"
**Fix:** Run `npm install` after generating code

**Issue:** "TypeORM entity not found"
**Fix:** Run `npm run provision` to sync schema

**Issue:** "Port 3001 already in use"
**Fix:** Kill existing process: `lsof -ti:3001 | xargs kill`

## What's Next?

After bootstrap, you're ready for:
1. **Frontend Setup** - Call `frontend-bootstrapper`
2. **Authentication** - Call `auth-implementer`
3. **Custom Endpoints** - Add business logic to extensions/
4. **Testing** - Call `test-generator`

## Ready?

I'll bootstrap a production-ready backend in about 5 minutes. Just provide your schema (or I can call `schema-architect` first if you don't have one yet).

**Do you have a schema ready, or should I design one first?**
