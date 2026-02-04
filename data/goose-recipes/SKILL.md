---
name: goose-recipes
description: Create, validate, and work with Goose recipes - reusable AI agent configurations that package specific setups for tasks. Use when creating recipe.yaml/recipe.json files, configuring Goose extensions, parameters, retry logic, structured outputs, or debugging recipe validation errors.
---

# Goose Recipes Skill

Create and work with Goose recipes - reusable configurations that package up specific AI agent setups.

## Quick Start

### Create a Basic Recipe

Start with the basic template from `assets/basic-recipe-template.yaml` and customize:

```yaml
version: "1.0.0"
title: "Your Recipe Title"
description: "What this recipe accomplishes"
prompt: "Initial task for the agent"
```

### Create an Advanced Recipe

For complex workflows, use `assets/advanced-recipe-template.yaml` which includes:
- Retry logic with success validation
- Structured JSON output
- Subrecipes and extensions
- File input parameters

## Core Recipe Creation Workflow

### 1. Define Required Fields

Every recipe MUST have:
- `version`: Use "1.0.0"
- `title`: Short, descriptive title
- `description`: Detailed explanation of purpose

### 2. Add Instructions or Prompt

Choose based on use case:
- `instructions`: Multi-step guidance for complex tasks
- `prompt`: Direct task statement for simple tasks
- Both: Instructions provide context, prompt initiates action

### 3. Configure Parameters

Define inputs with proper requirements:

```yaml
parameters:
  - key: param_name
    input_type: string  # or "file" to read file contents
    requirement: required  # or "optional" or "user_prompt"
    description: "What this parameter does"
    default: "value"  # Required for optional parameters
```

Use parameters in templates: `{{ param_name }}`

### 4. Add Extensions (if needed)

Include MCP servers or tools:

```yaml
extensions:
  - type: stdio
    name: extension_name
    cmd: command_to_run
    args: [arguments]
    timeout: 300
    description: "What this extension provides"
```

### 5. Configure Retry Logic (optional)

Enable automatic retries with validation:

```yaml
retry:
  max_retries: 3
  checks:
    - type: shell
      command: "test -f output.json"  # Must exit 0 for success
  on_failure: "rm -f output.json"  # Cleanup command
```

### 6. Define Structured Output (optional)

Enforce JSON response format:

```yaml
response:
  json_schema:
    type: object
    properties:
      result:
        type: string
        description: "Main result"
    required: [result]
```

## Common Patterns

### File Input Processing

Read and process file contents:

```yaml
parameters:
  - key: source_code
    input_type: file
    requirement: required
    description: "Source code file to analyze"

prompt: "Analyze this code:\n{{ source_code }}"
```

### Multi-Step Workflows

Use instructions for complex procedures:

```yaml
instructions: |
  1. Parse the input data
  2. Validate against schema
  3. Generate report with findings
  4. Save to specified location

prompt: "Begin processing {{ input_file }}"
```

### Subrecipe Composition

Combine multiple recipes:

```yaml
sub_recipes:
  - name: "validate"
    path: "./validation.yaml"
    values:
      strict_mode: "true"
```

### Environment Variables

Recipes can use environment-based secrets:

```yaml
extensions:
  - type: stdio
    name: github-mcp
    cmd: github-mcp-server
    env_keys: [GITHUB_PERSONAL_ACCESS_TOKEN]
```

### MCP Server Access with Authentication

**IMPORTANT**: When working with HTTP-based MCP servers that require authentication (Bearer tokens, API keys), do NOT use `sse` or `streamable_http` extension types - they don't properly support custom authentication headers in Goose recipes.

Instead, use this pattern:

```yaml
parameters:
  - key: API_KEY
    input_type: string
    requirement: optional
    description: "API key for MCP server authentication"
    default: "your-api-key"

instructions: |
  **MCP Server Access**
  The MCP server is available at: https://your-server.example.com/mcp
  Authentication: Use Bearer token with API key: {{ API_KEY }}

  The server provides tools for:
  - tool_name_1: Description
  - tool_name_2: Description

  Access these tools by making HTTP requests with the Authorization header.
```

This approach:
1. Passes authentication credentials as parameters
2. Documents the MCP server URL and available tools in instructions
3. Guides the agent to make authenticated HTTP calls directly
4. Avoids extension configuration issues with custom headers

## Validation and Testing

### Run Recipe Validation

Recipes are validated for:
- Required fields presence
- Parameter-template matching
- Optional parameters have defaults
- Valid YAML/JSON syntax
- Extension configuration validity

### Debug Common Issues

| Issue | Solution |
|-------|----------|
| "Template variable without parameter" | Add parameter definition for `{{ variable }}` |
| "Optional parameter without default" | Add `default: "value"` to parameter |
| "Invalid YAML syntax" | Check indentation and quotes |
| "Shell command failed" | Test command separately, ensure proper escaping |

## Template Features

### Parameter Substitution
- Basic: `{{ parameter_name }}`
- With filter: `{{ content | indent(2) }}`

### Template Inheritance
```yaml
{% extends "parent.yaml" %}
{% block content %}Modified content{% endblock %}
```

### Built-in Parameters
- `recipe_dir`: Directory containing the recipe file

## File Organization

### CLI vs Desktop Formats

**CLI Format** (root-level fields):
```yaml
version: "1.0.0"
title: "Recipe"
description: "Description"
```

**Desktop Format** (nested in recipe object):
```yaml
name: "Recipe Name"
recipe:
  version: "1.0.0"
  title: "Recipe"
  description: "Description"
```

Both formats work with `goose run --recipe` command.

## Reference Documentation

For complete field reference and advanced configurations, see:
- `references/recipe-structure.md` - Complete field reference and configuration options

## Recipe Templates

Ready-to-use templates in `assets/`:
- `basic-recipe-template.yaml` - Simple recipe structure
- `advanced-recipe-template.yaml` - Complex features showcase
- `mcp-server-recipe-template.yaml` - HTTP-based MCP servers with authentication
