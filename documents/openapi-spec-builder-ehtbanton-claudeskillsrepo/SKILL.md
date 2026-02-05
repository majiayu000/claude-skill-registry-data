---
name: openapi-spec-builder
description: Generate OpenAPI 3.x specification files (YAML) with endpoints, schemas, authentication, and examples for REST API documentation. Triggers on "create OpenAPI spec", "generate API documentation", "swagger spec for", "REST API schema".
---

# OpenAPI Spec Builder

Generate complete OpenAPI 3.x specification files for REST API documentation, SDK generation, and API testing.

## Output Requirements

**File Output:** `openapi.yaml` or `openapi.json`
**Format:** OpenAPI 3.0.x or 3.1.x specification
**Default:** YAML format (more readable)

## When Invoked

Immediately generate a complete, valid OpenAPI specification. Infer reasonable schemas, responses, and security from the API description.

## OpenAPI Structure

```yaml
openapi: 3.0.3
info:
  title: API Title
  version: 1.0.0
servers:
  - url: https://api.example.com/v1
paths:
  /resource:
    get: ...
components:
  schemas: ...
  securitySchemes: ...
```

## Complete Templates

### RESTful CRUD API
```yaml
openapi: 3.0.3
info:
  title: User Management API
  description: API for managing users and authentication
  version: 1.0.0
  contact:
    name: API Support
    email: api@example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server
  - url: http://localhost:3000/v1
    description: Development server

tags:
  - name: Users
    description: User management operations
  - name: Authentication
    description: Authentication and authorization

paths:
  /users:
    get:
      tags:
        - Users
      summary: List all users
      description: Retrieve a paginated list of users
      operationId: listUsers
      parameters:
        - $ref: '#/components/parameters/PageParam'
        - $ref: '#/components/parameters/LimitParam'
        - name: search
          in: query
          description: Search users by name or email
          schema:
            type: string
        - name: status
          in: query
          description: Filter by user status
          schema:
            type: string
            enum: [active, inactive, pending]
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserListResponse'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalError'
      security:
        - BearerAuth: []

    post:
      tags:
        - Users
      summary: Create a new user
      description: Create a new user account
      operationId: createUser
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
            example:
              email: john.doe@example.com
              firstName: John
              lastName: Doe
              password: SecurePass123!
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '400':
          $ref: '#/components/responses/BadRequest'
        '409':
          description: User already exists
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '500':
          $ref: '#/components/responses/InternalError'
      security:
        - BearerAuth: []

  /users/{userId}:
    parameters:
      - $ref: '#/components/parameters/UserIdParam'

    get:
      tags:
        - Users
      summary: Get user by ID
      description: Retrieve a single user by their ID
      operationId: getUserById
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'
        '500':
          $ref: '#/components/responses/InternalError'
      security:
        - BearerAuth: []

    put:
      tags:
        - Users
      summary: Update user
      description: Update an existing user's information
      operationId: updateUser
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateUserRequest'
      responses:
        '200':
          description: User updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'
        '500':
          $ref: '#/components/responses/InternalError'
      security:
        - BearerAuth: []

    delete:
      tags:
        - Users
      summary: Delete user
      description: Delete a user account
      operationId: deleteUser
      responses:
        '204':
          description: User deleted successfully
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'
        '500':
          $ref: '#/components/responses/InternalError'
      security:
        - BearerAuth: []

  /auth/login:
    post:
      tags:
        - Authentication
      summary: User login
      description: Authenticate user and receive access token
      operationId: login
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LoginRequest'
      responses:
        '200':
          description: Login successful
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuthResponse'
        '401':
          description: Invalid credentials
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /auth/refresh:
    post:
      tags:
        - Authentication
      summary: Refresh access token
      description: Get a new access token using refresh token
      operationId: refreshToken
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - refreshToken
              properties:
                refreshToken:
                  type: string
      responses:
        '200':
          description: Token refreshed successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuthResponse'
        '401':
          $ref: '#/components/responses/Unauthorized'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
          description: Unique user identifier
          example: 550e8400-e29b-41d4-a716-446655440000
        email:
          type: string
          format: email
          description: User's email address
          example: john.doe@example.com
        firstName:
          type: string
          description: User's first name
          example: John
        lastName:
          type: string
          description: User's last name
          example: Doe
        status:
          type: string
          enum: [active, inactive, pending]
          description: User account status
          example: active
        createdAt:
          type: string
          format: date-time
          description: Account creation timestamp
        updatedAt:
          type: string
          format: date-time
          description: Last update timestamp

    CreateUserRequest:
      type: object
      required:
        - email
        - firstName
        - lastName
        - password
      properties:
        email:
          type: string
          format: email
        firstName:
          type: string
          minLength: 1
          maxLength: 100
        lastName:
          type: string
          minLength: 1
          maxLength: 100
        password:
          type: string
          format: password
          minLength: 8

    UpdateUserRequest:
      type: object
      properties:
        firstName:
          type: string
          minLength: 1
          maxLength: 100
        lastName:
          type: string
          minLength: 1
          maxLength: 100
        status:
          type: string
          enum: [active, inactive]

    UserResponse:
      type: object
      properties:
        data:
          $ref: '#/components/schemas/User'

    UserListResponse:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        meta:
          $ref: '#/components/schemas/PaginationMeta'

    LoginRequest:
      type: object
      required:
        - email
        - password
      properties:
        email:
          type: string
          format: email
        password:
          type: string
          format: password

    AuthResponse:
      type: object
      properties:
        accessToken:
          type: string
          description: JWT access token
        refreshToken:
          type: string
          description: JWT refresh token
        expiresIn:
          type: integer
          description: Token expiration time in seconds
          example: 3600
        tokenType:
          type: string
          example: Bearer

    PaginationMeta:
      type: object
      properties:
        total:
          type: integer
          description: Total number of items
          example: 100
        page:
          type: integer
          description: Current page number
          example: 1
        limit:
          type: integer
          description: Items per page
          example: 20
        totalPages:
          type: integer
          description: Total number of pages
          example: 5

    Error:
      type: object
      properties:
        code:
          type: string
          description: Error code
          example: VALIDATION_ERROR
        message:
          type: string
          description: Human-readable error message
          example: Invalid request parameters
        details:
          type: array
          items:
            type: object
            properties:
              field:
                type: string
              message:
                type: string

  parameters:
    UserIdParam:
      name: userId
      in: path
      required: true
      description: User ID
      schema:
        type: string
        format: uuid

    PageParam:
      name: page
      in: query
      description: Page number
      schema:
        type: integer
        minimum: 1
        default: 1

    LimitParam:
      name: limit
      in: query
      description: Items per page
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: BAD_REQUEST
            message: Invalid request parameters

    Unauthorized:
      description: Unauthorized
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: UNAUTHORIZED
            message: Authentication required

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: NOT_FOUND
            message: Resource not found

    InternalError:
      description: Internal server error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: INTERNAL_ERROR
            message: An unexpected error occurred

  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT Bearer token authentication

    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
      description: API key authentication
```

