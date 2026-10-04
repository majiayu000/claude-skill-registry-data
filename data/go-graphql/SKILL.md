---
name: go-graphql
description: "Implementing GraphQL APIs in Golang. Covers schema-first design, resolvers, and N+1 prevention with DataLoaders."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 06:45:00 GMT
---

## Core Principles

1. **Schema-First Design** — Write your GraphQL Schema Definition (SDL) first, then generate or map Go types to it.
2. **N+1 Prevention** — Always use DataLoaders for nested fields to batch database queries.
3. **Thin Resolvers** — Resolvers should only translate GraphQL inputs to business logic calls and format the output.
4. **Opaque IDs** — Use the `ID` scalar and avoid leaking internal database primary keys.
5. **Pagination** — Favor cursor-based pagination (Relay spec) over offset-based for large lists.

## Library Comparison

| Library | Type | Features |
| --- | --- | --- |
| **`99designs/gqlgen`** | Codegen | High performance, type-safe, best for large schemas. **Recommended.** |
| **`graph-gophers/graphql-go`** | Reflection | Simple setup, no code generation. |
| **`graphql-go/graphql`** | Code-first | Verbose, harder to maintain. Avoid for new projects. |

## DataLoaders (N+1 Prevention)

DataLoaders batch multiple individual requests into a single batch request (e.g., `SELECT * FROM users WHERE id IN (...)`).

**Important**: DataLoaders MUST be created **per-request** (e.g., in a middleware), never globally, to avoid cross-user data leakage and stale caches.

```go
func DataLoaderMiddleware(db *sql.DB, next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        ctx := context.WithValue(r.Context(), loadersKey, NewLoaders(db))
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}
```

## Error Handling

Don't leak internal errors (like SQL strings) to the client. Use a custom error presenter to strip sensitive details and add extension codes.

```go
// gqlgen example
srv.SetErrorPresenter(func(ctx context.Context, err error) *gqlerror.Error {
    if _, ok := err.(MySafeError); ok {
        return gqlerror.Errorf(err.Error())
    }
    log.Printf("Internal error: %v", err)
    return gqlerror.Errorf("internal server error")
})
```

## Security

1. **Introspection** — Disable GraphQL introspection in production to prevent API discovery.
2. **Complexity Limits** — Enforce query complexity limits to prevent Denial of Service (DoS) attacks via deeply nested queries.
3. **Depth Limits** — Restrict the maximum depth of a query.

## Anti-patterns

- ❌ **N+1 Queries** — Fetching child objects one by one in a loop inside a resolver.
- ❌ **Global DataLoaders** — Sharing cache between different users (Security Risk!).
- ❌ **SQL in Resolvers** — Business logic and data access should live in a separate service layer.
- ❌ **Leaking DB IDs** — Exposing internal `int` IDs. Use UUIDs or Base64-encoded IDs.
- ❌ **No Complexity Caps** — Allowing clients to send arbitrarily deep/expensive queries.
