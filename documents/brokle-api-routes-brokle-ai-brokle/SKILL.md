---
name: brokle-api-routes
description: Use this skill when creating, modifying, or reviewing API endpoints and routes. This includes SDK routes (/v1/*), Dashboard routes (/api/v1/*), request/response structures, input validation, OpenAPI documentation, or API-related middleware.
---

# Brokle API Routes Skill

Expert guidance for API endpoint development following Brokle's dual-route architecture.

## Dual Route Architecture

### SDK Routes (`/v1/*`) - API Key Authentication
**Target**: SDK integration, programmatic access
**Auth**: API keys (`bk_{40_char_random}`)
**Rate Limiting**: API key-based

**Examples**:
- `POST /v1/chat/completions` - OpenAI-compatible chat
- `POST /v1/embeddings` - Embeddings
- `POST /v1/traces` - OTLP traces ingestion (OpenTelemetry standard)
- `GET /v1/models` - Available models
- `POST /v1/route` - AI routing decisions

### Dashboard Routes (`/api/v1/*`) - JWT Authentication
**Target**: Web dashboard, administrative access
**Auth**: Bearer JWT tokens
**Rate Limiting**: IP-based + user-based

**Examples**:
- `/api/v1/auth/*` - Authentication & sessions
- `/api/v1/users/*` - User management
- `/api/v1/organizations/*` - Organization management
- `/api/v1/projects/*` - Project management
- `/api/v1/analytics/*` - Metrics & reporting

## URL Structure Standards

```
/api/v1/{domain}/{resource}[/{id}][/{sub-resource}]

Examples:
GET    /api/v1/auth/users                    # List users
POST   /api/v1/auth/users                    # Create user
GET    /api/v1/auth/users/{id}               # Get user
PUT    /api/v1/auth/users/{id}               # Update user
DELETE /api/v1/auth/users/{id}               # Delete user
GET    /api/v1/auth/users/{id}/sessions      # Get user sessions
```

## Complete Handler Pattern

```go
package http

import (
    "github.com/gin-gonic/gin"
    authDomain "brokle/internal/core/domain/auth"
    "brokle/internal/transport/http/middleware"
    "brokle/pkg/response"
    "brokle/pkg/ulid"
    "brokle/pkg/apperrors"
)

type UserHandler struct {
    userService authDomain.UserService
}

func NewUserHandler(userService authDomain.UserService) *UserHandler {
    return &UserHandler{userService: userService}
}

// RegisterRoutes sets up all user-related routes
// Note: Called from server setup where middleware is already applied to parent group
func (h *UserHandler) RegisterRoutes(r *gin.RouterGroup) {
    users := r.Group("/users")
    {
        users.POST("", h.CreateUser)
        users.GET("", h.ListUsers)
        users.GET("/:id", h.GetUser)
        users.PUT("/:id", h.UpdateUser)
        users.DELETE("/:id", h.DeleteUser)
    }
}

// @Summary      Create a new user
// @Description  Create a new user account with the provided information
// @Tags         Users
// @Accept       json
// @Produce      json
// @Param        request  body      CreateUserRequest  true  "User creation data"
// @Success      201      {object}  CreateUserResponse
// @Failure      400      {object}  response.ErrorResponse
// @Failure      409      {object}  response.ErrorResponse
// @Router       /api/v1/auth/users [post]
// @Security     ApiKeyAuth
func (h *UserHandler) CreateUser(c *gin.Context) {
    var req CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        response.Error(c, appErrors.NewValidationError("Invalid request body", err))
        return
    }

    resp, err := h.userService.CreateUser(c.Request.Context(), &req)
    if err != nil {
        response.Error(c, err)
        return
    }

    response.Created(c, resp)
}
```

## Request/Response Patterns

### Create Request
```go
type CreateUserRequest struct {
    Email    string `json:"email" binding:"required,email" example:"user@example.com"`
    Name     string `json:"name" binding:"required,min=2,max=100" example:"John Doe"`
    Password string `json:"password" binding:"required,min=8" example:"secure123"`
}
```

### Update Request (Pointers for Optional)
```go
type UpdateUserRequest struct {
    Name   *string `json:"name,omitempty" binding:"omitempty,min=2,max=100"`
    Email  *string `json:"email,omitempty" binding:"omitempty,email"`
    Status *string `json:"status,omitempty" binding:"omitempty,oneof=active inactive"`
}
```

### List Request (Query Params)
```go
type ListUsersRequest struct {
    Page    int    `form:"page" binding:"omitempty,min=1" example:"1"`
    Limit   int    `form:"limit" binding:"omitempty,min=1,max=100" example:"20"`
    Search  string `form:"search" binding:"omitempty,max=100" example:"john"`
    Status  string `form:"status" binding:"omitempty,oneof=active inactive all"`
    SortBy  string `form:"sort_by" binding:"omitempty,oneof=created_at name email"`
    SortDir string `form:"sort_dir" binding:"omitempty,oneof=asc desc"`
}
```

### Response with Pagination
```go
type ListUsersResponse struct {
    Users      []*User     `json:"users"`
    Pagination *Pagination `json:"pagination"`
}

type Pagination struct {
    Page      int   `json:"page" example:"2"`
    PageSize  int   `json:"page_size" example:"20"`
    Total     int64 `json:"total" example:"156"`
    TotalPage int   `json:"total_page" example:"8"`
    HasNext   bool  `json:"has_next" example:"true"`
    HasPrev   bool  `json:"has_prev" example:"true"`
}
```

## Error Handling in Handlers

```go
// Input validation
if err := c.ShouldBindJSON(&req); err != nil {
    response.Error(c, appErrors.NewValidationError("Invalid request body", err))
    return
}

// Parameter validation
id, err := ulid.Parse(c.Param("id"))
if err != nil {
    response.Error(c, appErrors.NewValidationError("Invalid ID format", "id must be a valid ULID"))
    return
}

// Service layer errors (automatic HTTP mapping)
resp, err := h.service.Method(c.Request.Context(), req)
if err != nil {
    response.Error(c, err)  // Maps AppErrors to HTTP status
    return
}
```

## OpenAPI Documentation

```go
// @Summary      Brief description (1 line)
// @Description  Detailed description
// @Tags         Group endpoints logically
// @Accept       json
// @Produce      json
// @Param        id       path      string             true   "Resource ID"
// @Param        request  body      CreateUserRequest  true   "Request body"
// @Param        page     query     int                false  "Page number"  minimum(1)
// @Success      200      {object}  GetUserResponse
// @Success      201      {object}  CreateUserResponse
// @Failure      400      {object}  response.ErrorResponse
// @Failure      404      {object}  response.ErrorResponse
// @Router       /api/v1/auth/users/{id} [get]
// @Security     ApiKeyAuth
```

## Middleware Setup

### SDK Routes
```go
sdkRoutes := r.Group("/v1")
sdkRoutes.Use(sdkAuthMiddleware.RequireSDKAuth())
sdkRoutes.Use(rateLimitMiddleware.RateLimitByAPIKey())
{
    sdkRoutes.POST("/chat/completions", chatHandler.Completions)
    sdkRoutes.POST("/embeddings", embeddingsHandler.Create)
}
```

### Dashboard Routes (`internal/transport/http/server.go:219-223`)
```go
// Note: Middleware is injected via DI container (not package-level functions)
protected := router.Group("")
protected.Use(s.authMiddleware.RequireAuth())           // Instance method - JWT validation
protected.Use(s.csrfMiddleware.ValidateCSRF())          // Instance method - CSRF protection
protected.Use(s.rateLimitMiddleware.RateLimitByUser()) // Instance method - User rate limiting
{
    protected.POST("/users", userHandler.CreateUser)
    protected.GET("/users", userHandler.ListUsers)
}
```

## HTTP Status Code Mapping

| AppError Type | HTTP Status | Description |
|---------------|-------------|-------------|
| ValidationError | 400 | Invalid input |
| UnauthorizedError | 401 | Auth required |
| ForbiddenError | 403 | Insufficient permissions |
| NotFoundError | 404 | Resource not found |
| ConflictError | 409 | Already exists |
| RateLimitError | 429 | Rate limit exceeded |
| InternalError | 500 | Unexpected error |

## References

- `docs/development/API_DEVELOPMENT_GUIDE.md` - Complete API patterns
- `docs/development/PAGINATION_GUIDE.md` - Pagination standards
