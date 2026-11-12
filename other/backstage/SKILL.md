---
name: backstage
description: "Backstage 개발자 포털 — 아키텍처, 설치·초기 설정, Software Catalog, TechDocs, 주요 플러그인. Use when Backstage 를 처음 설치하고 서비스 카탈로그와 문서를 올릴 때. 템플릿·셀프서비스는 platform-backstage."
---

# Backstage 가이드

Developer Portal 구축, Software Catalog, 기본 설치 및 설정

## Quick Reference (결정 트리)

```
Backstage 기능 선택?
    │
    ├─ 서비스 카탈로그 ────────> Software Catalog
    │       │
    │       └─ catalog-info.yaml 작성
    │
    ├─ 서비스 생성 자동화 ────> Scaffolder (Templates)
    │       │
    │       └─ template.yaml 작성
    │
    ├─ 문서 통합 ───────────> TechDocs
    │       │
    │       └─ mkdocs.yml + Markdown
    │
    └─ 기능 확장 ───────────> Plugins
            │
            ├─ 공식 플러그인 설치
            └─ 커스텀 플러그인 개발
```

---

## CRITICAL: Backstage 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                     Backstage Architecture                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Frontend (React)                       │   │
│  │  ┌─────────┬─────────┬─────────┬─────────┐               │   │
│  │  │  Home   │ Catalog │ Create  │ Docs    │   Plugins...  │   │
│  │  └─────────┴─────────┴─────────┴─────────┘               │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Backend (Node.js)                      │   │
│  │  ┌─────────┬─────────┬─────────┬─────────┐               │   │
│  │  │ Catalog │Scaffol- │TechDocs │  Auth   │   Plugins...  │   │
│  │  │  API    │  der    │         │         │               │   │
│  │  └─────────┴─────────┴─────────┴─────────┘               │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                      Database (PostgreSQL)                │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 설치 및 초기 설정

### 로컬 개발 환경

```bash
# 요구사항: Node.js 18+, Yarn, Git

# 새 Backstage 앱 생성
npx @backstage/create-app@latest

# 프로젝트 이동
cd my-backstage-app

# 개발 서버 실행
yarn dev

# 브라우저에서 http://localhost:3000 접속
```

### Helm 설치 (프로덕션)

```bash
# Helm repo 추가
helm repo add backstage https://backstage.github.io/charts
helm repo update

# 설치
helm install backstage backstage/backstage \
  --namespace backstage \
  --create-namespace \
  --values backstage-values.yaml
```

### 프로덕션 설정

```yaml
# app-config.production.yaml
app:
  title: My Company Developer Portal
  baseUrl: https://backstage.company.com

organization:
  name: My Company

backend:
  baseUrl: https://backstage.company.com
  listen:
    port: 7007
  database:
    client: pg
    connection:
      host: ${POSTGRES_HOST}
      port: ${POSTGRES_PORT}
      user: ${POSTGRES_USER}
      password: ${POSTGRES_PASSWORD}

auth:
  providers:
    github:
      production:
        clientId: ${GITHUB_CLIENT_ID}
        clientSecret: ${GITHUB_CLIENT_SECRET}

integrations:
  github:
    - host: github.com
      token: ${GITHUB_TOKEN}
```

---

## Software Catalog

### Entity 종류

| Kind | 설명 | 예시 |
|------|------|------|
| **Component** | 소프트웨어 컴포넌트 | 서비스, 라이브러리 |
| **API** | API 정의 | REST, gRPC, GraphQL |
| **Resource** | 인프라 리소스 | DB, S3, Kafka |
| **System** | 컴포넌트 집합 | 주문 시스템 |
| **Domain** | 비즈니스 영역 | 커머스, 결제 |
| **Group** | 팀/조직 | team-platform |
| **User** | 사용자 | john.doe |

### catalog-info.yaml 기본 예시

