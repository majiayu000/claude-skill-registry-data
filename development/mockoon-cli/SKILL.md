---
name: mockoon-cli
description: Use Mockoon CLI to create API proxies with full request/response logging, mock API servers for testing, and record real API interactions for debugging. Use when testing APIs, creating compatibility layers, debugging microservices, analyzing API traffic patterns, or when the user mentions Mockoon, API mocking, mock servers, or API proxies.
---

# Mockoon CLI for API Proxy Testing and Mock Server Management

## Overview

Mockoon CLI is a production-ready Node.js tool that runs sophisticated mock API servers and transparent proxies for API testing, debugging, and development. With over 400,000 downloads and 7,600+ GitHub stars, it's widely used across Fortune 500 companies for API development workflows.

**Core capabilities:**
- Create transparent proxies to real APIs with full traffic logging
- Run mock API servers from configuration files
- Record and analyze API interactions for debugging
- Generate dynamic responses using templating (Faker.js, Handlebars)
- Combine real and mock endpoints (partial mocking)

## Installation

```bash
# Global installation (recommended)
npm install -g @mockoon/cli

# Verify installation
mockoon-cli --version

# Local project installation
npm install --save-dev @mockoon/cli
```

**Requirements:** Node.js 18+ or 20+

## When to Use Mockoon CLI

**For API Testing:**
- Test your application against controllable mock endpoints
- Simulate error scenarios impossible to trigger in production
- Create reproducible test environments without external dependencies

**For Debugging:**
- Proxy traffic to real APIs and log all requests/responses
- Analyze API behavior across microservices architectures
- Trace correlation IDs and debug integration issues

**For Compatibility Layers:**
- Record real API interactions through proxies
- Design adapters between incompatible API versions
- Convert recorded traffic into permanent mocks

## Quick Start Examples

### Basic Mock Server

```bash
# Start a mock from configuration file
mockoon-cli start --data ./mock-config.json --port 3000

# With transaction logging
mockoon-cli start --data ./mock-config.json --port 3000 --log-transaction
```

### Basic API Proxy

```bash
# Create proxy configuration first (see proxy configuration section)
mockoon-cli start --data ./proxy-config.json --port 3000 --log-transaction
```

## Understanding Mockoon Architecture

Mockoon CLI is fundamentally a companion to the Mockoon desktop GUI application. The workflow is:

1. **Design visually** - Use the desktop app's interface to configure mock APIs
2. **Export configuration** - Save as JSON file (Mockoon data format)
3. **Deploy via CLI** - Run those configurations in headless environments

This separation makes Mockoon uniquely accessible—non-technical team members can design APIs visually while developers automate deployment through CI/CD pipelines.

## Creating API Proxies for Testing and Debugging

### Single API Proxy with Full Logging

**Use case:** Debug interactions with `https://api1.example.com` by proxying all traffic through localhost:3000 and logging everything.

**Proxy configuration** (`api1-proxy.json`):

```json
{
  "uuid": "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
  "lastMigration": 29,
  "name": "API1 Proxy",
  "port": 3000,
  "hostname": "0.0.0.0",
  "routes": [],
  "proxyMode": true,
  "proxyHost": "https://api1.example.com",
  "proxyRemovePrefix": false,
  "cors": true,
  "headers": [
    {
      "key": "X-Proxy-By",
      "value": "Mockoon-Debug"
    }
  ]
}
```

**Start the proxy:**

```bash
mockoon-cli start \
  --data ./api1-proxy.json \
  --port 3000 \
  --log-transaction \
  --max-transaction-logs 500
```

**Route traffic through proxy:**

```bash
# Instead of: curl https://api1.example.com/users/123
# Use: curl http://localhost:3000/users/123

curl http://localhost:3000/users/123
curl -X POST http://localhost:3000/orders -d '{"item": "widget"}'
```

**Access logged data:**

```bash
# Get all transaction logs via Admin API
curl http://localhost:3000/mockoon-admin/logs > api1-logs.json

# Analyze with jq
cat api1-logs.json | jq '.transactions[] | select(.request.url | contains("/users"))'

# Count by HTTP method
cat api1-logs.json | jq '.transactions | group_by(.request.method) | map({method: .[0].request.method, count: length})'

# Find slow responses (>1000ms)
cat api1-logs.json | jq '.transactions[] | select(.responseTime > 1000)'
```

### Multiple API Proxies for Microservices

**Use case:** Debug a system with 3 microservices running on different domains.

Create separate proxy configurations for each service, then start all proxies:

```bash
# Background processes
mockoon-cli start --data ./api1-proxy.json --port 3000 --log-transaction &
mockoon-cli start --data ./api2-proxy.json --port 3001 --log-transaction &
mockoon-cli start --data ./api3-proxy.json --port 3002 --log-transaction &
```

