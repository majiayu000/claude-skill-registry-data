---
name: wordpress-plugin-scaffold
description: Scaffold WordPress plugins using WP-CLI commands (wp scaffold plugin, wp scaffold plugin-tests). Use this skill when creating new WordPress plugins or adding test infrastructure to existing plugins.
---

# WordPress Plugin Scaffold

This skill provides guidance for scaffolding WordPress plugins using WP-CLI's scaffold commands. It supports both creating new plugins from scratch and adding test infrastructure to existing plugins.

**Note:** This skill works seamlessly with the **wp-env skill (if available)**. When wp-env setup or management is needed, activate the wp-env skill for comprehensive environment handling.

## About WP-CLI Scaffold Commands

WP-CLI provides two primary scaffolding commands for plugin development:

### wp scaffold plugin

Generates starter code for a new plugin, including:

- Main plugin PHP file
- `readme.txt` for WordPress.org
- `package.json` with Grunt tasks for i18n and readme conversion
- Editor configuration files (`.editorconfig`, `.gitignore`, `.distignore`)
- Optional: PHPUnit test suite, CI configuration, and PHP_CodeSniffer rules

### wp scaffold plugin-tests

Adds PHPUnit test infrastructure to an existing plugin, including:

- `phpunit.xml.dist` configuration
- CI configuration (CircleCI, GitHub Actions, GitLab, Bitbucket)
- `bin/install-wp-tests.sh` for WordPress test suite setup
- `tests/bootstrap.php` to activate the plugin during tests
- `tests/test-sample.php` with example test cases
- `.phpcs.xml.dist` for PHP_CodeSniffer rules

## Prerequisites

Verify WP-CLI is installed and accessible:

```bash
wp --version
```

If WP-CLI is not installed, see [references/wp-cli-installation.md](references/wp-cli-installation.md) for comprehensive installation instructions across all platforms.

## Environment Detection

**IMPORTANT:** Before running any scaffold commands, detect which WordPress environment is available:

### Detection Strategy

1. **Check for existing WordPress installation** (preferred):

   ```bash
   wp core version 2>/dev/null
   ```

   - If successful → Use `wp scaffold plugin` directly
   - You're already in a WordPress installation, no additional setup needed

2. **Check for wp-env configuration**:

   ```bash
   # Look for wp-env config files
   [ -f .wp-env.json ] || [ -f .wp-env.override.json ]
   ```

   - If found → Check if wp-env is running
   - If running → Use `wp-env run cli wp scaffold plugin`
   - If not running → **Activate the wp-env skill (if available)** to start the environment

3. **Check for wp-env availability** (fallback):

   ```bash
   wp-env --version 2>/dev/null
   ```

   - If available → Ask user if they want to use wp-env
   - **Activate the wp-env skill (if available)** for environment setup and management

4. **No environment available** (error):
   - Inform user they need either:
     - A WordPress installation with `--path` flag
     - wp-env setup (see wp-env skill if available)

### Command Prefix Selection

Based on detection, use the appropriate command prefix throughout this skill:

- **In WordPress installation:** `wp scaffold plugin`
- **Using wp-env:** `wp-env run cli wp scaffold plugin`

All examples below show the base command. Prepend `wp-env run cli` when using wp-env.

## Workflow: Creating a New Plugin

When creating a new WordPress plugin, follow this interactive workflow:

### 1. Gather Plugin Metadata

Collect the following information from the user, offering smart defaults:

- **Plugin slug** (required) - Internal name, lowercase with hyphens
  - Default: Infer from current directory name or user's request

- **Plugin name** - Display name for the plugin header
  - Default: Title-case version of slug

- **Plugin description** - What the plugin does
  - Default: Ask user to provide

- **Plugin author** - Author name
  - Default: Use `git config user.name` if available

- **Plugin author URI** - Author website URL
  - Default: Use `git config user.url` if available, otherwise skip

- **Plugin URI** - Plugin project URL
  - Default: Skip unless user provides

### 2. Determine Additional Options

Ask the user about these options:

- **Include tests?** - Whether to generate PHPUnit test files
  - Default: Yes (recommended for all plugins)
  - Use `--skip-tests` flag to omit

- **CI provider** - Which continuous integration service to use
  - Options: `circle` (default), `github`, `gitlab`, `bitbucket`
  - Use `--ci=<provider>` flag

- **Target directory** - Where to create the plugin
  - Default: Current working directory
  - Use `--dir=<path>` to specify custom location

### 3. Construct and Execute Command

Build the `wp scaffold plugin` command with gathered information:

```bash
wp scaffold plugin <slug> \
  --plugin_name="<name>" \
  --plugin_description="<description>" \
  --plugin_author="<author>" \
  --plugin_author_uri="<author-uri>" \
  --plugin_uri="<plugin-uri>" \
  --ci=<provider>
```

Add `--skip-tests` if user declined test files.
Add `--dir=<path>` if custom directory specified.

### 4. Post-Scaffold Actions

After successfully scaffolding the plugin:

1. **Verify creation** - Confirm files were generated:

   ```bash
   ls -la <plugin-directory>
   ```

2. **Ask about activation** - If wp-env is running, offer to activate:
   - "Would you like me to activate this plugin in your wp-env environment?"
   - If yes, run: `wp-env run cli wp plugin activate <slug>`
   - For network activation: `wp-env run cli wp plugin activate <slug> --network`

