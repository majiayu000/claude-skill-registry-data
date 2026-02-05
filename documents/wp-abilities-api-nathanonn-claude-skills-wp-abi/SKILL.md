---
name: wp-abilities-api
description: Intelligent documentation system for the WordPress Abilities API. Activate automatically when working with WordPress plugins, ability registration, or when WordPress Abilities API terms are mentioned (wp_register_ability, ability categories, REST API, etc.). Provides context-aware documentation retrieval - fetches implementation guides for coding queries, API references for parameter lookups, and smart multi-page fetching for complex integrations.
---

# WordPress Abilities API Documentation

## Overview

Provide intelligent documentation retrieval for the WordPress Abilities API when building WordPress plugins and applications. The WordPress Abilities API provides a standardized framework for registering, discovering, and executing discrete units of functionality (abilities) in WordPress, with built-in support for REST API exposure, JavaScript client integration, permissions, validation, and extensibility.

This skill automatically fetches relevant documentation from bundled markdown files and provides context-aware routing to ensure users get the right information format for their query.

## Activation

### Automatically Activate When:

1. **WordPress Abilities API Functions Mentioned:**
   - Registration: wp_register_ability, wp_register_ability_category
   - Retrieval: wp_get_ability, wp_get_abilities, wp_get_ability_category, wp_get_ability_categories
   - Execution: execute, execute_callback, check_permissions
   - Validation: wp_has_ability, input_schema, output_schema

2. **WordPress Abilities API Terms:**
   - "Abilities API", "WordPress Abilities", "WP Abilities"
   - "ability registration", "ability categories"
   - "@wordpress/abilities" (JavaScript package)
   - "wp-abilities/v1" (REST API namespace)
   - Ability-related classes, callbacks, schemas

3. **File Context Detection:**
   - Files with wp_register_ability or wp_register_ability_category calls
   - Imports from @wordpress/abilities
   - REST API calls to /wp-abilities/v1/
   - WordPress plugin files mentioning abilities

4. **Implementation Queries:**
   - Building WordPress plugins with abilities
   - Registering custom abilities or categories
   - Creating JavaScript clients for abilities
   - Implementing permission callbacks or validation
   - Exposing abilities via REST API

### Do NOT Activate For:

- Generic WordPress plugin development without abilities context
- Other WordPress APIs (REST API, Settings API, etc.) unless specifically abilities-related
- Generic JavaScript/REST API discussions without WordPress Abilities context
- WordPress hooks unless specifically ability action/filter hooks

## Core Capabilities

### 1. Context-Aware Documentation Routing

Route queries intelligently based on intent to provide the most useful documentation format:

#### Route 1: Implementation Queries → Getting Started + Relevant API

**Triggers:**
- "how to...", "how do I...", "how can I..."
- "build a...", "create a...", "implement..."
- "register an ability", "execute an ability"
- "example of...", "show me how..."

**Action:**
1. Identify the relevant API area from INDEX.md
2. Read getting-started guide: `references/getting-started/[guide].md`
3. Read related API documentation: `references/[api-type]/[topic].md`
4. Include overview context if needed: `references/overview/intro.md`
5. Present with implementation pattern and code examples

**Example Query:** "How do I register an ability with input validation?"
**Fetch:**
- `references/getting-started/basic-usage.md`
- `references/php-api/registering-abilities.md`
- `references/php-api/error-handling.md`

#### Route 2: API Reference Queries → Specific API Documentation

**Triggers:**
- "what is...", "what does... do"
- "what parameters...", "what arguments..."
- "how does... work"
- "wp_register_ability parameters", "ability schema..."

**Action:**
1. Look up function/feature in INDEX.md
2. Read single API documentation file: `references/[api-type]/[topic].md`
3. Suggest 2-3 related functions/features from same category

**Example Query:** "What parameters does wp_register_ability accept?"
**Fetch:**
- `references/php-api/registering-abilities.md`
**Suggest:** Using abilities, Categories, Error handling (same category)

#### Route 3: Getting Started Queries → Installation + Basic Usage

