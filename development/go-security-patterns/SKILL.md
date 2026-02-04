---
name: Go Security Patterns
description: This skill should be used when the user asks about "gosec", "G115", "G404", "integer overflow", "weak random", "crypto/rand", "security lint", "hardcoded credentials", or needs guidance on fixing Go security vulnerabilities. Provides patterns for common security anti-patterns.
---

# Go Security Patterns

Patterns for fixing common Go security lint violations from gosec.

## Overview

gosec (Go Security Checker) identifies security anti-patterns:

| Rule | Category | Risk |
|------|----------|------|
| **G115** | Integer overflow | Data corruption, crashes |
| **G404** | Weak random | Predictable tokens |
| **G101** | Hardcoded secrets | Credential exposure |
| **G107** | Unvalidated URL | SSRF attacks |
| **G304** | Path traversal | File access bypass |
| **G401** | Weak crypto (MD5/SHA1) | Hash collisions |

## Pattern 1: Safe Integer Conversion (G115)

Converting between integer types can overflow on different architectures.

### Problem

```go
func ProcessCount(n int64) {
    count := int(n)  // G115: int is 32-bit on some systems
    buffer := make([]byte, count)
}
```

### Solution 1: Bounds Check

```go
import "math"

func ProcessCount(n int64) error {
    if n < 0 || n > math.MaxInt {
        return fmt.Errorf("count %d out of range", n)
    }
    count := int(n)
    buffer := make([]byte, count)
    return nil
}
```

### Solution 2: Keep Original Type

```go
func ProcessCount(n int64) {
    buffer := make([]byte, n)  // slice length accepts int64
}
```

### Solution 3: Document Constraint

When overflow is impossible due to domain constraints:

```go
// pageSize is always 1-100 from validated input
func ProcessPage(pageSize int64) {
    //nolint:gosec // pageSize validated to [1,100] by caller
    count := int(pageSize)
}
```

### Architecture-Safe Patterns

```go
// Instead of: int(x) where x is int64
// Use: explicit checks or keep type

// For array/slice indices from int64:
if idx < 0 || idx > math.MaxInt {
    return ErrIndexOutOfRange
}
arr[int(idx)]  // Now safe

// For loop counters:
for i := int64(0); i < n; i++ {
    // Keep as int64 throughout
}
```

## Pattern 2: Cryptographic Random (G404)

`math/rand` is deterministic - use `crypto/rand` for security.

### Problem

```go
import "math/rand"

func GenerateSessionID() string {
    return fmt.Sprintf("%x", rand.Int63())  // G404: predictable
}
```

### Solution

```go
import (
    "crypto/rand"
    "encoding/hex"
)

func GenerateSessionID() (string, error) {
    b := make([]byte, 16)
    if _, err := rand.Read(b); err != nil {
        return "", fmt.Errorf("generate session ID: %w", err)
    }
    return hex.EncodeToString(b), nil
}
```

### When math/rand is Acceptable

- Shuffling for display (not security)
- Test data generation
- Games/simulations
- Performance-critical non-security code

Add explicit nolint with justification:

```go
//nolint:gosec // shuffle for UI display order, not security
rand.Shuffle(len(items), func(i, j int) {
    items[i], items[j] = items[j], items[i]
})
```

### Crypto/Rand Patterns

```go
// Generate random bytes
b := make([]byte, 32)
_, err := rand.Read(b)

// Generate random number in range
n, err := rand.Int(rand.Reader, big.NewInt(100))

// Generate UUID-like token
func GenerateToken() string {
    b := make([]byte, 16)
    rand.Read(b)
    return base64.RawURLEncoding.EncodeToString(b)
}
```

## Pattern 3: Secrets Management (G101)

Never hardcode credentials, API keys, or tokens.

### Problem

```go
const (
    apiKey = "sk-abc123xyz"  // G101
    dbPass = "secret123"     // G101
)
```

### Solution: Environment Variables

```go
func getAPIKey() string {
    key := os.Getenv("API_KEY")
    if key == "" {
        log.Fatal("API_KEY not set")
    }
    return key
}
```

### Solution: Config Files

```go
type Config struct {
    APIKey string `env:"API_KEY" yaml:"api_key"`
}

func LoadConfig() (*Config, error) {
    // Load from environment or config file
}
```

### False Positives

gosec may flag non-secrets. Use nolint with reason:

```go
//nolint:gosec // example key for documentation
const exampleKey = "sk-example-not-real"

//nolint:gosec // password field name, not actual password
const passwordField = "password"
```

## Pattern 4: URL Validation (G107)

Unvalidated URLs in HTTP requests enable SSRF.

### Problem

```go
func Fetch(url string) (*http.Response, error) {
    return http.Get(url)  // G107: URL from variable
}
```

### Solution: Allowlist

```go
var allowedHosts = map[string]bool{
    "api.example.com": true,
    "cdn.example.com": true,
}

func Fetch(rawURL string) (*http.Response, error) {
    u, err := url.Parse(rawURL)
    if err != nil {
        return nil, fmt.Errorf("invalid URL: %w", err)
    }
    if !allowedHosts[u.Host] {
        return nil, fmt.Errorf("host %s not allowed", u.Host)
    }
    return http.Get(rawURL)
}
```

## Pattern 5: Path Sanitization (G304)

User-controlled paths enable directory traversal.

### Problem

```go
func ReadFile(name string) ([]byte, error) {
    return os.ReadFile(filepath.Join("/data", name))  // G304
}
```

### Solution

```go
func ReadFile(name string) ([]byte, error) {
    // Clean the path and verify it's within allowed directory
    clean := filepath.Clean(name)
    if strings.Contains(clean, "..") {
        return nil, fmt.Errorf("invalid path: %s", name)
    }

    full := filepath.Join("/data", clean)
    if !strings.HasPrefix(full, "/data/") {
        return nil, fmt.Errorf("path escapes data directory")
    }

    return os.ReadFile(full)
}
```

## Quick Reference

| Issue | Detection | Fix |
|-------|-----------|-----|
| `int(x)` where x is int64 | G115 | Bounds check or keep type |
| `math/rand` for tokens | G404 | Use `crypto/rand` |
| Literal secrets | G101 | Environment/config |
| `http.Get(variable)` | G107 | Validate/allowlist URL |
| `os.ReadFile(variable)` | G304 | Sanitize path |

## Verification

```bash
golangci-lint run --enable gosec ./...
go test ./...
```
