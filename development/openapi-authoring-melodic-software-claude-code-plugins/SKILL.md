---
name: openapi-authoring
description: Author and validate OpenAPI 3.1 specifications for REST API design, following API-first and contract-first development practices
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# OpenAPI Authoring Skill

## When to Use This Skill

Use this skill when:

- **Openapi Authoring tasks** - Working on author and validate openapi 3.1 specifications for rest api design, following api-first and contract-first development practices
- **Planning or design** - Need guidance on Openapi Authoring approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Author OpenAPI 3.1 specifications for REST API design using API-first methodology.

## OpenAPI 3.1 Structure

### Root Document

```yaml
openapi: "3.1.0"

info:
  title: "{Service Name} API"
  version: "1.0.0"
  description: |
    {Service description and purpose}
  contact:
    name: "{Team Name}"
    email: "{team@company.com}"
  license:
    name: "MIT"
    identifier: "MIT"

servers:
  - url: "https://api.example.com/v1"
    description: "Production"
  - url: "https://api.staging.example.com/v1"
    description: "Staging"
  - url: "http://localhost:5000/v1"
    description: "Local development"

tags:
  - name: "{Resource}"
    description: "Operations for {resource} management"

paths:
  # Path definitions

components:
  # Reusable components

security:
  - bearerAuth: []
```

### Path Operations

```yaml
paths:
  /resources:
    get:
      operationId: "listResources"
      summary: "List all resources"
      description: "Retrieves a paginated list of resources"
      tags:
        - Resources
      parameters:
        - $ref: "#/components/parameters/PageNumber"
        - $ref: "#/components/parameters/PageSize"
        - $ref: "#/components/parameters/SortBy"
      responses:
        "200":
          description: "Successful response"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ResourceListResponse"
        "400":
          $ref: "#/components/responses/BadRequest"
        "401":
          $ref: "#/components/responses/Unauthorized"

    post:
      operationId: "createResource"
      summary: "Create a new resource"
      description: "Creates a new resource with the provided data"
      tags:
        - Resources
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateResourceRequest"
      responses:
        "201":
          description: "Resource created"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ResourceResponse"
          headers:
            Location:
              description: "URL of the created resource"
              schema:
                type: string
                format: uri
        "400":
          $ref: "#/components/responses/BadRequest"
        "422":
          $ref: "#/components/responses/UnprocessableEntity"

  /resources/{resourceId}:
    parameters:
      - $ref: "#/components/parameters/ResourceId"

    get:
      operationId: "getResource"
      summary: "Get a resource by ID"
      description: "Retrieves a single resource by its unique identifier"
      tags:
        - Resources
      responses:
        "200":
          description: "Successful response"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ResourceResponse"
        "404":
          $ref: "#/components/responses/NotFound"

    put:
      operationId: "updateResource"
      summary: "Update a resource"
      description: "Replaces the entire resource with the provided data"
      tags:
        - Resources
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/UpdateResourceRequest"
      responses:
        "200":
          description: "Resource updated"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ResourceResponse"
        "404":
          $ref: "#/components/responses/NotFound"
        "409":
          $ref: "#/components/responses/Conflict"

    patch:
      operationId: "patchResource"
      summary: "Partially update a resource"
      description: "Updates specific fields of the resource"
      tags:
        - Resources
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/PatchResourceRequest"
      responses:
        "200":
          description: "Resource patched"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ResourceResponse"
        "404":
          $ref: "#/components/responses/NotFound"

    delete:
      operationId: "deleteResource"
      summary: "Delete a resource"
      description: "Permanently removes a resource"
      tags:
        - Resources
      responses:
        "204":
          description: "Resource deleted"
        "404":
          $ref: "#/components/responses/NotFound"
        "409":
          $ref: "#/components/responses/Conflict"
```

### Component Schemas

