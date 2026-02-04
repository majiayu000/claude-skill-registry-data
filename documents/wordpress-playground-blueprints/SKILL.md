---
name: wordpress-playground-blueprints
description: Guide for creating WordPress Playground Blueprint JSON files and executing WP-CLI commands. Use when building Blueprint files, automating WordPress/WooCommerce management via CLI, configuring WordPress Playground environments, or troubleshooting. Covers blueprint creation, WP-CLI commands, and WooCommerce CLI operations. All blueprints must conform to https://playground.wordpress.net/blueprint-schema.json
---

# WordPress Playground Blueprints

Blueprints are JSON configuration files that set up WordPress Playground instances with specific versions, plugins, themes, content, and settings.

## What are Blueprints?

Blueprints are JSON configuration files that:
- Set up WordPress Playground instances with specific PHP/WordPress versions
- Install and configure plugins, themes, and content
- Execute PHP code and SQL queries
- Manipulate files and directories
- Define WordPress constants and site options

## Blueprint Structure

### Required Schema Reference

Always include the schema reference as the first property:

```json
{
  "$schema": "https://playground.wordpress.net/blueprint-schema.json"
}
```

### Top-Level Properties

#### 1. `landingPage` (string)
The URL to navigate to after blueprint execution. Use relative paths.

```json
{
  "landingPage": "/wp-admin/site-editor.php"
}
```

Common landing pages:
- `/` - Homepage
- `/wp-admin/` - Admin dashboard
- `/wp-admin/post.php?post=4&action=edit` - Edit specific post
- `/wp-admin/site-editor.php` - Site editor
- `/wp-admin/plugin-install.php` - Plugin installer

#### 2. `preferredVersions` (object)
Specify PHP and WordPress versions.

```json
{
  "preferredVersions": {
    "php": "8.3",
    "wp": "latest"
  }
}
```

**Supported PHP versions:** `"8.4"`, `"8.3"`, `"8.2"`, `"8.1"`, `"8.0"`, `"7.4"`, `"7.3"`, `"7.2"`, or `"latest"`

**Supported WordPress versions:** `"latest"`, `"nightly"`, `"beta"`, or specific versions like `"6.5"`, `"6.6"`, `"6.7"`, `"6.8"`

**For older WordPress versions (6.2.1+):**
```json
{
  "preferredVersions": {
    "wp": "https://playground.wordpress.net/plugin-proxy.php?url=https://wordpress.org/wordpress-6.2.1.zip",
    "php": "8.3"
  }
}
```

**For WordPress trunk or specific commits:**
```json
{
  "preferredVersions": {
    "wp": "https://playground.wordpress.net/plugin-proxy.php?build-ref=trunk",
    "php": "8.3"
  }
}
```

#### 3. `features` (object)
Enable/disable Playground features.

```json
{
  "features": {
    "networking": true
  }
}
```

- `networking` (boolean): Enable HTTP requests (required for plugin/theme installation from WordPress.org)

#### 4. `extraLibraries` (array)
Preload additional libraries.

```json
{
  "extraLibraries": ["wp-cli"]
}
```

Currently supported: `"wp-cli"`

#### 5. `meta` (object)
Metadata for blueprint gallery (optional but recommended).

```json
{
  "meta": {
    "title": "My Blueprint",
    "description": "A brief explanation of what this blueprint does",
    "author": "github-username",
    "categories": ["development", "ecommerce"]
  }
}
```

## Shorthand Properties

These provide concise alternatives to step definitions:

### `login` (boolean or object)

```json
{
  "login": true
}
```

Equivalent to:
```json
{
  "steps": [
    {
      "step": "login",
      "username": "admin",
      "password": "password"
    }
  ]
}
```

### `plugins` (array)

```json
{
  "plugins": [
    "hello-dolly",
    "https://example.com/plugin.zip"
  ]
}
```

Equivalent to multiple `installPlugin` steps.

### `siteOptions` (object)

```json
{
  "siteOptions": {
    "blogname": "My Site",
    "blogdescription": "Just another WordPress site"
  }
}
```

Equivalent to `setSiteOptions` step.

### `constants` (object)

```json
{
  "constants": {
    "WP_DEBUG": true,
    "WP_DEBUG_DISPLAY": true
  }
}
```

