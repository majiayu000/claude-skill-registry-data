---
name: manifest-validator
description: Validates Kubernetes manifests using kubeconform, kube-score, and custom homelab policies. Use when creating or modifying YAML files, Helm values, or ArgoCD applications.
allowed-tools: Bash, Read, Grep, Glob, Write
---

# Manifest Validator

Validate Kubernetes manifests against schemas, best practices, and homelab standards.

## Trigger Phrases

- "validate", "검증해줘", "체크해줘"
- "manifest 확인", "yaml 검사"
- Before committing K8s YAML changes

## Validation Pipeline

### 1. YAML Syntax Check

```bash
# Basic YAML syntax
yamllint -d relaxed <file.yaml>

# Or with yq
yq eval '.' <file.yaml> > /dev/null && echo "Valid YAML"
```

### 2. Kubernetes Schema Validation (kubeconform)

```bash
# Single file
kubeconform -summary -output pretty <file.yaml>

# Directory
kubeconform -summary -output pretty platform/stacks/**/*.yaml

# With CRD schemas
kubeconform -summary \
  -schema-location default \
  -schema-location 'https://raw.githubusercontent.com/datreeio/CRDs-catalog/main/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json' \
  <file.yaml>
```

### 3. Best Practices (kube-score)

```bash
# Score a manifest
kube-score score <file.yaml>

# With specific checks
kube-score score --ignore-test container-resources <file.yaml>
```

### 4. Helm Template Validation

```bash
# Render and validate
helm template <release> <chart> -f values.yaml | kubeconform -summary

# With helmfile
cd bootstrap && helmfile -e home template | kubeconform -summary
```

## Homelab Policy Checks

### Required Fields

```yaml
# Every Deployment/StatefulSet must have:
spec:
  template:
    spec:
      containers:
        - resources:        # REQUIRED
            requests:
              cpu: "..."
              memory: "..."
            limits:
              cpu: "..."
              memory: "..."
          securityContext:  # REQUIRED
            runAsNonRoot: true
            readOnlyRootFilesystem: true
            allowPrivilegeEscalation: false
```

### Label Requirements

```yaml
metadata:
  labels:
    app.kubernetes.io/name: <app>        # REQUIRED
    app.kubernetes.io/instance: <app>    # REQUIRED
    app.kubernetes.io/managed-by: argocd # REQUIRED for platform apps
```

### GPU Workload Checks

```yaml
# If nvidia.com/gpu is requested:
tolerations:
  - key: nvidia.com/gpu  # REQUIRED
    operator: Exists
    effect: NoSchedule
nodeSelector:
  nvidia.com/gpu.present: "true"  # RECOMMENDED
```

### Secret Validation

- No hardcoded secrets in values
- Must use Infisical or external secrets
- No base64-encoded sensitive data in manifests

## ArgoCD Application Validation

### Required Structure

```yaml
apps:
  - name: <app-name>           # REQUIRED
    namespace: <namespace>      # REQUIRED
    chart: <chart>             # REQUIRED (or path for kustomize)
    repoURL: <url>             # REQUIRED
    targetRevision: "<version>" # REQUIRED, must be quoted string
```

### Values Validation

```bash
# Extract and validate values
yq '.apps[].values' <app.yaml> | kubeconform -summary
```

## Output Format

```
## Validation Results

### ✅ Passed
- YAML syntax valid
- Kubernetes schema valid
- Labels present

### ⚠️ Warnings
- [kube-score] Container has no readiness probe
- [policy] Missing recommended nodeSelector

### ❌ Errors
- [kubeconform] Invalid apiVersion: apps/v1beta1
- [policy] Missing required resource limits

### Fixes Required
1. Update apiVersion to apps/v1
2. Add resource limits to container spec
```

## Integration with CI

```bash
# Pre-commit hook
#!/bin/bash
set -e
changed_yamls=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.ya?ml$' || true)
if [ -n "$changed_yamls" ]; then
  echo "$changed_yamls" | xargs kubeconform -summary -output pretty
fi
```

## Reference

- @.claude/rules/kubernetes.md
- @.claude/rules/argocd-apps.md
- https://github.com/yannh/kubeconform
- https://github.com/zegl/kube-score
