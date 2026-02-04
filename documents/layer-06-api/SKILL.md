---
name: LAYER_06_API
description: Expert knowledge for API Layer modeling in Documentation Robotics
triggers:
  [
    "OpenAPI",
    "REST API",
    "endpoint",
    "operation",
    "swagger",
    "API specification",
    "HTTP method",
    "request",
    "response",
  ]
version: 0.6.0
---

# API Layer Skill

**Layer Number:** 06
**Specification:** Metadata Model Spec v0.6.0
**Purpose:** Defines REST API contracts using OpenAPI 3.0, specifying endpoints, operations, request/response schemas, and security requirements.

---

## Layer Overview

The API Layer captures **API contracts**:

- **OPERATIONS** - HTTP methods on paths (GET, POST, PUT, DELETE, PATCH)
- **SCHEMAS** - Request/response data structures
- **SECURITY** - Authentication and authorization schemes
- **DOCUMENTATION** - API metadata, descriptions, examples
- **INTEGRATION** - Links to business services, application services, data models

This layer uses **OpenAPI 3.0.3** (de facto industry standard) with custom extensions for cross-layer traceability.

**Central Entity:** The **Operation** (HTTP method on a path) is the core modeling unit.

---

## Entity Types

### Core OpenAPI Entities (13 entities)

| Entity Type         | Description                                                                                 |
| ------------------- | ------------------------------------------------------------------------------------------- |
| **OpenAPIDocument** | Root of an OpenAPI specification file (version 3.0.3)                                       |
| **Info**            | Metadata about the API (title, description, version, contact, license)                      |
| **Server**          | Server where the API is available (with URL and variables)                                  |
| **Paths**           | Available API endpoints and operations                                                      |
| **PathItem**        | Operations available on a path                                                              |
| **Operation**       | Single API operation (HTTP method on a path) - **CENTRAL ENTITY**                           |
| **Parameter**       | Parameter for an operation (locations: query, header, path, cookie)                         |
| **RequestBody**     | Request payload for an operation                                                            |
| **Responses**       | Possible responses from an operation                                                        |
| **Response**        | Single response definition with status code                                                 |
| **MediaType**       | Media type and schema for request/response body                                             |
| **Components**      | Reusable component definitions (schemas, responses, parameters, examples, security schemes) |
| **Schema**          | Data type definition (JSON Schema subset)                                                   |

### Metadata Entities (11 entities)

| Entity Type               | Description                                                            |
| ------------------------- | ---------------------------------------------------------------------- |
| **Tag**                   | Metadata label for grouping operations                                 |
| **ExternalDocumentation** | Reference to external documentation                                    |
| **Contact**               | Contact information for API owner                                      |
| **License**               | Legal license for API                                                  |
| **ServerVariable**        | Variable placeholder in server URL templates                           |
| **Header**                | HTTP header parameters for requests/responses                          |
| **Link**                  | Relationship between API responses and subsequent operations (HATEOAS) |
| **Callback**              | Webhook or callback URL pattern                                        |
| **Example**               | Sample values for documentation and testing                            |
| **Encoding**              | Serialization details for multipart content                            |
| **SecurityScheme**        | Security mechanism (types: apiKey, http, oauth2, openIdConnect)        |

### Supporting Entities (3 entities)

| Entity Type         | Description                              |
| ------------------- | ---------------------------------------- |
| **OAuthFlows**      | Configuration for OAuth 2.0 flows        |
| **Condition**       | Logical expression for policy evaluation |
| **RetentionPolicy** | Data retention policies                  |
| **ValidationRule**  | Data validation constraints              |

---

## Intra-Layer Relationships

### Composition Relationships (Part cannot exist without whole)

