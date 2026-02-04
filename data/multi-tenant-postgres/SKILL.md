---
name: multi-tenant-postgres
description: Implement multi-tenant PostgreSQL database layer with row-level security. Use for database schema design, tenant isolation, migrations, connection pooling, and data access patterns. Triggers on "database schema", "PostgreSQL", "multi-tenant", "row-level security", "RLS", "database migration", "sqlc", or when implementing the data layer for AgentStack.
---

# Multi-Tenant PostgreSQL

## Overview

Implement a multi-tenant PostgreSQL database with row-level security (RLS), providing complete tenant isolation while maintaining a single database instance for operational simplicity.

## Multi-Tenancy Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  Multi-Tenant Data Architecture                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Application Layer                     │   │
│  │  • Set project_id context on each request               │   │
│  │  • Connection pool with PgBouncer                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                             │                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    PostgreSQL                            │   │
│  │  ┌─────────────────────────────────────────────────┐    │   │
│  │  │  Row-Level Security (RLS)                       │    │   │
│  │  │  • All tables have project_id column            │    │   │
│  │  │  • Policies enforce project_id = current_setting │   │   │
│  │  └─────────────────────────────────────────────────┘    │   │
│  │                                                          │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │   │
│  │  │Project A│ │Project B│ │Project C│ │   ...   │        │   │
│  │  │ (rows)  │ │ (rows)  │ │ (rows)  │ │         │        │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Database Schema

### Core Tables

```sql
-- migrations/001_initial_schema.sql

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Organizations
CREATE TABLE organizations (
    id TEXT PRIMARY KEY DEFAULT 'org_' || gen_random_uuid()::text,
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    plan TEXT NOT NULL DEFAULT 'free' CHECK (plan IN ('free', 'pro', 'enterprise')),
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Projects (tenant boundary)
CREATE TABLE projects (
    id TEXT PRIMARY KEY DEFAULT 'prj_' || gen_random_uuid()::text,
    organization_id TEXT NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    slug TEXT NOT NULL,
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (organization_id, slug)
);

CREATE INDEX idx_projects_org ON projects(organization_id);

-- Agents
CREATE TABLE agents (
    id TEXT PRIMARY KEY DEFAULT 'agt_' || gen_random_uuid()::text,
    project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    framework TEXT NOT NULL CHECK (framework IN ('google-adk', 'langchain', 'crewai', 'custom')),
    status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'deploying', 'running', 'failed', 'stopped')),
    config JSONB NOT NULL DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (project_id, name)
);

CREATE INDEX idx_agents_project ON agents(project_id);
CREATE INDEX idx_agents_status ON agents(status);

-- Agent Revisions (immutable)
CREATE TABLE agent_revisions (
    id TEXT PRIMARY KEY DEFAULT 'rev_' || gen_random_uuid()::text,
    agent_id TEXT NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    revision_number INT NOT NULL,
    image TEXT NOT NULL,
    config JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (agent_id, revision_number)
);

CREATE INDEX idx_revisions_agent ON agent_revisions(agent_id);

-- Chat Sessions
CREATE TABLE chat_sessions (
    id TEXT PRIMARY KEY DEFAULT 'ses_' || gen_random_uuid()::text,
    agent_id TEXT NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    user_id TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_sessions_agent ON chat_sessions(agent_id);
CREATE INDEX idx_sessions_project ON chat_sessions(project_id);

-- Chat Messages
CREATE TABLE chat_messages (
    id TEXT PRIMARY KEY DEFAULT 'msg_' || gen_random_uuid()::text,
    session_id TEXT NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system', 'tool')),
    content TEXT NOT NULL,
    tool_calls JSONB,
    usage JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_messages_session ON chat_messages(session_id);
CREATE INDEX idx_messages_created ON chat_messages(created_at DESC);

-- API Keys
CREATE TABLE api_keys (
    id TEXT PRIMARY KEY DEFAULT 'key_' || gen_random_uuid()::text,
    project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    key_hash TEXT NOT NULL,
    key_prefix TEXT NOT NULL,  -- First 8 chars for identification
    scopes TEXT[] NOT NULL DEFAULT '{}',
    last_used_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_api_keys_project ON api_keys(project_id);
CREATE INDEX idx_api_keys_hash ON api_keys(key_hash);
```

## Row-Level Security

