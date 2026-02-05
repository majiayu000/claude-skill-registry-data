---
name: exa-context
description: Get code context from repositories with examples and documentation. Use when you need code snippets, implementation examples, API usage patterns, or technical documentation for programming concepts, frameworks, or libraries.
---

# Exa Context

Token-efficient strategies for retrieving code context using exa-ai.

**Use `--help` to see available commands and verify usage before running:**
```bash
exa-ai <command> --help
```

## Critical Requirements

**MUST follow these rules when using exa-ai context:**

### Shared Requirements

This skill inherits requirements from [Common Requirements](../../../docs/common-requirements.md):
- Output format selection → All output operations

### MUST Rules

1. **Use dynamic tokens**: Default `--tokens-num dynamic` adapts to content; specify exact number only when needed

### SHOULD Rules

1. **Prefer text format**: Use `--output-format text` for direct use in prompts or documentation (removes JSON wrapper overhead)

## Cost Optimization

### Pricing
- **1-25 results**: $0.005 per search
- **26-100 results**: $0.025 per search (5x more expensive)

**Cost strategy:**
1. **Default to 1-25 results**: 5x cheaper, sufficient for most queries
2. **Need 50+ results? Run multiple targeted searches**: Two 25-result searches with different angles beats one 50-result search (better quality, more control)
3. **Use 26-100 results sparingly**: Only when you need comprehensive coverage that multiple targeted searches would miss

## Token Optimization

**Apply these strategies:**

- **Use toon format**: `--output-format toon` for 40% fewer tokens than JSON (use when reading output directly)
- **Use text format**: `--output-format text` to get raw context without JSON wrapper (ideal for piping to other commands)
- **Use JSON + jq**: Extract only the context field with jq when processing programmatically
- **Set token limits**: Use `--tokens-num N` to control response size

**IMPORTANT**: Choose one approach, don't mix them:
- **Approach 1: text format** - Raw context output for direct use (no JSON wrapper)
- **Approach 2: toon format** - Compact YAML-like output for direct reading
- **Approach 3: JSON + jq** - Extract context field programmatically

Examples:
```bash
# ❌ High token usage - full JSON wrapper
exa-ai context "React hooks"

# ✅ Approach 1: text format for direct use (removes JSON overhead)
exa-ai context "React hooks" --output-format text

# ✅ Approach 2: toon format for reading (40% reduction)
exa-ai context "React hooks" --output-format toon

# ✅ Approach 3: JSON + jq to extract context only
exa-ai context "React hooks" | jq -r '.context'
```

## Quick Start

### Basic Context Retrieval
```bash
exa-ai context "React hooks useState useEffect" --output-format toon
```

### Specific Token Limit
```bash
exa-ai context "Python async/await patterns" --tokens-num 5000
```

### Authentication Patterns
```bash
exa-ai context "JWT authentication with Ruby on Rails" \
  --tokens-num 3000 \
  --output-format text
```

### Extract Context for Direct Use
```bash
exa-ai context "GraphQL schema design best practices" \
  --tokens-num 4000 | jq -r '.context'
```

## Detailed Reference

For complete options, examples, and advanced usage, consult [REFERENCE.md](REFERENCE.md).

### Shared Requirements

<shared-requirements>

## Schema Design

### MUST: Use object wrapper for schemas

**Applies to**: answer, search, find-similar, get-contents

When using schema parameters (`--output-schema` or `--summary-schema`), always wrap properties in an object:

```json
{"type":"object","properties":{"field_name":{"type":"string"}}}
```

**DO NOT** use bare properties without the object wrapper:
```json
{"properties":{"field_name":{"type":"string"}}}  // ❌ Missing "type":"object"
```

**Why**: The Exa API requires a valid JSON Schema with an object type at the root level. Omitting this causes validation errors.

**Examples**:
```bash
# ✅ CORRECT - object wrapper included
exa-ai search "AI news" \
  --summary-schema '{"type":"object","properties":{"headline":{"type":"string"}}}'

# ❌ WRONG - missing object wrapper
exa-ai search "AI news" \
  --summary-schema '{"properties":{"headline":{"type":"string"}}}'
```