| Source          | Predicate | Target         | Example                          |
| --------------- | --------- | -------------- | -------------------------------- |
| OpenAPIDocument | composes  | Info           | Document has metadata            |
| OpenAPIDocument | composes  | Paths          | Document defines endpoints       |
| OpenAPIDocument | composes  | Components     | Document has reusable components |
| Paths           | composes  | PathItem       | Paths contain path items         |
| PathItem        | composes  | Operation      | Path has HTTP methods            |
| PathItem        | composes  | Parameter      | Path-level parameters            |
| Operation       | composes  | Parameter      | Operation-specific parameters    |
| Operation       | composes  | RequestBody    | Request payload definition       |
| Operation       | composes  | Responses      | Response definitions             |
| Responses       | composes  | Response       | Individual status responses      |
| RequestBody     | composes  | MediaType      | Request content types            |
| Response        | composes  | MediaType      | Response content types           |
| Response        | composes  | Header         | Response headers                 |
| Response        | composes  | Link           | HATEOAS links                    |
| MediaType       | composes  | Schema         | Data structure                   |
| MediaType       | composes  | Example        | Sample data                      |
| MediaType       | composes  | Encoding       | Serialization details            |
| Components      | composes  | Schema         | Reusable schemas                 |
| Components      | composes  | Response       | Reusable responses               |
| Components      | composes  | Parameter      | Reusable parameters              |
| Components      | composes  | Example        | Reusable examples                |
| Components      | composes  | RequestBody    | Reusable request bodies          |
| Components      | composes  | Header         | Reusable headers                 |
| Components      | composes  | SecurityScheme | Security definitions             |
| Components      | composes  | Link           | Reusable links                   |
| Components      | composes  | Callback       | Reusable callbacks               |
| Info            | composes  | Contact        | API owner contact                |
| Info            | composes  | License        | API license                      |
| SecurityScheme  | composes  | OAuthFlows     | OAuth2 configuration             |

### Aggregation Relationships (Part can exist independently)

| Source          | Predicate  | Target              | Example                  |
| --------------- | ---------- | ------------------- | ------------------------ |
| OpenAPIDocument | aggregates | Server              | API deployment servers   |
| OpenAPIDocument | aggregates | Tag                 | Operation tags           |
| OpenAPIDocument | aggregates | SecurityRequirement | Global security          |
| Server          | aggregates | ServerVariable      | URL template variables   |
| PathItem        | aggregates | Parameter           | Shared parameters        |
| Operation       | aggregates | Callback            | Webhooks                 |
| Operation       | aggregates | SecurityRequirement | Operation-level security |

### Reference Relationships

| Source          | Predicate  | Target                | Example                                |
| --------------- | ---------- | --------------------- | -------------------------------------- |
| Schema          | references | Schema                | Schema $ref to another schema          |
| Parameter       | references | Schema                | Parameter uses schema                  |
| Header          | references | Schema                | Header uses schema                     |
| Link            | references | Operation             | Link points to operation (operationId) |
| Callback        | references | PathItem              | Callback references path definition    |
| Operation       | references | Tag                   | Operation tagged for grouping          |
| Tag             | references | ExternalDocumentation | Tag links to external docs             |
| OpenAPIDocument | references | ExternalDocumentation | Document links to external docs        |
| Encoding        | references | Header                | Encoding uses headers                  |

### Specialization Relationships

| Source | Predicate   | Target | Example                                  |
| ------ | ----------- | ------ | ---------------------------------------- |
| Schema | specializes | Schema | Schema inheritance (allOf, oneOf, anyOf) |

### Behavioral Relationships

| Source         | Predicate | Target    | Example                            |
| -------------- | --------- | --------- | ---------------------------------- |
| Operation      | triggers  | Callback  | Operation invokes webhook          |
| SecurityScheme | serves    | Operation | Security scheme protects operation |

### Association Relationships

| Source  | Predicate       | Target          | Example              |
| ------- | --------------- | --------------- | -------------------- |
| Contact | associated-with | OpenAPIDocument | Contact info for API |
| License | associated-with | OpenAPIDocument | Legal license        |

---

## Cross-Layer References

### Outgoing References (API → Other Layers)

OpenAPI specification includes **custom extensions** (x-\* properties) for cross-layer traceability:

| Target Layer              | Extension Property              | Example                                             |
| ------------------------- | ------------------------------- | --------------------------------------------------- |
| **Layer 1 (Motivation)**  | `x-supports-goals`              | Operation supports business goals                   |
| **Layer 1 (Motivation)**  | `x-fulfills-requirements`       | Operation fulfills functional requirements          |
| **Layer 1 (Motivation)**  | `x-governed-by-principles`      | Operation follows architectural principles          |
| **Layer 1 (Motivation)**  | `x-constrained-by`              | Operation subject to constraints (GDPR, HIPAA, SOX) |
| **Layer 2 (Business)**    | `x-business-service-ref`        | Operation realizes business service                 |
| **Layer 2 (Business)**    | `x-business-interface-ref`      | Operation exposed via business interface            |
| **Layer 4 (Application)** | `x-archimate-ref`               | OpenAPI document realizes ApplicationService        |
| **Layer 7 (Data Model)**  | `schema.$ref`                   | Schema references JSON Schema definition            |
| **Layer 3 (Security)**    | `x-security-resource`           | Operation protected by SecureResource               |
| **Layer 3 (Security)**    | `x-required-permissions`        | Operation requires specific permissions             |
| **Layer 3 (Security)**    | `x-rate-limit`                  | Rate limiting configuration                         |
| **Layer 11 (APM)**        | `x-apm-business-metrics`        | Operation tracked by business metrics               |
| **Layer 11 (APM)**        | `x-apm-sla-target-latency`      | Expected response time (e.g., "100ms")              |
| **Layer 11 (APM)**        | `x-apm-sla-target-availability` | Expected availability (e.g., "99.9%")               |
| **Layer 11 (APM)**        | `x-apm-trace`                   | Distributed tracing enabled                         |
| **Layer 11 (APM)**        | `x-apm-criticality`             | Business criticality (critical, high, medium, low)  |