```yaml
components:
  schemas:
    # Request schemas
    CreateResourceRequest:
      type: object
      required:
        - name
        - type
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
          description: "Resource name"
          example: "My Resource"
        type:
          $ref: "#/components/schemas/ResourceType"
        description:
          type: string
          maxLength: 500
          description: "Optional description"
        metadata:
          type: object
          additionalProperties: true
          description: "Custom metadata key-value pairs"

    UpdateResourceRequest:
      allOf:
        - $ref: "#/components/schemas/CreateResourceRequest"

    PatchResourceRequest:
      type: object
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
        description:
          type: string
          maxLength: 500
      minProperties: 1

    # Response schemas
    ResourceResponse:
      type: object
      required:
        - id
        - name
        - type
        - createdAt
        - updatedAt
      properties:
        id:
          type: string
          format: uuid
          description: "Unique identifier"
          example: "550e8400-e29b-41d4-a716-446655440000"
        name:
          type: string
          description: "Resource name"
        type:
          $ref: "#/components/schemas/ResourceType"
        description:
          type: string
        metadata:
          type: object
          additionalProperties: true
        createdAt:
          type: string
          format: date-time
          description: "Creation timestamp (ISO 8601)"
        updatedAt:
          type: string
          format: date-time
          description: "Last update timestamp (ISO 8601)"
        _links:
          $ref: "#/components/schemas/ResourceLinks"

    ResourceListResponse:
      type: object
      required:
        - data
        - pagination
      properties:
        data:
          type: array
          items:
            $ref: "#/components/schemas/ResourceResponse"
        pagination:
          $ref: "#/components/schemas/Pagination"
        _links:
          $ref: "#/components/schemas/PaginationLinks"

    # Enums
    ResourceType:
      type: string
      enum:
        - standard
        - premium
        - enterprise
      description: "Type of resource"

    # Common schemas
    Pagination:
      type: object
      required:
        - page
        - pageSize
        - totalItems
        - totalPages
      properties:
        page:
          type: integer
          minimum: 1
          description: "Current page number"
        pageSize:
          type: integer
          minimum: 1
          maximum: 100
          description: "Items per page"
        totalItems:
          type: integer
          minimum: 0
          description: "Total number of items"
        totalPages:
          type: integer
          minimum: 0
          description: "Total number of pages"

    ResourceLinks:
      type: object
      properties:
        self:
          type: string
          format: uri
        collection:
          type: string
          format: uri

    PaginationLinks:
      type: object
      properties:
        self:
          type: string
          format: uri
        first:
          type: string
          format: uri
        prev:
          type: string
          format: uri
        next:
          type: string
          format: uri
        last:
          type: string
          format: uri

    # Error schemas
    ErrorResponse:
      type: object
      required:
        - type
        - title
        - status
      properties:
        type:
          type: string
          format: uri
          description: "URI reference identifying the problem type"
        title:
          type: string
          description: "Short, human-readable summary"
        status:
          type: integer
          description: "HTTP status code"
        detail:
          type: string
          description: "Human-readable explanation"
        instance:
          type: string
          format: uri
          description: "URI reference identifying the specific occurrence"
        errors:
          type: array
          items:
            $ref: "#/components/schemas/ValidationError"

    ValidationError:
      type: object
      required:
        - field
        - message
      properties:
        field:
          type: string
          description: "Field path (e.g., 'name' or 'address.city')"
        message:
          type: string
          description: "Validation error message"
        code:
          type: string
          description: "Error code for programmatic handling"
```

### Parameters and Responses

