---
name: concierge
description: Expert assistant for provisioning charm development and testing environments using concierge. Use when setting up development machines, bootstrapping Juju controllers, installing craft tools (charmcraft, snapcraft, rockcraft), or preparing test environments. Keywords include concierge, provision, development environment, Juju bootstrap, LXD, MicroK8s, K8s, craft tools, prepare, restore.
license: Apache-2.0
compatibility: Requires concierge installed locally (snap or Go). Root/sudo access needed for most operations.
allowed-tools: Bash(concierge:*) Read
---

# Concierge Development Environment Assistant

Expert guidance for provisioning and managing charm development and testing environments using concierge.

## What is Concierge?

Concierge is an opinionated utility for automating the setup of charm development machines. It:
- Installs craft tools (charmcraft, snapcraft, rockcraft)
- Configures providers (LXD, MicroK8s, K8s, Google Cloud)
- Bootstraps Juju controllers
- Installs additional packages (snaps and debs)
- Provides environment restoration capabilities

## Core Workflows

### Quick Start with Presets

```bash
# Full development environment (recommended for most developers)
concierge prepare -p dev

# Machine charm development only
concierge prepare -p machine

# Kubernetes-focused development
concierge prepare -p k8s

# Lightweight K8s with MicroK8s
concierge prepare -p microk8s

# Build tools only (no Juju)
concierge prepare -p crafts
```

**Presets comparison:**

| Preset | Juju | LXD | K8s | MicroK8s | Charmcraft | Snapcraft | Rockcraft | Jhack |
|--------|------|-----|-----|----------|------------|-----------|-----------|-------|
| **dev** | ✓ | ✓† | ✓† | — | ✓ | ✓ | ✓ | ✓ |
| **machine** | ✓ | ✓† | — | — | ✓ | ✓ | — | — |
| **k8s** | ✓ | ✓* | ✓† | — | ✓ | — | ✓ | — |
| **microk8s** | ✓ | ✓* | — | ✓† | ✓ | — | ✓ | — |
| **crafts** | — | ✓ | — | — | ✓ | ✓ | ✓ | — |

**Legend:**
- ✓ = Installed
- ✓† = Installed and bootstrapped with Juju controller
- ✓* = Installed but NOT bootstrapped (only for charmcraft build backend)
- — = Not included

**For detailed preset information, see [references/presets.md](references/presets.md)**

### Environment Status

```bash
# Check provisioning status
concierge status

# Possible states:
# - "provisioning" - Setup in progress
# - "succeeded" - Ready for development
# - "failed" - Setup encountered errors
```

### Restoring Original State

```bash
# Reverse the prepare operation
concierge restore
```

**⚠️ CRITICAL WARNING:**
- `restore` does NOT account for packages/configuration that existed before `prepare`
- It literally reverses the `prepare` operation
- If you had LXD installed before running `prepare`, `restore` will remove it
- Use with caution on machines with existing configurations

### Custom Configuration

Create a `concierge.yaml` file in your working directory:

```yaml
juju:
  channel: "3.6/stable"
  agent_version: "3.6.0"
  bootstrap_constraints:
    cores: 4
    mem: 8G
  model_defaults:
    logging-config: "<root>=INFO"

providers:
  microk8s:
    enable: true
    bootstrap: true
    channel: "1.31-strict/stable"

  lxd:
    enable: true
    bootstrap: true
    channel: "5.21/stable"

  k8s:
    enable: false

  gcloud:
    enable: false

host:
  snaps:
    - name: astral-uv
      channel: "latest/edge"
      classic: true
    - name: jhack
      channel: "latest/stable"

  debs:
    - build-essential
    - python3-dev
```

Then run:
```bash
concierge prepare -c concierge.yaml
```

**For complete YAML schema, see [references/configuration.md](references/configuration.md)**

### Overriding Configuration

```bash
# Override snap channels
concierge prepare -p dev --juju-channel=4.0/edge

# Install extra packages
concierge prepare -p dev \
  --extra-snaps=astral-uv/latest/edge,jhack \
  --extra-debs=build-essential,python3-tox

# Skip Juju installation/bootstrap
concierge prepare -p crafts --disable-juju

# Use Google Cloud credentials
concierge prepare -p k8s --google-credential-file=~/gcloud-creds.json
```

