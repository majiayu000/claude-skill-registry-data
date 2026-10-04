---
name: api-design
description: "Design and document REST APIs following industry best practices: URL conventions, HTTP semantics, versioning, pagination, error formats, and OpenAPI/Swagger annotations. Use this skill whenever the user wants to design an API, define endpoints, create an API contract, add OpenAPI documentation, review API naming, or says things like \"design the API for X\", \"what endpoints do I need for X\", \"how should I structure this REST API\", \"add Swagger docs\", \"define the API contract\". Always use this skill for any REST API design or documentation task."
---

# REST API Design Skill

Design clean, consistent, and well-documented REST APIs following HTTP semantics and industry conventions.

## URL Design Rules

### Resource Naming
- Use **nouns**, never verbs: `/users` not `/getUsers`
- Use **plural** for collections: `/products`, `/orders`
- Use **kebab-case** for multi-word: `/order-items`, `/payment-methods`
- Nest resources to show ownership (max 2 levels deep):
  ```
  /users/{userId}/orders          ✅
  /users/{userId}/orders/{orderId}/items/{itemId}  ❌ too deep
  ```

### HTTP Methods Mapping
| Action | Method | URL | Response |
|--------|--------|-----|----------|
| List all | GET | `/resources` | 200 + array |
| Get one | GET | `/resources/{id}` | 200 + object |
| Create | POST | `/resources` | 201 + created object |
| Full update | PUT | `/resources/{id}` | 200 + updated object |
| Partial update | PATCH | `/resources/{id}` | 200 + updated object |
| Delete | DELETE | `/resources/{id}` | 204 no body |
| Search/filter | GET | `/resources?status=ACTIVE&sort=name` | 200 + array |

### Non-CRUD Actions
Use sub-resources or action endpoints:
```
POST /orders/{id}/cancel         ✅
POST /orders/{id}/items          ✅
POST /users/{id}/password-reset  ✅
GET  /cancelOrder/{id}           ❌
```

## Versioning Strategy

Always version APIs in the URL path:
```
/api/v1/users
/api/v2/users
```

Spring Boot configuration:
```java
@RequestMapping("/api/v1/users")
public class UserController { ... }
```

## Pagination

Standard query parameters:
```
GET /products?page=0&size=20&sort=name,asc&sort=createdAt,desc
```

Standard response envelope:
```json
{
  "content": [...],
  "page": 0,
  "size": 20,
  "totalElements": 150,
  "totalPages": 8,
  "first": true,
  "last": false
}
```

Spring Boot implementation:
```java
@GetMapping
public ResponseEntity<Page<ProductResponse>> findAll(
    @PageableDefault(size = 20, sort = "name") Pageable pageable) {
    return ResponseEntity.ok(service.findAll(pageable));
}
```

## Standard Error Response Format

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "status": 404,
  "error": "Not Found",
  "message": "User with id 42 was not found",
  "path": "/api/v1/users/42",
  "traceId": "abc123"
}
```

For validation errors (400):
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "status": 400,
  "error": "Validation Failed",
  "message": "Request validation failed",
  "path": "/api/v1/users",
  "violations": [
    { "field": "email", "message": "must be a valid email address" },
    { "field": "name", "message": "must not be blank" }
  ]
}
```

## OpenAPI / Swagger Annotations

```java
@Tag(name = "Users", description = "User management operations")
@RestController
@RequestMapping("/api/v1/users")
public class UserController {

    @Operation(
        summary = "Create a new user",
        description = "Creates a user and sends a welcome email"
    )
    @ApiResponses({
        @ApiResponse(responseCode = "201", description = "User created",
            content = @Content(schema = @Schema(implementation = UserResponse.class))),
        @ApiResponse(responseCode = "400", description = "Validation error",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))),
        @ApiResponse(responseCode = "409", description = "Email already exists")
    })
    @PostMapping
    public ResponseEntity<UserResponse> create(
        @Valid @RequestBody @io.swagger.v3.oas.annotations.parameters.RequestBody(
            description = "User creation request"
        ) CreateUserRequest request) { ... }
}
```

## Filtering, Sorting, and Searching

Use Spring's `@RequestParam` with sensible defaults:
```java
@GetMapping
public ResponseEntity<Page<ProductResponse>> search(
    @RequestParam(required = false) String name,
    @RequestParam(required = false) String category,
    @RequestParam(required = false) BigDecimal minPrice,
    @RequestParam(required = false) BigDecimal maxPrice,
    @RequestParam(defaultValue = "ACTIVE") ProductStatus status,
    @PageableDefault(size = 20) Pageable pageable) { ... }
```

For complex filtering, use a dedicated `@RequestParam`-based Specification pattern (Spring Data JPA Specifications).

## Security Headers Conventions

Always document authentication requirements:
```java
@SecurityRequirement(name = "bearerAuth")
```

OpenAPI security config:
```java
@Bean
public OpenAPI openAPI() {
    return new OpenAPI()
        .addSecurityItem(new SecurityRequirement().addList("bearerAuth"))
        .components(new Components()
            .addSecuritySchemes("bearerAuth",
                new SecurityScheme().type(SecurityScheme.Type.HTTP)
                    .scheme("bearer").bearerFormat("JWT")));
}
```

## API Design Checklist

Before finalizing an API design, verify:
- [ ] URLs use nouns, plural, kebab-case
- [ ] HTTP methods match semantics
- [ ] All endpoints return correct HTTP status codes
- [ ] Pagination on all collection endpoints
- [ ] Standard error format on all error responses
- [ ] Request DTOs have Bean Validation annotations
- [ ] Response DTOs don't expose internal entity IDs or sensitive fields
- [ ] OpenAPI annotations on all endpoints
- [ ] API versioned in the URL
