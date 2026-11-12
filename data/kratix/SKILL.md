---
name: kratix
description: "Kratix 플랫폼 오케스트레이터 — Promise CRD 작성, PostgreSQL·Redis as-a-Service 예제, Backstage 연동, 소규모 팀 적용 판단. Use when Promise 로 셀프서비스 플랫폼 API 를 만들지 판단하거나 Kratix 를 도입할 때."
---

# Kratix 플랫폼 오케스트레이터 가이드

Kratix Promise 기반 셀프서비스 플랫폼 API, Backstage 연동, 소규모~대규모 팀 적용 전략

## Quick Reference (결정 트리)

```
Kratix 도입 여부 판단?
    │
    ├─ 팀 규모 확인
    │   ├─ 1-3명 ──────────> 도입 비추천 (Helm + Kustomize로 충분)
    │   ├─ 3-5명 ──────────> 조건부 추천 (아래 "소규모 적용" 섹션 참고)
    │   ├─ 5-15명 ─────────> 적극 추천 (셀프서비스 가치 발생)
    │   └─ 15명+ ──────────> 필수 (플랫폼 팀 + 앱 팀 분리 시)
    │
    ├─ 인프라 복잡도
    │   ├─ 단일 앱, 단일 환경 ──> Kratix 불필요 (오버엔지니어링)
    │   ├─ 다수 앱, 2-3 환경 ───> 검토 가치 있음
    │   └─ 다수 앱, 멀티클러스터 ─> Kratix 강력 추천
    │
    └─ 핵심 질문
        ├─ "개발자가 인프라 요청을 티켓으로 하나?" ──> Yes: Kratix 도입 검토
        ├─ "동일 리소스를 반복 프로비저닝하나?" ────> Yes: Promise 패턴 적합
        └─ "플랫폼 API를 표준화하고 싶은가?" ──────> Yes: Kratix 핵심 가치
```

---

## 소규모 프로젝트 적용 가능성 (CRITICAL)

### 솔직한 평가: Kratix는 소규모 팀에 과한가?

**결론부터: 3-5명 팀에서는 대부분의 경우 오버엔지니어링이다.**

Kratix는 "플랫폼 팀이 앱 팀에게 셀프서비스를 제공하는" 시나리오에 최적화되어 있다. 팀이 3-5명이면 플랫폼 팀과 앱 팀의 구분 자체가 모호하다.

### 최소 요구사항

| 항목 | 최소 요구 | 비고 |
|------|----------|------|
| Kubernetes 클러스터 | 1개 (single cluster 가능) | multi-cluster 필수 아님 |
| State Store | MinIO/S3/Git 1개 | GitOps 상태 저장소 |
| 컨트롤러 리소스 | ~256MB RAM, 0.2 CPU | Kratix 컨트롤러 자체 |
| GitOps 도구 | Flux 또는 ArgoCD | State Store 동기화 필수 |
| 학습 곡선 | CRD, Pipeline 개념 이해 | 1-2주 소요 |

**Single Cluster 구성은 가능하다.** `kratix`와 `kratix-destination` Helm 차트를 동일 클러스터에 설치하면 된다.

### 소규모 팀(3-5명)에서의 장단점

**장점:**
- Promise로 인프라 요청을 코드화하면 팀 확장 시 즉시 활용 가능
- 단일 클러스터에서도 동작하므로 시작 비용이 낮음
- 반복 프로비저닝이 많다면 규모와 무관하게 가치 있음

**단점:**
- 학습 비용 대비 팀원 수가 적어 ROI 낮음
- Promise/Pipeline 작성보다 직접 kubectl apply가 빠름
- GitOps 도구(Flux/ArgoCD)가 선행 필요 -- 추가 운영 부담
- 커뮤니티가 Crossplane/Terraform 대비 작음

### 대안 비교: 소규모 팀 관점

```
"인프라가 단순하다" ──────────> Helm + Kustomize (가장 가벼운 선택)
"클라우드 리소스 관리 필요" ──> Crossplane (AWS/GCP 리소스 직접 관리)
"Terraform 이미 사용 중" ────> Terraform + Atlantis (기존 워크플로우 유지)
"앱 팀이 5명+ 생길 예정" ───> Kratix 도입 준비 (Promise 패턴 미리 설계)
"풀 플랫폼 엔지니어링" ─────> Kratix + Crossplane + Backstage (엔터프라이즈)
```

### 도입 타이밍 판단 기준

아래 조건 중 **3개 이상** 해당하면 도입 가치가 있다:
1. **개발자가 3팀 이상** 분리되어 각자 인프라를 요청
2. **동일 리소스를 월 5회 이상** 반복 프로비저닝
3. **플랫폼 팀이 별도로 존재**하거나 구성 예정
4. **멀티 환경(dev/staging/prod)** 에서 일관된 프로비저닝 필요
5. **셀프서비스 포탈(Backstage 등)** 을 운영하거나 계획 중

