---
name: technical-documentation
description: Generate architecture documentation, ADRs (Architecture Decision Records), design documents, and technical specifications. Use when documenting system.
---

# Technical Documentation

Document technical architecture, design decisions, system design, and development workflows for developers and technical stakeholders.

## When to Use This Skill

Use this skill when you need to:

- Document system architecture
- Write Architecture Decision Records (ADRs)
- Create design documents
- Document data flows
- Explain module organization
- Create developer onboarding guides

**Trigger phrases**: "architecture documentation", "design document", "ADR", "technical spec", "system design", "developer guide"

## What This Skill Does

### Documentation Types

1. **Architecture Overview** - System design and components
2. **ADRs** - Architecture Decision Records
3. **Design Documents** - Feature design specs
4. **Data Flow Diagrams** - How data moves
5. **Module Documentation** - Code organization
6. **Development Guides** - Setup and workflows

## Instructions

### Architecture Overview Template

```markdown
# System Architecture

## Overview

Brief description of the system's purpose and high-level design.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Load Balancer                        │
└─────────────────────────┬───────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │  API     │    │  API     │    │  API     │
    │  Server  │    │  Server  │    │  Server  │
    └────┬─────┘    └────┬─────┘    └────┬─────┘
         │               │               │
         └───────────────┼───────────────┘
                         ▼
              ┌──────────────────┐
              │   Message Queue  │
              └────────┬─────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
    ┌─────────┐  ┌─────────┐  ┌─────────┐
    │ Worker  │  │ Worker  │  │ Worker  │
    └────┬────┘  └────┬────┘  └────┬────┘
         │            │            │
         └────────────┼────────────┘
                      ▼
              ┌──────────────┐
              │   Database   │
              └──────────────┘
```

## Components

### API Server
- **Purpose**: Handle HTTP requests, authentication, validation
- **Technology**: Python/FastAPI
- **Scaling**: Horizontal, stateless

### Message Queue
- **Purpose**: Decouple request handling from processing
- **Technology**: RabbitMQ
- **Guarantees**: At-least-once delivery

### Worker
- **Purpose**: Process async jobs
- **Technology**: Python/Celery
- **Scaling**: Horizontal based on queue depth

### Database
- **Purpose**: Persistent data storage
- **Technology**: PostgreSQL
- **Replication**: Primary-replica

## Data Flow

1. Client sends request to load balancer
2. Load balancer routes to available API server
3. API server validates and enqueues job
4. Worker picks up job and processes
5. Result stored in database
6. Client polls for completion

## Security

- TLS 1.3 for all connections
- JWT authentication
- Role-based access control
- Secrets in HashiCorp Vault

## Monitoring

- Metrics: Prometheus + Grafana
- Logging: ELK Stack
- Tracing: Jaeger
- Alerts: PagerDuty
```

### ADR Template

```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status

Accepted

## Date

2025-01-15

## Context

We need to choose a primary database for our application. Requirements:
- ACID compliance for financial transactions
- Support for complex queries
- JSON storage for flexible schemas
- Strong ecosystem and community
- Team familiarity

Options considered:
1. PostgreSQL
2. MySQL
3. MongoDB
4. CockroachDB

## Decision

We will use PostgreSQL as our primary database.

## Rationale

**Pros:**
- ACID compliant with strong consistency
- Excellent JSON/JSONB support for flexible schemas
- Advanced indexing (GIN, GiST, partial indexes)
- Team has extensive experience
- Strong open-source ecosystem
- Good performance for our scale (<1M rows)

**Cons:**
- Horizontal scaling requires more effort than MongoDB
- Not as performant for pure document workloads

**Why not alternatives:**
- MySQL: Weaker JSON support, less advanced features
- MongoDB: Eventual consistency concerns for financial data
- CockroachDB: Overkill for current scale, higher complexity

## Consequences

### Positive
- Strong data integrity guarantees
- Flexible schema evolution with JSONB
- Team productivity with familiar technology

### Negative
- Need to plan for sharding if data grows significantly
- Must manage connection pooling carefully

### Risks
- Schema migrations need careful planning
- May need to revisit for >10M rows

## Related Decisions

- ADR-002: Use PgBouncer for Connection Pooling
- ADR-003: Database Migration Strategy

## References

