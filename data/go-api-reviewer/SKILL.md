---
name: go-api-reviewer
description: |
  WHEN: Go API review with Gin/Echo/Fiber/Chi, router patterns, middleware, request handling
  WHAT: Router organization + Middleware patterns + Request validation + Error responses + OpenAPI
  WHEN NOT: General Go → go-reviewer, Rust API → rust-api-reviewer
---

# Go API Reviewer Skill

## Purpose
Reviews Go API projects using Gin, Echo, Fiber, or Chi for routing, middleware, and API patterns.

## When to Use
- Go REST API code review
- Gin/Echo/Fiber/Chi project review
- Middleware implementation review
- API request/response handling
- API documentation review

## Project Detection
- `github.com/gin-gonic/gin` import
- `github.com/labstack/echo` import
- `github.com/gofiber/fiber` import
- `github.com/go-chi/chi` import
- `handlers/`, `routes/`, `middleware/` directories

## Workflow

### Step 1: Analyze Project
```
**Framework**: Gin v1.9+
**Router**: Group-based routing
**Middleware**: Auth, CORS, Logger, Recovery
**Validation**: go-playground/validator
**Docs**: Swagger/OpenAPI
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which areas to review?"
Options:
- Full API review (recommended)
- Router and handler patterns
- Middleware implementation
- Request validation
- Error handling and responses
multiSelect: true
```

## Detection Rules

### Router Organization
| Check | Recommendation | Severity |
|-------|----------------|----------|
| All routes in main | Use router groups | MEDIUM |
| No versioning | Add /api/v1 prefix | MEDIUM |
| Inconsistent naming | Follow REST conventions | LOW |
| No route grouping | Group by resource | MEDIUM |

```go
// BAD: All routes in main.go
func main() {
    r := gin.Default()
    r.GET("/users", getUsers)
    r.POST("/users", createUser)
    r.GET("/users/:id", getUser)
    r.GET("/products", getProducts)
    // ... 50 more routes
}

// GOOD: Organized route groups (Gin)
func SetupRouter() *gin.Engine {
    r := gin.Default()

    api := r.Group("/api/v1")
    {
        users := api.Group("/users")
        {
            users.GET("", listUsers)
            users.POST("", createUser)
            users.GET("/:id", getUser)
            users.PUT("/:id", updateUser)
            users.DELETE("/:id", deleteUser)
        }

        products := api.Group("/products")
        {
            products.GET("", listProducts)
            products.GET("/:id", getProduct)
        }
    }

    return r
}

// GOOD: Separate route files
// routes/users.go
func RegisterUserRoutes(rg *gin.RouterGroup) {
    users := rg.Group("/users")
    h := NewUserHandler()

    users.GET("", h.List)
    users.POST("", h.Create)
    users.GET("/:id", h.Get)
}
```

### Middleware Patterns
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Auth in handler | Extract to middleware | HIGH |
| No recovery middleware | Add panic recovery | HIGH |
| No request ID | Add request ID middleware | MEDIUM |
| Middleware order wrong | Order: Logger → Recovery → Auth | MEDIUM |

```go
// GOOD: Middleware stack (Gin)
func SetupMiddleware(r *gin.Engine) {
    // Order matters!
    r.Use(gin.Logger())
    r.Use(gin.Recovery())
    r.Use(RequestIDMiddleware())
    r.Use(CORSMiddleware())
}

// GOOD: Auth middleware
func AuthMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        if token == "" {
            c.AbortWithStatusJSON(401, gin.H{"error": "unauthorized"})
            return
        }

        claims, err := ValidateToken(token)
        if err != nil {
            c.AbortWithStatusJSON(401, gin.H{"error": "invalid token"})
            return
        }

        c.Set("user_id", claims.UserID)
        c.Next()
    }
}

// Usage
api := r.Group("/api/v1")
api.Use(AuthMiddleware())

// GOOD: Request ID middleware
func RequestIDMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        requestID := c.GetHeader("X-Request-ID")
        if requestID == "" {
            requestID = uuid.New().String()
        }
        c.Set("request_id", requestID)
        c.Header("X-Request-ID", requestID)
        c.Next()
    }
}
```

### Request Validation
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Manual validation | Use validator tags | MEDIUM |
| No binding errors | Return validation errors | HIGH |
| No request DTOs | Define request structs | MEDIUM |
| Missing required fields | Add binding:"required" | HIGH |

