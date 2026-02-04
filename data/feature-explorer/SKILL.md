---
name: feature-explorer
description: Discovers KrakenD features, checks edition availability (CE vs EE), and provides implementation examples
---

# KrakenD Feature Explorer

## Purpose
Helps users discover KrakenD features, understand their capabilities, check edition availability (CE vs EE), and learn how to implement them. Prevents non-existent feature usage and edition confusion.

## When to activate
- User asks about a specific KrakenD feature ("how to add rate limiting", "does KrakenD support websockets")
- User mentions "enable", "configure", "setup" + feature name
- User asks what features are available in a category
- User wants to know CE vs EE differences

## What this skill does

1. **Searches for features** by name, namespace, or category
2. **Checks edition availability** (Community vs Enterprise)
3. **Provides configuration examples** with explanations
4. **Links to documentation** for detailed learning
5. **Suggests related features** that work well together
6. **Warns about edition requirements** upfront

## Feature Categories

Understanding KrakenD's feature organization helps users discover what they need:

- **authentication**: JWT, API keys, OAuth, Basic Auth
- **security**: CORS, Policies, TLS, IP filtering
- **traffic-management**: Rate limiting, Circuit breakers
- **connectivity**: gRPC, GraphQL, WebSockets, SOAP
- **transformation**: JMESPath, Lua, Request/Response modifiers
- **reliability**: Circuit breakers, Timeouts, Retries
- **observability**: Metrics, Logging, Tracing
- **caching**: HTTP caching, Backend caching

## Tools used
- `list_features` - List all features with name, namespace, edition (CE/EE/both), category, and description
- `get_feature_config_template` - Get configuration template with required/optional fields
- `search_documentation` - Search KrakenD documentation for detailed information
- `check_edition_compatibility` - Detect which edition is required for a configuration
- `refresh_documentation_index` - Force refresh of doc cache (auto-runs if >7 days old)

## Feature Exploration Workflow

### Step 1: Understand User Need
- What feature are they looking for?
- What problem are they trying to solve?
- Do they have CE or EE?

### Step 2: Search and Verify
- Use `list_features` to find matching features (filter by category if helpful)
- Check edition availability for each match
- If EE-only and user has CE: Prepare alternatives

### Step 3: Provide Implementation Guidance
- Get config template with `get_feature_config_template`
- Explain what each field does
- Show complete example in context
- Link to docs for deeper details

### Step 4: Suggest Related Features
- What other features work well with this?
- What's the recommended combination?
- Any prerequisites or dependencies?

### Step 5: Provide Testing Command
When users ask "how do I test this?", provide command based on: (1) Feature edition (CE/EE), (2) Version from `$schema`, (3) LICENSE for EE.

**Examples:**
```bash
# CE feature
docker run --rm -v $(pwd):/etc/krakend krakend:latest check -tlc /etc/krakend/krakend.json

# EE feature (requires LICENSE file)
docker run --rm -v $(pwd):/etc/krakend krakend/krakend-ee:latest check -tlc /etc/krakend/krakend.json
```

**Flags:** Use `-tlc` (test + lint + config) for comprehensive validation including best practices.
**Images:** `krakend:VERSION` (CE), `krakend/krakend-ee:VERSION` (EE).

## Output format

```
# [Feature Name]

## Availability
✅ Community Edition | ⚠️ Enterprise Edition Only

## Description
[Clear explanation of what the feature does]

## Use Case
[When and why you'd use this feature]

## Configuration

\`\`\`json
{
  "extra_config": {
    "[namespace]": {
      "[field]": "[value]",
      // Explanation of what this does
    }
  }
}
\`\`\`

## Required Fields
- `field1`: Description
- `field2`: Description

## Optional Fields
- `field3`: Description (default: X)
- `field4`: Description

## Example
[Complete, working example in context]

## Related Features
- **[Feature A]**: Works great with this for [reason]
- **[Feature B]**: Consider adding for [benefit]

## Documentation
📚 [https://www.krakend.io/docs/...]

## Common Mistakes
❌ [Common mistake 1]
✅ [Correct approach]
```

## Best Practices

1. **Edition-first** - Always show edition availability prominently (users need to know immediately)
2. **Complete examples** - Show feature in full context, not isolated snippets
3. **Explain benefits** - Don't just show config, explain why users would want this
4. **Link to docs** - Official documentation for comprehensive information
5. **Suggest combinations** - Features rarely work in isolation
6. **Warn about gotchas** - Common mistakes and edge cases
7. **Show, don't tell** - Always include config examples, not just descriptions
8. **Context matters** - Explain when and why to use each feature
9. **Edition clarity** - Make CE vs EE crystal clear upfront
10. **Real examples** - Use realistic values, not dummy data

## Examples

### Example 1: User asks about rate limiting

**User**: "How do I add rate limiting to my API?"

**Response:**
"KrakenD has excellent rate limiting! Let me show you the options:

# Rate Limiting in KrakenD

KrakenD offers **two types** of rate limiting:

## 1. Endpoint Rate Limiting (Recommended)
✅ **Community Edition** - Available in both CE and EE
- Limits requests **to your endpoints**
- Protects your gateway from overload

**Configuration:**
\`\`\`json
{
  "endpoint": "/api/users",
  "extra_config": {
    "qos/ratelimit/router": {
      "max_rate": 100,      // Max requests per second
      "capacity": 100        // Burst capacity
    }
  }
}
\`\`\`

## 2. Backend Rate Limiting
✅ **Community Edition**
- Limits requests **to your backend services**
- Protects backends from overload

**Configuration:**
\`\`\`json
{
  "backend": [{
    "url_pattern": "/users",
    "host": ["https://api.example.com"],
    "extra_config": {
      "qos/ratelimit/proxy": {
        "max_rate": 50,
        "capacity": 50
      }
    }
  }]
}
\`\`\`

## 3. Stateful Rate Limiting (Enterprise Only)
⚠️ **Enterprise Edition** - Requires EE
- Uses Redis for distributed rate limiting
- Consistent limits across multiple gateway instances

Which type fits your needs? I can help you implement any of them.

📚 Docs: https://www.krakend.io/docs/endpoints/rate-limit/"

### Example 2: User asks about Enterprise feature

**User**: "How do I enable WebSockets?"

**Response:**
"WebSocket support is an **Enterprise Edition feature** and requires a commercial license.

# WebSocket Support

⚠️ **Enterprise Edition Only** - Not available in Community Edition

## What it provides
- Bidirectional communication
- Real-time data streaming
- Event-driven architecture

## Enterprise Configuration
\`\`\`json
{
  "endpoint": "/ws",
  "extra_config": {
    "websocket": {
      "input_headers": ["*"],
      "connect_event": true,
      "disconnect_event": true
    }
  }
}
\`\`\`

## Community Edition Alternatives

If you're using Community Edition, consider these alternatives:

### Option 1: Server-Sent Events (SSE)
✅ One-way real-time updates from server
✅ Works with standard HTTP
✅ Available in CE

### Option 2: Long Polling
✅ Simulate real-time with HTTP requests
✅ Available in CE
✅ Good browser compatibility

### Option 3: Upgrade to Enterprise
Get WebSockets plus:
- API key authentication
- Security policies engine
- Advanced features

Would you like help implementing an alternative, or information about Enterprise Edition?"

### Example 3: User asks "what can KrakenD do?"

**Response:**
"KrakenD is packed with features! Let me show you by category:

# KrakenD Features Overview

## 🔒 Security & Authentication
- JWT Validation ✅ CE
- CORS Configuration ✅ CE
- API Key Auth ⚠️ EE
- Security Policies ⚠️ EE
- Basic Auth ✅ CE
- OAuth Client ✅ CE
- TLS/mTLS ✅ CE

## 🚦 Traffic Management
- Rate Limiting (endpoint) ✅ CE
- Rate Limiting (backend) ✅ CE
- Rate Limiting (stateful) ⚠️ EE
- Circuit Breakers ✅ CE
- Load Balancing ✅ CE

## 🔌 Connectivity
- REST/HTTP ✅ CE
- gRPC ✅ CE
- GraphQL ✅ CE
- WebSockets ⚠️ EE
- SOAP ⚠️ EE
- AMQP/RabbitMQ ✅ CE

## 🔄 Data Transformation
- Response Manipulation (JMESPath) ✅ CE
- Request/Response Modifiers ✅ CE
- Data Aggregation ✅ CE
- Lua Scripting ✅ CE

## 📊 Observability
- OpenTelemetry ✅ CE
- Prometheus Metrics ✅ CE
- Logging (structured) ✅ CE
- Tracing (Jaeger, Zipkin) ✅ CE
- Moesif Integration ⚠️ EE

**Legend:**
✅ CE = Community Edition (open source, free)
⚠️ EE = Enterprise Edition (commercial)

What area interests you? I can provide detailed configuration for any feature."

## Feature Combinations

Always suggest powerful combinations:

- **Rate Limiting** → Add Circuit Breaker (reliability)
- **JWT Validation** → Add CORS (web clients)
- **Multiple Backends** → Add Circuit Breakers per backend
- **Public APIs** → Add Rate Limiting + Authentication
- **Microservices** → Add Service Discovery + Load Balancing
- **Production APIs** → Add Observability (metrics + tracing + logging)

## Integration & Error Handling

### Integration with other skills
- If user wants to implement feature → Hand off to `config-builder` skill
- If user wants to validate existing feature config → Hand off to `config-validator` skill
- If user asks about complex architecture → Consider spawning `config-architect` agent

### Error handling
- **Feature doesn't exist**: Search similar features, suggest alternatives
- **User has CE but wants EE feature**: Clearly explain, offer CE alternatives
- **Feature is deprecated**: Mention replacement, provide migration path
- **Multiple matches**: Show all, let user choose which they meant
- **Documentation outdated**: Use `refresh_documentation_index` and retry
