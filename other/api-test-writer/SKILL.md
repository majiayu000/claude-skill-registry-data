---
name: api-test-writer
description: Use when writing automated API tests or integration tests for REST or GraphQL endpoints, testing from an OpenAPI/Swagger spec or Postman collection, or checking status codes, response schemas, auth and error handling — Supertest, pytest + httpx, REST Assured, Postman/Newman and others.
---

# API Test Writer

## Overview

API tests check the contract clients depend on: status codes, response shape, validation, authorization and side effects. They are faster and more stable than UI tests, so most functional coverage belongs here.

## Method

1. **Inventory the endpoints** from routes, controllers or the OpenAPI spec: method, path, auth, request schema, responses.
2. **Match the project's tooling:** existing test framework and HTTP client (Supertest for Node, `httpx`/`requests` with pytest, REST Assured for Java, Newman for Postman collections). Follow existing test structure.
3. **Write cases per endpoint** using the matrix below.
4. **Control data:** create what each test needs through the API or factories, clean up afterwards, use unique values to allow parallel runs.
5. **Run** the suite and confirm each new test fails when the behavior is broken (change an expected value once to check).

## Case matrix per endpoint

| Category | Cases |
|---|---|
| Success | Valid request → correct status (200/201/204), body matches schema, headers (`Location`, `Content-Type`) |
| Validation | Missing required field, wrong type, out-of-range, too long, invalid format → 400/422 with field-level errors |
| Authentication | No token, expired token, malformed token → 401 |
| Authorization | Other user's resource (IDOR), insufficient role → 403 or 404 |
| Not found | Unknown ID → 404 with the standard error shape |
| Conflicts | Duplicate unique value, stale version → 409 |
| Side effects | Record created/updated in the database, event or email queued, idempotent retry does not duplicate |
| Lists | Pagination, filters, sorting, empty results, max page size |

## Example (Node, Supertest + Vitest)

```ts
import request from "supertest";
import { describe, it, expect } from "vitest";
import { app } from "../src/app";
import { createUser, tokenFor } from "./factories";

describe("POST /orders", () => {
  it("creates an order and returns 201 with a Location header", async () => {
    const user = await createUser();
    const res = await request(app)
      .post("/orders")
      .set("Authorization", `Bearer ${tokenFor(user)}`)
      .send({ items: [{ sku: "SKU-1", quantity: 2 }] });

    expect(res.status).toBe(201);
    expect(res.headers.location).toMatch(/^\/orders\/\w+$/);
    expect(res.body).toMatchObject({ status: "pending", items: [{ sku: "SKU-1", quantity: 2 }] });
  });

  it("rejects quantity 0 with a field error", async () => {
    const user = await createUser();
    const res = await request(app)
      .post("/orders")
      .set("Authorization", `Bearer ${tokenFor(user)}`)
      .send({ items: [{ sku: "SKU-1", quantity: 0 }] });

    expect(res.status).toBe(422);
    expect(res.body.errors).toContainEqual(expect.objectContaining({ field: "items[0].quantity" }));
  });
});
```

## Common mistakes

- Only testing the happy path.
- Asserting the whole response with a snapshot that includes IDs and timestamps.
- Tests that depend on data created by another test.
- Never testing authorization with a second user.
- Hitting production or shared environments with destructive tests.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
