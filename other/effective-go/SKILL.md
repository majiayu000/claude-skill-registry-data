---
name: effective-go
description: "Go 관용 패턴 결정 기준 — 인터페이스 설계, 에러 처리(wrapping), Functional Options, 동시성 기본기, Modern Go 문법. Use when Go 코드를 새로 설계하거나 idiomatic 한 구현 방식을 고를 때."
---

# Effective Go — 패턴 결정 가이드

Rob Pike의 Go Proverbs + Modern Go (1.21+) 기반 실전 결정 가이드.
"이 상황에서는 이 패턴을 써라" — 조건, 코드, 이유를 한 번에.

## Quick Reference — 결정 트리

```
동기화 방법 선택?
├── 고루틴 간 데이터 전달 ──────> Channel
├── 단순 공유 상태 보호 ────────> sync.Mutex
├── 읽기 80%+ ─────────────────> sync.RWMutex
├── 한 번만 초기화 ────────────> sync.Once
└── 여러 고루틴 에러 처리 ─────> errgroup

초기화 패턴 선택?
├── 파라미터 3개 미만 ──────────> 생성자 함수 NewXxx()
├── 선택적 옵션 필요 ──────────> Functional Options
└── 설정 구조체 ───────────────> Config struct

에러 처리 방법 선택?
├── 특정 에러 값 비교 ─────────> errors.Is()
├── 에러 타입 비교 ────────────> errors.As()
├── 컨텍스트 추가 ─────────────> fmt.Errorf("%w")
└── 패키지 경계 에러 ──────────> Sentinel error (var ErrXxx)

제네릭 사용?
├── 같은 로직, 타입만 다름 ────> Generics
├── 동작이 다름 ───────────────> Interface
└── 단순 유틸 ─────────────────> 복사 (10-20줄)
```

---

## CRITICAL: 인터페이스 설계

### Accept interfaces, return structs

파라미터는 interface, 반환은 concrete struct. 인터페이스는 소비자 패키지에 정의.

```go
// Bad — 생산자가 인터페이스 반환
func NewUserRepo(db *sql.DB) UserRepository { return &userRepo{db: db} }

// Good — struct 반환, 소비자가 인터페이스 정의
// producer (repo 패키지)
func NewUserRepo(db *sql.DB) *UserRepo { return &UserRepo{db: db} }
func (r *UserRepo) FindByID(ctx context.Context, id int64) (*User, error) { ... }

// consumer (service 패키지) — 필요한 것만 인터페이스로
type UserFinder interface {
    FindByID(ctx context.Context, id int64) (*User, error)
}
func NewService(finder UserFinder) *Service { return &Service{finder: finder} }
```

**이유**: 소비자가 인터페이스를 정의하면 불필요한 의존성이 없고 테스트 mock이 쉬움.

### The bigger the interface, the weaker the abstraction

인터페이스 메서드는 1-3개로 제한. io.Reader(1개), io.ReadWriter(2개)가 강력한 이유.

```go
// Bad — 거대 인터페이스 (mock 지옥)
type UserService interface {
    Create(ctx context.Context, u *User) error
    Update(ctx context.Context, u *User) error
    Delete(ctx context.Context, id int64) error
    FindByID(ctx context.Context, id int64) (*User, error)
    FindAll(ctx context.Context) ([]*User, error)
}

// Good — 작은 인터페이스 조합
type UserCreator interface { Create(ctx context.Context, u *User) error }
type UserFinder interface  { FindByID(ctx context.Context, id int64) (*User, error) }

type UserReadWriter interface {  // 필요하면 조합
    UserCreator
    UserFinder
}
```

### Make the zero value useful

선언 즉시 사용 가능하게 설계. sync.Mutex, bytes.Buffer가 대표 예시.

