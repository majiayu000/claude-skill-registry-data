---
name: crossplane
description: "Crossplane 기본 — 설치, Provider, Managed Resources, Compositions, Terraform 과 비교. Use when Kubernetes 로 클라우드 인프라를 선언적으로 관리하려고 Crossplane 을 도입할 때."
---

# Crossplane 멀티클라우드 가이드

Kubernetes-native 인프라 관리: Provider 설정, Compositions, 멀티클라우드 패턴

## Quick Reference (결정 트리)

```
IaC 도구 선택?
    |
    +-- Kubernetes 네이티브 우선 ----> Crossplane
    |       |
    |       +-- 자동 Drift 수정 -----> Crossplane (권장)
    |       +-- GitOps 통합 ---------> Crossplane + ArgoCD
    |
    +-- 기존 Terraform 자산 ---------> Terraform
    |       |
    |       +-- 점진적 전환 ---------> Crossplane + Terraform Provider
    |
    +-- 멀티클라우드 복잡 ------------> Crossplane Compositions
            |
            +-- 표준화된 추상화 -----> XRDs + Compositions

Crossplane vs Terraform?
    |
    +-- Drift 자동 복구 필요 --------> Crossplane
    +-- K8s 리소스와 동일 관리 ------> Crossplane
    +-- 기존 .tf 파일 재사용 --------> Terraform
    +-- 상태 파일 중앙화 ------------> Terraform Cloud
```

---

## CRITICAL: Crossplane vs Terraform 비교

| 항목 | Crossplane | Terraform |
|------|-----------|----------|
| **패러다임** | Kubernetes-native | 독립 CLI/상태 파일 |
| **Drift 감지** | 자동 (Reconciliation) | 수동 (`terraform plan`) |
| **Drift 수정** | **자동** | 수동 (`terraform apply`) |
| **상태 관리** | etcd (K8s) | .tfstate (S3, etc.) |
| **GitOps** | 네이티브 | 추가 도구 필요 |
| **학습 곡선** | K8s 경험 필요 | HCL 학습 |
| **성숙도** | 발전 중 (CNCF) | 검증됨 (10년+) |
| **모듈 생태계** | Compositions | 풍부한 모듈 |

### Crossplane 장점

```
Kubernetes Control Plane 활용
    |
    +-- 자동 Reconciliation (Drift 자동 수정)
    +-- RBAC 통합 (K8s 권한 모델)
    +-- GitOps 네이티브 (ArgoCD/Flux)
    +-- 단일 API 서버 (kubectl로 모든 관리)
    +-- 시크릿 관리 통합 (K8s Secrets)
```

---

## Crossplane 설치

### Helm 설치

```bash
# Crossplane 설치
helm repo add crossplane-stable https://charts.crossplane.io/stable
helm repo update

helm install crossplane crossplane-stable/crossplane \
  --namespace crossplane-system \
  --create-namespace \
  --set args='{"--enable-usages"}'

# 설치 확인
kubectl get pods -n crossplane-system
kubectl get providers
```

### Provider 설치

```yaml
# AWS Provider
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-aws
spec:
  package: xpkg.upbound.io/upbound/provider-family-aws:v1.14.0
  controllerConfigRef:
    name: aws-config
---
apiVersion: pkg.crossplane.io/v1alpha1
kind: ControllerConfig
metadata:
  name: aws-config
spec:
  args:
    - --debug
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 100m
      memory: 256Mi
---
# GCP Provider
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-gcp
spec:
  package: xpkg.upbound.io/upbound/provider-family-gcp:v1.8.0
---
# Azure Provider
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-azure
spec:
  package: xpkg.upbound.io/upbound/provider-family-azure:v1.3.0
```

---

## Provider 설정

### AWS ProviderConfig