**Triggers:**
- "getting started with Abilities API"
- "how to install...", "setup..."
- "first ability", "quick start..."
- "new to Abilities API"

**Action:**
1. Read getting started documentation:
   - `references/getting-started/installation.md`
   - `references/getting-started/basic-usage.md`
2. Optionally read `references/overview/intro.md` for context

**Example Query:** "I'm new to the Abilities API, how do I get started?"
**Fetch:**
- `references/getting-started/installation.md`
- `references/getting-started/basic-usage.md`
- `references/overview/intro.md`

#### Route 4: Category/API Type Queries → README + Specific Docs

**Triggers:**
- "PHP functions for abilities"
- "JavaScript client methods"
- "REST API endpoints"
- "what hooks are available"
- "show me all... functions"

**Action:**
1. Read `references/README.md` (contains categorized function/endpoint lists)
2. Read 1-2 key documentation files in that category
3. List all relevant functions/endpoints with brief descriptions from INDEX.md

**Example Query:** "What JavaScript functions are available for abilities?"
**Fetch:**
- `references/README.md`
- `references/javascript-client/overview.md`
- `references/javascript-client/abilities.md`

#### Route 5: Integration Queries → Multiple API Types

**Triggers:**
- "use abilities from JavaScript"
- "REST API and PHP together"
- "client-side and server-side"
- "integrate with..."

**Action:**
1. Identify relevant API types (PHP, JavaScript, REST)
2. Read overview for each type
3. Read specific implementation guides
4. Show integration pattern

**Example Query:** "How do I register a PHP ability and execute it from JavaScript?"
**Fetch:**
- `references/php-api/registering-abilities.md`
- `references/javascript-client/abilities.md`
- `references/rest-api/execution.md`

#### Route 6: Troubleshooting Queries → Error Handling + Relevant Feature

**Triggers:**
- "error...", "not working...", "failing..."
- "WP_Error...", "validation error..."
- "permission denied", "ability not found"
- "troubleshoot...", "debug..."

**Action:**
1. Read error handling documentation for relevant API
2. Read specific feature documentation if applicable
3. Reference hooks if extensibility needed

**Example Query:** "Why am I getting a permission denied error?"
**Fetch:**
- `references/php-api/error-handling.md`
- `references/php-api/using-abilities.md`
- `references/rest-api/execution.md`

### 2. Smart Multi-Page Fetching

**Fetch Multiple Pages (2-4 total) When:**
- Implementation queries requiring multiple concepts
- Query mentions multiple APIs (e.g., "PHP and JavaScript")
- Complex workflows (e.g., "register, validate, and execute")
- Related feature sets (registration + execution, categories + abilities)

**Fetch Single Page When:**
- Simple reference queries
- Troubleshooting lookups
- Single function explanations
- Hook documentation

**Stop Fetching When:**
- Already fetched 3-4 pages
- Query is answered sufficiently
- Additional pages would be tangential

### 3. Category-Aware Suggestions

After fetching documentation, always suggest 2-3 related topics using these category groupings:

**Overview:**
- Introduction, Core concepts, Goals and benefits, Use cases

**Getting Started:**
- Installation, Basic usage, First ability

**PHP API:**
- Categories (register, unregister, retrieve)
- Registering Abilities (wp_register_ability, parameters, conventions)
- Using Abilities (retrieve, execute, check permissions, inspect)
- Error Handling (WP_Error, validation, permissions)

**JavaScript Client:**
- Overview
- Working with Abilities (getAbilities, getAbility, executeAbility)
- Working with Categories (getAbilityCategories, getAbilityCategory)
- Registration (registerAbility, client-side abilities)
- Error Handling (JavaScript errors, error codes)

**REST API:**
- Overview (authentication, schema, show_in_rest)
- Abilities Endpoints (list, retrieve)
- Categories Endpoints (list, retrieve)
- Execution (run endpoint, HTTP methods, errors)

**Hooks:**
- Action Hooks (init, before/after execute)
- Filter Hooks (modify registration args)