```yaml
components:
  parameters:
    ResourceId:
      name: resourceId
      in: path
      required: true
      description: "Resource unique identifier"
      schema:
        type: string
        format: uuid

    PageNumber:
      name: page
      in: query
      description: "Page number (1-indexed)"
      schema:
        type: integer
        minimum: 1
        default: 1

    PageSize:
      name: pageSize
      in: query
      description: "Number of items per page"
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20

    SortBy:
      name: sortBy
      in: query
      description: "Sort field and direction"
      schema:
        type: string
        pattern: "^[a-zA-Z]+:(asc|desc)$"
        example: "createdAt:desc"

    IfMatch:
      name: If-Match
      in: header
      description: "ETag for optimistic concurrency"
      schema:
        type: string

  responses:
    BadRequest:
      description: "Bad Request - Invalid input"
      content:
        application/problem+json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
          example:
            type: "https://api.example.com/problems/bad-request"
            title: "Bad Request"
            status: 400
            detail: "The request body is malformed"

    Unauthorized:
      description: "Unauthorized - Authentication required"
      content:
        application/problem+json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"

    Forbidden:
      description: "Forbidden - Insufficient permissions"
      content:
        application/problem+json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"

    NotFound:
      description: "Not Found - Resource does not exist"
      content:
        application/problem+json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"

    Conflict:
      description: "Conflict - Resource state conflict"
      content:
        application/problem+json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"

    UnprocessableEntity:
      description: "Unprocessable Entity - Validation failed"
      content:
        application/problem+json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
          example:
            type: "https://api.example.com/problems/validation-error"
            title: "Validation Error"
            status: 422
            detail: "One or more validation errors occurred"
            errors:
              - field: "name"
                message: "Name is required"
                code: "required"

    TooManyRequests:
      description: "Too Many Requests - Rate limit exceeded"
      headers:
        Retry-After:
          description: "Seconds until rate limit resets"
          schema:
            type: integer
        X-RateLimit-Limit:
          description: "Requests per window"
          schema:
            type: integer
        X-RateLimit-Remaining:
          description: "Requests remaining"
          schema:
            type: integer
      content:
        application/problem+json:
          schema:
            $ref: "#/components/schemas/ErrorResponse"
```

### Security Schemes

```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: "JWT Bearer token authentication"

    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
      description: "API key for service-to-service auth"

    oauth2:
      type: oauth2
      description: "OAuth 2.0 authentication"
      flows:
        authorizationCode:
          authorizationUrl: "https://auth.example.com/authorize"
          tokenUrl: "https://auth.example.com/token"
          refreshUrl: "https://auth.example.com/refresh"
          scopes:
            "read:resources": "Read access to resources"
            "write:resources": "Write access to resources"
            "admin:resources": "Administrative access"
```

## C# Models for OpenAPI

