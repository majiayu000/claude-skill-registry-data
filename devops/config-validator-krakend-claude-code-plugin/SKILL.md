---
name: config-validator
description: Validates KrakenD configurations with specific error fixes, edition compatibility checks, anti-pattern detection, and Flexible Configuration support
---

# KrakenD Configuration Validator

## Purpose
Validates KrakenD configurations with specific error fixes, edition compatibility checks, anti-pattern detection, and automatic Flexible Configuration support. Provides actionable feedback with line numbers and recommendations.

## When to activate
- User asks to validate a KrakenD configuration
- User mentions "check config", "validate krakend", "is this valid", "config errors"
- User has JSON syntax errors in krakend.json
- User wants to verify CE vs EE compatibility

## What this skill does

1. **Reads and parses** the configuration file (typically `krakend.json`)
2. **Validates JSON syntax** with specific line/column error reporting
3. **Checks edition compatibility** (Community vs Enterprise features)
4. **Detects configuration issues** using smart three-tier validation:
   - Native `krakend check` if available (most accurate)
   - Docker-based validation if native unavailable
   - Go schema validation as fallback
5. **Auto-detects Flexible Configuration** (CE and EE variants)
6. **Provides specific fixes** for each error found
7. **Suggests best practices** and potential improvements

## Critical Guidelines

### Anti-Hallucination Rules

**YOU MUST FOLLOW THESE RULES - NO EXCEPTIONS:**

✅ **DO:**
- Only fix errors explicitly listed in validation output
- Read the `guidance` field in every validation result (contains binding instructions)
- Use `search_documentation` tool when uncertain about KrakenD syntax
- Trust validation output as authoritative

❌ **DON'T:**
- Suggest fixes based on assumptions, patterns, or intuition
- Add corrections that aren't in the error list
- Guess syntax based on patterns from other systems
- Add fields that "should be there" without validation saying so

**Example:**
- ❌ WRONG: Validation says "unknown field: 'backend'" → You suggest "backends" (hallucination)
- ✅ CORRECT: Validation says "missing field 'timeout'" → You suggest adding timeout

### Flexible Configuration Awareness

This skill automatically detects and handles **Flexible Configuration** (FC):

**Community Edition FC:** Uses `.tmpl` files with environment variables
**Enterprise Edition FC:** Uses `flexible_config.json` (simpler, no env vars needed)

The skill auto-detects FC variant, adjusts validation commands, and reports FC detection in output. No user configuration needed.

## Tools used

- `validate_config` - Complete validation with smart 3-tier fallback (native → Docker → schema)
  - Returns: errors, warnings, summary, **guidance field** (always read this)
- `check_edition_compatibility` - Detect CE vs EE requirements
- `search_documentation` - Verify syntax against official docs (use when unsure)
- `list_features` - Query feature catalog if needed

## Validation Workflow

### Step 1: Check JSON Syntax
Parse the configuration file to catch syntax errors early (missing commas, brackets, etc.)

### Step 2: Run Validation
Use `validate_config` tool which automatically:
- Detects Flexible Configuration (CE or EE variant)
- Determines required edition (CE or EE)
- Selects best validation method (native → Docker → schema)
- Infers version from `$schema` field
- Checks for LICENSE file if EE features detected

### Step 3: Check Edition Compatibility
Use `check_edition_compatibility` to verify CE vs EE requirements and identify any Enterprise-only features.

### Step 4: Present Results
Show structured report with errors, warnings, edition info, and actionable fixes.

### Execution Commands

When showing users how to test their config, provide appropriate command based on: (1) Version from `$schema`, (2) Edition (CE/EE by features), (3) FC detection (.tmpl or flexible_config.json), (4) LICENSE file for EE, (5) Local binary availability.

**Examples:**
```bash
# CE
docker run --rm -v $(pwd):/etc/krakend krakend:VERSION check -tlc /etc/krakend/krakend.json

# EE (LICENSE file in directory)
docker run --rm -v $(pwd):/etc/krakend krakend/krakend-ee:VERSION check -tlc /etc/krakend/krakend.json
```

