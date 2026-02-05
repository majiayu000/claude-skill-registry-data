---
name: wordpress-ability-api
description: This skill should be used when helping users create, edit, or register WordPress Abilities (both server-side PHP and client-side JavaScript), register ability categories, or set up the WordPress Abilities API as a dependency. Use when users say things like "create an ability", "help me build an ability", "set up the Ability API", or "register a category".
---

# WordPress Ability API

## Overview

This skill helps users work with the WordPress Abilities API - a standardized system for registering and discovering distinct units of functionality within WordPress. Use this skill to help users create server-side PHP abilities, client-side JavaScript abilities, register categories, and set up the API as a dependency.

The Abilities API makes WordPress functionality discoverable by AI agents and automation tools through machine-readable schemas, permissions, and validation.

## When to Use This Skill

Activate this skill when the user requests:

- **Creating abilities**: "Help me create an ability to...", "I want to make an ability that...", "Build me an ability for..."
- **Editing abilities**: "Update my ability", "Fix this ability code", "Modify the ability to..."
- **Setting up the API**: "Set up the Ability API", "Add the Ability API as a dependency", "Install the Abilities API"
- **Registering categories**: "Create a category for my abilities", "Register an ability category"

## Workflow Decision Tree

When this skill activates, determine what the user needs:

1. **Are they creating/editing an ability?**
   → Follow the "Creating Abilities" workflow below

2. **Do they need to set up the API first?**
   → Follow the "Setting Up the API" workflow below

3. **Are they just learning about the API?**
   → Reference the documentation in `references/` and explain concepts

## Using the Scaffold Script

The skill includes a `scripts/scaffold-ability.php` script designed for programmatic ability generation. Use this when creating abilities to quickly generate validated boilerplate code.

### Script Usage

```bash
php scripts/scaffold-ability.php \
  --name="plugin/ability-name" \
  --type="server" \
  --category="data-retrieval" \
  --label="Optional Label" \
  --description="Optional description"
```

**Required Arguments:**

- `--name` - Ability name in format "namespace/ability-name"
- `--type` - Either "server" (PHP) or "client" (JavaScript)
- `--category` - Category slug (e.g., "data-retrieval", "data-modification")

**Optional Arguments:**

- `--label` - Human-readable label (auto-generated from name if omitted)
- `--description` - Detailed description (placeholder if omitted)
- `--readonly` - "true" or "false" (default: false)
- `--destructive` - "true" or "false" (default: true)
- `--idempotent` - "true" or "false" (default: false)

**Output:** Complete ability code printed to stdout, ready to be written to plugin files.

### When to Use the Scaffold Script

Use the scaffold script after gathering requirements from the user (Steps 1-3 of the workflow below). The script generates clean, validated boilerplate that follows best practices.

**Important:** Always gather required information from the user BEFORE calling the script, or generate sensible defaults based on context.

## Creating Abilities

When helping users create or edit abilities, follow this conversational workflow:

### Step 1: Understand the Functionality

Ask clarifying questions to understand what the ability should do:

- **What should this ability do?** (e.g., "Get site analytics", "Send notifications", "Update settings")
- **Is this a server-side or client-side ability?**
  - **Server-side (PHP)**: Runs on the WordPress backend, accesses database, uses WordPress functions
  - **Client-side (JavaScript)**: Runs in the browser, manipulates DOM, handles UI interactions
- **What input parameters does it need?** (e.g., user ID, date range, options)
- **What should it return?** (e.g., array of data, success boolean, error messages)
- **Who should be able to use it?** (permissions: any user, logged-in users, administrators, custom capability)

### Step 2: Determine Plugin Location

Ask where the ability code should live:

- **"Which plugin should this ability be registered in?"**
  - If they have an existing plugin, use that
  - If they need a new plugin, offer to create one using the `wordpress-plugin-scaffold` skill

### Step 3: Check for Category

Abilities must belong to a category. Ask:

