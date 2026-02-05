---
name: charmcraft
description: Expert assistant for developing Juju charms using charmcraft. Use when initializing charm projects, building charms, managing charm libraries, publishing to Charmhub, running tests, or working with charmcraft.yaml configuration. Keywords include charmcraft, Juju, charm development, Charmhub publishing, charm libraries, pack, build, upload, release, init, extensions.
license: Apache-2.0
compatibility: Requires charmcraft 4.0+ installed locally. Network access needed for Charmhub operations.
allowed-tools: Bash(charmcraft:*) Read
---

# Charmcraft Development Assistant

Expert guidance for developing, building, testing, and publishing Juju charms using charmcraft.

## Core Workflows

### Project Initialization

```bash
# Initialize new charm with profile
charmcraft init --profile=kubernetes       # K8s charm (default)
charmcraft init --profile=machine          # Machine charm
charmcraft init --profile=django-framework # Django app
charmcraft init --profile=fastapi-framework # FastAPI app
charmcraft init --profile=flask-framework  # Flask app

# With custom name and author
charmcraft init --name=my-charm --author="Your Name"

# List/expand extensions
charmcraft list-extensions
charmcraft expand-extensions
```

**After init:**
1. Customize `charmcraft.yaml` (metadata, bases, relations, config)
2. Edit `README.md` (becomes Charmhub documentation)
3. Implement `src/charm.py` (using Ops framework)
4. Update tests in `tests/unit/` and `tests/integration/`

**For detailed charmcraft.yaml configuration, see [references/charmcraft-yaml-reference.md](references/charmcraft-yaml-reference.md)**

### Building and Packaging

```bash
# Build charm
charmcraft pack                    # Main command
charmcraft pack -o ./build/        # Custom output directory
charmcraft pack --bases-index=0    # Specific base (if multiple defined)

# Analyse charm (always run before uploading!)
charmcraft analyse ./my-charm_ubuntu-22.04-amd64.charm
charmcraft analyse --format=json ./my-charm.charm

# Clean build artifacts
charmcraft clean

# Remote build (for multi-architecture)
charmcraft remote-build
```

**Build lifecycle:** `pack` handles everything automatically. Only use individual steps (`pull`, `build`, `stage`, `prime`) for debugging.

**Always run `charmcraft analyse` before uploading to catch:**
- Missing/malformed metadata
- File permission issues
- Deprecated patterns

### Testing

```bash
# Run tests
charmcraft test                    # Integration tests
charmcraft test --shell            # Debug environment
charmcraft test --debug            # Shell on failure

# Local quality checks
tox -e format                      # Format with ruff
tox -e lint                        # Lint with ruff + pyright
tox -e unit                        # Unit tests (ops.testing)
tox -e integration                 # Integration tests
```

### Publishing to Charmhub

```bash
# Account setup
charmcraft login
charmcraft whoami
charmcraft register my-charm       # Register name first

# Upload and release
charmcraft upload ./my-charm.charm --release=edge
charmcraft status my-charm         # Check status
charmcraft revisions my-charm      # List revisions

# Release specific revision
charmcraft release my-charm --revision=5 --channel=stable

# Promote between channels
charmcraft promote my-charm --from=beta --to=stable

# Close channel
charmcraft close my-charm edge
```

**Channel structure:** `[track/]risk[/branch]`
- Risks: `edge` → `beta` → `candidate` → `stable`
- Examples: `stable`, `edge`, `2.0/candidate`, `beta/hotfix-123`

**Always:** Upload to `edge` first, test thoroughly, then promote through channels.

#### Resources

```bash
# Manage resources (images, binaries)
charmcraft resources my-charm
charmcraft upload-resource my-charm my-resource --filepath=./file.tar.gz
charmcraft resource-revisions my-charm my-resource

# Release with specific resources
charmcraft release my-charm --revision=5 --channel=stable --resource=my-resource:3
```

### Library Management

```bash
# Using libraries (define in charmcraft.yaml first)
charmcraft fetch-libs              # Fetch defined libraries
charmcraft list-lib postgresql     # List available libs

# Publishing libraries
charmcraft create-lib my-charm my_library
charmcraft publish-lib charms.my_charm.v0.my_library
```

**In charmcraft.yaml:**
```yaml
charm-libs:
  - lib: postgresql.postgres_client
    version: "0"           # Major version (auto-updates minor)
  - lib: mysql.client
    version: "0.57"        # Pinned version
```

**Library versioning:**
- `v0`, `v1` = breaking changes (API changes)
- Patch auto-increments for non-breaking changes
- Libraries go in `lib/charms/{charm_name}/v{X}/{lib_name}.py`

## Essential Files

