---
name: wp-playground
description: Test code with WordPress by starting a WordPress server. Use when testing changes to a WordPress plugin, a WordPress theme, WordPress source code, verifying WordPress behavior, or needing a running WordPress instance to validate work
license: GPL-2.0-or-later
user-invocable: true
---

# WordPress Playground

Run a local WordPress instance with your plugin, theme, wp-content directory, or whole WordPress directory mounted for testing.

**Requires:** Node.js 20.18+

## Quick Start

Use the helper scripts in `scripts/` relative to this skill's base directory:

```bash
# Start server and get PID + URL
./scripts/start-server.sh --login --auto-mount /path/to/plugin
# Output on success:
#   pid:12345
#   url:http://127.0.0.1:9400

# Stop server by PID
./scripts/stop-server.sh 12345
# Output: stopped:12345
```

| Flag | Purpose |
|------|---------|
| `--login` | Auto-login to wp-admin (required for Playwright) |
| `--auto-mount <path>` | Auto-detect and mount (see Path Detection) |
| `--port N` | Use custom port (default: 9400) |
| `--blueprint <path>` | Optional Blueprint JSON to run |

Run `npx @wp-playground/cli server --help` to print usage documentation for all options.

## Path Detection

`--auto-mount` detects path type by file signatures:

| Type | Detection Rule |
|------|----------------|
| Plugin | PHP file with `Plugin Name:` header |
| Theme | `style.css` with `Theme Name:` header |
| wp-content | Directory named `wp-content` |
| WordPress | Contains `wp-includes/` directory |

The principle: detection looks for WordPress-standard markers.

## Workflow

### Using Helper Scripts (Recommended)

1. Start server with `start-server.sh` - it waits for ready and returns PID + URL
2. Parse the output to get the URL
3. Navigate and interact via Playwright MCP tools
4. Stop server with `stop-server.sh <pid>` when done

```bash
# From skill base directory
result=$(./scripts/start-server.sh --login --auto-mount /path/to/plugin)
pid=$(echo "$result" | grep '^pid:' | cut -d: -f2)
url=$(echo "$result" | grep '^url:' | cut -d: -f2)
# Use $url for Playwright, then:
./scripts/stop-server.sh "$pid"
```

### When tests require logging into WordPress, enable auto-login by including the --login flag

<example type="CORRECT">
./scripts/start-server.sh --login --auto-mount /path/to/plugin
# Playwright can access /wp-admin/ immediately
</example>

<example type="INCORRECT">
./scripts/start-server.sh --auto-mount /path/to/plugin
# Playwright blocked by login screen at /wp-admin/
</example>

### When testing WordPress while logged out, omit the --login flag so auto-login is not enabled

<example type="CORRECT">
./scripts/start-server.sh --auto-mount /path/to/plugin
# Playwright can access /wp-admin/ immediately
</example>

<example type="INCORRECT">
./scripts/start-server.sh --login --auto-mount /path/to/plugin
# Playwright blocked by login screen at /wp-admin/
</example>

## Troubleshooting

**Recoverable errors** (retry automatically):

| Error | Action |
|-------|--------|
| `EADDRINUSE` / port in use | Use `--port <port>` to choose a subsequent port that is not in use |
| No ready signal in 60s | Read task output for errors, retry once |

**Configuration errors** (verify setup):

| Error | Action |
|-------|--------|
| Plugin not in admin list | Verify path contains PHP file with `Plugin Name:` header |
| Playwright tools unavailable | Ask user to install Playwright MCP server |
