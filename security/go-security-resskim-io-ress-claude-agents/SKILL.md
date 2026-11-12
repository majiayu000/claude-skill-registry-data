---
name: go-security
description: "Go 보안 리뷰 — 입력 검증·SQL/Command injection, 시크릿·인증 처리, 동시성 안전성, crypto/TLS 설정, 에러 정보 노출, path traversal, govulncheck/gosec 도구. Use when Go 코드 보안 리뷰나 취약점 점검이 필요할 때."
---

# Go 보안 리뷰

언어 무관 원칙은 `/security:secure-coding` / `/security:owasp-top10`.
여기서는 **Go 에서 실제로 틀리는 지점**을 코드 단위로 다룬다.

## Security Review Checklist

Go 코드 리뷰 시 반드시 점검해야 할 보안 항목. Red team 공격 시나리오 기반.

### Input Validation & Injection

```go
// ❌ VULNERABLE: SQL injection
func GetUser(db *sql.DB, id string) (*User, error) {
    query := "SELECT * FROM users WHERE id = '" + id + "'"
    return db.Query(query)
}
// 🔓 Attack: id = "'; DROP TABLE users; --"

// ✅ HARDENED: Parameterized query
func GetUser(db *sql.DB, id string) (*User, error) {
    return db.QueryRow("SELECT * FROM users WHERE id = $1", id).Scan(...)
}

// ❌ VULNERABLE: Command injection
func RunCommand(userInput string) {
    exec.Command("sh", "-c", "echo " + userInput).Run()
}
// 🔓 Attack: userInput = "; cat /etc/passwd"

// ✅ HARDENED: 직접 실행, 셸 우회
func RunCommand(filename string) {
    if !isValidFilename(filename) { return }
    exec.Command("echo", filename).Run()
}
```

### Authentication & Secrets

```go
// ❌ VULNERABLE: 하드코딩된 시크릿
const apiKey = "sk-live-abc123def456"

// ✅ HARDENED: 환경변수
apiKey := os.Getenv("API_KEY")
if apiKey == "" { log.Fatal("API_KEY not set") }

// ❌ VULNERABLE: JWT alg 미검증
token, _ := jwt.Parse(tokenString, func(t *jwt.Token) (interface{}, error) {
    return []byte("secret"), nil  // alg 검증 없음
})

// ✅ HARDENED: 알고리즘 검증
token, err := jwt.Parse(tokenString, func(t *jwt.Token) (interface{}, error) {
    if _, ok := t.Method.(*jwt.SigningMethodRSA); !ok {
        return nil, fmt.Errorf("unexpected signing method: %v", t.Header["alg"])
    }
    return publicKey, nil
})
```

### Concurrency Safety

```go
// ❌ VULNERABLE: Race condition
var cache = make(map[string]string)
func Set(k, v string) { cache[k] = v }  // concurrent map write → panic

// ✅ HARDENED: sync.Map 또는 RWMutex
var cache sync.Map
func Set(k, v string) { cache.Store(k, v) }
```

### Crypto & TLS

```go
// ❌ VULNERABLE: 취약한 TLS 설정
tlsConfig := &tls.Config{
    InsecureSkipVerify: true,  // MITM 공격 허용
    MinVersion: tls.VersionTLS10,
}

// ✅ HARDENED
tlsConfig := &tls.Config{
    MinVersion: tls.VersionTLS12,
    CipherSuites: []uint16{
        tls.TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,
        tls.TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,
    },
}
```

### Error Handling & Information Disclosure

```go
// ❌ VULNERABLE: 내부 정보 노출
func handler(w http.ResponseWriter, r *http.Request) {
    _, err := db.Query(query)
    if err != nil {
        http.Error(w, fmt.Sprintf("DB error: %v", err), 500)
        // 🔓 Attack: 에러 메시지로 DB 구조, 쿼리, 스택 노출
    }
}

// ✅ HARDENED: 내부 로깅 + generic 응답
func handler(w http.ResponseWriter, r *http.Request) {
    _, err := db.Query(query)
    if err != nil {
        log.Error("db query failed", "error", err, "query", query)
        http.Error(w, "Internal server error", 500)
    }
}
```

### Path Traversal

```go
// ❌ VULNERABLE: path traversal
func serveFile(w http.ResponseWriter, r *http.Request) {
    filename := r.URL.Query().Get("file")
    http.ServeFile(w, r, "/uploads/" + filename)
    // 🔓 Attack: file=../../../etc/passwd
}

// ✅ HARDENED: filepath.Clean + 경로 검증
func serveFile(w http.ResponseWriter, r *http.Request) {
    filename := filepath.Clean(r.URL.Query().Get("file"))
    fullPath := filepath.Join("/uploads", filename)
    if !strings.HasPrefix(fullPath, "/uploads/") {
        http.Error(w, "Forbidden", 403)
        return
    }
    http.ServeFile(w, r, fullPath)
}
```

### Security Tools

```bash
# 정적 분석
gosec ./...                    # Go 보안 린터
go vet ./...                   # 일반 분석
staticcheck ./...              # 확장 분석

# 의존성 취약점
govulncheck ./...              # Go 공식 취약점 스캐너
nancy sleuth < go.sum          # Sonatype 취약점 DB

# Race detector
go test -race ./...

# Fuzzing
go test -fuzz=FuzzParseInput ./...
```

## 참조 스킬

- `/security:secure-coding` — 언어 공통 입력 검증 / 인코딩 / 암호화
- `/security:owasp-top10` — A01~A10 매핑
- `/cicd:supply-chain-security` — 의존성 / SBOM / 서명
- `/security:secrets-management` — 시크릿 주입 경로
- [`go-performance`](../go-performance/SKILL.md) — 동시성 안전성과 성능의 트레이드오프
