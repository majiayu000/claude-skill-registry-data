---
name: concurrency-go
description: "Go 동시성 패턴 — race detector, Mutex·RWMutex, channel 설계, DB 동시성, goroutine 누수 방지. Use when Go 코드의 data race·deadlock을 잡거나 mutex와 channel 중 무엇을 쓸지 정할 때."
---

# Go Concurrency Patterns

MSA/대규모 트래픽 환경에서의 Go 동시성 문제 해결 패턴

## Quick Reference (결정 트리)

```
공유 상태 있음?
    │
    ├─ 없음 ──────────────> Channels (Go Way)
    │
    └─ 있음
         ├─ 읽기 많음 ──────> sync.RWMutex
         ├─ 쓰기 많음 ──────> sync.Mutex
         └─ 맵 캐시 ────────> sync.Map

DB 동시성?
    ├─ 충돌 드묾 ──────────> Optimistic (Version)
    ├─ 충돌 잦음 ──────────> Pessimistic (FOR UPDATE)
    └─ MSA/다중 서버 ──────> Distributed Lock (/architecture:distributed-lock)
```

---

## CRITICAL: Race Detector

**IMPORTANT**: CI에서 반드시 `-race` 플래그 사용

```bash
go test -race ./...   # 테스트 시
go build -race -o app # 빌드 시
```

---

## Mutex (상호 배제)

### sync.Mutex
```go
type SafeCounter struct {
    mu    sync.Mutex
    count int
}

func (c *SafeCounter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count++
}
```

### sync.RWMutex (읽기 많은 경우)
```go
type SafeCache struct {
    mu    sync.RWMutex
    items map[string]interface{}
}

func (c *SafeCache) Get(key string) (interface{}, bool) {
    c.mu.RLock()  // 읽기 락 (동시 읽기 허용)
    defer c.mu.RUnlock()
    return c.items[key]
}

func (c *SafeCache) Set(key string, value interface{}) {
    c.mu.Lock()  // 쓰기 락 (배타적)
    defer c.mu.Unlock()
    c.items[key] = value
}
```

---

## Channels (Go 철학)

> "Don't communicate by sharing memory; share memory by communicating."

### Worker Pool
```go
func worker(jobs <-chan int, results chan<- int) {
    for job := range jobs {
        results <- process(job)
    }
}

func main() {
    jobs := make(chan int, 100)
    results := make(chan int, 100)

    // 워커 3개 시작
    for w := 0; w < 3; w++ {
        go worker(jobs, results)
    }

    // 작업 전송 후 채널 닫기
    for j := 0; j < 9; j++ {
        jobs <- j
    }
    close(jobs)
}
```

### Select로 타임아웃
```go
func fetchWithTimeout(ctx context.Context, url string) ([]byte, error) {
    resultCh := make(chan []byte, 1)
    errCh := make(chan error, 1)

    go func() {
        data, err := fetch(url)
        if err != nil {
            errCh <- err
            return
        }
        resultCh <- data
    }()

    select {
    case data := <-resultCh:
        return data, nil
    case err := <-errCh:
        return nil, err
    case <-ctx.Done():
        return nil, ctx.Err()
    }
}
```

---

## Database 동시성

### Optimistic Locking (GORM)
```go
type Product struct {
    ID      uint `gorm:"primaryKey"`
    Stock   int
    Version int  `gorm:"default:1"`
}

func (p *Product) BeforeUpdate(tx *gorm.DB) error {
    tx.Statement.Where("version = ?", p.Version)
    p.Version++
    return nil
}

// 사용: RowsAffected == 0 이면 충돌 발생
result := tx.Save(&product)
if result.RowsAffected == 0 {
    return errors.New("concurrent modification")
}
```

### Pessimistic Locking
```go
// SELECT ... FOR UPDATE
tx.Clauses(clause.Locking{Strength: "UPDATE"}).
    First(&product, productID)
```

---

## 유틸리티

### sync.Once (싱글톤)
```go
var (
    instance *Database
    once     sync.Once
)

func GetDatabase() *Database {
    once.Do(func() {
        instance = &Database{/* 초기화 */}
    })
    return instance
}
```

### sync.Map (동시성 안전 맵)
```go
var cache sync.Map

cache.Store("key", "value")
val, ok := cache.Load("key")
cache.Delete("key")
```

### Context 취소
```go
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

select {
case <-ctx.Done():
    return ctx.Err()
default:
    // 작업 수행
}
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| `map` 동시 접근 | panic | `sync.Map` 또는 `Mutex` |
| `defer unlock` 누락 | 데드락 | 항상 `defer mu.Unlock()` |
| 무한 고루틴 생성 | 메모리 폭발 | Worker Pool 사용 |
| 채널 close 안함 | 고루틴 누수 | `defer close(ch)` |
| 버퍼 없는 채널 | 데드락 | 버퍼 설정 또는 select |
| Context 무시 | 취소 안됨 | Context 전파 |

---

## 체크리스트

- [ ] `go test -race` CI에 추가
- [ ] 공유 상태에 Mutex 또는 Channel 사용
- [ ] 고루틴 수 제한 (Worker Pool)
- [ ] Context로 타임아웃/취소 처리
- [ ] `defer`로 락 해제, 채널 close
- [ ] MSA 환경: `/architecture:distributed-lock` 참조
