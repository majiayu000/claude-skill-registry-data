---
name: docker-compose-readme
description: Generates comprehensive README.md files for Docker Compose projects by analyzing compose.yml and .env.example files. Use when user requests documentation for a docker-compose folder or asks to create/update README files for container services.
allowed-tools: Read, Glob, Write, Edit
---

# Docker Compose README Generator Skill

## Purpose
This skill automatically generates professional, comprehensive README.md files for Docker Compose projects by analyzing the configuration files and creating standardized documentation.

## Activation Triggers
Use this skill when the user:
- Asks to create a README for a docker-compose folder
- Requests documentation for a container service
- Wants to update/improve existing README files
- Mentions "document this compose file" or similar requests

## Process

### 1. Analyze Project Structure
First, identify the files in the target directory:
- `compose.yml` or `docker-compose.yml` (required)
- `.env.example` or `.env` (for environment variables)
- Existing `README.md` (if updating)

### 2. Read Configuration Files
Read the compose.yml file to extract:
- Service name(s)
- Docker image and version
- Port mappings
- Volume mounts
- Network configuration
- Environment variables
- Restart policies
- Dependencies between services

Read the .env.example file to understand:
- Required environment variables
- Default values
- Variable purposes and descriptions

### 3. Generate README Structure

Create a comprehensive README.md with the following sections:

#### Header Section
```markdown
# [Service Name]

Brief description of what this service does (1-2 sentences).
```

#### Overview Section
Explain:
- What the service is
- Its primary purpose
- Key features or capabilities
- How it fits into the larger infrastructure

#### Prerequisites Section
List requirements:
- Docker and Docker Compose versions (if specific)
- Required networks (especially external networks)
- Dependencies on other services
- System requirements

#### Configuration Section
Document environment variables in a table format:

```markdown
| Variable | Default | Description |
|----------|---------|-------------|
| `VAR_NAME` | `default_value` | What this variable controls |
```

Include instructions for:
- Copying `.env.example` to `.env`
- Customizing values
- Security considerations for secrets

#### Usage Section
Provide common commands:
- Starting the service: `docker compose up -d`
- Stopping the service: `docker compose down`
- Viewing logs: `docker compose logs -f`
- Updating: `docker compose pull && docker compose up -d`
- Restarting: `docker compose restart`

#### Network Configuration
Explain:
- Which networks are used
- Whether networks are external or created by compose
- How to create required networks
- Network connectivity considerations

#### Volumes Section (if applicable)
Document:
- What data is persisted
- Volume mount purposes
- Backup considerations
- Path mappings

#### Port Mappings Section (if applicable)
List:
- Exposed ports and their purposes
- How to access the service
- Default URLs or endpoints

#### Security Considerations
Include relevant security notes:
- Secrets management (environment variables, secrets)
- Access control recommendations
- Network security (firewall rules, exposed ports)
- Privilege escalation warnings (if mounting docker.sock)
- Update policies

#### Troubleshooting Section
Common issues and solutions:
- Connection problems
- Permission errors
- Configuration mistakes
- Log analysis tips

#### Additional Resources
Links to:
- Official documentation
- Project website
- Docker Hub image page
- Community resources

### 4. Writing Style Guidelines

- **EXTREME concision**: Sacrifice grammar for brevity. Short fragments ok. No fluff.
- **Clear headings**: Scannable markdown structure
- **Code blocks**: Bash syntax highlighting
- **Tables**: Env vars, config options
- **Practical only**: Actionable info. Skip obvious.
- **Assume Docker knowledge**: Explain service-specific only
- **Security first**: Always include security notes

### 5. Special Cases

#### Multi-Service Compose Files
When compose.yml contains multiple services:
- Create a README that covers all services
- Use subsections for service-specific configuration
- Explain how services interact
- Document dependencies and startup order

#### Complex Network Topologies
For advanced networking:
- Diagram the network architecture (if needed)
- Explain network isolation
- Document inter-service communication

#### External Dependencies
If services depend on external resources:
- Clearly document what must exist beforehand
- Provide setup instructions or links
- Explain integration points

## Quality Checklist

Before completing, ensure the README includes:
- [ ] Clear title and description
- [ ] All environment variables documented
- [ ] Common usage commands provided
- [ ] Network requirements explained
- [ ] Security considerations mentioned
- [ ] Troubleshooting section included
- [ ] Links to official documentation
- [ ] Proper markdown formatting
- [ ] Accurate information from actual config files

## Example Output Structure

```markdown
# Service Name

One-line description.

## Overview
Detailed explanation...

## Prerequisites
- Requirement 1
- Requirement 2

## Configuration
### Environment Variables
| Variable | Default | Description |
|----------|---------|-------------|

## Usage
### Starting the Service
```bash
docker compose up -d
```

## Network Configuration
Details about networks...

## Security Considerations
Important security notes...

## Troubleshooting
Common issues...

## Additional Resources
- [Official Docs](url)
```

## Notes
- Always read existing files before writing/editing
- Preserve user customizations when updating existing READMEs
- Infer service purpose from image name and configuration if not obvious
- Use relative links for local file references in markdown
- Keep the tone professional but approachable