```sql
-- migrations/002_rls_policies.sql

-- Enable RLS on all tenant tables
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_revisions ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;

-- Create application role
CREATE ROLE app_user;

-- RLS Policies for agents
CREATE POLICY agents_tenant_isolation ON agents
    FOR ALL
    TO app_user
    USING (project_id = current_setting('app.current_project_id', true))
    WITH CHECK (project_id = current_setting('app.current_project_id', true));

-- RLS Policies for revisions
CREATE POLICY revisions_tenant_isolation ON agent_revisions
    FOR ALL
    TO app_user
    USING (project_id = current_setting('app.current_project_id', true))
    WITH CHECK (project_id = current_setting('app.current_project_id', true));

-- RLS Policies for sessions
CREATE POLICY sessions_tenant_isolation ON chat_sessions
    FOR ALL
    TO app_user
    USING (project_id = current_setting('app.current_project_id', true))
    WITH CHECK (project_id = current_setting('app.current_project_id', true));

-- RLS Policies for messages
CREATE POLICY messages_tenant_isolation ON chat_messages
    FOR ALL
    TO app_user
    USING (project_id = current_setting('app.current_project_id', true))
    WITH CHECK (project_id = current_setting('app.current_project_id', true));

-- RLS Policies for API keys
CREATE POLICY api_keys_tenant_isolation ON api_keys
    FOR ALL
    TO app_user
    USING (project_id = current_setting('app.current_project_id', true))
    WITH CHECK (project_id = current_setting('app.current_project_id', true));
```

## Go Database Layer

### Connection Pool

```go
// internal/infrastructure/database/pool.go
package database

import (
    "context"
    "fmt"
    "time"

    "github.com/jackc/pgx/v5/pgxpool"
)

type Config struct {
    Host            string
    Port            int
    Database        string
    User            string
    Password        string
    MaxConns        int
    MinConns        int
    MaxConnLifetime time.Duration
    MaxConnIdleTime time.Duration
}

func NewPool(ctx context.Context, cfg Config) (*pgxpool.Pool, error) {
    connString := fmt.Sprintf(
        "postgres://%s:%s@%s:%d/%s?sslmode=require",
        cfg.User, cfg.Password, cfg.Host, cfg.Port, cfg.Database,
    )

    poolConfig, err := pgxpool.ParseConfig(connString)
    if err != nil {
        return nil, fmt.Errorf("parse config: %w", err)
    }

    poolConfig.MaxConns = int32(cfg.MaxConns)
    poolConfig.MinConns = int32(cfg.MinConns)
    poolConfig.MaxConnLifetime = cfg.MaxConnLifetime
    poolConfig.MaxConnIdleTime = cfg.MaxConnIdleTime

    pool, err := pgxpool.NewWithConfig(ctx, poolConfig)
    if err != nil {
        return nil, fmt.Errorf("create pool: %w", err)
    }

    return pool, nil
}
```

### Tenant Context

```go
// internal/infrastructure/database/tenant.go
package database

import (
    "context"
    "fmt"

    "github.com/jackc/pgx/v5"
    "github.com/jackc/pgx/v5/pgxpool"
)

type TenantDB struct {
    pool *pgxpool.Pool
}

func NewTenantDB(pool *pgxpool.Pool) *TenantDB {
    return &TenantDB{pool: pool}
}

// WithTenant returns a connection with tenant context set
func (db *TenantDB) WithTenant(ctx context.Context, projectID string) (*TenantConn, error) {
    conn, err := db.pool.Acquire(ctx)
    if err != nil {
        return nil, fmt.Errorf("acquire connection: %w", err)
    }

    // Set tenant context
    _, err = conn.Exec(ctx, "SELECT set_config('app.current_project_id', $1, true)", projectID)
    if err != nil {
        conn.Release()
        return nil, fmt.Errorf("set tenant context: %w", err)
    }

    return &TenantConn{conn: conn, projectID: projectID}, nil
}

type TenantConn struct {
    conn      *pgxpool.Conn
    projectID string
}

func (tc *TenantConn) Release() {
    tc.conn.Release()
}

func (tc *TenantConn) Query(ctx context.Context, sql string, args ...interface{}) (pgx.Rows, error) {
    return tc.conn.Query(ctx, sql, args...)
}

func (tc *TenantConn) QueryRow(ctx context.Context, sql string, args ...interface{}) pgx.Row {
    return tc.conn.QueryRow(ctx, sql, args...)
}

func (tc *TenantConn) Exec(ctx context.Context, sql string, args ...interface{}) (pgconn.CommandTag, error) {
    return tc.conn.Exec(ctx, sql, args...)
}

// Transaction with tenant context
func (tc *TenantConn) BeginTx(ctx context.Context) (pgx.Tx, error) {
    tx, err := tc.conn.Begin(ctx)
    if err != nil {
        return nil, err
    }
    
    // Re-set tenant context in transaction
    _, err = tx.Exec(ctx, "SELECT set_config('app.current_project_id', $1, true)", tc.projectID)
    if err != nil {
        tx.Rollback(ctx)
        return nil, err
    }
    
    return tx, nil
}
```

