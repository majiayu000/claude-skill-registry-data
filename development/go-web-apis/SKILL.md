---
name: go-web-apis
description: Build production REST APIs with Go - handlers, middleware, security
sasmp_version: "1.3.0"
bonded_agent: 03-go-web
bond_type: PRIMARY_BOND
---

# Go Web APIs Skill

Build production-ready REST APIs with Go's net/http and popular frameworks.

## Overview

Complete guide for building secure, performant web APIs including routing, middleware, authentication, and best practices.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| framework | string | no | "stdlib" | Framework: "stdlib", "gin", "echo", "chi" |
| auth_type | string | no | "jwt" | Auth method: "jwt", "api-key", "oauth" |
| include_openapi | bool | no | false | Generate OpenAPI spec |

## Core Topics

### HTTP Handler Pattern
```go
type Server struct {
    db     *sql.DB
    logger *slog.Logger
}

func (s *Server) handleGetUser() http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        id := chi.URLParam(r, "id")

        user, err := s.db.GetUser(r.Context(), id)
        if err != nil {
            if errors.Is(err, sql.ErrNoRows) {
                http.Error(w, "user not found", http.StatusNotFound)
                return
            }
            s.logger.Error("get user", "error", err)
            http.Error(w, "internal error", http.StatusInternalServerError)
            return
        }

        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(user)
    }
}
```

### Middleware
```go
func LoggingMiddleware(logger *slog.Logger) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            start := time.Now()
            ww := &responseWriter{ResponseWriter: w, status: 200}

            defer func() {
                logger.Info("request",
                    "method", r.Method,
                    "path", r.URL.Path,
                    "status", ww.status,
                    "duration", time.Since(start),
                )
            }()

            next.ServeHTTP(ww, r)
        })
    }
}

func RecoveryMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if err := recover(); err != nil {
                http.Error(w, "internal error", http.StatusInternalServerError)
            }
        }()
        next.ServeHTTP(w, r)
    })
}
```

### JWT Authentication
```go
func JWTMiddleware(secret []byte) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            auth := r.Header.Get("Authorization")
            if !strings.HasPrefix(auth, "Bearer ") {
                http.Error(w, "unauthorized", http.StatusUnauthorized)
                return
            }

            token, err := jwt.Parse(strings.TrimPrefix(auth, "Bearer "), func(t *jwt.Token) (interface{}, error) {
                return secret, nil
            })
            if err != nil || !token.Valid {
                http.Error(w, "invalid token", http.StatusUnauthorized)
                return
            }

            claims := token.Claims.(jwt.MapClaims)
            ctx := context.WithValue(r.Context(), "user_id", claims["sub"])
            next.ServeHTTP(w, r.WithContext(ctx))
        })
    }
}
```

### Request Validation
```go
type CreateUserRequest struct {
    Name  string `json:"name" validate:"required,min=2,max=100"`
    Email string `json:"email" validate:"required,email"`
    Age   int    `json:"age" validate:"gte=0,lte=130"`
}

func (s *Server) handleCreateUser() http.HandlerFunc {
    validate := validator.New()

    return func(w http.ResponseWriter, r *http.Request) {
        var req CreateUserRequest
        if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
            http.Error(w, "invalid json", http.StatusBadRequest)
            return
        }

        if err := validate.Struct(req); err != nil {
            http.Error(w, err.Error(), http.StatusBadRequest)
            return
        }

        // process valid request
    }
}
```

## Retry Logic

```go
type HTTPClient struct {
    client  *http.Client
    backoff []time.Duration
}

func (c *HTTPClient) Do(req *http.Request) (*http.Response, error) {
    var resp *http.Response
    var err error

    for i, delay := range c.backoff {
        resp, err = c.client.Do(req)
        if err == nil && resp.StatusCode < 500 {
            return resp, nil
        }
        if i < len(c.backoff)-1 {
            time.Sleep(delay)
        }
    }
    return resp, err
}
```

## Unit Test Template

```go
func TestHandleGetUser(t *testing.T) {
    srv := &Server{db: mockDB, logger: slog.Default()}

    req := httptest.NewRequest("GET", "/users/123", nil)
    w := httptest.NewRecorder()

    srv.handleGetUser().ServeHTTP(w, req)

    if w.Code != http.StatusOK {
        t.Errorf("got status %d, want %d", w.Code, http.StatusOK)
    }

    var user User
    json.NewDecoder(w.Body).Decode(&user)
    if user.ID != 123 {
        t.Errorf("got id %d, want 123", user.ID)
    }
}
```

## Troubleshooting

### Failure Modes
| Symptom | Cause | Fix |
|---------|-------|-----|
| 5xx spike | Handler panic | Add recovery middleware |
| Slow responses | Missing timeouts | Configure server timeouts |
| Memory leak | Unclosed body | Always `defer resp.Body.Close()` |

## Usage

```
Skill("go-web-apis")
```
