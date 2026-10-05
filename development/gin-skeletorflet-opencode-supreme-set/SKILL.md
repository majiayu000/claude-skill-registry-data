---
name: gin
description: Gin Go web framework. Use when building high-performance Go APIs, middleware chains, JSON/XML binding with validation, route grouping, or testing with httptest.
---

## gin

Fast Go HTTP framework with zero-allocation router and minimal memory footprint.

### Core Concepts
- Fast routing: radix tree-based router with `gin.Default()` for logger and recovery middleware
- Middleware chains: `r.Use()` for global middleware, group-level chains for scoped behavior
- JSON/XML binding: `c.ShouldBindJSON()` with struct tags for automatic request validation
- Route grouping: `v1 := r.Group("/api/v1")` with shared middleware and URL prefixes

### Common Patterns
- File uploads: `c.FormFile("file")` with `c.SaveUploadedFile()` for multipart form handling
- Custom middleware: `func() gin.HandlerFunc` closure pattern for request-scoped data injection
- Error handling: `c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})` for structured errors
- Testing: `httptest.NewRecorder()` with `r.ServeHTTP()` for integration tests without server

### Best Practices
- Use `ShouldBindJSON` for strict validation, `ShouldBindBodyWith` for content-type negotiation
- Validate structs with `binding` tags (required, min, max, oneof) rather than manual checks
- Group routes by version and domain for maintainable API organization
- Use `c.Set()`/`c.Get()` for request-scoped values like user identity from auth middleware

### Common Code Patterns
- `r.GET("/ping", func(c *gin.Context) { c.JSON(200, gin.H{"message": "pong"}) })`
- `authorized := r.Group("/", AuthRequired()); authorized.POST("/items", createItem)`