### Incoming References (Lower Layers → API)

Lower layers reference API layer to show implementation and data structure.

---

## Codebase Detection Patterns

### Pattern 1: FastAPI Python

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="User Management API",  # OpenAPIDocument: Info.title
    description="API for managing user accounts",  # Info.description
    version="1.0.0"  # Info.version
)

class UserCreateRequest(BaseModel):  # Schema (RequestBody)
    username: str
    email: str
    full_name: str

class UserResponse(BaseModel):  # Schema (Response)
    user_id: str
    username: str
    email: str
    created_at: datetime

@app.post(
    "/api/users",  # PathItem + Operation (POST)
    response_model=UserResponse,  # Response schema
    status_code=201,  # Response status
    tags=["Users"],  # Tag
    summary="Create a new user",  # Operation.summary
    description="Creates a new user account with the provided details"  # Operation.description
)
async def create_user(user: UserCreateRequest) -> UserResponse:  # RequestBody + Response
    """
    x-business-service-ref: business/service/user-management
    x-apm-sla-target-latency: 200ms
    x-required-permissions: users.write
    """
    pass
```

**Maps to:**

- OpenAPIDocument: "User Management API"
- PathItem: "/api/users"
- Operation: "POST /api/users"
- RequestBody: MediaType (application/json) with Schema (UserCreateRequest)
- Response: 201 with Schema (UserResponse)
- Tag: "Users"

### Pattern 2: Express.js TypeScript

```typescript
import express from "express";
import { body, param, query, validationResult } from "express-validator";

const router = express.Router();

/**
 * @openapi
 * /api/orders/{orderId}:
 *   get:
 *     summary: Get order by ID
 *     description: Retrieves a single order by its unique identifier
 *     tags:
 *       - Orders
 *     parameters:
 *       - name: orderId
 *         in: path
 *         required: true
 *         schema:
 *           type: string
 *           format: uuid
 *     responses:
 *       200:
 *         description: Order found
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Order'
 *       404:
 *         description: Order not found
 *     x-business-service-ref: business/service/order-management
 *     x-apm-sla-target-latency: 100ms
 *     x-apm-criticality: high
 */
router.get("/api/orders/:orderId", param("orderId").isUUID(), async (req, res) => {
  // Implementation
});
```

**Maps to:**

- PathItem: "/api/orders/{orderId}"
- Operation: "GET /api/orders/{orderId}"
- Parameter: "orderId" (in: path, type: string, format: uuid)
- Response: 200 with schema reference
- Response: 404 error response
- Custom extensions: x-business-service-ref, x-apm-sla-target-latency, x-apm-criticality

### Pattern 3: Spring Boot Java

```java
@RestController
@RequestMapping("/api/products")
@Tag(name = "Products", description = "Product management operations")
public class ProductController {

    @Operation(
        summary = "List products",
        description = "Returns a paginated list of products",
        extensions = {
            @Extension(name = "x-apm-sla-target-latency", properties = @ExtensionProperty(name = "latency", value = "150ms")),
            @Extension(name = "x-required-permissions", properties = @ExtensionProperty(name = "permissions", value = "products.read"))
        }
    )
    @ApiResponses({
        @ApiResponse(
            responseCode = "200",
            description = "Products retrieved successfully",
            content = @Content(
                mediaType = "application/json",
                schema = @Schema(implementation = ProductListResponse.class)
            )
        )
    })
    @GetMapping
    public ResponseEntity<ProductListResponse> listProducts(
        @Parameter(description = "Page number", example = "1") @RequestParam(defaultValue = "1") int page,
        @Parameter(description = "Page size", example = "20") @RequestParam(defaultValue = "20") int size
    ) {
        // Implementation
    }
}
```

**Maps to:**

- PathItem: "/api/products"
- Operation: "GET /api/products"
- Parameters: "page" (query), "size" (query)
- Response: 200 with ProductListResponse schema
- Tag: "Products"
- Custom extensions

### Pattern 4: OpenAPI YAML Definition

```yaml
openapi: 3.0.3
info:
  title: Payment Processing API
  description: API for processing customer payments
  version: 2.1.0
  contact:
    name: API Support
    email: api-support@example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT
  x-governed-by-principles:
    - motivation/principle/api-first-design
    - motivation/principle/security-by-design

