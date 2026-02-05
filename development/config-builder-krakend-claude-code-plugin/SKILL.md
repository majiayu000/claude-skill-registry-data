---
name: config-builder
description: Creates new KrakenD configurations with best practices, proper structure, and edition-appropriate features
---

# KrakenD Configuration Builder

## Purpose
Guides users through creating new KrakenD configurations with best practices, proper structure, and edition-appropriate features. Provides interactive creation with validation at each step.

## When to activate
- User asks to create a new KrakenD configuration
- User mentions "new config", "create krakend", "setup api gateway", "build config"
- User wants to add endpoints to existing config
- User needs help structuring their KrakenD setup

## What this skill does

Creates KrakenD configurations using one of two approaches:

### Simple Scenarios (Direct Generation)
**When:** 1-3 endpoints with straightforward routing
**Approach:** Generate directly using tools

1. Gather requirements through targeted questions
2. Generate configuration using templates and best practices
3. Validate as you build to prevent errors early
4. Suggest optimizations based on use case

### Complex Scenarios (Spawn Agent)
**When:** >3 endpoints, advanced features, or microservices architecture
**Approach:** Spawn `config-architect` agent

1. Agent designs complete architecture
2. Maps services and dependencies
3. Configures proper isolation and resilience
4. Returns comprehensive documentation

## Tools used
- `generate_basic_config` - Create complete configuration
- `generate_endpoint_config` - Create individual endpoints
- `generate_backend_config` - Create backend configurations
- `get_feature_config_template` - Get templates for specific features
- `list_features` - Browse available features and check edition requirements
- `check_edition_compatibility` - Verify if config requires CE or EE
- `validate_config` - Validate generated configuration
- `search_documentation` - Find relevant examples

## Configuration Generation Workflow

### Step 1: Understand Requirements
Ask user about:
- What endpoints do they need? (paths and methods)
- What are the backend services? (URLs)
- Do they need authentication? (JWT, API keys, etc.)
- Do they need rate limiting?
- Are they using Community or Enterprise Edition?

### Step 2: Choose Approach
**Simple (1-3 endpoints):** Continue with direct generation
**Complex (>3 services):** Spawn `config-architect` agent

### Step 3: Generate Configuration
```
1. Start with basic structure (generate_basic_config)
2. Add endpoints one by one (generate_endpoint_config)
3. Add features as needed (get_feature_config_template)
4. Validate after each addition (validate_config)
```

### Step 4: Apply Best Practices
Always include:
- ✅ Circuit breakers for reliability
- ✅ Timeouts to prevent hanging
- ✅ Rate limiting for protection
- ✅ Authentication for sensitive endpoints
- ✅ Proper error handling

### Step 5: Validate and Present
- Run `validate_config` on final result
- Track which edition features were used (CE or EE)
- Show appropriate test command based on configuration
- Highlight any warnings or best practices
- Offer to save to file

### Testing Commands

After generating config, provide test command based on: (1) Version from `$schema`, (2) Edition (CE/EE by features used), (3) FC if applicable, (4) LICENSE file for EE.

**Examples:**
```bash
# CE
docker run --rm -v $(pwd):/etc/krakend krakend:VERSION check -tlc /etc/krakend/krakend.json

# EE (requires LICENSE file)
docker run --rm -v $(pwd):/etc/krakend krakend/krakend-ee:VERSION check -tlc /etc/krakend/krakend.json
```

**Flags:** Use `-tlc` (test + lint + config) to catch anti-patterns and best practices violations.
**FC:** CE requires `FC_ENABLE=1` + env vars; EE auto-detects. **Images:** `krakend:VERSION` (CE), `krakend/krakend-ee:VERSION` (EE).

## Output format