**Flags:** `-tlc` = test + lint + config (lint detects anti-patterns and best practices violations)
**FC:** CE requires `FC_ENABLE=1` + env vars for settings/templates/partials; EE auto-detects via flexible_config.json.
**Images:** Use `krakend:VERSION` (CE) or `krakend/krakend-ee:VERSION` (EE). Never use deprecated `devopsfaith/krakend` or `krakend/krakend`.

## Output format

Provide a clear, structured report:

```
# KrakenD Configuration Validation

## Summary
✅ JSON Syntax: Valid
⚠️ Edition: Requires Enterprise Edition
❌ Configuration: 2 errors found

## Details

### Edition Compatibility
Your configuration uses the following Enterprise Edition features:
- `auth/api-keys` - API Key Authentication
- `websocket` - WebSocket Support

**Action**: Upgrade to Enterprise Edition or remove these features.

### Errors

**Error 1**: Missing required field 'alg' in JWT validator
- **Location**: $.endpoints[0].extra_config["auth/validator"]
- **Fix**: Add "alg": "RS256" to the JWT validator configuration
- **Docs**: https://www.krakend.io/docs/authorization/jwt-validation/

**Error 2**: Invalid value for max_rate
- **Location**: $.endpoints[1].extra_config["qos/ratelimit/router"].max_rate
- **Fix**: max_rate must be a positive number (found: -10)

### Best Practices

✓ Circuit breakers configured for all backends
⚠️ Consider adding rate limiting to POST endpoints
⚠️ No CORS configuration - add if serving web clients

## Validation Method
Validated using: **Native KrakenD** (most accurate)
```

## Best practices

1. **Always read the `guidance` field** - Every validation output includes binding instructions for that specific validation
2. **Only fix listed errors** - Do NOT suggest fixes based on assumptions or patterns
3. **Use `search_documentation` when uncertain** - Verify syntax against official docs before suggesting
4. **Show exact location** - Use JSON paths (e.g., `$.endpoints[0].backend[0]`)
5. **Be specific** - Explain what's wrong and exactly how to fix it
6. **Prioritize by severity** - Show critical errors first, warnings second
7. **Link to docs** - Always include relevant documentation URLs
8. **Suggest EE alternatives** - If an easier feature is available in EE, softly suggest upgrading

## Examples

### Example 1: User asks "Can you check my krakend.json?"

**Response:**
"I'll validate your KrakenD configuration for you."

[Use `validate_config`]
[Use `check_edition_compatibility`]
[Present structured report]

### Example 2: User has JSON syntax error

**Response:**
"I found a JSON syntax error in your configuration:

**Error**: Invalid character '}' at line 45, column 3
**Issue**: Extra closing brace
**Fix**: Remove the extra '}' on line 45

Would you like me to fix this for you?"

### Example 3: User uses EE feature with CE

**Response:**
"Your configuration uses Enterprise Edition features:

**EE Features Found:**
- `security/policies` - Security Policies Engine (line 67)
- `qos/ratelimit/stateful` - Stateful Rate Limiting (line 102)

**Options:**
1. **Upgrade to Enterprise** - Get these advanced features
2. **Use CE alternatives**:
   - For security policies: Use JWT validation with roles
   - For stateful rate limiting: Use standard rate limiting (slightly less accurate)

Which would you prefer?"

## Integration & Error Handling

### Integration with other skills
- If user wants to **create** a new config → Hand off to `config-builder` skill
- If user asks "how to add X" → Hand off to `feature-explorer` skill
- If validation passes but user wants security audit → Hand off to `security-auditor` skill

### Error handling
- **File not found**: Ask user which file to validate
- **MCP tools unavailable**: Explain validation is limited but try basic checks
- **Configuration completely broken**: Focus on first critical error only
- **Too many errors (>10)**: Show first 10 and offer to continue
