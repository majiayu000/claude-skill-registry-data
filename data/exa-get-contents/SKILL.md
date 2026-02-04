---
name: exa-get-contents
description: Retrieve and extract content from URLs with AI-powered summarization and structured data extraction. Use for scraping web pages, extracting specific information, summarizing articles, or crawling websites with subpages.
---

# Exa Get Contents

Token-efficient strategies for retrieving and extracting content from URLs using exa-ai.

**Use `--help` to see available commands and verify usage before running:**
```bash
exa-ai <command> --help
```

## Critical Requirements

**MUST follow these rules when using exa-ai get-contents:**

### Shared Requirements

This skill inherits requirements from [Common Requirements](../../../docs/common-requirements.md):
- Schema design patterns → All schema operations
- Output format selection → All output operations

### MUST Rules

1. **Always use livecrawl**: Include `--livecrawl-timeout 10000` for fresh, up-to-date content instead of cached results

### SHOULD Rules

1. **Prefer --summary over --text**: Use summaries with schemas for structured extraction instead of full text for better token efficiency

## Cost Optimization

### Pricing
- **Per piece of content**: $0.001

Each URL counts as one piece of content. Multiple URLs increase cost linearly.

**Cost strategy:**
- Only fetch URLs you need
- Use `--summary` instead of `--text` to reduce processing (and token costs)
- Combine with search results to target specific URLs rather than crawling broadly

## Token Optimization

**Apply these strategies:**

- **Use toon format**: `--output-format toon` for 40% fewer tokens than JSON (use when reading output directly)
- **Use JSON + jq**: Extract only needed fields with jq (use when piping/processing output)
- **Use --summary**: Get AI-generated summaries instead of full page text
- **Use schemas**: Extract structured data with `--summary-schema` (always pipe to jq)
- **Limit extraction**: Use `--text-max-characters`, `--links`, and `--image-links` to control output size

**IMPORTANT**: Choose one approach, don't mix them:
- **Approach 1: toon only** - Compact YAML-like output for direct reading
- **Approach 2: JSON + jq** - Extract specific fields programmatically
- **Approach 3: Schemas + jq** - Get structured data, always use JSON output (default) and pipe to jq

Examples:
```bash
# ❌ High token usage - full text
exa-ai get-contents "https://example.com" --text --livecrawl-timeout 10000

# ✅ Approach 1: toon format with summary (70% reduction)
exa-ai get-contents "https://example.com" --summary --livecrawl-timeout 10000 --output-format toon

# ✅ Approach 2: JSON + jq for summary extraction (80% reduction)
exa-ai get-contents "https://example.com" --summary --livecrawl-timeout 10000 | jq '.results[].summary'

# ✅ Approach 3: Schema + jq for structured extraction (85% reduction)
exa-ai get-contents "https://example.com" \
  --summary \
  --livecrawl-timeout 10000 \
  --summary-schema '{"type":"object","properties":{"key_info":{"type":"string"}}}' | \
  jq -r '.results[].summary | fromjson | .key_info'

# ❌ Don't mix toon with jq (toon is YAML-like, not JSON)
exa-ai get-contents "https://example.com" --output-format toon | jq -r '.results'
```

## Quick Start

### Basic Content with Summary
```bash
exa-ai get-contents "https://anthropic.com" --summary --livecrawl-timeout 10000 --output-format toon
```

### Custom Summary Query
```bash
exa-ai get-contents "https://techcrunch.com" \
  --summary \
  --livecrawl-timeout 10000 \
  --summary-query "What are the main tech news stories on this page?" | jq '.results[].summary'
```

### Structured Data Extraction
```bash
exa-ai get-contents "https://www.stripe.com" \
  --summary \
  --livecrawl-timeout 10000 \
  --summary-schema '{"type":"object","properties":{"company_name":{"type":"string"},"main_product":{"type":"string"},"target_market":{"type":"string"}}}' | jq -r '.results[].summary | fromjson'
```

### Multiple URLs
```bash
exa-ai get-contents "https://anthropic.com,https://openai.com,https://cohere.com" \
  --summary \
  --livecrawl-timeout 10000 \
  --output-format toon
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
