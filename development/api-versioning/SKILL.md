---
name: api-versioning
description: Use when planning API versioning strategy, handling breaking changes, or managing API deprecation. Covers URL, header, and query parameter versioning approaches.
allowed-tools: Read, Glob, Grep
---

# API Versioning

Strategies for versioning APIs, managing breaking changes, and deprecating old versions gracefully.

## When to Use This Skill

- Choosing an API versioning strategy
- Planning for breaking changes
- Deprecating API versions
- Managing multiple API versions
- Designing for API evolution

## Why Version APIs?

```text
APIs are contracts with clients.
Breaking changes break clients.

Without versioning:
- Change field name → All clients break
- Remove endpoint → All clients break
- Change behavior → Unexpected client behavior

With versioning:
- Old clients use old version
- New clients use new version
- Gradual migration possible
```

## Versioning Strategies

### URL Path Versioning

```text
https://api.example.com/v1/users
https://api.example.com/v2/users

Pros:
- Clear and explicit
- Easy to understand
- Easy to route
- Easy to cache

Cons:
- Version embedded in client code
- Multiple URLs for same resource
- Not truly RESTful (URL should identify resource)
```

### Header Versioning

```text
GET /users
Accept: application/vnd.example.v1+json

or custom header:
GET /users
API-Version: 1

Pros:
- Clean URLs
- More RESTful
- Version separate from resource

Cons:
- Hidden from URL
- Harder to test in browser
- Requires header support
```

### Query Parameter Versioning

```text
GET /users?version=1
GET /users?api-version=2023-01-01

Pros:
- Easy to add
- Optional (can default)
- Easy to test

Cons:
- Can be forgotten
- Pollutes query string
- Caching complexity
```

### Content Negotiation

```text
Accept: application/vnd.example+json; version=1

Pros:
- Standard HTTP mechanism
- Flexible

Cons:
- Complex to implement
- Hard to discover
```

## Strategy Comparison

| Strategy | Visibility | Implementation | Caching | Recommendation |
| -------- | ---------- | -------------- | ------- | -------------- |
| URL Path | High | Easy | Easy | Best for public APIs |
| Header | Low | Medium | Medium | Good for internal APIs |
| Query Param | Medium | Easy | Complex | Good for simple cases |
| Content Neg | Low | Complex | Medium | Rarely used |

## Versioning Schemes

### Integer Versions

```text
v1, v2, v3

Pros: Simple, clear major changes
Cons: Coarse-grained

Best for: Public APIs with infrequent breaking changes
```

### Semantic Versioning

```text
v1.2.3 (major.minor.patch)

Major: Breaking changes
Minor: New features (backward compatible)
Patch: Bug fixes

Pros: Fine-grained, predictable
Cons: More complex

Best for: Libraries, SDKs
```

### Date-Based Versioning

```text
2023-01-15, 2023-06-01

Pros: Clear when version was current
Cons: Doesn't indicate change magnitude

Best for: Frequently changing APIs (Stripe, GitHub)

Example (Stripe):
Stripe-Version: 2023-10-16
```

## What Requires a New Version?

### Breaking Changes (New Major Version)

```text
Always breaking:
- Removing endpoint
- Removing field
- Changing field type
- Changing field meaning
- Renaming field
- Adding required field
- Changing authentication
- Changing error format
```

### Non-Breaking Changes (No Version Needed)

```text
Safe changes:
- Adding new endpoint
- Adding optional field
- Adding new enum value
- Adding optional parameter
- Relaxing validation
- Adding new error codes
```

## Version Management

### Running Multiple Versions

```text
Option 1: Separate codebases
/v1/* → v1 service
/v2/* → v2 service

Pros: Full isolation
Cons: Duplication, maintenance burden

Option 2: Shared codebase with branching
if (version == 1) {
  return formatV1(data);
} else {
  return formatV2(data);
}

Pros: Single codebase
Cons: Code complexity grows

Option 3: Transformation layer
Internal model → Version-specific transformer → Response

Pros: Clean separation
Cons: Requires transformation code
```

### Version Routing

```text
API Gateway pattern:

Client → Gateway → Route by version → Service

Gateway responsibilities:
- Parse version from URL/header
- Route to appropriate backend
- Transform if needed
- Handle defaults
```

## Deprecation Strategy

### Lifecycle Phases

```text
1. Current: Active development
2. Maintained: Bug fixes only
3. Deprecated: No changes, sunset announced
4. Sunset: Removed

Timeline example:
v1: Current (12 months)
v1: Maintained when v2 launches (6 months)
v1: Deprecated (6 months)
v1: Sunset
```

### Deprecation Communication

```text
Headers:
Deprecation: true
Sunset: Sat, 1 Jul 2024 00:00:00 GMT
Link: <https://api.example.com/v2/docs>; rel="successor-version"

Response body:
{
  "data": {...},
  "_deprecation": {
    "message": "This API version is deprecated",
    "sunset": "2024-07-01",
    "successor": "https://api.example.com/v2"
  }
}
```

### Migration Support

```text
Provide:
1. Migration guide documenting all changes
2. Mapping of old → new endpoints
3. Code examples for common operations
4. SDK updates with compatibility layer
5. Sandbox environment for testing
```

## Best Practices

### Default Version

```text
Options:
1. Require explicit version (recommended for public APIs)
2. Default to latest (dangerous for stability)
3. Default to oldest supported (conservative)

Recommendation: Require version, fail without it
```

### Version in Response

```text
Include version info in responses:

{
  "data": {...},
  "_meta": {
    "api_version": "v2",
    "deprecated": false
  }
}
```

### Graceful Degradation

```text
When version unknown:
1. Return error with supported versions
2. Redirect to documentation
3. Return latest version with warning

HTTP 400 Bad Request
{
  "error": "Unknown API version",
  "supported_versions": ["v1", "v2"],
  "documentation": "https://docs.example.com/api"
}
```

### Testing Multiple Versions

```text
Test matrix:
- All supported versions
- Breaking change boundaries
- Deprecation warnings
- Sunset behavior

Automated tests:
- Contract tests per version
- Backward compatibility tests
- Migration path tests
```

## Real-World Examples

### Stripe

```text
Date-based: 2023-10-16
Header: Stripe-Version
Default: Account's API version
Rollback: Can pin to older version
Upgrades: Preview in dashboard
```

### GitHub

```text
Date-based: 2022-11-28
Header: X-GitHub-Api-Version
Default: Latest
Preview features: Accept header
```

### Google

```text
URL path: /v1/, /v2/
Discovery document for each version
Long deprecation cycles (years)
```

### Twilio

```text
Date-based: 2010-04-01
URL path includes date
Very long support windows
```

## Anti-Patterns

```text
1. Too many versions
   → Consolidate, set deprecation schedule

2. Breaking changes in minor versions
   → Follow semantic versioning strictly

3. No deprecation warnings
   → Always communicate before breaking

4. Instant sunset
   → Give clients time to migrate (6-12 months minimum)

5. Version per endpoint
   → Keep all endpoints in sync per version
```

## Related Skills

- `api-design-fundamentals` - API design patterns
- `idempotency-patterns` - Safe API operations
- `quality-attributes-taxonomy` - Maintainability attributes
