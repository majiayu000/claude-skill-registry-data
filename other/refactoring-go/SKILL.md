---
name: refactoring-go
description: "Go 리팩토링 — Early Return, 함수·인터페이스 추출, 의존성 주입, 에러 처리 개선, goroutine·channel 정리. Use when 동작을 유지한 채 Go 코드의 복잡도를 줄이거나 구조를 개선할 때."
---

# Go Refactoring Patterns

Go 코드 리팩토링 패턴 및 best practices.

## Quick Reference

```
Go 리팩토링 패턴
    │
    ├─ 중첩 깊음 ──────────> Early Return Pattern
    │
    ├─ 함수 20줄+ ─────────> Extract Function
    │
    ├─ 테스트 어려움 ──────> Interface 추출
    │
    ├─ 전역 의존성 ────────> 의존성 주입
    │
    └─ 성능 이슈 ──────────> 슬라이스/문자열 최적화
```

---

## CRITICAL: 리팩토링 전 준비

| 단계 | 체크 |
|------|------|
| 테스트 존재 | `go test ./...` 통과 확인 |
| 커버리지 확인 | `go test -cover ./...` |
| 린트 통과 | `golangci-lint run` |
| 작은 커밋 | 하나의 리팩토링 = 하나의 커밋 |

---

## Early Return Pattern

### 중첩 제거 (Guard Clause)

```go
// Before: 4단계 중첩 (Pyramid of Doom)
func ProcessOrder(order *Order) error {
    if order != nil {
        if order.Items != nil {
            if len(order.Items) > 0 {
                if order.Status == "pending" {
                    // 실제 로직 (들여쓰기 4단계)
                    return processItems(order)
                }
            }
        }
    }
    return errors.New("invalid order")
}

// After: Guard Clause로 평탄화
func ProcessOrder(order *Order) error {
    if order == nil {
        return errors.New("order is nil")
    }
    if order.Items == nil {
        return errors.New("order items is nil")
    }
    if len(order.Items) == 0 {
        return errors.New("order has no items")
    }
    if order.Status != "pending" {
        return errors.New("order is not pending")
    }

    // 실제 로직 (들여쓰기 0단계)
    return processItems(order)
}
```

### 에러 핸들링 Early Return

```go
// Before: else 사용
func GetUser(id int) (*User, error) {
    user, err := repo.FindByID(id)
    if err != nil {
        return nil, err
    } else {
        if user.IsActive {
            return user, nil
        } else {
            return nil, ErrUserInactive
        }
    }
}

// After: Early Return
func GetUser(id int) (*User, error) {
    user, err := repo.FindByID(id)
    if err != nil {
        return nil, fmt.Errorf("find user: %w", err)
    }
    if !user.IsActive {
        return nil, ErrUserInactive
    }
    return user, nil
}
```

---

## 함수 추출 (Extract Function)

### 20줄 초과 시 분리

```go
// Before: 긴 함수 (유효성 검증 + 재고 확인 + 주문 생성)
func CreateOrder(req CreateOrderRequest) (*Order, error) {
    // 50줄+ 로직...
}

// After: 책임별 함수 추출
func CreateOrder(req CreateOrderRequest) (*Order, error) {
    if err := validateOrderRequest(req); err != nil {
        return nil, fmt.Errorf("validate: %w", err)
    }
    if err := checkInventory(req.Items); err != nil {
        return nil, fmt.Errorf("inventory: %w", err)
    }
    return buildOrder(req)
}

func validateOrderRequest(req CreateOrderRequest) error {
    if req.UserID == 0 {
        return errors.New("user id required")
    }
    if len(req.Items) == 0 {
        return errors.New("items required")
    }
    return nil
}
```

---

## 인터페이스 추출

### 테스트 가능성 향상

```go
// Before: 구체 타입 직접 의존 (테스트 불가)
type UserService struct {
    db *sql.DB
}

func (s *UserService) GetUser(ctx context.Context, id int) (*User, error) {
    row := s.db.QueryRowContext(ctx, "SELECT * FROM users WHERE id = ?", id)
    // 실제 DB 연결 필요
}

// After: 인터페이스 의존 (Mock 가능)
type UserRepository interface {
    FindByID(ctx context.Context, id int) (*User, error)
    Save(ctx context.Context, user *User) error
}

type UserService struct {
    repo UserRepository
}

func NewUserService(repo UserRepository) *UserService {
    return &UserService{repo: repo}
}

func (s *UserService) GetUser(ctx context.Context, id int) (*User, error) {
    return s.repo.FindByID(ctx, id)
}
```

### Mock 테스트

```go
// 테스트용 Mock
type mockUserRepo struct {
    users map[int]*User
}

func (m *mockUserRepo) FindByID(ctx context.Context, id int) (*User, error) {
    if user, ok := m.users[id]; ok {
        return user, nil
    }
    return nil, ErrUserNotFound
}

func TestGetUser(t *testing.T) {
    repo := &mockUserRepo{
        users: map[int]*User{1: {ID: 1, Name: "Alice"}},
    }
    svc := NewUserService(repo)

    user, err := svc.GetUser(context.Background(), 1)
    assert.NoError(t, err)
    assert.Equal(t, "Alice", user.Name)
}
```

---

## 의존성 주입 리팩토링

### 전역변수 → 구조체 주입

