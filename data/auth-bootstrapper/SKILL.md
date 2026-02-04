---
name: auth-bootstrapper
description: Adds BetterAuth authentication to Apso backends. Handles entity setup, code generation, auto-fixes, and verification. Triggers when user needs to add authentication, setup auth, or integrate BetterAuth.
---

# Auth Bootstrapper

I add production-ready BetterAuth authentication to Apso backends, giving you a fully functional authenticated REST API in under 5 minutes with zero manual steps.

## Core Capabilities

### 1. setup-backend-with-auth
**Complete backend setup from scratch with authentication**

What I automate:
- Create Apso backend project structure
- Generate .apsorc with BetterAuth entities
- Run `apso server` code generation
- Fix known integration issues automatically
- Set up environment variables
- Initialize database
- Verify all endpoints work
- Test authentication flows

**Usage:** "Setup backend with auth" or "Create new backend with authentication"

### 2. add-auth-to-existing
**Add BetterAuth to existing Apso backend**

What I automate:
- Analyze current .apsorc schema
- Detect and resolve entity naming conflicts
- Add BetterAuth entities (User, account, session, verification)
- Regenerate code with `apso server`
- Fix DTO and entity issues
- Update database schema
- Configure auth endpoints
- Test integration

**Usage:** "Add auth to my backend" or "Integrate BetterAuth"

### 3. fix-auth-issues
**Auto-fix common BetterAuth integration problems**

Issues I fix automatically:
- Missing `id` field in DTOs
- Nullable field constraints
- Entity naming conflicts
- AppModule wiring issues
- Database NOT NULL constraint errors
- CORS configuration
- Session cookie settings

**Usage:** "Fix auth issues" or "My auth isn't working"

### 4. verify-auth-setup
**Run comprehensive verification checks**

What I verify:
- Database tables exist and are correct
- All CRUD endpoints respond
- User signup flow works
- User signin flow works
- Session creation works
- Token validation works
- Multi-tenancy isolation works
- Organization auto-creation works

**Usage:** "Verify auth setup" or "Test the backend"

## The 5-Minute Setup Process

When you say **"setup backend with auth"**, I execute this fully automated workflow:

### Phase 1: Project Initialization (30 seconds)

```bash
# 1. Create backend directory
mkdir backend && cd backend

# 2. Initialize Apso project
npx apso init

# 3. Install dependencies
npm install
```

### Phase 2: Schema Configuration (1 minute)

I create `.apsorc` with:

**BetterAuth Required Entities:**
- `User` (PascalCase) - Authentication user entity
- `account` (lowercase) - OAuth/credential providers
- `session` (lowercase) - Active user sessions
- `verification` (lowercase) - Email verification tokens

**Business Entities (renamed to avoid conflicts):**
- `Organization` (NOT "Account") - Multi-tenant root
- `DiscoverySession` (NOT "Session") - Your business sessions
- Junction tables for relationships

**Critical Configuration Points:**
```json
{
  "service": "your-backend",
  "database": {
    "provider": "postgresql",
    "multiTenant": true,
    "tenantKey": "account_id"
  },
  "entities": {
    "User": {
      "fields": {
        "avatar_url": { "nullable": true },      // ← MUST be nullable
        "password_hash": { "nullable": true },   // ← MUST be nullable
        "oauth_provider": { "nullable": true },  // ← MUST be nullable
        "oauth_id": { "nullable": true }         // ← MUST be nullable
      }
    }
  }
}
```

See `references/apsorc-templates/` for complete examples.

### Phase 3: Code Generation (30 seconds)

```bash
# Generate NestJS backend
apso server

# This creates:
# - REST API controllers
# - TypeORM entities
# - DTOs with validation
# - Service layer
# - OpenAPI docs
```

### Phase 4: Automatic Fixes (1 minute)

I apply these fixes automatically (no manual intervention):

**Fix 1: Add `id` to Create DTOs**
```typescript
// backend/src/autogen/User/dtos/User.dto.ts
export class UserCreate {
  @ApiProperty()
  @IsUUID()
  id: string;  // ← I add this automatically

  // ... rest of fields
}
```