---

## Kratix 아키텍처

```
┌──────────────────────────────────────────────────────┐
│                 Platform Cluster                      │
│  ┌──────────┐  ┌───────────┐  ┌───────────────┐     │
│  │ Promise  │─>│  Kratix   │─>│  State Store  │     │
│  │(CRD 정의) │  │Controller │  │ (Git/S3/MinIO)│     │
│  └──────────┘  └───────────┘  └──────┬────────┘     │
│  ┌──────────┐  ┌───────────┐         │              │
│  │ Resource │─>│ Pipeline  │         │              │
│  │ Request  │  │(OCI 컨테이너)│        │              │
│  └──────────┘  └───────────┘         │              │
└──────────────────────────────────────┼──────────────┘
                    Flux / ArgoCD 동기화 │
┌──────────────────────────────────────┼──────────────┐
│           Worker Cluster(s)          ▼              │
│  ┌───────────┐ ┌──────┐ ┌──────────────┐           │
│  │PostgreSQL │ │Redis │ │ Flux/ArgoCD  │           │
│  └───────────┘ └──────┘ └──────────────┘           │
└─────────────────────────────────────────────────────┘
```

핵심 개념:
- **Promise**: 플랫폼이 제공하는 서비스 계약. CRD + Pipeline + Dependencies
- **Pipeline**: Resource Request를 받아 K8s 매니페스트를 생성하는 컨테이너 워크플로우
- **Destination**: 리소스가 배포될 대상 클러스터(또는 시스템)
- **State Store**: Pipeline 결과물이 저장되는 Git 레포/S3 버킷

---

## Promise CRD 작성법

Promise는 3가지 핵심 요소로 구성: **API + Workflows + Dependencies**

```yaml
apiVersion: platform.kratix.io/v1alpha1
kind: Promise
metadata:
  name: postgresql
spec:
  # 1) API: 개발자가 사용할 CRD 정의
  api:
    apiVersion: apiextensions.k8s.io/v1
    kind: CustomResourceDefinition
    metadata:
      name: postgresqls.database.platform.company.com
    spec:
      group: database.platform.company.com
      names:
        kind: PostgreSQL
        singular: postgresql
        plural: postgresqls
      scope: Namespaced
      versions:
        - name: v1
          served: true
          storage: true
          schema:
            openAPIV3Schema:
              type: object
              properties:
                spec:
                  type: object
                  properties:
                    size:
                      type: string
                      enum: ["small", "medium", "large"]
                      default: "small"
                    version:
                      type: string
                      default: "16"
  # 2) Workflows: 요청 처리 파이프라인
  workflows:
    resource:
      configure:
        - apiVersion: platform.kratix.io/v1alpha1
          kind: Pipeline
          metadata:
            name: configure-postgresql
          spec:
            containers:
              - name: generate-manifests
                image: myorg/postgresql-promise-pipeline:v1.0
              - name: validate-security
                image: myorg/security-validator:v1.0
  # 3) Dependencies: Worker 클러스터에 미리 설치할 것들
  dependencies:
    - apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: postgresql-operator
        namespace: postgresql-system
      spec: # CloudNativePG Operator 등
        # ...
```

---

## 실전 Promise 예제: PostgreSQL as-a-Service

### Pipeline 컨테이너 코드

```python
#!/usr/bin/env python3
"""PostgreSQL Promise Pipeline: /kratix/input -> /kratix/output"""
import yaml

with open("/kratix/input/object.yaml") as f:
    request = yaml.safe_load(f)

spec = request["spec"]
name = request["metadata"]["name"]
namespace = request["metadata"].get("namespace", "default")
size = spec.get("size", "small")

SIZE_MAP = {
    "small":  {"cpu": "500m",  "memory": "1Gi",  "storage": "10Gi", "instances": 1},
    "medium": {"cpu": "1",     "memory": "4Gi",  "storage": "50Gi", "instances": 3},
    "large":  {"cpu": "2",     "memory": "8Gi",  "storage": "100Gi", "instances": 3},
}
r = SIZE_MAP[size]

pg_cluster = {
    "apiVersion": "postgresql.cnpg.io/v1",
    "kind": "Cluster",
    "metadata": {"name": f"pg-{name}", "namespace": namespace,
                 "labels": {"team": spec.get("teamName","unknown"), "managed-by": "kratix"}},
    "spec": {
        "instances": r["instances"],
        "imageName": f"ghcr.io/cloudnative-pg/postgresql:{spec.get('version','16')}",
        "storage": {"size": r["storage"]},
        "resources": {"requests": {"cpu": r["cpu"], "memory": r["memory"]}},
    },
}

with open("/kratix/output/pg-cluster.yaml", "w") as f:
    yaml.dump(pg_cluster, f)
```

