---
name: mermaid-architect
description: Generates clean, syntactically valid Mermaid.js diagrams for ERDs, system architecture, sequence flows, class diagrams, and C4 component models directly inside Markdown documents.
version: 1.0.0
---

# Mermaid Architect

Specialized skill for creating robust, syntactically correct Mermaid.js diagrams for Markdown documentation, PR descriptions, and architectural blueprints.

## Syntax Best Practices

1. **Quote Node Labels**: Always quote labels containing special characters, brackets, or parentheses:
   ```mermaid
   graph TD
     A["Client (Browser / Mobile)"] --> B["API Gateway (Hono / Next.js)"]
   ```
2. **Cardinality in ERDs**:
   - `||--||` : Exactly one to one
   - `||--o{` : One to zero-or-more
   - `||--|{` : One to one-or-more
   - `}o--o{` : Zero-or-more to zero-or-more

---

## Supported Diagram Types

### 1. Entity Relationship Diagram (ERD)
```mermaid
erDiagram
  USER ||--o{ POST : writes
  USER {
    uuid id PK
    string email UK
    datetime created_at
  }
  POST {
    uuid id PK
    uuid author_id FK
    string title
    text content
  }
```

### 2. Sequence Diagram (Auth & API Flow)
```mermaid
sequenceDiagram
  autonumber
  actor User
  participant Client as Client App
  participant Auth as Better Auth Server
  participant DB as Database

  User->>Client: Click Login with Google
  Client->>Auth: Redirect to /api/auth/sign-in/social
  Auth-->>Client: OAuth consent redirect
  User->>Auth: Approve scopes
  Auth->>DB: Upsert User & Session
  Auth-->>Client: Set HttpOnly session cookie
  Client-->>User: Redirect to /dashboard
```

### 3. C4 / System Topology Flowchart
```mermaid
flowchart TD
  subgraph Client Tier
    Web["Next.js Web App"]
    Mobile["Flutter App"]
  end

  subgraph Edge Tier
    Gateway["Cloudflare Workers (Hono API)"]
  end

  subgraph Service Tier
    AppServer["NestJS / Django Backend"]
    Worker["Async Celery / BullMQ"]
  end

  subgraph Data Tier
    Postgres[("PostgreSQL")]
    Redis[("Redis Cache / Queue")]
    S3[("R2 / S3 Object Storage")]
  end

  Web --> Gateway
  Mobile --> Gateway
  Gateway --> AppServer
  AppServer --> Postgres
  AppServer --> Redis
  AppServer --> S3
  Worker --> Redis
  Worker --> Postgres
```