---

## Output Format Selection

### MUST NOT: Mix toon format with jq

**Applies to**: answer, context, search, find-similar, get-contents

`toon` format produces YAML-like output, not JSON. DO NOT pipe toon output to jq for parsing:

```bash
# ❌ WRONG - toon is not JSON
exa-ai search "query" --output-format toon | jq -r '.results'

# ✅ CORRECT - use JSON (default) with jq
exa-ai search "query" | jq -r '.results[].title'

# ✅ CORRECT - use toon for direct reading only
exa-ai search "query" --output-format toon
```

**Why**: jq expects valid JSON input. toon format is designed for human readability and produces YAML-like output that jq cannot parse.

### SHOULD: Choose one output approach

**Applies to**: answer, context, search, find-similar, get-contents

Pick one strategy and stick with it throughout your workflow:

1. **Approach 1: toon only** - Compact YAML-like output for direct reading
   - Use when: Reading output directly, no further processing needed
   - Token savings: ~40% reduction vs JSON
   - Example: `exa-ai search "query" --output-format toon`

2. **Approach 2: JSON + jq** - Extract specific fields programmatically
   - Use when: Need to extract specific fields or pipe to other commands
   - Token savings: ~80-90% reduction (extracts only needed fields)
   - Example: `exa-ai search "query" | jq -r '.results[].title'`

3. **Approach 3: Schemas + jq** - Structured data extraction with validation
   - Use when: Need consistent structured output across multiple queries
   - Token savings: ~85% reduction + consistent schema
   - Example: `exa-ai search "query" --summary-schema '{...}' | jq -r '.results[].summary | fromjson'`

**Why**: Mixing approaches increases complexity and token usage. Choosing one approach optimizes for your use case.

---

## Shell Command Best Practices

### MUST: Run commands directly, parse separately

**Applies to**: monitor, search (websets), research, and all skills using complex commands

When using the Bash tool with complex shell syntax, run commands directly and parse output in separate steps:

```bash
# ❌ WRONG - nested command substitution
webset_id=$(exa-ai webset-create --search '{"query":"..."}' | jq -r '.webset_id')

# ✅ CORRECT - run directly, then parse
exa-ai webset-create --search '{"query":"..."}'
# Then in a follow-up command:
webset_id=$(cat output.json | jq -r '.webset_id')
```

**Why**: Complex nested `$(...)` command substitutions can fail unpredictably in shell environments. Running commands directly and parsing separately improves reliability and makes debugging easier.

### MUST NOT: Use nested command substitutions

**Applies to**: All skills when using complex multi-step operations

Avoid nesting multiple levels of command substitution:

```bash
# ❌ WRONG - deeply nested
result=$(exa-ai search "$(cat query.txt | tr '\n' ' ')" --num-results $(cat config.json | jq -r '.count'))

# ✅ CORRECT - sequential steps
query=$(cat query.txt | tr '\n' ' ')
count=$(cat config.json | jq -r '.count')
exa-ai search "$query" --num-results $count
```

**Why**: Nested command substitutions are fragile and hard to debug when they fail. Sequential steps make each operation explicit and easier to troubleshoot.

### SHOULD: Break complex commands into sequential steps

**Applies to**: All skills when working with multi-step workflows

For readability and reliability, break complex operations into clear sequential steps:

```bash
# ❌ Less maintainable - everything in one line
exa-ai webset-create --search '{"query":"startups","count":1}' | jq -r '.webset_id' | xargs -I {} exa-ai webset-search-create {} --query "AI" --behavior override

# ✅ More maintainable - clear steps
exa-ai webset-create --search '{"query":"startups","count":1}'
webset_id=$(jq -r '.webset_id' < output.json)
exa-ai webset-search-create $webset_id --query "AI" --behavior override
```

**Why**: Sequential steps are easier to understand, debug, and modify. Each step can be verified independently.

</shared-requirements>
