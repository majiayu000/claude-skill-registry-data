---
name: Foundry Agent Pattern
description: Convert Product Requirements Documents (PRDs) into technical blueprints and implementation plans
model: opus-4.5
---

# Foundry Agent Pattern

## File Paths & Versioning

**Input:**
- `project-docs/prd/prd-latest.md` — Latest PRD from Refinery

**Output:**
- `project-docs/blueprint/blueprint-v{N}.md` — Versioned blueprint
- `project-docs/blueprint/blueprint-latest.md` — Copy of the latest version

**Workflow:**
1. Read `project-docs/prd/prd-latest.md`
2. Detect next version number (check existing `blueprint-v*.md` files)
3. Generate `blueprint-v{N}.md`
4. Update `blueprint-latest.md` to match

**Version Header:** Each blueprint includes:
```markdown
---
version: 1
date: 2025-12-18
prd_version: 1
changes_from_previous: null | "Summary of changes"
---
```

## Purpose

The Foundry Agent is the second stage in the software factory workflow. It transforms Product Requirements Documents (PRDs) into detailed technical blueprints that define the architecture, technology choices, and implementation strategies for building the software.

## When to Use This Pattern

Use the Foundry Agent pattern when:
- You have a complete PRD that needs technical design
- You need to translate business requirements into technical specifications
- You're planning the architecture for a new system or major feature
- You need to evaluate technology choices and design patterns

## Core Responsibilities

### 1. Requirements Analysis
**Transform PRD requirements into technical needs:**
- Parse feature requirements
- Identify technical constraints
- Analyze performance requirements
- Extract integration points
- Understand scalability needs

### 2. Architecture Design
**Create system architecture:**
- Define overall system structure
- Choose architectural patterns (MVC, microservices, event-driven, etc.)
- Design data flow and communication patterns
- Plan service boundaries
- Design for scalability and maintainability

### 3. Technology Selection
**Choose appropriate technologies:**
- Programming languages and frameworks
- Databases and data stores
- APIs and communication protocols
- Third-party services and integrations
- Development and deployment tools

### 4. Implementation Strategy
**Define how to build the system:**
- Break down into buildable components
- Define interfaces and contracts
- Plan data models and schemas
- Design API endpoints
- Establish coding patterns and conventions

### 5. Blueprint Documentation
**Create comprehensive technical documentation:**
- System architecture diagrams
- Data models and schemas
- API specifications
- Component interaction diagrams
- Technical decisions and rationale

## Implementation Approach

### Step 1: Analyze the PRD

```
PRD → Technical Analysis → Technical Requirements
```

**Extract:**
- **Functional requirements**: What the system must do
- **Non-functional requirements**: Performance, security, scalability
- **Data requirements**: What data is stored, processed, transmitted
- **Integration requirements**: External systems to connect with
- **User volume and scale**: Expected traffic and growth

**Questions to answer:**
- What are the critical performance requirements?
- What are the security and compliance needs?
- What's the expected scale (users, data, requests)?
- What existing systems must we integrate with?
- What are the deployment constraints?

### Step 2: Design System Architecture

```
Technical Requirements → Architecture Design → System Blueprint
```

**Architecture decisions:**

**Frontend Architecture:**
- Single Page Application (SPA) vs Server-Side Rendering (SSR)
- State management approach
- Component structure
- Routing strategy
- UI framework choice

**Backend Architecture:**
- Monolith vs Microservices vs Serverless
- API design (REST, GraphQL, gRPC)
- Authentication and authorization strategy
- Caching layers
- Background job processing

**Data Architecture:**
- Database choice (SQL, NoSQL, hybrid)
- Data modeling approach
- Caching strategy (Redis, CDN)
- Search infrastructure
- Real-time data handling

**Infrastructure:**
- Deployment platform (cloud, on-premise, hybrid)
- Containerization strategy
- CI/CD pipeline design
- Monitoring and logging
- Backup and disaster recovery

