---
name: docker-local-docs
description: Search docker-local documentation for commands, configuration, and troubleshooting guides
---

# Docker-Local Documentation Skill

## Overview

This skill provides access to comprehensive docker-local documentation covering:
- Installation and setup
- CLI commands reference
- Service configuration
- Multi-project management
- Environment files
- Troubleshooting guides

## Activation

Use this skill when:
- User asks how to use docker-local
- User needs command syntax
- User wants to understand configuration
- Looking up troubleshooting steps

## MANDATORY: Prerequisite Check

**Before ANY docker-local command, verify installation:**

```bash
which docker-local > /dev/null 2>&1
```

**If docker-local is NOT found:**
1. Stop and ask the user if they want to install it
2. If yes, install via: `composer global require mwguerra/docker-local`
3. Add to PATH: `export PATH="$HOME/.composer/vendor/bin:$PATH"`
4. Initialize: `docker-local init`
5. Verify: `which docker-local && docker-local --version`

## Documentation Structure

```
references/
├── 01-overview.md           # Features and requirements
├── 02-installation.md       # Platform-specific installation
├── 03-quick-start.md        # New and existing projects
├── 04-commands.md           # All 50+ CLI commands
├── 05-services.md           # URLs, ports, credentials
├── 06-multi-project.md      # Isolation and conflict detection
├── 07-env-files.md          # Docker vs Laravel .env
├── 08-troubleshooting.md    # Common issues and solutions
└── 09-migration.md          # From project-specific Docker
```

## Quick Reference

### Installation
```bash
composer global require mwguerra/docker-local
export PATH="$HOME/.composer/vendor/bin:$PATH"
docker-local init
```

### Common Commands
```bash
docker-local up                # Start environment
docker-local status            # Check services
docker-local make:laravel NAME # Create project
docker-local doctor            # Health check
docker-local logs              # View logs
```

### Service URLs
- Projects: `https://<name>.test`
- Mailpit: `https://mail.localhost`
- MinIO: `https://minio.localhost`
- Traefik: `https://traefik.localhost`

### Default Credentials
- MySQL: `laravel` / `secret`
- PostgreSQL: `laravel` / `secret`
- MinIO: `minio` / `minio123`

## Usage

Read the specific documentation file based on user needs:

1. **Installation help** → `02-installation.md`
2. **Command syntax** → `04-commands.md`
3. **Service ports/URLs** → `05-services.md`
4. **Multi-project setup** → `06-multi-project.md`
5. **Troubleshooting** → `08-troubleshooting.md`

$ARGUMENTS
