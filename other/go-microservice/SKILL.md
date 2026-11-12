---
name: go-microservice
description: "Use when designing or refactoring Go microservices: gRPC server/client, HTTP handlers, context propagation, graceful shutdown, dependency injection, internal package layout. Apply when go.mod imports grpc-go, chi, echo, or gin."
version: 1.0.0
license: MIT
applies_when:
  files_present:
    - "**/go.mod"
    - "**/cmd/*/main.go"
  files_contain:
    "**/go.mod": '(google\.golang\.org/grpc|go-chi/chi|labstack/echo|gin-gonic/gin)'
  language:
    - go
  frameworks:
    - grpc
    - chi
    - echo
    - gin
portability:
  level: universal
  tested_on:
    - claude-code
    - codex
  model_dependency: none
  domain_specificity: focused
produces:
  - code
  - service-boundary
consumes:
  - api-contract
  - service-boundary
security:
  signature: ""
  sandbox: read-only
  network: none
---

# Go 마이크로서비스 가이드

Go 기반 MSA 프로젝트 구조, 레이어드/헥사고날 아키텍처, 미들웨어 체인, DI 패턴, 운영 패턴

## Quick Reference (결정 트리)

```
프로젝트 규모별 구조 선택
    ├─ 소규모 (1-3 엔드포인트) ──> Flat 구조 (main.go + handler + store)
    ├─ 중규모 (단일 서비스) ────> Standard Layout (cmd/ + internal/)
    ├─ 대규모 (MSA 다수) ──────> 헥사고날 아키텍처 + DDD
    └─ 모노레포 (다중 서비스) ──> cmd/svc-a, cmd/svc-b + shared internal/

프레임워크 선택
    ├─ 표준 라이브러리 우선 ────> net/http + chi (경량, 호환성)
    ├─ 빠른 프로토타이핑 ──────> Gin / Echo
    ├─ 엔터프라이즈 MSA ───────> Go-Kit (transport/endpoint/service)
    └─ gRPC 중심 ──────────────> 직접 구현 + grpc-ecosystem 미들웨어

DI 방식 선택
    ├─ 서비스 5개 이하 ────────> 수동 주입 (main에서 직접 생성)
    ├─ 정적 그래프, 컴파일 안전 ─> Google Wire (코드 생성)
    └─ 동적 해결, 라이프사이클 ──> Uber Fx (런타임 리플렉션)
```

---

## 프로젝트 구조 (Standard Layout)

```
myservice/
├── cmd/myservice/main.go       # 엔트리포인트, 의존성 조립
├── internal/
│   ├── domain/                 # 도메인 모델, 비즈니스 규칙, 에러
│   ├── service/                # 비즈니스 로직 (Use Cases)
│   ├── repository/             # 데이터 접근 (인터페이스 + 구현체)
│   │   └── postgres/
│   ├── handler/                # HTTP/gRPC 핸들러, 라우터
│   ├── middleware/             # Auth, Logging, Recovery
│   └── config/                 # 설정 구조체, 로더
├── pkg/                        # 외부 공개 가능 유틸리티
├── api/v1/                     # proto, OpenAPI spec
├── configs/                    # 환경별 설정 파일 (yaml)
├── migrations/                 # DB 마이그레이션
└── deployments/                # Dockerfile, k8s manifests
```

| 디렉토리 | 역할 | 접근 범위 |
|----------|------|----------|
| `cmd/` | 엔트리포인트, 의존성 조립 | 외부 |
| `internal/` | 비즈니스 로직 (외부 import 차단) | 프로젝트 내부 전용 |
| `pkg/` | 재사용 가능 라이브러리 | 외부 공개 |
| `api/` | API 정의 (proto, OpenAPI) | 외부 |

---

## 레이어드 아키텍처 (Handler -> Service -> Repository)

```
Request -> Handler(HTTP 파싱/응답) -> Service(비즈니스 로직) -> Repository(데이터 접근)
           각 계층은 인터페이스로 연결, 의존성은 항상 안쪽으로
```