Equivalent to `defineWpConfigConsts` step.

## Steps

The `steps` array defines actions to execute sequentially. Each step is an object with a `step` property identifying its type.

### Common Step Properties

All steps support optional `progress` configuration:

```json
{
  "step": "installPlugin",
  "progress": {
    "weight": 2,
    "caption": "Installing my plugin..."
  }
}
```

### Resource References

Many steps accept file/directory references. All resource types:

#### 1. URL Reference
```json
{
  "resource": "url",
  "url": "https://example.com/file.zip",
  "caption": "Downloading plugin..."
}
```

#### 2. WordPress.org Plugin
```json
{
  "resource": "wordpress.org/plugins",
  "slug": "akismet",
  "version": "5.0"
}
```

#### 3. WordPress.org Theme
```json
{
  "resource": "wordpress.org/themes",
  "slug": "twentytwentyfour",
  "version": "1.0"
}
```

#### 4. Git Directory Reference
```json
{
  "resource": "git:directory",
  "url": "https://github.com/WordPress/block-development-examples",
  "ref": "HEAD",
  "path": "plugins/data-basics-59c8f8"
}
```

#### 5. Bundled Reference
```json
{
  "resource": "bundled",
  "path": "/my-plugin.zip"
}
```

#### 6. VFS Reference
```json
{
  "resource": "vfs",
  "path": "/wordpress/wp-content/my-file.php"
}
```

#### 7. Literal Reference
```json
{
  "resource": "literal",
  "name": "my-file.txt",
  "contents": "Hello World!"
}
```

### Essential Steps Reference

#### installPlugin
Installs a WordPress plugin.

```json
{
  "step": "installPlugin",
  "pluginData": {
    "resource": "wordpress.org/plugins",
    "slug": "gutenberg"
  },
  "options": {
    "activate": true
  }
}
```

Properties:
- `pluginData`: FileReference or DirectoryReference (required)
- `options.activate`: Boolean to activate after install
- `options.targetFolderName`: Custom folder name
- `ifAlreadyInstalled`: `"overwrite"`, `"skip"`, or `"error"`

#### installTheme
Installs a WordPress theme.

```json
{
  "step": "installTheme",
  "themeData": {
    "resource": "wordpress.org/themes",
    "slug": "twentytwentyfour"
  },
  "options": {
    "activate": true,
    "importStarterContent": false
  }
}
```

Properties:
- `themeData`: FileReference or DirectoryReference (required)
- `options.activate`: Boolean to activate after install
- `options.importStarterContent`: Boolean to import starter content
- `options.targetFolderName`: Custom folder name
- `ifAlreadyInstalled`: `"overwrite"`, `"skip"`, or `"error"`

#### activatePlugin
Activates an installed plugin.

```json
{
  "step": "activatePlugin",
  "pluginPath": "plugin-folder/plugin-file.php",
  "pluginName": "My Plugin"
}
```

Properties:
- `pluginPath`: Absolute path or relative to plugins directory (required)
- `pluginName`: Display name for progress (optional)

#### activateTheme
Activates an installed theme.

```json
{
  "step": "activateTheme",
  "themeFolderName": "twentytwentyfour"
}
```

#### login
Logs in as a WordPress user.

```json
{
  "step": "login",
  "username": "admin"
}
```

Note: `password` parameter is deprecated and no longer required.

#### runPHP
Executes PHP code.

```json
{
  "step": "runPHP",
  "code": "<?php require_once '/wordpress/wp-load.php'; wp_insert_post(['post_title' => 'Hello', 'post_status' => 'publish', 'post_author' => 1]);"
}
```

**CRITICAL:** Always require `/wordpress/wp-load.php` when using WordPress functions.

Alternative format:
```json
{
  "step": "runPHP",
  "code": {
    "filename": "my-script.php",
    "content": "<?php require_once '/wordpress/wp-load.php'; // your code"
  }
}
```

#### runSql
Executes SQL queries.

```json
{
  "step": "runSql",
  "sql": {
    "resource": "literal",
    "name": "queries.sql",
    "contents": "UPDATE wp_posts SET post_status='publish' WHERE post_status='draft';"
  }
}
```

#### setSiteOptions
Sets WordPress site options.

