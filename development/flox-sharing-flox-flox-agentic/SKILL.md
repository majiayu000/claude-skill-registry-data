---
name: flox-sharing
description: Sharing and composing Flox environments. Use for environment composition, remote environments, FloxHub, and team collaboration patterns.
---

# Flox Environment Sharing & Composition Guide

## Core Concepts

**Composition**: Build-time merging of environments (deterministic)
**Remote Environments**: Shared environments via FloxHub
**Team Collaboration**: Reusable, shareable environment stacks

## Understanding Environment Sharing

**The `.flox/` directory contains the environment definition**:
- Package specifications and versions
- Environment variables
- Build definitions
- Hooks and services configuration

**The environment definition does NOT include**:
- Built binaries/artifacts (those are created by builds and can be published as packages)
- Local data or cache

**Two sharing mechanisms**:
1. **Git**: Commit `.flox/` directory to git. When used with development environments, this is typically alongside your source code in the same repository. Other developers clone the repo and get both the environment definition and source code.
2. **FloxHub**: Push environment definition only using `flox push`. This shares ONLY the `.flox/` directory, not any source code or other files. Useful for runtime environments or shared base environments used across multiple projects.

**This is different from publishing packages** (see **flox-publish** skill), where you build and distribute the actual binaries/artifacts.

## Core Commands

```bash
# Activate remote environment
flox activate -r owner/environment-name

# Pull remote environment locally
flox pull owner/environment-name

# Push local environment to FloxHub
flox push

# Compose environments in manifest
# (see [include] section below)
```

## Environment Composition

### Basic Composition

Merge environments at build time using `[include]`:

```toml
[include]
environments = [
    { remote = "team/postgres" },
    { remote = "team/redis" },
    { remote = "team/python-base" }
]
```

### Creating Composition-Optimized Environments

**Design for clean merging at build time:**

```toml
[install]
# Use pkg-groups to prevent conflicts
gcc.pkg-path = "gcc"
gcc.pkg-group = "compiler"

[vars]
# Never duplicate var names across composed envs
POSTGRES_PORT = "5432"  # Not "PORT"

[hook]
# Check if setup already done (idempotent)
setup_postgres() {
  [ -d "$FLOX_ENV_CACHE/postgres" ] || init_db
}
```

**Best practices:**
- No overlapping vars, services, or function names
- Use explicit, namespaced naming (e.g., `postgres_init` not `init`)
- Minimal hook logic (composed envs run ALL hooks)
- Avoid auto-run logic in `[profile]` (runs once per layer/composition; help displays will repeat)
- Test composability: `flox activate` each env standalone first

### Composition Example: Full Stack

```toml
# .flox/env/manifest.toml
[include]
environments = [
    { remote = "team/postgres" },
    { remote = "team/redis" },
    { remote = "team/nodejs" },
    { remote = "team/monitoring" }
]

[vars]
# Override composed environment variables
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5433"  # Non-standard port
```

### Use Cases for Composition

**Reproducible stacks:**
```toml
[include]
environments = [
    { remote = "team/cuda-base" },
    { remote = "team/cuda-math" },
    { remote = "team/python-ml" }
]
```

**Shared base configuration:**
```toml
[include]
environments = [
    { remote = "org/standards" },  # Company-wide settings
    { remote = "team/backend" }    # Team-specific tools
]
```

## Creating Dual-Purpose Environments

**Design for both layering and composition:**

```toml
[install]
# Clear package groups
python.pkg-path = "python311"
python.pkg-group = "runtime"

[vars]
# Namespace everything
MYPROJECT_VERSION = "1.0"
MYPROJECT_CONFIG = "$FLOX_ENV_CACHE/config"

[profile.common]
# Defensive function definitions
if ! type myproject_init >/dev/null 2>&1; then
  myproject_init() { ... }
fi
```

## Remote Environments

### Activating Remote Environments

```bash
# Activate remote environment directly
flox activate -r owner/environment-name

# Activate and run a command
flox activate -r owner/environment-name -- npm test
```

### Pulling Remote Environments

```bash
# Pull to work on locally
flox pull owner/environment-name

# Now it's in your local .flox/
flox activate
```

### Pushing Environments to FloxHub

```bash
# Initialize Git repo if needed
git init
git add .flox/
git commit -m "Initial environment"

# Push to FloxHub
flox push

# Others can now activate with:
# flox activate -r yourusername/your-repo
```

### Choosing Between Git and FloxHub

**Commit `.flox/` to Git when:**
- Environment is for development (includes build tools)
- Environment lives alongside source code
- You want version control history for environment changes
- Team already uses git for collaboration

**Push to FloxHub when:**
- Environment is for runtime/production (no source code needed)
- Creating shared base environments used across multiple projects
- Environment needs to be independently versioned from source code
- You want to share environment without exposing source code

