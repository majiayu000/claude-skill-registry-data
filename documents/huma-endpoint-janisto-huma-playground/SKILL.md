---
name: huma-endpoint
description: Guide for creating Huma API endpoints following this project's conventions including routing, input/output structs, error handling, and OpenAPI documentation.
---

# Huma Endpoint Creation

Use this skill when creating new API endpoints for this Huma REST API application.

For comprehensive coding guidelines, see `AGENTS.md` in the repository root.

## Router Setup

Create route handlers in `internal/http/v1/` and register them in `routes.go`:

```go
// internal/http/v1/routes/routes.go
func Register(api huma.API) {
    hello.Register(api)
    items.Register(api)
    // Add new routes here
}
```

Note: The health endpoint is a plain HTTP handler registered at the root level in `main.go`, not via Huma.

## Output Struct Pattern

Use plain structs with a `Body` field for the response payload:

```go
import "github.com/janisto/huma-playground/internal/platform/timeutil"

// ResourceData models the response payload.
type ResourceData struct {
    ID        string      `json:"id"        doc:"Unique identifier"   example:"res-001"`
    Name      string      `json:"name"      doc:"Display name"        example:"My Resource"`
    CreatedAt timeutil.Time `json:"createdAt" doc:"Creation timestamp"  example:"2024-01-15T10:30:00.000Z"`
}

// ResourceOutput is the response wrapper.
type ResourceOutput struct {
    Body ResourceData
}
```

## Input Struct Pattern

Define input structs for path parameters, query parameters, and request bodies:

```go
// Path parameters
type ResourceInput struct {
    ID string `path:"id" doc:"Resource identifier" example:"res-001"`
}

// Query parameters
type ListInput struct {
    Status string `query:"status" doc:"Filter by status" example:"active" enum:"active,inactive"`
    Limit  int    `query:"limit"  doc:"Maximum items"    example:"10"     minimum:"1" maximum:"100"`
}

// Request body
type CreateResourceInput struct {
    Body struct {
        Name string `json:"name" doc:"Resource name" example:"New Resource" minLength:"1" maxLength:"100"`
    }
}
```

## GET Endpoint

Simple retrieval endpoints use `huma.Get`:

```go
func registerResource(api huma.API) {
    huma.Get(api, "/resources/{id}", func(ctx context.Context, input *ResourceInput) (*ResourceOutput, error) {
        resource, err := getResource(input.ID)
        if err != nil {
            return nil, huma.Error404NotFound("resource not found")
        }
        return &ResourceOutput{Body: resource}, nil
    })
}
```

## POST Endpoint with 201 Created

Use `huma.Register` for operations requiring custom configuration:

```go
type CreateResourceOutput struct {
    Location string `header:"Location" doc:"URL of created resource"`
    Body     ResourceData
}

huma.Register(api, huma.Operation{
    OperationID:   "create-resource",
    Method:        http.MethodPost,
    Path:          "/resources",
    Summary:       "Create a new resource",
    Description:   "Creates a new resource and returns its data.",
    DefaultStatus: http.StatusCreated,
    Tags:          []string{"Resources"},
}, func(ctx context.Context, input *CreateResourceInput) (*CreateResourceOutput, error) {
    resource := createResource(input.Body.Name)
    return &CreateResourceOutput{
        Location: fmt.Sprintf("/resources/%s", resource.ID),
        Body:     resource,
    }, nil
})
```

## PUT/PATCH Endpoint

```go
type UpdateResourceInput struct {
    ID   string `path:"id"`
    Body struct {
        Name string `json:"name" doc:"Updated name" minLength:"1" maxLength:"100"`
    }
}

huma.Register(api, huma.Operation{
    OperationID: "update-resource",
    Method:      http.MethodPut,
    Path:        "/resources/{id}",
    Summary:     "Update a resource",
    Tags:        []string{"Resources"},
}, func(ctx context.Context, input *UpdateResourceInput) (*ResourceOutput, error) {
    resource, err := updateResource(input.ID, input.Body.Name)
    if err != nil {
        return nil, huma.Error404NotFound("resource not found")
    }
    return &ResourceOutput{Body: resource}, nil
})
```

## DELETE Endpoint

Return 204 No Content for successful deletions:

```go
huma.Register(api, huma.Operation{
    OperationID:   "delete-resource",
    Method:        http.MethodDelete,
    Path:          "/resources/{id}",
    Summary:       "Delete a resource",
    DefaultStatus: http.StatusNoContent,
    Tags:          []string{"Resources"},
}, func(ctx context.Context, input *ResourceInput) (*struct{}, error) {
    if err := deleteResource(input.ID); err != nil {
        return nil, huma.Error404NotFound("resource not found")
    }
    return nil, nil
})
```

## Error Handling

Use Huma's built-in error helpers for RFC 9457 Problem Details:

```go
// Common error responses
huma.Error400BadRequest("invalid request")
huma.Error403Forbidden("access denied")
huma.Error404NotFound("resource not found")
huma.Error422UnprocessableEntity("validation failed", fieldErrors...)
huma.Error500InternalServerError("internal error")

// Custom status codes
huma.NewError(http.StatusTeapot, "custom message")
huma.NewError(http.StatusConflict, "resource already exists")
```

## Logging

Use context-aware logging helpers:

```go
import (
    "go.uber.org/zap"
    applog "github.com/janisto/huma-playground/internal/platform/logging"
)

func handler(ctx context.Context, input *Input) (*Output, error) {
    applog.LogInfo(ctx, "processing request", zap.String("id", input.ID))

    if err != nil {
        applog.LogError(ctx, "operation failed", err, zap.String("id", input.ID))
        return nil, huma.Error500InternalServerError("operation failed")
    }

    return &Output{Body: result}, nil
}
```

## Field Documentation

Every field MUST have:
- `doc:` tag for OpenAPI description
- `example:` tag for OpenAPI examples

Validation tags:
- `minLength`, `maxLength` for strings
- `minimum`, `maximum` for numbers
- `enum:` for allowed values
- `pattern:` for regex validation

## Status Code Reference

| Method | Success Status | Use Case |
|--------|----------------|----------|
| GET    | 200 OK         | Retrieve resource(s) |
| POST   | 201 Created    | Create resource (include Location header) |
| PUT    | 200 OK         | Replace resource |
| PATCH  | 200 OK         | Partial update |
| DELETE | 204 No Content | Remove resource |

## Error Status Codes

| Status | Use Case |
|--------|----------|
| 400    | Malformed syntax, invalid cursor |
| 401    | Missing authentication |
| 403    | Authenticated but not authorized |
| 404    | Resource not found |
| 409    | Conflict (duplicate resource) |
| 422    | Validation failures |
| 500    | Unexpected server error |