```go
// internal/domain/user.go -- 도메인 모델
type User struct {
    ID    string    `json:"id"`
    Email string    `json:"email"`
    Name  string    `json:"name"`
}

// internal/service/user_service.go -- 서비스 인터페이스
type UserService interface {
    GetByID(ctx context.Context, id string) (*domain.User, error)
    Create(ctx context.Context, cmd CreateUserCmd) (*domain.User, error)
}

// internal/repository/user_repository.go -- 저장소 인터페이스
type UserRepository interface {
    FindByID(ctx context.Context, id string) (*domain.User, error)
    Save(ctx context.Context, user *domain.User) error
}

// internal/service/user_service_impl.go -- 구현체
type userService struct {
    repo   repository.UserRepository
    logger *zap.Logger
}

func NewUserService(repo repository.UserRepository, logger *zap.Logger) UserService {
    return &userService{repo: repo, logger: logger}
}

func (s *userService) GetByID(ctx context.Context, id string) (*domain.User, error) {
    user, err := s.repo.FindByID(ctx, id)
    if err != nil {
        return nil, fmt.Errorf("get user %s: %w", id, err)
    }
    return user, nil
}
```

---

## 헥사고날 아키텍처 (Ports & Adapters)

```
어댑터(Inbound)      포트(Interface)      도메인 코어        포트(Interface)     어댑터(Outbound)
HTTP Handler   -->  Service IF    -->  Use Cases     -->  Repository IF  -->  PostgreSQL
gRPC Handler   -->                     Domain Model  -->  Event IF       -->  Kafka
```

```
internal/
├── domain/          # 도메인 코어 (외부 의존성 없음, 순수 Go)
├── port/
│   ├── inbound/     # 서비스 인터페이스
│   └── outbound/    # 저장소, 외부 서비스 인터페이스
├── app/             # 유스케이스 구현 (포트 인터페이스 구현)
└── adapter/
    ├── inbound/     # HTTP, gRPC 핸들러
    └── outbound/    # PostgreSQL, Redis, Kafka 구현체
```

핵심: 도메인은 외부 프레임워크에 의존하지 않음. 의존성 방향은 항상 어댑터 -> 포트 -> 도메인

---

## 미들웨어 체인

```go
type Middleware func(http.Handler) http.Handler

func Chain(h http.Handler, mws ...Middleware) http.Handler {
    for i := len(mws) - 1; i >= 0; i-- { h = mws[i](h) }
    return h
}

// Recovery: 패닉 복구
func RecoveryMiddleware(logger *zap.Logger) Middleware {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            defer func() {
                if err := recover(); err != nil {
                    logger.Error("panic", zap.Any("error", err),
                        zap.String("stack", string(debug.Stack())))
                    http.Error(w, "internal server error", 500)
                }
            }()
            next.ServeHTTP(w, r)
        })
    }
}

// Logging: 요청/응답 로깅
func LoggingMiddleware(logger *zap.Logger) Middleware {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            start := time.Now()
            ww := &responseWriter{ResponseWriter: w, statusCode: 200}
            next.ServeHTTP(ww, r)
            logger.Info("request",
                zap.String("method", r.Method), zap.String("path", r.URL.Path),
                zap.Int("status", ww.statusCode), zap.Duration("latency", time.Since(start)))
        })
    }
}

// 적용: handler := Chain(myHandler, RecoveryMW, TracingMW, LoggingMW, AuthMW)
```

```go
// gRPC 인터셉터 체인
server := grpc.NewServer(grpc.ChainUnaryInterceptor(
    recovery.UnaryServerInterceptor(),    // 1. 패닉 복구
    otelgrpc.UnaryServerInterceptor(),    // 2. 분산 추적
    logging.UnaryServerInterceptor(log),  // 3. 로깅
    auth.UnaryServerInterceptor(authFn),  // 4. 인증
    ratelimit.UnaryServerInterceptor(lm), // 5. 레이트리밋
))
```