- **"Which category should this ability belong to?"**
  - Example categories: `data-retrieval`, `data-modification`, `communication`, `ecommerce`, `user-management`
  - If they need a custom category, use `scripts/scaffold-category.php` to generate it:

```bash
php scripts/scaffold-category.php \
  --name="custom-category" \
  --label="Custom Category" \
  --description="Description of what abilities belong here" \
  --type="server|client"
```

- Alternatively, manually customize `assets/category-template.php`
- See `references/7.registering-categories.md` for detailed category registration information

### Step 4: Generate the Ability Code

Use the scaffold script to generate complete, validated code:

```bash
php scripts/scaffold-ability.php \
  --name="namespace/ability-name" \
  --type="server|client" \
  --category="category-slug" \
  --label="Human Label" \
  --description="Detailed description" \
  --readonly="true|false" \
  --destructive="true|false" \
  --idempotent="true|false"
```

**For server-side (PHP):** Outputs complete PHP code with callback and registration functions
**For client-side (JavaScript):** Outputs complete JavaScript code with async callback

Alternatively, manually copy and customize templates from `assets/` directory:

- `server-ability-template.php` - PHP abilities
- `client-ability-template.js` - JavaScript abilities

Replace all `{{PLACEHOLDERS}}` with actual values. See templates for full list of placeholders.

### Step 5: Validate the Code

Before adding the code to plugin files, validate it using the appropriate validation script:

#### Validate Abilities

**For PHP abilities:**

```bash
php scripts/validate-ability.php path/to/ability-file.php
```

**For JavaScript abilities:**

```bash
node scripts/validate-ability.js path/to/ability-file.js
```

#### Validate Categories

**For PHP categories:**

```bash
php scripts/validate-category.php path/to/category-file.php
```

**For JavaScript categories:**

```bash
node scripts/validate-category.js path/to/category-file.js
```

All validators check:

- **Structure**: Required fields (name, label, description, schemas/callbacks) are present
- **JSON Schema validity**: Schemas follow JSON Schema specification (abilities only)
- **Best practices**: Proper naming (kebab-case), annotations, permission callbacks
- **Common mistakes**: TODO placeholders, empty descriptions, security concerns

**Exit codes:**

- `0` - Validation passed
- `1` - Validation failed (errors found)
- `2` - File not found or invalid usage

Fix any errors reported by the validator before proceeding.

### Step 6: Add to Plugin Files

Write the validated code to the appropriate plugin files:

- **PHP abilities**: Add to plugin's main PHP file or create a dedicated `includes/abilities.php` file and hook into `abilities_api_init`
- **JavaScript abilities**: Add to enqueued JavaScript file with `@wordpress/abilities` dependency
- **Categories**: Register on `abilities_api_categories_init` hook before abilities

Use the Write tool to add the code to the correct location in the plugin.

### Step 7: Test the Ability

After code is added to plugin files, suggest testing approaches:

**Server-side (PHP):**

- Use `wp_get_ability('namespace/name')` to verify registration
- Test execution via REST API: `POST /wp-json/abilities/v1/abilities/{namespace}/{ability-name}/execute`
- Or test directly: `$ability->execute( $input_data )`
- Verify permissions work as expected
- Check input validation catches invalid data

**Client-side (JavaScript):**

- Open browser DevTools console
- Check registration: `wp.data.select('core/abilities').getAbility('namespace/ability-name')`
- Execute ability: `wp.data.dispatch('core/abilities').executeAbility('namespace/ability-name', inputData)`
- Check available abilities: `wp.data.select('core/abilities').getAbilities()`
- Verify permissions and error handling work correctly

## Setting Up the API

The WordPress Abilities API must be available before abilities can be registered. Help users set up the API based on their WordPress version:

### Check WordPress Version

**WordPress 6.9+**: The Abilities API is included in core - no setup needed!

**WordPress < 6.9**: The API must be installed as a plugin or dependency.

### Installation Options

Reference `references/2.getting-started.md` for detailed setup instructions. Guide users through the most appropriate method:

#### Option 1: As a Plugin (Easiest for Testing)