### Step 3: Define Technology Stack

```
Architecture Design → Technology Evaluation → Technology Stack
```

**Evaluation criteria:**
- Team expertise and learning curve
- Community support and ecosystem
- Performance characteristics
- Licensing and cost
- Long-term maintenance and support

**Common stacks:**

**Web Application:**
```
Frontend: React/Vue/Svelte + TypeScript
Backend: Node.js/Python/Go + Express/FastAPI/Gin
Database: PostgreSQL/MongoDB
Cache: Redis
Deploy: Docker + AWS/GCP/Vercel
```

**Mobile Application:**
```
Mobile: React Native/Flutter
Backend: Node.js/Python with REST/GraphQL
Database: PostgreSQL + Firebase
Push: Firebase Cloud Messaging
Deploy: App Store + Google Play
```

**API Service:**
```
API: Python FastAPI / Node.js Express / Go Gin
Database: PostgreSQL with migrations
Cache: Redis
Queue: RabbitMQ/SQS
Deploy: Docker + Kubernetes
```

### Step 4: Design Data Models

```
Feature Requirements → Data Modeling → Schemas
```

**For each entity:**
- Define fields and types
- Establish relationships
- Plan indexes for performance
- Consider data validation rules
- Design for query patterns

**Example:**
```typescript
// User Model
interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'member';
  teamId: string;
  createdAt: Date;
  updatedAt: Date;
}

// Task Model
interface Task {
  id: string;
  title: string;
  description: string;
  status: 'todo' | 'in_progress' | 'done';
  assigneeId: string;
  teamId: string;
  priority: 'low' | 'medium' | 'high';
  dueDate?: Date;
  createdBy: string;
  createdAt: Date;
  updatedAt: Date;
}
```

### Step 5: Design API Interfaces

```
Data Models → API Design → Endpoint Specifications
```

**For each API endpoint:**
- HTTP method and path
- Request parameters and body
- Response structure
- Error responses
- Authentication requirements

**Example:**
```
POST /api/tasks
Auth: Required (Bearer token)
Request:
{
  "title": "string",
  "description": "string",
  "assigneeId": "string",
  "priority": "low" | "medium" | "high",
  "dueDate": "ISO8601 date (optional)"
}
Response 201:
{
  "id": "string",
  "title": "string",
  ...
  "createdAt": "ISO8601 date"
}
Response 400: { "error": "Validation failed", "details": [...] }
Response 401: { "error": "Unauthorized" }
```

### Step 6: Plan Component Structure

```
Features → Component Breakdown → Implementation Units
```

**Break down into:**
- Reusable UI components
- Service layers (business logic)
- Data access layers (repositories)
- Utility modules
- Configuration modules

**Example structure:**
```
src/
├── components/        # UI components
│   ├── TaskList/
│   ├── TaskCard/
│   └── TaskForm/
├── services/          # Business logic
│   ├── taskService.ts
│   └── authService.ts
├── repositories/      # Data access
│   ├── taskRepository.ts
│   └── userRepository.ts
├── models/           # Type definitions
│   ├── Task.ts
│   └── User.ts
├── utils/            # Helper functions
├── config/           # Configuration
└── api/              # API route handlers
```

## Output Format

### Blueprint Document Structure