**Or use package.json scripts:**

```json
{
  "scripts": {
    "proxy:api1": "mockoon-cli start -d ./api1-proxy.json -p 3000 --log-transaction",
    "proxy:api2": "mockoon-cli start -d ./api2-proxy.json -p 3001 --log-transaction",
    "proxy:api3": "mockoon-cli start -d ./api3-proxy.json -p 3002 --log-transaction",
    "proxy:all": "run-p proxy:api1 proxy:api2 proxy:api3"
  }
}
```

## Partial Mocking: Combining Real and Mock Endpoints

**Use case:** Proxy most traffic to production, but intercept specific problematic endpoints for testing.

```json
{
  "uuid": "partial-mock-001",
  "lastMigration": 29,
  "name": "Partial Mock Proxy",
  "port": 3000,
  "proxyMode": true,
  "proxyHost": "https://api1.example.com",
  "routes": [
    {
      "uuid": "route-001",
      "method": "get",
      "endpoint": "users/90",
      "responses": [
        {
          "uuid": "response-001",
          "statusCode": 200,
          "body": "{\"id\": 90, \"name\": \"Test User\", \"error_case\": true}",
          "headers": [{"key": "Content-Type", "value": "application/json"}]
        }
      ]
    },
    {
      "uuid": "route-002",
      "method": "post",
      "endpoint": "orders",
      "responses": [
        {
          "uuid": "response-002",
          "statusCode": 500,
          "body": "{\"error\": \"Simulated server error\"}",
          "headers": [{"key": "Content-Type", "value": "application/json"}]
        }
      ]
    }
  ]
}
```

**Behavior:**
- `GET /users/90` → Mocked (returns test data)
- `POST /orders` → Mocked (simulates 500 error)
- All other requests → Proxied to api1.example.com

## Dynamic Response Templating

### Request-Based Responses

```json
{
  "routes": [
    {
      "uuid": "dynamic-001",
      "method": "get",
      "endpoint": "users/:userId",
      "responses": [
        {
          "uuid": "resp-001",
          "statusCode": 200,
          "body": "{\"id\": {{urlParam 'userId'}}, \"name\": \"{{faker 'person.fullName'}}\", \"email\": \"{{faker 'internet.email'}}\"}",
          "headers": [{"key": "Content-Type", "value": "application/json"}]
        }
      ]
    }
  ]
}
```

**Available template helpers:**
- `{{urlParam 'name'}}` - Path parameters
- `{{queryParam 'name' 'default'}}` - Query strings
- `{{body 'path.to.field'}}` - Request body properties
- `{{header 'Header-Name'}}` - Request headers
- `{{faker 'category.method'}}` - Generate fake data
- `{{now}}` - Current timestamp
- `{{faker 'string.uuid'}}` - Generate UUID

### Conditional Responses for Error Testing

```json
{
  "routes": [
    {
      "uuid": "conditional-001",
      "method": "post",
      "endpoint": "payments",
      "responses": [
        {
          "uuid": "resp-success",
          "statusCode": 200,
          "body": "{\"status\": \"success\", \"transactionId\": \"{{faker 'string.uuid'}}\"}",
          "rules": [
            {
              "target": "body",
              "modifier": "amount",
              "value": "100",
              "operator": "gte"
            }
          ]
        },
        {
          "uuid": "resp-insufficient",
          "statusCode": 400,
          "body": "{\"error\": \"Insufficient funds\"}",
          "default": true
        }
      ]
    }
  ]
}
```

## Minimal Configuration Structure

```json
{
  "uuid": "unique-environment-id",
  "lastMigration": 29,
  "name": "My Mock API",
  "port": 3000,
  "hostname": "0.0.0.0",
  "routes": [],
  "cors": true
}
```

## Command Reference

### Core Commands

```bash
# Start with basic options
mockoon-cli start -d ./config.json -p 3000

# Enable file watching (auto-reload on changes)
mockoon-cli start -d ./config.json -p 3000 --watch

# Multiple environments simultaneously
mockoon-cli start -d ./api1.json -d ./api2.json -p 3000 -p 3001

# Custom hostname
mockoon-cli start -d ./config.json -p 3000 --hostname 127.0.0.1

# Disable TLS for testing
mockoon-cli start -d ./config.json -p 3000 --disable-tls
```

### Validation

```bash
# Validate configuration files
mockoon-cli validate --data ~/api1.json ~/api2.json

# Returns specific errors like:
# - "name is required"
# - "port must be a number"
# - "routes must be an array"
```

### OpenAPI Import/Export

