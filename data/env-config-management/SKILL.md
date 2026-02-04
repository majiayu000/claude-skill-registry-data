---
name: env-config-management
description: 환경변수(.env.*), Spring 프로파일(application-*.yml) 수정 시 사용. app/backend/CLAUDE.md 참조 필수. 서비스별 포트 중복 검증, 민감 정보는 .env.local만, application-*.yml은 플레이스홀더만(기본값 금지). 의미없는 override 지양. SQS 엔드포인트 정확성 확인.
allowed-tools: Read, Grep, Glob, Edit
---

# 환경변수 및 Spring 프로파일 관리

## 참조 문서
- **필수**: [app/backend/CLAUDE.md](../../../app/backend/CLAUDE.md) - 환경변수 철학, 프로파일 구조
- **필수**: [docs/design/system-architecture.md](../../../docs/design/system-architecture.md) - 서비스 포트, API 엔드포인트
- **SQS**: [docs/design/sqs-architecture.md](../../../docs/design/sqs-architecture.md) - SQS 큐 이름, 엔드포인트

## 핵심 철학

### 환경변수 파일 역할

| 파일 | 역할 | 커밋 | 민감 정보 | 사용 시점 |
|------|------|------|----------|----------|
| **`.env`** | docker-compose 인프라 설정 (MySQL, LocalStack) | ✅ | ❌ | docker-compose up |
| **`.env.common`** | 컨테이너 공통 앱 설정 (Service URLs, SQS 큐) | ✅ | ❌ | docker-compose.{acceptance\|demo}.yml |
| **`.env.local`** | **Spring 직접 실행용 모든 설정** | ❌ (gitignore) | ✅ | Gradle bootRun/test (IDE) |
| **`.env.acceptance`** | .env.common 오버라이드 (테스트 DB, 더미 키) | ✅ | ❌ | docker-compose.acceptance.yml |
| **`.env.demo`** | .env.common 오버라이드 (데모 환경) | ✅ | ❌ | docker-compose.demo.yml |

### Spring 프로파일 파일

| 파일 | 환경 | 커밋 | 하드코딩 | 환경변수 로드 |
|------|------|------|----------|--------------|
| `application.yml` | 공통 | ✅ | ❌ (플레이스홀더만) | - |
| `application-local.yml` | 로컬 개발 (IDE) | ✅ | ❌ (플레이스홀더만) | Gradle이 .env.local 로드 |
| `application-acceptance.yml` | 인수 테스트 | ✅ | ❌ (플레이스홀더만) | .env.common + .env.acceptance |
| `application-prod.yml` | 운영/데모 | ✅ | ❌ (플레이스홀더만) | .env.common + .env.demo |

## 핵심 원칙 (절대 위반 금지 ⚠️)

### 1. 민감 정보 분리
```yaml
# ❌ 나쁜 예: application-local.yml에 하드코딩
jwt:
  secret: "my-secret-key-12345"  # 절대 금지!

# ✅ 좋은 예: 플레이스홀더만
jwt:
  secret: ${JWT_SECRET}
```

**규칙:**
- `.env.local`에만 민감 정보 저장 (gitignore)
- `application-*.yml`은 `${...}` 플레이스홀더만 사용
- 커밋되는 파일에는 절대 민감 정보 하드코딩 금지

### 2. 서비스별 포트 고정 (절대 변경 금지)
```
8080 - API Gateway (모든 요청 진입점)
8081 - User-Service
8082 - Course-Service
8083 - Schedule-Service
```

**검증:**
- 포트 번호 변경 시 모든 서비스의 `SERVICE_URL` 환경변수 확인
- API Gateway 라우팅 설정 확인

### 3. .env.local 필수 내용
```bash
# IDE 직접 실행 시 필요한 모든 설정 포함
# 1. 비밀 정보
JWT_SECRET=...
ENCRYPTION_KEY=...
LOCALSTACK_AUTH_TOKEN=...

# 2. 로컬 전용 설정 (localhost)
USER_SERVICE_URL=http://localhost:8081
COURSE_SERVICE_URL=http://localhost:8082
SCHEDULE_SERVICE_URL=http://localhost:8083

# 3. .env.common의 모든 내용 복사
# (중복이지만 로컬 실행 시 필요)
CANVAS_API_BASE_URL=https://khcanvas.khu.ac.kr/api/v1
SQS_ENDPOINT=http://localhost:4566
...
```

