---
name: k8s-helm
description: "Use when modifying Helm charts (Chart.yaml, templates/*.tpl, values*.yaml) to enforce chart structure, values override hierarchy, helper template patterns. Skip when kustomize is the deployment tool."
version: 1.0.0
license: MIT
applies_when:
  files_present:
    - "**/Chart.yaml"
    - "**/values*.yaml"
    - "**/templates/*.tpl"
    - "**/templates/*.yaml"
  files_contain:
    "**/Chart.yaml": '^apiVersion:\s*v[12]'
  frameworks:
    - helm
  exclude_when:
    files_present:
      - "**/kustomization.yaml"
portability:
  level: universal
  tested_on:
    - claude-code
    - codex
  model_dependency: none
  domain_specificity: focused
produces:
  - helm-chart
consumes:
  - k8s-manifest
  - service-boundary
security:
  signature: ""
  sandbox: read-only
  network: none
---

# Helm Best Practices

Helm chart 개발 패턴 및 best practices.

## Chart Structure

```
charts/myapp/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default values
├── values-dev.yaml     # Dev overrides
├── values-prod.yaml    # Prod overrides
├── templates/
│   ├── _helpers.tpl    # Template helpers
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── ingress.yaml
│   └── NOTES.txt       # Post-install notes
└── README.md
```

## Chart.yaml

```yaml
apiVersion: v2
name: myapp
description: A Helm chart for MyApp
type: application
version: 0.1.0        # Chart version (SemVer)
appVersion: "1.2.3"   # Application version
```

## values.yaml Template

```yaml
# Image configuration
image:
  repository: myregistry/myapp
  tag: "v1.2.3"
  pullPolicy: IfNotPresent

# Resource limits
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "256Mi"
    cpu: "250m"

# Replica count
replicaCount: 2

# Service configuration
service:
  type: ClusterIP
  port: 80

# Ingress configuration
ingress:
  enabled: false
  className: nginx
  hosts: []

# Security context
podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000

securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop:
      - ALL

# Probes
livenessProbe:
  httpGet:
    path: /healthz
    port: http
  initialDelaySeconds: 15
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: http
  initialDelaySeconds: 5
  periodSeconds: 5
```

## Template Helpers (_helpers.tpl)

```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "myapp.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "myapp.fullname" -}}
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
{{- define "myapp.labels" -}}
helm.sh/chart: {{ include "myapp.chart" . }}
{{ include "myapp.selectorLabels" . }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
```

## Deployment Template

```yaml
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
    metadata:
      labels:
        {{- include "myapp.selectorLabels" . | nindent 8 }}
    spec:
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        securityContext:
          {{- toYaml .Values.securityContext | nindent 12 }}
        resources:
          {{- toYaml .Values.resources | nindent 12 }}
        {{- with .Values.livenessProbe }}
        livenessProbe:
          {{- toYaml . | nindent 12 }}
        {{- end }}
```

## Library Chart 패턴

### Library vs Application Chart

```yaml
# Library Chart: type: library (직접 설치 불가, 공통 템플릿 제공)
# charts/common-lib/Chart.yaml
apiVersion: v2
name: common-lib
type: library          # ← 핵심 차이
version: 0.1.0

# Application Chart: type: application (기본값, 설치 가능)
# charts/example-server/Chart.yaml
apiVersion: v2
name: example-server
type: application
dependencies:
  - name: common-lib
    version: "0.1.x"
    repository: "file://../common-lib"   # 로컬 참조
```

### 공통 템플릿 정의 → include 호출

```yaml
# Library Chart: charts/common-lib/templates/_deployment.tpl
{{- define "common-lib.deployment" -}}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "common-lib.fullname" . }}
  labels: {{- include "common-lib.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels: {{- include "common-lib.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels: {{- include "common-lib.selectorLabels" . | nindent 8 }}
    spec:
      serviceAccountName: {{ include "common-lib.serviceAccountName" . }}
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        {{- with .Values.resources }}
        resources: {{- toYaml . | nindent 10 }}
        {{- end }}
{{- end }}

# Application Chart: charts/example-server/templates/deployment.yaml
{{- include "common-lib.deployment" . }}
```

### MSA 확장 구조

```
charts/
├── common-lib/           # Library Chart (공통 템플릿)
│   ├── Chart.yaml         # type: library
│   └── templates/
│       ├── _deployment.tpl
│       ├── _service.tpl
│       ├── _gateway.tpl
│       ├── _serviceaccount.tpl
│       ├── _hpa.tpl
│       └── _pdb.tpl
├── example-server/           # Application Chart
│   ├── Chart.yaml         # depends on common-lib
│   ├── values.yaml
│   └── templates/
│       └── deployment.yaml  # {{ include "common-lib.deployment" . }}
└── example-payment/          # 새 서비스도 같은 Library Chart 활용
    ├── Chart.yaml
    └── ...
```