```json
{
  "step": "setSiteOptions",
  "options": {
    "blogname": "My Awesome Site",
    "blogdescription": "A demo site",
    "permalink_structure": "/%postname%/"
  }
}
```

#### defineWpConfigConsts
Defines WordPress constants in wp-config.php.

```json
{
  "step": "defineWpConfigConsts",
  "consts": {
    "WP_DEBUG": true,
    "WP_DEBUG_LOG": true,
    "WP_DEBUG_DISPLAY": false,
    "WP_DISABLE_FATAL_ERROR_HANDLER": true
  },
  "method": "rewrite-wp-config"
}
```

Methods:
- `"rewrite-wp-config"`: Modifies wp-config.php file (default)
- `"define-before-run"`: Defines before script execution (no file modification)

#### defineSiteUrl
Sets the WordPress site URL.

```json
{
  "step": "defineSiteUrl",
  "siteUrl": "https://example.com"
}
```

#### importWxr
Imports WordPress content from WXR file.

```json
{
  "step": "importWxr",
  "file": {
    "resource": "url",
    "url": "https://example.com/content.wxr"
  }
}
```

#### importThemeStarterContent
Imports a theme's starter content.

```json
{
  "step": "importThemeStarterContent",
  "themeSlug": "twentytwentyfour"
}
```

#### writeFile
Writes content to a file.

```json
{
  "step": "writeFile",
  "path": "/wordpress/wp-content/mu-plugins/custom.php",
  "data": "<?php // Custom code"
}
```

Data can be:
- String
- FileReference
- Uint8Array (binary data)

#### writeFiles
Writes multiple files from a directory structure.

```json
{
  "step": "writeFiles",
  "writeToPath": "/wordpress/wp-content/themes/my-theme",
  "filesTree": {
    "resource": "literal:directory",
    "name": "my-theme",
    "files": {
      "style.css": "/* Theme styles */",
      "functions.php": "<?php // Theme functions",
      "templates/index.html": "<!-- Template -->"
    }
  }
}
```

#### mkdir
Creates a directory.

```json
{
  "step": "mkdir",
  "path": "/wordpress/wp-content/uploads/custom"
}
```

#### cp
Copies a file or directory.

```json
{
  "step": "cp",
  "fromPath": "/wordpress/wp-content/plugins/source",
  "toPath": "/wordpress/wp-content/plugins/destination"
}
```

#### mv
Moves/renames a file or directory.

```json
{
  "step": "mv",
  "fromPath": "/wordpress/wp-content/themes/old-name",
  "toPath": "/wordpress/wp-content/themes/new-name"
}
```

#### rm
Removes a file.

```json
{
  "step": "rm",
  "path": "/wordpress/wp-content/plugins/unwanted.php"
}
```

#### rmdir
Removes a directory.

```json
{
  "step": "rmdir",
  "path": "/wordpress/wp-content/themes/old-theme"
}
```

#### unzip
Extracts a zip file.

```json
{
  "step": "unzip",
  "zipFile": {
    "resource": "url",
    "url": "https://example.com/files.zip"
  },
  "extractToPath": "/wordpress/wp-content/uploads"
}
```

#### request
Makes an HTTP request to WordPress.

```json
{
  "step": "request",
  "request": {
    "url": "/wp-admin/admin-ajax.php",
    "method": "POST",
    "headers": {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    "body": "action=my_action&data=value"
  }
}
```

#### wp-cli
Executes WP-CLI commands.

```json
{
  "step": "wp-cli",
  "command": "post list --format=json"
}
```

Or with array format:
```json
{
  "step": "wp-cli",
  "command": ["post", "create", "--post_title=Hello", "--post_status=publish"]
}
```

Note: Requires `"extraLibraries": ["wp-cli"]` or will be auto-included if using wp-cli steps.

#### enableMultisite
Enables WordPress multisite.

```json
{
  "step": "enableMultisite"
}
```

#### resetData
Resets WordPress database to initial state.

```json
{
  "step": "resetData"
}
```

#### updateUserMeta
Updates user metadata.

```json
{
  "step": "updateUserMeta",
  "userId": 1,
  "meta": {
    "first_name": "John",
    "last_name": "Doe",
    "description": "WordPress developer"
  }
}
```

#### setSiteLanguage
Sets the site language.