**Recommended pattern**: Commit development environments to git with source code; push runtime environments to FloxHub.

## Team Collaboration Patterns

### Base + Specialization

**Create base environment:**
```toml
# team/base
[install]
git.pkg-path = "git"
gh.pkg-path = "gh"
jq.pkg-path = "jq"

[vars]
ORG_REGISTRY = "registry.company.com"
```

**Specialize for teams:**
```toml
# team/frontend
[include]
environments = [{ remote = "team/base" }]

[install]
nodejs.pkg-path = "nodejs"
pnpm.pkg-path = "pnpm"
```

```toml
# team/backend
[include]
environments = [{ remote = "team/base" }]

[install]
python.pkg-path = "python311Full"
uv.pkg-path = "uv"
```

### Service Libraries

**Create reusable service environments:**

```toml
# team/postgres-service
[install]
postgresql.pkg-path = "postgresql"

[services.postgres]
command = '''
  mkdir -p "$FLOX_ENV_CACHE/postgres"
  if [ ! -d "$FLOX_ENV_CACHE/postgres/data" ]; then
    initdb -D "$FLOX_ENV_CACHE/postgres/data"
  fi
  exec postgres -D "$FLOX_ENV_CACHE/postgres/data" \
    -h "$POSTGRES_HOST" -p "$POSTGRES_PORT"
'''
is-daemon = true

[vars]
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
```

**Compose into projects:**
```toml
# my-project
[include]
environments = [
    { remote = "team/postgres-service" },
    { remote = "team/redis-service" }
]
```

### Development vs Runtime Environments

**Development environment (for building):**
```toml
# project-dev (committed to git with source code)
[install]
gcc.pkg-path = "gcc13"
make.pkg-path = "make"
debugpy.pkg-path = "python311Packages.debugpy"
pytest.pkg-path = "python311Packages.pytest"

[build.myapp]
command = '''
  make release
  mkdir -p $out/bin
  cp build/myapp $out/bin/
'''
version = "1.0.0"

[vars]
DEBUG = "true"
LOG_LEVEL = "debug"
```

Developers commit this `.flox/` directory to git with the source code. Other developers `git clone` and `flox activate` to get the same development environment.

**Runtime environment (for consuming):**
```toml
# project-runtime (pushed to FloxHub, no source code)
[install]
myapp.pkg-path = "myorg/myapp"  # Published package, not source

[vars]
DEBUG = "false"
LOG_LEVEL = "info"
MYAPP_CONFIG = "$FLOX_ENV_CACHE/config"
```

After publishing `myapp`, consumers create this runtime environment and install the published package. The runtime environment can be pushed to FloxHub and shared without exposing source code.

**Key distinction**: Development environments contain build tools and source code; runtime environments contain published packages (binaries/artifacts).

(See **flox-environments** skill for layering environments at runtime)

## Composition with Local Packages

Combine composed environments with local packages:

```toml
# Compose base services
[include]
environments = [
    { remote = "team/database-services" },
    { remote = "team/cache-services" }
]

# Add project-specific packages
[install]
myapp.pkg-path = "company/myapp"
```

See **flox-environments** skill for layering environments at runtime.

## Best Practices

### For Shareable Environments

1. **Use descriptive names**: `team/postgres-service` not `db`
2. **Document expectations**: What vars/ports/services are provided
3. **Namespace everything**: Prefix vars, functions, services
4. **Keep focused**: One responsibility per environment
5. **Test standalone**: `flox activate` should work without composition

### For Composed Environments

1. **No name collisions**: Check for overlapping vars/services
2. **Idempotent hooks**: Can run multiple times safely
3. **Minimal auto-run**: Avoid output in `[profile]`
4. **Clear dependencies**: Document what environments are needed

(For layering best practices, see **flox-environments** skill)

## Version Management

### Pin Specific Versions

```toml
[include]
environments = [
    { remote = "team/base", version = "v1.2.3" }
]
```

### Use Latest

```toml
[include]
environments = [
    { remote = "team/base" }  # Uses latest
]
```

## Troubleshooting

### Conflicts in Composition

If composed environments conflict:
1. Use different `pkg-group` values
2. Adjust `priority` for file conflicts
3. Namespace variables to avoid collisions
4. Test each environment standalone first

(For layering troubleshooting, see **flox-environments** skill)

### Remote Environment Not Found

```bash
# Check available remote environments
flox search --remote owner/

# Pull and inspect locally
flox pull owner/environment-name
flox list -c
```

## Related Skills

- **flox-environments** - Creating base environments
- **flox-services** - Sharing service configurations
- **flox-containers** - Deploying shared environments
- **flox-publish** - Publishing built packages (binaries/artifacts) vs sharing environments (definitions only)
