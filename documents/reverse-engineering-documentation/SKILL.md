---
name: Reverse-Engineering Documentation
description: Creating documentation from legacy code when none exists, focusing on what future maintainers need to know
when_to_use: when legacy codebase has no documentation and you need to create it from code analysis for future maintainers
version: 1.0.0
languages: all
---

# Reverse-Engineering Documentation

## Overview

Good documentation answers questions before they're asked. Reverse-engineered documentation captures what you learned the hard way, so others don't have to.

**Core principle:** Document for the next person (who might be future you). What did you wish existed when you started?

## When to Use

Create reverse-engineered documentation when:
- Legacy code has no (or outdated) documentation
- You've just finished understanding a complex system
- Before leaving a project (knowledge transfer)
- After debugging a subtle issue
- Implementing a feature taught you how system works

**Document while fresh.** Wait a week and you'll forget the insights.

## What to Document

### 1. Architecture Overview (START HERE)

**Purpose:** 30,000-foot view before diving into details.

**Include:**
```markdown
## Architecture

### System Components
- **Web API** (Node.js/Express) - REST endpoints for client
- **Background Workers** (Bull queues) - Async processing
- **Database** (PostgreSQL) - User data, transactions
- **Cache** (Redis) - Session storage, rate limiting
- **File Storage** (S3) - User uploads

### Data Flow
User Request → API → Validate → Queue Job → Worker → Database → Response

### Key Patterns
- Repository pattern for data access
- Factory pattern for worker creation
- Strategy pattern for payment processors
```

### 2. Entry Points

**What triggers the code to run?**

```markdown
## Entry Points

### HTTP Endpoints
- `POST /api/users` → `UserController.create()` → Creates new user
- `GET /api/orders/:id` → `OrderController.get()` → Fetches order details

### Background Jobs
- `process-payment` → `PaymentWorker.handle()` → Processes queued payments
- `send-email` → `EmailWorker.handle()` → Sends notification emails

### Scheduled Tasks
- `daily-cleanup` (runs 2am UTC) → Removes old sessions
```

### 3. Critical Paths

**The code that matters most.**

```markdown
## Critical User Flows

### User Registration
1. POST /api/register → `UserController.register()`
2. Validate email/password → `ValidationService.validateUser()`
3. Hash password → `bcrypt.hash()`
4. Create user → `UserRepository.create()`
5. Send welcome email → Queue `send-email` job
6. Return JWT token → `TokenService.generate()`

**Failure modes:**
- Duplicate email → Returns 400 with "Email already exists"
- Invalid password → Returns 400 with validation errors
- DB error → Returns 500, logs error, email not sent
```

### 4. Configuration

**Where are the knobs?**

```markdown
## Configuration

### Environment Variables
- `DATABASE_URL` - PostgreSQL connection string (required)
- `REDIS_URL` - Redis connection for sessions/queues (required)
- `JWT_SECRET` - Token signing key (required, rotate monthly)
- `MAX_UPLOAD_SIZE` - File upload limit (default: 10MB)

### Feature Flags
- `ENABLE_NEW_CHECKOUT` - New checkout flow (default: false)
- `ENABLE_SOCIAL_LOGIN` - OAuth providers (default: true)

### Important Constants
- Token expiry: 24 hours (`config/auth.js:12`)
- Rate limit: 100 req/min per IP (`config/rateLimit.js:5`)
```

### 5. Known Issues and Gotchas

**Landmines for future developers.**

```markdown
## Known Issues

### Critical Bugs
1. **Race condition in payment processing** (`PaymentWorker.js:145`)
   - If two workers process same payment → double charge
   - Workaround: Redis lock with 30s timeout
   - TODO: Add idempotency key

2. **Memory leak in file uploads** (`FileController.js:67`)
   - Large files (>50MB) not properly streamed
   - Workaround: Upload size limit set to 10MB
   - TODO: Implement streaming

### Gotchas
- Sessions stored in Redis, not DB → Lost on Redis restart
- Background jobs retry 3 times then fail silently
- PostgreSQL connection pool size=20 → Increase for >1000 users
```

### 6. Testing

**How to verify it works.**

```markdown
## Testing

### Running Tests
```bash
npm test              # Unit tests
npm run test:integration  # Integration tests
npm run test:e2e     # End-to-end tests
```

### Test Coverage
- Unit tests: 75% coverage (target: 80%)
- Critical paths: 95% coverage
- Known gaps: Background workers (20% coverage)

### Manual Testing
1. Create user: `curl -X POST http://localhost:3000/api/register -d '{"email":"test@example.com","password":"Test123!"}'`
2. Login: `curl -X POST http://localhost:3000/api/login -d '{"email":"test@example.com","password":"Test123!"}'`
```

## Documentation Templates

### Quick Start Template

```markdown
# [System Name]

## What is this?
[One paragraph: What does this system do? Who uses it?]

## Quick Start
1. Install dependencies: `npm install`
2. Set environment variables: Copy `.env.example` to `.env`
3. Start database: `docker-compose up -d`
4. Run migrations: `npm run migrate`
5. Start server: `npm start`

## Architecture
[Diagram or bullet list of main components]

## Key Concepts
- **[Concept 1]**: [Definition]
- **[Concept 2]**: [Definition]

## Common Tasks
- [Task]: [How to do it]
```

### Decision Record Template

```markdown
# ADR-001: [Decision Title]

## Context
[What problem are we solving? What constraints exist?]

## Decision
[What did we decide to do?]

## Rationale
[Why this decision? What alternatives were considered?]

## Consequences
[What are the trade-offs? What becomes easier/harder?]

## Date
[When was this decided?]
```

## Checklist

- [ ] Architecture overview with components and data flow
- [ ] Entry points (endpoints, jobs, scheduled tasks)
- [ ] Critical user flows with failure modes
- [ ] Configuration (env vars, feature flags, constants)
- [ ] Known issues and workarounds
- [ ] Testing instructions
- [ ] Quick start guide for new developers
- [ ] Decision records for important choices

## Anti-Patterns

### ❌ Documenting Implementation Details

**Bad:** "Line 145 calls bcrypt.hash() with cost factor 10"
**Good:** "Passwords are hashed with bcrypt (cost factor 10 for security/performance balance)"

Document WHAT and WHY, not HOW (code shows how).

### ❌ Copying Code into Docs

**Bad:** *Paste 50 lines of code*
**Good:** "See `UserController.register()` for registration flow"

Link to code, don't duplicate it. Code changes, docs go stale.

### ❌ Writing for Yourself Today

**Bad:** "The thing does the stuff"
**Good:** "The PaymentWorker processes queued payment jobs asynchronously"

Write for someone with zero context.

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| "Code is self-documenting" | Code shows how, not why. Document intent. |
| "I'll document it later" | Later = never. Document while it's fresh. |
| "Too much to document" | Start with architecture and critical paths. Expand over time. |
| "Documentation will get outdated" | Outdated docs with kernel of truth > no docs. |

## Integration with Other Skills

- **skills/analysis/code-archaeology** - Document what you learned while analyzing
- **skills/understanding/mental-model-building** - Documentation captures mental models
- **skills/research/tracing-knowledge-lineages** - Decision records preserve history

## Remember

- Document for next person (future you)
- Start with architecture overview
- Focus on WHY and WHAT, not HOW
- Capture known issues and gotchas
- Document while knowledge is fresh
- Perfect documentation doesn't exist - good enough documentation prevents pain
