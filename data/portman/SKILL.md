---
name: portman
description: Port management for local development with git worktrees. Use when setting up local development environments, booking ports for services to avoid collisions between parallel worktrees, or configuring docker-compose with dynamic ports.
---

# Portman Skill

This skill provides patterns for managing port allocations in local development environments using portman. It enables running multiple worktrees of the same project in parallel without port conflicts.

## Why Portman?

When working with git worktrees or multiple project instances:
- Each worktree needs unique ports for services (postgres, redis, web server, etc.)
- Manual port management is error-prone and tedious
- Docker-compose files hardcode ports causing conflicts

Portman automatically assigns unique ports per worktree context.

## Core Workflow

### 1. Initial Setup (Once per machine)

```bash
# Initialize portman and show shell integration
portman init

# For direnv users (recommended)
portman init --direnv
```

### 2. Setting Up a New Worktree

When cloning or creating a new worktree, book ports for all services:

```bash
# Auto-discover services from docker-compose.yml
portman book --auto

# Or book specific services
portman book postgres
portman book redis
portman book frontend --port 3000
```

### 3. Using Ports in Your Environment

```bash
# Export as environment variables (add to .envrc for direnv)
eval "$(portman export --auto)"

# Get a specific port
PGPORT=$(portman get postgres -q)
```

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `portman book` | Reserve ports for services | `portman book --auto` |
| `portman get` | Get port for a service | `portman get postgres -q` |
| `portman export` | Export as env vars | `eval "$(portman export)"` |
| `portman status` | Show current allocations | `portman status --all` |
| `portman release` | Free port allocations | `portman release --all` |
| `portman context` | Show current context | `portman context` |
| `portman discover` | Preview auto-discovery | `portman discover` |
| `portman prune` | Clean orphaned allocations | `portman prune --dry-run` |

## Integration with Docker Compose

### Dynamic Port Configuration

Use environment variables in `docker-compose.yml`:

```yaml
services:
  postgres:
    image: postgres:16
    ports:
      - "${POSTGRES_PORT:-5432}:5432"
    environment:
      POSTGRES_PASSWORD: dev

  redis:
    image: redis:7
    ports:
      - "${REDIS_PORT:-6379}:6379"

  web:
    build: .
    ports:
      - "${WEB_PORT:-8000}:8000"
    environment:
      DATABASE_URL: postgres://localhost:${POSTGRES_PORT:-5432}/app
```

### Direnv Integration (.envrc)

```bash
# .envrc - Automatically set ports when entering directory
eval "$(portman export --auto)"

# Or with fallbacks
export POSTGRES_PORT=$(portman get postgres -q 2>/dev/null || echo 5432)
export REDIS_PORT=$(portman get redis -q 2>/dev/null || echo 6379)
export WEB_PORT=$(portman get web -q 2>/dev/null || echo 8000)
```

## Context-Aware Port Allocation

Portman uses the current directory and git remote to create a unique context:

```bash
# View your current context
portman context

# Output:
# Context: abc123
# Path: /home/user/projects/myapp-feature-x
# Git Remote: github.com/org/myapp
# Git Branch: feature-x
```

Each worktree gets its own context, ensuring port isolation.

## Port Ranges Configuration

Configure port ranges per service:

```bash
# Set custom range for postgres
portman config --set-range postgres:5500-5599

# View current configuration
portman config --show
```

## Maintenance Commands

### View All Allocations

```bash
# Show current context only
portman status

# Show all contexts
portman status --all

# Check if ports are actually listening
portman status --all --live
```

### Cleanup Orphaned Allocations

```bash
# Preview what would be removed
portman prune --dry-run

# Remove allocations for deleted worktrees
portman prune

# Also remove stale allocations (not accessed in 30 days)
portman prune --stale 30
```

## Common Patterns

### Setup Script for New Developers

```bash
#!/bin/bash
# scripts/dev-setup.sh

# Book ports for all services
portman book --auto

# Show allocated ports
portman status

# Export for current shell
eval "$(portman export --auto)"

echo "Development environment ready!"
echo "PostgreSQL: localhost:$POSTGRES_PORT"
echo "Redis: localhost:$REDIS_PORT"
```

### Makefile Integration

```makefile
.PHONY: setup ports

setup:
	portman book --auto
	@echo "Ports allocated. Run 'make ports' to see them."

ports:
	@portman status

start:
	eval "$$(portman export --auto)" && docker-compose up
```

### CI/CD Considerations

In CI environments, portman context is unique per workspace, allowing parallel CI jobs:

```yaml
# GitHub Actions
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup ports
        run: |
          portman book --auto
          eval "$(portman export --auto)"
      - name: Run tests
        run: docker-compose up -d && pytest
```

## Troubleshooting

### Port Already in Use

```bash
# Check what's using a port
portman status --all --live

# Release and rebook
portman release postgres
portman book postgres
```

### Reset All Allocations

```bash
# Release all for current context
portman release --all

# Rebook
portman book --auto
```
