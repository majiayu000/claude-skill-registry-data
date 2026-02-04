---
name: dokploy-template-validation
description: "Validate Dokploy templates against conventions: YAML syntax, network structure, health checks, environment variables, security patterns, and quality standards."
version: 1.0.0
author: Home Lab Infrastructure Team
---

# Dokploy Template Validation

## When to Use This Skill

- As final step before completing a template
- When reviewing existing templates for issues
- When troubleshooting deployment problems
- When user asks to "validate" or "check" template

## When NOT to Use This Skill

- During template creation (use other skills first)
- For application-level debugging

## Prerequisites

- Complete docker-compose.yml
- Complete template.toml (if applicable)
- README.md (recommended)

---

## Validation Checklist

### 1. Structure Validation

#### 1.1 Required Sections
```yaml
# docker-compose.yml must have:
services:    # At least one service
volumes:     # If any services use volumes
networks:    # Must have app-net + dokploy-network
```

#### 1.2 Network Structure
```yaml
# REQUIRED: Two networks
networks:
  ${app}-net:
    driver: bridge
  dokploy-network:
    external: true
```

**Validation:**
- [ ] Internal network exists with `driver: bridge`
- [ ] `dokploy-network` exists with `external: true`
- [ ] Web services connect to both networks
- [ ] Database/cache services connect only to internal

### 2. Service Validation

#### 2.1 Image Configuration
```yaml
# CORRECT
image: postgres:16-alpine

# WRONG - fails validation
image: postgres:latest
image: postgres
image: myapp  # No tag
```

**Validation:**
- [ ] All images have explicit version tags
- [ ] No `:latest` tags
- [ ] Using official/verified images where possible

#### 2.2 Restart Policy
```yaml
# REQUIRED
restart: always
```

**Validation:**
- [ ] All services have `restart: always`

#### 2.3 Health Checks
```yaml
# REQUIRED for services with dependencies
healthcheck:
  test: [...]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 30s
```

**Validation:**
- [ ] All database services have health checks
- [ ] All app services have health checks
- [ ] Helper services can skip health checks

#### 2.4 Dependencies
```yaml
# CORRECT
depends_on:
  postgres:
    condition: service_healthy

# WRONG - no condition
depends_on:
  - postgres
```

**Validation:**
- [ ] Dependencies use `condition: service_healthy` or `service_started`
- [ ] Referenced services exist
- [ ] No circular dependencies

### 3. Environment Validation

#### 3.1 Required Variables
```yaml
# CORRECT - with error message
environment:
  DOMAIN: ${DOMAIN:?Set your domain}

# WRONG - no message
environment:
  DOMAIN: ${DOMAIN:?}

# WRONG - hardcoded
environment:
  PASSWORD: mysecretpassword
```

**Validation:**
- [ ] Secrets use `${VAR:?message}` syntax
- [ ] No hardcoded passwords/secrets
- [ ] Optional vars use `${VAR:-default}`
- [ ] Error messages are descriptive

#### 3.2 Connection Strings
```yaml
# CORRECT - uses service name
DATABASE_URL: postgresql://user:pass@postgres:5432/db

# WRONG - hardcoded IP
DATABASE_URL: postgresql://user:pass@172.17.0.2:5432/db
```

**Validation:**
- [ ] URLs use service names, not IPs
- [ ] Ports match service configuration

### 4. Traefik Validation

#### 4.1 Required Labels
```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.${name}.rule=Host(`${DOMAIN}`)"
  - "traefik.http.routers.${name}.entrypoints=websecure"
  - "traefik.http.routers.${name}.tls.certresolver=letsencrypt"
  - "traefik.http.services.${name}.loadbalancer.server.port=${port}"
  - "traefik.docker.network=dokploy-network"
```

**Validation:**
- [ ] `traefik.enable=true` present
- [ ] Router rule with Host
- [ ] Entrypoint is `websecure` (not `web`)
- [ ] TLS certresolver configured
- [ ] Loadbalancer port specified
- [ ] Docker network specified

#### 4.2 Router Names
**Validation:**
- [ ] Router names are unique across services
- [ ] Router names follow naming conventions

### 5. Volume Validation

```yaml
volumes:
  postgres-data:
    driver: local
```

**Validation:**
- [ ] All volumes defined in volumes section
- [ ] Using named volumes (not bind mounts)
- [ ] Volume names follow conventions

### 6. Security Validation

**Validation:**
- [ ] No hardcoded secrets
- [ ] Databases not on dokploy-network
- [ ] No privileged mode
- [ ] Debug disabled by default
- [ ] Image versions pinned

---

## Validation Commands