If they're using **wp-env** (check for `.wp-env.json`), help them add it via the `wp-env` skill:

```json
{
  "plugins": ["WordPress/abilities-api"]
}
```

If they're using **WP-CLI**:

```bash
wp plugin install https://github.com/WordPress/abilities-api/releases/latest/download/abilities-api.zip
wp plugin activate abilities-api
```

#### Option 2: As a Plugin Dependency (Recommended for Plugins)

Help them add to their plugin header:

```php
/**
 * Plugin Name: My Plugin
 * Requires Plugins: abilities-api
 */
```

Then add availability check:

```php
if ( ! class_exists( 'WP_Ability' ) ) {
    add_action( 'admin_notices', function() {
        wp_admin_notice(
            __( 'This plugin requires the Abilities API. Please install and activate it.', 'my-plugin' ),
            'error'
        );
    } );
    return;
}
```

#### Option 3: As a Composer Dependency

```bash
composer require wordpress/abilities-api
```

### Verify Installation

Help users verify the API is loaded:

```php
if ( class_exists( 'WP_Ability' ) ) {
    // API is available
    echo 'Abilities API version: ' . WP_ABILITIES_API_VERSION;
}
```

## Integration with Other Skills

This skill works well with:

- **wordpress-plugin-scaffold**: Use when users need a new plugin to register abilities in
- **wp-env**: Use for local development environment setup when installing the Abilities API

## Reference Documentation

The `references/` directory contains complete API documentation:

- **1.intro.md**: Core concepts, goals, and benefits of the Abilities API
- **2.getting-started.md**: Installation methods and basic usage examples
- **3.registering-abilities.md**: Comprehensive guide to `wp_register_ability()` with all parameters and examples
- **4.using-abilities.md**: How to retrieve and execute abilities in PHP
- **5.rest-api.md**: REST API endpoints for abilities
- **6.hooks.md**: Available WordPress hooks in the Abilities API
- **7.javascript-client.md**: Complete client-side JavaScript API reference
- **7.registering-categories.md**: How to register ability categories

**When to read references:**

- For specific parameter details → `3.registering-abilities.md`
- For setup instructions → `2.getting-started.md`
- For client-side abilities → `7.javascript-client.md`
- For category registration → `7.registering-categories.md`
- For conceptual understanding → `1.intro.md`

## Scripts and Templates

### Scripts (`scripts/`)

The skill includes automation scripts for generating and validating both abilities and categories:

#### Ability Scripts

- **scaffold-ability.php**: Programmatically generate ability code from CLI arguments
  - Accepts: name, type, category, label, description, and annotation flags
  - Outputs: Complete, validated ability code to stdout
  - Usage: `php scripts/scaffold-ability.php --name="plugin/ability" --type="server" --category="data-retrieval"`
  - Use when: Creating new abilities after gathering requirements

- **validate-ability.php**: Validate PHP ability code independently of WordPress
  - Checks: Required fields, JSON Schema validity, best practices
  - Outputs: Detailed validation results with errors and warnings
  - Usage: `php scripts/validate-ability.php path/to/ability-file.php`
  - Use when: Validating server-side PHP ability code before registration

- **validate-ability.js**: Validate JavaScript ability registration code
  - Requirements: Node.js and acorn parser (`npm install acorn`)
  - Parser: Uses acorn AST parser for accurate JavaScript parsing
  - Checks: Required fields (name, category, callback), name format, schemas, permissions, annotations
  - Outputs: Detailed validation results with errors and warnings
  - Usage: `node scripts/validate-ability.js path/to/ability-file.js`
  - Use when: Validating client-side JavaScript ability code before registration

#### Category Scripts

- **scaffold-category.php**: Programmatically generate category registration code
  - Accepts: name, label, description, type (server/client)
  - Outputs: Complete category registration code to stdout
  - Usage: `php scripts/scaffold-category.php --name="category-slug" --label="Label" --description="Description" --type="server"`
  - Use when: Creating custom categories for abilities
  - Includes helpful comments about registration hooks and timing