```yaml
# Secret for AWS credentials
apiVersion: v1
kind: Secret
metadata:
  name: aws-creds
  namespace: crossplane-system
type: Opaque
stringData:
  credentials: |
    [default]
    aws_access_key_id = AKIA...
    aws_secret_access_key = ...
---
# ProviderConfig
apiVersion: aws.upbound.io/v1beta1
kind: ProviderConfig
metadata:
  name: default
spec:
  credentials:
    source: Secret
    secretRef:
      namespace: crossplane-system
      name: aws-creds
      key: credentials
---
# IRSA (권장 - EKS 환경)
apiVersion: aws.upbound.io/v1beta1
kind: ProviderConfig
metadata:
  name: irsa
spec:
  credentials:
    source: IRSA
```

---

## Managed Resources

### AWS S3 Bucket

```yaml
apiVersion: s3.aws.upbound.io/v1beta2
kind: Bucket
metadata:
  name: my-bucket
  labels:
    environment: production
spec:
  forProvider:
    region: ap-northeast-2
    tags:
      Environment: production
      ManagedBy: crossplane
  providerConfigRef:
    name: default
```

### AWS RDS Instance

```yaml
apiVersion: rds.aws.upbound.io/v1beta2
kind: Instance
metadata:
  name: my-postgres
spec:
  forProvider:
    region: ap-northeast-2
    allocatedStorage: 20
    engine: postgres
    engineVersion: "15.4"
    instanceClass: db.t3.micro
    dbName: mydb
    username: admin
    passwordSecretRef:
      name: db-password
      namespace: crossplane-system
      key: password
    skipFinalSnapshot: true
    publiclyAccessible: false
    vpcSecurityGroupIdSelector:
      matchLabels:
        app: my-app
  providerConfigRef:
    name: default
  writeConnectionSecretToRef:
    name: db-connection
    namespace: default
```

### GCP CloudSQL

```yaml
apiVersion: sql.gcp.upbound.io/v1beta2
kind: DatabaseInstance
metadata:
  name: my-cloudsql
spec:
  forProvider:
    region: asia-northeast3
    databaseVersion: POSTGRES_15
    settings:
      - tier: db-f1-micro
        ipConfiguration:
          - ipv4Enabled: false
            privateNetworkRef:
              name: my-vpc
    deletionProtection: false
  providerConfigRef:
    name: default
```

---

## Compositions (추상화)

### 아키텍처

```
+------------------------------------------------------------------+
|                     Application Developer                          |
|                     (Claim: DatabaseClaim)                         |
+------------------------------------------------------------------+
                               |
                               v
+------------------------------------------------------------------+
|                     Platform Team                                  |
|                     (XRD: XDatabase)                               |
+------------------------------------------------------------------+
                               |
          +--------------------+--------------------+
          |                    |                    |
          v                    v                    v
+------------------+  +------------------+  +------------------+
| Composition      |  | Composition      |  | Composition      |
| (AWS RDS)        |  | (GCP CloudSQL)   |  | (Azure SQL)      |
+------------------+  +------------------+  +------------------+
          |                    |                    |
          v                    v                    v
+------------------+  +------------------+  +------------------+
| Managed Resource |  | Managed Resource |  | Managed Resource |
| (RDS Instance)   |  | (CloudSQL)       |  | (Azure SQL DB)   |
+------------------+  +------------------+  +------------------+
```

### CompositeResourceDefinition (XRD)

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: xdatabases.platform.example.com
spec:
  group: platform.example.com
  names:
    kind: XDatabase
    plural: xdatabases

  claimNames:
    kind: DatabaseClaim
    plural: databaseclaims

  versions:
    - name: v1alpha1
      served: true
      referenceable: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              required:
                - parameters
              properties:
                parameters:
                  type: object
                  required:
                    - size
                    - engine
                  properties:
                    size:
                      type: string
                      enum: ["small", "medium", "large"]
                      description: "Database size"
                    engine:
                      type: string
                      enum: ["postgres", "mysql"]
                      description: "Database engine"
                    version:
                      type: string
                      default: "15"
                    highAvailability:
                      type: boolean
                      default: false
            status:
              type: object
              properties:
                connectionSecret:
                  type: string
                endpoint:
                  type: string
