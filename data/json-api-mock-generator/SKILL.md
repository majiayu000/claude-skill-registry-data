---
name: json-api-mock-generator
description: Generate realistic JSON API mock response files with proper data types, nested structures, and configurable record counts. Triggers on "create mock API response", "generate JSON mock data", "fake API data for", "mock endpoint response".
---

# JSON API Mock Generator

Generate production-realistic JSON API mock response files for development, testing, and prototyping.

## Output Requirements

**File Output:** `.json` files with valid JSON structure
**Naming Convention:** `mock-{resource}-{endpoint}.json` (e.g., `mock-users-list.json`)

## When Invoked

Immediately generate a complete, valid JSON file. Ask no clarifying questions unless the domain is completely ambiguous.

## Default Behavior

If minimal context provided, generate:
- 10 records for list endpoints
- Realistic fake data (names, emails, dates, IDs)
- Proper data types (strings, numbers, booleans, arrays, nested objects)
- RESTful response wrapper structure

## JSON Structure Patterns

### List Endpoint Response
```json
{
  "data": [...],
  "meta": {
    "total": 100,
    "page": 1,
    "per_page": 10,
    "total_pages": 10
  },
  "links": {
    "self": "/api/v1/resource?page=1",
    "next": "/api/v1/resource?page=2",
    "last": "/api/v1/resource?page=10"
  }
}
```

### Single Resource Response
```json
{
  "data": {
    "id": "uuid-here",
    "type": "resource_name",
    "attributes": {...},
    "relationships": {...}
  }
}
```

### Error Response
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": [...],
    "timestamp": "ISO-8601"
  }
}
```

## Data Generation Rules

### IDs
- Use UUIDs for primary keys: `"id": "550e8400-e29b-41d4-a716-446655440000"`
- Use sequential integers only if specified: `"id": 1`

### Timestamps
- ISO 8601 format: `"2024-01-15T09:30:00Z"`
- Include `created_at`, `updated_at` for resources

### Names and Text
- Use realistic but clearly fake names: "Jane Smith", "Acme Corp"
- Vary lengths appropriately
- No lorem ipsum unless specifically for content fields

### Numbers
- Currency: integers in cents `"amount": 9999` (represents $99.99)
- Percentages: decimals `"rate": 0.15`
- Counts: integers `"quantity": 5`

### Relationships
- Use consistent IDs across related resources
- Include both ID references and nested objects where appropriate

## Domain-Specific Patterns

### E-commerce
```json
{
  "id": "prod_abc123",
  "name": "Wireless Bluetooth Headphones",
  "sku": "WBH-001-BLK",
  "price": 7999,
  "currency": "USD",
  "inventory": {
    "quantity": 150,
    "warehouse": "US-WEST-01"
  },
  "images": [
    {"url": "https://cdn.example.com/products/wbh-001-1.jpg", "alt": "Front view"}
  ]
}
```

### User/Auth
```json
{
  "id": "usr_123abc",
  "email": "jane.smith@example.com",
  "username": "janesmith",
  "profile": {
    "first_name": "Jane",
    "last_name": "Smith",
    "avatar_url": "https://cdn.example.com/avatars/123.jpg"
  },
  "roles": ["user", "admin"],
  "verified": true,
  "created_at": "2024-01-15T09:30:00Z"
}
```

### SaaS/Subscription
```json
{
  "id": "sub_xyz789",
  "customer_id": "cus_abc123",
  "plan": {
    "id": "plan_pro",
    "name": "Professional",
    "amount": 4999,
    "interval": "month"
  },
  "status": "active",
  "current_period_start": "2024-01-01T00:00:00Z",
  "current_period_end": "2024-02-01T00:00:00Z"
}
```

## Validation Checklist

Before outputting, verify:
- [ ] Valid JSON (parseable)
- [ ] Consistent data types throughout
- [ ] IDs are unique within the file
- [ ] Timestamps are valid ISO 8601
- [ ] No trailing commas
- [ ] Proper null handling (not "null" strings)
- [ ] Arrays are properly bracketed
- [ ] Nested objects are complete

## Example Invocations

**Prompt:** "Create mock API response for a blog posts endpoint"
**Output:** Complete `mock-posts-list.json` with 10 realistic blog posts including title, content, author, tags, dates, view counts.

**Prompt:** "Generate fake user data JSON for 25 users with addresses"
**Output:** Complete `mock-users-list.json` with 25 users including nested address objects.

**Prompt:** "Mock API error response for 404 not found"
**Output:** Complete `mock-error-404.json` with proper error structure.
