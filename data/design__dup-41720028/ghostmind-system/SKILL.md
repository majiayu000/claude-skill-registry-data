---
name: ghostmind-system
description: This skill should be used when working with the Ghostmind development system, which uses meta.json as a central configuration for Docker, Compose, Terraform, and Tmux. Use this skill when creating or modifying configurations for any of these components, setting up new applications, or understanding how the system components interconnect.
---

# Ghostmind System Skill

This skill should be used when working with the Ghostmind development system, which uses meta.json as a central configuration for Docker, Compose, Terraform, and Tmux. Use this skill when creating or modifying configurations for any of these components, setting up new applications, or understanding how the system components interconnect.

## When to Use This Skill

Use this skill when:

- Creating or configuring new applications in the Ghostmind system
- Working with `meta.json` configuration files
- Setting up Docker containers, Docker Compose services, or Terraform infrastructure
- Configuring Tmux sessions, windows, and panes
- Writing or modifying custom scripts in the system
- Setting up MCP (Model Context Protocol) servers
- Configuring Cloudflared tunnels for local development
- Creating shell command routines
- Troubleshooting configuration issues
- Understanding the relationship between system components
- Working with environment variables, vault secrets, or variable substitution
- Setting up development environments in VS Code devcontainers

## ⚠️ CRITICAL: ALWAYS Fetch the Schema First

**This is the most important rule when working with the Ghostmind system:**

### Before ANY work involving meta.json, ALWAYS fetch the latest schema:

```
Schema URL: https://raw.githubusercontent.com/ghostmind-dev/run/refs/heads/main/meta/schema.json
```

**Why this is imperative:**
- The schema is the **authoritative source** for all available meta.json properties
- It contains validation rules, property structures, and available options
- The schema is actively maintained and may change
- Working without the schema can lead to invalid configurations
- Every component (docker, compose, terraform, etc.) has its configuration structure defined in the schema

**When to fetch:**
- At the start of any task involving the Ghostmind system
- Before creating or modifying meta.json files
- When documenting configuration options
- When troubleshooting configuration issues
- Before reading any component guides

**How to fetch:**
Use WebFetch to retrieve the schema and understand the complete structure before proceeding with configuration work

## Core Capabilities

### 1. Meta.json Configuration

meta.json is the **foundation** of every application in the Ghostmind system. It:

- Acts as the single source of truth for application configuration
- Defines what components exist (docker, compose, terraform, tmux, etc.)
- Links different parts together
- Configures development tools (MCP, tunnels, routines, custom scripts)
- Enables the `run` tool to orchestrate the application
- Supports variable substitution for dynamic behavior

**Key files to reference:**
- `references/meta-json-guide.md` - Core meta.json concepts and structure
- `references/system-overview.md` - Foundation document for understanding the system

### 2. Run CLI Tool

The `run` command is the unified orchestrator for all system operations. It's both:
- A CLI tool for executing commands
- A Deno TypeScript library for custom scripts

**Key commands:**
- `run docker` - Docker operations (build, push, exec)
- `run compose` - Docker Compose operations (up, down, build)
- `run terraform` - Terraform operations (plan, apply, destroy)
- `run tmux` - Tmux session management (init, attach, kill)
- `run custom` - Execute custom TypeScript scripts
- `run vault` - Secrets management (import, export)

**Reference:** `references/run-cli-overview.md`

### 3. Component Configuration

Each component has its own guide with meta.json configuration, examples, and best practices:

| Component      | Purpose                          | Guide                              |
|----------------|----------------------------------|------------------------------------|
| Docker         | Container configuration          | `references/docker-overview.md`    |
| Compose        | Multi-container orchestration    | `references/compose-overview.md`   |
| Terraform      | Infrastructure as code           | `references/terraform-overview.md` |
| Tmux           | Terminal session management      | `references/tmux-sections-guide.md`|
| Custom Scripts | TypeScript/Deno workflow scripts | `references/custom-scripts-guide.md`|
| Routines       | Shell command aliases            | `references/routines-guide.md`     |
| MCP            | AI agent tool servers            | `references/mcp-configuration.md`  |
| Tunnel         | Cloudflared public URL exposure  | `references/tunnel-configuration.md`|

**Each component guide includes:**
- Schema-fetching reminder
- Meta.json configuration section specific to that component
- Practical examples and patterns
- Best practices and common workflows

### 4. Development Environment

**VS Code Devcontainers:**
- 95% of projects are developed inside VS Code devcontainers
- Containers provide isolated, reproducible development environments
- Special environment variables are used for Docker-in-Docker scenarios

**Critical Environment Variables:**

