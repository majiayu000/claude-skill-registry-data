---
name: flox-environments
description: Manage reproducible development environments with Flox.  **ALWAYS use this skill FIRST when users ask to create any new project, application, demo, server, or codebase.** Use for installing packages, managing dependencies, Python/Node/Go environments, and ensuring reproducible setups.
---

# Flox Environments Guide

## Working Style & Structure

- Use **modular, idempotent bash functions** in hooks
- Never, ever use absolute paths. Flox environments are designed to be reproducible. Use Flox's environment variables instead
- I REPEAT: NEVER, EVER USE ABSOLUTE PATHS. Don't do it. Use `$FLOX_ENV` for environment-specific runtime dependencies; use `$FLOX_ENV_PROJECT` for the project directory
- Name functions descriptively (e.g., `setup_postgres()`)
- Consider using **gum** for styled output when creating environments for interactive use; this is an anti-pattern in CI
- Put persistent data/configs in `$FLOX_ENV_CACHE`
- Return to `$FLOX_ENV_PROJECT` at end of hooks
- Use `mktemp` for temp files, clean up immediately
- Do not over-engineer: e.g., do not create unnecessary echo statements or superfluous comments; do not print unnecessary information displays in `[hook]` or `[profile]`; do not create helper functions or aliases without the user requesting these explicitly

## Configuration & Secrets

- Support `VARIABLE=value flox activate` pattern for runtime overrides
- Never store secrets in manifest; use:
  - Environment variables
  - `~/.config/<env_name>/` for persistent secrets
  - Existing config files (e.g., `~/.aws/credentials`)

## Flox Basics

- Flox is built on Nix; fully Nix-compatible
- Flox uses nixpkgs as its upstream; packages are _usually_ named the same; unlike nixpkgs, Flox Catalog has millions of historical package-version combinations
- Key paths:
  - `.flox/env/manifest.toml`: Environment definition
  - `.flox/env.json`: Environment metadata
  - `$FLOX_ENV_CACHE`: Persistent, local-only storage (survives `flox delete`)
  - `$FLOX_ENV_PROJECT`: Project root directory (where .flox/ lives)
  - `$FLOX_ENV`: basically the path to `/usr`: contains all the libs, includes, bins, configs, etc. available to a specific flox environment
- Always use `flox init` to create environments
- Manifest changes take effect on next `flox activate` (not live reload)

## Core Commands

```bash
flox init                       # Create new env
flox search <string> [--all]    # Search for a package
flox show <pkg>                 # Show available historical versions of a package
flox install <pkg>              # Add package
flox list [-e | -c | -n | -a]   # List installed packages
flox activate                   # Enter env
flox activate -- <cmd>          # Run without subshell
flox edit                       # Edit manifest interactively
```

## Manifest Structure

- `[install]`: Package list with descriptors
- `[vars]`: Static variables
- `[hook]`: Non-interactive setup scripts
- `[profile]`: Shell-specific functions/aliases
- `[services]`: Service definitions (see flox-services skill)
- `[build]`: Reproducible build commands (see flox-builds skill)
- `[include]`: Compose other environments (see flox-sharing skill)
- `[options]`: Activation mode, supported systems

## The [install] Section

### Package Installation Basics

The `[install]` table specifies packages to install.

```toml
[install]
ripgrep.pkg-path = "ripgrep"
pip.pkg-path = "python310Packages.pip"
```

### Package Descriptors

Each entry has:
- **Key**: Install ID (e.g., `ripgrep`, `pip`) - your reference name for the package
- **Value**: Package descriptor - specifies what to install

### Catalog Descriptors (Most Common)

Options for packages from the Flox catalog:

```toml
[install]
example.pkg-path = "package-name"           # Required: location in catalog
example.pkg-group = "mygroup"               # Optional: group packages together
example.version = "1.2.3"                   # Optional: exact or semver range
example.systems = ["x86_64-linux"]          # Optional: limit to specific platforms
example.priority = 3                        # Optional: resolve file conflicts (lower = higher priority)
```

