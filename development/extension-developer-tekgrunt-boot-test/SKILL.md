---
name: extension-developer
description: Use this skill when the user needs help building, testing, or deploying custom LimaCharlie extensions.
---

# LimaCharlie Extension Developer

This skill helps you build custom LimaCharlie extensions. Use this when users ask for help creating extensions, understanding the extension architecture, building UI components, or debugging extension issues.

## What are LimaCharlie Extensions?

LimaCharlie Extensions are small HTTPS services that receive webhooks from the LimaCharlie cloud, enabling you to expand and customize security environments by integrating third-party tools, automating workflows, and adding new capabilities.

### Key Benefits

- **Multi-tenancy**: LC organizations can subscribe to your extension and replicate features across tenants
- **Credentials handling**: No need to store credentials - every callback includes an authenticated LimaCharlie SDK with requested permissions
- **Configuration**: LC provides a configuration JSON object stored in Hive with validation callbacks
- **Auto-generated UI**: Extensions define a schema that LimaCharlie interprets to generate custom user interfaces

### Public vs Private Extensions

- **Private Extensions**: Require `billing.ctrl` and `user.ctrl` permissions to subscribe an organization
- **Public Extensions**: Visible and subscribable by everyone (contact answers@limacharlie.io to make an extension public)

## Extension Architecture

### High-Level Structure

Extensions are HTTPS services that:
1. Receive webhooks from LimaCharlie cloud
2. Process requests using the LimaCharlie SDK (provided in callbacks)
3. Return responses in JSON format
4. Can be hosted on Google Cloud Run, AWS Lambda, or custom infrastructure

### Request/Response Model

```
User/D&R Rule → LimaCharlie Cloud → Extension (via webhook)
                                   ↓
                        Process with LC SDK
                                   ↓
                        Return JSON Response
```

Each webhook includes:
- **Request data**: Action name and parameters
- **Authenticated SDK**: Pre-configured with org-specific permissions
- **Organization context**: Relevant to the callback
- **Signature**: Shared secret for authenticity verification

## Quick Start

### Step 1: Choose Framework

**Golang** (recommended for stricter typing):
```
https://github.com/refractionPOINT/lc-extension
```

**Python**:
```
https://github.com/refractionPOINT/lc-extension/tree/master/python
```

### Step 2: Create Extension Definition

Navigate to: https://app.limacharlie.io/add-ons/published

Required fields:
- **Destination URL**: HTTPS endpoint for your extension
- **Required Extensions**: List of other extensions your extension depends on
- **Shared Secret**: Random string (32+ characters) for webhook signature verification
- **Extension Flairs**:
  - `segment`: Isolates resources (extension can only see/modify what it created)
  - `bulk`: Increases API quota for extensions making many API calls
- **Permissions**: List of required permissions (use least privilege)

### Step 3: Define Schema

Create a basic schema with configuration and actions:

```json
{
  "config_schema": {
    "fields": {
      "api_key": {
        "data_type": "secret",
        "description": "API key for external service",
        "label": "API Key"
      }
    },
    "requirements": [["api_key"]]
  },
  "request_schema": {
    "scan": {
      "is_impersonated": false,
      "is_user_facing": true,
      "short_description": "Scan a sensor",
      "parameters": {
        "fields": {
          "sid": {
            "data_type": "sid",
            "description": "Sensor ID to scan",
            "label": "Sensor"
          }
        },
        "requirements": [["sid"]]
      }
    }
  },
  "required_events": ["subscribe", "unsubscribe"]
}
```

### Step 4: Implement Callbacks

```go
e.OnRequest("scan", func(ctx *ext.Context) (interface{}, error) {
    sid := ctx.Params["sid"].(string)
    results := performScan(ctx.SDK, sid)
    return map[string]interface{}{"status": "completed", "findings": results}, nil
})

e.OnEvent("subscribe", func(ctx *ext.Context) error {
    log.Printf("New subscription: %s", ctx.OID)
    return nil
})
```

### Step 5: Deploy and Test

1. Deploy to Cloud Run, Lambda, or custom infrastructure
2. Update extension with destination URL
3. Test locally with ngrok for debugging
4. Subscribe a test organization
5. Invoke actions from UI or D&R rules

## Extension Schema Basics

### Schema Structure

```json
{
  "config_schema": {
    "fields": { /* configuration fields */ },
    "requirements": [ /* required fields */ ]
  },
  "request_schema": {
    "action_name": {
      "is_impersonated": false,
      "is_user_facing": true,
      "short_description": "Brief description",
      "long_description": "Detailed description",
      "parameters": {
        "fields": { /* action parameters */ },
        "requirements": [ /* required parameters */ ]
      },
      "response": {
        "fields": { /* response structure */ }
      }
    }
  },
  "required_events": ["subscribe", "unsubscribe", "update"]
}
```

### Field Structure

Every field follows this minimal structure:

```json
{
  "field_name": {
    "data_type": "string",
    "description": "Field description",
    "label": "Human Readable Label",
    "placeholder": "Example value",
    "display_index": 1,
    "default_value": "default"
  }
}
```

### Requirements Array

The `requirements` field defines which fields are required:

```json
// Both fields required
"requirements": [["denominator"], ["numerator"]]

// denominator AND (numerator OR default) required
"requirements": [["denominator"], ["numerator", "default"]]
```

- First array joins with AND
- Nested arrays join with OR

## Common Data Types

