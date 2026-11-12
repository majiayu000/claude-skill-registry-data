---
name: docker
description: "Dockerfile 최적화 — 멀티스테이지 빌드, Go·Spring Boot 컨테이너, 레이어 캐시, 보안, 멀티 플랫폼 빌드, Compose. Use when Dockerfile 을 작성하거나 이미지 크기와 빌드 속도를 개선할 때."
---

# Docker & Dockerfile Patterns

Dockerfile 최적화, 멀티스테이지 빌드, Go/Java 컨테이너 패턴

## Quick Reference (결정 트리)

```
베이스 이미지 선택
    │
    ├─ Go ──────────> scratch (12MB) 또는 distroless
    │
    └─ Java ────────> eclipse-temurin:21-jre-alpine
                      └─ 빠른 시작 필요 ──> GraalVM Native

빌드 최적화
    │
    ├─ 캐시 ────────> BuildKit --mount=type=cache
    │
    └─ 이미지 크기 ──> 멀티스테이지 + .dockerignore
```

---

## CRITICAL: 멀티스테이지 빌드

**IMPORTANT**: 반드시 멀티스테이지 사용 (이미지 크기 90% 감소)

| | 단일 스테이지 | 멀티스테이지 |
|---|-------------|-------------|
| Go | ~800MB | ~12MB |
| Java | ~600MB | ~150MB |

---

## Go Dockerfile (Production-Ready)

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.23-alpine AS builder

RUN apk add --no-cache git ca-certificates tzdata

WORKDIR /app
COPY go.mod go.sum ./

# CRITICAL: BuildKit 캐시 (12배 빌드 속도)
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

COPY . .
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-w -s" -o /app/server ./cmd/api

# scratch = 0MB 베이스 (보안 최우선)
FROM scratch
COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /etc/passwd /etc/passwd
USER nobody
COPY --from=builder /app/server /server
EXPOSE 8080
ENTRYPOINT ["/server"]
```

### Go 빌드 옵션

| 옵션 | 설명 |
|------|------|
| `CGO_ENABLED=0` | 순수 Go (C 라이브러리 불필요) |
| `-ldflags="-w -s"` | 디버그 정보 제거 (30% 감소) |

### 베이스 이미지 비교

| 이미지 | 크기 | 쉘 | 용도 |
|--------|------|-----|------|
| `scratch` | 0MB | ❌ | 프로덕션 (보안 최우선) |
| `distroless` | 2MB | ❌ | 프로덕션 |
| `alpine` | 5MB | ✅ | 디버깅 필요 시 |

---

## Java/Spring Boot Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
FROM eclipse-temurin:21-jdk-alpine AS builder

WORKDIR /app
COPY gradle gradle
COPY gradlew build.gradle.kts settings.gradle.kts ./

RUN --mount=type=cache,target=/root/.gradle \
    ./gradlew dependencies --no-daemon

COPY src src
RUN --mount=type=cache,target=/root/.gradle \
    ./gradlew bootJar --no-daemon -x test

# Spring Boot 3+ 레이어 추출
RUN java -Djarmode=layertools -jar build/libs/*.jar extract

FROM eclipse-temurin:21-jre-alpine
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring
WORKDIR /app

# 레이어 순서 (변경 빈도 낮은 것 먼저)
COPY --from=builder /app/dependencies/ ./
COPY --from=builder /app/spring-boot-loader/ ./
COPY --from=builder /app/snapshot-dependencies/ ./
COPY --from=builder /app/application/ ./

ENV JAVA_OPTS="-XX:MaxRAMPercentage=75.0"
EXPOSE 8080
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS org.springframework.boot.loader.launch.JarLauncher"]
```

### JVM vs Native

| | JVM | Native (GraalVM) |
|---|-----|------------------|
| 시작 시간 | ~2초 | ~50ms |
| 메모리 | ~300MB | ~50MB |
| 빌드 시간 | ~30초 | ~5분 |
| 용도 | 일반 서비스 | 서버리스 |

### GraalVM Native Image Dockerfile

```dockerfile
FROM ghcr.io/graalvm/graalvm-community:21 AS builder
WORKDIR /app
COPY gradle gradle
COPY gradlew build.gradle.kts settings.gradle.kts ./
RUN --mount=type=cache,target=/root/.gradle \
    ./gradlew dependencies --no-daemon
COPY src src
RUN --mount=type=cache,target=/root/.gradle \
    ./gradlew nativeCompile --no-daemon  # 3-10분 소요

FROM gcr.io/distroless/base-debian12
COPY --from=builder /app/build/native/nativeCompile/app /app
EXPOSE 8080
ENTRYPOINT ["/app"]
```

---

## 레이어 최적화

**IMPORTANT**: 변경 빈도 낮은 것 → 높은 것 순서

```dockerfile
# 1. 시스템 패키지 (거의 안 변함)
RUN apt-get update && apt-get install -y ...

# 2. 의존성 (가끔 변함)
COPY go.mod go.sum ./
RUN go mod download

# 3. 소스 코드 (자주 변함)
COPY . .
RUN go build
```

### .dockerignore

```
.git
.idea
.vscode
bin/
build/
target/
*_test.go
Dockerfile*
.env
*.log
```

---

## 보안 Best Practices

```dockerfile
# 1. 논루트 유저
RUN addgroup -S app && adduser -S app -G app
USER app

# 2. 태그 명시 (latest 금지)
FROM golang:1.23-alpine  # ✅
FROM golang:latest       # ❌
```

### 시크릿 처리

```dockerfile
# Bad: 이미지에 포함
COPY .env /app/.env

# Good: 런타임 주입
# docker run -e DATABASE_URL=... myapp

# Good: BuildKit 시크릿
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm install
```