### 4. 플레이스홀더 기본값 절대 금지 (Fail Fast)
```yaml
# ❌ 나쁜 예: 기본값 사용
spring:
  datasource:
    url: ${DATABASE_URL:jdbc:mysql://localhost:3306/default}  # 절대 금지!

# ✅ 좋은 예: 기본값 없이 명시적 실패
spring:
  datasource:
    url: ${DATABASE_URL}  # 환경변수 없으면 에러 발생
```

**철학:**
- **예상치 못한 기본값은 예상치 못한 동작을 야기함**
- 환경변수가 누락되면 **명시적으로 에러 발생**시켜 즉시 파악
- "조용히 잘못 동작"보다 "명시적으로 실패"가 훨씬 안전

**규칙:**
- `${VAR_NAME:default}` 형식 절대 금지
- `${VAR_NAME}` 형식만 사용
- 누락된 환경변수는 즉시 감지되어야 함

### 5. 의미없는 Override 지양 (DRY 원칙)
```bash
# ❌ 나쁜 예: .env.common과 동일한 값을 .env.acceptance에서 반복
# .env.common
CANVAS_API_BASE_URL=https://khcanvas.khu.ac.kr/api/v1

# .env.acceptance (의미없는 중복)
CANVAS_API_BASE_URL=https://khcanvas.khu.ac.kr/api/v1  # 절대 금지! base와 동일

# ✅ 좋은 예: 실제로 다른 값만 override
# .env.common
DATABASE_URL=jdbc:mysql://mysql:3306/unisync

# .env.acceptance (테스트 DB로 override)
DATABASE_URL=jdbc:mysql://mysql:3306/unisync_test  # 이건 OK (실제로 다름)
```

**철학:**
- **base & override 관계에서 같은 값 반복은 의미 없음**
- 환경변수 개수가 지나치게 많아지면 관리 어려움
- 변경 시 여러 파일 수정해야 하는 부담 증가

**규칙:**
- `.env.common`에 있는 값을 `.env.{acceptance|demo}`에서 동일하게 반복 금지
- `application.yml`에 있는 값을 `application-{local|acceptance|prod}.yml`에서 동일하게 반복 금지
- **실제로 다른 값일 때만 override**

**Base & Override 관계:**
```
# 환경변수 파일
.env.common (base)
  ├── .env.acceptance (override: 테스트 전용 값만)
  └── .env.demo (override: 데모 전용 값만)

# Spring 프로파일
application.yml (base)
  ├── application-local.yml (override: 로컬 전용 값만)
  ├── application-acceptance.yml (override: 테스트 전용 값만)
  └── application-prod.yml (override: 운영 전용 값만)
```

### 6. SQS 큐 이름 정확성
```bash
# 반드시 docs/design/sqs-architecture.md와 일치해야 함
SQS_LAMBDA_TO_COURSE_ENROLLMENTS=lambda-to-courseservice-enrollments
SQS_LAMBDA_TO_COURSE_ASSIGNMENTS=lambda-to-courseservice-assignments
SQS_COURSE_TO_SCHEDULE_ASSIGNMENTS=courseservice-to-scheduleservice-assignments
```

**검증:**
- SQS 큐 이름 변경 시 관련 서비스 모두 확인
- LocalStack에서 큐 생성 스크립트 확인 (`init-aws.sh`)

## 체크리스트

### .env.* 파일 수정 시

#### 작성 전
- [ ] app/backend/CLAUDE.md 환경변수 철학 확인
- [ ] 수정할 파일 역할 확인 (.env vs .env.common vs .env.local)
- [ ] 민감 정보는 .env.local에만 작성 확인

#### 작성 중
- [ ] **민감 정보 분리**: 비밀 정보는 .env.local만
- [ ] **포트 중복 검증**: 8080-8083 범위 확인
- [ ] **SERVICE_URL 정확성**: http://localhost:{포트} 형식
- [ ] **SQS 큐 이름**: docs/design/sqs-architecture.md와 일치
- [ ] **CANVAS_API_BASE_URL**: https://khcanvas.khu.ac.kr/api/v1 고정
- [ ] **의미없는 override 금지**: base 파일과 동일한 값 반복 금지

#### 작성 후
- [ ] .env.local.example 업데이트 (새 변수 추가 시)
- [ ] 관련 서비스 재시작하여 환경변수 로드 확인
- [ ] `./gradlew printEnv` 실행하여 로드 검증

### application-*.yml 파일 수정 시

