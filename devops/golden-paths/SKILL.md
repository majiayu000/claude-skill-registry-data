---
name: golden-paths
description: "Golden Path 설계 — 원칙, 구성 요소, 서비스 템플릿, best practice. Use when 개발자가 따를 표준 경로와 서비스 템플릿의 범위를 정하려 할 때. 인프라·CI/CD 템플릿 실체는 golden-paths-infra."
---

# Golden Paths 가이드

개발자를 위한 표준화된 경로 설계, 템플릿 패턴

## Quick Reference (결정 트리)

```
Golden Path 유형?
    │
    ├─ 서비스 생성 ─────────> Service Template
    │       │
    │       ├─ Backend API ───> Spring Boot / Go
    │       ├─ Frontend ──────> React / Next.js
    │       └─ Worker ────────> K8s Job / CronJob
    │
    ├─ 인프라 프로비저닝 ───> Infrastructure Template
    │       │
    │       ├─ Database ──────> RDS / CloudSQL
    │       ├─ Cache ─────────> ElastiCache / Redis
    │       └─ Queue ─────────> SQS / Kafka
    │
    └─ 환경 구성 ───────────> Environment Template
            │
            ├─ Dev ───────────> 개발 환경
            ├─ Staging ───────> 스테이징
            └─ Production ────> 프로덕션
```

---

## CRITICAL: Golden Path 원칙

### 정의

> **Golden Path**: 개발자가 일반적인 작업을 수행할 때 따르는 사전 정의된, 권장되는 경로. 인지 부하를 줄이고 Best Practices를 자동으로 적용.

### 4가지 필수 원칙

| 원칙 | 설명 | 예시 |
|------|------|------|
| **Optional** | 강제가 아닌 선택 | 표준 외 도구 허용 |
| **Transparent** | 내부 동작이 투명 | 생성된 코드 확인 가능 |
| **Extensible** | 팀별 확장 가능 | 플러그인 추가 가능 |
| **Customizable** | 필요시 수정 가능 | 설정 오버라이드 |

### Golden Path 성숙도

```
Level 1: Documented
  └─ 위키/문서로 Best Practice 정리

Level 2: Templated
  └─ 코드 템플릿, 파이프라인 템플릿 제공

Level 3: Automated
  └─ 셀프서비스 포탈에서 원클릭 생성

Level 4: Product
  └─ 릴리스 관리, 피드백 루프, 지속 개선
```

---

## Golden Path 구성 요소

### 전체 구조

```
Golden Path = Repository Template
            + CI/CD Pipeline
            + Infrastructure as Code
            + Observability Defaults
            + Security Baseline
            + Documentation
```

### 예시: Spring Boot 서비스 Golden Path

```
spring-boot-golden-path/
│
├── 1. Repository Template
│   ├── src/main/java/...
│   ├── Dockerfile
│   ├── build.gradle
│   └── catalog-info.yaml
│
├── 2. CI/CD Pipeline
│   └── .github/workflows/
│       ├── ci.yaml           # 빌드, 테스트
│       ├── security.yaml     # SAST, SCA
│       └── deploy.yaml       # CD
│
├── 3. Infrastructure
│   └── terraform/
│       ├── database.tf       # RDS
│       ├── cache.tf          # ElastiCache
│       └── iam.tf            # IAM Role
│
├── 4. Kubernetes Manifests
│   └── helm/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│
├── 5. Observability
│   ├── grafana/
│   │   └── dashboard.json
│   └── prometheus/
│       └── alerts.yaml
│
└── 6. Documentation
    ├── docs/
    └── mkdocs.yml
```

---

## Service Templates

### Spring Boot API Template