**Common Feature Pairings:**
- wp_register_ability → Using abilities, Categories, Error handling
- Execute → Permissions, Error handling, REST execution
- Categories → Registering abilities, Organization
- JavaScript client → REST API, PHP registration
- Input/output schema → Validation, Error handling
- Permissions → Error handling, REST API authentication
- Hooks → Extensibility, Custom behavior

Suggest topics from:
1. Same category (highest priority)
2. Commonly used together
3. Prerequisites or next steps

### 4. Code Example Generation

Always include relevant code examples in responses:

**PHP Registration:**
```php
wp_register_ability( 'my-plugin/get-site-info', array(
    'label'             => 'Get Site Information',
    'description'       => 'Returns basic site information',
    'category'          => 'my-plugin-site-management',  // Dashes only
    'execute_callback'  => function( $input ) {
        return array(
            'name' => get_bloginfo( 'name' ),
            'url'  => get_site_url(),
        );
    },
    'permission_callback' => function() {
        return current_user_can( 'manage_options' );
    },
    'meta' => array(
        'show_in_rest' => true,      // Inside meta array
        'mcp'          => array(
            'public' => true,        // Required for MCP discovery
            'type'   => 'tool',
        ),
    ),
) );
```

**JavaScript Execution:**
```javascript
import { executeAbility } from '@wordpress/abilities';

const result = await executeAbility( 'my-plugin/get-site-info', {
    // input parameters
} );
```

**REST API Call:**
```bash
GET /wp-json/wp-abilities/v1/my-plugin/get-site-info/run
```

**Prerequisites:**
- WordPress 5.0 or later
- PHP 7.4 or later
- Abilities API plugin installed and activated
- Check `references/getting-started/installation.md` for setup

## Response Formats

### Single-Page Response Format

```markdown
I've fetched the [Topic Name] documentation from the WordPress Abilities API.

**Quick Setup:**
[Include installation/setup if relevant to query]

[Full documentation content from file]

---

**Related Topics:**
- **[Topic 1]** - [Brief description of relationship]
- **[Topic 2]** - [Brief description of relationship]
- **[Topic 3]** - [Brief description of relationship]

**Code Example:**
[Include relevant code snippet if applicable]
```

### Multi-Page Response Format

```markdown
This requires understanding multiple aspects of the Abilities API. I've fetched:

---

## [Topic 1 Name]

**Quick Setup:**
[Include setup code if relevant]

[Full content from file]

---

## [Topic 2 Name]

[Full content from file]

---

## [Topic 3 Name] (if needed)

[Full content from file]

---

**Integration Pattern:**
[2-3 sentences explaining how these concepts work together, referencing examples from the documentation]

**Related Topics:**
- **[Additional Topic]** - [Description]
- **[Tutorial/Guide]** - [Description]

**Complete Example:**
[Include comprehensive code example showing integration]
```

## Implementation Guidance Scope

### ✅ DO Provide:

1. **Code Examples from Documentation**
   - Show registration patterns from the docs
   - Reference execution examples
   - Demonstrate permission callbacks

2. **Feature Integration Patterns**
   - "Categories help organize related abilities"
   - "Use input_schema for automatic validation"
   - "Set show_in_rest: true inside meta array to expose via REST API"
   - "Add mcp.public: true for AI assistant discoverability"
   - "Check external plugin availability with class_exists()"

3. **Best Practices from Docs**
   - "Follow namespace conventions: plugin-name/ability-name for abilities, plugin-name-category for categories"
   - "Always implement permission_callback for security"
   - "Use WP_Error for error handling with appropriate status codes"
   - "Place show_in_rest and mcp settings inside meta array, not top-level"
   - "Category slugs must use dashes only, never slashes"

4. **Setup and Configuration**
   - Plugin installation methods
   - Availability checking
   - Hook timing (when to register)

5. **Common Patterns**
   - Registration during init hooks
   - Error handling with WP_Error
   - Schema validation with JSON Schema
   - Permission checking patterns

6. **API Integration Guidance**
   - PHP to JavaScript integration
   - REST API authentication
   - Client-side vs server-side execution

### ❌ DON'T Provide:

1. **Custom Implementations Beyond Docs** - Only show documented patterns
2. **Undocumented Features** - Stick to documented capabilities only
3. **Complex Plugin Development** - Focus on Abilities API usage
4. **Debugging Complex User Code** - Can reference error handling docs only
5. **WordPress Core Development** - Only Abilities API specific features

## Documentation Access

### File Structure

All documentation is bundled in the skill at:
```
.claude/skills/wp-abilities-api/
├── SKILL.md (this file)
└── references/
    ├── INDEX.md (searchable keyword reference)
    ├── README.md (overview and quick reference)
    ├── overview/
    │   └── intro.md
    ├── getting-started/
    │   ├── installation.md
    │   └── basic-usage.md
    ├── php-api/
    │   ├── categories.md
    │   ├── registering-abilities.md
    │   ├── using-abilities.md
    │   └── error-handling.md
    ├── javascript-client/
    │   ├── overview.md
    │   ├── abilities.md
    │   ├── categories.md
    │   ├── registration.md
    │   └── error-handling.md
    ├── rest-api/
    │   ├── overview.md
    │   ├── abilities-endpoints.md
    │   ├── categories-endpoints.md
    │   └── execution.md
    └── hooks/
        ├── actions.md
        └── filters.md
```

### How to Access Documentation

1. **Search INDEX.md** for function names, keywords, or categories
2. **Read files** using the Read tool with absolute paths:
   - PHP API: `.claude/skills/wp-abilities-api/references/php-api/[topic].md`
   - JavaScript: `.claude/skills/wp-abilities-api/references/javascript-client/[topic].md`
   - REST API: `.claude/skills/wp-abilities-api/references/rest-api/[topic].md`
   - Getting Started: `.claude/skills/wp-abilities-api/references/getting-started/[topic].md`
   - Hooks: `.claude/skills/wp-abilities-api/references/hooks/[type].md`
3. **Extract metadata** from INDEX.md entries (keywords, categories)
4. **Generate suggestions** using category groupings and common pairings

## Query Interpretation Examples

### Example 1: Implementation Query

**Query:** "How do I register an ability with input validation?"

**Routing:** Implementation query → Getting Started + PHP API

**Process:**
1. Search INDEX.md for "register", "validation", "input_schema"
2. Read `references/getting-started/basic-usage.md`
3. Read `references/php-api/registering-abilities.md`
4. Include schema example

**Response includes:**
- Basic registration pattern
- input_schema parameter with JSON Schema
- Validation error handling
- Related: Error handling, Using abilities

### Example 2: API Reference Query

**Query:** "What parameters does wp_register_ability accept?"

**Routing:** API reference query → PHP API only

**Process:**
1. Look up "wp_register_ability" in INDEX.md
2. Read `references/php-api/registering-abilities.md`
3. Find related: Using abilities, Categories, Error handling

**Response includes:**
- Complete parameter list and descriptions
- Code examples
- Naming conventions
- Suggestions: Using abilities, Categories, Error handling

### Example 3: Getting Started Query

**Query:** "I'm new to the Abilities API, how do I get started?"

**Routing:** General guidance → Getting started docs

**Process:**
1. Read `references/overview/intro.md`
2. Read `references/getting-started/installation.md`
3. Read `references/getting-started/basic-usage.md`

**Response includes:**
- What the Abilities API is
- Installation instructions
- First ability example
- Next steps

### Example 4: Integration Query

**Query:** "How do I execute a PHP ability from JavaScript?"

**Routing:** Integration query → Multiple APIs

**Process:**
1. Read `references/php-api/registering-abilities.md` (show_in_rest)
2. Read `references/javascript-client/abilities.md` (executeAbility)
3. Read `references/rest-api/execution.md`

**Response includes:**
- PHP registration with show_in_rest: true
- JavaScript executeAbility example
- REST API authentication
- Error handling on both sides

### Example 5: Troubleshooting Query

**Query:** "Why am I getting a WP_Error when executing an ability?"

**Routing:** Troubleshooting → Error handling + Execution