### charmcraft.yaml
Core configuration defining:
- Charm metadata (`name`, `title`, `summary`, `description`)
- Base OS (`bases`)
- Build config (`parts`)
- Relations (`provides`, `requires`, `peers` - always use `optional: true` for requires!)
- Config options (`config`)
- Actions (`actions`)
- Resources (`resources`)
- Containers (K8s charms)

**See [references/charmcraft-yaml-reference.md](references/charmcraft-yaml-reference.md) for complete specification.**

### src/charm.py
Main charm implementation:
- Config/action dataclasses
- Charm class (extends `CharmBase`)
- Event observation and handlers
- Uses Ops framework: https://documentation.ubuntu.com/ops/

## Best Practices

### Development Workflow
1. **Write integration tests first** - define expected behavior
2. **Implement incrementally** - get basic functionality working
3. **Run quality checks** - `tox -e lint` and `tox -e format` frequently
4. **Analyse before upload** - `charmcraft analyse` on every build
5. **Test locally** - `charmcraft pack` then `juju deploy ./my-charm.charm`

### Documentation
Keep updated:
- `README.md` - Main docs (appears on Charmhub)
- `CONTRIBUTING.md` - Development workflow
- `CHANGELOG.md` - User-facing changes
- `SECURITY.md` - Security reporting
- `TUTORIAL.md` - Basic usage guide

### Version Control
Commit: `charmcraft.yaml`, all source, `uv.lock`, `pyproject.toml`, tests, docs

Ignore: `*.charm`, `__pycache__/`, `.tox/`, `venv/`, `.claude/settings.local.json`

## Common Patterns

### Multi-Base Builds
```yaml
bases:
  - build-on:
      - name: ubuntu
        channel: "22.04"
    run-on:
      - name: ubuntu
        channel: "22.04"
  - build-on:
      - name: ubuntu
        channel: "24.04"
    run-on:
      - name: ubuntu
        channel: "24.04"
```

Pack for specific base: `charmcraft pack --bases-index=0`

### Database Integration Example
```yaml
# In charmcraft.yaml
requires:
  database:
    interface: postgresql_client
    optional: true  # ALWAYS include the `optional` field, rather than relying on the default. Use `optional: false` if the charm works without the relation

charm-libs:
  - lib: data_platform_libs.data_interfaces
    version: "0"
```

```python
# In src/charm.py
from charms.data_platform_libs.v0.data_interfaces import DatabaseRequires

class MyCharm(CharmBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.database = DatabaseRequires(self, "database", "myapp")
        self.framework.observe(
            self.database.on.database_created,
            self._on_database_created
        )
```

## Troubleshooting

**Build fails:**
- Check `charmcraft.yaml` syntax
- Verify required files exist (`src/charm.py`, `uv.lock`)
- Run `charmcraft -v pack` for verbose output

**Upload fails:**
- Login: `charmcraft login`
- Register name: `charmcraft register my-charm`
- Analyse first: `charmcraft analyse ./my-charm.charm`

**Library errors:**
- Fetch: `charmcraft fetch-libs`
- Check library definitions in `charmcraft.yaml`

**Runtime issues:**
- Check Juju logs: `juju debug-log`
- Verify resources uploaded: `charmcraft resources my-charm`
- Test base compatibility

**For comprehensive troubleshooting, see [references/troubleshooting.md](references/troubleshooting.md)**

## Quick Reference

```bash
# Setup
charmcraft init --profile=kubernetes
charmcraft login

# Development cycle
charmcraft pack
charmcraft analyse ./my-charm.charm
tox -e lint
tox -e unit

# Publishing
charmcraft upload ./my-charm.charm --release=edge
charmcraft status my-charm
charmcraft promote my-charm --from=edge --to=beta

# Libraries
charmcraft fetch-libs
charmcraft publish-lib charms.my_charm.v0.my_library

# Testing with Juju
juju deploy ./my-charm.charm
juju status
juju debug-log
```

## Resources

- **Charmcraft docs**: https://documentation.ubuntu.com/charmcraft/stable/
- **Juju docs**: https://documentation.ubuntu.com/juju/latest/
- **Ops framework**: https://documentation.ubuntu.com/ops/latest/
- **Charmhub**: https://charmhub.io/

## Additional References

When you need detailed information:
- **Complete charmcraft.yaml reference**: See [references/charmcraft-yaml-reference.md](references/charmcraft-yaml-reference.md)
- **Troubleshooting guide**: See [references/troubleshooting.md](references/troubleshooting.md)
- **Quick project setup**: Use `scripts/quick-start.sh` helper

---

**Key reminders:**
- Always run `charmcraft analyse` before uploading
- Test on `edge` before promoting to `stable`
- Use `optional: true` for all `requires` relations
- Keep `uv.lock` in version control
- Follow conventional commits for changelogs
