---
name: test-endpoints
description: This skill automates API endpoint testing and documentation. It runs curl requests against specified endpoints, captures responses, validates against OpenAPI spec, and generates markdown documentation. Use after implementing new endpoints or when verifying API behavior.
---

<objective>
Test API endpoints with curl, validate responses, and generate comprehensive documentation of the results.
</objective>

<intake>
What would you like to test?

1. **Single endpoint** - Test one specific endpoint
2. **Multiple endpoints** - Test a list of endpoints
3. **All endpoints for a resource** - Test all endpoints under a path prefix
4. **Regression test** - Re-test previously documented endpoints

**Provide endpoint(s) or select an option.**
</intake>

<workflow>
## Step 1: Determine Test Target

Get from user:
- Base URL (default: `http://localhost:8080`)
- Endpoint path(s) to test
- HTTP method(s)
- Query parameters or request body
- Headers (e.g., `Accept-Language: id`)
- Authentication if needed

## Step 2: Execute Curl Requests

For each endpoint, execute curl with full options:

```bash
# GET with query params
curl -s -X GET "http://localhost:8080/api/v1/endpoint?param=value" \
  -H "Accept: application/json" \
  -H "Accept-Language: id" | jq '.'

# POST with JSON body
curl -s -X POST "http://localhost:8080/api/v1/endpoint" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"key": "value"}' | jq '.'

# GET with path parameter
curl -s -X GET "http://localhost:8080/api/v1/resource/01HGXK3V6P8QWNM0T1234ABCDE" \
  -H "Accept: application/json" | jq '.'
```

## Step 3: Capture and Format Response

For each response, capture:
- HTTP status code
- Response headers
- Response body (formatted with jq)
- Response time

```bash
# Capture with timing and status
curl -s -w "\n\nStatus: %{http_code}\nTime: %{time_total}s\n" \
  -X GET "http://localhost:8080/api/v1/endpoint" | jq '.'
```

## Step 4: Validate Response Structure

Compare response against OpenAPI spec:
- All required fields present
- Field types match spec
- Enum values are valid
- Nested objects have correct structure

## Step 5: Generate Documentation

Create markdown documentation in this format:

```markdown
# API Endpoint Test Results

**Test Date:** YYYY-MM-DD HH:MM:SS
**Base URL:** http://localhost:8080
**Environment:** local/staging/production

---

## Endpoint: GET /api/v1/resource

### Request

```bash
curl -X GET "http://localhost:8080/api/v1/resource?page=1&limit=10" \
  -H "Accept: application/json" \
  -H "Accept-Language: id"
```

### Response

**Status:** 200 OK
**Time:** 0.045s

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100
  }
}
```

### Validation

- [x] Status code matches expected (200)
- [x] Response structure matches OpenAPI spec
- [x] All required fields present
- [x] Field types correct

---
```
</workflow>

<test_scenarios>
## Common Test Scenarios

### Pagination Testing
```bash
# First page
curl -s "http://localhost:8080/api/v1/resource?page=1&limit=10" | jq '.pagination'

# Last page
curl -s "http://localhost:8080/api/v1/resource?page=999&limit=10" | jq '.pagination'

# Invalid page
curl -s "http://localhost:8080/api/v1/resource?page=-1&limit=10" | jq '.'
```

### Filter Testing
```bash
# Single filter
curl -s "http://localhost:8080/api/v1/search?subject_type=individual" | jq '.'

# Multiple filters
curl -s "http://localhost:8080/api/v1/search?subject_type=individual&nation=indonesia" | jq '.'

# Empty filter (should return all)
curl -s "http://localhost:8080/api/v1/search" | jq '.'
```

### Sort Testing
```bash
# Sort ascending
curl -s "http://localhost:8080/api/v1/search?sort=name_asc" | jq '.data[:3]'

# Sort descending
curl -s "http://localhost:8080/api/v1/search?sort=name_desc" | jq '.data[:3]'
```

### i18n Testing
```bash
# Indonesian
curl -s "http://localhost:8080/api/v1/resource" -H "Accept-Language: id" | jq '.data[0]'

# English
curl -s "http://localhost:8080/api/v1/resource" -H "Accept-Language: en" | jq '.data[0]'
```

### Error Response Testing
```bash
# Invalid ID format
curl -s "http://localhost:8080/api/v1/resource/invalid-id" | jq '.'

# Not found
curl -s "http://localhost:8080/api/v1/resource/01HGXK3V6P8QWNM0T1234XXXXX" | jq '.'

# Invalid parameters
curl -s "http://localhost:8080/api/v1/search?year_range=invalid" | jq '.'
```
</test_scenarios>

<output_formats>
## Output Format Options

### 1. Inline (default)
Show results directly in conversation.

### 2. Markdown File
Save to `docs/api-tests/YYYY-MM-DD-{endpoint}.md`

### 3. Summary Table
```markdown
| Endpoint | Method | Status | Time | Valid |
|----------|--------|--------|------|-------|
| /api/v1/search | GET | 200 | 0.05s | Yes |
| /api/v1/filters | GET | 200 | 0.02s | Yes |
```
</output_formats>

<quick_test_commands>
## Quick Test Commands

```bash
# Health check
curl -s http://localhost:8080/health | jq '.'

# Beneficial ownership search
curl -s "http://localhost:8080/api/v1/beneficial-ownership/search?keyword=test&page=1&limit=10" | jq '.'

# Filters endpoint
curl -s http://localhost:8080/api/v1/beneficial-ownership/filters | jq '.'

# Chart data
curl -s http://localhost:8080/api/v1/beneficial-ownership/chart/countries | jq '.'

# Procurement search
curl -s "http://localhost:8080/api/v1/procurement/search?page=1&limit=10" | jq '.'

# LLM chatbot
curl -s -X POST "http://localhost:8080/api/v1/chatbot/message" \
  -H "Content-Type: application/json" \
  -d '{"thread_id":"test","user_message":"hello"}' | jq '.'
```
</quick_test_commands>

<success_criteria>
Testing is complete when:
- [ ] All specified endpoints tested
- [ ] Response structure documented
- [ ] Status codes verified
- [ ] Edge cases tested (empty results, invalid params)
- [ ] i18n variations tested (if applicable)
- [ ] Documentation generated
</success_criteria>
