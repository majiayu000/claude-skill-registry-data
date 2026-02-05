---
name: patterns-devops
description: 로컬 CI부터 배포까지 DevOps 패턴을 제공합니다. Justfile, E2E 테스트, CI/CD 파이프라인, Docker, 배포 자동화가 필요할 때 사용하세요.
---

# DevOps Patterns

로컬 개발 환경부터 배포까지 DevOps 전반의 패턴과 베스트 프랙티스를 제공합니다.

**핵심 철학**:
- Justfile로 로컬 자동화 통합
- E2E 테스트: 실제 DB 컨테이너 사용
- compose.yaml (docker compose v2)
- 언어별 도구는 최신 표준 (TypeScript: Biome)
- 점진적 도입: 필요한 것부터 하나씩

## Instructions

### 워크플로우: 요청 분석 및 리소스 선택

사용자 요청을 분석하여 필요한 리소스만 선택적으로 로드합니다.

#### 1. 키워드 매칭

사용자 요청의 키워드를 분석하여 필요한 리소스를 판단:

**Local CI 관련** (`resources/01-local-ci.md`)
- "lint", "linter", "포맷터", "formatter"
- "test", "테스트"
- "justfile", "task runner"
- "pre-commit", "hooks"
- "E2E", "통합 테스트"

**CI/CD 파이프라인** (`resources/02-ci-cd-pipelines.md`)
- "CI/CD", "파이프라인", "pipeline"
- "GitHub Actions", "GitLab CI"
- "자동화", "automation"
- "빌드", "build"

**Docker** (`resources/03-docker.md`)
- "Docker", "docker"
- "compose", "compose.yaml"
- "컨테이너", "container"
- "이미지", "image"
- "멀티스테이지", "multi-stage"

**배포** (`resources/04-deployment.md`)
- "배포", "deploy", "deployment"
- "PM2", "프로세스"
- "롤백", "rollback"
- "서비스", "service"

**데이터베이스** (`resources/05-database.md`)
- "postgres", "postgresql", "psql"
- "mysql", "mariadb"
- "DB 설정", "database"
- "익스텐션", "extension"
- "쿼리 튜닝", "성능 분석"

**언어별 도구** (`resources/languages/{언어}.md`)
- "TypeScript" + (lint/test) → `languages/typescript.md`
- "Python" + (lint/test) → `languages/python.md` (향후)
- "Ruby" + (lint/test) → `languages/ruby.md` (향후)

#### 2. 리소스 로딩 전략

**단일 키워드 감지**
- User: "Justfile로 lint 실행하고 싶어"
- → Read resources/01-local-ci.md
- → Read resources/languages/typescript.md (언어 감지 시)

**복합 요청**
- User: "프로젝트 전체 CI/CD 설정해줘"
- → Read resources/01-local-ci.md (Local CI)
- → Read resources/02-ci-cd-pipelines.md (CI/CD)
- → Read resources/03-docker.md (Docker)
- → 필요 시 languages/{언어}.md

**불명확한 요청**
- User: "개발 환경 설정"
- → REFERENCE.md 확인하여 사용자에게 선택지 제시
- → 선택에 따라 리소스 로드

#### 3. 리소스 적용

1. **현재 프로젝트 구조 파악**
   - pwd로 프로젝트 루트 확인
   - 기존 설정 파일 확인 (justfile, compose.yaml 등)

2. **리소스 Read**
   - 필요한 리소스만 Read
   - 다른 리소스 참조 필요 시 추가 Read

3. **패턴 적용**
   - Read한 리소스의 패턴을 프로젝트에 적용
   - 기존 설정이 있으면 수정, 없으면 생성
   - 사용자에게 변경 사항 확인

4. **검증**
   - 설정 파일 문법 검증
   - 가능하면 실행하여 동작 확인
   - 문제 발생 시 사용자에게 보고

### 예시

#### 예시 1: TypeScript 프로젝트 Local CI

User: "TypeScript 프로젝트에 lint와 test 자동화 설정해줘"

1. 키워드 매칭: "TypeScript", "lint", "test" → Local CI + TypeScript
2. Read resources/01-local-ci.md
3. Read resources/languages/typescript.md
4. justfile 생성/수정 (lint, test 태스크)
5. Biome 설정 (biome.json)
6. E2E 테스트용 compose.yaml 생성
7. 실행 확인: just lint, just test

#### 예시 2: GitHub Actions CI/CD

User: "GitHub Actions로 CI/CD 파이프라인 만들어줘"

1. 키워드 매칭: "GitHub Actions", "CI/CD" → CI/CD + 언어별
2. Read resources/02-ci-cd-pipelines.md
3. Read resources/languages/typescript.md (언어 확인 시)
4. .github/workflows/ci.yml 생성
5. compose.yaml 기반 service container 설정
6. 캐싱 전략 적용
7. 사용자에게 설정 확인

#### 예시 3: Docker 환경 구축

User: "Docker로 개발 환경 구축해줘"

1. 키워드 매칭: "Docker" → Docker
2. Read resources/03-docker.md
3. Dockerfile 생성 (멀티스테이지)
4. compose.yaml 생성 (app + DB + 기타 서비스)
5. .dockerignore 생성
6. 로컬 실행 확인: docker compose up

## 중요 원칙

1. **토큰 효율**: 필요한 리소스만 Read (40-60% 절감)
2. **점진적 도입**: 한 번에 모든 것을 설정하지 않음
3. **사용자 확인**: 변경 전후 사용자와 소통
4. **실행 검증**: 가능하면 항상 실행하여 동작 확인
5. **언어별 최신 도구**: ESLint 대신 Biome 등 최신 표준 사용

## Technical Details

상세한 설정 및 예제는 각 리소스 파일 참조:
- `REFERENCE.md`: 리소스 전체 개요
- `resources/01-local-ci.md`: Justfile, E2E 테스트 패턴
- `resources/02-ci-cd-pipelines.md`: GitHub Actions/GitLab CI
- `resources/03-docker.md`: Docker, compose.yaml
- `resources/04-deployment.md`: 배포 스크립트, PM2
- `resources/05-database.md`: PostgreSQL/MySQL 개발 환경, 성능 분석 도구
- `resources/languages/typescript.md`: Biome, Vitest/Jest