```go
// Good — zero value가 유효
type Counter struct {
    mu    sync.Mutex  // zero value = unlocked
    count int         // zero value = 0
}
var c Counter  // 즉시 사용 가능

// Bad — map의 zero value는 nil (panic!)
type Registry struct { items map[string]Item }

// Good — lazy init으로 zero value 보완
func (r *Registry) Add(key string, item Item) {
    if r.items == nil { r.items = make(map[string]Item) }
    r.items[key] = item
}
```

---

## CRITICAL: 에러 처리

### Errors are values — 에러를 프로그래밍 가능한 값으로

```go
// Sentinel errors — 패키지 경계에서 사용
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
)

// Custom error type — 추가 정보 필요 시
type ValidationError struct {
    Field   string
    Message string
}
func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation: %s — %s", e.Field, e.Message)
}
```

### Error wrapping — 컨텍스트를 항상 추가

```go
// Bad — 컨텍스트 없음
if err != nil { return err }

// Good — 실패 지점을 명확히
if err != nil {
    return fmt.Errorf("get user %d: %w", userID, err)
}
```

### errors.Is() / errors.As() — 에러 비교

```go
// errors.Is: sentinel 비교
if errors.Is(err, ErrNotFound) {
    return nil, status.Error(codes.NotFound, "user not found")
}

// errors.As: 타입 비교
var valErr *ValidationError
if errors.As(err, &valErr) {
    log.Printf("field=%s msg=%s", valErr.Field, valErr.Message)
}
```

### Don't panic — 라이브러리에서 panic 절대 금지

```go
// Bad — 라이브러리에서 panic (호출자가 복구 불가)
func MustParse(s string) *Config {
    c, err := Parse(s)
    if err != nil { panic(err) }
    return c
}

// Good — 에러 반환
func Parse(s string) (*Config, error) { ... }

// Must는 main/init에서만 허용
func must[T any](v T, err error) T {
    if err != nil { panic(err) }
    return v
}
```

---

## 동시성 패턴

### Channel vs Mutex — 사용 상황 비교

| 상황 | Channel | Mutex |
|------|---------|-------|
| 데이터 전달 (파이프라인) | **적합** | 부적합 |
| 소유권 이전 | **적합** | 부적합 |
| 고루틴 조율 (fan-out/fan-in) | **적합** | 부적합 |
| 단순 카운터/캐시 보호 | 과도함 | **적합** |
| 읽기 80%+ 쓰기 20%- | 과도함 | **RWMutex** |

### Context propagation — 항상 첫 번째 파라미터

```go
// Bad — struct에 context 저장
type Server struct {
    ctx context.Context  // 절대 금지! context는 요청 스코프
}

// Good — 함수 첫 번째 파라미터로 전달
func (s *Server) HandleRequest(ctx context.Context, req *Request) error {
    ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()
    return s.repo.FindByID(ctx, req.ID)
}
```

**규칙**: ctx는 저장하지 말고 흘려보내라. WithTimeout/WithCancel로 파생.

### Worker Pool 패턴

```go
func processItems(ctx context.Context, items []Item, workers int) error {
    g, ctx := errgroup.WithContext(ctx)
    ch := make(chan Item)

    g.Go(func() error {  // Producer
        defer close(ch)
        for _, item := range items {
            select {
            case ch <- item:
            case <-ctx.Done():
                return ctx.Err()
            }
        }
        return nil
    })

    for i := 0; i < workers; i++ {  // Workers
        g.Go(func() error {
            for item := range ch {
                if err := process(ctx, item); err != nil {
                    return err  // 하나 실패 → 전체 취소
                }
            }
            return nil
        })
    }
    return g.Wait()
}
```

### errgroup — 여러 고루틴의 에러를 하나로

```go
func fetchAll(ctx context.Context, urls []string) ([]Result, error) {
    g, ctx := errgroup.WithContext(ctx)
    results := make([]Result, len(urls))

    for i, url := range urls {
        g.Go(func() error {
            res, err := fetch(ctx, url)
            if err != nil { return fmt.Errorf("fetch %s: %w", url, err) }
            results[i] = res  // 각 고루틴이 고유 인덱스 → 안전
            return nil
        })
    }
    if err := g.Wait(); err != nil { return nil, err }
    return results, nil
}
```