| 순서 | 미들웨어 | 이유 |
|------|---------|------|
| 1 | Recovery | 패닉이 다른 미들웨어까지 전파 방지 |
| 2 | Tracing | 모든 처리에 trace ID 부여 |
| 3 | Logging | 요청/응답 기록 |
| 4 | Auth | 인증/인가 확인 |
| 5 | RateLimit | 과도한 요청 차단 |

---

## DI 패턴

### 수동 주입 (소규모 권장)

```go
func main() {
    db := postgres.NewConnection(cfg.DatabaseURL)
    userRepo := postgres.NewUserRepository(db)
    userSvc := service.NewUserService(userRepo, logger)
    userHandler := handler.NewUserHandler(userSvc, logger)
    // 명시적이고 추적 가능
}
```

### Google Wire (컴파일 타임)

```go
//go:build wireinject
package wire

func InitializeApp(cfg *config.Config) (*App, error) {
    wire.Build(
        postgres.NewConnection, postgres.NewUserRepository,
        service.NewUserService, handler.NewUserHandler, NewApp,
    )
    return nil, nil
}
// wire ./internal/wire/ -> wire_gen.go 생성
```

**장점**: 컴파일 타임 검증, 런타임 오버헤드 없음, 순환 의존성 감지
**단점**: 코드 생성 필요, 라이프사이클 관리 미지원

### Uber Fx (런타임)

```go
func main() {
    fx.New(
        fx.Provide(config.Load, zap.NewProduction, postgres.NewConnection,
            postgres.NewUserRepository, service.NewUserService, handler.NewUserHandler),
        fx.Invoke(startServer),
    ).Run()
}

func startServer(lc fx.Lifecycle, h *handler.UserHandler, logger *zap.Logger) {
    srv := &http.Server{Addr: ":8080", Handler: handler.SetupRouter(h)}
    lc.Append(fx.Hook{
        OnStart: func(ctx context.Context) error { go srv.ListenAndServe(); return nil },
        OnStop:  func(ctx context.Context) error { return srv.Shutdown(ctx) },
    })
}
```

**장점**: 라이프사이클 관리 내장, 동적 모듈 구성
**단점**: 런타임 리플렉션, 컴파일 타임 안전성 부족

---

## Configuration (Viper)

```go
type Config struct {
    Server   ServerConfig   `mapstructure:"server"`
    Database DatabaseConfig `mapstructure:"database"`
}
type ServerConfig struct {
    Port            int           `mapstructure:"port"`
    ShutdownTimeout time.Duration `mapstructure:"shutdown_timeout"`
}

func Load() (*Config, error) {
    v := viper.New()
    v.SetConfigName("config")
    v.AddConfigPath("./configs")
    v.SetEnvPrefix("APP")                                // APP_SERVER_PORT -> server.port
    v.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))
    v.AutomaticEnv()
    v.SetDefault("server.port", 8080)
    v.SetDefault("server.shutdown_timeout", "10s")
    if err := v.ReadInConfig(); err != nil {
        return nil, fmt.Errorf("read config: %w", err)
    }
    var cfg Config
    return &cfg, v.Unmarshal(&cfg)
}
```

```yaml
# configs/config.yaml
server:
  port: 8080
  shutdown_timeout: 10s
database:
  host: localhost
  port: 5432
  max_open_conns: 25
```

운영 전략: 기본 yaml + 환경 변수 오버라이드 (`APP_DATABASE_HOST=prod-db.internal`)

---

## Graceful Shutdown

```go
srv := &http.Server{Addr: ":8080", Handler: router}
go func() {
    if err := srv.ListenAndServe(); err != http.ErrServerClosed {
        logger.Fatal("server error", zap.Error(err))
    }
}()

quit := make(chan os.Signal, 1)
signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
<-quit
// 새 요청 중단 -> 진행 중 요청 완료 -> 리소스 정리
ctx, cancel := context.WithTimeout(context.Background(), cfg.Server.ShutdownTimeout)
defer cancel()
srv.Shutdown(ctx); db.Close(); logger.Sync()
```