```csharp
using System.Text.Json.Serialization;

namespace SpecDrivenDevelopment.OpenApi;

/// <summary>
/// Represents an OpenAPI specification document
/// </summary>
public record OpenApiSpec
{
    public required string OpenApi { get; init; } = "3.1.0";
    public required OpenApiInfo Info { get; init; }
    public List<OpenApiServer> Servers { get; init; } = [];
    public Dictionary<string, OpenApiPathItem> Paths { get; init; } = [];
    public OpenApiComponents? Components { get; init; }
    public List<OpenApiSecurityRequirement> Security { get; init; } = [];
    public List<OpenApiTag> Tags { get; init; } = [];
}

public record OpenApiInfo
{
    public required string Title { get; init; }
    public required string Version { get; init; }
    public string? Description { get; init; }
    public OpenApiContact? Contact { get; init; }
    public OpenApiLicense? License { get; init; }
}

public record OpenApiContact
{
    public string? Name { get; init; }
    public string? Email { get; init; }
    public string? Url { get; init; }
}

public record OpenApiLicense
{
    public required string Name { get; init; }
    public string? Identifier { get; init; }
    public string? Url { get; init; }
}

public record OpenApiServer
{
    public required string Url { get; init; }
    public string? Description { get; init; }
    public Dictionary<string, OpenApiServerVariable>? Variables { get; init; }
}

public record OpenApiServerVariable
{
    public required string Default { get; init; }
    public List<string>? Enum { get; init; }
    public string? Description { get; init; }
}

public record OpenApiTag
{
    public required string Name { get; init; }
    public string? Description { get; init; }
}

public record OpenApiPathItem
{
    public string? Summary { get; init; }
    public string? Description { get; init; }
    public OpenApiOperation? Get { get; init; }
    public OpenApiOperation? Post { get; init; }
    public OpenApiOperation? Put { get; init; }
    public OpenApiOperation? Patch { get; init; }
    public OpenApiOperation? Delete { get; init; }
    public List<OpenApiParameter>? Parameters { get; init; }
}

public record OpenApiOperation
{
    public required string OperationId { get; init; }
    public string? Summary { get; init; }
    public string? Description { get; init; }
    public List<string>? Tags { get; init; }
    public List<OpenApiParameter>? Parameters { get; init; }
    public OpenApiRequestBody? RequestBody { get; init; }
    public required Dictionary<string, OpenApiResponse> Responses { get; init; }
    public List<OpenApiSecurityRequirement>? Security { get; init; }
    public bool Deprecated { get; init; }
}

public record OpenApiParameter
{
    public required string Name { get; init; }

    [JsonConverter(typeof(JsonStringEnumConverter))]
    public required ParameterLocation In { get; init; }

    public string? Description { get; init; }
    public bool Required { get; init; }
    public OpenApiSchema? Schema { get; init; }

    [JsonPropertyName("$ref")]
    public string? Ref { get; init; }
}

public enum ParameterLocation
{
    Query,
    Header,
    Path,
    Cookie
}

public record OpenApiRequestBody
{
    public string? Description { get; init; }
    public required Dictionary<string, OpenApiMediaType> Content { get; init; }
    public bool Required { get; init; }
}

public record OpenApiResponse
{
    public required string Description { get; init; }
    public Dictionary<string, OpenApiMediaType>? Content { get; init; }
    public Dictionary<string, OpenApiHeader>? Headers { get; init; }

    [JsonPropertyName("$ref")]
    public string? Ref { get; init; }
}

public record OpenApiMediaType
{
    public OpenApiSchema? Schema { get; init; }
    public object? Example { get; init; }
    public Dictionary<string, OpenApiExample>? Examples { get; init; }
}

public record OpenApiExample
{
    public string? Summary { get; init; }
    public string? Description { get; init; }
    public object? Value { get; init; }
}

public record OpenApiHeader
{
    public string? Description { get; init; }
    public OpenApiSchema? Schema { get; init; }
}

public record OpenApiSchema
{
    public string? Type { get; init; }
    public string? Format { get; init; }
    public string? Description { get; init; }
    public List<string>? Enum { get; init; }
    public object? Default { get; init; }
    public object? Example { get; init; }
    public List<string>? Required { get; init; }
    public Dictionary<string, OpenApiSchema>? Properties { get; init; }
    public OpenApiSchema? Items { get; init; }
    public bool? Nullable { get; init; }
    public int? MinLength { get; init; }
    public int? MaxLength { get; init; }
    public int? Minimum { get; init; }
    public int? Maximum { get; init; }
    public string? Pattern { get; init; }
    public List<OpenApiSchema>? AllOf { get; init; }
    public List<OpenApiSchema>? OneOf { get; init; }
    public List<OpenApiSchema>? AnyOf { get; init; }
    public bool? AdditionalProperties { get; init; }

    [JsonPropertyName("$ref")]
    public string? Ref { get; init; }
}

public record OpenApiComponents
{
    public Dictionary<string, OpenApiSchema>? Schemas { get; init; }
    public Dictionary<string, OpenApiParameter>? Parameters { get; init; }
    public Dictionary<string, OpenApiResponse>? Responses { get; init; }
    public Dictionary<string, OpenApiSecurityScheme>? SecuritySchemes { get; init; }
}

public record OpenApiSecurityScheme
{
    public required string Type { get; init; }
    public string? Scheme { get; init; }
    public string? BearerFormat { get; init; }
    public string? Description { get; init; }
    public string? Name { get; init; }
    public string? In { get; init; }
    public OpenApiOAuthFlows? Flows { get; init; }
}

public record OpenApiOAuthFlows
{
    public OpenApiOAuthFlow? AuthorizationCode { get; init; }
    public OpenApiOAuthFlow? ClientCredentials { get; init; }
}

public record OpenApiOAuthFlow
{
    public required string AuthorizationUrl { get; init; }
    public required string TokenUrl { get; init; }
    public string? RefreshUrl { get; init; }
    public required Dictionary<string, string> Scopes { get; init; }
}

public record OpenApiSecurityRequirement : Dictionary<string, List<string>>;
```

