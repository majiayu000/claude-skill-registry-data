---
name: docs-generation"
description: Generates and maintains documentation including API docs, READMEs, architecture decision records, and changelogs. Use when creating or updating project documentation.
---

# Documentation Generation Skill

## Documentation Types

### 1. README.md (Project Entry Point)

```markdown
# Project Name

> One-line description of what this project does.

## Features
- Feature 1
- Feature 2
- Feature 3

## Quick Start
```bash
# Install
npm install

# Development
npm run dev

# Build
npm run build

# Test
npm test
```

## Configuration
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PORT` | No | `3000` | Server port |
| `DATABASE_URL` | Yes | - | PostgreSQL connection |

## API Reference
See [API Documentation](./docs/api.md)

## Architecture
See [Architecture Decision Records](./docs/adr/)

## Contributing
See [CONTRIBUTING.md](./CONTRIBUTING.md)

## License
MIT
```

### 2. API Documentation (OpenAPI/Swagger)

```yaml
# docs/api/openapi.yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
  description: User management endpoints

servers:
  - url: https://api.example.com/v1

paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema: { type: integer, default: 1 }
        - name: limit
          in: query
          schema: { type: integer, default: 20 }
      responses:
        '200':
          description: Paginated user list
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedUsers'

  /users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema: { type: string, format: uuid }
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: User not found

components:
  schemas:
    User:
      type: object
      properties:
        id: { type: string, format: uuid }
        email: { type: string, format: email }
        name: { type: string }
        createdAt: { type: string, format: date-time }
    PaginatedUsers:
      type: object
      properties:
        data:
          type: array
          items: { $ref: '#/components/schemas/User' }
        page: { type: integer }
        limit: { type: integer }
        total: { type: integer }
```

### 3. Architecture Decision Records (ADR)

```markdown
# docs/adr/001-use-postgresql.md

# ADR 001: Use PostgreSQL as Primary Database

## Status
Accepted

## Context
We need a relational database for:
- Complex queries with joins
- ACID transactions
- JSON support for flexible schemas
- Strong consistency requirements

## Decision
Use PostgreSQL 15+ as the primary database.

## Alternatives Considered
| Option | Pros | Cons |
|--------|------|------|
| MySQL | Widely known | Limited JSON, no CTEs |
| MongoDB | Flexible schema | No ACID, eventual consistency |
| SQLite | Zero config | Not for production scale |

## Consequences
- **Positive**: Mature ecosystem, great tooling, JSONB support
- **Negative**: Operational overhead (backups, replication)
- **Mitigation**: Use managed service (RDS, Cloud SQL)

## Implementation
- Connection pooling with PgBouncer
- Read replicas for scaling reads
- Automated backups with point-in-time recovery
```

### 4. Changelog (Keep a Changelog Format)

```markdown
# CHANGELOG.md

## [1.2.0] - 2024-01-15

### Added
- User profile API endpoints (`GET/PUT /api/users/:id/profile`)
- Dark mode support in UI
- Export to CSV feature

### Changed
- **BREAKING**: User API now returns `createdAt` instead of `created_at`
- Improved login performance by 40%
- Updated dependencies to latest versions

### Deprecated
- `GET /api/users/:id/settings` (use `/profile` instead)

### Removed
- Legacy authentication endpoint `/api/auth/legacy`

### Fixed
- Race condition in order processing
- Memory leak in WebSocket connections

### Security
- Updated vulnerable dependency `lodash` from 4.17.20 to 4.17.21
```

### 5. Code Comments (JSDoc/TSDoc)

```typescript
/**
 * Calculates shipping cost for an order.
 * 
 * @param order - The order to calculate shipping for
 * @param options - Shipping calculation options
 * @returns The shipping cost in cents
 * @throws {ValidationError} If order is invalid
 * @example
 * const cost = calculateShipping(order, { method: 'express' });
 */
function calculateShipping(
  order: Order,
  options: ShippingOptions = { method: 'standard' }
): number {
  // Implementation
}
```

## Automation

### Generate API Docs from Code
```bash
# TypeScript -> OpenAPI
npx tsoa spec-and-routes

# Python FastAPI -> OpenAPI
python -c "from app.main import app; print(app.openapi())" > openapi.json

# Generate client SDKs
npx openapi-generator-cli generate -i openapi.json -g typescript-axios -o ./client
```

### Generate README from Package.json
```bash
npx readme-generator
```

### Validate Links
```bash
npx markdown-link-check README.md
```

## Templates Location

Store templates in `.github/docs-templates/`:
- `README.md.template`
- `ADR.md.template`
- `CHANGELOG.md.template`
- `CONTRIBUTING.md.template`

## When to Use

- Creating new project documentation
- Updating API documentation after changes
- Writing ADRs for architectural decisions
- Maintaining changelogs for releases
- Documenting complex business logic
- Onboarding new team members