---
name: webapp-api-bola
description: "Webapp Api Bola."
domain: cybersecurity
---

|
| **BOLA** | Broken Object Level Authorization (OWASP API1:2023) - the API does not verify that the authenticated user has permission to access the specific object referenced by the request |
| **IDOR** | Insecure Direct Object Reference - a closely related term where the application uses user-controllable input to directly access objects without authorization checks |
| **Horizontal Privilege Escalation** | Accessing resources belonging to another user at the same privilege level by manipulating object identifiers |
| **Vertical Privilege Escalation** | Accessing resources or functions restricted to a higher privilege level (e.g., regular user accessing admin endpoints) |
| **Object ID Enumeration** | Predicting valid object identifiers by analyzing their format (sequential integers, UUID patterns, encoded values) |
| **Autorize** | A Burp Suite extension that automates authorization testing by replaying requests with different user tokens |

## Tools & Systems

- **Burp Suite Professional**: Intercepting proxy for capturing and manipulating API requests with Autorize extension for automated BOLA testing
- **OWASP ZAP**: Open-source alternative with Access Control Testing add-on for authorization boundary testing
- **Autorize**: Burp extension that automatically detects authorization enforcement by replaying requests with different user contexts
- **Postman**: API testing platform for crafting and replaying requests with different authentication tokens across collections
- **ffuf**: Web fuzzer that can enumerate object IDs at scale: `ffuf -u https://api.example.com/orders/FUZZ -w ids.txt -H "Authorization: Bearer token"`

## Common Scenarios

### Scenario: E-Commerce API BOLA Assessment

**Context**: An e-commerce platform exposes a REST API for its mobile app. The API uses sequential integer IDs for orders, users, and addresses. Two test accounts are provided: a regular customer (User A, ID 1001) and another customer (User B, ID 1002).

**Approach**:
1. Map all endpoints from the Swagger spec at `/api/docs`: identify 47 endpoints, 23 of which take object IDs
2. Capture User A's requests for their own resources: profile, orders, addresses, payment methods, wishlist
3. Replace User A's object IDs with User B's IDs systematically across all 23 endpoints
4. Find that `GET /api/v1/orders/{id}` returns any order regardless of ownership (BOLA on read)
5. Find that `PATCH /api/v1/addresses/{id}` allows modifying any user's address (BOLA on write)
6. Find that `GET /api/v1/users/{id}/payment-methods` leaks payment card last-four digits for any user
7. Test batch endpoint `POST /api/v1/orders/export` - accepts array of order IDs and exports all without ownership check
8. Verify that `DELETE /api/v1/orders/{id}` correctly returns 403 for non-owned orders (authorization enforced)

**Pitfalls**:
- Only testing GET requests and missing BOLA in PUT/PATCH/DELETE methods that allow data modification or destruction
- Assuming UUIDs prevent BOLA - UUIDs are less predictable but can be leaked in API responses, logs, or URL parameters
- Not testing nested resource paths where authorization may be checked on the parent but not the child resource
- Missing BOLA in bulk/batch endpoints that accept arrays of object IDs
- Not considering that different API versions (v1 vs v2) may have different authorization implementations

## Output Format

```
## Finding: Broken Object Level Authorization in Order API

**ID**: API-BOLA-001
**Severity**: High (CVSS 7.5)
**OWASP API**: API1:2023 - Broken Object Level Authorization
**Affected Endpoints**:
  - GET /api/v1/orders/{id}
  - PATCH /api/v1/addresses/{id}
  - GET /api/v1/users/{id}/payment-methods
  - POST /api/v1/orders/export

**Description**:
The API does not enforce object-level authorization on order retrieval,
address modification, payment method viewing, or order export endpoints.
An authenticated user can access or modify any other user's resources by
substituting object IDs in the request. Sequential integer IDs make
enumeration trivial.

**Proof of Concept**:
1. Authenticate as User A (ID 1001): POST /api/v1/auth/login
2. Retrieve User A's order: GET /api/v1/orders/5001 -> 200 OK (legitimate)
3. Access User B's order: GET /api/v1/orders/5003 -> 200 OK (BOLA - returns full order details)
4. Modify User B's address: PATCH /api/v1/addresses/2002 -> 200 OK (BOLA - address changed)

**Impact**:
- Read access to all 850,000+ customer orders including shipping addresses and order contents
- Write access to any customer's delivery address, enabling package redirection
- Exposure of partial payment card data for all customers

**Remediation**:
1. Implement object-level authorization middleware that verifies the authenticated user owns the requested resource
2. Use authorization checks at the data access layer: `WHERE order.user_id = authenticated_user.id`
3. Replace sequential integer IDs with UUIDs to reduce predictability (defense in depth, not a fix alone)
4. Add authorization tests to the CI/CD pipeline for every endpoint that accepts object IDs
5. Implement rate limiting per user to slow enumeration attempts
```