## OpenAPI Design Patterns

### Versioning Strategy

```yaml
versioning_strategies:
  url_path:
    description: "Version in URL path"
    example: "/v1/resources"
    pros:
      - "Explicit and visible"
      - "Easy to route"
      - "Cache-friendly"
    cons:
      - "URL changes on major version"

  header:
    description: "Version in custom header"
    example: "X-API-Version: 2023-01-15"
    pros:
      - "Clean URLs"
      - "Fine-grained control"
    cons:
      - "Less discoverable"
      - "Harder to test in browser"

  query_parameter:
    description: "Version as query parameter"
    example: "/resources?version=2"
    pros:
      - "Easy to specify"
      - "Fallback to default"
    cons:
      - "Cache complications"
      - "Less clean"

  recommended: "url_path"
  rationale: "Most explicit, widely adopted, cache-friendly"
```

### Pagination Patterns

```yaml
pagination_patterns:
  offset_based:
    description: "Traditional page/pageSize pagination"
    parameters:
      - "page (1-indexed)"
      - "pageSize (default 20, max 100)"
    response:
      pagination:
        page: 2
        pageSize: 20
        totalItems: 150
        totalPages: 8
    pros:
      - "Simple to implement"
      - "Random access to pages"
    cons:
      - "Inconsistent with concurrent writes"
      - "Performance degrades at high offsets"

  cursor_based:
    description: "Cursor/continuation token pagination"
    parameters:
      - "cursor (opaque token)"
      - "limit (default 20, max 100)"
    response:
      pagination:
        nextCursor: "eyJpZCI6MTIzfQ=="
        hasMore: true
    pros:
      - "Consistent with concurrent writes"
      - "Better performance at scale"
    cons:
      - "No random access"
      - "Harder to implement"

  recommended: "cursor_based for large datasets, offset_based for small"
```

### Error Handling (RFC 7807)

```yaml
error_handling:
  standard: "RFC 7807 Problem Details"
  content_type: "application/problem+json"

  structure:
    type: "URI reference identifying problem type"
    title: "Short human-readable summary"
    status: "HTTP status code"
    detail: "Human-readable explanation specific to this occurrence"
    instance: "URI reference to specific occurrence"

  extensions:
    errors: "Array of field-level validation errors"
    traceId: "Correlation ID for debugging"

  example:
    type: "https://api.example.com/problems/validation-error"
    title: "Validation Error"
    status: 422
    detail: "The request contains invalid data"
    instance: "/resources/123"
    traceId: "abc-123-xyz"
    errors:
      - field: "email"
        message: "Invalid email format"
        code: "invalid_format"
```

## Validation Checklist

```yaml
openapi_validation_checklist:
  structure:
    - "Valid OpenAPI 3.1.0 syntax"
    - "All required fields present (openapi, info, paths)"
    - "No undefined $ref references"
    - "Consistent naming conventions"

  operations:
    - "Every operation has unique operationId"
    - "All operations have summary and description"
    - "All operations tagged appropriately"
    - "All path parameters defined"
    - "Response codes cover success and error cases"

  schemas:
    - "All schemas have descriptions"
    - "Required fields explicitly listed"
    - "Examples provided for complex types"
    - "Enums documented with descriptions"
    - "String formats specified (uuid, date-time, email, uri)"

  security:
    - "Security schemes defined"
    - "Operations specify security requirements"
    - "OAuth scopes documented"

  documentation:
    - "API description explains purpose"
    - "Contact information provided"
    - "Server URLs for all environments"
    - "Tags organized logically"

  best_practices:
    - "Use RFC 7807 for errors"
    - "Consistent pagination approach"
    - "HATEOAS links where appropriate"
    - "Idempotency keys for POST operations"
    - "ETag/If-Match for optimistic concurrency"
```

## References

- `references/openapi-patterns.md` - Common OpenAPI design patterns
- `references/api-guidelines.md` - API design guidelines and standards

---

**Last Updated:** 2025-12-26