### 개발자 사용법

```yaml
apiVersion: database.platform.company.com/v1
kind: PostgreSQL
metadata:
  name: my-app-db
  namespace: team-alpha
spec:
  size: medium
  version: "16"
```

```bash
kubectl apply -f my-database-request.yaml
# Kratix Pipeline 실행 -> State Store -> Flux/ArgoCD -> Worker 클러스터에 배포
```

---

## 실전 Promise 예제: Redis as-a-Service

```yaml
apiVersion: platform.kratix.io/v1alpha1
kind: Promise
metadata:
  name: redis-as-a-service
spec:
  api:
    apiVersion: apiextensions.k8s.io/v1
    kind: CustomResourceDefinition
    metadata:
      name: caches.cache.platform.example.com
    spec:
      group: cache.platform.example.com
      names: { kind: Cache, singular: cache, plural: caches }
      scope: Namespaced
      versions:
        - name: v1
          served: true
          storage: true
          schema:
            openAPIV3Schema:
              type: object
              properties:
                spec:
                  type: object
                  properties:
                    mode:
                      type: string
                      enum: ["standalone", "sentinel", "cluster"]
                      default: "standalone"
                    maxMemory: { type: string, default: "256Mi" }
                    version: { type: string, default: "7.2" }
  workflows:
    resource:
      configure:
        - apiVersion: platform.kratix.io/v1alpha1
          kind: Pipeline
          metadata: { name: deploy-redis }
          spec:
            containers:
              - name: generate-redis
                image: myorg/redis-promise-pipeline:v1.0
  dependencies:
    - apiVersion: apps/v1
      kind: Deployment
      metadata: { name: redis-operator, namespace: redis-system }
      spec:
        replicas: 1
        selector: { matchLabels: { app: redis-operator } }
        template:
          metadata: { labels: { app: redis-operator } }
          spec:
            containers:
              - name: redis-operator
                image: spotahome/redis-operator:v1.3.0
```

---

## Backstage 연동

```
개발자 -> Backstage Template -> Kratix Promise API -> Pipeline -> 리소스 생성
                                      |
                                      v
                             Backstage Catalog에 Component 자동 등록
```

### Backstage Template에서 Kratix 리소스 생성

```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: request-database
  title: "데이터베이스 요청"
spec:
  type: resource
  parameters:
    - title: 데이터베이스 설정
      properties:
        teamName: { title: 팀 이름, type: string }
        size: { title: 크기, type: string, enum: ["small","medium","large"], default: "small" }
        version: { title: PG 버전, type: string, enum: ["14","15","16"], default: "16" }
  steps:
    - id: create-resource
      name: Kratix 리소스 요청
      action: kubernetes:apply
      input:
        manifest:
          apiVersion: database.platform.company.com/v1
          kind: PostgreSQL
          metadata:
            name: ${{ parameters.teamName }}-db
          spec:
            size: ${{ parameters.size }}
            version: ${{ parameters.version }}
```

SKE(Syntasso Kratix Enterprise) 사용 시 Promise가 자동으로 Backstage Catalog Component와 Template을 생성한다.

---

## Kratix vs Crossplane vs Terraform 비교표

| 항목 | Kratix | Crossplane | Terraform |
|------|--------|-----------|-----------|
| **핵심 역할** | 플랫폼 오케스트레이터 | 인프라 컨트롤 플레인 | IaC 도구 |
| **추상화 수준** | 비즈니스 서비스 단위 | 클라우드 리소스 단위 | 인프라 리소스 단위 |
| **API 정의** | Promise (CRD) | XRD (Composite) | HCL 모듈 |
| **실행 방식** | Pipeline 컨테이너 | Provider 컨트롤러 | CLI / CI |
| **상태 관리** | State Store (Git/S3) | etcd (K8s) | tfstate |
| **K8s 필수** | Yes | Yes | No |
| **멀티 클러스터** | 네이티브 지원 | 가능 (직접 구성) | 가능 (Workspace) |
| **커뮤니티** | 작음 (성장 중) | 큼 (CNCF) | 매우 큼 |
| **상호 관계** | Crossplane/TF 위에 올림 | Kratix와 함께 사용 | Pipeline에서 호출 |

**핵심**: Kratix는 Crossplane/Terraform의 **대체가 아니라 그 위의 오케스트레이션 레이어**다.

---

## Pipeline 작성 상세

### 입출력 구조

```
/kratix/input/object.yaml      # 사용자의 Resource Request
/kratix/output/*.yaml           # Worker 클러스터에 배포할 매니페스트
/kratix/metadata/destination.yaml  # 배포 대상 Destination 지정 (선택)
/kratix/metadata/status.yaml       # Resource Request 상태 업데이트 (선택)
```

