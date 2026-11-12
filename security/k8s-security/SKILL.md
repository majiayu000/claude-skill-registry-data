---
name: k8s-security
description: "Kubernetes 보안 — Pod Security Standards, NetworkPolicy, RBAC, Secrets 관리, Kyverno 정책, Trivy 스캔, AppProject 최소 권한. Use when 클러스터와 워크로드의 보안 설정을 점검하거나 강화할 때."
---

# Kubernetes Security Patterns

Kubernetes 보안 패턴 및 best practices.

## Quick Reference

```
K8s 보안 적용 순서
    │
    ├─ Pod Security ───> runAsNonRoot + readOnlyRootFilesystem
    │
    ├─ Namespace ─────> PSS labels (enforce: restricted)
    │
    ├─ Network ───────> Default Deny + 허용 정책
    │
    ├─ RBAC ──────────> 최소 권한 Role + Custom SA
    │
    └─ Secrets ───────> Volume mount (env 지양)
```

---

## Pod Security Standards

### Restricted SecurityContext

```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
  containers:
  - name: app
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
          - ALL
```

### Namespace PSS Labels

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

## Network Policy

### Default Deny All

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### Allow Specific Traffic

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
```

## RBAC

### Minimal Role

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-role
  namespace: production
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list"]
  resourceNames: ["app-config", "app-secrets"]  # Specific resources only
```

### RBAC `create` verb + `resourceNames` 제약

K8s API 제약: `create` verb는 아직 존재하지 않는 리소스 대상 → `resourceNames` 매칭 불가 (무시됨).

```yaml
# ❌ 잘못된 예: create에 resourceNames 적용 → 무시됨 (사실상 전체 create 허용)
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["create", "get", "delete"]
  resourceNames: ["ecr-pull-secret"]

# ✅ 올바른 예: create는 별도 rule (resourceNames 없이), get/delete만 resourceNames 적용
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["create"]                              # resourceNames 없음
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "delete"]
  resourceNames: ["ecr-pull-secret"]             # 특정 리소스만
```

**영향받는 verb**: `create`, `deletecollection` — 리소스가 아직 없으므로 이름 매칭 불가
**부분적**: `list`, `watch` — collection 작업이라 `resourceNames` 적용이 제한적

### ServiceAccount

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-sa
  namespace: production
automountServiceAccountToken: false  # Disable unless needed
---
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: app-sa
  automountServiceAccountToken: false
```

## Secrets Management

```yaml
# Mount as file (preferred)
spec:
  volumes:
  - name: secrets
    secret:
      secretName: app-secrets
  containers:
  - name: app
    volumeMounts:
    - name: secrets
      mountPath: /etc/secrets
      readOnly: true

# NOT recommended: environment variable
env:
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: db-secrets
      key: password
```

## Security Checklist

| Category | Check | Required |
|----------|-------|----------|
| Container | runAsNonRoot: true | Yes |
| Container | allowPrivilegeEscalation: false | Yes |
| Container | readOnlyRootFilesystem: true | Yes |
| Container | capabilities.drop: ALL | Yes |
| Image | No :latest tag | Yes |
| Image | Trusted registry only | Yes |
| Network | NetworkPolicy defined | Yes |
| RBAC | Custom ServiceAccount | Yes |
| RBAC | Minimal permissions | Yes |
| Secrets | Volume mount, not env | Recommended |

## 2026 트렌드: 추가 보안 레이어

### ValidatingAdmissionPolicy (K8s 1.30+)

PSS를 보완하는 CEL 기반 정책

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicy
metadata:
  name: require-labels
spec:
  failurePolicy: Fail
  matchConstraints:
    resourceRules:
    - apiGroups: ["apps"]
      resources: ["deployments"]
      operations: ["CREATE", "UPDATE"]
  validations:
  - expression: "has(object.metadata.labels.app)"
    message: "deployment must have 'app' label"
```

### Zero Trust / mTLS

```yaml
# Istio/Linkerd로 서비스 간 mTLS 적용
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT
```

**추가 도구**:
- Kyverno: 정책 관리 (PSS 확장)
- Falco: 런타임 위협 탐지

---

## AppProject 최소 권한 원칙

ArgoCD AppProject에서 와일드카드 남용은 최소 권한 원칙 위반.

### `namespaceResourceWhitelist` 검증

```yaml
# ❌ 2개 이상 API 그룹에서 kind: "*" → 전체적 최소 권한 위반
namespaceResourceWhitelist:
  - group: '*'
    kind: '*'         # 모든 그룹의 모든 리소스 허용

# ✅ 필요한 리소스 종류를 명시적으로 나열
namespaceResourceWhitelist:
  - group: ''
    kind: ConfigMap
  - group: ''
    kind: Secret
  - group: ''
    kind: Service
  - group: apps
    kind: Deployment
  - group: apps
    kind: StatefulSet
  - group: networking.k8s.io
    kind: Ingress
```

### `clusterResourceWhitelist`에서 `kind: "*"` 특히 위험

```yaml
# ❌ 클러스터 전체 리소스 생성 가능 → RBAC, Namespace 삭제까지 허용
clusterResourceWhitelist:
  - group: '*'
    kind: '*'

# ✅ 필요한 클러스터 리소스만 허용
clusterResourceWhitelist:
  - group: ''
    kind: Namespace
  - group: networking.k8s.io
    kind: IngressClass
```