**SRC vs LOCALHOST_SRC:**
- `SRC`: Path to source code inside the devcontainer (e.g., `/workspaces/my-app`)
- `LOCALHOST_SRC`: Path on the host machine (e.g., `/Users/me/code/my-app`)
- Required for Docker-in-Docker volume mounting
- Automatically set in devcontainer configurations

**PROJECT and APP:**
- `PROJECT`: Extracted from root meta.json `name` property
- `APP`: Extracted from app meta.json `name` property
- Used throughout the system for naming consistency
- Support variable substitution: `${PROJECT}`, `${APP}`

**Reference:** `references/system-overview.md` - Comprehensive environment variable documentation

### 5. Variable Substitution

Environment variables can be used dynamically in:
- meta.json files
- .env files
- Docker Compose configurations
- Terraform configurations

**Syntax:** `${VARIABLE_NAME}`

**Common patterns:**
```bash
# In .env files
SERVER_URL="http://localhost:${PORT}"
PUBLIC_URL="https://${TUNNEL_NAME}"

# In meta.json
"image": "${PROJECT}/${APP}:${VERSION}"
"hostname": "${APP}.${DOMAIN}"
```

**Reference:** `references/system-overview.md` - Variable substitution section

### 6. Secrets Management with Vault

**Vault Integration:**
- Centralized secrets management using Google Cloud Secret Manager
- Automatic import/export of environment variables
- Secure sharing across teams and environments

**Workflow:**
```bash
# Export secrets to vault
run vault export

# Import secrets from vault
run vault import
```

**File patterns:**
- `.env.base` - Non-sensitive defaults, committed to git
- `.env.local` - Local overrides, gitignored
- `.env.{environment}` - Environment-specific, gitignored
- `.env` - Generated by merging base + environment, gitignored

**Reference:** `references/system-overview.md` - Vault and secrets section

## Common Workflows

### Creating a New Application

1. **Fetch the schema** (always first!)
2. Create `meta.json` with basic properties (id, name, version)
3. Add component configurations as needed:
   - `docker` for containerization
   - `compose` for local development
   - `terraform` for cloud deployment
   - `tmux` for development environment
4. Create `.env.base` with non-sensitive defaults
5. Set up vault secrets if needed
6. Define custom scripts or routines for common tasks

**Reference:** `references/system-overview.md` - Project structure patterns

### Configuring a Component

1. **Fetch the schema** to understand available properties
2. Read the component-specific guide (e.g., `references/docker-overview.md`)
3. Add the component section to meta.json
4. Test the configuration using `run` commands
5. Document any custom scripts or routines

### Troubleshooting Configuration Issues

1. **Fetch the schema** to verify property names and structure
2. Validate meta.json against the schema
3. Check environment variables and variable substitution
4. Review component-specific logs using `run` commands
5. Consult the relevant component guide

### Working with Custom Scripts

1. Create TypeScript file in scripts directory
2. Import types: `CustomArgs`, `CustomOptions`
3. Import functions from `jsr:@ghostmind/run`
4. Add script reference to meta.json `custom` section
5. Execute with `run custom <script-name>`

**Reference:** `references/custom-scripts-guide.md`

## System Architecture Overview

### GitHub Organization

All Ghostmind repositories are in: https://github.com/orgs/ghostmind-dev/repositories

**Key repositories:**
- **config repos**: Shared configuration (Terraform, Docker, etc.)
- **init repos**: Application initialization and setup
- **play repos**: Experimentation and development environments
- **run**: The orchestrator CLI tool and library

### Multi-Meta.json Support

Projects can have:
- **Single meta.json**: At project root for simple applications
- **Multiple meta.json**: One root + multiple apps, each with their own meta.json
- **Root meta.json**: Defines project-level properties (PROJECT variable source)
- **App meta.json**: Defines app-specific configuration (APP variable source)

**Reference:** `references/meta-json-guide.md` - Multi-meta.json section

### Component Interconnection

Components in meta.json work together:

```
meta.json
├── docker       → Defines container image
│   └── Used by: compose (services), terraform (Cloud Run)
├── compose      → Local development orchestration
│   └── Uses: docker images, .env files
├── terraform    → Cloud infrastructure
│   └── Uses: docker images, .env variables
├── tmux         → Development environment
│   └── Can: run custom scripts, start compose services
├── custom       → TypeScript workflows
│   └── Can: orchestrate all components
├── routines     → Shell command aliases
│   └── Can: chain run commands
├── mcp          → AI agent tools
└── tunnel       → Public URL exposure
    └── Uses: PORT variable from .env
```

**Reference:** `references/system-overview.md` - System components section

## Best Practices

### 1. Schema-First Approach

- **ALWAYS fetch the schema** before working with meta.json
- Use the schema as documentation, not just validation
- Check the schema for new features and properties
- Validate configurations against the schema

### 2. Environment Variables