```go
// Before: 전역 변수 의존 (테스트 어려움)
var db *sql.DB
var cache *redis.Client
var logger *zap.Logger

func GetProduct(id int) (*Product, error) {
    logger.Info("getting product", zap.Int("id", id))

    cached, err := cache.Get(ctx, fmt.Sprintf("product:%d", id)).Result()
    if err == nil {
        return unmarshal(cached)
    }

    return queryFromDB(db, id)
}

// After: 구조체로 의존성 주입
type ProductService struct {
    db     *sql.DB
    cache  *redis.Client
    logger *zap.Logger
}

func NewProductService(db *sql.DB, cache *redis.Client, logger *zap.Logger) *ProductService {
    return &ProductService{db: db, cache: cache, logger: logger}
}

func (s *ProductService) GetProduct(ctx context.Context, id int) (*Product, error) {
    s.logger.Info("getting product", zap.Int("id", id))
    // ...
}
```

### Functional Options Pattern

```go
type ServerOption func(*Server)

func WithTimeout(d time.Duration) ServerOption {
    return func(s *Server) {
        s.timeout = d
    }
}

func WithLogger(l *zap.Logger) ServerOption {
    return func(s *Server) {
        s.logger = l
    }
}

func NewServer(addr string, opts ...ServerOption) *Server {
    s := &Server{
        addr:    addr,
        timeout: 30 * time.Second,  // 기본값
        logger:  zap.NewNop(),      // 기본값
    }
    for _, opt := range opts {
        opt(s)
    }
    return s
}

// 사용
server := NewServer(":8080",
    WithTimeout(60*time.Second),
    WithLogger(logger),
)
```

---

## 에러 처리 개선

### 에러 래핑 전환

```go
// Before: 컨텍스트 없는 에러
func ProcessOrder(orderID int) error {
    order, err := getOrder(orderID)
    if err != nil {
        return err  // 어디서 발생했는지 모름
    }
    return nil
}

// After: 컨텍스트가 있는 에러 래핑
func ProcessOrder(orderID int) error {
    order, err := getOrder(orderID)
    if err != nil {
        return fmt.Errorf("get order %d: %w", orderID, err)
    }
    return nil
}
```

### Custom Error Type 전환

```go
// Before: 문자열 에러
if product.Stock < quantity {
    return errors.New("insufficient stock")
}

// After: Custom Error Type
type InsufficientStockError struct {
    ProductID int
    Available int
    Requested int
}

func (e *InsufficientStockError) Error() string {
    return fmt.Sprintf("insufficient stock for product %d: available %d, requested %d",
        e.ProductID, e.Available, e.Requested)
}

if product.Stock < quantity {
    return &InsufficientStockError{
        ProductID: product.ID,
        Available: product.Stock,
        Requested: quantity,
    }
}
```

---

## 고루틴/채널 리팩토링

### Mutex vs Channel 선택

| 상황 | 선택 |
|------|------|
| 단순 카운터/상태 보호 | `sync.Mutex` |
| 복잡한 동기화/통신 | Channel |
| 작업 분배 | Worker Pool (`/go:concurrency-go`) |

```go
// Mutex: 단순 상태 보호
type Counter struct {
    mu    sync.Mutex
    value int
}

func (c *Counter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.value++
}
```

자세한 패턴은 `/go:concurrency-go` 참조.

---

## 성능 최적화 리팩토링

### 슬라이스 사전할당

```go
// Before: 동적 확장 (재할당 발생)
func collectIDs(users []User) []int {
    var ids []int
    for _, u := range users {
        ids = append(ids, u.ID)
    }
    return ids
}

// After: 사전할당
func collectIDs(users []User) []int {
    ids := make([]int, 0, len(users))
    for _, u := range users {
        ids = append(ids, u.ID)
    }
    return ids
}
```

### strings.Builder 사용

```go
// Before: 문자열 연결 (O(n²))
func buildReport(items []Item) string {
    result := ""
    for _, item := range items {
        result += fmt.Sprintf("- %s: %d\n", item.Name, item.Price)
    }
    return result
}

// After: strings.Builder (O(n))
func buildReport(items []Item) string {
    var sb strings.Builder
    sb.Grow(len(items) * 50)  // 예상 크기 사전할당

    for _, item := range items {
        fmt.Fprintf(&sb, "- %s: %d\n", item.Name, item.Price)
    }
    return sb.String()
}
```

### Map 사전할당

```go
// Before
userMap := make(map[int]*User)

// After
userMap := make(map[int]*User, len(users))
```

---

## Anti-Patterns

| Anti-Pattern | 문제 | 해결 |
|--------------|------|------|
| `interface{}` 남용 | 타입 안전성 상실 | 구체적 타입 또는 제네릭 사용 |
| 거대 인터페이스 | 구현 부담 | 작은 인터페이스로 분리 |
| init() 남용 | 테스트/순서 어려움 | 명시적 초기화 |
| 패키지 순환 | 컴파일 불가 | 인터페이스로 의존성 역전 |
| 불필요한 포인터 | GC 부담 | 작은 구조체는 값 복사 |

---

## 체크리스트

### 리팩토링 전

- [ ] `go test ./...` 통과?
- [ ] `go vet ./...` 경고 없음?
- [ ] 변경 범위 명확?

### 리팩토링 중

- [ ] Early Return 적용?
- [ ] 함수 20줄 이하?
- [ ] 인터페이스가 작은가? (1-3 메서드)
- [ ] 에러에 컨텍스트 추가?

### 리팩토링 후

- [ ] 테스트 통과?
- [ ] 벤치마크 성능 저하 없음?
- [ ] `golangci-lint run` 통과?

---

**관련 skill**: `/dx:refactoring-principles`, `/go:effective-go`, `/go:concurrency-go`
