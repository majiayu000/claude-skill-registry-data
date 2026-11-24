---
name: spring-boot-api-contracts
description: >
  Design of idiomatic REST contracts in Spring Boot 4.x: RFC 9457 (ProblemDetail)
  normalized errors, consistent pagination, API versioning, OpenAPI documentation
  with springdoc, and decisions around HATEOAS/built-in versioning. Use when
  designing endpoints, refactoring controller responses, or building APIs for
  external consumers.
---

# REST API Contracts

## Contract deliverable

Inspect existing clients, controllers and published OpenAPI first. Produce method/path, request shape, success/error responses, authorization, pagination/versioning choices and compatibility impact. Mark which choices are existing requirements versus proposed conventions. `openapi_endpoints` can compare a live OpenAPI document with static mappings; static route evidence alone is not an OpenAPI specification.

The wrapper below is an optional convention. Preserve an established raw-resource, HAL or pagination contract unless changing it is explicitly in scope. State how consumers migrate before introducing a new envelope or version.

## Unified response format

If the project chooses an envelope, use it for body-bearing success responses; errors use RFC 9457 (`ProblemDetail`).

| Code | Body                                           |
|------|------------------------------------------------|
| 200  | `{ "data": <T>, "meta": { ... } }`             |
| 201  | `{ "data": <T> }` + `Location:` header         |
| 204  | (no body)                                      |
| 4xx  | `ProblemDetail` (RFC 9457)                     |
| 5xx  | `ProblemDetail` (no stack details, only traceId) |

### Pagination

```java
public record PageResponse<T>(
    @JsonProperty("data") List<T> items,
    @JsonProperty("meta") PageMeta meta
) {}

public record PageMeta(
    int page, int size,
    long totalElements, int totalPages,
    boolean first, boolean last
) {}
```

> **JSON stack:** Boot 4 defaults to **Jackson 3** (`tools.jackson` package). Import Jackson databind from `tools.jackson.*`; shared annotations such as `@JsonProperty` remain under `com.fasterxml.jackson.annotation.*` — do not import `com.fasterxml.jackson.databind.*` in application code.

**Controller request params**: `page` (0-based, default 0), `size` (default 20, max 1000). Return the pagination metadata chosen by the existing contract; set limits from the service capacity.

### Errors (RFC 9457)

Spring Framework 7 + Boot 4.1 has built-in support for `ProblemDetail`. Enable it:

```yaml
spring.mvc.problemdetails.enabled: true
```

Response (the `traceId` extension is added by the application, e.g. via `setProperty` in an advice; the property does not produce it):
```json
{
  "type": "about:blank",
  "title": "Not Found",
  "status": 404,
  "detail": "User with id 42 not found",
  "instance": "/api/v1/users/42",
  "traceId": "abc-123"
}
```

```java
import java.util.List;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.ErrorResponseException;

public final class ApiErrors {
    public static ErrorResponseException invalidEmail(String traceId) {
        var problem = ProblemDetail.forStatusAndDetail(
            HttpStatus.BAD_REQUEST, "Request validation failed");
        problem.setProperty("traceId", traceId);
        problem.setProperty("errors", List.of(Map.of(
            "field", "email", "message", "must be a valid email")));
        return new ErrorResponseException(HttpStatus.BAD_REQUEST, problem, null);
    }
}
```

**Never** return validation errors as flat arrays; use `"errors": [ { "field": "email", "message": "must be a valid email" } ]` as a top-level extension via `problem.setProperty("errors", errors)`. Keep `detail` a string. Map Bean Validation failures in a `@RestControllerAdvice` or `ResponseEntityExceptionHandler` override.

### API versioning

Spring Framework 7 ships **built-in API versioning** (configured via `WebMvcConfigurer`), for resolving and matching request versions:

```java
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.ApiVersionConfigurer;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class ApiVersionConfig implements WebMvcConfigurer {
    @Override
    public void configureApiVersioning(ApiVersionConfigurer config) {
        // /api/v1/users: version from segment 1, only for /api paths (Framework 7.0.6+).
        // Without the predicate, every other handler-mapped path fails version resolution (400).
        config.usePathSegment(1, path -> path.pathWithinApplication().value().startsWith("/api/"));
        config.setDefaultVersion("1"); // unversioned paths resolve to null; a default keeps them valid
    }
}
```

For path-based versioning, map a variable version segment (for example `@GetMapping(path = "/api/{version}/users", version = "1")`) so the resolver sees that segment. Define supported versions and test missing/unsupported versions plus an unversioned endpoint outside `/api`. Choose retirement timing from the consumer support policy; keep old contracts until the agreed sunset date.

### Calling other services: HTTP interface clients

Framework 7 provides declarative HTTP interface clients — use them instead of ad-hoc `RestTemplate`/`WebClient` code:

```java
public interface UserClient {

    @GetExchange("/api/v1/users/{id}")
    UserDTO getUser(@PathVariable Long id);

    @PostExchange("/api/v1/users")
    UserDTO create(@RequestBody CreateUserRequest request);
}

@Configuration
public class UserClientConfig {

    @Bean
    UserClient userClient(RestClient.Builder builder) {
        var restClient = builder.baseUrl("http://users-service").build();
        var httpServiceAdapter = HttpServiceProxyFactory
            .builderFor(RestClientAdapter.create(restClient))
            .build();
        return httpServiceAdapter.createClient(UserClient.class);
    }
}
```

Use `RestClient` (synchronous) or `WebClient` (reactive) as the underlying transport; `RestTemplate` is legacy and should not appear in new code.

### OpenAPI with springdoc

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-api</artifactId>
    <version>3.2.0</version> <!-- verified 2026-11-10 for Boot 4.1.x; Boot 4.0.x uses springdoc 3.0.x -->
</dependency>
```

```java
@Operation(summary = "Search users", description = "Paginated user search by filters")
@GetMapping("/api/v1/users")
public ResponseEntity<PageResponse<UserDTO>> search(
    @ParameterObject @Valid UserFilter filter,
    @RequestParam(defaultValue = "0") int page,
    @RequestParam(defaultValue = "20") int size) { ... }
```

OpenAPI endpoint: `GET /v3/api-docs` (default) or `GET /api-docs` if configured.

### DTOs

- Input: records with Bean Validation (`@NotBlank`, `@Email`, `@Size`, etc.)
- Output: immutable records, no circular JPA relationships
- Mappers: MapStruct (interface, `@Mapper` annotation) or manual field-by-field mapping
- **Nullability:** packages are `@NullMarked` via `package-info.java`; use `@Nullable` (e.g. `org.jspecify.annotations.Nullable`) on record components and fields where null is allowed. Do not use Spring's `org.springframework.lang` nullability annotations — they are deprecated.
- **Never expose JPA entities as responses** — always go through DTOs.
- Dates in ISO 8601 UTC (`2026-10-06T14:30:00Z`).

## References

- [Spring MVC ProblemDetail](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-rest-exceptions.html)
- [springdoc artifacts and Boot compatibility](https://springdoc.org/)
- [Framework API version path variables](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-config/api-version.html)

Use springdoc `webmvc-ui` instead of `webmvc-api` when Swagger UI is needed; verify its compatibility matrix against the project Boot release before upgrading.
