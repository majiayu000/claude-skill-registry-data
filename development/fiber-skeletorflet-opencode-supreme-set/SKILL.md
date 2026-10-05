---
name: fiber
description: Fiber Go web framework. Use when building Express-like Go APIs, middleware chains, static file serving, the Fiber client, WebSocket endpoints, or request validation.
---

## fiber

Express-inspired Go framework built on fasthttp for zero-allocation performance.

### Core Concepts
- Express-like API: familiar syntax with `app.Get()`, `app.Post()`, route parameters and query strings
- Middleware: `app.Use()` for global middleware, `app.Group().Use()` for scoped chains
- Static files: `app.Static("/", "./public")` for directory serving with caching headers
- Fiber client: built-in HTTP client with `client.Get()` for outbound requests and retries

### Common Patterns
- WebSocket: `app.Get("/ws", websocket.New(func(c *websocket.Conn) {}))` for real-time connections
- Validation: `validate := validator.New()` with struct tags for request body validation
- Error handling: custom `ErrorHandler` in `app.Config` for centralized error response formatting
- Testing: `app.Test()` method sends requests directly without external server process

### Best Practices
- Use `fiber.Map` for JSON response construction instead of anonymous structs in handlers
- Initialize `validator` globally and use `validate.Struct()` for consistent validation
- Group routes by domain with `app.Group("/api/v1")` and dedicated middleware per group
- Configure `Prefork: true` for multi-CPU scaling in production deployments behind a load balancer

### Common Code Patterns
- `app.Get("/user/:id", func(c *fiber.Ctx) error { return c.JSON(fiber.Map{"id": c.Params("id")}) })`
- `app.Use(logger.New())` for request logging, `app.Use(recover.New())` for panic recovery
