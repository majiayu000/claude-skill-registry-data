---
name: go-performance
description: "Go 고성능 패턴 — sync.Pool 오브젝트 풀링, zero-allocation 기법, GC 튜닝(GOGC/GOMEMLIMIT), DB·HTTP 커넥션 관리, Graceful Shutdown, pprof 프로파일링 명령, Circuit Breaker, 대용량 트래픽 Performance Target. Use when Go 서비스의 지연·메모리·GC·커넥션 병목을 잡거나 pprof 로 프로파일링할 때."
---

# Go 고성능 / 프로파일링

동시성 기본기(Worker Pool, Mutex vs Channel, errgroup)는 [`effective-go`](../effective-go/SKILL.md) / [`concurrency-go`](../concurrency-go/SKILL.md),
Circuit Breaker·Retry·Bulkhead 설계는 `/architecture:msa-resilience` 참조. 여기서는 **측정과 튜닝**을 다룬다.

## High-Traffic Patterns

### Worker Pool (Production-Grade)

```go
// ❌ BAD: Unbounded goroutines (OOM risk)
for _, job := range jobs {
    go process(job)  // 수백만 goroutine 생성
}

// ✅ GOOD: Bounded worker pool with backpressure
type WorkerPool struct {
    jobs    chan Job
    results chan Result
    wg      sync.WaitGroup
}

func NewWorkerPool(workers, queueSize int) *WorkerPool {
    pool := &WorkerPool{
        jobs:    make(chan Job, queueSize),
        results: make(chan Result, queueSize),
    }
    for i := 0; i < workers; i++ {
        pool.wg.Add(1)
        go pool.worker()
    }
    return pool
}

func (p *WorkerPool) worker() {
    defer p.wg.Done()
    for job := range p.jobs {
        result := process(job)
        select {
        case p.results <- result:
        default:
            metrics.Increment("worker.overflow")  // Backpressure
        }
    }
}

func (p *WorkerPool) Submit(ctx context.Context, job Job) error {
    select {
    case p.jobs <- job:
        return nil
    case <-ctx.Done():
        return ctx.Err()
    default:
        return ErrPoolFull  // Rate limiting
    }
}
```

### Fan-Out/Fan-In

```go
// Fan-out: 작업 분배
func FanOut(ctx context.Context, input <-chan Request, workers int) []<-chan Response {
    outputs := make([]<-chan Response, workers)
    for i := 0; i < workers; i++ {
        outputs[i] = worker(ctx, input)
    }
    return outputs
}

// Fan-in: 결과 병합
func FanIn(ctx context.Context, channels ...<-chan Response) <-chan Response {
    merged := make(chan Response)
    var wg sync.WaitGroup

    for _, ch := range channels {
        wg.Add(1)
        go func(c <-chan Response) {
            defer wg.Done()
            for resp := range c {
                select {
                case merged <- resp:
                case <-ctx.Done():
                    return
                }
            }
        }(ch)
    }

    go func() { wg.Wait(); close(merged) }()
    return merged
}
```

### Rate Limiting

```go
import "golang.org/x/time/rate"

type RateLimiter struct {
    clients sync.Map
    rate    rate.Limit
    burst   int
}

func (rl *RateLimiter) Allow(clientID string) bool {
    limiter, _ := rl.clients.LoadOrStore(clientID, rate.NewLimiter(rl.rate, rl.burst))
    return limiter.(*rate.Limiter).Allow()
}

// Middleware
func RateLimitMiddleware(rl *RateLimiter) gin.HandlerFunc {
    return func(c *gin.Context) {
        if !rl.Allow(c.ClientIP()) {
            c.AbortWithStatusJSON(429, gin.H{"error": "rate limit exceeded"})
            return
        }
        c.Next()
    }
}
```

### Circuit Breaker

```go
import "github.com/sony/gobreaker"

var cb = gobreaker.NewCircuitBreaker(gobreaker.Settings{
    Name:        "payment-service",
    MaxRequests: 3,                // Half-open state
    Interval:    10 * time.Second,
    Timeout:     30 * time.Second, // Open → Half-open
    ReadyToTrip: func(counts gobreaker.Counts) bool {
        return counts.Requests >= 10 && float64(counts.TotalFailures)/float64(counts.Requests) >= 0.5
    },
})

func CallPaymentService(ctx context.Context, req *PaymentRequest) (*PaymentResponse, error) {
    result, err := cb.Execute(func() (interface{}, error) {
        return paymentClient.Process(ctx, req)
    })
    if err != nil { return nil, err }
    return result.(*PaymentResponse), nil
}
```

## Memory Optimization

### Object Pooling (sync.Pool)