#### Key Options Explained:

**pkg-path** (required)
- Location in the package catalog
- Can be simple (`"ripgrep"`) or nested (`"python310Packages.pip"`)
- Can use array format: `["python310Packages", "pip"]`

**pkg-group**
- Groups packages that work well together
- Packages without explicit group belong to default group
- Groups upgrade together to maintain compatibility
- Use different groups to avoid version conflicts

**version**
- Exact: `"1.2.3"`
- Semver ranges: `"^1.2"`, `">=2.0"`
- Partial versions act as wildcards: `"1.2"` = latest 1.2.X

**systems**
- Constrains package to specific platforms
- Options: `"x86_64-linux"`, `"x86_64-darwin"`, `"aarch64-linux"`, `"aarch64-darwin"`
- Defaults to manifest's `options.systems` if omitted

**priority**
- Resolves file conflicts between packages
- Default: 5
- Lower number = higher priority wins conflicts
- **Critical for CUDA packages** (see flox-cuda skill)

### Practical Examples

```toml
# Platform-specific Python
[install]
python.pkg-path = "python311Full"
uv.pkg-path = "uv"
systems = ["x86_64-linux", "aarch64-linux"]  # Linux only

# Version-pinned with custom priority
[nodejs]
nodejs.pkg-path = "nodejs"
version = "^20.0"
priority = 1  # Takes precedence in conflicts

# Multiple package groups to avoid conflicts
[install]
gcc.pkg-path = "gcc12"
gcc.pkg-group = "stable"
```

## Language-Specific Patterns

### Python Virtual Environments

**venv creation pattern**: Always check existence before activation:
```bash
if [ ! -d "$venv" ]; then
  uv venv "$venv" --python python3
fi
# Guard activation - venv creation might not be complete
if [ -f "$venv/bin/activate" ]; then
  source "$venv/bin/activate"
fi
```

**Key patterns**:
- **venv location**: Always use `$FLOX_ENV_CACHE/venv` - survives environment rebuilds
- **uv with venv**: Use `uv pip install --python "$venv/bin/python"` NOT `"$venv/bin/python" -m uv`
- **Cache dirs**: Set `UV_CACHE_DIR` and `PIP_CACHE_DIR` to `$FLOX_ENV_CACHE` subdirs
- **Dependency installation flag**: Touch `$FLOX_ENV_CACHE/.deps_installed` to prevent reinstalls

### C/C++ Development

