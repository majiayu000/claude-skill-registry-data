---
name: helm-chart-creation
description: >
  Complete patterns for creating and managing Helm charts: chart structure,
  templates, values, dependencies, and deployment workflows for packaging
  Kubernetes applications.
---

# Helm Chart Creation Skill

## When to use this Skill

Use this Skill whenever you are:

- Creating new Helm charts for Kubernetes applications.
- Packaging multiple Kubernetes manifests into a reusable chart.
- Templating Kubernetes resources for different environments.
- Managing chart dependencies and subcharts.
- Deploying applications with Helm install/upgrade/rollback.
- Setting up Helm repositories for chart distribution.

This Skill works for **any** Helm project, not just a single repository.

## Core Goals

- Create **reusable, maintainable** Helm charts.
- Follow **official Helm best practices**.
- Use **proper templating** for flexibility.
- Implement **sensible defaults** with override capability.
- Enable **multi-environment** deployments.
- Provide **clear documentation** for chart users.

## What is Helm?

Helm is the **package manager for Kubernetes**. It allows you to:

- Package multiple K8s manifests into a single **chart**.
- Template values for different environments.
- Install/upgrade/rollback applications with single commands.
- Share charts via repositories.

```
Without Helm:                    With Helm:
kubectl apply -f file1.yaml      helm install my-app ./chart
kubectl apply -f file2.yaml      (one command!)
kubectl apply -f file3.yaml
... (10+ commands)
```

## Helm Chart Structure

### Basic Structure

```
my-chart/
├── Chart.yaml          # Chart metadata (name, version)
├── values.yaml         # Default configuration values
├── charts/             # Dependencies (subcharts)
├── templates/          # Kubernetes manifest templates
│   ├── _helpers.tpl    # Template helpers/partials
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   └── NOTES.txt       # Post-install notes
└── .helmignore         # Files to ignore when packaging
```

### Complete Structure

```
my-chart/
├── Chart.yaml          # Required: Chart metadata
├── Chart.lock          # Generated: Dependency lock file
├── values.yaml         # Required: Default values
├── values.schema.json  # Optional: JSON schema for values
├── charts/             # Optional: Dependencies
├── crds/               # Optional: Custom Resource Definitions
├── templates/          # Required: Template files
│   ├── _helpers.tpl    # Partial templates
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── ingress.yaml
│   ├── hpa.yaml
│   ├── serviceaccount.yaml
│   ├── NOTES.txt       # Post-install instructions
│   └── tests/          # Helm tests
│       └── test-connection.yaml
├── .helmignore         # Ignore patterns
└── README.md           # Chart documentation
```

## Chart.yaml

The Chart.yaml file contains metadata about the chart.

### Minimal Chart.yaml

```yaml
apiVersion: v2
name: my-app
description: A Helm chart for my application
type: application
version: 0.1.0
appVersion: "1.0.0"
```

### Complete Chart.yaml

```yaml
apiVersion: v2
name: todo-app
description: A Helm chart for Todo Application
type: application
version: 1.0.0
appVersion: "1.0.0"

# Chart maintainers
maintainers:
  - name: Your Name
    email: your@email.com
    url: https://github.com/yourusername

# Keywords for searching
keywords:
  - todo
  - fastapi
  - nextjs

# Home page
home: https://github.com/yourusername/todo-app

# Source code
sources:
  - https://github.com/yourusername/todo-app

# Icon URL
icon: https://example.com/icon.png

# Dependencies (subcharts)
dependencies:
  - name: postgresql
    version: "12.0.0"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled

# Kubernetes version constraint
kubeVersion: ">=1.25.0"
```

### Chart Types

| Type | Description |
|------|-------------|
| `application` | Deploys an application (default) |
| `library` | Provides helpers for other charts |

### Versioning

- **version**: Chart version (SemVer 2)
- **appVersion**: Application version (informational)

```yaml
version: 1.2.3      # Chart version
appVersion: "2.0.0" # Your app's version
```

## values.yaml

The values.yaml file contains default configuration values.

### Basic values.yaml

```yaml
# Number of replicas
replicaCount: 1

# Container image
image:
  repository: my-app
  tag: "latest"
  pullPolicy: IfNotPresent

# Service configuration
service:
  type: ClusterIP
  port: 80

# Resource limits
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi
```

### Complete values.yaml