```go
// ❌ BAD: 매 요청마다 할당
func handleRequest(w http.ResponseWriter, r *http.Request) {
    buf := make([]byte, 64*1024)  // GC 압박
}

// ✅ GOOD: sync.Pool로 재사용
var bufferPool = sync.Pool{
    New: func() interface{} { return make([]byte, 64*1024) },
}

func handleRequest(w http.ResponseWriter, r *http.Request) {
    buf := bufferPool.Get().([]byte)
    defer bufferPool.Put(buf)
    buf = buf[:0]  // Reset
    // use buf...
}
```

### Zero-Allocation Patterns

```go
// ❌ BAD: String concat allocates
func buildKey(prefix, id string) string {
    return prefix + ":" + id
}

// ✅ GOOD: strings.Builder
func buildKey(prefix, id string) string {
    var b strings.Builder
    b.Grow(len(prefix) + 1 + len(id))
    b.WriteString(prefix)
    b.WriteByte(':')
    b.WriteString(id)
    return b.String()
}

// Escape analysis 확인
// go build -gcflags="-m" ./...
```

## Connection Management

### Database

```go
func NewDB(dsn string) (*sql.DB, error) {
    db, err := sql.Open("postgres", dsn)
    if err != nil { return nil, err }

    db.SetMaxOpenConns(100)
    db.SetMaxIdleConns(25)               // 25% of max
    db.SetConnMaxLifetime(5 * time.Minute)
    db.SetConnMaxIdleTime(1 * time.Minute)
    return db, nil
}
```

### HTTP Client

```go
// ❌ BAD: Default client (no pool control)
resp, err := http.Get(url)

// ✅ GOOD: Configured transport
var httpClient = &http.Client{
    Transport: &http.Transport{
        MaxIdleConns:        100,
        MaxIdleConnsPerHost: 100,
        MaxConnsPerHost:     100,
        IdleConnTimeout:     90 * time.Second,
        ForceAttemptHTTP2:   true,
    },
    Timeout: 30 * time.Second,
}
```

## Graceful Shutdown

```go
func main() {
    srv := &http.Server{
        Addr:         ":8080",
        Handler:      router,
        ReadTimeout:  5 * time.Second,
        WriteTimeout: 10 * time.Second,
    }

    go func() {
        if err := srv.ListenAndServe(); err != http.ErrServerClosed {
            log.Fatalf("Server error: %v", err)
        }
    }()

    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    if err := srv.Shutdown(ctx); err != nil {
        log.Fatalf("Forced shutdown: %v", err)
    }
}
```

## Profiling Commands

```bash
# CPU profiling
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30

# Memory profiling
go tool pprof http://localhost:6060/debug/pprof/heap

# Goroutine leak detection
go tool pprof http://localhost:6060/debug/pprof/goroutine

# Execution trace
curl -o trace.out http://localhost:6060/debug/pprof/trace?seconds=5
go tool trace trace.out

# Race detector
go test -race ./...
```

## Anti-Patterns

| Anti-Pattern | 문제 | 해결 |
|-------------|------|------|
| `for item := range items { go process(item) }` | OOM | Worker Pool |
| `func DoWork() error { return longOperation() }` | Context 없음 | `ctx` 첫 파라미터 |
| `var cache = map[string]string{}` | Race condition | `sync.Map` or `RWMutex` |
| `var mu sync.Mutex` in hot path | 병목 | Sharding or lock-free |
| `client := &http.Client{}` per request | 커넥션 누수 | 패키지 레벨 재사용 |
| `log.Error(err); return err` | 중복 로그 | Handle OR Return |

## Performance Targets

| 메트릭 | 목표 | 경고 |
|--------|------|------|
| P50 Latency | < 10ms | > 20ms |
| P99 Latency | < 100ms | > 200ms |
| Goroutine Count | < 10,000 | > 50,000 |
| Heap Alloc | Stable | > 20% growth/min |
| GC Pause | < 1ms | > 5ms |

## Error Handling + OTel 통합

### Handle OR Return 원칙 (Dave Cheney)

에러를 로깅하는 것은 에러를 처리하는 것이다. **로깅했으면 반환하지 말고, 반환했으면 로깅하지 말라.**