**Process:**
1. Read `references/php-api/error-handling.md`
2. Read `references/php-api/using-abilities.md`
3. Identify common error patterns

**Response includes:**
- WP_Error handling patterns
- Common error scenarios (permissions, validation, execution)
- Checking for errors with is_wp_error()
- Related: Permissions, Validation

## Common Issues & Quick Fixes

### Registration Failures

**Issue:** Ability not found / "category must contain only lowercase alphanumeric characters and dashes"
**Fix:** Category slug uses slashes → Change to dashes only (`my-plugin-content` not `my-plugin/content`)

**Issue:** "Property 'show_in_rest' is not a valid property"
**Fix:** Move `show_in_rest` inside `meta` array, not top-level

**Issue:** Ability not discoverable via MCP
**Fix:** Add `'mcp' => array('public' => true)` inside `meta` array

### Schema Validation Failures

**Issue:** Output validation fails with "field is not of type X" when field is null
**Fix:** Use array type syntax to allow null: `'type' => array('object', 'null')`

**Issue:** Enum validation fails when field value is empty string
**Fix:** Include empty string in enum: `'enum' => array('option1', 'option2', '')`

### REST API Issues

**Issue:** GET request `input` param not being parsed correctly
**Fix:** Use array-style params (`input[post_id]=1`) instead of JSON string. POST with JSON body works normally.

### WP-CLI Testing

**Issue:** `ability_invalid_permissions` error when testing via WP-CLI
**Fix:** Pass `--user=admin` flag to provide user context for permission checks

### External Plugin Integration

When integrating with external plugins, always check availability first:
```php
'execute_callback' => function( $input ) {
    if ( ! class_exists( 'PluginNamespace\Class' ) ) {
        return new WP_Error( 'plugin_not_active', 'Required plugin not active', array( 'status' => 503 ) );
    }
    // Use plugin functionality
},
```

### Correct Meta Structure

```php
'meta' => array(
    'show_in_rest' => true,        // REST API exposure
    'mcp'          => array(
        'public' => true,          // MCP discoverability
        'type'   => 'tool',        // 'tool', 'resource', or 'prompt'
    ),
),
```

## Important Notes

### Naming Conventions

Always mention:
- **Ability names:** `plugin-name/ability-name` (forward slash after prefix)
- **Category slugs:** `plugin-name-category-name` (dashes only, NO slashes)
- Use lowercase with hyphens throughout
- Include plugin/theme prefix for uniqueness

**CRITICAL:** Category slugs must use dashes only. Forward slashes cause validation errors.

### Security

Reference security when appropriate:
- Always implement permission_callback
- Validate and sanitize input
- Use WordPress nonce for AJAX requests
- Follow WordPress security best practices

### WordPress Integration

- Register abilities on `wp_abilities_api_init` or `init` hooks
- Use `wp_abilities_api_categories_init` for categories
- Check availability with `class_exists( 'WP_Abilities_Registry' )`
- Follow WordPress coding standards

### REST API & MCP Exposure

**REST API:**
- Set `show_in_rest: true` (inside `meta` array) to expose via REST API
- Consider authentication requirements
- Use readonly annotation for safe GET execution
- Destructive operations require POST

**MCP (Model Context Protocol):**
- Set `mcp.public: true` (inside `meta` array) to make discoverable by AI assistants
- Type options: `'tool'` (default), `'resource'`, `'prompt'`
- Only abilities with `mcp.public = true` are exposed via MCP adapter

## Workflow Summary

**For every query:**

1. **Identify intent** → Implementation, API reference, getting started, integration, or troubleshooting
2. **Route appropriately** → Determine which files to fetch
3. **Search INDEX.md** → Find relevant functions, keywords, categories
4. **Read files** → Use Read tool to access documentation
5. **Format response** → Include code examples, content, integration patterns, suggestions
6. **Suggest related** → Use category groupings and common pairings

**Keep responses:**
- Focused on documented information
- Formatted with clear code examples
- Enriched with relevant topic suggestions
- Practical with setup and usage guidance
- Security-conscious with permission reminders
