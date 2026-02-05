---
name: pagination-endpoint
description: Guide for creating paginated list endpoints with cursor-based pagination and RFC 8288 Link headers following this project's conventions.
---

# Pagination Endpoint Creation

Use this skill when creating paginated list endpoints for this Huma REST API application.

For comprehensive pagination guidelines, see `AGENTS.md` in the repository root.

## Pagination Package

The project uses cursor-based pagination via `internal/pagination`:

- `pagination.Params` - Embeddable query parameters (cursor, limit)
- `pagination.Cursor` - Decoded cursor with type and value
- `pagination.Paginate` - Generic pagination helper
- `pagination.DecodeCursor` / `Cursor.Encode()` - Cursor encoding/decoding

## Input Struct Pattern

Embed `pagination.Params` for standard pagination query parameters:

```go
type ListResourcesInput struct {
    pagination.Params
    Category string `query:"category" doc:"Filter by category" example:"active" enum:"active,inactive"`
    SortBy   string `query:"sortBy"   doc:"Sort field"         example:"createdAt" enum:"createdAt,name"`
}
```

`pagination.Params` provides:
- `Cursor string` - Opaque pagination cursor
- `Limit int` - Items per page (default 20, max 100)
- `DefaultLimit()` - Returns limit with default applied

## Output Struct Pattern

Include Link header for RFC 8288 pagination links:

```go
type ResourcesData struct {
    Resources []Resource `json:"resources" doc:"List of resources"`
    Total     int        `json:"total"     doc:"Total count matching filter" example:"100"`
}

type ListResourcesOutput struct {
    Link string `header:"Link" doc:"RFC 8288 pagination links"`
    Body ResourcesData
}
```

## Handler Implementation

```go
const resourceCursorType = "resource"

func registerResources(api huma.API) {
    huma.Register(api, huma.Operation{
        OperationID: "list-resources",
        Method:      http.MethodGet,
        Path:        "/resources",
        Summary:     "List resources with cursor-based pagination",
        Description: "Returns a paginated list. Use the cursor from the Link header to navigate.",
        Tags:        []string{"Resources"},
    }, func(ctx context.Context, input *ListResourcesInput) (*ListResourcesOutput, error) {
        // 1. Decode and validate cursor
        cursor, err := pagination.DecodeCursor(input.Cursor)
        if err != nil {
            return nil, huma.Error400BadRequest("invalid cursor format")
        }

        // 2. Validate cursor type matches endpoint
        if cursor.Type != "" && cursor.Type != resourceCursorType {
            return nil, huma.Error400BadRequest("cursor type mismatch")
        }

        // 3. Apply filters
        filtered := filterResources(allResources, input.Category)

        // 4. Validate cursor references existing item
        if cursor.Value != "" && !resourceExists(filtered, cursor.Value) {
            return nil, huma.Error400BadRequest("cursor references unknown item")
        }

        // 5. Build query params for Link header
        query := url.Values{}
        if input.Category != "" {
            query.Set("category", input.Category)
        }

        // 6. Paginate using helper
        result := pagination.Paginate(
            filtered,
            cursor,
            input.DefaultLimit(),
            resourceCursorType,
            func(r Resource) string { return r.ID },
            "/resources",
            query,
        )

        return &ListResourcesOutput{
            Link: result.LinkHeader,
            Body: ResourcesData{
                Resources: result.Items,
                Total:     result.Total,
            },
        }, nil
    })
}
```

## Cursor Validation Rules

Invalid cursors MUST return 400 Bad Request:

```go
// Decode error (malformed base64, invalid JSON)
cursor, err := pagination.DecodeCursor(input.Cursor)
if err != nil {
    return nil, huma.Error400BadRequest("invalid cursor format")
}

// Type mismatch (cursor from different endpoint)
if cursor.Type != "" && cursor.Type != resourceCursorType {
    return nil, huma.Error400BadRequest("cursor type mismatch")
}

// Invalid reference (cursor points to deleted/nonexistent item)
if cursor.Value != "" && !resourceExists(filtered, cursor.Value) {
    return nil, huma.Error400BadRequest("cursor references unknown item")
}
```