**Fix 2: Verify Nullable Fields**
```typescript
// backend/src/autogen/User/User.entity.ts
@Column({ nullable: true })  // ← I verify this is set
avatar_url: string;

@Column({ nullable: true })  // ← I verify this is set
password_hash: string;
```

**Fix 3: AppModule Wiring**
```typescript
// backend/src/app.module.ts
// I ensure all auth modules are imported
imports: [
  UserModule,
  AccountModule,
  SessionModule,
  VerificationModule,
  OrganizationModule,
  // ...
]
```

### Phase 5: Environment Setup (30 seconds)

I create `.env` files:

```bash
# .env.development
NODE_ENV=development
PORT=3001

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/backend_dev

# BetterAuth (I generate secure secrets)
BETTER_AUTH_SECRET=generated-32-char-secret
BETTER_AUTH_URL=http://localhost:3001

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3003
```

### Phase 6: Database Initialization (1 minute)

```bash
# Start PostgreSQL via Docker
docker-compose up -d

# Run migrations (TypeORM sync)
npm run start:dev

# Verify tables created
psql -U postgres -d backend_dev -c "\dt"
```

Expected tables:
- `user`
- `account`
- `session`
- `verification`
- `organization`
- `account_user`

### Phase 7: Verification & Testing (1 minute)

I run these tests automatically:

**Test 1: Server Health**
```bash
curl http://localhost:3001/health
# Expected: {"status": "ok"}
```

**Test 2: User Signup**
```bash
curl -X POST http://localhost:3001/Users \
  -H "Content-Type: application/json" \
  -d '{
    "id": "generated-uuid",
    "email": "test@example.com",
    "name": "Test User",
    "email_verified": false
  }'
# Expected: User object with ID
```

**Test 3: Database Verification**
```sql
SELECT id, email, name, email_verified FROM "user";
SELECT id, "userId", "providerId" FROM account;
SELECT COUNT(*) FROM organization;
```

**Test 4: CRUD Operations**
```bash
# GET all users
curl http://localhost:3001/Users

# GET user by ID
curl http://localhost:3001/Users/{id}

# UPDATE user
curl -X PATCH http://localhost:3001/Users/{id} \
  -d '{"name": "Updated Name"}'

# DELETE user
curl -X DELETE http://localhost:3001/Users/{id}
```

## Complete .apsorc Templates

I provide ready-to-use templates in `references/apsorc-templates/`:

### 1. minimal-auth.json
**Use for:** Simple apps with just authentication
**Includes:** User, account, session, verification, Organization

### 2. saas-platform.json
**Use for:** Full SaaS with multi-tenancy
**Includes:** Auth + Organization + Projects + Billing + Audit logs

### 3. marketplace.json
**Use for:** Multi-vendor platforms
**Includes:** Auth + Vendors + Products + Orders + Reviews

### 4. collaboration-tool.json
**Use for:** Team collaboration apps
**Includes:** Auth + Workspaces + Channels + Messages + Files

## Common Issues I Auto-Fix

### Issue 1: "null value in column 'avatar_url' violates not-null constraint"

**What I do:**
1. Check `User.entity.ts` for nullable settings
2. Update to `@Column({ nullable: true })`
3. Drop and recreate database schema
4. Verify with test insert

**Script:** `references/fix-scripts/fix-nullable-fields.sh`

### Issue 2: "null value in column 'id' of relation 'account'"

**What I do:**
1. Add `id` field to `accountCreate` DTO
2. Add `id` field to `UserCreate` DTO
3. Add `@IsUUID()` validator
4. Regenerate OpenAPI docs

**Script:** `references/fix-scripts/fix-dto-id-fields.sh`

### Issue 3: "Entity 'Account' conflicts with Better Auth"

**What I do:**
1. Detect conflict in .apsorc parsing
2. Rename `Account` → `Organization`
3. Update all foreign key references
4. Update entity descriptions
5. Regenerate code

**Script:** `references/fix-scripts/fix-entity-conflicts.sh`

### Issue 4: "AppModule doesn't import auth entities"

**What I do:**
1. Parse AppModule imports
2. Add missing module imports
3. Verify module wiring
4. Test module loading

