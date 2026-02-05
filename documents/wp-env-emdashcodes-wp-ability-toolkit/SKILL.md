---
name: wp-env
description: Local WordPress development environment management using @wordpress/env for plugin and theme development. Use this skill when setting up, configuring, starting, stopping, or managing wp-env Docker-based WordPress environments.
---

# wp-env - WordPress Local Development Environment

This skill provides assistance for working with `wp-env`, a tool that sets up local WordPress development environments using Docker with minimal configuration.

## About wp-env

`wp-env` (`@wordpress/env`) creates Docker-based WordPress environments for plugin and theme development. It provides:

- **Zero-config setup** - Works out of the box for plugins and themes
- **Dual environments** - Separate development (port 8888) and testing (port 8889) instances
- **Pre-configured tools** - Includes WP-CLI, Composer, PHPUnit, and Xdebug
- **Flexible configuration** - Customize via `.wp-env.json` for complex setups

**Default Access:**

- Development site: <http://localhost:8888>
- Testing site: <http://localhost:8889>
- Login: username `admin`, password `password`
- Database: user `root`, password `password`

## Prerequisites Check

Before working with wp-env, verify these dependencies are installed and running:

```bash
# Check Docker is installed and running
docker --version
docker ps

# Check Node.js and npm
node --version
npm --version

# Check if wp-env is installed
wp-env --version
```

**If Docker is not running:** Start Docker Desktop application first - wp-env cannot function without Docker.

**If wp-env is not installed:** Install globally with `npm -g install @wordpress/env`

## Common Workflows

### First-Time Environment Setup

When setting up wp-env for the first time in a plugin or theme directory:

```bash
# 1. Ensure Docker Desktop is running
docker ps

# 2. Install wp-env globally (if not already installed)
npm -g install @wordpress/env

# 3. Navigate to your plugin or theme directory
cd /path/to/your/plugin

# 4. Start the environment (downloads WordPress, sets up containers)
wp-env start

# 5. Access the site at http://localhost:8888
# Login with admin/password
```

wp-env will automatically detect if the current directory is a plugin or theme and mount it appropriately.

### Daily Development Operations

**Starting the environment:**

```bash
# Start with existing configuration
wp-env start

# Start and update WordPress/sources
wp-env start --update

# Start with Xdebug enabled for debugging
wp-env start --xdebug
```

**Stopping the environment:**

```bash
# Stop containers (preserves data)
wp-env stop
```

**Checking environment status:**

```bash
# View running containers
docker ps

# Should show: wordpress (8888), tests-wordpress (8889), mariadb (3306)
```

### Running WP-CLI Commands

Execute WordPress CLI commands inside the environment using `wp-env run`:

```bash
# List users on development instance
wp-env run cli wp user list

# Install a plugin
wp-env run cli wp plugin install contact-form-7 --activate

# Create a test post on the testing instance
wp-env run tests-cli wp post create --post_title="Test Post" --post_status=publish

# Update permalink structure (enables REST API access)
wp-env run cli "wp rewrite structure /%postname%/"

# Open WordPress shell for interactive PHP
wp-env run cli wp shell
```

**Environment types:**

- `cli` / `wordpress` - Development environment (shares database with port 8888)
- `tests-cli` / `tests-wordpress` - Testing environment (separate database, port 8889)

**Working directory context:**
By default, commands run from WordPress root. For plugin-specific commands, use `--env-cwd`:

```bash
# Run composer install in your plugin directory
wp-env run cli --env-cwd=wp-content/plugins/your-plugin composer install

# Run PHPUnit tests in your plugin
wp-env run tests-cli --env-cwd=wp-content/plugins/your-plugin phpunit
```

### Database Reset for Testing

Reset the database to clean state:

```bash
# Reset only the tests database (default)
wp-env clean

# Reset development database
wp-env clean development

# Reset both databases
wp-env clean all
```

⚠️ **Warning:** This permanently deletes all posts, pages, media, and custom data.

### Viewing Logs

Monitor PHP errors and Docker container logs:

```bash
# View development environment logs (follows/watches by default)
wp-env logs

# View testing environment logs
wp-env logs tests

# View both environments
wp-env logs all

# Disable following/watching
wp-env logs --watch=false
```

### Working with Ports

If the default port 8888 conflicts with another service:

```bash
# Using environment variables
WP_ENV_PORT=3333 wp-env start

# Check which ports are in use
docker ps
```

Or configure ports in `.wp-env.json`:

```json
{
  "port": 3333,
  "testsPort": 3334
}
```

Note: Environment variables take precedence over `.wp-env.json` values.

## Quick Reference - Essential Commands

