---
name: rest-api-patterns
description: REST API implementation patterns. Use when building HTTP APIs.
---

# REST API Patterns Skill

REST API implementation patterns for Go.

## When to Use

Use when building HTTP APIs.

## Handler Pattern

```go
type Handler struct {
    service *Service
    logger  *log.Logger
}

func NewHandler(service *Service) *Handler {
    return &Handler{service: service, logger: log.Default()}
}

func (h *Handler) GetUser(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()

    // Parse ID
    userID, err := strconv.Atoi(chi.URLParam(r, "id"))
    if err != nil {
        respondError(w, http.StatusBadRequest, "invalid user ID")
        return
    }

    // Get user
    user, err := h.service.GetUser(ctx, userID)
    if err != nil {
        respondError(w, http.StatusInternalServerError, err.Error())
        return
    }

    respondJSON(w, http.StatusOK, user)
}
```

## Response Helpers

```go
func respondJSON(w http.ResponseWriter, status int, data interface{}) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteStatus(status)
    json.NewEncoder(w).Encode(data)
}

func respondError(w http.ResponseWriter, status int, message string) {
    respondJSON(w, status, map[string]string{"error": message})
}
```

## Middleware

```go
// Logging middleware
func loggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        next.ServeHTTP(w, r)
        log.Printf("%s %s %v", r.Method, r.URL.Path, time.Since(start))
    })
}

// Auth middleware
func authMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        token := r.Header.Get("Authorization")
        if !isValidToken(token) {
            http.Error(w, "Unauthorized", http.StatusUnauthorized)
            return
        }
        next.ServeHTTP(w, r)
    })
}
```

## Router Setup (Chi)

```go
func setupRoutes() http.Handler {
    r := chi.NewRouter()

    // Middleware
    r.Use(middleware.Logger)
    r.Use(middleware.Recoverer)
    r.Use(corsMiddleware)

    // Routes
    r.Get("/health", healthHandler)

    r.Route("/api/v1", func(r chi.Router) {
        r.Use(authMiddleware)
        r.Get("/users/{id}", handler.GetUser)
        r.Post("/users", handler.CreateUser)
        r.Put("/users/{id}", handler.UpdateUser)
        r.Delete("/users/{id}", handler.DeleteUser)
    })

    return r
}
```

## Request Validation

```go
type CreateUserRequest struct {
    Name  string `json:"name" validate:"required,min=2,max=100"`
    Email string `json:"email" validate:"required,email"`
}

func (h *Handler) CreateUser(w http.ResponseWriter, r *http.Request) {
    var req CreateUserRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        respondError(w, http.StatusBadRequest, "invalid JSON")
        return
    }

    if err := validate.Struct(req); err != nil {
        respondError(w, http.StatusBadRequest, err.Error())
        return
    }

    // process request
}
```

## Best Practices

- Use proper HTTP methods (GET, POST, PUT, DELETE)
- Return appropriate status codes
- Validate all inputs
- Use middleware for cross-cutting concerns
- Implement proper error handling
- Add request/response logging
- Use context for cancellation
- Implement graceful shutdown
