---
name: api-design
description: "Design REST/GraphQL/OpenAPI contracts before implementation — API-first approach. Use when: API, endpoint, REST, GraphQL, OpenAPI, API contract, API design, HTTP endpoint, grpc, soap."
license: CC-BY-SA-4.0
metadata:
  source: "agents/skills/architecture/api-design.skill.md"
  tags: "architecture"
  core: "true"
  context_cost: "medium"
---
# API Design Skill

## Goal
Design and document API contracts before writing implementation code. API-first development ensures consumers (frontend, mobile, third-party) have stable contracts and implementation details don't leak into the interface.

## Steps

1. **Clarify the API requirements**
   - Who are the consumers? (frontend SPA, mobile app, third-party, internal service)
   - Protocol? (REST, GraphQL, gRPC, AsyncAPI)
   - Auth? (JWT, API key, OAuth2, mTLS)
   - Rate limiting & Quotas?

2. **Design the resource model**
   ```yaml
   # Identify resources (nouns, not verbs)
   Resources:
     - /users            -> User resource
     - /orders           -> Order resource

   # Operations
   GET    /users          -> list users (pagination required)
   POST   /users          -> create user (idempotency key required)
   ```

3. **Define request/response schemas**
   - Use explicit schemas — no "any" types.
   - **Versioning**: URI Versioning (`/v1/...`) or Header Versioning (`Accept: application/vnd.app.v1+json`).
   - **Fields**: camelCase for JSON, snake_case for query params (standard choice).

4. **Define error responses (RFC 7807 Problem Details)**
   ```json
   {
     "type": "https://example.com/probs/out-of-credit",
     "title": "You do not have enough credit.",
     "status": 403,
     "detail": "Your current balance is 30, but that costs 50.",
     "instance": "/account/12345/msgs/abc"
   }
   ```

5. **Write the Spec**
   - **REST**: OpenAPI 3.1 (YAML preferred).
   - **GraphQL**: Schema Definition Language (SDL).
   - **gRPC**: Protocol Buffers (.proto).

6. **Security considerations**
   - All endpoints require authentication unless explicitly public.
   - **Scopes**: OAuth2 scopes (`read:users`, `write:orders`).
   - Sensitive fields (passwords, PII) never in responses.

7. **Pagination and filtering**
   - **Cursor-based**: `?cursor=xyz` (Preferred for infinite scroll/data export).
   - **Offset-based**: `?page=1` (OK for admin dashboards).

8. **Validate the design**
   - Can all use cases from the PRD be satisfied?
   - **N+1 Check**: Does the client need to make 100 calls to get a list? (If so, use `expand` or GraphQL).

9. **Store and share**
   - Save spec to: `docs/api/`.
   - Lint with Spectral.

## Constraints
- **Breaking Changes**: Strictly forbidden without version bump.
- **IDs**: Use UUIDv4 or nanoID (never auto-increment integers externally).
- **Dates**: ISO 8601 UTC always (`2024-01-01T12:00:00Z`).

## Output Format
API Spec file + summary of design decisions.

## Security & Guardrails

### 1. Skill Security (API Design)
- **Implicit "Any" Blocking**: The agent must strictly forbid the use of unstructured types (e.g., `any` in OpenAPI, or `JSON` scalar types in GraphQL) in the API contract. Every payload must be rigidly bounded and typed to allow code generators and WAFs to automatically reject malformed or exceptionally large payloads (JSON bombing).
- **Wildcard Scope Denial**: When defining OAuth2 or JWT scopes for the API, the agent is strictly prohibited from generating "admin" or wildcard (`*`) scopes. It must decompose authorization down to the resource and action level (e.g., `orders:read`, `orders:write`).

### 2. System Integration Security
- **BOLA/IDOR by Design Validation**: The agent must verify that every single endpoint targeting a specific resource ID (e.g., `GET /users/{id}/billing`) includes a documented authorization pre-condition stating that the authenticated caller has explicit ownership or admin rights to `{id}`. Lack of this documented constraint is an architectural flaw.
- **Rate Limit Blueprinting**: The API design cannot be finalized without explicit rate limiting headers and HTTP 429 schemas defined. The agent must attach quota assumptions to the OpenAPI spec, ensuring the infrastructure team knows the expected burst limits to mitigate L7 DDoS attacks.

### 3. LLM & Agent Guardrails
- **Security-by-Obscurity Hallucination**: The LLM might suggest hiding sensitive internal APIs by placing them on non-standard ports or giving them obfuscated URIs (e.g., `/api/v1/_hidden_debug_77`). The agent must reject this. All endpoints, regardless of intended audience, must enforce explicit Authentication and Authorization layers.
- **REST vs. GraphQL Exposure**: If the agent designs a GraphQL API, it must automatically append mandatory security constraints for depth limiting, complexity analysis, and pagination to prevent resource exhaustion attacks. It cannot output a "raw" GraphQL schema without these defensive properties.
