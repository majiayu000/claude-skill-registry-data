---
name: gitops-argocd
description: "ArgoCD 기본 — GitOps 원칙, 설치, Application 정의, App of Apps, CLI, bootstrap sync-wave. Use when ArgoCD 를 처음 도입하거나 Application 을 정의할 때."
---

# GitOps & ArgoCD 가이드

ArgoCD를 활용한 선언적 GitOps 배포 및 App of Apps 패턴

## Quick Reference (결정 트리)

```
GitOps 도구 선택?
    │
    ├─ 단일 클러스터 ────────> ArgoCD (추천)
    ├─ 멀티 클러스터 ────────> ArgoCD + ApplicationSet
    ├─ 파이프라인 통합 ──────> ArgoCD + Tekton
    └─ Flux 생태계 ─────────> Flux CD

매니페스트 관리?
    │
    ├─ 단순한 앱 ──────> Kustomize
    ├─ 복잡한 앱 ──────> Helm Chart
    └─ 멀티 환경 ──────> Kustomize + Helm
        │
        └─ App of Apps ──> 조직 전체 관리
```

---

## CRITICAL: GitOps 원칙

```
┌─────────────────────────────────────────────────────────────┐
│                    GitOps Workflow                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Git Repository (Single Source of Truth)                     │
│       │                                                      │
│       ▼                                                      │
│  ArgoCD (Reconciliation Loop)                                │
│       │                                                      │
│       ├─ Sync: Git → K8s                                    │
│       ├─ Diff: Git ↔ K8s                                    │
│       └─ Health: K8s 상태 모니터링                           │
│       │                                                      │
│       ▼                                                      │
│  Kubernetes Cluster                                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**핵심 원칙**:
| 원칙 | 설명 |
|------|------|
| **선언적** | 원하는 상태를 Git에 선언 |
| **버전 관리** | 모든 변경은 Git 커밋 |
| **자동 적용** | Git 변경 → 자동 배포 |
| **자가 치유** | Drift 감지 → 자동 복구 |

---

## ArgoCD 설치

### Helm 설치

```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

helm install argocd argo/argo-cd \
  --namespace argocd \
  --create-namespace \
  --set server.service.type=LoadBalancer \
  --set configs.params."server\.insecure"=true
```

### 초기 설정

```bash
# 초기 admin 비밀번호
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d

# CLI 로그인
argocd login <ARGOCD_SERVER>

# 비밀번호 변경
argocd account update-password
```

---

## Application 정의

### 기본 Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io  # 삭제 시 리소스도 삭제
spec:
  project: default

  source:
    repoURL: https://github.com/myorg/my-app.git
    targetRevision: main  # 브랜치, 태그, 또는 커밋 SHA
    path: k8s/overlays/prod

  destination:
    server: https://kubernetes.default.svc
    namespace: my-app

  syncPolicy:
    automated:
      prune: true      # 삭제된 리소스 정리
      selfHeal: true   # Drift 자동 복구
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### Helm Chart Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: nginx-ingress
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://kubernetes.github.io/ingress-nginx
    chart: ingress-nginx
    targetRevision: 4.8.3
    helm:
      releaseName: nginx-ingress
      values: |
        controller:
          replicaCount: 2
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
      valueFiles:
        - values-prod.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: ingress-nginx
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Kustomize Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app-prod
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/my-app.git
    targetRevision: main
    path: k8s/overlays/prod
    kustomize:
      images:
        - myapp=ghcr.io/myorg/myapp:v1.2.3
      namePrefix: prod-
      commonLabels:
        env: production
  destination:
    server: https://kubernetes.default.svc
    namespace: my-app-prod
```

---

## App of Apps 패턴

### CRITICAL: 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                    App of Apps Pattern                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  root-app (ArgoCD Application)                               │
│       │                                                      │
│       ├── apps/                                              │
│       │   ├── app-a.yaml ──> Application A                  │
│       │   ├── app-b.yaml ──> Application B                  │
│       │   └── app-c.yaml ──> Application C                  │
│       │                                                      │
│       └── infra/                                             │
│           ├── cert-manager.yaml                              │
│           ├── ingress.yaml                                   │
│           └── monitoring.yaml                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Root Application

```yaml
# apps/root-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: root-app
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/gitops-config.git
    targetRevision: main
    path: apps  # Application 매니페스트가 있는 폴더
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Child Applications

```yaml
# apps/app-a.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: app-a
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/app-a.git
    targetRevision: v1.0.0  # 고정 버전 권장
    path: k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: app-a
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

### 폴더 구조 (권장)

