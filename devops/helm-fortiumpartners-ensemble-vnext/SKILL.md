---
name: helm
description: Package and template Kubernetes apps with Helm — Chart.yaml, values, template helpers, releases.
when_to_use: Reach for this specifically when authoring or installing Helm charts (Chart.yaml, templates/, values.yaml). For writing raw Kubernetes manifests directly use kubernetes; to detect whether a project uses Helm/K8s/Kustomize/ArgoCD run tooling-detector. Helm packaging skill — a layer on top of Kubernetes.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
paths:
  - "**/Chart.yaml"
  - "**/values*.yaml"
  - "templates/**/*.yaml"
  - "charts/**"
---

# Helm Chart Quick Reference

**Version**: 1.0.0 | **Target Size**: <100KB | **Purpose**: Fast reference for Helm chart development and deployment

---

## Overview

Helm is a package manager for Kubernetes that simplifies application deployment through **charts** - pre-configured Kubernetes resource templates. This quick reference provides essential patterns for chart creation, templating, and deployment.

**When to Load This Skill**:
- Detected: `Chart.yaml`, `values.yaml`, `templates/` directory
- Manual: `--tools=helm` flag
- Use Case: Kubernetes application packaging and deployment

**Progressive Disclosure**:
- **This file (SKILL.md)**: Quick reference for immediate use
- **REFERENCE.md**: Comprehensive guide with advanced patterns and 10+ production examples

---

## Table of Contents