Kubernetes 연동: SIGTERM 후 readiness false 전환, Pod grace period(30s)보다 짧은 timeout, `preStop: sleep 5`

---

## Health Check

```go
// Liveness: 프로세스 생존 확인 (실패 시 Pod 재시작)
func (h *HealthChecker) Liveness(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusOK)
    json.NewEncoder(w).Encode(map[string]string{"status": "alive"})
}

// Readiness: 트래픽 수신 준비 확인 (실패 시 Service에서 제외)
func (h *HealthChecker) Readiness(w http.ResponseWriter, r *http.Request) {
    ctx, cancel := context.WithTimeout(r.Context(), 2*time.Second)
    defer cancel()
    if err := h.db.PingContext(ctx); err != nil {
        w.WriteHeader(http.StatusServiceUnavailable)
        json.NewEncoder(w).Encode(map[string]string{"status": "not ready"})
        return
    }
    w.WriteHeader(http.StatusOK)
    json.NewEncoder(w).Encode(map[string]string{"status": "ready"})
}
```

```yaml
# Kubernetes probe 설정
livenessProbe:
  httpGet: { path: /healthz, port: 8080 }
  initialDelaySeconds: 5
  periodSeconds: 10
readinessProbe:
  httpGet: { path: /readyz, port: 8080 }
  initialDelaySeconds: 5
  periodSeconds: 5
```

---

## Error Handling

```go
// internal/domain/errors.go
var (
    ErrNotFound      = errors.New("resource not found")
    ErrAlreadyExists = errors.New("resource already exists")
    ErrUnauthorized  = errors.New("unauthorized")
    ErrForbidden     = errors.New("forbidden")
    ErrInvalidInput  = errors.New("invalid input")
)

type AppError struct {
    Code    string `json:"code"`
    Message string `json:"message"`
    Err     error  `json:"-"`
}
func (e *AppError) Error() string { return e.Message }
func (e *AppError) Unwrap() error { return e.Err }
```

### HTTP / gRPC 상태 코드 매핑

| 도메인 에러 | HTTP | gRPC |
|------------|------|------|
| `ErrNotFound` | 404 | `NotFound` |
| `ErrAlreadyExists` | 409 | `AlreadyExists` |
| `ErrUnauthorized` | 401 | `Unauthenticated` |
| `ErrForbidden` | 403 | `PermissionDenied` |
| `ErrInvalidInput` | 400 | `InvalidArgument` |
| 기타 | 500 | `Internal` |

```go
func mapErrorToHTTPStatus(err error) int {
    switch {
    case errors.Is(err, domain.ErrNotFound):      return http.StatusNotFound
    case errors.Is(err, domain.ErrAlreadyExists): return http.StatusConflict
    case errors.Is(err, domain.ErrUnauthorized):  return http.StatusUnauthorized
    case errors.Is(err, domain.ErrInvalidInput):  return http.StatusBadRequest
    default:                                       return http.StatusInternalServerError
    }
}
```

---

## 코드 예제: 서비스 Boilerplate

```go
// cmd/myservice/main.go
func main() {
    cfg, err := config.Load()
    if err != nil { panic(fmt.Sprintf("config: %v", err)) }
    logger, _ := zap.NewProduction()
    defer logger.Sync()
    db, err := postgres.NewConnection(cfg.Database)
    if err != nil { logger.Fatal("db failed", zap.Error(err)) }
    defer db.Close()

    // 의존성 조립
    userRepo := postgres.NewUserRepository(db)
    userSvc := service.NewUserService(userRepo, logger)
    userHandler := handler.NewUserHandler(userSvc, logger)

    // 라우터 + 미들웨어
    mux := http.NewServeMux()
    mux.HandleFunc("/healthz", handler.NewHealthChecker(db).Liveness)
    mux.HandleFunc("/readyz", handler.NewHealthChecker(db).Readiness)
    mux.Handle("/api/v1/", handler.SetupAPIRoutes(userHandler))
    wrapped := middleware.Chain(mux, middleware.Recovery(logger),
        middleware.RequestID(), middleware.Logging(logger))

    // 서버 시작 + graceful shutdown
    srv := &http.Server{Addr: fmt.Sprintf(":%d", cfg.Server.Port), Handler: wrapped}
    go func() { srv.ListenAndServe() }()
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit
    ctx, cancel := context.WithTimeout(context.Background(), cfg.Server.ShutdownTimeout)
    defer cancel()
    srv.Shutdown(ctx)
}
```