```
gitops-config/
├── apps/
│   ├── root-app.yaml        # Root application
│   ├── app-a.yaml           # 비즈니스 앱
│   ├── app-b.yaml
│   └── app-c.yaml
├── infra/
│   ├── cert-manager.yaml    # 인프라 컴포넌트
│   ├── ingress-nginx.yaml
│   ├── monitoring.yaml
│   └── sealed-secrets.yaml
└── clusters/
    ├── dev/
    │   └── values.yaml
    ├── staging/
    │   └── values.yaml
    └── prod/
        └── values.yaml
```

---

## CLI 명령어

```bash
# 애플리케이션 목록
argocd app list

# 상태 확인
argocd app get my-app

# 수동 Sync
argocd app sync my-app

# Sync 상태 대기
argocd app wait my-app

# 롤백
argocd app rollback my-app <revision>

# Diff 확인
argocd app diff my-app
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 소스/설정 같은 저장소 | 무한 Sync 루프 | 설정 저장소 분리 |
| HEAD/main 직접 참조 | 예측 불가 배포 | 태그/커밋 SHA 사용 (아래 상세) |
| selfHeal 없음 | Drift 방치 | selfHeal: true |
| 시크릿 평문 커밋 | 보안 취약 | Sealed Secrets |
| 단일 root-app | SPOF | 계층화된 App of Apps |

### `targetRevision: main` 위험성

```yaml
# ❌ prod: 누군가 main에 push하면 즉시 프로덕션 배포
targetRevision: main

# ✅ prod: 태그 또는 커밋 SHA 고정
targetRevision: v1.2.3
targetRevision: a1b2c3d4e5f6

# ⚠️ dev 환경에서 main 허용 시: 반드시 주석으로 사유 명시
targetRevision: main    # dev only: auto-sync from main for rapid iteration
```

**구체적 위험 시나리오**:
- 실수로 main에 직접 push → auto-sync가 즉시 프로덕션 반영
- 여러 PR이 연속 머지 → 중간 상태가 일시적으로 배포
- 롤백 시 "어떤 커밋이 배포되어 있었는지" 추적 불가

**규칙**: prod/staging은 태그/SHA **필수**. dev에서 `main` 사용 시 주석 사유 명시.

---

## Bootstrap Sync-Wave 패턴

클러스터 부트스트랩 시 리소스 생성 순서를 보장하는 패턴.

### Sync-Wave 번호 체계

```
Wave -5: Namespaces (다른 모든 리소스의 전제 조건)
Wave -3: CRDs (Operator가 인식할 커스텀 리소스 정의)
Wave -2: Operators + ExternalSecrets (CRD 기반 컨트롤러)
Wave -1: Gateways, Config (서비스 진입점)
Wave  0: Applications (실제 워크로드)
```

### 예제: Istio + 모니터링 부트스트랩

```yaml
# Root Application이 관리하는 child Application들
# Wave -3: Istio Base (CRDs)
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: istio-base
  annotations:
    argocd.argoproj.io/sync-wave: "-3"
spec:
  source:
    chart: base
    repoURL: https://istio-release.storage.googleapis.com/charts
    targetRevision: 1.24.3

---
# Wave -2: Istiod (컨트롤 플레인, CRD 필요)
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: istiod
  annotations:
    argocd.argoproj.io/sync-wave: "-2"

---
# Wave -1: Istio Gateway (istiod 필요)
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: istio-gateway
  annotations:
    argocd.argoproj.io/sync-wave: "-1"

---
# Wave 0: 앱 워크로드 (모든 인프라 준비 완료 후)
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: example-server
  annotations:
    argocd.argoproj.io/sync-wave: "0"
```

### Root → Child 순서 보장

Root Application의 `syncPolicy`에서 child Application의 `sync-wave` 순서대로 생성.
각 wave의 리소스가 Healthy 상태가 되어야 다음 wave로 진행.

---

## 체크리스트

### 초기 설정
- [ ] ArgoCD 설치
- [ ] 저장소 연결 (SSH/HTTPS)
- [ ] AppProject 생성

### Application
- [ ] 적절한 targetRevision (태그/SHA)
- [ ] syncPolicy 설정 (automated, prune, selfHeal)
- [ ] finalizers 설정

### App of Apps
- [ ] Root Application 생성
- [ ] 폴더 구조 설계
- [ ] ApplicationSet 고려 (멀티 환경)

---

**참조 스킬**: `/cicd:gitops-argocd-advanced` (ApplicationSet, Sync 전략, 시크릿), `/cicd:gitops-argocd-ai` (AI-assisted GitOps, Spacelift Intent, 예측적 배포), `/cicd:cicd-devsecops`, `/cicd:deployment-strategies`, `/observability:aiops`