```json
{
  "step": "setSiteLanguage",
  "language": "es_ES"
}
```

#### runWpInstallationWizard
Runs the WordPress installation wizard.

```json
{
  "step": "runWpInstallationWizard",
  "options": {
    "adminUsername": "admin",
    "adminPassword": "password"
  }
}
```

#### runPHPWithOptions
Runs PHP with detailed options.

```json
{
  "step": "runPHPWithOptions",
  "options": {
    "code": "<?php echo 'Hello';",
    "env": {
      "MY_VAR": "value"
    },
    "$_SERVER": {
      "REQUEST_METHOD": "POST"
    }
  }
}
```

## Common Patterns

### Pattern 1: Basic Plugin Demo
```json
{
  "$schema": "https://playground.wordpress.net/blueprint-schema.json",
  "landingPage": "/wp-admin/plugins.php",
  "preferredVersions": {
    "php": "8.3",
    "wp": "latest"
  },
  "features": {
    "networking": true
  },
  "steps": [
    {
      "step": "login"
    },
    {
      "step": "installPlugin",
      "pluginData": {
        "resource": "url",
        "url": "https://example.com/my-plugin.zip"
      },
      "options": {
        "activate": true
      }
    }
  ]
}
```

### Pattern 2: Theme Demo with Content
```json
{
  "$schema": "https://playground.wordpress.net/blueprint-schema.json",
  "landingPage": "/",
  "preferredVersions": {
    "php": "8.3",
    "wp": "latest"
  },
  "features": {
    "networking": true
  },
  "siteOptions": {
    "blogname": "Demo Site"
  },
  "steps": [
    {
      "step": "installTheme",
      "themeData": {
        "resource": "wordpress.org/themes",
        "slug": "twentytwentyfour"
      },
      "options": {
        "activate": true,
        "importStarterContent": true
      }
    },
    {
      "step": "importWxr",
      "file": {
        "resource": "url",
        "url": "https://example.com/sample-content.xml"
      }
    }
  ]
}
```

### Pattern 3: Development Environment
```json
{
  "$schema": "https://playground.wordpress.net/blueprint-schema.json",
  "landingPage": "/wp-admin/",
  "preferredVersions": {
    "php": "8.3",
    "wp": "latest"
  },
  "features": {
    "networking": true
  },
  "constants": {
    "WP_DEBUG": true,
    "WP_DEBUG_LOG": true,
    "WP_DEBUG_DISPLAY": true,
    "SCRIPT_DEBUG": true
  },
  "login": true,
  "plugins": ["query-monitor", "debug-bar"],
  "steps": [
    {
      "step": "setSiteOptions",
      "options": {
        "permalink_structure": "/%postname%/"
      }
    }
  ]
}
```

### Pattern 4: Custom MU-Plugin
```json
{
  "$schema": "https://playground.wordpress.net/blueprint-schema.json",
  "landingPage": "/",
  "steps": [
    {
      "step": "writeFile",
      "path": "/wordpress/wp-content/mu-plugins/custom-functions.php",
      "data": "<?php\nadd_action('after_setup_theme', function() {\n    global $wp_rewrite;\n    $wp_rewrite->set_permalink_structure('/%postname%/');\n    $wp_rewrite->flush_rules();\n});"
    }
  ]
}
```

### Pattern 5: WP-CLI Integration
```json
{
  "$schema": "https://playground.wordpress.net/blueprint-schema.json",
  "landingPage": "/wp-admin/",
  "extraLibraries": ["wp-cli"],
  "features": {
    "networking": true
  },
  "steps": [
    {
      "step": "login"
    },
    {
      "step": "wp-cli",
      "command": "plugin install gutenberg --activate"
    },
    {
      "step": "wp-cli",
      "command": ["post", "create", "--post_title=Hello World", "--post_status=publish"]
    }
  ]
}
```

### Pattern 6: Blueprint Bundle
For a bundle named `my-bundle.zip` containing:
- `/blueprint.json`
- `/my-plugin.zip`
- `/assets/custom.css`

```json
{
  "$schema": "https://playground.wordpress.net/blueprint-schema.json",
  "landingPage": "/",
  "steps": [
    {
      "step": "installPlugin",
      "pluginData": {
        "resource": "bundled",
        "path": "/my-plugin.zip"
      },
      "options": {
        "activate": true
      }
    },
    {
      "step": "writeFile",
      "path": "/wordpress/wp-content/themes/twentytwentyfour/custom.css",
      "data": {
        "resource": "bundled",
        "path": "/assets/custom.css"
      }
    }
  ]
}
```

