---
name: provider-config-validator
description: Validate and debug Vercel AI SDK provider configurations including API keys, environment setup, model compatibility, and rate limiting. Use when encountering provider errors, authentication failures, API key issues, missing environment variables, model compatibility problems, rate limiting errors, or when user mentions provider setup, configuration debugging, or SDK connection issues.
allowed-tools: Read, Grep, Glob, Bash
---

# Provider Configuration Validator

**Purpose:** Autonomously validate, diagnose, and fix Vercel AI SDK provider configurations.

**Activation Triggers:**
- API errors (401, 403, 429, 404)
- Missing/invalid API keys
- Package installation issues
- Model compatibility errors
- Environment variable problems
- Import/connection failures

**Key Resources:**
- `scripts/validate-provider.sh` - Full validation (packages, keys, env)
- `scripts/check-model-compatibility.sh` - Validate model names
- `scripts/generate-fix.sh` - Generate fixes for common issues
- `scripts/test-provider-connection.sh` - Test real API connection
- `examples/troubleshooting-guide.md` - Comprehensive troubleshooting (10+ scenarios)
- `templates/` - .env, .gitignore, error handler code templates

## Diagnostic Workflow

### 1. Detect Issue Type

Identify error from symptoms:
- **401/403**: Invalid API key → Check key format and env var
- **429**: Rate limiting → Add retry logic
- **404/model_not_found**: Invalid model → Validate model name
- **Cannot find module**: Missing package → Install provider SDK
- **Missing env var**: No .env → Create .env file
- **Import error**: Wrong syntax → Fix imports for framework

### 2. Run Validation Script

```bash
# Main validation - checks everything
./scripts/validate-provider.sh <provider>

# Examples:
./scripts/validate-provider.sh openai
./scripts/validate-provider.sh anthropic
```

**Checks performed:**
- ✅ Provider package installed (correct version)
- ✅ Core SDK (`ai`) installed
- ✅ .env file exists
- ✅ API key set with correct format
- ✅ .env in .gitignore (security)

### 3. Validate Model Name (if applicable)

```bash
./scripts/check-model-compatibility.sh <provider> <model>

# Examples:
./scripts/check-model-compatibility.sh openai gpt-4o
./scripts/check-model-compatibility.sh anthropic claude-sonnet-4-5-20250929
```

Shows valid models if name is wrong, suggests closest matches.

### 4. Generate Fixes

```bash
./scripts/generate-fix.sh <issue-type> <provider>

# Issue types:
# - missing-api-key      → Creates .env with correct format
# - wrong-format         → Shows valid key format
# - missing-package      → Installs provider package
# - model-compatibility  → Lists valid models
# - rate-limiting        → Adds retry helper with exponential backoff
# - import-error         → Fixes import statements
```

### 5. Test Connection

```bash
# Verify API credentials work
./scripts/test-provider-connection.sh <provider>
```

Makes real API call with minimal tokens to verify setup.

## Provider-Specific Info

**OpenAI:**
- Package: `@ai-sdk/openai`
- Env: `OPENAI_API_KEY`
- Format: `sk-proj-...` or `sk-...`
- Models: gpt-4o, gpt-4o-mini, gpt-4, gpt-3.5-turbo

**Anthropic:**
- Package: `@ai-sdk/anthropic`
- Env: `ANTHROPIC_API_KEY`
- Format: `sk-ant-api03-...`
- Models: claude-sonnet-4-5-20250929, claude-opus-4-20250514

**Google:**
- Package: `@ai-sdk/google`
- Env: `GOOGLE_GENERATIVE_AI_API_KEY`
- Format: `AIza...`
- Models: gemini-1.5-pro, gemini-1.5-flash

**xAI:**
- Package: `@ai-sdk/xai`
- Env: `XAI_API_KEY`
- Format: `xai-...`
- Models: grok-beta, grok-vision-beta

## Common Fixes

### Missing API Key
```bash
# Create .env with correct structure
./scripts/generate-fix.sh missing-api-key openai

# Then add actual key from provider dashboard
```

### Wrong Model Name
```bash
# Check valid models
./scripts/check-model-compatibility.sh anthropic claude-v3-opus
# Shows: Did you mean? → claude-opus-4-20250514
```

### Rate Limiting
```bash
# Generate retry helper
./scripts/generate-fix.sh rate-limiting openai
# Creates retryHelper.ts with exponential backoff
```

### Package Not Installed
```bash
# Install provider package
./scripts/generate-fix.sh missing-package anthropic
# Runs: npm install ai @ai-sdk/anthropic
```

## Resources

**Scripts:** All scripts in `scripts/` directory are executable and documented in README.md

**Templates:** `templates/` contains .env, .gitignore, and error-handler-template.ts

**Examples:** `examples/troubleshooting-guide.md` has detailed solutions for 10+ scenarios including CORS, streaming, TypeScript, and provider-specific issues

---

**Supported Providers:** OpenAI, Anthropic, Google, xAI, Groq, Mistral, Cohere, DeepSeek

**Version:** 1.0.0
**SDK Compatibility:** Vercel AI SDK 5+