**Script:** `references/fix-scripts/fix-app-module.sh`

## Environment Variables Management

I manage these environment files:

### `.env.development`
```bash
NODE_ENV=development
PORT=3001
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/backend_dev
BETTER_AUTH_SECRET=dev-secret-min-32-chars
BETTER_AUTH_URL=http://localhost:3001
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3003
LOG_LEVEL=debug
```

### `.env.test`
```bash
NODE_ENV=test
PORT=3002
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/backend_test
BETTER_AUTH_SECRET=test-secret-min-32-chars
LOG_LEVEL=error
```

### `.env.production` (template)
```bash
NODE_ENV=production
PORT=3001
DATABASE_URL=${DATABASE_URL}  # From AWS RDS
BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}  # From AWS Secrets Manager
BETTER_AUTH_URL=https://api.yourdomain.com
ALLOWED_ORIGINS=https://yourdomain.com
LOG_LEVEL=info
```

## Verification Checklist

Before marking setup as complete, I verify:

**Backend Services:**
- [ ] Server starts without errors (port 3001)
- [ ] Database connection successful
- [ ] All tables created in database
- [ ] OpenAPI docs accessible at /api/docs
- [ ] Health endpoint returns 200

**Entity Endpoints:**
- [ ] GET /Users returns 200
- [ ] POST /Users creates user
- [ ] GET /accounts returns 200
- [ ] GET /sessions returns 200
- [ ] GET /verifications returns 200
- [ ] GET /Organizations returns 200

**Authentication Flow:**
- [ ] User signup creates user + account
- [ ] User signin validates credentials
- [ ] Session creation works
- [ ] Token validation works
- [ ] Password hashing works

**Multi-Tenancy (via scopeBy):**
- [ ] Organization auto-created on signup
- [ ] User-Organization link created
- [ ] Queries scoped to organizationId via ScopeGuard
- [ ] Cross-tenant access blocked by scope verification

**Data Integrity:**
- [ ] Foreign keys enforced
- [ ] Unique constraints work
- [ ] Nullable fields accept null
- [ ] Required fields reject null
- [ ] Enums validate values

## Generated API Documentation

After setup, you get interactive docs at `http://localhost:3001/api/docs`

**Endpoints per entity:**
- `GET /{entity}` - List all (paginated, filtered)
- `GET /{entity}/{id}` - Get by ID
- `POST /{entity}` - Create new
- `PUT /{entity}/{id}` - Full update
- `PATCH /{entity}/{id}` - Partial update
- `DELETE /{entity}/{id}` - Delete

**Built-in features:**
- Pagination: `?page=1&limit=10`
- Sorting: `?sort=created_at&order=desc`
- Filtering: `?status=active`
- Search: `?search=keyword`
- Relations: `?include=organization,user`

## File Structure Created

```
backend/
├── src/
│   ├── autogen/              # ⚠️ NEVER MODIFY - Auto-generated by Apso
│   │   ├── User/
│   │   │   ├── User.entity.ts
│   │   │   ├── User.controller.ts
│   │   │   ├── User.service.ts
│   │   │   └── dtos/User.dto.ts
│   │   ├── account/
│   │   ├── session/
│   │   ├── verification/
│   │   ├── Organization/
│   │   └── guards/           # ⚠️ AUTO-GENERATED - Auth & scope guards
│   │       ├── auth.guard.ts     # AuthGuard for session validation
│   │       ├── scope.guard.ts    # ScopeGuard for multi-tenant data isolation
│   │       ├── guards.module.ts  # NestJS module for guards
│   │       └── index.ts          # Barrel exports
│   │
│   ├── extensions/           # ✅ Your custom code (safe to modify)
│   │   ├── auth/
│   │   │   ├── auth.decorator.ts
│   │   │   └── auth.service.ts
│   │   └── organization/
│   │       └── organization.hooks.ts
│   │
│   ├── common/
│   │   ├── filters/
│   │   ├── interceptors/
│   │   └── pipes/
│   │
│   ├── app.module.ts
│   └── main.ts
│
├── test/
│   ├── e2e/
│   │   ├── auth.e2e-spec.ts
│   │   └── users.e2e-spec.ts
│   └── unit/
│
├── .apsorc                   # Schema definition
├── .env.development
├── .env.test
├── docker-compose.yml
├── package.json
└── README.md
```