## Best Practices

### 1. Always Include Schema
```json
{
  "$schema": "https://playground.wordpress.net/blueprint-schema.json"
}
```

### 2. Use Appropriate PHP/WordPress Versions
- Use `"latest"` for most cases
- Specify exact versions only when necessary for compatibility
- Minimum WordPress version: 6.2.1 (due to SQLite integration)

### 3. Enable Networking When Needed
If installing from wordpress.org or making HTTP requests:
```json
{
  "features": {
    "networking": true
  }
}
```

### 4. Use Shorthands for Simplicity
Instead of:
```json
{
  "steps": [
    {
      "step": "login",
      "username": "admin"
    }
  ]
}
```

Use:
```json
{
  "login": true
}
```

### 5. Always Require wp-load.php in runPHP
```json
{
  "step": "runPHP",
  "code": "<?php require_once '/wordpress/wp-load.php'; // Your WordPress code"
}
```

### 6. Use Progress Captions for Long Operations
```json
{
  "step": "installPlugin",
  "progress": {
    "caption": "Installing WooCommerce (this may take a moment)..."
  },
  "pluginData": {
    "resource": "wordpress.org/plugins",
    "slug": "woocommerce"
  }
}
```

### 7. Handle Plugin Installation Conflicts
```json
{
  "step": "installPlugin",
  "pluginData": { ... },
  "ifAlreadyInstalled": "skip"
}
```

Options: `"overwrite"`, `"skip"`, `"error"`

### 8. Set Landing Pages Appropriately
- Demos: Land on homepage `/` or relevant page
- Admin features: Land on `/wp-admin/` or specific admin page
- Editor features: Land on post editor or site editor

### 9. Use Metadata for Gallery Submissions
```json
{
  "meta": {
    "title": "WooCommerce Demo",
    "description": "A complete WooCommerce store setup",
    "author": "your-github-username",
    "categories": ["ecommerce", "demo"]
  }
}
```

### 10. Organize Complex Blueprints
Group related steps with comments (in your development environment):
```json
{
  "steps": [
    {
      "step": "login"
    },
    // Install core plugins
    {
      "step": "installPlugin",
      "pluginData": { ... }
    },
    // Configure site
    {
      "step": "setSiteOptions",
      "options": { ... }
    }
  ]
}
```

## Troubleshooting

### Common Issues

#### 1. Database Connection Error with WP-CLI on Mounted Sites
**Problem:** `wp-cli` commands fail with database connection error.

**Solution:** Explicitly install SQLite integration:
```json
{
  "plugins": ["sqlite-database-integration"]
}
```

#### 2. Plugin Not Activating
**Problem:** Plugin installs but doesn't activate.

**Solution:** Ensure `activate: true` in options:
```json
{
  "step": "installPlugin",
  "pluginData": { ... },
  "options": {
    "activate": true
  }
}
```

#### 3. runPHP Not Working
**Problem:** WordPress functions undefined in PHP code.

**Solution:** Always require wp-load.php:
```json
{
  "step": "runPHP",
  "code": "<?php require_once '/wordpress/wp-load.php'; wp_insert_post([...]);"
}
```

#### 4. Networking Required
**Problem:** Can't install plugins from wordpress.org.

**Solution:** Enable networking:
```json
{
  "features": {
    "networking": true
  }
}
```

#### 5. File Paths
**Problem:** Files not found or created in wrong location.

**Solution:** Use absolute paths starting with `/wordpress/`:
- Plugins: `/wordpress/wp-content/plugins/`
- Themes: `/wordpress/wp-content/themes/`
- Uploads: `/wordpress/wp-content/uploads/`
- MU-Plugins: `/wordpress/wp-content/mu-plugins/`

### Debugging Tools

#### Use error_log in runPHP
```json
{
  "step": "runPHP",
  "code": "<?php error_log('Debug message: ' . print_r($data, true));"
}
```

View logs via Playground menu: Options > View Logs

#### Test Incrementally
Build blueprints step by step, testing after each addition.