```bash
# Import OpenAPI to create Mockoon config
mockoon-cli import --input ~/openapi.yaml --output ./mockoon.json --prettify

# Export Mockoon config to OpenAPI v3
mockoon-cli export --input ~/mockoon.json --output ./openapi.json --prettify
```

### Admin API Endpoints

```bash
# Get transaction logs
curl http://localhost:3000/mockoon-admin/logs

# Clear transaction logs
curl -X PURGE http://localhost:3000/mockoon-admin/logs

# Get server state
curl http://localhost:3000/mockoon-admin/state

# Manage global variables
curl http://localhost:3000/mockoon-admin/global-vars
curl -X PURGE http://localhost:3000/mockoon-admin/global-vars
```

### Environment Variables

```bash
# Access with MOCKOON_ prefix by default
# In templates: {{getEnvVar 'API_KEY'}}
# Reads from: MOCKOON_API_KEY environment variable

# Custom prefix
mockoon-cli start -d ./config.json --env-vars-prefix CUSTOM_

# No prefix
mockoon-cli start -d ./config.json --env-vars-prefix ""
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: API Integration Tests
on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Mockoon CLI
        run: npm install -g @mockoon/cli

      - name: Start API Proxy
        run: |
          mockoon-cli start \
            --data ./test/proxy-config.json \
            --port 3000 \
            --log-transaction &
          sleep 3

      - name: Run Integration Tests
        run: npm test
        env:
          API_BASE_URL: http://localhost:3000

      - name: Collect Proxy Logs
        if: always()
        run: curl http://localhost:3000/mockoon-admin/logs > proxy-logs.json

      - name: Upload Logs
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: proxy-logs
          path: proxy-logs.json
```

## Analyzing Transaction Logs

### Log Structure

```json
{
  "transactions": [
    {
      "request": {
        "method": "POST",
        "url": "/api/users",
        "headers": {
          "content-type": "application/json",
          "authorization": "Bearer token123"
        },
        "body": "{\"name\":\"John\",\"email\":\"john@example.com\"}"
      },
      "response": {
        "statusCode": 201,
        "headers": {
          "content-type": "application/json"
        },
        "body": "{\"id\":\"123\",\"name\":\"John\"}"
      },
      "timestamp": "2025-10-24T10:30:45.123Z",
      "responseTime": 45
    }
  ]
}
```

## Best Practices

### Project Organization

```
project/
├── mockoon/
│   ├── api1-proxy.json
│   ├── api2-proxy.json
│   ├── api3-proxy.json
│   └── data/
│       └── mock-responses/
├── scripts/
│   ├── collect-logs.sh
│   └── analyze-logs.js
└── package.json
```

### Configuration Management

- **Descriptive names:** Use `users-api.json`, not `environment-1.json`
- **Version control:** Commit all JSON configurations to Git
- **Relative paths:** Use `./data/user-123.json` for portability
- **Documentation:** Add comments in route `documentation` fields

### Security Considerations

- Disable admin API in production: `--disable-admin-api`
- Use environment variables for sensitive data
- Don't commit API keys in configuration files
- Run as non-root user in containers

## Troubleshooting

### Port Conflicts

```bash
# Check if port is in use
netstat -tln | grep 3000

# Use different port
mockoon-cli start -d ./config.json -p 3001
```

### Validation Errors

```bash
# Validate before starting
mockoon-cli validate --data ./config.json

# Common issues:
# - Missing required fields (name, port)
# - Invalid JSON syntax
# - Incorrect route structure
```

### Proxy Connection Issues

```bash
# Test proxy target is reachable
curl -v https://api1.example.com/health

# Check proxy logs
mockoon-cli start -d ./proxy.json --log-transaction

# Verify proxy configuration
cat proxy.json | jq '.proxyHost'
```

### Performance Issues

```bash
# Limit transaction logs to reduce memory
mockoon-cli start -d ./config.json --max-transaction-logs 100

# Disable file logging
mockoon-cli start -d ./config.json --disable-log-to-file

# Use --watch only in development
mockoon-cli start -d ./config.json --watch
```

## Additional Resources

- Official documentation: https://mockoon.com/docs/latest/
- CLI reference: https://mockoon.com/docs/latest/mockoon-cli/overview/
- Desktop application: https://mockoon.com/download/
- GitHub repository: https://github.com/mockoon/mockoon

## Summary

Mockoon CLI enables:
- **Transparent API proxying** with full traffic logging for debugging
- **Multi-service debugging** across microservices architectures
- **Compatibility layer design** through recorded interactions
- **Integration testing** with controllable mock responses
- **Performance analysis** via transaction log examination

The proxy-first approach makes Mockoon CLI ideal for understanding real API behavior, debugging integration issues, and designing adapters without modifying application code.