**Important:** Guards are now generated inside `src/autogen/guards/` to clearly indicate they are auto-generated and should not be manually edited. All files in `autogen/` are overwritten on every `apso server scaffold` run.

## Troubleshooting Commands

I provide these commands for debugging:

```bash
# Check database connection
npm run db:ping

# View all tables
npm run db:tables

# Run migrations
npm run db:migrate

# Seed test data
npm run db:seed

# Reset database
npm run db:reset

# View logs
npm run logs

# Test all endpoints
npm run test:e2e

# Generate new migration
npm run migration:generate -- -n AddAuthTables
```

## CRITICAL: Better Auth Architecture

**Understanding how Better Auth stores credentials is essential for debugging!**

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    Better Auth Data Model                                 │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  User table:              account table:                                  │
│  ┌────────────────┐       ┌─────────────────────────────┐                │
│  │ id             │       │ id                          │                │
│  │ email          │───────│ userId                      │                │
│  │ name           │   1:N │ providerId = "credential"   │ ← CRITICAL!    │
│  │ email_verified │       │ password (bcrypt hash)      │ ← Password!    │
│  │ avatar_url     │       │ accountId                   │                │
│  └────────────────┘       └─────────────────────────────┘                │
│                                                                           │
│  KEY INSIGHT: Passwords are in the ACCOUNT table, NOT the User table!    │
│                                                                           │
│  Sign-in flow:                                                            │
│  1. Better Auth calls: findUserByEmail(email, { includeAccounts: true }) │
│  2. Adapter returns user WITH accounts array populated                    │
│  3. Better Auth finds: user.accounts.find(a => a.providerId === "credential")
│  4. Password verified against account.password (bcrypt)                   │
│                                                                           │
│  If providerId is undefined/null → Login ALWAYS fails!                   │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

### Why Signup Works But Login Fails

The most common issue is: signup succeeds but login fails with "Invalid email or password".

**Root Cause:** The `account.providerId` field is not being set to `"credential"` during account creation, OR the adapter isn't returning it correctly during user lookup.

**Solution:**
1. Use `@apso/better-auth-adapter@2.0.2` or higher
2. Ensure `.apsorc` has `providerId` field in account entity
3. Verify database: `SELECT "providerId" FROM account;` should show `"credential"`

## Integration with Frontend

After backend setup, I guide you to:

1. **Install BetterAuth adapter in frontend (CRITICAL: use v2.0.2+):**
   ```bash
   cd frontend
   npm install better-auth @apso/better-auth-adapter@latest
   ```

2. **Configure auth client:**
   ```typescript
   // frontend/lib/auth.ts
   import { betterAuth } from 'better-auth';
   import { createApsoAdapter } from '@apso/better-auth-adapter';

   export const auth = betterAuth({
     database: createApsoAdapter({
       baseUrl: process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:3001',
     }),
     emailAndPassword: { enabled: true },
   });
   ```

3. **Test end-to-end flow (BOTH signup AND login!):**
   - Frontend signup → Backend creates user + account with providerId="credential"
   - Frontend signin → Backend validates via account.password (NOT user.password_hash!)
   - Frontend protected route → Backend validates token

## Reference Documentation

All in `references/`:

- `apsorc-templates/` - Complete .apsorc examples
- `fix-scripts/` - Automated fix scripts
- `verification-commands/` - Test commands
- `troubleshooting/` - Common issues & solutions
- `better-auth-integration.md` - Complete auth guide

## Success Metrics

**Setup time:** < 5 minutes from start to working API
**Manual steps:** 0 (fully automated)
**Error rate:** < 5% (auto-fixes handle most issues)
**Test coverage:** 100% of CRUD endpoints verified

## Ready to Start?

Just say:
- **"Setup backend with auth"** - Complete new backend
- **"Add auth to backend"** - Add to existing backend
- **"Fix auth issues"** - Debug current setup
- **"Verify backend"** - Run all checks

I'll handle everything automatically and show you exactly what's happening at each step.