## Cursor Type Constants

Define a constant for each paginated endpoint to prevent cursor reuse:

```go
const (
    itemCursorType     = "item"
    resourceCursorType = "resource"
    userCursorType     = "user"
)
```

## Pagination Helper

The `pagination.Paginate` function handles:
- Finding start position from cursor
- Slicing items to requested limit
- Generating next cursor
- Building RFC 8288 Link header

```go
result := pagination.Paginate(
    items,           // []T - full filtered slice
    cursor,          // Cursor - decoded cursor
    limit,           // int - items per page
    cursorType,      // string - cursor type constant
    getID,           // func(T) string - ID extractor
    basePath,        // string - endpoint path for links
    query,           // url.Values - preserved query params
)

// result.Items      - []T paginated items
// result.Total      - int total count before pagination
// result.LinkHeader - string RFC 8288 Link header
```

## Link Header Format

The Link header follows RFC 8288:

```
Link: </resources?cursor=eyJ0Ijoi...>; rel="next"
```

Multiple links are comma-separated:

```
Link: </resources?cursor=abc>; rel="next", </resources>; rel="first"
```

## Filter Helper Pattern

Create filter functions for query parameters:

```go
func filterResources(resources []Resource, category string) []Resource {
    if category == "" {
        return resources
    }
    return slices.DeleteFunc(slices.Clone(resources), func(r Resource) bool {
        return r.Category != category
    })
}
```

## ID Extractor Pattern

The paginator needs a function to extract IDs for cursor generation:

```go
// Inline function
func(r Resource) string { return r.ID }

// Or named function for reuse
func resourceID(r Resource) string {
    return r.ID
}
```

## Query Parameter Preservation

Preserve filter parameters in pagination links:

```go
query := url.Values{}
if input.Category != "" {
    query.Set("category", input.Category)
}
if input.SortBy != "" {
    query.Set("sortBy", input.SortBy)
}
```

## Testing Paginated Endpoints

```go
func TestListResources_Pagination(t *testing.T) {
    router := setupTestRouter()

    // First page
    req := httptest.NewRequest(http.MethodGet, "/resources?limit=5", nil)
    resp := httptest.NewRecorder()
    router.ServeHTTP(resp, req)

    if resp.Code != http.StatusOK {
        t.Fatalf("expected 200, got %d", resp.Code)
    }

    link := resp.Header().Get("Link")
    if !strings.Contains(link, `rel="next"`) {
        t.Error("expected next link")
    }

    var body ResourcesData
    json.Unmarshal(resp.Body.Bytes(), &body)
    if len(body.Resources) != 5 {
        t.Errorf("expected 5 items, got %d", len(body.Resources))
    }
}

func TestListResources_InvalidCursor(t *testing.T) {
    router := setupTestRouter()

    req := httptest.NewRequest(http.MethodGet, "/resources?cursor=invalid", nil)
    resp := httptest.NewRecorder()
    router.ServeHTTP(resp, req)

    if resp.Code != http.StatusBadRequest {
        t.Fatalf("expected 400, got %d", resp.Code)
    }
}

func TestListResources_CursorTypeMismatch(t *testing.T) {
    router := setupTestRouter()

    // Create a cursor with wrong type
    wrongCursor := pagination.Cursor{
        Type:  "other-type",
        Value: "item-001",
    }.Encode()

    req := httptest.NewRequest(http.MethodGet, "/resources?cursor="+wrongCursor, nil)
    resp := httptest.NewRecorder()
    router.ServeHTTP(resp, req)

    if resp.Code != http.StatusBadRequest {
        t.Fatalf("expected 400, got %d", resp.Code)
    }
}
```

## Complete Example

See [internal/http/v1/items/handler.go](internal/http/v1/items/handler.go) for a complete implementation.
