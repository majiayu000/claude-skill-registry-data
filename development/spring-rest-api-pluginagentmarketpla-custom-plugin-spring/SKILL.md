---
name: spring-rest-api
description: Build production-ready REST APIs with Spring MVC - controllers, validation, exception handling, OpenAPI
sasmp_version: "1.3.0"
bonded_agent: 02-spring-mvc
bond_type: PRIMARY_BOND
version: "2.0.0"
updated: "2024-12-30"
---

# Spring REST API Skill

Master building robust, well-documented REST APIs with Spring MVC including validation, error handling, and OpenAPI documentation.

## Overview

This skill covers everything needed to build production-grade REST APIs following industry best practices.

## Parameters

| Name | Type | Required | Default | Validation |
|------|------|----------|---------|------------|
| `api_version` | string | ✗ | v1 | Pattern: v[0-9]+ |
| `content_type` | enum | ✗ | json | json \| xml \| both |
| `documentation` | enum | ✗ | openapi | openapi \| none |

## Topics Covered

### Core (Must Know)
- **REST Controllers**: `@RestController`, `@RequestMapping`
- **Request Handling**: Path variables, query params, request body
- **Response Building**: `ResponseEntity`, status codes
- **Bean Validation**: `@Valid`, `@NotNull`, custom validators

### Intermediate
- **Exception Handling**: `@ControllerAdvice`, Problem Details (RFC 7807)
- **Content Negotiation**: JSON/XML, custom converters
- **CORS Configuration**: Cross-origin resource sharing

### Advanced
- **HATEOAS**: Hypermedia-driven APIs
- **API Versioning**: URL, header strategies
- **OpenAPI Documentation**: springdoc-openapi

## Code Examples

### Complete REST Controller
```java
@RestController
@RequestMapping("/api/v1/products")
@RequiredArgsConstructor
public class ProductController {

    private final ProductService productService;

    @GetMapping
    public Page<ProductResponse> list(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        return productService.findAll(PageRequest.of(page, size));
    }

    @GetMapping("/{id}")
    public ProductResponse get(@PathVariable Long id) {
        return productService.findById(id);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public ProductResponse create(@Valid @RequestBody CreateProductRequest request) {
        return productService.create(request);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable Long id) {
        productService.delete(id);
    }
}
```

### Request DTO with Validation
```java
public record CreateProductRequest(
    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 100)
    String name,

    @NotNull @DecimalMin("0.01")
    BigDecimal price,

    @Size(max = 1000)
    String description
) {}
```

### Global Exception Handler
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ProblemDetail handleNotFound(ResourceNotFoundException ex) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(
            HttpStatus.NOT_FOUND, ex.getMessage());
        problem.setTitle("Resource Not Found");
        problem.setProperty("timestamp", Instant.now());
        return problem;
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail handleValidation(MethodArgumentNotValidException ex) {
        ProblemDetail problem = ProblemDetail.forStatus(HttpStatus.BAD_REQUEST);
        problem.setTitle("Validation Failed");
        Map<String, String> errors = ex.getBindingResult()
            .getFieldErrors().stream()
            .collect(Collectors.toMap(
                FieldError::getField,
                e -> e.getDefaultMessage() != null ? e.getDefaultMessage() : "Invalid"
            ));
        problem.setProperty("errors", errors);
        return problem;
    }
}
```

## Troubleshooting

### Failure Modes

| Issue | Diagnosis | Fix |
|-------|-----------|-----|
| 404 on valid path | Missing @RestController | Add annotation |
| Request body null | Missing @RequestBody | Add to parameter |
| Validation ignored | Missing @Valid | Add before @RequestBody |

### Debug Checklist

```
□ Verify @RestController on class
□ Check @RequestMapping path
□ Confirm @Valid on request body
□ Test with curl to isolate issues
□ Check Content-Type header
```

## Unit Test Template

```java
@WebMvcTest(ProductController.class)
class ProductControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private ProductService productService;

    @Test
    void shouldCreateProduct() throws Exception {
        mockMvc.perform(post("/api/v1/products")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\":\"Test\",\"price\":19.99}"))
            .andExpect(status().isCreated());
    }
}
```

## Usage

```
Skill("spring-rest-api")
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2024-12-30 | RFC 7807, OpenAPI, comprehensive examples |
| 1.0.0 | 2024-01-01 | Initial release |