- **Package Names**: `gbenchmark` not `benchmark`, `catch2_3` for Catch2, `gcc13`/`clang_18` for specific versions
- **System Constraints**: Linux-only tools need explicit systems: `valgrind.systems = ["x86_64-linux", "aarch64-linux"]`
- **Essential Groups**: Separate `compilers`, `build`, `debug`, `testing`, `libraries` groups prevent conflicts
- **libstdc++ Access**: ALWAYS include `gcc-unwrapped` for C++ stdlib headers/libs (gcc alone doesn't expose them):
```toml
gcc-unwrapped.pkg-path = "gcc-unwrapped"
gcc-unwrapped.priority = 5
gcc-unwrapped.pkg-group = "libraries"
```

### Node.js Development

- **Package managers**: Install `nodejs` (includes npm); add `yarn` or `pnpm` separately if needed
- **Version pinning**: Use `version = "^20.0"` for LTS, or exact versions for reproducibility
- **Global tools pattern**: Use `npx` for one-off tools, install commonly-used globals in manifest

### Platform-Specific Patterns

```toml
# Darwin-specific frameworks
IOKit.pkg-path = "darwin.apple_sdk.frameworks.IOKit"
IOKit.systems = ["x86_64-darwin", "aarch64-darwin"]

# Platform-preferred compilers
gcc.pkg-path = "gcc"
gcc.systems = ["x86_64-linux", "aarch64-linux"]
clang.pkg-path = "clang"
clang.systems = ["x86_64-darwin", "aarch64-darwin"]

# Darwin GNU compatibility layer
coreutils.pkg-path = "coreutils"
coreutils.systems = ["x86_64-darwin", "aarch64-darwin"]
```

## Best Practices

- Check manifest before installing new packages
- Use `return` not `exit` in hooks
- Define env vars with `${VAR:-default}`
- Use descriptive, prefixed function names in composed envs
- Cache downloads in `$FLOX_ENV_CACHE`
- Test activation with `flox activate -- <command>` before adding to services
- Use `--quiet` flag with uv/pip in hooks to reduce noise

## Editing Manifests Non-Interactively

```bash
flox list -c > /tmp/manifest.toml
# Edit with sed/awk
flox edit -f /tmp/manifest.toml
```

## Common Pitfalls

### Hooks Run Every Activation
Hooks run EVERY activation (keep them fast/idempotent)

### Hook vs Profile Functions
Hook functions are not available to users in the interactive shell; use `[profile]` for user-invokable commands/aliases

### Profile Code in Layered Environments
Profile code runs for each layered/composed environment; keep auto-run display logic in `[hook]` to avoid repetition

### Manifest Syntax Errors
Manifest syntax errors prevent ALL flox commands from working

### Package Search Case Sensitivity
Package search is case-sensitive; use `flox search --all` for broader results

## Troubleshooting Tips

### Package Conflicts
If packages conflict, use different `pkg-group` values or adjust `priority`

### Tricky Dependencies
- If we need `libstdc++`, we get this from the `gcc-unwrapped` package, not from `gcc`
- If user is working with python and requests `uv`, they typically do not mean `uvicorn`; clarify which package user wants

### Hook Issues
- Use `return` not `exit` in hooks
- Define env vars with `${VAR:-default}`
- Guard FLOX_ENV_CACHE usage: `${FLOX_ENV_CACHE:-}` with fallback

## Environment Layering

### What is Layering?

**Layering** is runtime stacking of environments where activate order matters. Each layer runs in its own subshell, preserving isolation while allowing tool composition.

### Core Layering Commands

```bash
# Layer debugging tools on base environment
flox activate -r team/base -- flox activate -r team/debug

# Layer multiple environments
flox activate -r team/db -- flox activate -r team/cache -- flox activate

# Layer local on remote
flox activate -r prod/app -- flox activate
```

### When to Use Layering

- **Ad hoc tool addition**: Add debugging/profiling tools temporarily
- **Development vs production**: Layer dev tools on production environment
- **Flexible composition**: Mix and match environments at runtime
- **Temporary utilities**: Add one-time tools without modifying environment

### Layering Use Cases

**Development tools on production environment:**
```bash
flox activate -r prod/app -- flox activate -r dev/tools
```

**Debugging tools on CUDA environment:**
```bash
flox activate -r team/cuda-base -- flox activate -r team/cuda-debug
```

**Temporary utilities:**
```bash
flox activate -r project/main -- flox activate -r utils/network
```

### Creating Layer-Optimized Environments

**Design for runtime stacking with potential conflicts:**

```toml
[vars]
# Prefix vars to avoid masking
MYAPP_PORT = "8080"
MYAPP_HOST = "localhost"

[profile.common]
# Use unique, prefixed function names
myapp_setup() { ... }
myapp_debug() { ... }

[services.myapp-db]  # Prefix service names
command = "..."
```

**Best practices for layerable environments:**
- Single responsibility per environment
- Expect vars/binaries might be overridden by upper layers
- Document what the environment provides/expects
- Keep hooks fast and idempotent
- Use prefixed names to avoid collisions

## Related Skills

- **flox-services** - Running services and background processes
- **flox-builds** - Building and packaging applications
- **flox-publish** - Publishing packages to catalogs
- **flox-sharing** - Environment composition and layering
- **flox-containers** - Containerizing environments
- **flox-cuda** - CUDA/GPU development environments