- [PostgreSQL Documentation](https://postgresql.org/docs/)
- [Designing Data-Intensive Applications](https://dataintensive.net/)
```

### Design Document Template

```markdown
# Design Document: User Authentication System

## Overview

### Problem Statement
Users need secure authentication to access the platform.

### Goals
- Secure authentication with industry-standard practices
- Support multiple authentication methods
- Session management with appropriate timeouts
- Audit logging for compliance

### Non-Goals
- Single Sign-On (deferred to phase 2)
- Biometric authentication

## Background

Current state: No authentication system exists.
Users: ~10,000 expected in year 1.
Compliance: SOC 2 Type II required.

## Detailed Design

### Authentication Flow

```
┌──────┐     ┌─────────┐     ┌─────────┐     ┌──────────┐
│Client│────▶│   API   │────▶│  Auth   │────▶│ Database │
└──────┘     │ Gateway │     │ Service │     └──────────┘
             └─────────┘     └─────────┘
                  │
                  ▼
             ┌─────────┐
             │  Redis  │
             │(Sessions│
             └─────────┘
```

### Components

#### AuthService
```python
class AuthService:
    def authenticate(self, email: str, password: str) -> AuthResult:
        """Validate credentials and create session."""

    def create_session(self, user_id: str) -> Session:
        """Create new authenticated session."""

    def validate_session(self, token: str) -> User | None:
        """Validate session token and return user."""

    def logout(self, token: str) -> None:
        """Invalidate session."""
```

#### Security Measures

| Measure | Implementation |
|---------|----------------|
| Password Hashing | bcrypt, cost 12 |
| Session Tokens | 256-bit random |
| Rate Limiting | 5 attempts/minute |
| Session Timeout | 24 hours |
| Secure Cookies | HttpOnly, Secure, SameSite |

### API Endpoints

```
POST /auth/login
  Request: { email, password }
  Response: { token, expires_at }

POST /auth/logout
  Headers: Authorization: Bearer <token>
  Response: { success: true }

GET /auth/me
  Headers: Authorization: Bearer <token>
  Response: { user }
```

### Data Model

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

CREATE TABLE sessions (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Alternatives Considered

### Alternative 1: OAuth2 Only
- Rejected: Need password-based auth for B2B customers

### Alternative 2: JWT without Sessions
- Rejected: Need server-side session revocation

## Security Considerations

- Password requirements: 12+ chars, complexity check
- Brute force protection via rate limiting
- Session hijacking prevention via token rotation
- CSRF protection via SameSite cookies

## Testing Strategy

- Unit tests for AuthService
- Integration tests for auth flow
- Security penetration testing
- Load testing for rate limiting

## Rollout Plan

1. Deploy to staging
2. Security review
3. Beta with 100 users
4. Full rollout

## Open Questions

- [ ] Password reset flow (separate design doc)
- [ ] MFA implementation timeline
```

### Module Documentation Template

```markdown
# Module: data_processing

## Overview

The data_processing module handles all data transformation,
validation, and export operations.

## Directory Structure

```
data_processing/
├── __init__.py
├── transformers/
│   ├── __init__.py
│   ├── base.py          # Base transformer class
│   ├── text.py          # Text transformations
│   └── numeric.py       # Numeric transformations
├── validators/
│   ├── __init__.py
│   ├── schema.py        # Schema validation
│   └── business.py      # Business rule validation
├── exporters/
│   ├── __init__.py
│   ├── json.py          # JSON export
│   └── csv.py           # CSV export
└── utils/
    ├── __init__.py
    └── helpers.py        # Shared utilities
```

## Key Classes

### Transformer (base.py)
Abstract base class for all transformers.

```python
class Transformer(ABC):
    @abstractmethod
    def transform(self, data: Any) -> Any:
        """Transform input data."""

    def validate_input(self, data: Any) -> bool:
        """Validate input before transformation."""
```

### Pipeline (pipeline.py)
Chains multiple transformers.

```python
pipeline = Pipeline([
    TextNormalizer(),
    SchemaValidator(schema),
    JsonExporter()
])
result = pipeline.process(data)
```

## Dependencies

- Internal: `config`, `logging`, `exceptions`
- External: `pydantic`, `pandas`

## Configuration

```yaml
data_processing:
  max_batch_size: 1000
  timeout_seconds: 30
  retry_attempts: 3
```

## Usage Examples

```python
from data_processing import Pipeline, TextNormalizer

# Simple transformation
normalizer = TextNormalizer()
result = normalizer.transform("  HELLO  ")  # "hello"

# Pipeline processing
pipeline = Pipeline([...])
results = pipeline.process_batch(data_list)
```
```

## Quality Checklist

- [ ] Architecture overview complete
- [ ] All components documented
- [ ] Data flows illustrated
- [ ] ADRs written for key decisions
- [ ] Module structure documented
- [ ] API contracts defined
- [ ] Security considerations covered
- [ ] Diagrams up to date
- [ ] Version numbers accurate
- [ ] Links valid

## Common Issues and Solutions

### Issue: Architecture diagrams become outdated
**Solution**: Use diagram-as-code tools (Mermaid, PlantUML) in the repository.

### Issue: Too much detail in overview docs
**Solution**: Use layers - overview links to detailed docs.

### Issue: Decisions not documented
**Solution**: Make ADRs part of the PR process for architecture changes.

## Related Skills

- `user-documentation` - User guides
- `api-documentation` - API reference
- `code-quality` - Code quality review

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates documentation_generation/technical_docs/


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