### YAML Syntax Check
```bash
# Check YAML syntax
docker compose -f docker-compose.yml config
```

### Compose Validation
```bash
# Validate and show resolved config
docker compose config

# Dry run
docker compose up --dry-run
```

### Environment Variable Check
```bash
# Check for undefined required variables
grep -E '\$\{[A-Z_]+:\?' docker-compose.yml
```

---

## Common Issues and Fixes

### Issue 1: Network Not Found
```
Error: network dokploy-network declared as external, but could not be found
```
**Fix:** Ensure Dokploy is running and has created the network.

### Issue 2: Service Not Healthy
```
dependency failed to start: container for service "postgres" is unhealthy
```
**Fix:** Check health check command, increase start_period.

### Issue 3: Port Already in Use
```
Error: port is already allocated
```
**Fix:** Change exposed port or stop conflicting service.

### Issue 4: Volume Permission Denied
```
Error: permission denied
```
**Fix:** Check volume permissions, consider init container.

### Issue 5: Traefik Not Routing
**Symptoms:** 404 or 502 errors
**Checks:**
- Service on dokploy-network?
- Router name unique?
- Port matches container port?
- Domain DNS configured?

---

## Validation Report Template

```markdown
# Template Validation Report: [Template Name]

## Summary
- Status: [PASS/FAIL/WARN]
- Date: [Date]
- Validator: [Name/Claude]

## Structure
- [ ] PASS: Required sections present
- [ ] PASS: Network structure correct
- [ ] PASS: Volume definitions valid

## Services
| Service | Image | Health | Networks | Status |
|---------|-------|--------|----------|--------|
| app     | myapp:1.0.0 | Yes | both | PASS |
| postgres| 16-alpine | Yes | internal | PASS |

## Environment
- [ ] PASS: All secrets use variable syntax
- [ ] PASS: No hardcoded passwords
- [ ] PASS: Connection strings use service names

## Traefik
- [ ] PASS: Required labels present
- [ ] PASS: Router names unique
- [ ] PASS: Using websecure entrypoint

## Security
- [ ] PASS: No privileged containers
- [ ] PASS: Databases internal only
- [ ] PASS: Image versions pinned

## Issues Found
1. [Issue description] - [Severity: High/Medium/Low]
2. [Issue description] - [Severity: High/Medium/Low]

## Recommendations
1. [Recommendation]
2. [Recommendation]

## Conclusion
Template is [ready for deployment / needs fixes before deployment].
```

---

## Automated Validation Script

```bash
#!/bin/bash
# validate-dokploy-template.sh

COMPOSE_FILE=${1:-docker-compose.yml}

echo "Validating Dokploy template: $COMPOSE_FILE"

# Check file exists
if [ ! -f "$COMPOSE_FILE" ]; then
    echo "ERROR: $COMPOSE_FILE not found"
    exit 1
fi

# YAML syntax
echo "Checking YAML syntax..."
docker compose -f "$COMPOSE_FILE" config > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: Invalid YAML syntax"
    docker compose -f "$COMPOSE_FILE" config
    exit 1
fi
echo "  PASS: YAML syntax valid"

# Check for :latest
echo "Checking image versions..."
if grep -q ":latest" "$COMPOSE_FILE"; then
    echo "  WARN: Found :latest tag"
fi

# Check for hardcoded passwords
echo "Checking for hardcoded secrets..."
if grep -qE "password:\s*['\"]?[a-zA-Z0-9]+" "$COMPOSE_FILE"; then
    echo "  WARN: Possible hardcoded password found"
fi

# Check for dokploy-network
echo "Checking networks..."
if ! grep -q "dokploy-network" "$COMPOSE_FILE"; then
    echo "  ERROR: dokploy-network not found"
fi

# Check for health checks
echo "Checking health checks..."
if ! grep -q "healthcheck" "$COMPOSE_FILE"; then
    echo "  WARN: No health checks found"
fi

echo "Validation complete"
```

---

## Integration

### Skills-First Approach (v2.0+)

This skill is part of the **skills-first architecture** - loaded during Validation phase (Phase 4) as the final automated validation before documentation.

### Related Skills
- All dokploy-* skills (validates their output)

### Invoked By
- `/dokploy-create` command: Phase 4 (Validation) - Step 2 (Final automated check)
- Manual validation requests

### Order in Workflow (Progressive Loading)
1-3. Phase 3: Generation skills (all files created)
4. `dokploy-security-hardening`: Security review
5. **This skill**: Convention compliance validation (Phase 4, Step 2)
6. `docker compose config`: Syntax validation
7. Phase 5: Documentation generation (no skills)

See: `.claude/commands/dokploy-create.md` for full workflow
