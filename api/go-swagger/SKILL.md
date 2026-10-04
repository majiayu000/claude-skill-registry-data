---
name: go-swagger
description: "API documentation with swaggo/swag. Covers annotations, security definitions, and generating OpenAPI specifications from Go code."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 06:35:00 GMT
---

## Core Tool: swaggo/swag

`swaggo/swag` converts Go annotations into Swagger 2.0 (OpenAPI 2.0) documentation.

### Workflow
1. Add annotations to your API handlers and `main.go`.
2. Run `swag init` to generate the `docs/` directory.
3. Import the generated `docs` package with a blank import in `main.go`.
4. Serve the Swagger UI using a middleware (e.g., `http-swagger`, `gin-swagger`, `echo-swagger`).

## Essential Annotations

### General Info (in `main.go`)
```go
// @title           My Awesome API
// @version         1.0
// @description     This is a sample server celler server.
// @host            localhost:8080
// @BasePath        /api/v1
```

### Endpoint Definition
```go
// @Summary      Get user by ID
// @Description  Retrieves a user's profile information by their unique identifier.
// @Tags         users
// @Accept       json
// @Produce      json
// @Param        id   path      string  true  "User ID"
// @Success      200  {object}  model.User
// @Failure      404  {object}  api.ErrorResponse
// @Router       /users/{id} [get]
func GetUser(w http.ResponseWriter, r *http.Request) { ... }
```

## Security Definitions

```go
// @securityDefinitions.apikey Bearer
// @in header
// @name Authorization
```

Apply to an endpoint:
```go
// @Security Bearer
```

## Struct Tags

Enrich your models with `example`, `enums`, and `format` tags:
```go
type User struct {
    ID    string `json:"id" example:"user_123"`
    Role  string `json:"role" enums:"admin,user" example:"user"`
    Email string `json:"email" format:"email"`
}
```

## Best Practices

1. **Keep it Fresh** — Run `swag init` after every change to your API annotations.
2. **Blank Import** — Ensure `_ "github.com/my/project/docs"` is in your `main.go` so the UI loads the correct spec.
3. **Use Structs for Body Params** — Never use primitive types for `@Param body`. Create a dedicated request struct instead.
4. **Group by Tags** — Use `@Tags` to group related endpoints in the Swagger UI.
5. **Secure the UI** — Disable the Swagger UI in production or protect it behind authentication.

## Anti-patterns

- ❌ **Stale Documentation** — Forgetting to run `swag init` leads to docs that don't match the code.
- ❌ **No Security Definitions** — Testers can't use the "Authorize" button in Swagger UI.
- ❌ **Unclear Error Responses** — Not documenting `@Failure` codes makes the API hard to integrate with.
- ❌ **Implicit Types** — Relying on swag to guess types for complex fields. Use `swaggertype` to be explicit.
- ❌ **Hardcoded Host** — Don't hardcode `@host` if the API runs in multiple environments; use relative paths or environment variables.