#### Validate JSON
Use the schema for validation:
```json
{
  "$schema": "https://playground.wordpress.net/blueprint-schema.json"
}
```

## Loading Blueprints

### 1. URL Fragment (for small blueprints)
```
https://playground.wordpress.net/#{"preferredVersions":{"php":"8.3","wp":"latest"}}
```

### 2. Base64 Encoded (for GitHub compatibility)
```
https://playground.wordpress.net/#eyJwcmVmZXJyZWRWZXJzaW9ucyI6eyJwaHAiOiI4LjMiLCJ3cCI6ImxhdGVzdCJ9fQ==
```

### 3. Blueprint URL (for large blueprints)
```
https://playground.wordpress.net/?blueprint-url=https://example.com/blueprint.json
```

Must serve with CORS header:
```
Access-Control-Allow-Origin: *
```

### 4. Blueprint Bundle URL (for bundles)
```
https://playground.wordpress.net/?blueprint-url=https://example.com/my-bundle.zip
```

## Advanced Blueprint Features

### Multisite Setup
```json
{
  "steps": [
    {
      "step": "enableMultisite"
    }
  ]
}
```

### Custom WordPress Build
```json
{
  "preferredVersions": {
    "wp": "https://playground.wordpress.net/plugin-proxy.php?build-ref=trunk",
    "php": "8.3"
  }
}
```

### Git Repository Integration
```json
{
  "step": "installPlugin",
  "pluginData": {
    "resource": "git:directory",
    "url": "https://github.com/WordPress/block-development-examples",
    "ref": "HEAD",
    "path": "plugins/data-basics-59c8f8"
  }
}
```

## WP-CLI Integration

WP-CLI is a command-line interface for WordPress that enables powerful automation and management tasks. Use WP-CLI both in blueprints and directly for WordPress/WooCommerce operations.

### Enabling WP-CLI in Blueprints

To use WP-CLI commands in blueprints, load the wp-cli library:

```json
{
  "$schema": "https://playground.wordpress.net/blueprint-schema.json",
  "extraLibraries": ["wp-cli"],
  "steps": [
    {
      "step": "wp-cli",
      "command": "plugin list --status=active"
    }
  ]
}
```

### Essential WP-CLI Commands

#### Core WordPress Management
```bash
# Download WordPress
wp core download

# Install WordPress
wp core install --url=example.com --title="Site Title" --admin_user=admin --admin_password=pass --admin_email=admin@example.com

# Update WordPress
wp core update
```

#### Plugin Management
```bash
# List plugins
wp plugin list
wp plugin list --status=active --format=json

# Install and activate
wp plugin install akismet --activate
wp plugin install woocommerce --activate

# Update all plugins
wp plugin update --all
```

#### Theme Management
```bash
# List themes
wp theme list

# Install and activate
wp theme install twentytwentyfour --activate

# Update themes
wp theme update --all
```

#### Database Operations
```bash
# Create database
wp db create

# Export database
wp db export backup.sql

# Search and replace
wp search-replace 'http://oldsite.com' 'https://newsite.com'
wp search-replace 'old' 'new' --dry-run
```

#### User Management
```bash
# Create user
wp user create bob bob@example.com --role=author

# List users
wp user list --role=administrator

# Update password
wp user update 1 --user_pass=newpassword
```

#### Site Options
```bash
# Get option
wp option get blogname

# Update option
wp option update blogname "My New Site"
```

### WooCommerce CLI Commands

All WooCommerce commands require `--user=<id>` parameter for authentication.

#### Product Management
```bash
# List products
wp wc product list --user=1
wp wc product list --user=1 --status=publish --format=json

# Create product
wp wc product create --user=1 \
  --name="T-Shirt" \
  --type=simple \
  --regular_price=19.99 \
  --sku=TSHIRT001

# Update product
wp wc product update 123 --user=1 --regular_price=24.99

# Delete product
wp wc product delete 123 --user=1 --force
```

#### Customer Management
```bash
# Create customer
wp wc customer create --user=1 \
  --email=customer@example.com \
  --first_name=John \
  --last_name=Doe \
  --username=johndoe \
  --password=securepass

# List customers
wp wc customer list --user=1 --format=json

# Update customer
wp wc customer update 17 --user=1 --email=newemail@example.com
```