- **validate-category.php**: Validate PHP category registration code
  - Parser: Uses PHP's `token_get_all()` for accurate parsing
  - Checks: Name format (kebab-case), required fields, description quality
  - Outputs: Detailed validation results with errors and warnings
  - Usage: `php scripts/validate-category.php path/to/category-file.php`
  - Use when: Validating server-side PHP category code

- **validate-category.js**: Validate JavaScript category registration code
  - Requirements: Node.js and acorn parser (`npm install acorn`)
  - Parser: Uses acorn AST parser for accurate JavaScript parsing
  - Checks: Same validations as PHP validator
  - Outputs: Detailed validation results with errors and warnings
  - Usage: `node scripts/validate-category.js path/to/category-file.js`
  - Use when: Validating client-side JavaScript category code

### Template Assets (`assets/`)

The skill also includes manual starter templates:

- **server-ability-template.php**: Complete boilerplate for server-side PHP abilities
- **client-ability-template.js**: Complete boilerplate for client-side JavaScript abilities
- **category-template.php**: Template for server-side PHP category registration
- **client-category-template.js**: Template for client-side JavaScript category registration

**Note:** Templates use `{{PLACEHOLDER}}` syntax and are read by scaffold scripts. You can also manually copy and replace placeholders for custom needs. Scaffold scripts generate code by loading these templates and replacing placeholders with actual values.

## Best Practices

When helping users create abilities:

1. **Use descriptive names**: `my-plugin/get-user-analytics` not `my-plugin/analytics`
2. **Write detailed descriptions**: Help AI agents understand WHEN and HOW to use the ability
3. **Define complete schemas**: Use JSON Schema to validate inputs and document outputs
4. **Implement proper permissions**: Never use `__return_true` for sensitive operations
5. **Use appropriate annotations**:
   - `readonly: true` for data retrieval abilities
   - `destructive: false` for abilities that only add/update (never delete)
   - `idempotent: true` for abilities that can be called repeatedly safely
6. **Handle errors gracefully**: Return `WP_Error` objects with clear error messages
7. **Test thoroughly**: Verify schema validation, permissions, and error cases

## Common Patterns

### Read-Only Data Retrieval

```php
'meta' => array(
    'annotations' => array(
        'readonly' => true,
        'destructive' => false,
        'idempotent' => true,
    ),
)
```

### Data Modification (Non-Destructive)

```php
'meta' => array(
    'annotations' => array(
        'readonly' => false,
        'destructive' => false,
        'idempotent' => false,
    ),
)
```

### Potentially Destructive Operations

```php
'meta' => array(
    'annotations' => array(
        'readonly' => false,
        'destructive' => true,
        'idempotent' => false,
    ),
),
'permission_callback' => function() {
    return current_user_can( 'manage_options' );
}
```

## Advanced Features

### Client-Side Category Registration

When registering client-side abilities with custom categories, use `registerAbilityCategory()` before registering the ability:

```javascript
import { registerAbilityCategory, registerAbility } from '@wordpress/abilities';

// Register the category first
await registerAbilityCategory('my-custom-category', {
  label: 'My Custom Category',
  description: 'Description of what abilities belong in this category',
  meta: {
    icon: 'dashicons-admin-customizer',
    priority: 10,
  },
});

// Then register abilities using that category
await registerAbility({
  name: 'my-plugin/my-ability',
  category: 'my-custom-category', // Uses the client-registered category
  // ... other properties
});
```

### Custom Ability Classes (Advanced)

For advanced use cases requiring custom behavior, specify a custom class that extends `WP_Ability` using the `ability_class` parameter:

```php
class Custom_Ability extends WP_Ability {
    // Override methods for custom behavior
    public function execute( $input = array() ) {
        // Custom execution logic
        return parent::execute( $input );
    }
}

wp_register_ability( 'my-plugin/custom-ability', array(
    // ... standard parameters
    'ability_class' => Custom_Ability::class, // Use custom class instead of WP_Ability
) );
```

**Note:** This is an advanced feature. Most abilities should use the default `WP_Ability` class.