1. [Chart Structure](#chart-structure)
2. [Chart.yaml Configuration](#chartyaml-configuration)
3. [Template Syntax Quick Reference](#template-syntax-quick-reference)
4. [Values File Patterns](#values-file-patterns)
5. [Common Helm Commands](#common-helm-commands)
6. [Dependency Management](#dependency-management)
7. [Release Lifecycle](#release-lifecycle)
8. [Testing with Helm](#testing-with-helm)
9. [Security Best Practices](#security-best-practices)
10. [Quick Examples](#quick-examples)

---

## Chart Structure

Standard Helm chart directory layout:

```
mychart/
├── Chart.yaml          # Chart metadata (name, version, description)
├── values.yaml         # Default configuration values
├── charts/             # Chart dependencies (subcharts)
├── templates/          # Kubernetes manifest templates
│   ├── NOTES.txt       # Post-install usage notes
│   ├── _helpers.tpl    # Named templates (partials)
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   └── secret.yaml
├── .helmignore         # Files to exclude from packaging
└── README.md           # Chart documentation
```

**Key Concepts**:
- **Chart.yaml**: Defines chart metadata (name, version, dependencies)
- **values.yaml**: Default configuration values (can be overridden)
- **templates/**: Go templates that render to Kubernetes manifests
- **charts/**: Dependency charts (populated by `helm dependency update`)

---

## Chart.yaml Configuration

**Chart.yaml** defines chart metadata and dependencies:

```yaml
apiVersion: v2                    # Helm 3 uses v2
name: webapp                      # Chart name (DNS-compatible)
version: 1.2.3                    # Chart version (SemVer)
appVersion: "2.0.1"               # Application version
description: Production web application with autoscaling
type: application                 # application or library
keywords:
  - webapp
  - kubernetes
  - production
home: https://example.com
sources:
  - https://github.com/example/webapp
maintainers:
  - name: DevOps Team
    email: devops@example.com
dependencies:
  - name: postgresql
    version: "12.1.0"
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled  # Optional: conditional dependency
  - name: redis
    version: "17.3.0"
    repository: https://charts.bitnami.com/bitnami
    condition: redis.enabled
```

**Version Guidelines**:
- **Chart version**: Increment when chart templates/structure changes
- **appVersion**: Application/container image version (independent of chart version)
- Use [Semantic Versioning](https://semver.org/): MAJOR.MINOR.PATCH

**Dependency Types**:
- **Condition**: Enable/disable via values (`postgresql.enabled: true`)
- **Tags**: Group dependencies (`--set tags.database=false`)
- **Import-values**: Import child chart values into parent

---

## Template Syntax Quick Reference

Helm uses [Go templates](https://pkg.go.dev/text/template) with additional functions.

### Built-in Objects

```yaml
# Access values from values.yaml
{{ .Values.replicaCount }}
{{ .Values.image.repository }}
{{ .Values.service.port }}

# Release information
{{ .Release.Name }}           # Release name (helm install <name>)
{{ .Release.Namespace }}      # Kubernetes namespace
{{ .Release.IsInstall }}      # true if installing (not upgrading)
{{ .Release.IsUpgrade }}      # true if upgrading
{{ .Release.Revision }}       # Revision number

# Chart metadata (from Chart.yaml)
{{ .Chart.Name }}
{{ .Chart.Version }}
{{ .Chart.AppVersion }}

# Kubernetes cluster capabilities
{{ .Capabilities.APIVersions.Has "apps/v1" }}
{{ .Capabilities.KubeVersion.Major }}
{{ .Capabilities.KubeVersion.Minor }}

# Template context
{{ .Template.Name }}          # Current template file name
{{ .Template.BasePath }}      # Template directory path
```

### Control Structures

```yaml
# If/Else conditionals
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
# ... ingress spec
{{- end }}

# If/Else with multiple conditions
{{- if and .Values.persistence.enabled (not .Values.persistence.existingClaim) }}
# Create new PVC
{{- else if .Values.persistence.existingClaim }}
# Use existing PVC
{{- else }}
# Use emptyDir
{{- end }}

# Range (loops)
{{- range .Values.extraEnv }}
- name: {{ .name }}
  value: {{ .value | quote }}
{{- end }}

# Range with key-value pairs
{{- range $key, $value := .Values.config }}
{{ $key }}: {{ $value | quote }}
{{- end }}

# With (scope modification)
{{- with .Values.nodeSelector }}
nodeSelector:
  {{- toYaml . | nindent 2 }}
{{- end }}
```

### Template Functions

**String Functions**:
```yaml
{{ .Values.name | quote }}              # "webapp"
{{ .Values.name | upper }}              # WEBAPP
{{ .Values.name | lower }}              # webapp
{{ .Values.name | title }}              # Webapp
{{ .Values.name | trim }}               # Remove whitespace
{{ .Values.name | trunc 10 }}           # Truncate to 10 chars
{{ .Values.name | default "default" }}  # Default if empty
```

**Type Conversion**:
```yaml
{{ .Values.port | toString }}           # Convert to string
{{ .Values.replicas | int }}            # Convert to integer
{{ .Values.enabled | ternary "yes" "no" }}  # Conditional value
```

**Encoding**:
```yaml
{{ .Values.config | b64enc }}           # Base64 encode
{{ .Values.secret | b64dec }}           # Base64 decode
{{ .Values.data | toJson }}             # Convert to JSON
{{ .Values.data | toYaml }}             # Convert to YAML
```

**Lists and Dictionaries**:
```yaml
{{ .Values.list | first }}              # First element
{{ .Values.list | rest }}               # All but first
{{ .Values.list | last }}               # Last element
{{ .Values.list | has "item" }}         # Check if contains
{{ .Values.dict | keys }}               # Dictionary keys
{{ .Values.dict | values }}             # Dictionary values
```

**Kubernetes-Specific**:
```yaml
{{ include "mychart.labels" . | nindent 4 }}  # Include named template with indent
{{ .Values.resources | toYaml | nindent 8 }}  # Convert resources to YAML
{{ .Release.Name | trunc 63 | trimSuffix "-" }}  # DNS-safe name (≤63 chars)
```

### Named Templates (Helpers)

**Define in templates/_helpers.tpl**:
```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "mychart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a fully qualified app name.
*/}}
{{- define "mychart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "mychart.labels" -}}
helm.sh/chart: {{ include "mychart.chart" . }}
{{ include "mychart.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "mychart.selectorLabels" -}}
app.kubernetes.io/name: {{ include "mychart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

**Use in templates**:
```yaml
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  selector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
```

---

## Values File Patterns

**values.yaml** provides default configuration values:

```yaml
# Replica configuration
replicaCount: 3

# Image configuration
image:
  repository: myapp
  pullPolicy: IfNotPresent
  tag: ""  # Defaults to .Chart.AppVersion

# Image pull secrets
imagePullSecrets:
  - name: regcred

# Service account
serviceAccount:
  create: true
  annotations: {}
  name: ""

# Pod annotations
podAnnotations: {}

# Pod security context
podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 2000

# Container security context
securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop:
      - ALL

# Service configuration
service:
  type: ClusterIP
  port: 80
  targetPort: 8080

# Ingress configuration
ingress:
  enabled: false
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: example-tls
      hosts:
        - example.com

# Resources
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

# Autoscaling
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
  targetMemoryUtilizationPercentage: 80

# Node selector
nodeSelector: {}

# Tolerations
tolerations: []

# Affinity
affinity: {}

# Persistence
persistence:
  enabled: true
  storageClass: "gp3"
  size: 10Gi
  accessMode: ReadWriteOnce

# Environment variables
env:
  - name: APP_ENV
    value: production
  - name: LOG_LEVEL
    value: info

# ConfigMap data
config:
  database_host: postgres.default.svc.cluster.local
  database_port: "5432"
  cache_ttl: "3600"

# Secrets (base64 encoded)
secrets:
  database_password: ""  # Override at install time
```

**Environment-Specific Overrides**:

```bash
# Development values (values-dev.yaml)
replicaCount: 1
resources:
  limits:
    cpu: 200m
    memory: 256Mi

# Production values (values-prod.yaml)
replicaCount: 5
resources:
  limits:
    cpu: 1000m
    memory: 1Gi
autoscaling:
  enabled: true
  maxReplicas: 20
```

---

## Common Helm Commands

### Chart Creation

```bash
# Create new chart
helm create mychart

# Validate chart structure
helm lint mychart/

# Package chart into archive
helm package mychart/
# Output: mychart-1.0.0.tgz

# Render templates locally (dry-run)
helm template myrelease mychart/
helm template myrelease mychart/ --values values-prod.yaml

# Show computed values
helm show values mychart/
```

### Release Management

```bash
# Install chart
helm install myrelease mychart/
helm install myrelease mychart/ --namespace production --create-namespace

# Install with custom values
helm install myrelease mychart/ --values values-prod.yaml
helm install myrelease mychart/ --set replicaCount=5 --set image.tag=v2.0.0

# Dry-run installation (validate without installing)
helm install myrelease mychart/ --dry-run --debug

# Upgrade release
helm upgrade myrelease mychart/
helm upgrade myrelease mychart/ --values values-prod.yaml --set image.tag=v2.1.0

# Upgrade or install (install if doesn't exist)
helm upgrade --install myrelease mychart/

# Rollback to previous revision
helm rollback myrelease
helm rollback myrelease 3  # Rollback to specific revision

# Uninstall release
helm uninstall myrelease
helm uninstall myrelease --namespace production

# Keep history after uninstall
helm uninstall myrelease --keep-history
```

### Release Information

```bash
# List releases
helm list
helm list --namespace production
helm list --all-namespaces

# Show release status
helm status myrelease

# Show release history
helm history myrelease

# Get release values
helm get values myrelease
helm get values myrelease --revision 3

# Get release manifest
helm get manifest myrelease

# Get all release information
helm get all myrelease
```

### Chart Repository

```bash
# Add repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add stable https://charts.helm.sh/stable

# Update repositories
helm repo update

# Search repositories
helm search repo postgresql
helm search repo bitnami/postgresql --versions

# Show chart information
helm show chart bitnami/postgresql
helm show values bitnami/postgresql
helm show readme bitnami/postgresql
```

### Dependencies

```bash
# Update chart dependencies
helm dependency update mychart/

# List dependencies
helm dependency list mychart/

# Build dependencies (download to charts/ directory)
helm dependency build mychart/
```

---

## Dependency Management

### Declaring Dependencies (Chart.yaml)

```yaml
dependencies:
  # Database dependency
  - name: postgresql
    version: "12.1.0"
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
    tags:
      - database

  # Cache dependency
  - name: redis
    version: "17.3.0"
    repository: https://charts.bitnami.com/bitnami
    condition: redis.enabled
    tags:
      - cache

  # Local chart dependency
  - name: common
    version: "1.0.0"
    repository: file://../common
```

### Managing Dependency Values

**Parent chart values.yaml**:
```yaml
# Configure postgresql subchart
postgresql:
  enabled: true
  auth:
    username: myapp
    password: changeme
    database: myapp_production
  primary:
    persistence:
      enabled: true
      size: 20Gi

# Configure redis subchart
redis:
  enabled: true
  auth:
    enabled: false
  master:
    persistence:
      enabled: false
```

### Conditional Dependencies

```yaml
# Enable/disable dependencies
helm install myrelease mychart/ \
  --set postgresql.enabled=true \
  --set redis.enabled=false

# Using tags
helm install myrelease mychart/ \
  --set tags.database=true \
  --set tags.cache=false
```

### Import Values from Dependencies

**Chart.yaml**:
```yaml
dependencies:
  - name: postgresql
    version: "12.1.0"
    repository: https://charts.bitnami.com/bitnami
    import-values:
      - child: auth.password
        parent: dbPassword
```

**Access in templates**:
```yaml
env:
  - name: DB_PASSWORD
    value: {{ .Values.dbPassword }}
```

---

## Release Lifecycle

### Installation Workflow

```bash
# 1. Dry-run to validate
helm install myrelease mychart/ --dry-run --debug

# 2. Install to staging
helm install myrelease mychart/ \
  --namespace staging \
  --create-namespace \
  --values values-staging.yaml

# 3. Verify installation
helm status myrelease --namespace staging
kubectl get pods --namespace staging

# 4. Promote to production
helm install myrelease mychart/ \
  --namespace production \
  --create-namespace \
  --values values-prod.yaml
```

### Upgrade Workflow

```bash
# 1. Check current values
helm get values myrelease --namespace production

# 2. Dry-run upgrade
helm upgrade myrelease mychart/ \
  --namespace production \
  --values values-prod.yaml \
  --set image.tag=v2.1.0 \
  --dry-run --debug

# 3. Perform upgrade
helm upgrade myrelease mychart/ \
  --namespace production \
  --values values-prod.yaml \
  --set image.tag=v2.1.0

# 4. Monitor rollout
kubectl rollout status deployment/myrelease-webapp --namespace production

# 5. Verify upgrade
helm status myrelease --namespace production
```

### Rollback Workflow

```bash
# 1. Check release history
helm history myrelease --namespace production

# 2. Rollback to previous version
helm rollback myrelease --namespace production

# 3. Rollback to specific revision
helm rollback myrelease 3 --namespace production

# 4. Verify rollback
helm status myrelease --namespace production
kubectl rollout status deployment/myrelease-webapp --namespace production
```

### Cleanup

```bash
# Uninstall release (removes all resources)
helm uninstall myrelease --namespace production

# Keep history (allows rollback after uninstall)
helm uninstall myrelease --namespace production --keep-history

# Delete namespace
kubectl delete namespace production
```

---

## Testing with Helm

### Lint Validation

```bash
# Lint chart for issues
helm lint mychart/

# Lint with custom values
helm lint mychart/ --values values-prod.yaml

# Strict linting (fail on warnings)
helm lint mychart/ --strict
```

**Common lint issues**:
- Chart.yaml missing required fields
- Invalid YAML syntax in templates
- Missing `{{ required }}` for critical values
- Chart version not following SemVer

### Template Validation

```bash
# Render templates locally
helm template myrelease mychart/

# Render with custom values
helm template myrelease mychart/ --values values-prod.yaml

# Debug template rendering
helm template myrelease mychart/ --debug

# Validate against Kubernetes API
helm template myrelease mychart/ | kubectl apply --dry-run=client -f -
```

### Helm Tests

**Create test pod (templates/tests/test-connection.yaml)**:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "mychart.fullname" . }}-test-connection"
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": test  # Mark as test hook
spec:
  containers:
    - name: wget
      image: busybox
      command: ['wget']
      args: ['{{ include "mychart.fullname" . }}:{{ .Values.service.port }}']
  restartPolicy: Never
```

**Run tests**:
```bash
# Run all tests for release
helm test myrelease --namespace production

# Show test logs
helm test myrelease --namespace production --logs

# Cleanup test pods after run
kubectl delete pod -l 'helm.sh/hook=test' --namespace production
```

---

## Security Best Practices

### 1. Image Security

```yaml
# Pin specific image versions (avoid :latest)
image:
  repository: myapp
  tag: "v2.1.0"  # Explicit version
  pullPolicy: IfNotPresent

# Use SHA256 digests for immutability
image:
  repository: myapp
  digest: "sha256:abc123..."  # Immutable image
```

### 2. RBAC Configuration

```yaml
# Create minimal service account
serviceAccount:
  create: true
  annotations:
    # AWS IRSA example
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/my-app-role
  name: ""

# Define RBAC role (templates/role.yaml)
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: {{ include "mychart.fullname" . }}
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list"]
```

### 3. Pod Security

```yaml
# Pod security context
podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 2000
  seccompProfile:
    type: RuntimeDefault

# Container security context
securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop:
      - ALL
  runAsNonRoot: true
  runAsUser: 1000
```

### 4. Secrets Management

```yaml
# Use Kubernetes Secrets (not ConfigMaps)
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "mychart.fullname" . }}
type: Opaque
data:
  # Base64 encoded values
  database-password: {{ .Values.secrets.databasePassword | b64enc | quote }}

# Reference secrets in pods
env:
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: {{ include "mychart.fullname" . }}
        key: database-password
```

**External Secrets Integration**:
```yaml
# Use External Secrets Operator
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: {{ include "mychart.fullname" . }}
spec:
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: {{ include "mychart.fullname" . }}-secrets
  data:
    - secretKey: database-password
      remoteRef:
        key: /prod/myapp/db-password
```

### 5. Network Policies

```yaml
# Restrict pod network access
{{- if .Values.networkPolicy.enabled }}
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: {{ include "mychart.fullname" . }}
spec:
  podSelector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
      - podSelector:
          matchLabels:
            app: frontend
      ports:
        - protocol: TCP
          port: {{ .Values.service.targetPort }}
  egress:
    - to:
      - podSelector:
          matchLabels:
            app: database
      ports:
        - protocol: TCP
          port: 5432
{{- end }}
```

### 6. Resource Limits

```yaml
# Always set resource limits
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi
```

### 7. Required Values Validation

```yaml
# Force required values at install time
{{- if not .Values.secrets.databasePassword }}
{{- fail "secrets.databasePassword is required" }}
{{- end }}

# Or use required function
database:
  password: {{ required "Database password required" .Values.secrets.databasePassword }}
```

---

## Quick Examples

### Minimal Web Application Chart

**Chart.yaml**:
```yaml
apiVersion: v2
name: webapp
version: 1.0.0
appVersion: "1.0"
description: Simple web application
```

**values.yaml**:
```yaml
replicaCount: 2
image:
  repository: nginx
  tag: "1.21"
service:
  port: 80
```

**templates/deployment.yaml**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Release.Name }}
  template:
    metadata:
      labels:
        app: {{ .Release.Name }}
    spec:
      containers:
      - name: webapp
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        ports:
        - containerPort: 80
```

**templates/service.yaml**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}
spec:
  type: ClusterIP
  ports:
  - port: {{ .Values.service.port }}
    targetPort: 80
  selector:
    app: {{ .Release.Name }}
```

**Install**:
```bash
helm install myapp webapp/
```

---

## Next Steps

**For Advanced Patterns**:
- See **REFERENCE.md** for comprehensive guide with 10+ production examples
- Covers: Hooks, CI/CD integration, OCI registries, testing strategies

**Common Use Cases**:
- Multi-environment deployments → REFERENCE.md § CI/CD Integration
- Chart testing → REFERENCE.md § Testing Strategies
- Complex dependencies → REFERENCE.md § Dependencies Deep Dive
- Production patterns → REFERENCE.md § Production Examples

---

**Progressive Disclosure**: Start here for quick reference, load REFERENCE.md for comprehensive patterns and production examples.

**Performance Target**: <100ms skill loading (this file ~75KB)

**Last Updated**: 2025-10-23 | **Version**: 1.0.0