```

### Composition (AWS)

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: xdatabase-aws
  labels:
    provider: aws
    engine: postgres
spec:
  compositeTypeRef:
    apiVersion: platform.example.com/v1alpha1
    kind: XDatabase

  mode: Pipeline
  pipeline:
    - step: patch-and-transform
      functionRef:
        name: function-patch-and-transform
      input:
        apiVersion: pt.fn.crossplane.io/v1beta1
        kind: Resources
        resources:
          # RDS Instance
          - name: rds-instance
            base:
              apiVersion: rds.aws.upbound.io/v1beta2
              kind: Instance
              spec:
                forProvider:
                  region: ap-northeast-2
                  engine: postgres
                  skipFinalSnapshot: true
                  publiclyAccessible: false
                providerConfigRef:
                  name: default
            patches:
              # Size 매핑
              - type: FromCompositeFieldPath
                fromFieldPath: spec.parameters.size
                toFieldPath: spec.forProvider.instanceClass
                transforms:
                  - type: map
                    map:
                      small: db.t3.micro
                      medium: db.t3.small
                      large: db.t3.medium

              # Storage 매핑
              - type: FromCompositeFieldPath
                fromFieldPath: spec.parameters.size
                toFieldPath: spec.forProvider.allocatedStorage
                transforms:
                  - type: map
                    map:
                      small: 20
                      medium: 50
                      large: 100

              # Engine Version
              - type: FromCompositeFieldPath
                fromFieldPath: spec.parameters.version
                toFieldPath: spec.forProvider.engineVersion

              # HA 설정
              - type: FromCompositeFieldPath
                fromFieldPath: spec.parameters.highAvailability
                toFieldPath: spec.forProvider.multiAz

              # Connection Secret
              - type: ToCompositeFieldPath
                fromFieldPath: status.atProvider.endpoint
                toFieldPath: status.endpoint

            connectionDetails:
              - type: FromFieldPath
                fromFieldPath: status.atProvider.endpoint
                name: endpoint
              - type: FromFieldPath
                fromFieldPath: status.atProvider.username
                name: username
              - type: FromConnectionSecretKey
                fromConnectionSecretKey: password
                name: password
```

### Claim 사용

```yaml
# 개발자가 요청하는 간단한 인터페이스
apiVersion: platform.example.com/v1alpha1
kind: DatabaseClaim
metadata:
  name: my-app-db
  namespace: production
spec:
  parameters:
    size: medium
    engine: postgres
    version: "15"
    highAvailability: true

  compositionSelector:
    matchLabels:
      provider: aws

  writeConnectionSecretToRef:
    name: my-app-db-connection
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| Provider 버전 미고정 | 예기치 않은 변경 | 버전 명시 |
| 모든 리소스 직접 정의 | 유지보수 어려움 | Compositions 활용 |
| Drift 수정 비활성화 | 구성 불일치 | 기본값 유지 |
| Connection Secret 미사용 | 시크릿 하드코딩 | writeConnectionSecretToRef |
| XRD 과도한 복잡성 | 사용성 저하 | 간단한 인터페이스 |

---

## 체크리스트

### 설치
- [ ] Crossplane Helm 설치
- [ ] Provider 설치 (AWS/GCP/Azure)
- [ ] ProviderConfig 설정
- [ ] IRSA/Workload Identity 설정

### XRD/Compositions
- [ ] XRD 정의 (간단한 인터페이스)
- [ ] Composition 작성 (Provider별)
- [ ] Function 설치

## 참조 스킬

- `/infra:crossplane-advanced` - 멀티클라우드 패턴, GitOps 통합, Drift Detection
- `/infra:terraform-modules` - Terraform 모듈
- `/cicd:gitops-argocd` - ArgoCD GitOps