```go
// ❌ BAD: log AND return — 모든 레이어에서 중복 로그 발생
func (s *Service) GetUser(ctx context.Context, id string) (*User, error) {
    user, err := s.repo.Find(ctx, id)
    if err != nil {
        slog.Error("failed to find user", "error", err)  // 여기서 로깅
        return nil, fmt.Errorf("find user: %w", err)      // 또 반환 → 상위에서도 로깅
    }
    return user, nil
}

// ✅ GOOD: 각 레이어는 wrap + return만. 로깅은 최상위 핸들러에서만.
// Repo: return nil, fmt.Errorf("querying user %s: %w", id, err)
// Service: return nil, fmt.Errorf("getting user: %w", err)   ← wrap만, 로깅 X
// Handler (경계): 로깅 + OTel 기록 ↓
func (h *Handler) GetUser(w http.ResponseWriter, r *http.Request) {
    user, err := h.svc.GetUser(r.Context(), chi.URLParam(r, "id"))
    if err != nil {
        span := trace.SpanFromContext(r.Context())
        span.RecordError(err)
        span.SetStatus(codes.Error, "get user failed")
        slog.Error("get user failed", "error", err, "user_id", chi.URLParam(r, "id"))
        http.Error(w, "internal error", http.StatusInternalServerError)
        return
    }
    // 결과: 로그 1줄에 전체 컨텍스트 체인
    // "get user failed: error=getting user: querying user abc123: sql: no rows"
}
```

### OTel Span에 에러 기록

```go
// span.RecordError()는 상태를 변경하지 않음 — 반드시 SetStatus()도 호출
func (s *Service) ProcessOrder(ctx context.Context, req OrderRequest) error {
    ctx, span := tracer.Start(ctx, "Service.ProcessOrder")
    defer span.End()

    if err := s.validate(ctx, req); err != nil {
        span.RecordError(err)                           // 에러 이벤트 기록
        span.SetStatus(codes.Error, "validation failed") // 스팬 실패 표시
        return fmt.Errorf("validating order: %w", err)
    }

    // 성공적으로 재시도된 에러 — 스팬 실패가 아님
    if err := s.callPayment(ctx, req); err != nil {
        span.RecordError(err)  // 가시성을 위해 기록만
        // SetStatus 호출 안 함 — 재시도로 복구됨
        slog.Warn("payment retry", "error", err)
    }

    return nil
}
```

### 에러 타입 선택 가이드

| 패턴 | 용도 | 예시 |
|------|------|------|
| Sentinel Error | 잘 알려진 조건 분기 | `var ErrNotFound = errors.New("not found")` |
| Custom Error Type | 구조화된 데이터 전달 (HTTP 상태 매핑) | `type ValidationError struct { Field, Message string }` |
| `fmt.Errorf %w` | 컨텍스트 추가 전파 (기본값) | `fmt.Errorf("create order %s: %w", id, err)` |
| `errors.Join` | 독립적 에러 수집 (fan-out, validation) | `errors.Join(err1, err2, err3)` |

```go
// Sentinel Error — 호출자가 분기할 때
var ErrNotFound = errors.New("not found")
// 호출: if errors.Is(err, ErrNotFound) { ... }

// Custom Error Type — HTTP 상태 매핑이 필요할 때
type AppError struct {
    Code    int    // HTTP status code
    Message string // 사용자 노출용
    Err     error  // 원본 에러 (내부용)
}
func (e *AppError) Error() string { return e.Message }
func (e *AppError) Unwrap() error { return e.Err }
// 호출: var appErr *AppError; if errors.As(err, &appErr) { w.WriteHeader(appErr.Code) }

// errors.Join — 여러 goroutine 결과 수집
func validateAll(items []Item) error {
    var errs []error
    for _, item := range items {
        if err := validate(item); err != nil {
            errs = append(errs, err)
        }
    }
    return errors.Join(errs...)  // nil if no errors
}
```

## 체크리스트

### Concurrency
- [ ] goroutine 누수 없음 (context 취소 전파)
- [ ] channel 버퍼 크기 근거 있음
- [ ] `-race` 로 검증했는가

### Memory
- [ ] 핫 패스에 `sync.Pool` 적용 검토
- [ ] slice/map 사전 할당(`make(..., n)`)
- [ ] `GOMEMLIMIT` 을 컨테이너 메모리 한도에 맞췄는가

### Connections
- [ ] `SetMaxOpenConns` / `SetMaxIdleConns` / `SetConnMaxLifetime` 명시
- [ ] HTTP client 를 재사용하는가 (요청마다 생성 금지)
- [ ] Graceful Shutdown 에서 in-flight 요청을 기다리는가

## 참조 스킬

- [`effective-go`](../effective-go/SKILL.md) — 인터페이스 / 에러 / 동시성 관용구
- [`concurrency-go`](../concurrency-go/SKILL.md) — Mutex / Channel / Race Detector
- [`go-microservice`](../go-microservice/SKILL.md) — 프로젝트 구조 / Graceful Shutdown / Health Check
- `/architecture:msa-resilience` — Circuit Breaker / Retry / Bulkhead 설계
- `/observability:observability-pyroscope` — 상시 프로파일링
- [`go-security`](../go-security/SKILL.md) — Go 보안 리뷰 체크리스트
