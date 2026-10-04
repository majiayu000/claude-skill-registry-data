---
name: pulumi-cli
description: "Use for hands-on Pulumi CLI work: running deployments, fixing broken stacks, and managing infrastructure state. Handles: recovering from stuck or interrupted `pulumi up` with pending operations, cleaning orphaned resources from state after out-of-band cloud deletions, protecting critical resources from accidental `pulumi destroy`, moving resources between stacks without recreating them, targeting specific resources during deployment, migrating between backends (local file to Pulumi Cloud, S3), stack lifecycle management, state export/import/repair, CI/CD pipeline setup, and importing existing cloud resources. Use this skill — not the language-specific Pulumi skills — whenever the user's question is about operating, troubleshooting, or recovering Pulumi infrastructure rather than writing program code."
---

# Pulumi CLI Skill

## Quick Command Reference

### Deployment Workflow

```bash
# 1. Create new project
pulumi new typescript                    # Interactive
pulumi new aws-typescript --name myapp --stack dev --yes  # Non-interactive

# 2. Preview changes
pulumi preview                           # Interactive preview
pulumi preview --diff                    # Show detailed diff

# 3. Deploy
pulumi up                                # Interactive deployment
pulumi up --yes                          # Non-interactive
pulumi up --skip-preview --yes           # Skip preview step

# 4. View outputs
pulumi stack output
pulumi stack output --json

# 5. Tear down
pulumi destroy --yes
```

### Stack Management

```bash
# List stacks
pulumi stack ls

# Create and select stacks
pulumi stack init dev
pulumi stack select prod

# View stack info
pulumi stack
pulumi stack history

# Stack outputs
pulumi stack output
pulumi stack output bucketName --show-secrets

# Remove stack
pulumi stack rm dev --yes
```

### State Operations

```bash
# Refresh state from cloud
pulumi refresh --yes

# Export/import state
pulumi stack export --file backup.json
pulumi stack import --file backup.json

# Delete resource from state (keeps cloud resource)
pulumi state delete 'urn:pulumi:dev::myproject::aws:s3/bucket:Bucket::my-bucket'

# Move resource between stacks (preferred over delete+import)
# This is a single atomic operation that transfers state without touching cloud resources
pulumi state move --source dev --dest prod 'urn:...'

# Protect critical resources
pulumi state protect 'urn:...'
```

### Configuration

```bash
# Set config values
pulumi config set aws:region us-west-2
pulumi config set dbPassword secret --secret

# Get config
pulumi config get aws:region
pulumi config                            # List all

# Link ESC environment (see language-specific skills for ESC details)
pulumi config env add myorg/myproject-dev
```

## Common Flags

| Flag | Description |
|------|-------------|
| `--yes` / `-y` | Skip confirmation prompts |
| `--stack` / `-s` | Specify stack name |
| `--parallel` / `-p` | Limit concurrent operations |
| `--target` | Target specific resource URNs |
| `--refresh` | Refresh state before operation |
| `--diff` | Show detailed diff |
| `--json` | Output in JSON format |
| `--skip-preview` | Skip preview step |
| `--suppress-outputs` | Hide stack outputs |

## CI/CD Quick Setup

These three environment variables are essential for non-interactive Pulumi in CI/CD — without `PULUMI_CI=true`, Pulumi may prompt for input and hang your pipeline:

```bash
# Required environment variables (all three are important)
export PULUMI_ACCESS_TOKEN=pul-xxx    # Authentication token
export PULUMI_CI=true                  # Disables interactive prompts
export PULUMI_SKIP_UPDATE_CHECK=true   # Avoids update check delays

# Typical CI workflow
pulumi login                           # Authenticates via PULUMI_ACCESS_TOKEN
pulumi stack select prod               # Select target stack explicitly
pulumi preview                         # Always preview before deploying
pulumi up --yes                        # --yes for non-interactive confirmation
```

## Importing Existing Resources

```bash
# Import single resource
pulumi import aws:s3/bucket:Bucket my-bucket existing-bucket-name

# Bulk import from file
pulumi import --file resources.json
```

**resources.json format:**
```json
{
  "resources": [
    {"type": "aws:s3/bucket:Bucket", "name": "my-bucket", "id": "existing-bucket-name"}
  ]
}
```

## State Recovery Patterns

### Resource deleted outside Pulumi
```bash
pulumi refresh --yes
# Or manually remove from state:
pulumi state delete 'urn:pulumi:dev::myproject::aws:s3/bucket:Bucket::deleted-bucket'
```

### Stuck pending operations
```bash
pulumi refresh --clear-pending-creates --yes
# Or:
pulumi cancel --yes
pulumi state repair
```

### State corruption
```bash
# Backup current state
pulumi stack export --file current.json

# Try repair
pulumi state repair

# Or restore from history
pulumi stack export --version <previous-version> --file good.json
pulumi stack import --file good.json
```

## URN Format

```
urn:pulumi:<stack>::<project>::<type>::<name>

Example:
urn:pulumi:dev::myproject::aws:s3/bucket:Bucket::my-bucket
```

## Backend Options

```bash
# Pulumi Cloud (default)
pulumi login

# Self-hosted backends
pulumi login s3://my-bucket
pulumi login azblob://my-container
pulumi login gs://my-bucket
pulumi login file://~/.pulumi-state
```

## References

- [references/pulumi-cli-commands.md](references/pulumi-cli-commands.md) - Complete command documentation
- [references/pulumi-state-management.md](references/pulumi-state-management.md) - State operations and recovery
- [references/pulumi-environment-variables.md](references/pulumi-environment-variables.md) - CI/CD environment variables
