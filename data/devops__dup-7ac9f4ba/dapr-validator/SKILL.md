---
name: Dapr Validator
description: Validate Dapr component configs, sidecar annotations, and mTLS settings. Use when: (1) Creating Dapr Component manifests, (2) Adding Dapr annotations to deployments, (3) Configuring pub/sub, state stores, or bindings, (4) Before deploying Dapr-enabled applications, (5) Generating new Dapr components. Validates secrets management (secretKeyRef), scopes, mTLS, sidecar resource limits, and namespace configuration.
---

## Overview

This skill validates Dapr configurations for security, correctness, and best practices. It ensures all Dapr components and sidecar annotations follow standards before deployment.

## Quick Start

### Validate Existing Components

```bash
# Validate a Dapr component file
python scripts/validate_component.py <component-file.yaml>

# Validate deployment Dapr annotations
python scripts/validate_deployment.py <deployment-file.yaml>
```

### Generate New Components

```bash
# Generate from templates
python scripts/generate_component.py --type statestore-postgres --name mystore --namespace todo-app

# Available templates in assets/:
# - statestore-postgres, statestore-redis
# - pubsub-kafka, pubsub-redis
# - configuration (mTLS)
```

## Validation Rule Codes

| Code | Category | Description |
|------|----------|-------------|
| DAPR-001 | Component | Missing namespace |
| DAPR-002 | Component | Using 'default' namespace |
| DAPR-003 | Security | Inline credentials (not using secretKeyRef) |
| DAPR-004 | Component | Missing or empty scopes |
| DAPR-005 | Configuration | mTLS not enabled |
| DAPR-006 | Deployment | Missing dapr.io/app-id annotation |
| DAPR-007 | Deployment | Missing sidecar resource limits |
| DAPR-008 | Component | Invalid component type |
| DAPR-009 | Deployment | app-id doesn't match component scopes |
| DAPR-010 | Deployment | Missing dapr.io/app-port annotation |

## Component Structure

Every Dapr component MUST have:

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: <lowercase-hyphenated>
  namespace: <explicit-namespace>    # Never "default"
spec:
  type: <component-type>
  version: v1
  metadata:
    - name: <key>
      secretKeyRef:                  # For sensitive values
        name: <secret-name>
        key: <secret-key>
scopes:                              # REQUIRED
  - <app-id-1>
```

## Validation Rules

### Secrets Management

```yaml
# ✅ CORRECT
metadata:
  - name: connectionString
    secretKeyRef:
      name: postgres-secrets
      key: connection-string

# ❌ WRONG - Never inline secrets
metadata:
  - name: connectionString
    value: "postgresql://user:password@host/db"
```

### Scopes (Required)

```yaml
# ✅ CORRECT - Scoped to specific apps
scopes:
  - todo-backend
  - todo-mcp-server

# ❌ WRONG - Empty or missing scopes
```

### mTLS Configuration

```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: dapr-config
spec:
  mtls:
    enabled: true    # MANDATORY
```

## Deployment Annotations

Every Dapr-enabled deployment MUST have:

```yaml
annotations:
  dapr.io/enabled: "true"
  dapr.io/app-id: "<unique-app-id>"
  dapr.io/app-port: "<container-port>"
  dapr.io/app-protocol: "http"
  dapr.io/sidecar-cpu-request: "100m"
  dapr.io/sidecar-memory-request: "128Mi"
  dapr.io/sidecar-cpu-limit: "300m"
  dapr.io/sidecar-memory-limit: "256Mi"
```

## Component Examples

### PostgreSQL State Store

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
  namespace: todo
spec:
  type: state.postgresql
  version: v1
  metadata:
    - name: connectionString
      secretKeyRef:
        name: postgres-secrets
        key: connection-string
scopes:
  - todo-backend
```

### Kafka Pub/Sub

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
  namespace: todo
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "kafka:9092"
    - name: authType
      value: "password"
    - name: saslUsername
      secretKeyRef:
        name: kafka-secrets
        key: username
    - name: saslPassword
      secretKeyRef:
        name: kafka-secrets
        key: password
scopes:
  - todo-backend
```

## Validation Output

```
## Dapr Validation Report

### Component: statestore
✅ Structure valid
✅ Namespace explicit
✅ Secrets use secretKeyRef
✅ Scopes defined
❌ ERROR: Empty scopes

### Deployment: todo-backend
✅ Dapr enabled
✅ App-id matches scopes
⚠️ WARNING: No sidecar limits

### Status: PASSED / BLOCKED
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Inline secrets | Use `secretKeyRef` |
| Missing scopes | Add explicit app-ids |
| Wrong app-id | Match annotation to scopes |
| No sidecar limits | Add resource annotations |
| Missing namespace | Use explicit namespace |

## Checklist

```
Components:
[ ] apiVersion: dapr.io/v1alpha1
[ ] Explicit namespace
[ ] secretKeyRef for credentials
[ ] Scopes defined

Deployments:
[ ] dapr.io/enabled: "true"
[ ] dapr.io/app-id set
[ ] dapr.io/app-port correct
[ ] Sidecar resource limits

Configuration:
[ ] mTLS enabled
```

## CLI Commands

```bash
dapr status -k
dapr components -k -n todo
kubectl describe component statestore -n todo
```