| Command                            | Description                                   |
| ---------------------------------- | --------------------------------------------- |
| `wp-env start`                     | Start the environment                         |
| `wp-env start --update`            | Start and update WordPress/sources            |
| `wp-env stop`                      | Stop the environment                          |
| `wp-env clean [env]`               | Reset database (env: tests, development, all) |
| `wp-env destroy`                   | Completely remove containers and data         |
| `wp-env logs [env]`                | View logs (env: development, tests, all)      |
| `wp-env run <container> <command>` | Execute command in container                  |
| `wp-env install-path`              | Show where environment files are stored       |
| `docker ps`                        | Check which containers are running            |

**Common containers for `wp-env run`:**

- `cli` - WP-CLI, Composer, PHPUnit (development)
- `tests-cli` - WP-CLI, Composer, PHPUnit (testing)
- `wordpress` - WordPress PHP environment (development)
- `tests-wordpress` - WordPress PHP environment (testing)

## Configuration with .wp-env.json

Create a `.wp-env.json` file in your project root to customize the environment.

### Common Configuration Patterns

**Basic plugin development:**

```json
{
  "plugins": ["."]
}
```

**Custom WordPress version:**

```json
{
  "core": "WordPress/WordPress#6.4.0",
  "plugins": ["."]
}
```

**Multi-plugin setup:**

```json
{
  "plugins": [".", "WordPress/classic-editor", "../another-plugin"]
}
```

For complete configuration reference with 20+ examples, environment-specific overrides, custom mappings, multisite setup, and lifecycle scripts, see [references/configuration-guide.md](references/configuration-guide.md).

## When Things Go Wrong

### Common Errors

**Error: "Error while running docker-compose command"**

- Check that Docker Desktop is started and running
- Check Docker Desktop dashboard for logs, restart, or remove existing virtual machines
- Then try rerunning `wp-env start`

**Error: "Host is already in use by another container"**

- The container you are attempting to start is already running, or another container is. You can stop an existing container by running `wp-env stop` from the directory that you started it in
- If you do not remember the directory where you started `wp-env`, you can stop all containers by running `docker stop $(docker ps -q)`. This will stop all Docker containers, so use with caution
- Then try rerunning `wp-env start`

For comprehensive troubleshooting including Ubuntu Docker setup, database issues, and advanced debugging, see [references/troubleshooting.md](references/troubleshooting.md).

## Advanced Features

For detailed information on these features, see [references/command-reference.md](references/command-reference.md).

**Xdebug:** Enable step debugging with `wp-env start --xdebug`. Configure your IDE for port 9003.

**PHPUnit:** WordPress test files included. Run with `wp-env run tests-cli --env-cwd=wp-content/plugins/your-plugin phpunit`.

**Composer:** Execute commands with `wp-env run cli --env-cwd=wp-content/plugins/your-plugin composer install`.

## Best Practices

### Directory Context

- Run `wp-env start` from your plugin or theme directory for automatic mounting
- Use `--env-cwd` when running commands that need to execute in specific directories
- Use absolute paths when possible to avoid confusion

### Development Workflow

1. Start environment once per work session: `wp-env start`
2. Make code changes - they're immediately reflected (no rebuild needed)
3. Use `wp-env run cli wp` commands for WordPress operations
4. Check logs when debugging: `wp-env logs`
5. Stop when done: `wp-env stop`

### Testing Workflow

1. Use `tests-cli` and `tests-wordpress` for isolated testing
2. Reset test database frequently: `wp-env clean tests`
3. Keep test and development environments separate
4. Use `wp-env clean all` before running full integration tests

### Configuration Management

- Keep `.wp-env.json` in version control for team consistency
- Use `.wp-env.override.json` (gitignored) for local-only overrides
- Document custom configurations in project README

## Where Files Are Stored

wp-env stores files in a home directory (defaults vary by platform):

```bash
# Get the install path for current project
wp-env install-path

# Default locations:
# macOS/Windows: ~/.wp-env/$md5_of_project_path
# Linux: ~/wp-env/$md5_of_project_path
```

Override with `WP_ENV_HOME` environment variable:

```bash
WP_ENV_HOME="./local-wp-env" wp-env start
```

## Additional Resources

- **Command Reference:** [references/command-reference.md](references/command-reference.md) - Complete CLI documentation
- **Configuration Guide:** [references/configuration-guide.md](references/configuration-guide.md) - All `.wp-env.json` options
- **Troubleshooting:** [references/troubleshooting.md](references/troubleshooting.md) - Common issues and solutions

External documentation:

- [@wordpress/env npm package](https://www.npmjs.com/package/@wordpress/env)
- [WordPress Developer Handbook - wp-env](https://developer.wordpress.org/block-editor/getting-started/devenv/get-started-with-wp-env/)
- [Docker Desktop](https://docs.docker.com/desktop/)