### Repository Pattern

```go
// internal/infrastructure/database/agent_repository.go
package database

import (
    "context"
    "github.com/raphaelmansuy/agentstack/internal/domain/agent"
)

type AgentRepository struct {
    db *TenantDB
}

func NewAgentRepository(db *TenantDB) *AgentRepository {
    return &AgentRepository{db: db}
}

func (r *AgentRepository) Create(ctx context.Context, projectID string, a *agent.Agent) error {
    conn, err := r.db.WithTenant(ctx, projectID)
    if err != nil {
        return err
    }
    defer conn.Release()

    query := `
        INSERT INTO agents (id, project_id, name, description, framework, status, config)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING created_at, updated_at
    `
    
    return conn.QueryRow(ctx, query,
        a.ID, projectID, a.Name, a.Description, a.Framework, a.Status, a.Config,
    ).Scan(&a.CreatedAt, &a.UpdatedAt)
}

func (r *AgentRepository) GetByID(ctx context.Context, projectID, agentID string) (*agent.Agent, error) {
    conn, err := r.db.WithTenant(ctx, projectID)
    if err != nil {
        return nil, err
    }
    defer conn.Release()

    query := `
        SELECT id, project_id, name, description, framework, status, config, created_at, updated_at
        FROM agents
        WHERE id = $1
    `
    // Note: RLS automatically filters by project_id
    
    var a agent.Agent
    err = conn.QueryRow(ctx, query, agentID).Scan(
        &a.ID, &a.ProjectID, &a.Name, &a.Description, &a.Framework, 
        &a.Status, &a.Config, &a.CreatedAt, &a.UpdatedAt,
    )
    if err != nil {
        return nil, err
    }
    
    return &a, nil
}

func (r *AgentRepository) List(ctx context.Context, projectID, cursor string, limit int) ([]*agent.Agent, string, error) {
    conn, err := r.db.WithTenant(ctx, projectID)
    if err != nil {
        return nil, "", err
    }
    defer conn.Release()

    query := `
        SELECT id, project_id, name, description, framework, status, config, created_at, updated_at
        FROM agents
        WHERE ($1 = '' OR id > $1)
        ORDER BY id
        LIMIT $2
    `
    // Note: RLS automatically filters by project_id
    
    rows, err := conn.Query(ctx, query, cursor, limit+1)
    if err != nil {
        return nil, "", err
    }
    defer rows.Close()

    var agents []*agent.Agent
    for rows.Next() {
        var a agent.Agent
        err := rows.Scan(
            &a.ID, &a.ProjectID, &a.Name, &a.Description, &a.Framework,
            &a.Status, &a.Config, &a.CreatedAt, &a.UpdatedAt,
        )
        if err != nil {
            return nil, "", err
        }
        agents = append(agents, &a)
    }

    var nextCursor string
    if len(agents) > limit {
        nextCursor = agents[limit].ID
        agents = agents[:limit]
    }

    return agents, nextCursor, nil
}
```

## Migrations with Atlas

```hcl
# atlas.hcl
env "local" {
  src = "file://migrations"
  url = "postgres://postgres:postgres@localhost:5432/agentstack?sslmode=disable"
  dev = "docker://postgres/16/dev"
}

env "prod" {
  src = "file://migrations"
  url = env("DATABASE_URL")
}
```

```bash
# Create migration
atlas migrate diff create_agents --env local

# Apply migrations
atlas migrate apply --env local

# Validate schema
atlas migrate validate --env local
```

## Resources

- `references/cursor-pagination.md` - Cursor-based pagination patterns
- `references/connection-pooling.md` - PgBouncer configuration
- `scripts/migrate.sh` - Migration automation script