---

## ArgoCD 환경에서 Helm의 역할

### 역할 분리

```
ArgoCD가 하는 것:
  1. helm template → 매니페스트 렌더링
  2. kubectl apply  → 클러스터에 적용
  3. 릴리즈 관리 (Sync, Rollback, Health)

Helm이 하는 것:
  1. 템플릿 엔진 (Go template)
  2. 패키징 (Chart archive)
  3. 의존성 관리 (Chart.yaml dependencies)

ArgoCD가 하지 않는 것:
  ✗ helm install / helm upgrade  ← 직접 실행 안 함
  ✗ Helm Release 객체 생성       ← Tiller/Secret 기반 릴리즈 없음
  ✗ Helm Hook 트리거             ← ArgoCD Hook으로 교체 필수
```

### Helm Hook → ArgoCD Hook 교체

ArgoCD는 `helm template`만 실행하므로 `helm.sh/hook`은 무시됨.
반드시 `argocd.argoproj.io/hook`으로 교체. 상세: `/gitops-argocd-helm`

---

## values.schema.json

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["image", "replicaCount"],
  "properties": {
    "image": {
      "type": "object",
      "required": ["repository", "tag"],
      "properties": {
        "repository": { "type": "string" },
        "tag": { "type": "string", "pattern": "^v?[0-9]" }
      }
    },
    "replicaCount": { "type": "integer", "minimum": 1 }
  }
}
```

- `helm lint` 시 자동 검증, CI에서 `helm lint --strict` 활용
- 필수 값 누락 즉시 감지, 잘못된 타입(문자열 대신 숫자 등) 방지

---

## YAML Anchor / Alias

Kind, ArgoCD, Helm values 모두 표준 Go YAML 파서 사용 → anchor/alias **정상 지원**.

```yaml
# Kind 클러스터 설정 예시: 이미지 반복 제거
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
    image: &nodeImage kindest/node:v1.32.0   # anchor 정의
  - role: worker
    image: *nodeImage                         # alias 참조
  - role: worker
    image: *nodeImage

# Helm values: 공통 설정 재사용
defaults: &defaults
  resources:
    requests: { cpu: "100m", memory: "128Mi" }
    limits: { cpu: "200m", memory: "256Mi" }

server:
  <<: *defaults           # merge key로 defaults 병합
  replicaCount: 2

worker:
  <<: *defaults
  replicaCount: 4
```

---

## 멀티 환경 Values 관리

### 디렉토리 기반 구조

```
environments/
├── dev/
│   ├── example-server/values.yaml    # dev 전용 override
│   └── monitoring/values.yaml
├── staging/
│   └── example-server/values.yaml
└── prod/
    └── example-server/values.yaml

charts/
└── example-server/
    └── values.yaml                # 기본값 (모든 환경 공통)
```

### ApplicationSet + Multi-source `$values/` 패턴

```yaml
sources:
  - repoURL: https://github.com/myorg/k8s-config.git
    chart: example-server
    targetRevision: "1.0.0"
    helm:
      valueFiles:
        - $values/environments/dev/example-server/values.yaml
  - repoURL: https://github.com/myorg/k8s-config.git
    targetRevision: main
    ref: values                   # $values로 참조
```

### 원칙
- **기본값**은 `charts/{service}/values.yaml`에 정의
- **환경별 override**만 `environments/{env}/{service}/values.yaml`에 작성
- 기본값을 환경별 파일에 중복 정의하지 않음 (override만)

---

## Validation Commands

```bash
# Lint chart (schema 포함)
helm lint charts/myapp/ --strict

# Template rendering
helm template myapp charts/myapp/ -f values-prod.yaml

# Dry run install
helm install myapp charts/myapp/ --dry-run --debug

# Validate with kubeval
helm template myapp charts/myapp/ | kubeval
```

## Anti-patterns

| Mistake | Correct | Why |
|---------|---------|-----|
| Hardcoded values in templates | Use values.yaml | Configurability |
| No default values | Provide sensible defaults | Usability |
| Long template names | Use _helpers.tpl | DRY principle |
| Missing NOTES.txt | Add post-install info | User guidance |
| No resource limits | Always set limits | Cluster stability |
| ArgoCD 환경에서 `helm upgrade` 직접 실행 | ArgoCD Sync 사용 | 릴리즈 상태 충돌, drift 발생 |
| "YAML anchor 미지원" 확인 없이 단정 | 공식 문서 확인 후 판단 | Go YAML 파서는 anchor/alias 지원 |
| 환경별 values에 기본값 중복 정의 | override만 작성 | 변경 시 동기화 누락 위험 |

**관련 skill**: `/docker`, `/k8s-security`, `/gitops-argocd-helm`