**Channel override flags:**
- `--juju-channel`
- `--lxd-channel`
- `--k8s-channel`
- `--microk8s-channel`
- `--charmcraft-channel`
- `--snapcraft-channel`
- `--rockcraft-channel`

### Environment Variables

All flags have environment variable equivalents:

```bash
# Set via environment
export CONCIERGE_JUJU_CHANNEL="4.0/edge"
export CONCIERGE_EXTRA_SNAPS="astral-uv/latest/edge,jhack"
export CONCIERGE_EXTRA_DEBS="build-essential"

concierge prepare -p dev
```

**Variable naming:** Flag `--juju-channel` becomes `CONCIERGE_JUJU_CHANNEL`

## Common Workflows

### Setting Up a New Development Machine

```bash
# 1. Install concierge
sudo snap install --classic concierge

# 2. Prepare full dev environment
concierge prepare -p dev --extra-snaps=jhack

# 3. Verify installation
concierge status
juju controllers
lxc list

# 4. Start developing
cd my-charm-project
charmcraft pack
juju deploy ./my-charm.charm
```

### Quick K8s Testing Environment

```bash
# Prepare K8s environment
concierge prepare -p k8s

# Verify controller
juju controllers
juju models

# Deploy a K8s charm
juju add-model test
juju deploy postgresql-k8s
```

### Minimal Build-Only Setup

```bash
# Just install craft tools (no Juju)
concierge prepare -p crafts

# Build charms and rocks
cd my-charm
charmcraft pack

cd ../my-rock
rockcraft pack
```

### CI/CD Environment Setup

```bash
# Automated setup for CI
concierge prepare -p dev \
  --juju-channel=3.6/stable \
  --extra-snaps=astral-uv/latest/edge \
  --extra-debs=python3-tox,make

# Check it worked
concierge status
if [ $? -eq 0 ]; then
  echo "Environment ready"
fi
```

### Cleaning Up After Testing

```bash
# Remove everything concierge installed
concierge restore

# Verify cleanup
concierge status
```

## Best Practices

### Choosing a Preset

1. **Use `dev` for general charm development** - Includes everything most developers need
2. **Use `machine` for traditional charms** - No K8s overhead
3. **Use `k8s` or `microk8s` for K8s-only work** - Lighter than `dev`
4. **Use `crafts` for build servers** - Minimal installation for building only

### Configuration Management

1. **Check config into version control** - Share team configurations via `concierge.yaml`
2. **Use environment variables in CI** - Easier than managing config files
3. **Document custom setups** - Add comments to `concierge.yaml`
4. **Test configurations locally first** - Before deploying to CI

### Safety

1. **⚠️ Never run `restore` on production machines** - It removes configurations blindly
2. **Use virtual machines for testing** - Try configurations safely
3. **Check status before and after** - `concierge status` shows what happened
4. **Review preset contents** - Know what will be installed before running

### Development Workflow

1. **Prepare once per machine** - Don't re-run `prepare` unnecessarily
2. **Update tools via snap** - Use `snap refresh` for updates, not `restore`+`prepare`
3. **Use jhack for iteration** - Once environment is ready, jhack speeds up development
4. **Keep environments consistent** - Use same preset across team

## Troubleshooting

### Prepare Fails

```bash
# Run with verbose logging
concierge prepare -p dev -v

# Run with trace logging for detailed output
concierge prepare -p dev --trace

# Check status
concierge status
```

**Common issues:**
- Insufficient permissions - Run with sudo
- Network connectivity - Check internet access
- Conflicting installations - Remove existing snaps first
- Disk space - Ensure adequate free space (10GB+ recommended)

### Controller Bootstrap Fails

If Juju controller bootstrap fails:

```bash
# Check Juju logs
juju debug-log -m controller

# Manually bootstrap if needed
juju bootstrap lxd
juju bootstrap microk8s

# Check provider status
lxc list            # For LXD
microk8s status     # For MicroK8s
```

