---
name: helm-charts
description: Use when helm chart development — templates, values, hooks, dependencies,
  chart testing, repository management. Use when working with helm charts.
domain: devops
author: oyi77
license: Apache-2.0
subdomain: devops
tags:
- charts
- ci-cd
- devops
- helm
- infrastructure
- testing
version: 1.0.0
category: devops
---



## Overview

Helm is the Kubernetes package manager. Charts are templated Kubernetes manifests with configurable values. Supports dependencies, hooks, release management, and chart repositories.

## Capabilities

- Templated Kubernetes manifests with Go templates
- Values-driven configuration
- Chart dependencies and subcharts
- Pre/post install/upgrade hooks
- Release lifecycle management (install/upgrade/rollback)
- Chart testing and repository publishing

## When to Use
**Trigger phrases:**
- "helm charts"
- "Helm chart development — templates, values, hooks, dependencies, chart testing, "


- Packaging Kubernetes applications for distribution
- Multi-environment deployments with value overrides
- Complex applications with multiple K8s resources
- Need release history and rollback capabilities
- Sharing reusable K8s packages via repositories

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The helm-charts workflow follows a standard pipeline pattern.

Core flow:
```
# helm-charts primary flow
input = prepare(raw_data)
result = process(input, config={chart, charts, dependencies, development, helm})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Chart Structure
```
mychart/
  Chart.yaml          # Metadata + dependencies
  values.yaml         # Default values
  templates/
    deployment.yaml
    service.yaml
    ingress.yaml
    _helpers.tpl      # Template helpers
    NOTES.txt         # Post-install notes
  charts/             # Subcharts
  tests/
    test-connection.yaml
```

### Chart.yaml
```yaml
apiVersion: v2
name: myapp
version: 1.2.0
appVersion: "2.0.0"
description: My application Helm chart
dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
```

### Template with Values
```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  template:
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          ports:
            - containerPort: {{ .Values.service.port }}
          {{- if .Values.resources }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          {{- end }}
          envFrom:
            - configMapRef:
                name: {{ include "myapp.fullname" . }}-config
```

### Hooks
```yaml
# templates/job-migrate.yaml
apiVersion: batch/v1
kind: Job
metadata:
  annotations:
    "helm.sh/hook": pre-upgrade
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": before-hook-creation
spec:
  template:
    spec:
      containers:
        - name: migrate
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          command: ["./migrate", "up"]
      restartPolicy: Never
```

### Commands
```bash
# Install
helm install myapp ./mychart -f values-prod.yaml

# Upgrade
helm upgrade myapp ./mychart -f values-prod.yaml --set image.tag=v2.1

# Rollback
helm rollback myapp 1

# Test
helm test myapp

# Package
helm package ./mychart

# Lint
helm lint ./mychart
```

## Common Patterns

- **_helpers.tpl**: define reusable template snippets
- **Named templates**: `{{ define "name" }}...{{ end }}`
- **Conditional sections**: `{{- if .Values.ingress.enabled }}`
- **Range loops**: `{{- range .Values.env }}`
- **Lookup**: `lookup` function to check existing resources

## How to Use

1. Define infrastructure as code (Terraform, CloudFormation, Pulumi)
2. Review changes through PR process before applying
3. Configure monitoring and alerting for critical paths
4. Set up secrets management (Vault, AWS Secrets Manager, etc.)
5. Document runbooks for deployment, rollback, and incident response
6. Test disaster recovery procedures regularly

## Red Flags

- **Infrastructure changes without review**: Unreviewed changes cause outages — use PRs for infra code
- **No rollback strategy**: Every deployment needs a tested rollback plan before it runs
- **Secrets in configuration files**: Secrets in YAML/JSON get committed to version control
- **Missing monitoring and alerting**: Without monitoring, outages go undetected until users report them
- **No documentation for runbooks**: Without runbooks, on-call engineers waste time re-discovering procedures

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Manual deployments are fine" | Manual deployments are error-prone and不可 repeatable. Automate. |
| "We do not need monitoring" | Without monitoring, you are flying blind. Add observability from day one. |
| "Infrastructure as code is overkill" | IaC enables reproducibility, version control, and disaster recovery. |