---

## Docker Compose

```yaml
services:
  app:
    build:
      context: .
      target: builder  # 개발용
    volumes:
      - .:/app
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 5s
      retries: 5
```

### 포트 바인딩 가이드

| 형식 | 의미 | 접근 범위 |
|------|------|----------|
| `"127.0.0.1:3000:3000"` | localhost만 바인딩 | 로컬만 접근 가능 |
| `"3000:3000"` | `0.0.0.0:3000:3000`과 동일 | 모든 네트워크 접근 가능 |
| `"0.0.0.0:3000:3000"` | 명시적 전체 바인딩 | 모든 네트워크 접근 가능 |

**CRITICAL**: ALB/reverse proxy 뒤에 있는 컨테이너는 **`0.0.0.0` 바인딩 필수**.
`127.0.0.1` 바인딩 시 ALB health check 및 외부 트래픽 전달 불가.
네트워크 접근 제한은 Security Group에서 처리한다.

### Healthcheck 프로토콜

| 방법 | HTTP 메서드 | 호환성 | 권장 |
|------|-----------|--------|------|
| `wget --spider` | HEAD | 일부 서비스 HEAD 미지원 (Loki 등) | ❌ |
| `wget -qO /dev/null` | GET | 범용 호환 | ✅ |
| `curl -f` | GET | 가장 범용적 (alpine에 curl 필요) | ✅ |

```yaml
# ❌ HEAD 미지원 서비스에서 실패
healthcheck:
  test: ["CMD", "wget", "--spider", "-q", "http://localhost:3100/ready"]

# ✅ GET 요청으로 안전하게
healthcheck:
  test: ["CMD", "wget", "-qO", "/dev/null", "http://localhost:3100/ready"]
```

**ALB Healthcheck**: 인증 불필요한 엔드포인트 선택 (Spring Boot → `/actuator/health`)

### 환경변수 기본값 패턴

Docker Compose에서 앱에 전달하는 환경변수는 **반드시 기본값** 설정.

```yaml
# ✅ 기본값 패턴: .env 없이도 기동 가능
services:
  app:
    environment:
      DB_HOST: ${DB_HOST:-localhost}
      DB_PORT: ${DB_PORT:-5432}
      JWT_ACCESS_TIME: ${JWT_ACCESS_TIME:-3600000}
      JWT_SOCIAL_VERIFY_TIME: ${JWT_SOCIAL_VERIFY_TIME:-300000}   # 누락 주의

# ❌ 기본값 없음: .env 미설정 시 "${JWT_SOCIAL_VERIFY_TIME}" 문자열이 그대로 전달
environment:
  JWT_SOCIAL_VERIFY_TIME: ${JWT_SOCIAL_VERIFY_TIME}
```

**application.yml 양쪽 동기화 필수**:
```yaml
# Spring Boot application.yml — Docker 밖에서도 기본값 보장
jwt:
  social-verify-valid-time: ${JWT_SOCIAL_VERIFY_TIME:300000}
```

**체크 포인트**: 새 환경변수 추가 시 3곳 확인
1. `docker-compose*.yml` — `${VAR:-default}`
2. `application*.yml` — `${VAR:default}`
3. `.env.example` — 문서화

---

### 네트워크 설정

```yaml
# 새 네트워크 생성 (기본)
networks:
  app-net:
    driver: bridge

# 기존 네트워크 재사용
networks:
  existing-net:
    external: true

# ❌ name + driver 조합 — 기존 네트워크와 Docker Compose 라벨 충돌 가능
networks:
  my-net:
    name: shared-network
    driver: bridge  # 라벨 com.docker.compose.network 충돌
```

**`external: true`**: Docker Compose 외부에서 미리 생성된 네트워크를 참조. Compose가 생성/삭제하지 않음.
**`name:` + `driver:`**: Compose가 네트워크를 생성하려 하지만, 동일 이름의 기존 네트워크가 있으면 라벨 충돌 발생.

---

## 멀티 플랫폼 빌드

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t myapp:latest --push .
```

---

## Anti-Patterns

| 실수 | 올바른 방법 |
|------|------------|
| `FROM ubuntu` | `FROM ubuntu:22.04` (태그 명시) |
| `latest` 태그 | 구체적 버전 |
| Root로 실행 | `USER nobody` |
| 빌드 도구 포함 | 멀티스테이지 분리 |
| `COPY . .` 먼저 | 의존성 파일 먼저 |
| apt 캐시 남김 | `rm -rf /var/lib/apt/lists/*` |
| ALB 뒤 컨테이너에 `127.0.0.1` 포트 바인딩 | `0.0.0.0` 바인딩 (SG로 제한) |
| Healthcheck에 `wget --spider` | `wget -qO /dev/null` 또는 `curl -f` (GET) |
| `name:` + `driver:` 네트워크 조합 | 기존 네트워크 재사용 시 `external: true` |

---

## 체크리스트

### 이미지 최적화
- [ ] 멀티스테이지 빌드
- [ ] 적절한 베이스 이미지
- [ ] .dockerignore 설정
- [ ] 레이어 순서 최적화
- [ ] BuildKit 캐시 활용

### 보안
- [ ] 논루트 유저
- [ ] 태그 버전 명시
- [ ] 시크릿 이미지에 포함 X

### Go 특화
- [ ] `CGO_ENABLED=0`
- [ ] `-ldflags="-w -s"`
- [ ] scratch/distroless 사용

### Java 특화
- [ ] JRE 이미지 (JDK X)
- [ ] Spring Boot layered JAR
- [ ] `-XX:MaxRAMPercentage`

**관련 skill**: `/k8s:k8s-helm`, `/k8s:k8s-security`
