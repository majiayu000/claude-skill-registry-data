---
name: docker-docs
description: Reference Docker and Compose documentation for configuration patterns and best practices
---

# Docker Documentation Reference Skill

## Overview

This skill provides access to comprehensive Docker and Docker Compose documentation. Use this skill to look up exact configurations, command syntax, and best practices before generating any Docker-related files.

## Documentation Location

All documentation is stored in:
`/home/mwguerra/projects/mwguerra/claude-code-plugins/docker-specialist/skills/docker-docs/references/`

## Directory Structure

```
references/
├── 01-introduction.md       # Docker concepts, key terms
├── 02-dockerfile.md         # Dockerfile instructions, multi-stage builds
├── 03-compose-fundamentals.md  # Compose file structure, options
├── 04-networking.md         # Network types, DNS, external networks
├── 05-databases.md          # PostgreSQL, MySQL, MongoDB, Redis
├── 06-services.md           # Dependencies, scaling, patterns
├── 07-ports-ssl.md          # Port mapping, Traefik, Nginx SSL
├── 08-volumes.md            # Volume types, persistence, backups
├── 09-environment.md        # Env vars, secrets, .env files
├── 10-architecture.md       # Project structures, folder organization
├── 11-global-local.md       # Global vs project containers
├── 12-examples.md           # Complete working examples
├── 13-commands.md           # Essential Docker commands
├── 14-security.md           # Security best practices
├── 15-port-conflicts.md     # Port conflict resolution
├── 16-restart-strategies.md # Restart policies, data persistence
└── 17-troubleshooting.md    # Common issues and solutions
```

## Usage

### When to Use This Skill

1. Before generating any Dockerfile or compose configuration
2. When troubleshooting Docker errors
3. To verify correct command syntax
4. To find proper configuration patterns
5. To understand Docker networking
6. For security best practices

### Search Workflow

1. **Identify Topic**: Determine what documentation is needed
2. **Navigate to File**: Go to relevant documentation file
3. **Read Documentation**: Extract exact patterns
4. **Apply Knowledge**: Use in configuration generation

### Common Lookups

| Topic | File |
|-------|------|
| Dockerfile creation | `02-dockerfile.md` |
| Compose configuration | `03-compose-fundamentals.md` |
| Container networking | `04-networking.md` |
| Database setup | `05-databases.md` |
| Multi-container apps | `06-services.md` |
| SSL/TLS setup | `07-ports-ssl.md` |
| Volume management | `08-volumes.md` |
| Environment variables | `09-environment.md` |
| Project structure | `10-architecture.md` |
| Commands reference | `13-commands.md` |
| Security | `14-security.md` |
| Troubleshooting | `17-troubleshooting.md` |

## Documentation Reading Pattern

When reading documentation:

1. **Find the right file**: Match topic to documentation file
2. **Read the overview**: Understand the concept
3. **Extract code examples**: Copy exact patterns
4. **Note configuration options**: Review available settings
5. **Check best practices**: Apply security and performance tips

## Example Usage

### Looking up PostgreSQL Configuration

1. Navigate to `05-databases.md`
2. Find PostgreSQL section
3. Extract:
   - Image version
   - Environment variables
   - Health check configuration
   - Volume setup
   - Network configuration

### Looking up Network Configuration

1. Navigate to `04-networking.md`
2. Find relevant section (bridge, external, internal)
3. Extract:
   - Network definition syntax
   - Service network configuration
   - DNS resolution patterns

## Output

After reading documentation, provide:

1. **Exact configuration pattern** from docs
2. **Required settings**
3. **Optional configurations**
4. **Best practices noted**
5. **Security considerations**
