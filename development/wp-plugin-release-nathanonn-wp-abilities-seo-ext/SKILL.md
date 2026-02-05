---
name: wp-plugin-release
description: Generate README.md, build.sh, and GitHub release workflows for WordPress plugins. Activate when creating release infrastructure for a WordPress plugin, setting up distribution packaging, or creating GitHub Actions workflows for plugin releases. Works with any WordPress plugin structure.
---

# WordPress Plugin Release

## Overview

This skill generates release infrastructure for WordPress plugins: README.md documentation, build.sh packaging scripts, and GitHub Actions release workflows. It works with any WordPress plugin, with optional sections for WordPress Abilities API integrations.

## Workflow

### Step 1: Detect Plugin Metadata

Before generating files, extract metadata from the main plugin PHP file header:

```php
/**
 * Plugin Name: {{PLUGIN_NAME}}
 * Description: {{PLUGIN_DESCRIPTION}}
 * Version: {{VERSION}}
 * Requires at least: {{MIN_WP_VERSION}}
 * Requires PHP: {{MIN_PHP_VERSION}}
 * Author: {{AUTHOR}}
 * License: {{LICENSE}}
 * Text Domain: {{PLUGIN_SLUG}}
 */
```

Also identify:
- **PLUGIN_SLUG**: Directory name and text domain (e.g., `internal-links-api`)
- **MAIN_FILE**: Main PHP filename (e.g., `internal-links-api.php`)
- **NAMESPACE**: PHP namespace if using PSR-4 autoloading
- **VERSION_CONSTANT**: The constant name for version (e.g., `INTERNAL_LINKS_API_VERSION`)
- **HAS_COMPOSER**: Whether `composer.json` exists
- **HAS_SRC_DIR**: Whether `src/` directory exists for autoloading

### Step 2: Generate Requested Files

Use the templates in `assets/` as starting points, replacing placeholders with detected metadata.

## File Generation

### README.md

Use `assets/readme-template.md` as the base template.

**Core sections (always include):**
- Plugin name and description
- Requirements (WordPress version, PHP version, dependencies)
- Installation instructions
- License

**Optional sections (include based on plugin features):**
- MCP Setup Guide - Include for Abilities API plugins with MCP integration
- Available Abilities - Include for plugins registering WordPress Abilities
- Configuration - Include if plugin has settings page or filter hooks
- Usage Examples - Include with realistic examples for the plugin's features
- Troubleshooting - Include common issues and solutions
- Building for Distribution - Include when generating build.sh

When generating README.md:
1. Read the main plugin file to extract metadata
2. Analyze plugin structure to determine which optional sections apply
3. Replace all placeholders in the template
4. Remove section markers and unused optional sections
5. Add plugin-specific content for usage examples and troubleshooting

### build.sh

Use `assets/build-template.sh` as the base template.

The build script:
1. Extracts version from the main plugin file header
2. Creates a clean build directory
3. Copies necessary files (main file, src/, vendor/ after composer install, etc.)
4. Runs `composer install --no-dev --optimize-autoloader` if composer.json exists
5. Creates versioned and latest zip files in `dist/`

Customize the `FILES_TO_COPY` array based on plugin structure:
- Always include main PHP file
- Include `src/` if using PSR-4 autoloading
- Include `composer.json` and `composer.lock` if using Composer
- Include `README.md` for distribution
- Include any other essential directories (e.g., `includes/`, `assets/`, `templates/`)

### GitHub Release Workflow

Use `assets/release-workflow-template.yml` as the base template.

The workflow:
1. Triggers on version tags (`v*`)
2. Sets up PHP with Composer
3. Extracts version from tag name
4. Updates version in plugin file(s)
5. Runs build.sh
6. Creates GitHub Release with auto-generated notes
7. Attaches zip files to release

Customize version update commands based on:
- Main plugin file location
- Version constant naming pattern
- Any other files containing version numbers

## Placeholders Reference

| Placeholder | Description | Detection Method |
|-------------|-------------|-----------------|
| `{{PLUGIN_NAME}}` | Human-readable name | Plugin Name header |
| `{{PLUGIN_SLUG}}` | Directory/text-domain | Text Domain header or directory name |
| `{{PLUGIN_DESCRIPTION}}` | Plugin description | Description header |
| `{{MAIN_FILE}}` | Main PHP filename | Plugin file in root matching slug |
| `{{NAMESPACE}}` | PHP namespace | First `namespace` declaration |
| `{{VERSION_CONSTANT}}` | Version constant | Look for `define('*_VERSION'` pattern |
| `{{AUTHOR}}` | Plugin author | Author header |
| `{{LICENSE}}` | License type | License header |
| `{{MIN_WP_VERSION}}` | Minimum WP version | Requires at least header |
| `{{MIN_PHP_VERSION}}` | Minimum PHP version | Requires PHP header |
| `{{HAS_COMPOSER}}` | Uses Composer | Check for composer.json |
| `{{FILES_TO_COPY}}` | Files for distribution | Analyze plugin structure |

## Detecting Abilities API Plugins

A plugin uses WordPress Abilities API if it:
- Has a dependency on `WP_Abilities_Registry` class
- Hooks into `wp_abilities_api_init` or `wp_abilities_api_categories_init`
- Contains files in an `Abilities/` directory
- Has `Ability` classes that implement `execute()` method

When an Abilities API plugin is detected, include the MCP Setup Guide and Available Abilities sections in README.md.

## Resources

### assets/

- `readme-template.md` - README template with core and optional sections
- `build-template.sh` - Build script template with placeholders
- `release-workflow-template.yml` - GitHub Actions workflow template

### references/

- `wordpress-plugin-structure.md` - Reference for WordPress plugin standards and conventions
