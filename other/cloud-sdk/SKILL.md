---
version: "2.0.0"
name: Go Cloud
description: "The Go Cloud Development Kit (Go CDK): A library and tools for open cloud development in Go. go cloud, go, aws, azure, cloud, gcp."
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
---
# Cloud SDK

Developer workflow automation tool for project lifecycle management. Provides commands for initializing projects, running checks, building, testing, deploying, managing configuration, generating templates, producing documentation, and cleaning build artifacts — all from a single CLI interface.

## Commands

| Command | Description |
|---------|-------------|
| `cloud-sdk init` | Initialize a new project in the current working directory |
| `cloud-sdk check` | Run lint, type-check, and test passes against the project |
| `cloud-sdk build` | Build the project artifacts |
| `cloud-sdk test` | Execute the full test suite |
| `cloud-sdk deploy` | Show the deployment pipeline guide (build → test → stage → prod) |
| `cloud-sdk config` | Display or manage project configuration (`config.json`) |
| `cloud-sdk status` | Check overall project health and status |
| `cloud-sdk template <name>` | Generate a code template for the given component name |
| `cloud-sdk docs` | Generate project documentation |
| `cloud-sdk clean` | Remove build artifacts and temporary files |
| `cloud-sdk help` | Show the built-in help message with all commands |
| `cloud-sdk version` | Print the current version (v2.0.0) |

## Data Storage

All operational data is stored in `~/.local/share/cloud-sdk/` by default. You can override this by setting the `CLOUD_SDK_DIR` environment variable. Key files inside the data directory:

- `history.log` — timestamped log of every command executed
- `config.json` — project-level configuration (managed via `config` command)

The tool respects `XDG_DATA_HOME` if set, falling back to `$HOME/.local/share`.

## Requirements

- **Bash** 4.0+ (uses `set -euo pipefail` for strict error handling)
- **coreutils** (standard `date`, `mkdir`, `echo`)
- No external dependencies or API keys required
- Works on Linux and macOS out of the box

## When to Use

1. **Bootstrapping a new project** — run `cloud-sdk init` to set up project scaffolding quickly from the terminal without remembering per-tool init commands
2. **Pre-commit quality gates** — use `cloud-sdk check` as part of a Git pre-commit hook to run lint + type-check + tests before every commit
3. **CI/CD pipeline steps** — chain `cloud-sdk build` and `cloud-sdk test` inside your continuous integration scripts for a consistent, tool-agnostic interface
4. **Deployment checklists** — run `cloud-sdk deploy` to get a guided walkthrough of the build → test → stage → prod pipeline so nothing gets skipped
5. **Housekeeping and cleanup** — execute `cloud-sdk clean` to wipe build artifacts after releases, freeing disk space and resetting state

## Examples

```bash
# Initialize a new project in the current directory
cloud-sdk init

# Run all quality checks (lint + type-check + tests)
cloud-sdk check

# Build the project
cloud-sdk build

# Run the test suite
cloud-sdk test

# View the deployment guide
cloud-sdk deploy

# Generate a code template for a component called "service"
cloud-sdk template service

# Generate project documentation
cloud-sdk docs

# Check project health
cloud-sdk status

# Clean up build artifacts
cloud-sdk clean

# Show version
cloud-sdk version
```

## Configuration

Set the `CLOUD_SDK_DIR` environment variable to change the data directory:

```bash
export CLOUD_SDK_DIR="$HOME/my-project/.cloud-sdk"
```

Default location: `~/.local/share/cloud-sdk/`

## Output

All command output goes to stdout. Redirect to a file if needed:

```bash
cloud-sdk status > project-health.txt
```

History is automatically logged to `$DATA_DIR/history.log` with timestamps.

---
Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
