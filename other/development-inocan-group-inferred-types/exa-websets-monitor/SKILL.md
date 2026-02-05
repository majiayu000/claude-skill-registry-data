---
name: exa-websets-monitor
description: Use when setting up monitors - periodic searches to add new items or refresh existing items in a webset automatically.
---

# Exa Websets Monitor

Automate webset updates on a schedule using monitors.

**Use `--help` to see available commands and verify usage before running:**
```bash
exa-ai <command> --help
```

## Working with Complex Shell Commands

When using the Bash tool with complex shell syntax, follow these best practices for reliability:

1. **Run commands directly**: Capture JSON output directly rather than nesting command substitutions
2. **Parse in subsequent steps**: Use `jq` to parse output in a follow-up command if needed
3. **Avoid nested substitutions**: Complex nested `$(...)` can be fragile; break into sequential steps

Example:
```bash
# Less reliable: nested command substitution
monitor_id=$(exa-ai monitor-create ws_abc123 --cron "0 9 * * *" --behavior-type search | jq -r '.monitor_id')

# More reliable: run directly, then parse
exa-ai monitor-create ws_abc123 --cron "0 9 * * *" --behavior-type search
# Then in a follow-up command if needed:
monitor_id=$(cat output.json | jq -r '.monitor_id')
```

## Critical Requirements

**MUST follow these rules when using monitors:**

1. **Use separate monitors for search and refresh**: Create one monitor for adding new items and another for refreshing existing ones
2. **Schedule refreshes during off-peak hours**: Run refresh monitors at night to avoid rate limits
3. **Set appropriate timezones**: Use your local timezone for business-hour schedules

## Monitor Behavior Types

- **search**: Run search periodically to add/update items
- **refresh**: Refresh existing items periodically

## Output Formats

All exa-ai monitor commands support output formats:
- **JSON (default)**: Pipe to `jq` to extract specific fields (e.g., `| jq -r '.monitor_id'`)
- **toon**: Compact, readable format for direct viewing
- **pretty**: Human-friendly formatted output
- **text**: Plain text output

## Quick Start

### Create Search Monitor

```bash
# Daily search for new items
exa-ai monitor-create ws_abc123 \
  --cron "0 9 * * *" \
  --timezone "America/New_York" \
  --behavior-type search \
  --query "new AI startups" \
  --count 5
```

### Create Refresh Monitor

```bash
# Nightly refresh of existing items
exa-ai monitor-create ws_abc123 \
  --cron "0 2 * * *" \
  --timezone "America/New_York" \
  --behavior-type refresh
```

### Common Cron Patterns

```bash
"0 0 * * *"       # Daily at midnight
"0 9 * * 1"       # Weekly on Monday at 9 AM
"0 */6 * * *"     # Every 6 hours
"0 0 1 * *"       # Monthly on the 1st at midnight
"0 12 * * 1-5"    # Weekdays at noon
```

### Manage Monitors

```bash
# List all monitors
exa-ai monitor-list

# Get monitor details
exa-ai monitor-get mon_xyz789

# View execution history
exa-ai monitor-runs-list mon_xyz789
```

## Example Workflow

```bash
# 1. Create webset
webset_id=$(exa-ai webset-create \
  --search '{"query":"AI startups","count":50}' | jq -r '.webset_id')

# 2. Set up daily search monitor
monitor_id=$(exa-ai monitor-create $webset_id \
  --cron "0 9 * * *" \
  --timezone "America/New_York" \
  --behavior-type search \
  --query "new AI startups" \
  --behavior-mode append \
  --count 10 | jq -r '.monitor_id')

# 3. Set up nightly refresh
exa-ai monitor-create $webset_id \
  --cron "0 2 * * *" \
  --timezone "America/New_York" \
  --behavior-type refresh

# 4. Check execution history
exa-ai monitor-runs-list $monitor_id
```

## Best Practices

1. **Use separate monitors for search and refresh**: Create one monitor for adding new items and another for refreshing existing ones
2. **Schedule refreshes during off-peak hours**: Run refresh monitors at night to avoid rate limits
3. **Use append mode for continuous growth**: Only use override when you want to completely replace the collection
3. **Set appropriate timezones**: Use your local timezone for business-hour schedules
5. **Monitor execution history**: Check runs regularly to ensure monitors are working as expected
6. **Start with conservative schedules**: Begin with daily or weekly runs, then increase frequency if needed

## Detailed Reference

For complete options, examples, and cron patterns, consult [REFERENCE.md](REFERENCE.md).

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