```
# KrakenD Configuration Created

I've created a KrakenD configuration for you:

## Summary
- Port: 8080
- Endpoints: 3
- Features: JWT validation, rate limiting, circuit breakers
- Edition: Community Edition compatible

## Configuration

\`\`\`json
{
  "version": 3,
  "$schema": "https://www.krakend.io/schema/krakend.json",
  "port": 8080,
  "timeout": "3000ms",
  "endpoints": [
    ...
  ]
}
\`\`\`

## Features Included

### Authentication (JWT)
- Validates tokens from your identity provider
- **Location**: endpoints[0].extra_config["auth/validator"]
- **Docs**: https://www.krakend.io/docs/authorization/jwt-validation/

### Rate Limiting
- Protects endpoints from overload
- **Config**: 100 requests/second per endpoint
- **Docs**: https://www.krakend.io/docs/endpoints/rate-limit/

### Circuit Breakers
- Prevents cascade failures
- **Config**: Opens after 5 errors in 60 seconds
- **Docs**: https://www.krakend.io/docs/backends/circuit-breaker/

## Next Steps

1. **Save this configuration** to `krakend.json`
2. **Test it**: `docker run --rm -v $(pwd):/etc/krakend krakend:latest check -tlc /etc/krakend/krakend.json`
3. **Run it**: `docker run --rm -p 8080:8080 -v $(pwd):/etc/krakend krakend:latest run -c /etc/krakend/krakend.json`
4. **Monitor**: Check logs at startup

Would you like me to:
- Add more endpoints?
- Add additional features (caching, CORS, etc.)?
- Optimize for specific use case?
- Explain any part in detail?
```

## Best practices

1. **Ask before assuming** - Don't guess backend URLs or requirements
2. **Validate edition compatibility** - Check if requested features need EE (warn users upfront)
3. **Always include safety features** - Circuit breakers, timeouts, rate limits
4. **Explain what you're adding** - Don't just dump JSON, explain each part
5. **Offer alternatives** - If they request EE feature but have CE, suggest alternatives
6. **Validate before presenting** - Never show invalid configurations
7. **Track edition features** - Remember which features require EE as you add them
8. **Provide appropriate commands** - Show test/run commands matching their config's edition

## Examples

### Example 1: Simple REST API Gateway

**User**: "Create a config for my REST API at https://api.example.com"

**Response:**
"I'll create a KrakenD configuration for your REST API. Let me ask a few questions:

1. What endpoints do you want to expose? (e.g., GET /users, POST /users)
2. Do you need authentication? (JWT, API keys, or none)
3. Should I add rate limiting?

Or should I create a basic setup and you can tell me what to adjust?"

[User provides answers]
[Generate configuration using tools]
[Present as shown in output format above]

### Example 2: Complex Microservices Gateway

**User**: "I need a gateway for my microservices: user-service, order-service, payment-service, and inventory-service. Each has multiple endpoints."

**Response:**
"This sounds like a complex microservices architecture with 4+ services. I'm going to spawn the config-architect agent to design this properly. The agent will:

1. Map out all your services and endpoints
2. Design the aggregation strategy
3. Configure proper isolation (circuit breakers per service)
4. Set up authentication and rate limiting
5. Optimize for performance

One moment while I analyze your requirements..."

[Spawn config-architect agent]

### Example 3: Adding features to existing config

**User**: "Add JWT validation to my existing config"

**Response:**
"I'll add JWT validation to your configuration. I need a few details:

1. **Algorithm**: Which algorithm does your JWT use? (RS256, HS256, etc.)
2. **JWK URL**: Where can KrakenD fetch your public keys?
3. **Audience**: What audience value should KrakenD expect?

Also, which endpoints need JWT validation? (all, or specific ones?)"

[User provides details]
[Use `get_feature_config_template` for JWT]
[Merge into existing config]
[Validate with `validate_config`]
[Present updated configuration with test command]

## Integration & Error Handling

### Integration with other skills
- After creating config → Offer to validate with `config-validator` skill
- If user asks "what features are available" → Hand off to `feature-explorer` skill
- If config already exists and user wants changes → Treat as modification, not new creation
- After generation → Suggest security audit with `security-auditor` skill

### Error handling
- **User's backend URLs are unreachable**: Note this, proceed with config anyway
- **Requested feature requires EE but user has CE**: Explain clearly and offer CE alternatives
- **Requirements are unclear**: Ask specific questions, don't guess
- **Configuration becomes too complex**: Suggest splitting into multiple configs or use agent

### When to spawn config-architect agent
- More than 3 services with multiple endpoints each
- Complex aggregation needed (combining multiple backends)
- Advanced patterns requested (sequential calls, conditional routing)
- User explicitly asks for architectural guidance
- Microservices architecture mentioned

## Tips for Great Configs

1. **Start small** - Basic config first, add features incrementally
2. **Explain defaults** - Tell user why you chose specific timeout, rate limit, etc.
3. **Think about production** - Include monitoring, logging, error handling from the start
4. **Edition awareness** - Always check CE vs EE before adding features
5. **Link to docs** - Help user learn, don't just generate config
6. **Provide test commands** - Show exactly how to validate and run their new config