### `sourceRepos` / `destinations` 범위 제한

```yaml
# ❌ 모든 소스 허용
sourceRepos: ['*']

# ✅ 조직/팀 prefix로 제한
sourceRepos:
  - 'https://github.com/my-org/*'
  - 'https://charts.helm.sh/*'

# ❌ 모든 네임스페이스 허용
destinations:
  - namespace: '*'

# ✅ 팀 패턴으로 제한
destinations:
  - namespace: '{team}-*'
    server: https://kubernetes.default.svc
```

---

## kubectl Secret 특수문자 처리

### `$` 문자 shell escaping 문제

```bash
# ❌ 큰따옴표: $HOME이 쉘 변수로 치환됨
kubectl create secret generic my-secret \
  --from-literal=password="Pa$$w0rd!$HOME"
# 실제 저장값: Pa$w0rd!/Users/ress  ← $$ → $, $HOME → 실제 경로

# ✅ 작은따옴표: 리터럴 문자열 보존
kubectl create secret generic my-secret \
  --from-literal=password='Pa$$w0rd!$HOME'
# 실제 저장값: Pa$$w0rd!$HOME  ← 의도한 값

# ✅ --from-file: 특수문자 걱정 없음
echo -n 'Pa$$w0rd!$HOME' > /tmp/password.txt
kubectl create secret generic my-secret --from-file=password=/tmp/password.txt
rm /tmp/password.txt
```

### Secret 등록 후 검증 (필수)

```bash
# 실제 저장된 값 확인
kubectl get secret my-secret -o jsonpath='{.data.password}' | base64 -d
```

---

## Anti-patterns

| Mistake | Correct | Why |
|---------|---------|-----|
| `privileged: true` | Never use | Full host access |
| `hostNetwork: true` | Pod network | Host network exposure |
| No NetworkPolicy | Default deny | Unrestricted traffic |
| Default ServiceAccount | Custom SA | Minimal permissions |
| ClusterRole for app | Role (namespaced) | Scope limitation |
| PSS만 의존 | + ValidatingAdmissionPolicy | 세부 정책 필요 |
| `create` verb에 `resourceNames` 적용 | create는 별도 rule | K8s API가 무시함 |
| AppProject `kind: "*"` 와일드카드 남용 | 필요 리소스 명시적 나열 | 최소 권한 원칙 위반 |
| kubectl secret 값을 큰따옴표로 감싸기 | 작은따옴표 또는 --from-file | `$` 등 특수문자 쉘 치환 위험 |

---

## Kyverno (Policy as Code)

### 설치

```bash
helm repo add kyverno https://kyverno.github.io/kyverno/
helm install kyverno kyverno/kyverno -n kyverno --create-namespace
```

### 핵심 정책 예제

```yaml
# 1. 이미지 레지스트리 제한
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: restrict-image-registries
spec:
  validationFailureAction: Enforce
  rules:
    - name: validate-registries
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "이미지는 허용된 레지스트리에서만 가져올 수 있습니다"
        pattern:
          spec:
            containers:
              - image: "ghcr.io/* | gcr.io/* | *.dkr.ecr.*.amazonaws.com/*"
---
# 2. 리소스 제한 필수
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-resources
spec:
  validationFailureAction: Enforce
  rules:
    - name: require-limits
      match:
        any:
          - resources:
              kinds:
                - Pod
      validate:
        message: "CPU/메모리 limits 설정이 필요합니다"
        pattern:
          spec:
            containers:
              - resources:
                  limits:
                    memory: "?*"
                    cpu: "?*"
---
# 3. 필수 라벨 강제
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-labels
spec:
  validationFailureAction: Enforce
  rules:
    - name: require-team-label
      match:
        any:
          - resources:
              kinds:
                - Deployment
      validate:
        message: "team, app 라벨이 필요합니다"
        pattern:
          metadata:
            labels:
              team: "?*"
              app: "?*"
```

### Kyverno CLI (CI 검증)

```bash
# 정책 테스트
kyverno apply ./policies/ --resource ./k8s/deployment.yaml

# 결과 출력
kyverno apply ./policies/ -r ./k8s/ -o json
```

---

## Trivy (취약점 스캔)

### 이미지 스캔

```bash
# 기본 스캔
trivy image myapp:latest

# CRITICAL/HIGH만 검출, 실패 시 exit code 1
trivy image --severity CRITICAL,HIGH --exit-code 1 myapp:latest

# SBOM 생성
trivy image --format spdx-json -o sbom.json myapp:latest
```

### Kubernetes Operator

```bash
# Trivy Operator 설치
helm repo add aqua https://aquasecurity.github.io/helm-charts/
helm install trivy-operator aqua/trivy-operator \
  --namespace trivy-system \
  --create-namespace

# VulnerabilityReport 조회
kubectl get vulnerabilityreports -A
```

### CI/CD 통합 (GitHub Actions)

```yaml
- name: Trivy Scan
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ${{ env.IMAGE }}
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'CRITICAL,HIGH'
    exit-code: '1'
```

상세한 CI/CD 보안 통합은 `/cicd:cicd-devsecops` 스킬 참조

**관련 skill**: `/k8s:k8s-helm`, `/infra:docker`, `/cicd:cicd-devsecops`
