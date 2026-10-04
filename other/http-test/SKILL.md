---
name: http-test
description: HTTP API testing with assertions and validations
activation_keywords: [http, api, test, request, assert, response, endpoint]
execution_mode: server
---

# HTTP Test Skill

Perform HTTP API testing with request building and response assertions:

- Send HTTP requests (GET, POST, PUT, DELETE, PATCH)
- Set headers, query params, body
- Assert response status code, headers, body
- Validate JSON response structure and values
- Support authentication (Bearer, Basic, API Key)
- Chain requests (login → API calls)

Use `builtin_http_test` tool with fields:
- `operation`: "request" | "assert"
- `method`: HTTP method (GET, POST, PUT, DELETE, PATCH)
- `url`: Target endpoint URL
- `headers`: (optional) Request headers as JSON
- `body`: (optional) Request body (JSON string)
- `assertions`: (optional) Array of assertions:
  - `type`: "status" | "header" | "body" | "json_path"
  - `expected`: Expected value

Examples:
- Assert status: {"type": "status", "expected": 200}
- Assert body contains: {"type": "body", "expected": "success"}
- Assert JSON path: {"type": "json_path", "path": "$.data.id", "expected": "123"}

Note: All operations are read-only testing, no data modification.