#### 작성 전
- [ ] 수정할 프로파일 확인 (local/acceptance/prod)
- [ ] 해당 프로파일의 용도 확인 (app/backend/CLAUDE.md 참조)

#### 작성 중
- [ ] **하드코딩 금지**: 모든 값은 `${...}` 플레이스홀더
- [ ] **플레이스홀더 기본값 금지**: `${VAR:default}` 형식 절대 금지, `${VAR}` 만 사용
- [ ] **플레이스홀더 네이밍**: 대문자_스네이크_케이스
- [ ] **환경변수 존재 확인**: 해당 환경변수가 .env.* 파일에 존재하는지 확인
- [ ] **의미없는 override 금지**: application.yml과 동일한 값 반복 금지

#### 작성 후
- [ ] 해당 프로파일로 서비스 실행하여 검증
- [ ] 누락된 환경변수 없는지 확인 (에러 로그 확인)

### 새 환경변수 추가 시

#### 단계별 작업
1. **docs/design/system-architecture.md** 또는 **app/backend/CLAUDE.md** 업데이트
   - 새 환경변수 목적, 형식 문서화

2. **.env.common** 또는 **.env.local**에 추가
   - 공통 설정: .env.common
   - 민감 정보: .env.local만

3. **.env.local.example** 업데이트
   - 새 환경변수 템플릿 추가
   - 설명 주석 추가

4. **application-*.yml**에 플레이스홀더 추가
   - `${NEW_VARIABLE_NAME}` (기본값 없이)
   - ⚠️ **절대 금지**: `${NEW_VARIABLE_NAME:default-value}` (기본값 설정)

5. **검증**
   - `./gradlew printEnv` 실행
   - 서비스 재시작 후 로그 확인
   - 환경변수 누락 시 에러 발생 확인 (Fail Fast)

## 금지사항

- ❌ **application-*.yml에 하드코딩**: 민감 정보, URL, 포트 등 절대 금지
- ❌ **플레이스홀더 기본값 사용**: `${VAR:default}` 형식 절대 금지 (Fail Fast 위반)
- ❌ **의미없는 override**: base 파일과 동일한 값을 override 파일에서 반복
- ❌ **포트 번호 변경**: 8080-8083 고정, 변경 시 전체 시스템 영향
- ❌ **SERVICE_URL 오타**: http://localhost:8081 형식 정확히 준수
- ❌ **.env.local 커밋**: gitignore 확인, 민감 정보 유출 방지
- ❌ **SQS 큐 이름 오타**: docs/design/sqs-architecture.md와 정확히 일치
- ❌ **.env.common에 민감 정보**: JWT_SECRET, ENCRYPTION_KEY 등 .env.local만

## 트러블슈팅

### 문제: 환경변수가 로드 안됨
**해결**:
1. `.env.local` 파일 존재 확인
2. Gradle 스크립트 확인 (build.gradle.kts)
3. `./gradlew printEnv` 실행하여 로드 상태 확인

### 문제: LocalStack 연결 실패
**해결**:
1. `docker-compose ps` 실행하여 LocalStack 상태 확인
2. `.env.local`에 `LOCALSTACK_AUTH_TOKEN` 존재 확인
3. `SQS_ENDPOINT=http://localhost:4566` 확인

### 문제: 서비스 간 통신 실패
**해결**:
1. 포트 번호 확인 (8080-8083)
2. `SERVICE_URL` 환경변수 확인
3. API Gateway 라우팅 설정 확인 (GatewayRoutesConfig.java)

## 환경변수 검증 명령

```bash
# User Service 환경변수 확인
cd app/backend/user-service
./gradlew printEnv

# Course Service
cd app/backend/course-service
./gradlew printEnv

# Schedule Service
cd app/backend/schedule-service
./gradlew printEnv

# API Gateway
cd app/backend/api-gateway
./gradlew printEnv
```

## 참고: 환경별 실행 방법

### 로컬 개발 (IDE)
```bash
# 1. 인프라 실행
docker-compose up -d

# 2. IDE에서 서비스 실행
# Profile: local
# Gradle이 .env.local 자동 로드
```

### Acceptance 테스트
```bash
# 사전 준비: .env.local 필요 (LOCALSTACK_AUTH_TOKEN)
docker-compose -f docker-compose.acceptance.yml up --build
```

### Demo (전체 시스템)
```bash
# 사전 준비: .env.local 필요 (LOCALSTACK_AUTH_TOKEN)
docker-compose -f docker-compose.demo.yml up
```