servers:
  - url: https://api.example.com/v2
    description: Production server
  - url: https://staging-api.example.com/v2
    description: Staging server

paths:
  /payments:
    post:
      summary: Process payment
      description: Processes a payment transaction
      operationId: processPayment
      tags:
        - Payments
      security:
        - oauth2: [payments.write]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/PaymentRequest"
            examples:
              credit-card:
                $ref: "#/components/examples/CreditCardPayment"
      responses:
        "201":
          description: Payment processed successfully
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/PaymentResponse"
        "400":
          $ref: "#/components/responses/BadRequest"
        "401":
          $ref: "#/components/responses/Unauthorized"
      x-business-service-ref: business/service/payment-processing
      x-apm-sla-target-latency: 500ms
      x-apm-sla-target-availability: 99.99%
      x-apm-criticality: critical
      x-required-permissions:
        - payments.write
      x-rate-limit:
        requests: 100
        window: 60s

components:
  schemas:
    PaymentRequest:
      type: object
      required:
        - amount
        - currency
        - payment_method
      properties:
        amount:
          type: number
          format: double
          minimum: 0.01
          example: 99.99
        currency:
          type: string
          enum: [USD, EUR, GBP]
          example: USD
        payment_method:
          $ref: "#/components/schemas/PaymentMethod"

    PaymentResponse:
      type: object
      properties:
        transaction_id:
          type: string
          format: uuid
        status:
          type: string
          enum: [pending, completed, failed]
        timestamp:
          type: string
          format: date-time

  securitySchemes:
    oauth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.example.com/oauth/authorize
          tokenUrl: https://auth.example.com/oauth/token
          scopes:
            payments.read: Read payment information
            payments.write: Process payments

  responses:
    BadRequest:
      description: Invalid request
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"

  examples:
    CreditCardPayment:
      value:
        amount: 99.99
        currency: USD
        payment_method:
          type: credit_card
          card_number: "4111111111111111"
```

---

## Modeling Workflow

### Step 1: Create OpenAPI Document

```bash
# Create the API specification document
dr add api document "payment-api" \
  --properties version=3.0.3,title="Payment Processing API",api-version=2.1.0 \
  --description "API for processing customer payments"

# Add API metadata
dr add api info "payment-api-info" \
  --properties title="Payment Processing API",version=2.1.0,contact-email=api@example.com \
  --description "API metadata and contact information"

# Link to motivation layer
dr relationship add "api/document/payment-api" \
  governed-by "motivation/principle/api-first-design"
```

### Step 2: Define Servers

```bash
# Production server
dr add api server "production-server" \
  --properties url=https://api.example.com/v2,description="Production server" \
  --description "Production API server"

# Staging server
dr add api server "staging-server" \
  --properties url=https://staging-api.example.com/v2,description="Staging server" \
  --description "Staging API server"
```

### Step 3: Define Security Schemes

```bash
# OAuth2 security
dr add api security-scheme "oauth2-auth" \
  --properties type=oauth2,flow=authorizationCode,authorization-url=https://auth.example.com/oauth/authorize,token-url=https://auth.example.com/oauth/token \
  --description "OAuth2 authorization code flow"

# API Key security
dr add api security-scheme "api-key-auth" \
  --properties type=apiKey,in=header,name=X-API-Key \
  --description "API key authentication"
```

### Step 4: Define Schemas (Data Models)

```bash
# Request schema
dr add api schema "payment-request" \
  --properties type=object,required=amount:currency:payment_method \
  --description "Payment request payload"

# Response schema
dr add api schema "payment-response" \
  --properties type=object \
  --description "Payment processing response"

# Link to data model layer
dr relationship add "api/schema/payment-request" \
  references "data-model/schema/payment-request"
```

### Step 5: Define Operations (Core Entities)

```bash
# POST operation
dr add api operation "process-payment" \
  --properties path=/payments,method=POST,operation-id=processPayment \
  --description "Processes a payment transaction"

