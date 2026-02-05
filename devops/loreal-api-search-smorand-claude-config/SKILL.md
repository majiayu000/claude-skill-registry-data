---
name: loreal-api-search
description: Expert in searching and retrieving API information from L'Oréal's API Portal. **Use this skill whenever the user mentions 'API search', 'find API', 'API information', 'API spec', 'API schema', 'Swagger', 'OpenAPI', or asks about available APIs in the API portal.** Handles searching APIs by pattern, retrieving API metadata, and fetching OpenAPI specifications using Azure OAuth authentication.
---

# API Search

**Trigger**: Use this skill whenever the user mentions "API search", "find API", "API portal", "API information", "API spec", "API schema", "Swagger", "OpenAPI", or asks about available APIs.

## Scope

Search and retrieve API information from L'Oréal's API Portal. Use it for:
- Searching for APIs by name pattern
- Retrieving detailed API information and metadata
- Fetching Swagger/OpenAPI specifications and schemas
- Discovering available APIs in the portal
- Getting complete API endpoint definitions and request/response formats

## Authentication

**IMPORTANT**: API Portal access requires Azure OAuth authentication.

### Option 1: Using Python Scripts (Recommended)

Generate and save the token once:

```bash
~/.claude/skills/btdp-api-search/scripts/run.sh get_token --save
```

This saves the token to `~/.claude/credentials/api_portal_token` for reuse by other scripts.

### Option 2: Manual curl Commands

For direct curl usage, generate the token inline:

```bash
# Get token and use directly
ACCESS_TOKEN=$(~/.claude/skills/btdp-api-search/scripts/run.sh get_token)

# Or read from saved file
ACCESS_TOKEN=$(cat ~/.claude/credentials/api_portal_token)
```

**Configuration**:
- Token is retrieved from Google Secret Manager (`itg-btdpsecurity-gbl-ww-pd/btdp-srt-azure_app-pd`)
- OAuth URL: `https://api.loreal.net/v1/oauth20/token`
- Scope: `api://32a1cb44-61cd-4c6b-bd8e-1ecff52de813/.default`

## Service URL

```bash
API_BASE_URL="https://api.loreal.net/global/it4it/coe/v1/apiinfos/api"
```

## Workflow Guide

### Decision Tree

1. **User wants to search for APIs by name/pattern**
   → Use `search_api` script or curl command
   → Save results to file for large result sets

2. **User wants detailed info about a specific API**
   → Use `get_api_info` script or curl command
   → Returns metadata: title, description, version, category, etc.

3. **User wants OpenAPI/Swagger specification or API schema**
   → Use `get_api_spec` script or curl command
   → Save to file (specs can be large)
   → Contains complete endpoint definitions, request/response schemas, parameters

4. **User wants to browse all APIs**
   → Use `search_api` with pattern `.*` to match all
   → MUST save to file (9000+ APIs)

## Operations

### 1. Search for APIs by Pattern

**Using Python Script** (Recommended):

```bash
# Search for APIs containing "semantic" in the name
~/.claude/skills/btdp-api-search/scripts/run.sh search_api "semantic"

# Search with case-insensitive pattern
~/.claude/skills/btdp-api-search/scripts/run.sh search_api "btdp.*service"

# Save results to file
~/.claude/skills/btdp-api-search/scripts/run.sh search_api "semantic" --output /tmp/apis.json
```

**Using curl**:

```bash
ACCESS_TOKEN=$(cat ~/.claude/credentials/api_portal_token)

# Get all APIs (must save to file - large dataset)
curl -s -X GET \
  "${API_BASE_URL}/api-datas?top=9000&skip=0&environment=prd" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  > /tmp/all_apis.json

# Count total APIs
jq '.data | length' /tmp/all_apis.json

# Search locally with jq
jq '.data[] | select(.apiName | test("semantic"; "i"))' /tmp/all_apis.json
```

**Best Practice**: Always save search results to file when expecting many matches:

```bash
~/.claude/skills/btdp-api-search/scripts/run.sh search_api ".*" --output /tmp/all_apis.json
COUNT=$(jq '.data | length' /tmp/all_apis.json 2>/dev/null || jq 'length' /tmp/all_apis.json)
echo "Found ${COUNT} APIs. Results saved to /tmp/all_apis.json"
```

### 2. Get API Information

**Using Python Script**:

```bash
# Get info for a specific API
~/.claude/skills/btdp-api-search/scripts/run.sh get_api_info "global-it4it-btdp-semanticservices-v1"

# Save to file
~/.claude/skills/btdp-api-search/scripts/run.sh get_api_info "global-it4it-btdp-semanticservices-v1" --output /tmp/api_info.json
```

**Using curl**:

```bash
ACCESS_TOKEN=$(cat ~/.claude/credentials/api_portal_token)
API_NAME="global-it4it-btdp-semanticservices-v1"

curl -s -X GET \
  "${API_BASE_URL}/api-datas?top=9000&skip=0&apiName=${API_NAME}&environment=prd" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  | jq .
```

**Response Format**:

```json
{
  "data": [
    {
      "apiName": "global-it4it-btdp-semanticservices-v1",
      "apiTitle": "BTDP Semantic Services API",
      "apiDescription": "API for semantic services...",
      "apiVersion": "v1",
      "apiCategory": "data-services",
      "baseUrl": "https://api.loreal.net/...",
      ...
    }
  ]
}
```

### 3. Get API Specification/Schema (Swagger/OpenAPI)

**IMPORTANT**: API specifications can be very large (10k+ lines). Always save to file.

This operation retrieves the complete OpenAPI schema including:
- All available endpoints and HTTP methods
- Request/response schemas and data models
- Authentication requirements
- Parameter definitions
- Error responses

**Using Python Script**:

```bash
# Get spec and save to file
~/.claude/skills/btdp-api-search/scripts/run.sh get_api_spec "global-it4it-btdp-semanticservices-v1" --output /tmp/api_spec.json
```

**Using curl**:

```bash
ACCESS_TOKEN=$(cat ~/.claude/credentials/api_portal_token)
API_NAME="global-it4it-btdp-semanticservices-v1"

curl -s -X GET \
  "${API_BASE_URL}/api-swagger?top=9000&skip=0&apiName=${API_NAME}&environment=prd" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  > /tmp/api_spec.json

# Check spec size
wc -l /tmp/api_spec.json
```

**Working with Specs**:

```bash
# Extract endpoints
jq '.data[].swagger.paths | keys' /tmp/api_spec.json

# Get specific endpoint details
jq '.data[].swagger.paths["/v1/endpoint"]' /tmp/api_spec.json

# Extract all POST endpoints
jq '.data[].swagger.paths | to_entries | map(select(.value.post)) | from_entries' /tmp/api_spec.json
```

## Common Use Cases

### Use Case 1: Find APIs Related to a Domain

```bash
# Search for all semantic-related APIs
~/.claude/skills/btdp-api-search/scripts/run.sh search_api "semantic" --output /tmp/semantic_apis.json

# Show summary
jq '.[] | {apiName, apiTitle, apiVersion}' /tmp/semantic_apis.json
```

### Use Case 2: Get Complete API Documentation

```bash
API_NAME="global-it4it-btdp-semanticservices-v1"

# Step 1: Get API information
~/.claude/skills/btdp-api-search/scripts/run.sh get_api_info "${API_NAME}" --output "/tmp/${API_NAME}_info.json"

# Step 2: Get API specification
~/.claude/skills/btdp-api-search/scripts/run.sh get_api_spec "${API_NAME}" --output "/tmp/${API_NAME}_spec.json"

# Step 3: Extract key info
echo "=== API Information ==="
jq '.data[0] | {apiName, apiTitle, apiDescription, apiVersion}' "/tmp/${API_NAME}_info.json"

echo ""
echo "=== Available Endpoints ==="
jq '.data[0].swagger.paths | keys' "/tmp/${API_NAME}_spec.json"
```