- Use `.env.base` for defaults (committed)
- Use `.env.local` for local overrides (gitignored)
- Use `.env.{environment}` for environment-specific values (gitignored)
- Never commit secrets to git - use vault
- Use variable substitution for dynamic values

### 3. Project Organization

- Start with minimal meta.json
- Add components incrementally as needed
- Keep custom scripts focused and single-purpose
- Use routines for simple command aliases
- Document complex workflows in custom scripts

### 4. Development Workflow

- Work in VS Code devcontainers for consistency
- Use `run` commands instead of direct docker/terraform
- Leverage Tmux for persistent development environments
- Use MCP for project-specific AI agent tools
- Use tunnels for webhook/OAuth testing

### 5. Configuration Management

- Keep meta.json clean and well-structured
- Use comments sparingly (JSON doesn't support them)
- Reference the schema for available options
- Test configurations in local environment first
- Use version control for configuration changes

## Getting Started

### First Steps with the Skill

1. **Fetch the schema** (https://raw.githubusercontent.com/ghostmind-dev/run/refs/heads/main/meta/schema.json)
2. Read `references/system-overview.md` for foundational understanding
3. Review `references/meta-json-guide.md` for core concepts
4. Identify which components you need (docker, compose, terraform, etc.)
5. Read the relevant component guides
6. Start with a minimal configuration and iterate

### Essential Reading Order

For comprehensive understanding, read in this order:

1. **SKILL.md** (this file) - Overview and when to use
2. **references/system-overview.md** - Foundation and architecture
3. **references/meta-json-guide.md** - Core configuration concepts
4. **Component guides** - As needed for specific components
5. **references/run-cli-overview.md** - CLI tool usage

### Quick Reference

**Common tasks:**
- New app setup → `system-overview.md` + `meta-json-guide.md`
- Docker config → `docker-overview.md`
- Compose config → `compose-overview.md`
- Terraform config → `terraform-overview.md`
- Tmux setup → `tmux-sections-guide.md`
- Custom workflows → `custom-scripts-guide.md`
- Simple aliases → `routines-guide.md`
- MCP servers → `mcp-configuration.md`
- Tunnels → `tunnel-configuration.md`

## Important Considerations

### Devcontainer Context

When working in VS Code devcontainers:
- Use `SRC` for paths inside the container
- Use `LOCALHOST_SRC` for Docker-in-Docker volume mounts
- Environment variables are automatically set
- Docker socket is shared from host

**Reference:** `references/system-overview.md` - Devcontainer section

### Variable Substitution Rules

- Variables use `${VAR_NAME}` syntax
- Substitution happens at runtime
- Variables must be defined in .env files or environment
- `PROJECT` and `APP` are automatically extracted from meta.json
- Nested substitution is not supported

**Reference:** `references/system-overview.md` - Variable substitution section

### Schema Validation

- meta.json files should validate against the schema
- The `run` tool validates configurations automatically
- Schema violations will cause errors
- Always fetch latest schema for validation

### Component Dependencies

Some components depend on others:
- **Compose** services reference **docker** images
- **Terraform** Cloud Run services reference **docker** images
- **Custom scripts** can orchestrate all components
- **Routines** can chain **run** commands
- **Tmux** can execute **custom** scripts or **routines**

## Support and Resources

### GitHub Organization
https://github.com/orgs/ghostmind-dev/repositories

### Key Repositories
- **run**: https://github.com/ghostmind-dev/run (CLI tool and library)
- **config repos**: Shared configuration templates
- **init repos**: Application initialization

### Schema URL
https://raw.githubusercontent.com/ghostmind-dev/run/refs/heads/main/meta/schema.json

### Documentation Files

All reference files are in `references/` directory:
- `system-overview.md` - Comprehensive system documentation
- `meta-json-guide.md` - Central configuration guide
- `run-cli-overview.md` - CLI tool documentation
- `docker-overview.md` - Docker configuration
- `compose-overview.md` - Docker Compose configuration
- `terraform-overview.md` - Terraform configuration
- `tmux-sections-guide.md` - Tmux configuration
- `custom-scripts-guide.md` - Custom script development
- `routines-guide.md` - Shell command aliases
- `mcp-configuration.md` - MCP server setup
- `tunnel-configuration.md` - Cloudflared tunnels

## Remember

The Ghostmind system is designed to be:
- **Flexible**: Not prescriptive about project structure
- **Configuration-driven**: meta.json as single source of truth
- **Component-based**: Add only what you need
- **Schema-validated**: Always fetch and use the schema
- **Environment-aware**: Support for multiple environments
- **Secure**: Vault integration for secrets

**Most importantly:** ALWAYS fetch the schema before working with meta.json configuration. This is the foundation of successful work with the Ghostmind system