```yaml
# Component (서비스)
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: order-service
  title: Order Service
  description: Handles order processing
  annotations:
    github.com/project-slug: my-org/order-service
    backstage.io/techdocs-ref: dir:.
  tags:
    - java
    - spring-boot
spec:
  type: service
  lifecycle: production
  owner: group:team-commerce
  system: e-commerce-platform
  providesApis:
    - order-api
  dependsOn:
    - resource:orders-db
```

### Catalog Provider 설정

```yaml
# app-config.yaml
catalog:
  rules:
    - allow: [Component, API, Resource, System, Domain, Group, User, Template]

  providers:
    # GitHub Discovery
    github:
      myOrg:
        organization: 'my-org'
        catalogPath: '/catalog-info.yaml'
        filters:
          branch: 'main'
        schedule:
          frequency: { minutes: 30 }
          timeout: { minutes: 3 }
```

---

## TechDocs

### 프로젝트 설정

```yaml
# mkdocs.yml (프로젝트 루트)
site_name: Order Service
site_description: Documentation for Order Service

nav:
  - Home: index.md
  - Architecture: architecture.md
  - API Reference: api.md
  - Runbook: runbook.md

plugins:
  - techdocs-core

markdown_extensions:
  - admonition
  - codehilite
  - pymdownx.superfences
```

### TechDocs 설정

```yaml
# app-config.yaml
techdocs:
  builder: 'external'  # local 또는 external
  generator:
    runIn: 'docker'
  publisher:
    type: 'awsS3'
    awsS3:
      bucketName: 'my-techdocs-bucket'
      region: 'ap-northeast-2'
```

---

## 주요 플러그인

### 설치 방법

```bash
# Frontend 플러그인
yarn --cwd packages/app add @backstage/plugin-kubernetes

# Backend 플러그인
yarn --cwd packages/backend add @backstage/plugin-kubernetes-backend
```

### 필수 플러그인 목록

| 플러그인 | 패키지 | 용도 |
|----------|--------|------|
| Kubernetes | `@backstage/plugin-kubernetes` | K8s 리소스 조회 |
| GitHub Actions | `@backstage/plugin-github-actions` | CI 상태 |
| ArgoCD | `@roadiehq/backstage-plugin-argo-cd` | GitOps 상태 |
| PagerDuty | `@pagerduty/backstage-plugin` | 인시던트 |
| Tech Radar | `@backstage/plugin-tech-radar` | 기술 현황 |

### Kubernetes 플러그인 설정

```yaml
# app-config.yaml
kubernetes:
  serviceLocatorMethod:
    type: 'multiTenant'
  clusterLocatorMethods:
    - type: 'config'
      clusters:
        - url: ${K8S_CLUSTER_URL}
          name: production
          authProvider: 'serviceAccount'
          serviceAccountToken: ${K8S_SA_TOKEN}
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 카탈로그 미등록 | 서비스 발견 불가 | CI에서 자동 등록 |
| 템플릿 미업데이트 | 보안 취약점 | 정기 업데이트 |
| 문서 미동기화 | 정보 불일치 | TechDocs + Git 연동 |
| 플러그인 과다 | 성능 저하 | 필수만 설치 |
| 단일 인스턴스 | 장애 위험 | HA 구성 |

---

## 체크리스트

### 초기 설정
- [ ] PostgreSQL 프로덕션 DB 설정
- [ ] GitHub/GitLab OAuth 인증
- [ ] 조직 구조 (Groups, Users) 정의
- [ ] 카탈로그 Discovery 설정

### 운영
- [ ] 헬스체크 엔드포인트 모니터링
- [ ] 데이터베이스 백업
- [ ] 플러그인 버전 업데이트
- [ ] 사용량 메트릭 수집

**관련 agent**: `platform-engineer`
**관련 skill**: `/platform:platform-backstage` (고급 패턴), `/platform:golden-paths`, `/cicd:gitops-argocd`