## Common Patterns

### File Upload Endpoint
```yaml
/files/upload:
  post:
    summary: Upload a file
    requestBody:
      content:
        multipart/form-data:
          schema:
            type: object
            properties:
              file:
                type: string
                format: binary
              description:
                type: string
    responses:
      '201':
        description: File uploaded successfully
```

### Webhook Callback
```yaml
callbacks:
  onStatusChange:
    '{$request.body#/callbackUrl}':
      post:
        requestBody:
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WebhookPayload'
        responses:
          '200':
            description: Webhook received
```

## Validation Checklist

Before outputting, verify:
- [ ] Valid OpenAPI 3.x syntax
- [ ] All $ref references resolve
- [ ] Required fields marked in schemas
- [ ] Response codes follow HTTP standards
- [ ] Security schemes applied to protected endpoints
- [ ] Examples provided for complex schemas
- [ ] Tags organize endpoints logically
- [ ] operationId is unique for each operation

## Example Invocations

**Prompt:** "Create OpenAPI spec for a blog API with posts, comments, and users"
**Output:** Complete `openapi.yaml` with CRUD operations, relationships, authentication.

**Prompt:** "Generate swagger spec for e-commerce product catalog"
**Output:** Complete `openapi.yaml` with products, categories, search, filtering.

**Prompt:** "OpenAPI documentation for payment processing API"
**Output:** Complete `openapi.yaml` with transactions, webhooks, idempotency.
