---
name: container-validator
description: Dockerfile best practices, Kubernetes manifest validation, container security
version: 1.0.0
tags: [container, docker, kubernetes, validation, security]
---

# Container Validator Skill

## Purpose

The Container Validator Skill validates Docker containers and Kubernetes manifests against best practices, security standards, and compliance requirements. It ensures containers are production-ready, secure, and optimized.

**Key Capabilities:**
- Dockerfile best practice validation
- Kubernetes manifest validation
- Container security scanning
- Resource limit verification
- Image optimization recommendations
- CIS Docker Benchmark compliance

**Target Token Savings:** 75% (from ~2400 tokens to ~600 tokens)

## When to Use

- Building Docker images
- Deploying to Kubernetes
- Security audits
- CI/CD pipelines
- Production deployments
- Compliance checks

## Operations

### 1. validate-dockerfile
Validates Dockerfile against best practices.

### 2. validate-k8s
Validates Kubernetes manifests.

### 3. validate-compose
Validates docker-compose.yml files.

### 4. validate-all
Comprehensive container validation.

## Scripts

```bash
# Validate Dockerfile
python ~/.claude/skills/container-validator/scripts/main.py \
  --operation validate-dockerfile \
  --file Dockerfile

# Validate Kubernetes manifests
python ~/.claude/skills/container-validator/scripts/main.py \
  --operation validate-k8s \
  --dir ./k8s

# Validate docker-compose
python ~/.claude/skills/container-validator/scripts/main.py \
  --operation validate-compose \
  --file docker-compose.yml

# Comprehensive validation
python ~/.claude/skills/container-validator/scripts/main.py \
  --operation validate-all \
  --dir .
```

## Configuration

```json
{
  "container-validator": {
    "dockerfile": {
      "require_user": true,
      "require_healthcheck": true,
      "max_layers": 20,
      "scan_security": true
    },
    "kubernetes": {
      "require_resources": true,
      "require_liveness_probe": true,
      "require_readiness_probe": true,
      "scan_rbac": true
    },
    "security": {
      "allow_privileged": false,
      "require_read_only_root": true,
      "scan_vulnerabilities": true
    }
  }
}
```

## Examples

### Example 1: Validate Dockerfile

```bash
python ~/.claude/skills/container-validator/scripts/main.py \
  --operation validate-dockerfile \
  --file Dockerfile
```

**Output:**
```json
{
  "success": true,
  "operation": "validate-dockerfile",
  "issues": [
    {
      "line": 15,
      "severity": "critical",
      "type": "root_user",
      "description": "Container runs as root",
      "recommendation": "Add: USER nonroot"
    },
    {
      "line": 8,
      "severity": "medium",
      "type": "no_healthcheck",
      "description": "Missing HEALTHCHECK instruction",
      "recommendation": "Add: HEALTHCHECK CMD curl -f http://localhost/ || exit 1"
    }
  ],
  "execution_time_ms": 45
}
```

### Example 2: Validate Kubernetes Manifests

```bash
python ~/.claude/skills/container-validator/scripts/main.py \
  --operation validate-k8s \
  --dir ./k8s
```

**Output:**
```json
{
  "success": true,
  "operation": "validate-k8s",
  "files_validated": 5,
  "issues": [
    {
      "file": "deployment.yaml",
      "severity": "high",
      "type": "missing_resources",
      "description": "Container missing resource limits",
      "recommendation": "Add resources.limits.memory and resources.limits.cpu"
    },
    {
      "file": "deployment.yaml",
      "severity": "medium",
      "type": "missing_probe",
      "description": "Missing livenessProbe",
      "recommendation": "Add livenessProbe to container spec"
    }
  ],
  "execution_time_ms": 123
}
```

### Example 3: Validate Docker Compose

```bash
python ~/.claude/skills/container-validator/scripts/main.py \
  --operation validate-compose \
  --file docker-compose.yml
```

**Output:**
```json
{
  "success": true,
  "operation": "validate-compose",
  "services": 3,
  "issues": [
    {
      "service": "web",
      "severity": "high",
      "type": "exposed_port",
      "description": "Port exposed without security configuration",
      "recommendation": "Use internal network or add authentication"
    }
  ],
  "execution_time_ms": 67
}
```

### Example 4: Comprehensive Validation

```bash
python ~/.claude/skills/container-validator/scripts/main.py \
  --operation validate-all \
  --dir .
```

**Output:**
```json
{
  "success": true,
  "operation": "validate-all",
  "summary": {
    "dockerfiles": 2,
    "k8s_manifests": 5,
    "compose_files": 1,
    "total_issues": 8,
    "critical": 1,
    "high": 3,
    "medium": 4
  },
  "execution_time_ms": 234
}
```

## Token Economics

**Without Skill:** ~2400 tokens
**With Skill:** ~600 tokens (75% savings)

## Success Metrics

- Execution time: <100ms for Dockerfile validation
- Accuracy: >98% issue detection
- False positive rate: <3%

---

**Container Validator Skill v1.0.0** - Ensuring container best practices
