---
name: aip-knowledge
description: Reference knowledge for Google API Improvement Proposals (AIP), adapted for REST/OpenAPI. Use when reviewing APIs, designing endpoints, or explaining AIP rules. Contains patterns for errors, pagination, filtering, LRO, field masks, and batch operations.
---

# AIP Knowledge

Quick reference for API Improvement Proposals adapted to REST/OpenAPI.

## When to Load References

Based on the task, load the relevant reference file:

| Topic                | Reference File    | When to Use                                      |
| -------------------- | ----------------- | ------------------------------------------------ |
| Error responses      | `errors.md`       | Designing error schema, reviewing error handling |
| Pagination           | `pagination.md`   | Adding pagination to list endpoints              |
| Filtering & sorting  | `filtering.md`    | Adding filter/order_by parameters                |
| Long-running ops     | `lro.md`          | Async operations, jobs, polling                  |
| Partial updates      | `field-masks.md`  | PATCH implementation, update semantics           |
| Batch operations     | `batch.md`        | Batch create/update/delete                       |
| Proto → REST mapping | `rest-mapping.md` | Translating AIP concepts to REST                 |

## Implemented Linter Rules

The AIP reviewer includes 17 automated rules across 6 categories:

### Naming (AIP-122)

| Rule ID                    | Severity   | What It Checks                                                  |
| -------------------------- | ---------- | --------------------------------------------------------------- |
| `aip122/plural-resources`  | warning    | Resource paths use plural nouns                                 |
| `aip122/no-verbs`          | error      | Paths contain nouns, not verbs                                  |
| `aip122/consistent-casing` | warning    | Path segments use consistent casing (kebab, snake, camel)       |
| `aip122/nested-ownership`  | suggestion | Nested resource params have descriptive names (not just `{id}`) |

### Standard Methods (AIP-131 to 135)

| Rule ID                    | Severity   | What It Checks                                     |
| -------------------------- | ---------- | -------------------------------------------------- |
| `aip131/get-no-body`       | error      | GET requests have no request body                  |
| `aip133/post-returns-201`  | suggestion | POST returns 201 Created or 202 Accepted           |
| `aip134/patch-over-put`    | suggestion | PATCH available for partial updates (not just PUT) |
| `aip135/delete-idempotent` | warning    | DELETE has no body and uses standard status codes  |

### Pagination (AIP-158)

| Rule ID                      | Severity   | What It Checks                                      |
| ---------------------------- | ---------- | --------------------------------------------------- |
| `aip158/list-paginated`      | warning    | List endpoints have page_size and page_token params |
| `aip158/max-page-size`       | suggestion | page_size param has maximum constraint              |
| `aip158/response-next-token` | warning    | Paginated responses include next_page_token field   |

### Filtering (AIP-132, 160)

| Rule ID                | Severity   | What It Checks                            |
| ---------------------- | ---------- | ----------------------------------------- |
| `aip132/has-filtering` | suggestion | List endpoints document filter parameters |
| `aip132/has-ordering`  | suggestion | List endpoints support order_by parameter |

### Errors (AIP-193)

| Rule ID                       | Severity   | What It Checks                                            |
| ----------------------------- | ---------- | --------------------------------------------------------- |
| `aip193/schema-defined`       | warning    | Error schema defined in components                        |
| `aip193/responses-documented` | suggestion | Operations document error responses                       |
| `aip193/standard-codes`       | suggestion | Standard HTTP error codes used (400, 401, 403, 404, etc.) |

### Idempotency (AIP-155)

| Rule ID                  | Severity   | What It Checks                               |
| ------------------------ | ---------- | -------------------------------------------- |
| `aip155/idempotency-key` | suggestion | POST endpoints accept Idempotency-Key header |

## Topics Without Automated Rules (Reference Only)

The following topics have detailed reference documentation but no automated linter rules yet:

- **Field Masks** (`field-masks.md`) - AIP-134 partial update patterns (only `aip134/patch-over-put` checks for PATCH availability)
- **Batch Operations** (`batch.md`) - AIP-231+ batch patterns
- **Long-Running Operations** (`lro.md`) - AIP-151, 155 async patterns
- **Proto → REST Mapping** (`rest-mapping.md`) - Translation guide

## Quick Reference

### Standard Methods → HTTP

| Method | HTTP   | Path              | Idempotent | Related Rules                                                          |
| ------ | ------ | ----------------- | ---------- | ---------------------------------------------------------------------- |
| Get    | GET    | `/resources/{id}` | Yes        | `aip131/get-no-body`                                                   |
| List   | GET    | `/resources`      | Yes        | `aip158/list-paginated`, `aip132/has-filtering`, `aip132/has-ordering` |
| Create | POST   | `/resources`      | No\*       | `aip133/post-returns-201`, `aip155/idempotency-key`                    |
| Update | PATCH  | `/resources/{id}` | Yes        | `aip134/patch-over-put`                                                |
| Delete | DELETE | `/resources/{id}` | Yes        | `aip135/delete-idempotent`                                             |

\*Use Idempotency-Key header for safe retries

### Naming Rules (AIP-122)

- `/users`, `/orders`, `/products` (plural nouns)
- `/user`, `/order` (singular - triggers `aip122/plural-resources`)
- `/getUsers`, `/createOrder` (verbs - triggers `aip122/no-verbs`)
- `/users/{id}/orders` (nested ownership)

### Pagination (AIP-158)

Request: `?page_size=20&page_token=xxx`

Response:

```json
{
  "data": [...],
  "next_page_token": "yyy"
}
```

### Error Response (AIP-193)

```json
{
  "error": {
    "code": "INVALID_ARGUMENT",
    "message": "Human-readable message",
    "details": [...],
    "request_id": "req_abc123"
  }
}
```

### Fetch AIPs On Demand

For detailed guidance, fetch from:

- `https://google.aip.dev/{number}` (e.g., `/158` for pagination)
- Only fetch when user needs deeper explanation