### Use Case 3: Discover APIs by Category

```bash
# Get all APIs
~/.claude/skills/btdp-api-search/scripts/run.sh search_api ".*" --output /tmp/all_apis.json

# Group by category
jq 'group_by(.apiCategory) | map({category: .[0].apiCategory, count: length})' /tmp/all_apis.json

# List APIs in specific category
jq '.[] | select(.apiCategory == "data-services") | {apiName, apiTitle}' /tmp/all_apis.json
```

### Use Case 4: Extract Endpoint Information

```bash
API_NAME="global-it4it-btdp-semanticservices-v1"

# Get spec
~/.claude/skills/btdp-api-search/scripts/run.sh get_api_spec "${API_NAME}" --output /tmp/spec.json

# Extract all endpoints with methods
jq -r '.data[0].swagger.paths | to_entries[] | "\(.key): \(.value | keys | join(", "))"' /tmp/spec.json

# Get endpoint details
jq '.data[0].swagger.paths["/v1/search"]' /tmp/spec.json
```

## File Management Best Practices

1. **Search Results**: Save to `/tmp/` for inspection
   ```bash
   ~/.claude/skills/btdp-api-search/scripts/run.sh search_api "pattern" --output /tmp/search_results.json
   ```

2. **Large Datasets**: Always check size before loading to context
   ```bash
   wc -l /tmp/all_apis.json
   head -20 /tmp/all_apis.json  # Show first 20 lines
   ```

3. **Filtering**: Use `jq` for post-processing
   ```bash
   jq '.[] | select(.apiVersion == "v1")' /tmp/all_apis.json
   ```

4. **Count Results**: Report counts before showing data
   ```bash
   COUNT=$(jq 'length' /tmp/search_results.json)
   echo "Found ${COUNT} APIs matching the pattern"
   ```

## Response Handling

### Success Response (200)

```json
{
  "data": [
    { "apiName": "...", "apiTitle": "...", ... }
  ],
  "totalCount": 1234
}
```

### Error Response (401)

Token expired or invalid. Regenerate:

```bash
~/.claude/skills/btdp-api-search/scripts/run.sh get_token --save
```

### Error Response (404)

API not found. Verify the API name is correct.

## Troubleshooting

**Token Issues**:

```bash
# Test token validity
ACCESS_TOKEN=$(cat ~/.claude/credentials/api_portal_token)
curl -s -X GET \
  "${API_BASE_URL}/api-datas?top=1&skip=0&environment=prd" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"

# If error, regenerate
~/.claude/skills/btdp-api-search/scripts/run.sh get_token --save
```

**Script Errors**:

```bash
# Check uv is available
which uv

# Manually check dependencies
cd ~/.claude/skills/btdp-api-search/scripts
cat pyproject.toml
```

**API Not Found**:

Search for similar names:

```bash
~/.claude/skills/btdp-api-search/scripts/run.sh search_api "partial.*name" --output /tmp/results.json
jq '.[] | .apiName' /tmp/results.json
```

## Summary Workflow

When the user asks about APIs:

1. **Searching**: Use `search_api` script with regex pattern
   - Always save large results to file
   - Report count before showing data

2. **Getting Info**: Use `get_api_info` for metadata
   - Can output directly for single API
   - Save to file if checking multiple

3. **Getting Spec**: Use `get_api_spec` for OpenAPI docs
   - **Always** save to file (large)
   - Use `jq` to extract relevant sections

4. **Authentication**: Scripts handle automatically
   - Generate token once with `--save`
   - Token reused from `~/.claude/credentials/api_portal_token`

5. **Best Practices**:
   - Save large outputs to `/tmp/` files
   - Count results before displaying
   - Use `jq` for filtering and extraction
   - Check file size with `wc -l`