---

## Functional Options Pattern

조건: 선택적 파라미터 3개 이상, 하위 호환성 필요, 설정이 늘어날 가능성.

```go
type Server struct {
    addr     string
    timeout  time.Duration
    maxConns int
    logger   *slog.Logger
}

type Option func(*Server)

func WithTimeout(d time.Duration) Option { return func(s *Server) { s.timeout = d } }
func WithMaxConns(n int) Option          { return func(s *Server) { s.maxConns = n } }
func WithLogger(l *slog.Logger) Option   { return func(s *Server) { s.logger = l } }

func NewServer(addr string, opts ...Option) *Server {
    s := &Server{
        addr: addr, timeout: 30 * time.Second,
        maxConns: 100, logger: slog.Default(),
    }
    for _, opt := range opts { opt(s) }
    return s
}

// 사용
srv := NewServer(":8080", WithTimeout(10*time.Second), WithMaxConns(500))
```

**언제 쓰지 않나**: 필수 파라미터만 있으면 `NewXxx(필수값들)` 생성자가 단순하고 명확.

---

## Modern Go (1.21+)

### Generics — 같은 로직, 타입만 다를 때만

```go
// Good — 타입만 다르고 로직 동일
func Map[T, U any](s []T, f func(T) U) []U {
    result := make([]U, len(s))
    for i, v := range s { result[i] = f(v) }
    return result
}

// Bad — interface면 충분한데 generic 남용
func PrintAll[T fmt.Stringer](items []T) {  // Stringer 인터페이스로 충분
    for _, item := range items { fmt.Println(item.String()) }
}
```

**규칙**: "이 함수가 타입 파라미터 없이 작성 가능한가?" → 가능하면 generic 불필요.

### Structured Logging (slog)

```go
// Good — slog 구조화 로깅
logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    Level: slog.LevelInfo,
}))
logger.Info("request processed",
    slog.String("method", r.Method),
    slog.String("path", r.URL.Path),
    slog.Int("status", statusCode),
    slog.Duration("latency", elapsed),
)

// Bad — 파싱 불가능한 비구조화 로깅
log.Printf("request: method=%s path=%s status=%d", r.Method, r.URL.Path, code)
```

### Range over func (Go 1.23+)

```go
// Iterator 패턴 — 컬렉션 순회를 함수로 추상화
func (db *DB) Users(ctx context.Context) iter.Seq2[*User, error] {
    return func(yield func(*User, error) bool) {
        rows, err := db.QueryContext(ctx, "SELECT id, name FROM users")
        if err != nil { yield(nil, err); return }
        defer rows.Close()
        for rows.Next() {
            var u User
            if err := rows.Scan(&u.ID, &u.Name); err != nil {
                if !yield(nil, err) { return }
                continue
            }
            if !yield(&u, nil) { return }
        }
    }
}

// 사용 — range로 자연스럽게 순회
for user, err := range db.Users(ctx) {
    if err != nil { return err }
    fmt.Println(user.Name)
}
```

### A little copying > a little dependency

10-20줄 유틸은 복사가 의존성 추가보다 낫다.

```go
// Good — 간단한 유틸은 복사 (또는 slices.Contains 사용, 1.21+)
func contains[T comparable](s []T, v T) bool {
    for _, item := range s {
        if item == v { return true }
    }
    return false
}

// Bad — 작은 유틸 하나 때문에 외부 라이브러리 의존
import "github.com/samber/lo"  // lo.Contains(s, v)
```

---

## 코드 스타일

### Clear is better than clever