```markdown
# Technical Blueprint: [Project Name]

## Executive Summary
- **Project**: [Name]
- **PRD Reference**: [Link or ID]
- **Architecture Type**: [Monolith/Microservices/Serverless/etc.]
- **Primary Technology**: [Main framework/language]
- **Estimated Complexity**: [Low/Medium/High]

## System Architecture

### High-Level Overview
[Diagram or description of system components and how they interact]

### Architecture Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| Frontend Framework | React | Team expertise, rich ecosystem, component reusability |
| Backend Framework | FastAPI (Python) | Fast development, auto-generated docs, type safety |
| Database | PostgreSQL | ACID compliance, JSON support, proven at scale |

### Design Patterns
- **Frontend**: Component-based architecture, unidirectional data flow
- **Backend**: Repository pattern, dependency injection
- **API**: RESTful design, versioned endpoints

## Technology Stack

### Frontend
- **Framework**: React 18 + TypeScript
- **State Management**: Zustand
- **Styling**: Tailwind CSS
- **Build Tool**: Vite
- **Testing**: Vitest + React Testing Library

### Backend
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Testing**: pytest

### Database & Storage
- **Primary Database**: PostgreSQL 15
- **Cache**: Redis 7
- **File Storage**: AWS S3

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Orchestration**: Kubernetes (production)
- **CI/CD**: GitHub Actions
- **Hosting**: AWS (ECS + RDS + ElastiCache)
- **Monitoring**: DataDog

## Data Models

### Core Entities

#### User
```typescript
interface User {
  id: UUID;
  email: string;
  passwordHash: string;
  name: string;
  role: UserRole;
  teamId: UUID;
  createdAt: timestamp;
  updatedAt: timestamp;
}
```

#### [Other entities...]

### Relationships
- User belongs to Team (many-to-one)
- Task belongs to Team (many-to-one)
- Task assigned to User (many-to-one)

### Database Schema
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  role VARCHAR(50) NOT NULL,
  team_id UUID REFERENCES teams(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_team_id ON users(team_id);
CREATE INDEX idx_users_email ON users(email);
```

## API Specifications

### Authentication Endpoints

#### POST /api/auth/register
[Detailed specification]

#### POST /api/auth/login
[Detailed specification]

### Resource Endpoints

#### GET /api/tasks
[Detailed specification]

#### POST /api/tasks
[Detailed specification]

[Continue for all endpoints...]

## Component Architecture

### Frontend Components
```
src/
├── components/
│   ├── layout/
│   │   ├── Header.tsx
│   │   └── Sidebar.tsx
│   ├── tasks/
│   │   ├── TaskList.tsx
│   │   ├── TaskCard.tsx
│   │   └── TaskForm.tsx
│   └── common/
│       ├── Button.tsx
│       └── Input.tsx
```

### Backend Services
```
src/
├── api/              # API route handlers
├── services/         # Business logic
├── repositories/     # Data access
├── models/           # Data models
└── utils/            # Utilities
```

## Implementation Strategy

### Phase 1: Foundation (Week 1-2)
- Set up development environment
- Initialize project structure
- Configure database and migrations
- Implement authentication system

### Phase 2: Core Features (Week 3-5)
- Implement task CRUD operations
- Build team management
- Create main dashboard UI
- Implement real-time updates

### Phase 3: Enhancement (Week 6-7)
- Add notifications
- Implement search
- Add analytics dashboard
- Performance optimization

### Phase 4: Polish (Week 8)
- UI/UX refinement
- Testing and bug fixes
- Documentation
- Deployment preparation

## Technical Decisions & Rationale

### Why PostgreSQL over MongoDB?
- Requirements include complex relationships between entities
- Need for strong consistency (ACID properties)
- Team has more PostgreSQL expertise

### Why React over Vue?
- Larger community and ecosystem
- More third-party integrations available
- Team familiarity

[Document other significant decisions...]

## Non-Functional Requirements

### Performance
- API response time: < 200ms (p95)
- Page load time: < 2s (p95)
- Support 1000 concurrent users

### Security
- Authentication: JWT with refresh tokens
- Authorization: Role-based access control (RBAC)
- Data encryption: TLS in transit, AES-256 at rest
- Input validation: All inputs sanitized

### Scalability
- Horizontal scaling via load balancers
- Database read replicas for read-heavy operations
- Redis cache to reduce database load
- CDN for static assets

## Testing Strategy
- Unit tests: 80%+ coverage for business logic
- Integration tests: All API endpoints
- E2E tests: Critical user flows
- Performance tests: Load testing with k6