### Dockerfile (멀티스테이지)

```dockerfile
FROM golang:1.23-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /myservice ./cmd/myservice

FROM gcr.io/distroless/static-debian12
COPY --from=builder /myservice /myservice
COPY configs/ /configs/
EXPOSE 8080
ENTRYPOINT ["/myservice"]
```

---

## Anti-Patterns

| 실수 | 올바른 방법 | 이유 |
|------|------------|------|
| God Package (하나의 패키지에 모든 코드) | 도메인별 패키지 분리 | 유지보수성, 테스트 용이성 저하 |
| 순환 의존성 (a->b, b->a) | 인터페이스로 의존성 역전 | 컴파일 불가, 설계 결함 |
| `init()` 남용 (DB 연결, 전역 상태) | `main()`에서 명시적 초기화 | 테스트 어려움, 실행 순서 불명확 |
| 구현 측에서 인터페이스 정의 | 소비자 측에서 정의 | Go 암시적 인터페이스 활용 |
| `context.Background()` 남용 | 요청별 context 전파 | 타임아웃/취소 전파 불가 |
| 핸들러에 비즈니스 로직 | Service 계층으로 분리 | 재사용 불가, 테스트 어려움 |
| 전역 변수로 의존성 공유 | 생성자 주입 | 테스트 격리 불가, 경쟁 상태 |
| 에러 무시 `_ = fn()` | 에러 처리 + `%w` 래핑 | 조용한 실패, 디버깅 불가 |

---

## 체크리스트

- [ ] 구조: `cmd/`, `internal/`, `pkg/` 분리
- [ ] 의존성: 인터페이스 기반, 단방향 (Handler -> Service -> Repository)
- [ ] 설정: 환경 변수 오버라이드, 시크릿 미포함
- [ ] 에러: 도메인 에러 + `%w` 래핑 + HTTP/gRPC 코드 매핑
- [ ] 미들웨어: Recovery > Tracing > Logging > Auth > RateLimit
- [ ] Health: `/healthz` (liveness), `/readyz` (readiness)
- [ ] Shutdown: SIGTERM + 진행 중 요청 완료 대기
- [ ] Docker: 멀티스테이지 빌드, distroless 이미지
- [ ] 테스트: 인터페이스 mock, testcontainers

---

## 관련 Skills

- `/go-errors`, `/go-gin`, `/go-testing` -- Go 에러/프레임워크/테스트
- `/grpc` -- gRPC, Protocol Buffers
- `/msa-resilience` -- Circuit Breaker, Retry
- `/msa-observability` -- 분산 추적, 메트릭

## 참고 레퍼런스

- [go-food-delivery-microservices](https://github.com/mehdihadeli/go-food-delivery-microservices) -- DDD + CQRS + Event Sourcing + gRPC + OTel
- [go-hexagonal](https://github.com/RanchoCooper/go-hexagonal) -- Hexagonal + DDD 프레임워크
- [evrone/go-clean-template](https://github.com/evrone/go-clean-template) -- Clean Architecture 템플릿
- [todo-api-microservice-example](https://github.com/MarioCarrion/todo-api-microservice-example) -- DDD + Onion 튜토리얼
- [Three Dots Labs](https://threedots.tech/post/introducing-clean-architecture/) -- Go Clean Architecture 블로그
