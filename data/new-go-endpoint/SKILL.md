---
name: new-go-endpoint
description: This skill automates the API-first workflow for creating new Go API endpoints. It handles OpenAPI spec updates, code generation, SQLC query creation, handler implementation, and Redis caching patterns. Use when adding new endpoints to the Lexicon backend.
---

<objective>
Automate the complete workflow for adding new API endpoints to the Lexicon Go backend, following API-first development principles.
</objective>

<workflow>
## Step 1: Gather Requirements

Ask the user for:
1. **Endpoint path** (e.g., `/api/v1/beneficial-ownership/search`)
2. **HTTP method** (GET, POST, PUT, DELETE)
3. **Purpose** - Brief description of what the endpoint does
4. **Request parameters** - Query params, path params, or request body
5. **Response structure** - What data should be returned
6. **Caching requirements** - Should this endpoint use Redis caching?
7. **Database query needed** - Does this need a new SQLC query?

## Step 2: Update OpenAPI Spec

Edit `api/openapi.yaml` to add:
- New path and operation
- Request parameters/body schema
- Response schema with all fields
- Proper tags for grouping

**Template for new endpoint:**
```yaml
  /api/v1/{resource}:
    get:
      summary: Brief description
      operationId: GetResource
      tags:
        - resource
      parameters:
        - name: param
          in: query
          schema:
            type: string
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResourceResponse'
```

## Step 3: Generate API Code

Run code generation:
```bash
make api-generate
```

This generates `internal/api/api.gen.go` with:
- Request/response types
- Server interface with new method signature

## Step 4: Create SQLC Query (if needed)

Add query to `internal/db/queries/{resource}.sql`:

**Query patterns from this codebase:**
```sql
-- Array-based filtering (prevents SQL injection)
-- name: SearchCases :many
SELECT * FROM bo_v1.cases
WHERE (cardinality($1::int[]) = 0 OR subject_type = ANY($1::int[]))
AND (cardinality($2::text[]) = 0 OR LOWER(nation) = ANY($2::text[]))
LIMIT $3 OFFSET $4;

-- Count query for pagination
-- name: CountCases :one
SELECT COUNT(*) FROM bo_v1.cases
WHERE (cardinality($1::int[]) = 0 OR subject_type = ANY($1::int[]));
```

Then generate:
```bash
make sqlc-generate
```

## Step 5: Implement Handler

Add handler in `internal/api/handlers.go`:

**Handler template with caching:**
```go
func (s *Server) GetResource(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()

    // Parse parameters
    params := r.URL.Query()

    // Check cache (if applicable)
    cacheKey := "resource:key"
    if cached, err := s.redis.Get(ctx, cacheKey).Result(); err == nil {
        var result ResourceResponse
        if err := json.Unmarshal([]byte(cached), &result); err == nil {
            respondJSON(w, http.StatusOK, result)
            return
        }
    }

    // Query database
    data, err := s.queries.GetResource(ctx, db.GetResourceParams{...})
    if err != nil {
        respondError(w, http.StatusInternalServerError, "Failed to fetch resource")
        return
    }

    // Map to response
    response := mapToResourceResponse(data)

    // Cache result (5 minute TTL)
    if jsonData, err := json.Marshal(response); err == nil {
        s.redis.Set(ctx, cacheKey, jsonData, 5*time.Minute)
    }

    respondJSON(w, http.StatusOK, response)
}
```

**Handler template without caching:**
```go
func (s *Server) GetResource(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()

    // Parse and validate parameters
    // ...

    // Query database
    data, err := s.queries.GetResource(ctx, params)
    if err != nil {
        respondError(w, http.StatusInternalServerError, "Failed to fetch resource")
        return
    }

    respondJSON(w, http.StatusOK, mapToResponse(data))
}
```

## Step 6: Add Route

Add route in `internal/api/routes.go` if not auto-registered.

## Step 7: Type Mapping Helpers

For SQLC queries with CASE expressions, add helper functions:

```go
// Convert nullable interface{} to string (for CASE expressions)
func convertLabel(label interface{}) string {
    if label == nil {
        return ""
    }
    if str, ok := label.(string); ok {
        return str
    }
    return fmt.Sprintf("%v", label)
}

// Map database int codes to API string enums
func mapSubjectType(code int32) string {
    switch code {
    case 1: return "individual"
    case 2: return "company"
    case 3: return "organization"
    default: return "unknown"
    }
}
```

## Step 8: Test the Endpoint

Run the server and test with curl:
```bash
make api-dev
curl -X GET "http://localhost:8080/api/v1/{resource}?param=value" | jq
```
</workflow>

<validation_patterns>
## ULID Validation
```go
var ulidRegex = regexp.MustCompile(`^[0-9A-HJKMNP-TV-Z]{26}$`)

func isValidULID(id string) bool {
    return ulidRegex.MatchString(id)
}
```

## Year Range Validation
```go
const (
    MinYear = 1900
    MaxYear = 2100
    MaxYearSpan = 50
)

func validateYearRange(startYear, endYear int) error {
    if startYear < MinYear || endYear > MaxYear {
        return errors.New("year out of range")
    }
    if endYear - startYear > MaxYearSpan {
        return errors.New("year range too large")
    }
    return nil
}
```
</validation_patterns>

<cache_keys>
## Standard Cache Key Patterns

| Pattern | TTL | Example |
|---------|-----|---------|
| `chart:{type}` | 5 min | `chart:countries` |
| `lkpp:{type}` | 5 min | `lkpp:province` |
| `filter:{hash}` | 1 min | `filter:abc123` |
| `search:{hash}` | 30 sec | `search:def456` |
</cache_keys>

<success_criteria>
Endpoint creation is complete when:
- [ ] OpenAPI spec updated with full schema
- [ ] `make api-generate` runs without errors
- [ ] SQLC query added (if needed)
- [ ] `make sqlc-generate` runs without errors
- [ ] Handler implemented with proper error handling
- [ ] Route registered
- [ ] Tested with curl and response documented
- [ ] `make check` passes (lint + tests)
</success_criteria>
