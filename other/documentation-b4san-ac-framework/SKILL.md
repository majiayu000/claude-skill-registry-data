---
name: documentation
description: Generate clear documentation for each task including technical descriptions, architecture diagrams, and usage guides. Use when documenting completed features, creating README files, writing API documentation, generating architecture diagrams, or maintaining project documentation. Ensures knowledge is preserved and accessible.
license: MIT
metadata:
  author: AC Framework
  version: "1.0"
---

# Documentation

Automated generation and maintenance of technical documentation, architecture diagrams, and usage guides.

## When to Use This Skill

Use this skill when:
- Documenting a completed feature or change
- Creating or updating README files
- Writing API documentation
- Generating architecture diagrams (Mermaid, PlantUML)
- Maintaining project documentation
- Creating user guides or developer onboarding docs
- Documenting design decisions (ADRs)

## Instructions

### Step 1: Analyze Documentation Needs

1. **Identify the audience**:
   - Developers (technical details)
   - End users (usage guides)
   - DevOps (deployment docs)
   - New team members (onboarding)

2. **Determine document type**:
   - README (project overview)
   - API docs (endpoints, requests, responses)
   - Architecture docs (diagrams, decisions)
   - User guides (step-by-step instructions)
   - Changelog (release notes)

3. **Check existing docs**:
   - What's already documented?
   - What's outdated?
   - What's missing?

### Step 2: Generate README.md

Structure for project README:

```markdown
# Project Name

Brief description of what this project does.

## Features

- Feature 1: Brief description
- Feature 2: Brief description
- Feature 3: Brief description

## Installation

\`\`\`bash
# Clone the repository
git clone https://github.com/user/repo.git

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env

# Run database migrations
npm run migrate
\`\`\`

## Usage

### Quick Start

\`\`\`bash
# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm test
\`\`\`

### Configuration

Describe configuration options here.

## API Documentation

See [API.md](docs/API.md) for detailed API documentation.

## Architecture

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design details.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

[MIT](LICENSE)
```

### Step 3: Generate API Documentation

Document each endpoint:

```markdown
## Endpoint: POST /api/users

Create a new user account.

### Request

\`\`\`http
POST /api/users
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securePassword123"
}
\`\`\`

### Response

**Success (201 Created)**:
\`\`\`json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "John Doe",
  "email": "john@example.com",
  "createdAt": "2024-01-15T10:30:00Z"
}
\`\`\`

**Error (400 Bad Request)**:
\`\`\`json
{
  "error": "Validation failed",
  "details": [
    { "field": "email", "message": "Invalid email format" }
  ]
}
\`\`\`

### Authentication

Requires Bearer token in Authorization header.

### Notes

- Email must be unique
- Password minimum 8 characters
- Rate limited to 10 requests per minute
```

### Step 4: Create Architecture Diagrams

Use Mermaid for diagrams:

**System Architecture**:
```markdown
\`\`\`mermaid
graph TB
    Client[Client Browser] -->|HTTP| LB[Load Balancer]
    LB -->|Route| API[API Gateway]
    API -->|Auth| Auth[Auth Service]
    API -->|Request| App[Application Server]
    App -->|Query| DB[(Database)]
    App -->|Cache| Redis[(Redis)]
    App -->|Queue| MQ[Message Queue]
    MQ -->|Process| Worker[Background Worker]
\`\`\`
```

**Data Flow**:
```markdown
\`\`\`mermaid
sequenceDiagram
    participant User
    participant API
    participant Service
    participant DB
    
    User->>API: POST /orders
    API->>Service: createOrder(data)
    Service->>DB: INSERT INTO orders
    DB-->>Service: order_id
    Service-->>API: Order created
    API-->>User: 201 Created
\`\`\`
```

**Component Diagram**:
```markdown
\`\`\`mermaid
classDiagram
    class User {
        +String id
        +String name
        +String email
        +login()
        +logout()
    }
    
    class Order {
        +String id
        +String userId
        +Date createdAt
        +calculateTotal()
    }
    
    User "1" --> "*" Order : places
\`\`\`
```

### Step 5: Write Technical Documentation

Document modules/components:

```markdown
## Module: Authentication

### Purpose

Handles user authentication and session management.

### Components

#### AuthService

**Location**: `src/services/auth.js`

**Methods**:
- `login(email, password)`: Authenticate user
- `logout()`: End user session
- `validateToken(token)`: Verify JWT token
- `refreshToken(token)`: Get new access token

**Usage**:
\`\`\`javascript
import { AuthService } from './services/auth';

const auth = new AuthService();
const user = await auth.login('user@example.com', 'password');
\`\`\`

### Configuration

\`\`\`javascript
{
  jwtSecret: process.env.JWT_SECRET,
  expiresIn: '24h',
  refreshExpiresIn: '7d'
}
\`\`\`

### Dependencies

- jsonwebtoken: JWT handling
- bcrypt: Password hashing
- User model: Database operations
```

### Step 6: Create Usage Guides

Step-by-step guides for common tasks:

```markdown
## How to Add a New Feature

### 1. Create a Change

\`\`\`bash
acfm spec new my-feature
\`\`\`

### 2. Write Proposal

Edit `.acfm/changes/my-feature/proposal.md`

### 3. Design Specifications

Create files in `.acfm/changes/my-feature/specs/`

### 4. Implement

Run the apply command:
\`\`\`bash
acfm spec apply my-feature
\`\`\`

### 5. Verify

\`\`\`bash
acfm spec verify my-feature
\`\`\`

### 6. Archive

\`\`\`bash
acfm spec archive my-feature
\`\`\`
```

### Step 7: Document Design Decisions (ADRs)

Architecture Decision Records:

```markdown
# ADR 001: Use PostgreSQL as Primary Database

## Status

Accepted

## Context

We needed a relational database for structured data with complex queries.

## Decision

Use PostgreSQL as our primary database.

## Consequences

**Positive**:
- ACID compliance
- Rich query capabilities
- JSON support for flexible schemas
- Strong community

**Negative**:
- Requires database migrations
- Vertical scaling limitations
- Operational complexity

## Alternatives Considered

- **MySQL**: Good, but less feature-rich
- **MongoDB**: Better for unstructured data, but we need relations
- **DynamoDB**: Good for simple queries, complex joins are difficult

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
```

### Step 8: Verify Documentation

1. **Check completeness**:
   - All features documented?
   - All APIs covered?
   - All environment variables listed?

2. **Check accuracy**:
   - Code examples work?
   - URLs are correct?
   - Configuration values accurate?

3. **Check links**:
   - Internal links work
   - External links are valid
   - Images display correctly

4. **Check formatting**:
   - Markdown renders correctly
   - Code blocks have language tags
   - Tables are readable

### Step 9: Link to OpenSpec Artifacts

Reference OpenSpec changes in documentation:

```markdown
## Recent Changes

- [User Authentication](.acfm/changes/user-auth/) - Implemented JWT-based auth
- [API Rate Limiting](.acfm/changes/rate-limit/) - Added rate limiting middleware
- [Database Migration](.acfm/changes/db-migration/) - Migrated to PostgreSQL 15
```

## Output Format

After documentation is complete:

```
## Documentation Summary

**Files Created**:
- README.md (updated)
- docs/API.md (new)
- docs/ARCHITECTURE.md (new)
- docs/GUIDE.md (new)
- docs/adr/001-postgresql.md (new)

**Diagrams Generated**:
- System architecture (Mermaid)
- Data flow sequence (Mermaid)
- Component diagram (Mermaid)

**Skills Referenced**:
- openspec-new-change
- openspec-continue-change
- vercel-react-best-practices
```

## Guardrails

- **Keep it concise** - Don't document the obvious
- **Update incrementally** - Update docs with each change
- **Use examples** - Show, don't just tell
- **Version your docs** - Mark API versions clearly
- **Test code examples** - Ensure they actually work
- **Link related docs** - Help readers navigate

## Requirements

- Understanding of the codebase
- Access to Mermaid or PlantUML for diagrams
- Knowledge of Markdown
- Familiarity with the target audience

## See Also

- `sync-index` - Keep docs in sync with code
- `changelog-generator` - Generate release notes
- `openspec-archive-change` - Document archived changes
- `skill-writer` - Document new skills