# Add custom extensions for cross-layer traceability
dr add api operation "process-payment" \
  --properties x-business-service-ref=business/service/payment-processing,x-apm-sla-target-latency=500ms,x-apm-sla-target-availability=99.99%,x-apm-criticality=critical,x-required-permissions=payments.write

# GET operation
dr add api operation "get-payment" \
  --properties path=/payments/{paymentId},method=GET,operation-id=getPayment \
  --description "Retrieves payment details by ID"
```

### Step 6: Define Parameters

```bash
# Path parameter
dr add api parameter "payment-id-param" \
  --properties name=paymentId,in=path,required=true,type=string,format=uuid \
  --description "Payment transaction ID"

# Query parameter
dr add api parameter "status-filter" \
  --properties name=status,in=query,required=false,type=string,enum=pending:completed:failed \
  --description "Filter payments by status"

# Link parameter to operation
dr relationship add "api/operation/get-payment" \
  has-parameter "api/parameter/payment-id-param"
```

### Step 7: Define Request/Response Bodies

```bash
# Request body
dr add api request-body "payment-request-body" \
  --properties required=true,content-type=application/json \
  --description "Payment request payload"

# Link request body to schema
dr relationship add "api/request-body/payment-request-body" \
  uses-schema "api/schema/payment-request"

# Response
dr add api response "payment-success-response" \
  --properties status-code=201,description="Payment processed successfully" \
  --description "Successful payment response"

# Link response to schema
dr relationship add "api/response/payment-success-response" \
  uses-schema "api/schema/payment-response"
```

### Step 8: Define Tags for Organization

```bash
# Add tags
dr add api tag "payments" \
  --properties name=Payments \
  --description "Payment processing operations"

dr add api tag "refunds" \
  --properties name=Refunds \
  --description "Refund operations"

# Tag operations
dr relationship add "api/operation/process-payment" \
  tagged-with "api/tag/payments"
```

### Step 9: Cross-Layer Integration

```bash
# Link to business layer
dr relationship add "api/operation/process-payment" \
  realizes "business/service/payment-processing"

# Link to application layer
dr relationship add "api/document/payment-api" \
  realizes "application/service/payment-api"

# Link to security layer
dr relationship add "api/operation/process-payment" \
  protected-by "security/secure-resource/payment-api"

# Link to motivation layer
dr relationship add "api/operation/process-payment" \
  supports "motivation/goal/reduce-checkout-time"

# Link to APM layer
dr relationship add "api/operation/process-payment" \
  tracked-by "apm/metric/payment-processing-latency"
```

### Step 10: Validate and Export

```bash
# Validate API layer
dr validate --layer api

# Export to OpenAPI YAML
dr export openapi --output payment-api.yaml

# Validate exported OpenAPI with external tools
spectral lint payment-api.yaml
```

---

## Operation-Level SLA Patterns

Different operations have different SLA targets:

```yaml
# Search operation: fast response
x-apm-sla-target-latency: "50ms"
x-apm-sla-target-availability: "99.9%"
x-apm-criticality: "high"

# Write operation: moderate latency
x-apm-sla-target-latency: "200ms"
x-apm-sla-target-availability: "99.95%"
x-apm-criticality: "critical"

# Batch operation: longer latency acceptable
x-apm-sla-target-latency: "10s"
x-apm-sla-target-availability: "99.5%"
x-apm-criticality: "medium"