3. **Next steps guidance** - Inform user about:
   - Main plugin file location: `<slug>/<slug>.php`
   - How to run tests if included: `wp-env run tests-cli --env-cwd=wp-content/plugins/<slug> phpunit`
   - NPM scripts available: `npm run readme`, `npm run i18n`

## Workflow: Adding Tests to Existing Plugin

When adding test infrastructure to an existing plugin:

### 1. Identify Plugin

Determine which plugin needs tests:

- **Plugin slug** - The plugin directory name
- **Plugin directory** - Path to the plugin (use `--dir` if non-standard)

### 2. Determine CI Provider

Ask which CI service the user wants:

- Options: `circle` (default), `github`, `gitlab`, `bitbucket`

### 3. Execute Command

Run the scaffold plugin-tests command:

```bash
# Standard plugin location
wp scaffold plugin-tests <plugin-slug> --ci=<provider>

# Non-standard location
wp scaffold plugin-tests --dir=<path/to/plugin> --ci=<provider>
```

Add `--force` flag to overwrite existing test files if needed.

### 4. Post-Scaffold Actions

After generating test files:

1. **Set up test environment** - Guide user through test setup:

   ```bash
   # Install WordPress test suite (if not using wp-env)
   bash bin/install-wp-tests.sh wordpress_test root password localhost latest

   # Or use wp-env for testing
   wp-env run tests-cli --env-cwd=wp-content/plugins/<slug> phpunit
   ```

2. **Verify test execution** - Run the sample test:

   ```bash
   wp-env run tests-cli --env-cwd=wp-content/plugins/<slug> phpunit
   ```

3. **Next steps** - Inform user about:
   - Writing additional tests in `tests/` directory
   - Running specific test files or test cases
   - CI/CD integration based on chosen provider

## Common Options Reference

| Option               | Description                                          | Example              |
| -------------------- | ---------------------------------------------------- | -------------------- |
| `--skip-tests`       | Don't generate PHPUnit test files                    | `--skip-tests`       |
| `--ci=<provider>`    | CI configuration (circle, github, gitlab, bitbucket) | `--ci=github`        |
| `--activate`         | Activate plugin after creation                       | `--activate`         |
| `--activate-network` | Network activate plugin after creation               | `--activate-network` |
| `--force`            | Overwrite existing files                             | `--force`            |
| `--dir=<path>`       | Custom directory for plugin                          | `--dir=/custom/path` |

**Note:** `--activate` and `--activate-network` flags work with local wp-cli WordPress installations but not with wp-env. For wp-env, use `wp-env run cli wp plugin activate` instead.

## Best Practices

### Plugin Naming

- Use lowercase letters, numbers, and hyphens only
- Be descriptive but concise
- Follow WordPress plugin naming conventions
- Examples: `my-contact-form`, `analytics-dashboard`, `custom-post-types`

### When to Skip Tests

Skip tests (`--skip-tests`) only when:

- Creating a quick prototype or proof-of-concept
- Building a personal plugin that won't be distributed
- Planning to add tests later with `wp scaffold plugin-tests`

**Always include tests for:**

- Plugins intended for public distribution
- Team projects with multiple contributors
- Plugins with complex business logic
- Any production-ready code

### CI Provider Selection

Choose a CI provider based on your repository host:

- **GitHub repositories** → `--ci=github` (GitHub Actions)
- **GitLab repositories** → `--ci=gitlab` (GitLab CI)
- **Bitbucket repositories** → `--ci=bitbucket` (Bitbucket Pipelines)
- **Other/unknown** → `--ci=circle` (CircleCI)

### Working with wp-env

When developing with wp-env:

1. **Scaffold inside wp-env directory structure:**

   ```bash
   # Create plugin in wp-env's plugin directory
   cd /path/to/wp-env-project
   wp scaffold plugin my-plugin --dir=plugins/
   ```

2. **Or scaffold separately and configure .wp-env.json:**

   ```json
   {
     "plugins": [".", "../other-plugin"]
   }
   ```

3. **Activate after scaffolding:**

   ```bash
   wp-env run cli wp plugin activate my-plugin
   ```

4. **Run tests in wp-env:**

   ```bash
   wp-env run tests-cli --env-cwd=wp-content/plugins/my-plugin phpunit
   ```

## Example Interactions

### Creating a New Plugin

**User:** "Create a new WordPress plugin called 'site-analytics' for tracking visitor analytics"

**Process:**

1. Gather metadata (use smart defaults from git config)
2. Ask about tests (default: yes) and CI provider (default: github)
3. Execute: `wp scaffold plugin site-analytics --plugin_name="Site Analytics" --plugin_description="Track visitor analytics and generate reports" --plugin_author="Em" --ci=github`
4. Ask: "Would you like me to activate this plugin in wp-env?"

### Adding Tests to Existing Plugin

**User:** "Add tests to my existing 'custom-widgets' plugin"

**Process:**

1. Identify plugin location
2. Ask about CI provider
3. Execute: `wp scaffold plugin-tests custom-widgets --ci=github`
4. Guide user through running tests with wp-env

## Additional Resources

- [WP-CLI Scaffold Plugin Documentation](https://developer.wordpress.org/cli/commands/scaffold/plugin/)
- [WP-CLI Scaffold Plugin Tests Documentation](https://developer.wordpress.org/cli/commands/scaffold/plugin-tests/)
- [Plugin Unit Tests Handbook](https://make.wordpress.org/cli/handbook/misc/plugin-unit-tests/)
- [WordPress Plugin Handbook](https://developer.wordpress.org/plugins/)
