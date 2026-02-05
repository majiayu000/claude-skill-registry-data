---
name: Cursor Development Rules
description: Provides comprehensive development rules and guidelines for Cursor project development. Use when working on Cursor projects, setting up development environments, or implementing coding standards.
---

# Cursor Project Development Rules

This Skill provides comprehensive development rules and guidelines for Cursor project development, including worktree-aware Docker development, coding standards, API design, frontend development, testing strategies, and Docker best practices.

## Quick Start

To access specific development rules:

```bash
# View coding standards
cat rules/coding-standards.md

# View API guidelines
cat rules/api-guidelines.md

# View frontend guidelines
cat rules/frontend-guidelines.md

# View testing guidelines
cat rules/testing-guidelines.md

# View Docker development rules
cat rules/docker-development.md

# Get project information
python scripts/helper.py info
```

## Available Rules

- **coding-standards.md**: Coding conventions and style guides for TypeScript, Python, and general development
- **api-guidelines.md**: FastAPI API design guidelines and best practices
- **frontend-guidelines.md**: Next.js frontend development guidelines with TypeScript and Tailwind CSS
- **testing-guidelines.md**: Testing strategy and implementation guidelines for unit, integration, and E2E tests
- **docker-development.md**: Docker development environment rules and worktree integration

## Project Overview

This is a worktree-aware Docker scaffold with Next.js + FastAPI + PostgreSQL + Playwright E2E that enables parallel development across multiple git worktrees without port/container/network/volume/database name conflicts.

## Key Features

- **Worktree Support**: Simultaneous development on multiple branches
- **Docker Development**: Consistent containerized development environment
- **Automatic Environment**: Git hooks for automatic .env generation
- **Complete Isolation**: Each worktree has independent environment
- **Port Management**: Automatic port allocation (3000+Δ, 8000+Δ, 5400+Δ)
- **Database Isolation**: Worktree-specific database names (app_<hash6>)
- **Volume Isolation**: Worktree-specific Docker volumes
- **Network Isolation**: Worktree-specific Docker networks

## Development Commands

```bash
# Environment management
python tool-scripts/devctl.py env-gen --write-root
python tool-scripts/devctl.py up
python tool-scripts/devctl.py down

# Testing
python tool-scripts/devctl.py test js      # Frontend unit tests
python tool-scripts/devctl.py test py      # Backend unit tests
python tool-scripts/devctl.py test ui      # Playwright E2E
python tool-scripts/devctl.py test api     # API E2E tests
python tool-scripts/devctl.py test all    # All tests

# Database
python tool-scripts/devctl.py migrate upgrade
python tool-scripts/devctl.py migrate downgrade base

# Worktree management
git worktree add ../wt-feature feature/my-branch
git worktree remove wt-feature
```

## Architecture

- **Frontend**: Next.js 14 with TypeScript, Tailwind CSS, Vitest, Playwright
- **Backend**: FastAPI with Python 3.11, SQLAlchemy, Alembic, pytest
- **Database**: PostgreSQL with worktree-specific databases
- **Testing**: Vitest (unit), Playwright (UI E2E), httpx (API E2E)
- **Development**: Docker Compose with worktree isolation