#### Order Management
```bash
# List orders
wp wc shop_order list --user=1
wp wc shop_order list --user=1 --status=processing

# Update order status
wp wc shop_order update 355 --user=1 --status=completed

# Add order note
wp wc order_note create 355 --user=1 \
  --note="Package shipped" \
  --customer_note=true
```

#### Coupon Management
```bash
# Create coupon
wp wc shop_coupon create --user=1 \
  --code=SUMMER20 \
  --discount_type=percent \
  --amount=20 \
  --description="Summer sale"

# Update coupon
wp wc shop_coupon update 45 --user=1 --amount=25

# List coupons
wp wc shop_coupon list --user=1
```

### Using WP-CLI in Blueprints

#### Basic WP-CLI Step
```json
{
  "step": "wp-cli",
  "command": "plugin list --status=active"
}
```

#### Complex Blueprint with WP-CLI
```json
{
  "$schema": "https://playground.wordpress.net/blueprint-schema.json",
  "extraLibraries": ["wp-cli"],
  "features": {
    "networking": true
  },
  "steps": [
    {
      "step": "installPlugin",
      "pluginData": {
        "resource": "wordpress.org/plugins",
        "slug": "woocommerce"
      },
      "options": {
        "activate": true
      }
    },
    {
      "step": "wp-cli",
      "command": "wc product create --user=1 --name='Demo Product' --type=simple --regular_price=29.99"
    },
    {
      "step": "wp-cli",
      "command": "wc product_cat create --user=1 --name='Electronics'"
    },
    {
      "step": "wp-cli",
      "command": "wc shop_coupon create --user=1 --code=WELCOME10 --discount_type=percent --amount=10"
    }
  ]
}
```

#### Automating Site Setup
```json
{
  "extraLibraries": ["wp-cli"],
  "steps": [
    {
      "step": "wp-cli",
      "command": "option update blogname 'My Awesome Store'"
    },
    {
      "step": "wp-cli",
      "command": "option update blogdescription 'Best products online'"
    },
    {
      "step": "wp-cli",
      "command": "plugin install woocommerce --activate"
    },
    {
      "step": "wp-cli",
      "command": "theme install storefront --activate"
    }
  ]
}
```

### WP-CLI Output Formats

All WP-CLI commands support multiple output formats:

```bash
--format=table   # Default table view
--format=json    # JSON output
--format=csv     # CSV output
--format=yaml    # YAML output
--format=ids     # Space-separated IDs
--format=count   # Count only
```

### Common WP-CLI Workflows

#### Fresh WordPress Install
```bash
wp core download
wp config create --dbname=wpdb --dbuser=root --dbpass=password
wp db create
wp core install --url=localhost --title="My Site" --admin_user=admin --admin_email=admin@example.com
```

#### Site Migration
```bash
wp db export backup.sql
wp search-replace 'http://oldsite.com' 'https://newsite.com' --dry-run
wp search-replace 'http://oldsite.com' 'https://newsite.com'
wp cache flush
```

#### Bulk Operations
```bash
wp plugin update --all
wp theme update --all
wp media regenerate --yes
```

### WP-CLI Troubleshooting

#### Database Connection Issues
- Ensure SQLite integration is installed in Playground: `"plugins": ["sqlite-database-integration"]`
- For traditional WordPress, verify wp-config.php credentials

#### Permission Issues
- Always run as appropriate user (not root)
- Use `--user=<id>` for WooCommerce commands

#### Path Issues
- Use `--path` to specify WordPress directory
- In Playground, paths start with `/wordpress/`

### Reference Files for Detailed Commands

For comprehensive command references, see:

- **references/wp-cli-commands.md** - Complete WP-CLI command reference with examples
- **references/woocommerce-cli-commands.md** - WooCommerce CLI commands and workflows
- **references/wp-cli-troubleshooting.md** - Common issues and solutions

Read these references when you need:
- Detailed syntax for specific commands
- Advanced usage patterns
- Troubleshooting specific errors
- Complete list of available options

### Global WP-CLI Parameters

These work with all commands:

- `--path=<path>` - Path to WordPress installation
- `--url=<url>` - URL for multisite subsites
- `--user=<id>` - Run as specific user (required for WooCommerce)
- `--skip-plugins` - Skip loading plugins
- `--skip-themes` - Skip loading themes
- `--quiet` - Suppress output
- `--debug` - Show debugging output