```yaml
# ======================
# Global settings
# ======================
global:
  environment: production

# ======================
# Backend Configuration
# ======================
backend:
  enabled: true
  replicaCount: 2

  image:
    repository: todo-backend
    tag: "v1.0.0"
    pullPolicy: IfNotPresent

  service:
    type: ClusterIP
    port: 8000

  resources:
    requests:
      cpu: "100m"
      memory: "128Mi"
    limits:
      cpu: "500m"
      memory: "512Mi"

  # Environment variables
  env:
    APP_ENV: "production"
    LOG_LEVEL: "info"

  # Health probes
  livenessProbe:
    enabled: true
    path: /health
    initialDelaySeconds: 10
    periodSeconds: 15

  readinessProbe:
    enabled: true
    path: /ready
    initialDelaySeconds: 5
    periodSeconds: 10

# ======================
# Frontend Configuration
# ======================
frontend:
  enabled: true
  replicaCount: 2

  image:
    repository: todo-frontend
    tag: "v1.0.0"
    pullPolicy: IfNotPresent

  service:
    type: NodePort
    port: 3000
    nodePort: 30000

  resources:
    requests:
      cpu: "100m"
      memory: "128Mi"
    limits:
      cpu: "500m"
      memory: "256Mi"

  env:
    NEXT_PUBLIC_API_URL: "http://backend-service:8000"

# ======================
# Secrets (use external secret manager in production)
# ======================
secrets:
  databaseUrl: ""
  authSecret: ""
  apiKey: ""

# ======================
# Ingress Configuration
# ======================
ingress:
  enabled: false
  className: "nginx"
  hosts:
    - host: todo.example.com
      paths:
        - path: /
          pathType: Prefix
  tls: []

# ======================
# Autoscaling
# ======================
autoscaling:
  enabled: false
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
```

### Values Best Practices

1. **Group related values** under parent keys.
2. **Use comments** to document each section.
3. **Provide sensible defaults** that work out of the box.
4. **Use `enabled` flags** for optional features.
5. **Keep secrets empty** (override at install time).

## Templates

Templates are Kubernetes manifests with Go templating.

### Template Syntax Basics

```yaml
# Access values
{{ .Values.replicaCount }}

# Access chart metadata
{{ .Chart.Name }}
{{ .Chart.Version }}

# Access release info
{{ .Release.Name }}
{{ .Release.Namespace }}

# Built-in objects
{{ .Capabilities.KubeVersion }}
```

### Common Template Patterns

#### Accessing Values

```yaml
# Simple value
replicas: {{ .Values.replicaCount }}

# Nested value
image: {{ .Values.image.repository }}:{{ .Values.image.tag }}

# With default
port: {{ .Values.service.port | default 80 }}

# Quote strings
env: {{ .Values.environment | quote }}
```

#### Conditionals (if/else)

```yaml
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ .Release.Name }}-ingress
spec:
  # ...
{{- end }}

# if-else
{{- if eq .Values.service.type "NodePort" }}
  nodePort: {{ .Values.service.nodePort }}
{{- else }}
  # ClusterIP doesn't need nodePort
{{- end }}

# Multiple conditions
{{- if and .Values.backend.enabled (gt .Values.backend.replicaCount 0) }}
  # Deploy backend
{{- end }}
```

#### Loops (range)

```yaml
# Loop over list
env:
{{- range .Values.env }}
  - name: {{ .name }}
    value: {{ .value | quote }}
{{- end }}

# Loop over map
{{- range $key, $value := .Values.labels }}
  {{ $key }}: {{ $value | quote }}
{{- end }}

# Loop with index
{{- range $index, $host := .Values.ingress.hosts }}
  - host: {{ $host }}
{{- end }}
```

#### With (Scope)

```yaml
# Narrow scope for cleaner templates
{{- with .Values.backend }}
spec:
  replicas: {{ .replicaCount }}
  template:
    spec:
      containers:
        - name: backend
          image: {{ .image.repository }}:{{ .image.tag }}
{{- end }}
```

### _helpers.tpl

Define reusable template helpers in `templates/_helpers.tpl`.

```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "my-chart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "my-chart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "my-chart.labels" -}}
helm.sh/chart: {{ include "my-chart.chart" . }}
{{ include "my-chart.selectorLabels" . }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "my-chart.selectorLabels" -}}
app.kubernetes.io/name: {{ include "my-chart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create chart name and version
*/}}
{{- define "my-chart.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Backend image
*/}}
{{- define "my-chart.backendImage" -}}
{{- printf "%s:%s" .Values.backend.image.repository .Values.backend.image.tag }}
{{- end }}
```

### Using Helpers

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-chart.fullname" . }}-backend
  labels:
    {{- include "my-chart.labels" . | nindent 4 }}
spec:
  selector:
    matchLabels:
      {{- include "my-chart.selectorLabels" . | nindent 6 }}
      component: backend
```

## Template Examples

### deployment.yaml

```yaml
{{- if .Values.backend.enabled }}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-chart.fullname" . }}-backend
  namespace: {{ .Release.Namespace }}
  labels:
    {{- include "my-chart.labels" . | nindent 4 }}
    component: backend