### Restore Issues

```bash
# Check what will be restored
concierge status

# Run restore with logging
concierge restore -v
```

**If restore fails:**
- Check sudo/root access
- Review logs for specific errors
- Manually remove remaining configurations

### Snap Installation Failures

```bash
# Check snap connectivity
snap version
snap list

# Manually install problematic snaps
sudo snap install juju --channel=3.6/stable --classic

# Then retry prepare
concierge prepare -p dev
```

## Command Reference

```bash
# Prepare environment
concierge prepare [flags]
concierge prepare -p <preset>
concierge prepare -c <config-file>

# Check status
concierge status

# Restore/cleanup
concierge restore

# Shell completion
concierge completion bash
concierge completion zsh
concierge completion fish

# Help
concierge --help
concierge prepare --help
concierge --version

# Logging
concierge prepare -p dev -v        # Verbose
concierge prepare -p dev --trace   # Trace (very detailed)
```

## Integration with Development Tools

### With Charmcraft

```bash
# Prepare environment
concierge prepare -p dev

# Develop charm
cd my-charm
charmcraft init --profile=kubernetes
charmcraft pack
charmcraft test

# Deploy
juju deploy ./my-charm.charm
```

### With Jhack

```bash
# Install jhack during prepare
concierge prepare -p dev --extra-snaps=jhack

# Or add to concierge.yaml
# host:
#   snaps:
#     - name: jhack
#       channel: latest/stable

# Use jhack for development
jhack sync src/ myapp/0
jhack tail myapp/0
```

### With Tox and UV

```bash
# Install build tools
concierge prepare -p dev \
  --extra-snaps=astral-uv/latest/edge \
  --extra-debs=python3-tox

# Use in charm development
cd my-charm
tox -e lint
tox -e unit
uv sync
```

### With CI/CD

```yaml
# GitHub Actions example
- name: Prepare environment
  run: |
    sudo snap install --classic concierge
    concierge prepare -p dev --extra-snaps=astral-uv/latest/edge

- name: Verify setup
  run: concierge status

- name: Run tests
  run: |
    charmcraft pack
    charmcraft test
```

## Configuration Priority

Concierge uses this priority order (highest to lowest):

1. **Command-line flags** - `--juju-channel=4.0/edge`
2. **Environment variables** - `CONCIERGE_JUJU_CHANNEL=4.0/edge`
3. **Configuration file** - `concierge.yaml`
4. **Preset defaults** - Built-in preset values
5. **Fallback** - If no config found, defaults to `dev` preset

## Quick Reference

```bash
# Common operations
concierge prepare -p dev                   # Full dev environment
concierge prepare -p machine               # Machine charm dev
concierge prepare -p k8s                   # K8s charm dev
concierge status                           # Check status
concierge restore                          # Remove everything

# With customisation
concierge prepare -p dev --extra-snaps=jhack
concierge prepare -p dev --juju-channel=4.0/edge
concierge prepare -c my-config.yaml
concierge prepare -p dev -v                # Verbose output

# Environment variables
export CONCIERGE_JUJU_CHANNEL="3.6/stable"
export CONCIERGE_EXTRA_SNAPS="jhack"
concierge prepare -p dev
```

## Resources

- **Concierge GitHub**: https://github.com/canonical/concierge
- **Juju docs**: https://documentation.ubuntu.com/juju/latest/
- **Charmcraft docs**: https://documentation.ubuntu.com/charmcraft/
- **LXD docs**: https://documentation.ubuntu.com/lxd/
- **MicroK8s docs**: https://microk8s.io/docs

## Additional References

When you need detailed information:
- **Complete preset comparison**: See [references/presets.md](references/presets.md)
- **Configuration YAML schema**: See [references/configuration.md](references/configuration.md)

---

**Key reminders:**
- Choose the right preset for your use case
- `restore` does NOT preserve pre-existing configurations
- Use `concierge status` to verify setup
- Add `--extra-snaps=jhack` for rapid development
- Run with `-v` or `--trace` when troubleshooting