```go
// GOOD: Request struct with validation
type CreateUserRequest struct {
    Name     string `json:"name" binding:"required,min=1,max=100"`
    Email    string `json:"email" binding:"required,email"`
    Age      int    `json:"age" binding:"gte=0,lte=150"`
    Role     string `json:"role" binding:"oneof=admin user guest"`
    Password string `json:"password" binding:"required,min=8"`
}

// GOOD: Handler with validation
func (h *UserHandler) Create(c *gin.Context) {
    var req CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(400, gin.H{
            "error":   "validation_error",
            "details": formatValidationErrors(err),
        })
        return
    }

    user, err := h.service.Create(c.Request.Context(), &req)
    if err != nil {
        handleError(c, err)
        return
    }

    c.JSON(201, user)
}

// GOOD: Format validation errors
func formatValidationErrors(err error) map[string]string {
    errors := make(map[string]string)

    var ve validator.ValidationErrors
    if errors.As(err, &ve) {
        for _, e := range ve {
            field := strings.ToLower(e.Field())
            errors[field] = getErrorMessage(e)
        }
    }

    return errors
}
```

### Error Handling
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Inconsistent error format | Use standard error response | HIGH |
| Internal errors exposed | Hide implementation details | HIGH |
| No error codes | Add error codes | MEDIUM |
| HTTP status inconsistent | Follow REST conventions | MEDIUM |

```go
// GOOD: Standard error response
type ErrorResponse struct {
    Error   string            `json:"error"`
    Code    string            `json:"code,omitempty"`
    Details map[string]string `json:"details,omitempty"`
}

// GOOD: Custom errors
var (
    ErrNotFound     = &AppError{Code: "NOT_FOUND", Status: 404}
    ErrUnauthorized = &AppError{Code: "UNAUTHORIZED", Status: 401}
    ErrConflict     = &AppError{Code: "CONFLICT", Status: 409}
)

type AppError struct {
    Code    string
    Status  int
    Message string
}

func (e *AppError) Error() string {
    return e.Message
}

// GOOD: Error handler
func handleError(c *gin.Context, err error) {
    var appErr *AppError
    if errors.As(err, &appErr) {
        c.JSON(appErr.Status, ErrorResponse{
            Error: appErr.Message,
            Code:  appErr.Code,
        })
        return
    }

    // Log internal error, return generic message
    log.Printf("internal error: %v", err)
    c.JSON(500, ErrorResponse{
        Error: "Internal server error",
        Code:  "INTERNAL_ERROR",
    })
}
```

### Framework-Specific (Echo)
```go
// Echo example
func SetupEcho() *echo.Echo {
    e := echo.New()

    e.Use(middleware.Logger())
    e.Use(middleware.Recover())
    e.Use(middleware.RequestID())
    e.Use(middleware.CORS())

    api := e.Group("/api/v1")
    api.Use(AuthMiddleware)

    RegisterUserRoutes(api)

    return e
}

// Echo handler
func (h *UserHandler) Create(c echo.Context) error {
    var req CreateUserRequest
    if err := c.Bind(&req); err != nil {
        return echo.NewHTTPError(400, "invalid request")
    }

    if err := c.Validate(&req); err != nil {
        return err
    }

    user, err := h.service.Create(c.Request().Context(), &req)
    if err != nil {
        return err
    }

    return c.JSON(201, user)
}
```

## Response Template
```
## Go API Code Review Results

**Project**: [name]
**Framework**: Gin 1.9 | **Go**: 1.22

### Router Organization
| Status | File | Issue |
|--------|------|-------|
| MEDIUM | main.go | 40+ routes in single file |

### Middleware
| Status | File | Issue |
|--------|------|-------|
| HIGH | handlers/user.go | Auth check in handler, not middleware |

### Validation
| Status | File | Issue |
|--------|------|-------|
| HIGH | handlers/user.go:34 | No request validation |

### Error Handling
| Status | File | Issue |
|--------|------|-------|
| HIGH | handlers/product.go | Inconsistent error response format |

### Recommended Actions
1. [ ] Split routes into separate files by resource
2. [ ] Extract auth logic to middleware
3. [ ] Add request struct validation
4. [ ] Implement standard error response format
```

## Best Practices
1. **Router**: Group by resource, version API
2. **Middleware**: Proper order, reusable
3. **Validation**: Use validator tags
4. **Errors**: Standard format, hide internals
5. **Docs**: Generate OpenAPI from code

## Integration
- `go-reviewer`: General Go patterns
- `security-scanner`: API security
- `api-documenter`: OpenAPI documentation