spec:
  replicas: {{ .Values.backend.replicaCount }}
  selector:
    matchLabels:
      {{- include "my-chart.selectorLabels" . | nindent 6 }}
      component: backend
  template:
    metadata:
      labels:
        {{- include "my-chart.selectorLabels" . | nindent 8 }}
        component: backend
    spec:
      containers:
        - name: backend
          image: "{{ .Values.backend.image.repository }}:{{ .Values.backend.image.tag }}"
          imagePullPolicy: {{ .Values.backend.image.pullPolicy }}
          ports:
            - containerPort: {{ .Values.backend.service.port }}
              protocol: TCP
          {{- if .Values.backend.env }}
          env:
            {{- range $key, $value := .Values.backend.env }}
            - name: {{ $key }}
              value: {{ $value | quote }}
            {{- end }}
          {{- end }}
          envFrom:
            - secretRef:
                name: {{ include "my-chart.fullname" . }}-secrets
          {{- with .Values.backend.resources }}
          resources:
            {{- toYaml . | nindent 12 }}
          {{- end }}
          {{- if .Values.backend.livenessProbe.enabled }}
          livenessProbe:
            httpGet:
              path: {{ .Values.backend.livenessProbe.path }}
              port: {{ .Values.backend.service.port }}
            initialDelaySeconds: {{ .Values.backend.livenessProbe.initialDelaySeconds }}
            periodSeconds: {{ .Values.backend.livenessProbe.periodSeconds }}
          {{- end }}
          {{- if .Values.backend.readinessProbe.enabled }}
          readinessProbe:
            httpGet:
              path: {{ .Values.backend.readinessProbe.path }}
              port: {{ .Values.backend.service.port }}
            initialDelaySeconds: {{ .Values.backend.readinessProbe.initialDelaySeconds }}
            periodSeconds: {{ .Values.backend.readinessProbe.periodSeconds }}
          {{- end }}
{{- end }}
```

### service.yaml

```yaml
{{- if .Values.backend.enabled }}
apiVersion: v1
kind: Service
metadata:
  name: {{ include "my-chart.fullname" . }}-backend
  namespace: {{ .Release.Namespace }}
  labels:
    {{- include "my-chart.labels" . | nindent 4 }}
    component: backend
spec:
  type: {{ .Values.backend.service.type }}
  ports:
    - port: {{ .Values.backend.service.port }}
      targetPort: {{ .Values.backend.service.port }}
      protocol: TCP
      name: http
      {{- if and (eq .Values.backend.service.type "NodePort") .Values.backend.service.nodePort }}
      nodePort: {{ .Values.backend.service.nodePort }}
      {{- end }}
  selector:
    {{- include "my-chart.selectorLabels" . | nindent 4 }}
    component: backend
{{- end }}
```

### secret.yaml

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "my-chart.fullname" . }}-secrets
  namespace: {{ .Release.Namespace }}
  labels:
    {{- include "my-chart.labels" . | nindent 4 }}
type: Opaque
stringData:
  {{- if .Values.secrets.databaseUrl }}
  DATABASE_URL: {{ .Values.secrets.databaseUrl | quote }}
  {{- end }}
  {{- if .Values.secrets.authSecret }}
  BETTER_AUTH_SECRET: {{ .Values.secrets.authSecret | quote }}
  {{- end }}
  {{- if .Values.secrets.apiKey }}
  API_KEY: {{ .Values.secrets.apiKey | quote }}
  {{- end }}
```

### configmap.yaml

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "my-chart.fullname" . }}-config
  namespace: {{ .Release.Namespace }}
  labels:
    {{- include "my-chart.labels" . | nindent 4 }}
data:
  APP_ENV: {{ .Values.global.environment | quote }}
  {{- range $key, $value := .Values.backend.env }}
  {{ $key }}: {{ $value | quote }}
  {{- end }}
```

### NOTES.txt

```
Thank you for installing {{ .Chart.Name }}!

Your release is named: {{ .Release.Name }}

To get the application URL, run:

{{- if .Values.ingress.enabled }}
{{- range $host := .Values.ingress.hosts }}
  http{{ if $.Values.ingress.tls }}s{{ end }}://{{ $host.host }}
{{- end }}
{{- else if contains "NodePort" .Values.frontend.service.type }}
  export NODE_PORT=$(kubectl get --namespace {{ .Release.Namespace }} -o jsonpath="{.spec.ports[0].nodePort}" services {{ include "my-chart.fullname" . }}-frontend)
  export NODE_IP=$(kubectl get nodes --namespace {{ .Release.Namespace }} -o jsonpath="{.items[0].status.addresses[0].address}")
  echo "Frontend: http://$NODE_IP:$NODE_PORT"
{{- else if contains "ClusterIP" .Values.frontend.service.type }}
  kubectl port-forward --namespace {{ .Release.Namespace }} svc/{{ include "my-chart.fullname" . }}-frontend 3000:{{ .Values.frontend.service.port }}
  echo "Frontend: http://127.0.0.1:3000"
{{- end }}