## Deployment Architecture
[Diagram showing production deployment setup]

## Monitoring & Observability
- Application metrics: Response times, error rates
- Infrastructure metrics: CPU, memory, disk
- Logging: Centralized logging with structured logs
- Alerts: On-call rotation for critical errors

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Third-party API downtime | High | Medium | Implement circuit breakers, fallback mechanisms |
| Database performance at scale | High | Medium | Implement caching, read replicas, query optimization |

## Open Technical Questions
- [ ] Do we need real-time collaboration features? (WebSockets vs polling)
- [ ] Should we implement optimistic UI updates?
- [ ] What's the data retention policy?
```

## Best Practices

### DO:
- **Justify technology choices** with clear rationale
- **Design for maintainability** not just initial development
- **Consider team expertise** when choosing technologies
- **Plan for monitoring and debugging** from the start
- **Document architecture decisions** with context
- **Design APIs before implementing them**

### DON'T:
- **Choose trendy tech** without considering long-term support
- **Over-engineer** for scale you don't need yet
- **Ignore existing codebase** patterns and conventions
- **Skip non-functional requirements** (security, performance, etc.)
- **Design in isolation** - validate with PRD and stakeholders

## Integration with Other Agents

### Input ← Refinery Agent
Receives the PRD containing:
- Feature requirements
- User stories
- Success criteria
- Constraints and preferences

### Output → Planner Agent
Provides the blueprint for task breakdown:
- System architecture
- Technology stack
- Component structure
- Implementation strategy
- Technical specifications

### Feedback Loop ← Validator/Assembler
May receive feedback on:
- Technical debt discovered during implementation
- Performance issues found during testing
- Architecture limitations encountered

## Example Usage

### Input PRD (Summary)
```
Project: Collaborative Task Manager
Features:
- User authentication
- Task CRUD
- Team management
- Real-time updates
- Notifications

Constraints:
- Small team (2-5 developers)
- 6-week timeline
- Moderate budget
```

### Foundry Analysis
1. **Scale analysis**: Small-medium scale → Monolith appropriate
2. **Team skills**: JavaScript/TypeScript → Node.js + React
3. **Real-time needs**: WebSocket support required
4. **Timeline**: Need rapid development → Choose proven stack

### Output Blueprint
```
Architecture: Monolithic web application
Frontend: React + TypeScript
Backend: Node.js + Express + Socket.io
Database: PostgreSQL
Real-time: Socket.io for live updates
Auth: JWT with refresh tokens
Deployment: Docker on AWS ECS
```

## Tips for Effective Blueprint Creation

1. **Start with constraints**: Let constraints guide technology choices
2. **Prototype risky decisions**: Build proof-of-concepts for uncertain choices
3. **Plan for evolution**: Design systems that can adapt to changing requirements
4. **Balance pragmatism and idealism**: Perfect architecture vs shipping on time
5. **Document trade-offs**: Explain what you chose NOT to do and why

## Common Pitfalls

- **Analysis paralysis**: Don't spend weeks choosing between similar frameworks
- **Resume-driven development**: Choosing tech to learn rather than solve the problem
- **Ignoring operational complexity**: Microservices sound great but require significant ops overhead
- **Not planning for data migrations**: Database schema will evolve, plan for it
- **Underestimating integration complexity**: Third-party APIs are never as simple as the docs suggest

## Summary

The Foundry Agent translates "what to build" into "how to build it." It bridges the gap between business requirements and executable code, providing a clear technical roadmap for the development team.

**Remember**: A good blueprint is:
- **Specific**: Clear technology choices and architecture decisions
- **Justified**: Every major decision has documented rationale
- **Practical**: Aligned with team skills and timeline
- **Complete**: Covers all aspects from data models to deployment
- **Flexible**: Can accommodate reasonable changes without full redesign