# Reporting: can be slower
x-apm-sla-target-latency: "5s"
x-apm-sla-target-availability: "99%"
x-apm-criticality: "low"
```

---

## Best Practices

1. **Operation is the Central Entity** - Model operations, not just paths
2. **Use OpenAPI 3.0.3** - Latest stable version with broad tooling support
3. **Tag Operations** - Organize operations by domain or resource
4. **Define Reusable Components** - Schemas, responses, parameters in Components section
5. **Document Examples** - Include request/response examples for testing and documentation
6. **Security at Operation Level** - Different operations can have different security requirements
7. **Link to Business Services** - Use x-business-service-ref for traceability
8. **Define SLA Targets** - Use x-apm-sla-target-\* for monitoring
9. **Version APIs Properly** - Use semantic versioning (major.minor.patch)
10. **Generate from Code** - Use FastAPI, NestJS decorators, or Springdoc to auto-generate OpenAPI specs

---

## OpenAPI Tooling Ecosystem

### Generation Tools

- **FastAPI** (Python) - Auto-generates OpenAPI from Python decorators
- **NestJS** (TypeScript) - Swagger module for OpenAPI generation
- **Springdoc** (Java) - OpenAPI 3 for Spring Boot applications
- **Express + swagger-jsdoc** (Node.js) - Generate from JSDoc comments

### Validation Tools

- **Spectral** - OpenAPI linter and validator
- **openapi-validator** - IBM's OpenAPI validator
- **swagger-cli** - Validate and bundle OpenAPI specs

### Documentation Tools

- **Swagger UI** - Interactive API documentation
- **Redoc** - Clean, customizable API documentation
- **Postman** - Import OpenAPI for API testing

### Code Generation Tools

- **OpenAPI Generator** - Generate client SDKs and server stubs
- **swagger-codegen** - Legacy code generation tool
- **oapi-codegen** (Go) - Generate Go server/client from OpenAPI

---

## Validation Tips

| Issue                | Cause                                  | Fix                                            |
| -------------------- | -------------------------------------- | ---------------------------------------------- |
| Missing Operations   | Paths defined but no operations        | Add HTTP methods (GET, POST, etc.)             |
| Unlinked Schemas     | Schemas not referenced by operations   | Link schemas to request/response bodies        |
| Missing Security     | Operations lack security requirements  | Add securitySchemes and apply to operations    |
| No Cross-Layer Links | API not linked to business/application | Add x-business-service-ref and x-archimate-ref |
| Missing SLA Targets  | Operations lack performance targets    | Add x-apm-sla-target-\* extensions             |
| Untagged Operations  | Operations not organized by tags       | Add tags for grouping                          |
| No Examples          | Schemas lack examples                  | Add example values for documentation           |
| Invalid OpenAPI      | Spec doesn't validate                  | Use Spectral or openapi-validator              |

---

## Quick Reference

**Add Commands:**

```bash
dr add api document <name> --properties version=3.0.3,title=<title>
dr add api operation <name> --properties path=<path>,method=<method>
dr add api schema <name> --properties type=<type>
dr add api parameter <name> --properties name=<name>,in=<location>
dr add api security-scheme <name> --properties type=<type>
dr add api tag <name> --properties name=<display-name>
```

**Relationship Commands:**

```bash
dr relationship add <operation> uses-schema <schema>
dr relationship add <operation> has-parameter <parameter>
dr relationship add <operation> tagged-with <tag>
dr relationship add <schema> references <schema>
```

**Cross-Layer Commands:**

```bash
dr relationship add api/<operation> realizes business/<service>
dr relationship add api/<document> realizes application/<service>
dr relationship add api/<schema> references data-model/<schema>
dr relationship add api/<operation> protected-by security/<resource>
dr relationship add api/<operation> supports motivation/<goal>
```

**Export Commands:**

```bash
dr export openapi --output api-spec.yaml
dr export openapi --layer api --format json --output api-spec.json
```

**Validation Commands:**

```bash
dr validate --layer api
spectral lint api-spec.yaml
swagger-cli validate api-spec.yaml
```

---

## Custom Extension Reference

Documentation Robotics defines custom OpenAPI extensions for cross-layer traceability:

```yaml
# Motivation Layer Links
x-supports-goals: [motivation/goal/id1, motivation/goal/id2]
x-fulfills-requirements: [motivation/requirement/id1]
x-governed-by-principles: [motivation/principle/id1]
x-constrained-by: [motivation/constraint/id1]

# Business Layer Links
x-business-service-ref: business/service/id
x-business-interface-ref: business/interface/id

# Application Layer Links
x-archimate-ref: application/service/id

# Security Layer Links
x-security-resource: security/secure-resource/id
x-required-permissions: [users.read, users.write]
x-rate-limit:
  requests: 100
  window: 60s

# APM Layer Links
x-apm-business-metrics: [apm/metric/id1]
x-apm-sla-target-latency: "100ms"
x-apm-sla-target-availability: "99.9%"
x-apm-trace: true
x-apm-criticality: "high" # critical, high, medium, low
```

These extensions enable full traceability from API operations to business goals, requirements, security controls, and monitoring metrics.

---

## Summary

The API Layer is the **contract layer** - it defines HOW external consumers interact with your system. Every operation should:

1. Be linked to a business service (traceability)
2. Have clear request/response schemas
3. Define security requirements
4. Specify SLA targets for monitoring
5. Include examples for documentation and testing

Use OpenAPI 3.0.3 as the foundation, leverage auto-generation tools from your framework, and extend with custom properties for full cross-layer integration.