### Best Practices for WP-CLI

1. **Test with --dry-run** when available (e.g., search-replace)
2. **Backup before major operations** (`wp db export`)
3. **Use --format=json** for scripting and automation
4. **Check command help** (`wp help <command>`)
5. **Enable debugging** (`wp --debug <command>`)
6. **Use appropriate user context** (`--user=1` for WooCommerce)
7. **Verify environment** (`wp --info`)

## Schema Validation

When building blueprints:

1. **Always start with the schema reference**
2. **Validate all property names** against the schema
3. **Check required properties** for each step type
4. **Use correct value types** (string, boolean, number, object, array)
5. **Follow enum constraints** (e.g., PHP versions, HTTP methods)
6. **Use proper resource references** with correct `resource` property values

## Final Checklist

Before finalizing a blueprint:

- [ ] Includes `$schema` reference
- [ ] All step types are valid
- [ ] Required properties present for each step
- [ ] Resource references use correct format
- [ ] File paths are absolute and start with `/wordpress/`
- [ ] `runPHP` steps include `require_once '/wordpress/wp-load.php'`
- [ ] `networking` enabled if needed
- [ ] Landing page is appropriate
- [ ] Progress captions added for long operations (optional)
- [ ] Metadata included for gallery submissions (if applicable)
- [ ] JSON is valid and properly formatted

## Examples Summary

Common blueprint types:
1. **Plugin Demo**: Install and showcase a plugin
2. **Theme Demo**: Install theme with sample content
3. **Development Environment**: Debug tools and constants
4. **Custom Code**: MU-plugins or custom functions
5. **WP-CLI Automation**: Scripted setup via CLI
6. **Content Import**: WXR file with posts/pages
7. **Multi-plugin Setup**: Multiple plugins with configuration
8. **Complete Site**: Theme + plugins + content + settings

## Additional Resources

- Schema: https://playground.wordpress.net/blueprint-schema.json
- Gallery: https://github.com/WordPress/blueprints/blob/trunk/GALLERY.md
- Documentation: https://wordpress.github.io/wordpress-playground/blueprints
- Builder Tool: https://playground.wordpress.net/builder/builder.html
- Step Library: https://akirk.github.io/playground-step-library/

---

## Quick Reference: Step Types

| Step | Purpose |
|------|---------|
| `activatePlugin` | Activate an installed plugin |
| `activateTheme` | Activate an installed theme |
| `cp` | Copy file/directory |
| `defineWpConfigConsts` | Define WordPress constants |
| `defineSiteUrl` | Set site URL |
| `enableMultisite` | Enable multisite |
| `importWxr` | Import WXR content |
| `importThemeStarterContent` | Import theme starter content |
| `importWordPressFiles` | Import WordPress files from zip |
| `installPlugin` | Install a plugin |
| `installTheme` | Install a theme |
| `login` | Log in as user |
| `mkdir` | Create directory |
| `mv` | Move/rename file/directory |
| `request` | Make HTTP request |
| `resetData` | Reset database |
| `rm` | Remove file |
| `rmdir` | Remove directory |
| `runPHP` | Execute PHP code |
| `runPHPWithOptions` | Execute PHP with options |
| `runSql` | Execute SQL queries |
| `runWpInstallationWizard` | Run WP installer |
| `setSiteOptions` | Set site options |
| `setSiteLanguage` | Set site language |
| `unzip` | Extract zip file |
| `updateUserMeta` | Update user metadata |
| `wp-cli` | Execute WP-CLI command |
| `writeFile` | Write single file |
| `writeFiles` | Write multiple files |

## When to Use Each Resource Type

- `"wordpress.org/plugins"` - Official WordPress.org plugins
- `"wordpress.org/themes"` - Official WordPress.org themes  
- `"url"` - Remote files via HTTPS
- `"git:directory"` - Git repositories or subdirectories
- `"bundled"` - Files included in blueprint bundle
- `"vfs"` - Files in virtual filesystem
- `"literal"` - Inline content

---

This skill provides comprehensive guidance for building WordPress Playground Blueprints that strictly conform to the official schema. Always validate against the schema and test blueprints incrementally.