Backend API is available internally at:
  http://{{ include "my-chart.fullname" . }}-backend:{{ .Values.backend.service.port }}
```

## Helm Commands

### Chart Development

```bash
# Create new chart
helm create my-chart

# Lint chart (check for errors)
helm lint ./my-chart

# Template locally (see rendered output)
helm template my-release ./my-chart

# Template with custom values
helm template my-release ./my-chart -f custom-values.yaml

# Dry run (validate against cluster)
helm install my-release ./my-chart --dry-run --debug
```

### Install & Upgrade

```bash
# Install chart
helm install my-release ./my-chart

# Install in namespace
helm install my-release ./my-chart -n my-namespace --create-namespace

# Install with custom values file
helm install my-release ./my-chart -f production-values.yaml

# Install with value overrides
helm install my-release ./my-chart --set replicaCount=3

# Install with multiple value overrides
helm install my-release ./my-chart \
  --set backend.replicaCount=3 \
  --set frontend.replicaCount=2 \
  --set secrets.databaseUrl="postgresql://..."

# Upgrade release
helm upgrade my-release ./my-chart

# Upgrade with values
helm upgrade my-release ./my-chart -f new-values.yaml

# Install or upgrade (idempotent)
helm upgrade --install my-release ./my-chart
```

### Management

```bash
# List releases
helm list
helm list -A  # All namespaces

# Get release status
helm status my-release

# Get release history
helm history my-release

# Rollback to previous revision
helm rollback my-release

# Rollback to specific revision
helm rollback my-release 2

# Uninstall release
helm uninstall my-release

# Get values of deployed release
helm get values my-release

# Get all info about release
helm get all my-release
```

### Repositories

```bash
# Add repository
helm repo add bitnami https://charts.bitnami.com/bitnami

# Update repositories
helm repo update

# Search repository
helm search repo nginx

# Install from repository
helm install my-nginx bitnami/nginx
```

### Packaging

```bash
# Package chart
helm package ./my-chart

# Package with version
helm package ./my-chart --version 1.0.0

# Create index file (for repo)
helm repo index .
```

## Multi-Environment Deployment

### values-dev.yaml

```yaml
backend:
  replicaCount: 1
  image:
    tag: "dev"
  resources:
    requests:
      cpu: "50m"
      memory: "64Mi"
    limits:
      cpu: "200m"
      memory: "256Mi"

frontend:
  replicaCount: 1
  image:
    tag: "dev"

secrets:
  databaseUrl: "postgresql://dev-db/todo"
```

### values-prod.yaml

```yaml
backend:
  replicaCount: 3
  image:
    tag: "v1.0.0"
  resources:
    requests:
      cpu: "200m"
      memory: "256Mi"
    limits:
      cpu: "1000m"
      memory: "1Gi"

frontend:
  replicaCount: 3
  image:
    tag: "v1.0.0"

ingress:
  enabled: true
  hosts:
    - host: todo.example.com

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
```

### Deployment Commands

```bash
# Development
helm upgrade --install todo-dev ./todo-chart \
  -f values-dev.yaml \
  -n development --create-namespace

# Production
helm upgrade --install todo-prod ./todo-chart \
  -f values-prod.yaml \
  --set secrets.databaseUrl="$DATABASE_URL" \
  --set secrets.authSecret="$AUTH_SECRET" \
  -n production --create-namespace
```

## Best Practices Summary

### Chart Structure

- Use `helm create` to generate initial structure.
- Keep template file names descriptive (resource type in name).
- Use `_helpers.tpl` for reusable template functions.
- Include `NOTES.txt` with post-install instructions.

### Values

- Group related values under parent keys.
- Provide sensible defaults.
- Use `enabled` flags for optional features.
- Document values with comments.
- Keep secrets empty in default values.

### Templates

- Use helper functions for names and labels.
- Use `nindent` for proper YAML indentation.
- Quote strings with `| quote`.
- Use `{{- }}` to control whitespace.
- Use `with` to scope nested values.

### Security

- Never commit actual secrets in values files.
- Use external secret management in production.
- Set resource limits on all containers.
- Run containers as non-root when possible.

### Deployment

- Use `helm upgrade --install` for idempotent deploys.
- Use separate values files per environment.
- Pass secrets via `--set` or external secret manager.
- Test with `--dry-run` before actual deployment.

## References

- [Helm Official Documentation](https://helm.sh/docs/)
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Chart Template Guide](https://helm.sh/docs/chart_template_guide/)
- [Helm Cheatsheet](https://helm.sh/docs/intro/cheatsheet/)
- [Helm Charts 2025 Guide](https://atmosly.com/knowledge/helm-charts-in-kubernetes-definitive-guide-for-2025)