### 다단계 Pipeline

```yaml
workflows:
  resource:
    configure:
      - apiVersion: platform.kratix.io/v1alpha1
        kind: Pipeline
        metadata: { name: full-pipeline }
        spec:
          containers:
            - name: generate          # 1단계: 매니페스트 생성
              image: myorg/generator:v1.0
            - name: validate          # 2단계: 보안 정책 검증
              image: myorg/policy-checker:v1.0
              env: [{ name: POLICY_LEVEL, value: "production" }]
            - name: inject-metadata   # 3단계: 라벨 주입
              image: myorg/metadata-injector:v1.0
  promise:
    configure:                        # Promise 설치 시 실행
      - apiVersion: platform.kratix.io/v1alpha1
        kind: Pipeline
        metadata: { name: setup-deps }
        spec:
          containers:
            - name: install-operator
              image: myorg/operator-installer:v1.0
```

### Pipeline 셸 스크립트 패턴

```bash
#!/bin/bash
NAME=$(cat /kratix/input/object.yaml | yq '.metadata.name')
cat > /kratix/output/deployment.yaml <<EOF
apiVersion: apps/v1
kind: Deployment
metadata: { name: ${NAME} }
spec: { replicas: 1 }
EOF
# (선택) Destination 라우팅: /kratix/metadata/destination.yaml
# - matchLabels: { environment: production }
```

---

## Multi-Cluster 배포 전략 (Destinations)

```yaml
apiVersion: platform.kratix.io/v1alpha1
kind: Destination
metadata:
  name: production-cluster
  labels: { environment: production, region: ap-northeast-2 }
spec:
  stateStoreRef: { name: default-state-store, kind: BucketStateStore }
---
apiVersion: platform.kratix.io/v1alpha1
kind: BucketStateStore                    # S3/MinIO 기반
metadata: { name: default-state-store }
spec:
  endpoint: s3.amazonaws.com
  bucketName: kratix-state
  authMethod: accessKey
  secretRef: { name: s3-credentials }
---
apiVersion: platform.kratix.io/v1alpha1
kind: GitStateStore                       # Git 기반
metadata: { name: git-state-store }
spec:
  url: https://github.com/myorg/platform-state.git
  branch: main
  authMethod: basicAuth
  secretRef: { name: git-credentials }
```

Pipeline에서 `/kratix/metadata/destination.yaml`에 `matchLabels`로 지정하면 라벨이 일치하는 모든 Destination에 배포.

---

## 모니터링 & 디버깅

디버깅 순서: Promise 확인 -> Resource Request 상태 -> Pipeline Pod 로그 -> State Store -> GitOps 동기화 -> Worker 클러스터

```bash
kubectl get promises                                              # Promise 목록
kubectl get <resource-kind> -A                                    # 리소스 요청 상태
kubectl logs -n kratix-platform-system \
  -l kratix.io/promise-name=<name> --tail=50                      # Pipeline 로그
kubectl get destinations                                          # Destination 상태
kubectl get bucketstatestores,gitstatestores                      # State Store 상태
kubectl get kustomization -A  # Flux / kubectl get application -A # GitOps 동기화
```

---

## Anti-Patterns

| Anti-Pattern | 문제 | 올바른 접근 |
|-------------|------|-----------|
| 모든 것을 Promise로 만들기 | 추상화 과다 | 반복 프로비저닝되는 것만 |
| Pipeline에 비즈니스 로직 과다 | 유지보수 어려움 | 매니페스트 생성에 집중 |
| API에 옵션 과다 노출 | 개발자 혼란 | 합리적 기본값 + 최소 옵션 |
| State Store 미백업 | 상태 유실 | Git 사용 or S3 버전닝 |
| Pipeline 이미지 latest 태그 | 재현 불가 | 시맨틱 버저닝 필수 |
| Crossplane 없이 Kratix만 사용 | 클라우드 리소스 직접 관리 불편 | Kratix + Crossplane 조합 |
| Promise 테스트 미작성 | 회귀 버그 | kratix CLI로 로컬 테스트 |

---

## 체크리스트

**도입 전**: 팀 규모/인프라 복잡도 평가 | K8s 클러스터(최소 1개) | GitOps 도구(Flux/ArgoCD) | State Store(Git/S3) | 첫 Promise 후보 선정

**초기 설정**: kratix Helm 차트 설치 | kratix-destination 차트 설치 | State Store 연결 | Destination 등록 | 테스트 Promise 검증

**운영**: Pipeline Pod 모니터링 | State Store 백업 | Promise 버전 관리 | 개발자 문서화 | Backstage 연동(선택)

---

**관련 Skills**: `/infra:crossplane`, `/platform:backstage`, `/platform:golden-paths`, `/platform:developer-self-service`, `/cicd:gitops-argocd`