```go
// Bad — 한 줄에 모든 것 (clever)
return resp != nil && resp.StatusCode >= 200 && resp.StatusCode < 300 && resp.Body != nil

// Good — 의도가 명확 (clear)
func isSuccessResponse(resp *http.Response) bool {
    if resp == nil { return false }
    return resp.StatusCode >= 200 && resp.StatusCode < 300
}
```

### Early return (Guard Clause)

```go
// Bad — 중첩
func process(order *Order) error {
    if order != nil {
        if order.IsValid() {
            return execute(order)
        }
        return errors.New("invalid order")
    }
    return errors.New("nil order")
}

// Good — guard clause로 일찍 탈출
func process(order *Order) error {
    if order == nil { return errors.New("nil order") }
    if !order.IsValid() { return errors.New("invalid order") }
    return execute(order)
}
```

### 변수 이름 — 스코프가 좁을수록 짧게

```go
for i, v := range items { ... }    // 좁은 스코프 → 짧은 이름
for k, v := range m { ... }

var userRepository *UserRepo        // 넓은 스코프 → 설명적 이름
var requestTimeout time.Duration
```

### godoc 주석 — 함수명으로 시작

```go
// FindByID returns the user with the given ID.
// It returns ErrNotFound if no user exists.
func (r *UserRepo) FindByID(ctx context.Context, id int64) (*User, error) {
```

---

## Anti-Patterns

| 실수 | 해결 | 이유 |
|------|------|------|
| `interface{}` 남용 | 구체 타입 또는 제네릭 | 타입 안전성 상실 |
| struct에 context 저장 | 함수 파라미터로 전달 | context는 요청 스코프 |
| init() 남용 | 명시적 초기화 함수 | 테스트/순서 제어 어려움 |
| goroutine leak | `defer cancel()` + select | 메모리 누수 |
| `panic` in library | `error` 반환 | 호출자가 복구 불가 |
| named return 남용 | 명시적 return | 가독성 저하, shadowing |
| 거대 인터페이스 | 1-3 메서드 인터페이스 | mock 지옥 |
| `sync.Map` 범용 사용 | `map` + `sync.RWMutex` | 특수 케이스에만 유리 |
| error 문자열 비교 | `errors.Is()` / `errors.As()` | 리팩토링에 취약 |
| channel 과다 사용 | 단순하면 mutex | 불필요한 복잡도 |
| `time.Sleep` 동기화 | `sync.WaitGroup` / channel | 불안정, 느림 |
| 패키지 순환 참조 | interface로 의존 역전 | 컴파일 에러 |

---

## 체크리스트

### 새 패키지 작성 시

- [ ] zero value가 유용한가?
- [ ] 인터페이스가 소비자 측에 정의되었는가?
- [ ] 에러에 컨텍스트가 포함되었는가?
- [ ] context가 첫 번째 파라미터인가?
- [ ] goroutine이 정리되는가? (defer cancel)
- [ ] godoc 주석이 함수명으로 시작하는가?

### 코드 리뷰 시

- [ ] 중첩 3단계 이하인가? (guard clause 적용)
- [ ] 인터페이스 메서드 3개 이하인가?
- [ ] `go test -race ./...` 통과?
- [ ] sentinel error에 `Err` 접두사 사용?

---

## 관련 Skills

- `/go:concurrency-go` — 동시성 심화 (Race Detector, Distributed Lock)
- `/go:go-testing` — 테스트 패턴, 테이블 드리븐 테스트
- `/go:go-microservice` — MSA 구조, Clean Architecture
- `/go:go-database` — pgx, sqlc, sqlx, ent, bun 패턴

## 참고 레퍼런스

- [Go Proverbs](https://go-proverbs.github.io/) — Rob Pike의 Go 설계 철학
- [Effective Go](https://go.dev/doc/effective_go) — 공식 가이드
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments) — 코드 리뷰 체크리스트
- [Uber Go Style Guide](https://github.com/uber-go/guide/blob/master/style.md) — 실전 스타일 가이드