| Type | Description | Example |
|------|-------------|---------|
| `string` | Text value | Any text |
| `integer` | Number | 42 |
| `bool` | Boolean | true/false |
| `enum` | Selection from list | Requires `enum_values` |
| `sid` | Sensor ID | UUID format |
| `secret` | Secret from secrets manager | Encrypted value |
| `json` | JSON data | Any JSON object |
| `yaml` | YAML data | YAML content |
| `object` | Nested fields | Complex structures |

For complete data type reference, see [REFERENCE.md](./REFERENCE.md).

## Request Handling

Actions are defined in `request_schema` with parameters:
- **is_impersonated**: Uses user's authentication context
- **is_user_facing**: Shows in UI (false = API/D&R only)
- **parameters**: Input fields for the action
- **response**: Expected output structure

```go
e.OnRequest("action_name", func(ctx *ext.Context) (interface{}, error) {
    param := ctx.Params["param_name"].(string)
    config, _ := ctx.SDK.Hive().Get("extension_configuration", "my-ext")
    sensor, _ := ctx.SDK.Sensor(param).Get()
    return map[string]interface{}{"status": "success", "data": sensor}, nil
})

e.OnEvent("subscribe", func(ctx *ext.Context) error {
    return ctx.SDK.Rules().Add("my-rule", ruleContent)
})
```

## UI Development Basics

### Auto-Generated UI

LimaCharlie automatically generates UI from your schema. The UI adapts based on data types and layout configuration.

### Layout Types

Specify layout in schema's top-level `layout` field:

- **auto** (default): Automatically selects appropriate layout
- **config**: Prioritizes configuration display
- **editor**: For large code blocks (YAML/JSON editing)
- **action**: Prioritizes specific actions with in-page forms
- **description**: Description-focused layout

### Multiple Layouts (Tabs)

```json
{
  "views": [
    {
      "name": "Configuration",
      "layout": "config"
    },
    {
      "name": "Actions",
      "layout": "action",
      "default_action": "scan"
    },
    {
      "name": "Documentation",
      "layout": "description"
    }
  ]
}
```

### Tables with Object Lists

Use `is_list: true` with object data type to create table UI:

```json
{
  "rules": {
    "data_type": "object",
    "is_list": true,
    "description": "Detection rules",
    "object": {
      "fields": {
        "name": {
          "data_type": "string",
          "description": "Rule name"
        },
        "severity": {
          "data_type": "enum",
          "enum_values": ["low", "medium", "high"]
        }
      }
    }
  }
}
```

## Using Extensions

### From D&R Rules

```yaml
detect:
  event: NEW_PROCESS
  op: is
  path: event/FILE_PATH
  value: /usr/bin/suspicious
respond:
  - action: extension request
    extension name: my-scanner
    extension action: scan
    extension request:
      sid: '{{ .routing.sid }}'
```

### From CLI

```bash
limacharlie extension request \
  --name my-scanner \
  --action scan \
  --data '{"sid": "sensor-id"}'
```

### From API

```bash
curl -X POST "https://api.limacharlie.io/v1/ext/my-scanner/request" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"oid": "org-id", "action": "scan", "params": {"sid": "sensor-id"}}'
```

## Best Practices

**Security**: Always verify webhook signatures, use least privilege permissions, validate all input, secure secrets in environment variables, use segment flair for resource isolation.

**Performance**: Use async operations for long tasks, cache configurations, use bulk flair for high API usage, implement timeouts.

**Error Handling**: Return meaningful errors, handle partial failures gracefully, maintain comprehensive logs.

## Simplified Frameworks

**D&R Framework**: Package D&R rules for distribution using `lc-extension/simplified/dr`

**Lookup Framework**: Package threat intelligence lookups using `lc-extension/simplified/lookup`

**CLI Framework**: Integrate external CLI tools using `lc-extension/simplified/cli`

See [EXAMPLES.md](./EXAMPLES.md) for complete implementations.

## Navigation

- **[REFERENCE.md](./REFERENCE.md)**: Complete extension architecture, all data types, field options, request/response formats
- **[EXAMPLES.md](./EXAMPLES.md)**: Complete extension examples with full code (alerting, scanning, etc.)
- **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)**: Testing strategies, deployment guides, debugging tips

## Quick Reference

**Extension Definition**: Destination URL (HTTPS endpoint), Shared Secret (32+ chars), Permissions array, Extension Flairs (`segment`, `bulk`)

**Schema Fields**: `config_schema` (configuration), `request_schema` (actions), `required_events` (subscribe/unsubscribe/update), `layout` (UI type), `views` (tabs)

**Callbacks**: Request (handle actions), Event (handle subscribe/unsubscribe/update), Config Validation (validate changes)

**Common Permissions**: `sensor.get/task`, `dr.get/set`, `hive.get/set`, `artifact.get`, `outputs.get/set`

## Additional Resources

**Code**: [Golang Framework](https://github.com/refractionPOINT/lc-extension) | [Python Framework](https://github.com/refractionPOINT/lc-extension/tree/master/python)

**API Docs**: [Extension API](https://api.limacharlie.io/static/swagger/#/Extension-Request) | [Schema API](https://api.limacharlie.io/static/swagger/#/Extension-Schema)

**Support**: Community Slack | answers@limacharlie.io

## Key Reminders

Always verify webhook signatures, use least privilege permissions, validate input, test with test organizations first, use segment flair for isolation, implement proper error handling, cache configurations, use simplified frameworks for common patterns, test locally with ngrok before deploying.