```yaml
# Backstage template.yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: spring-boot-api
  title: Spring Boot REST API
  description: |
    Production-ready Spring Boot API with:
    - Java 21, Spring Boot 3.2+
    - PostgreSQL + Redis
    - GitHub Actions CI/CD
    - Helm + ArgoCD deployment
  tags:
    - java
    - spring-boot
    - golden-path
spec:
  owner: group:team-platform
  type: service

  parameters:
    - title: Service Details
      required: [serviceName, owner]
      properties:
        serviceName:
          title: Service Name
          type: string
          pattern: '^[a-z][a-z0-9-]{2,30}$'
        owner:
          title: Owner Team
          type: string
          ui:field: OwnerPicker
        tier:
          title: Service Tier
          type: string
          enum: ['tier-1', 'tier-2', 'tier-3']
          default: 'tier-2'

    - title: Technical Options
      properties:
        database:
          title: Database
          type: string
          enum: ['postgresql', 'mysql', 'none']
          default: 'postgresql'
        cache:
          title: Cache
          type: boolean
          default: true

  steps:
    - id: fetch-template
      action: fetch:template
      input:
        url: ./skeleton
        values:
          serviceName: ${{ parameters.serviceName }}
          owner: ${{ parameters.owner }}
          tier: ${{ parameters.tier }}

    - id: publish
      action: publish:github
      input:
        repoUrl: github.com?owner=my-org&repo=${{ parameters.serviceName }}

    - id: register
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps.publish.output.repoContentsUrl }}
        catalogInfoPath: /catalog-info.yaml

  output:
    links:
      - title: Repository
        url: ${{ steps.publish.output.remoteUrl }}
      - title: Open in Catalog
        entityRef: ${{ steps.register.output.entityRef }}
```

### Go Service Template

```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: go-service
  title: Go Microservice
  description: High-performance Go service with Gin framework
spec:
  owner: group:team-platform
  type: service

  parameters:
    - title: Service Details
      required: [serviceName, owner]
      properties:
        serviceName:
          title: Service Name
          type: string
          pattern: '^[a-z][a-z0-9-]{2,30}$'
        owner:
          title: Owner Team
          type: string
          ui:field: OwnerPicker

    - title: Framework
      properties:
        framework:
          title: HTTP Framework
          type: string
          enum: ['gin', 'echo', 'chi', 'stdlib']
          default: 'gin'
        grpc:
          title: Enable gRPC
          type: boolean
          default: false

  steps:
    - id: fetch-template
      action: fetch:template
      input:
        url: ./go-skeleton
        values:
          serviceName: ${{ parameters.serviceName }}
          framework: ${{ parameters.framework }}
```

### React Frontend Template

```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: react-frontend
  title: React Frontend Application
  description: React SPA with Vite, TypeScript, CloudFront deployment
spec:
  owner: group:team-platform
  type: website

  parameters:
    - title: Application Details
      properties:
        appName:
          title: Application Name
          type: string
        owner:
          title: Owner Team
          type: string
          ui:field: OwnerPicker

    - title: Features
      properties:
        stateManagement:
          title: State Management
          type: string
          enum: ['zustand', 'redux-toolkit', 'jotai', 'none']
          default: 'zustand'
```

---

## Best Practices

### Do's

| Practice | 이유 |
|----------|------|
| 80% 규칙 적용 | 대부분 케이스만 커버, 예외는 허용 |
| 개발자와 공동 설계 | 실제 필요 반영 |
| 정기 업데이트 | 보안 취약점, 버전 관리 |
| 피드백 수집 | 지속적 개선 |
| 문서화 | 선택 이유, 탈출구 명시 |

### Don'ts

| Anti-Pattern | 문제 |
|--------------|------|
| 강제 채택 | 반발, 우회 |
| 과도한 추상화 | 디버깅 어려움 |
| 모든 것 표준화 | 혁신 저해 |
| 업데이트 방치 | 보안 위험 |
| 피드백 무시 | 사용자 이탈 |

---

## 체크리스트

### Golden Path 설계
- [ ] 80% 유스케이스 식별
- [ ] 팀별 요구사항 인터뷰
- [ ] 기존 Best Practice 문서화
- [ ] 탈출구(Escape Hatch) 정의

### 템플릿 구현
- [ ] Repository template
- [ ] CI/CD pipeline
- [ ] Infrastructure modules
- [ ] Observability defaults
- [ ] Security baseline

### 운영
- [ ] 분기별 템플릿 리뷰
- [ ] 보안 취약점 스캔
- [ ] 사용률 메트릭 수집
- [ ] 개발자 피드백 수집

**관련 agent**: `platform-engineer`
**관련 skill**: `/platform:golden-paths-infra` (Infrastructure, CI/CD), `/platform:backstage`, `/cicd:gitops-argocd`
