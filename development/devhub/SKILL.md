---
name: devhub
description: Generate devhub.toml configuration files and manage multi-project development environments. Use when setting up projects, creating service configs, starting/stopping services, checking status, or managing development workflows. Triggers on mentions of devhub, project setup, service management, or development environment configuration.
---

# DevHub Skill

DevHub is a multi-project development environment manager that lets you start, stop, and monitor all your local development services from one place.

## When to Use This Skill

Use DevHub when the user wants to:
- Set up a new project for local development
- Generate a `devhub.toml` configuration file
- Start, stop, or restart development services
- Check the status of running services
- Manage multiple projects or services
- View logs from services
- Manage favorite projects

## Primary Workflow: Setting Up a New Project

### Step 1: Preview Discovery (Always Do This First)

```bash
devhub discover --dry-run
```

This shows what DevHub would detect without writing any files. Review the output with the user before proceeding.

### Step 2: Generate Configuration

If the preview looks correct:

```bash
devhub discover
```

This creates `devhub.toml` in the project root.

### Step 3: Register the Project

```bash
devhub register
```

This adds the project to DevHub's registry so it can be managed globally.

### Step 4: Start Services

```bash
devhub start
```

Or start a specific service:

```bash
devhub start -s api
```

## Key Commands Quick Reference

| Command | Purpose |
|---------|---------|
| `devhub discover --dry-run` | Preview auto-detection |
| `devhub discover` | Generate devhub.toml |
| `devhub register` | Add project to registry |
| `devhub start [project]` | Start all services |
| `devhub stop [project]` | Stop all services |
| `devhub status` | Show all project statuses |
| `devhub logs <project> -f` | Follow service logs |
| `devhub list` | List all registered projects |

## Supported Project Types

DevHub auto-detects these project types:

| Type | Detection File | Default Command |
|------|---------------|-----------------|
| Rust | `Cargo.toml` | `cargo run` |
| Node.js | `package.json` | `npm run dev` |
| Python (UV) | `pyproject.toml` | `uv run python` |
| Python (pip) | `requirements.txt` | `python` |
| Go | `go.mod` | `go run .` |
| Flutter | `pubspec.yaml` | `flutter run` |
| Docker | `docker-compose.yml` | `docker compose up` |

## Monorepo Support

When no root project marker is found, DevHub scans subdirectories and creates a multi-service configuration automatically.

## Additional Reference

For detailed information, see:
- [COMMANDS.md](COMMANDS.md) - Complete CLI reference
- [CONFIG-FORMAT.md](CONFIG-FORMAT.md) - devhub.toml specification
- [EXAMPLES.md](EXAMPLES.md) - Real-world configuration examples

## Best Practices

1. **Always preview first**: Run `devhub discover --dry-run` before generating config
2. **Review generated config**: Check the devhub.toml and adjust ports/commands if needed
3. **Use favorites**: Mark frequently-used projects with `devhub fav add <project>`
4. **Check for conflicts**: Run `devhub ports --check` to detect port conflicts
5. **Follow logs**: Use `devhub logs <project> -f` to monitor service output
