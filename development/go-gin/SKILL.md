---
name: go-gin
description: "Use when building or extending Gin HTTP servers: route groups, middleware (logger/recover/auth), bind validators, structured error responses, graceful shutdown. Apply when go.mod imports gin-gonic/gin."
version: 1.0.0
license: MIT
applies_when:
  files_present:
    - "**/go.mod"
  files_contain:
    "**/go.mod": 'gin-gonic/gin'
  language:
    - go
  frameworks:
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
consumes:
  - api-contract
security:
  signature: ""
  sandbox: read-only
  network: none
---

# Gin Framework Patterns

Gin 웹 프레임워크 패턴 및 best practices.

## Quick Reference

```
Gin 패턴 선택
    │
    ├─ 핸들러 구조 ────> Handler struct + DI (service, logger)
    │
    ├─ 라우팅 ────────> gin.New() + Group() 기반 구조화
    │
    ├─ 미들웨어 ──────> Recovery, Logging, Auth 순서
    │
    └─ 요청 바인딩 ───> ShouldBindJSON + validator tags
```

---

## Handler Structure

```go
// internal/handler/user_handler.go
type UserHandler struct {
    userService service.UserService
    logger      *zap.Logger
}

func NewUserHandler(us service.UserService, logger *zap.Logger) *UserHandler {
    return &UserHandler{
        userService: us,
        logger:      logger,
    }
}

func (h *UserHandler) GetUser(c *gin.Context) {
    id, err := strconv.ParseInt(c.Param("id"), 10, 64)
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "invalid user id"})
        return
    }

    user, err := h.userService.GetByID(c.Request.Context(), id)
    if err != nil {
        if errors.Is(err, domain.ErrUserNotFound) {
            c.JSON(http.StatusNotFound, gin.H{"error": "user not found"})
            return
        }
        h.logger.Error("failed to get user", zap.Error(err))
        c.JSON(http.StatusInternalServerError, gin.H{"error": "internal error"})
        return
    }

    c.JSON(http.StatusOK, user)
}
```

## Router Setup

```go
// internal/handler/router.go
func SetupRouter(h *UserHandler) *gin.Engine {
    r := gin.New()
    r.Use(gin.Recovery())
    r.Use(ginzap.Ginzap(logger, time.RFC3339, true))

    api := r.Group("/api/v1")
    {
        users := api.Group("/users")
        {
            users.GET("/:id", h.GetUser)
            users.POST("", h.CreateUser)
            users.PUT("/:id", h.UpdateUser)
            users.DELETE("/:id", h.DeleteUser)
        }
    }

    return r
}
```

## Middleware

```go
func AuthMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        if token == "" {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "unauthorized"})
            return
        }
        // validate token...
        c.Set("userID", userID)
        c.Next()
    }
}

func LoggingMiddleware(logger *zap.Logger) gin.HandlerFunc {
    return func(c *gin.Context) {
        start := time.Now()
        c.Next()
        logger.Info("request",
            zap.String("method", c.Request.Method),
            zap.String("path", c.Request.URL.Path),
            zap.Int("status", c.Writer.Status()),
            zap.Duration("latency", time.Since(start)),
        )
    }
}
```

## Request Binding

```go
type CreateUserRequest struct {
    Name  string `json:"name" binding:"required,min=1,max=100"`
    Email string `json:"email" binding:"required,email"`
    Age   int    `json:"age" binding:"gte=0,lte=150"`
}

func (h *UserHandler) CreateUser(c *gin.Context) {
    var req CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }
    // ...
}
```

## Response Patterns

```go
// Success
c.JSON(http.StatusOK, user)
c.JSON(http.StatusCreated, gin.H{"id": user.ID})
c.Status(http.StatusNoContent)

// Error
c.JSON(http.StatusBadRequest, gin.H{"error": "invalid input"})
c.JSON(http.StatusNotFound, gin.H{"error": "not found"})
c.JSON(http.StatusInternalServerError, gin.H{"error": "internal error"})
```

## Anti-patterns

| Mistake | Correct | Why |
|---------|---------|-----|
| `c.Abort()` without response | `c.AbortWithStatusJSON()` | 클라이언트에 응답 필요 |
| Using `c.Copy()` in goroutine | Context 데이터 미리 추출 | 원본 context는 요청 후 무효화 |
| `panic` for errors | Error response 반환 | Recovery 미들웨어 의존 금지 |
| Business logic in handler | Service 계층으로 분리 | 핸들러는 HTTP만 처리 |
