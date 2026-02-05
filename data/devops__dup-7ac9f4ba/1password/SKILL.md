---
name: 1password
description: Guide for implementing 1Password secrets management - CLI operations, service accounts, and Kubernetes integration. Use when retrieving secrets, managing vaults, configuring CI/CD pipelines, integrating with External Secrets Operator, or automating secrets workflows with 1Password.
---

# 1Password

## Overview

This skill provides comprehensive guidance for working with 1Password's secrets management ecosystem. It covers the `op` CLI for local development, service accounts for automation, and Kubernetes integrations including the native 1Password Operator and External Secrets Operator.

## Quick Reference

### Command Structure

1Password CLI uses a noun-verb structure: `op <noun> <verb> [flags]`

```bash
# Authentication
op signin                    # Sign in to account
op signout                   # Sign out
op whoami                    # Show signed-in account info

# Secret retrieval
op read "op://vault/item/field"              # Read single secret
op run -- <command>                          # Inject secrets as env vars
op inject -i template.env -o .env            # Inject secrets into file

# Item management
op item list                                 # List all items
op item get <item>                           # Get item details
op item create --category login              # Create new item
op item edit <item> field=value              # Edit item
op item delete <item>                        # Delete item

# Vault management
op vault list                                # List vaults
op vault get <vault>                         # Get vault info
op vault create <name>                       # Create vault

# Document management
op document list                             # List documents
op document get <document>                   # Download document
op document create <file> --vault <vault>    # Upload document
```

## Workflow Decision Tree

```
What do you need to do?
├── Retrieve a secret for local development?
│   └── Use: op read, op run, or op inject
├── Manage items/vaults in 1Password?
│   └── Use: op item, op vault, op document commands
├── Automate secrets in CI/CD?
│   └── Use: Service Accounts with OP_SERVICE_ACCOUNT_TOKEN
├── Sync secrets to Kubernetes?
│   ├── Using External Secrets Operator?
│   │   └── See: External Secrets Operator Integration
│   └── Using native 1Password Operator?
│       └── See: 1Password Kubernetes Operator
└── Configure shell plugins for CLI tools?
    └── Use: op plugin commands
```

## Secret Retrieval

### Secret Reference Format

The standard format for referencing secrets:

```
op://<vault>/<item>/<field>
```

Examples:

- `op://Development/AWS/access_key_id`
- `op://Production/Database/password`
- `op://Shared/API Keys/github_token`

### Reading Secrets Directly

```bash
# Read a specific field
op read "op://Development/AWS/access_key_id"

# Read with JSON output
op item get "AWS" --vault Development --format json

# Read specific field from item
op item get "AWS" --vault Development --fields access_key_id
```

### Injecting Secrets into Commands

The `op run` command injects secrets as environment variables:

```bash
# Run command with secrets
op run --env-file=.env.tpl -- ./deploy.sh

# Example .env.tpl file:
# AWS_ACCESS_KEY_ID=op://Development/AWS/access_key_id
# AWS_SECRET_ACCESS_KEY=op://Development/AWS/secret_access_key
```

### Injecting Secrets into Files

The `op inject` command replaces secret references in template files:

```bash
# Inject secrets from template to output file
op inject -i config.tpl.yaml -o config.yaml

# Example config.tpl.yaml:
# database:
#   host: localhost
#   password: op://Production/Database/password
```

## Item Management

### Creating Items

```bash
# Create a login item
op item create --category login \
  --title "My Service" \
  --vault Development \
  username=admin \
  password=secretpassword

# Create with generated password
op item create --category login \
  --title "New Account" \
  --generate-password

# Create from JSON template
op item create --template item.json
```

### Item Template (JSON)

```json
{
  "title": "my-service-credentials",
  "vault": {"id": "vault-uuid-or-name"},
  "category": "LOGIN",
  "fields": [
    {"label": "username", "value": "admin", "type": "STRING"},
    {"label": "password", "value": "secret", "type": "CONCEALED"},
    {"label": "api_key", "value": "key123", "type": "CONCEALED"}
  ]
}
```

### Editing Items

```bash
# Edit a field
op item edit "My Service" password=newpassword

# Add a new field
op item edit "My Service" api_key=newkey

# Edit with specific vault
op item edit "My Service" --vault Development password=newpassword
```

## Service Accounts

Service accounts enable automation without personal credentials.

### Prerequisites

- 1Password CLI version 2.18.0 or later
- Active 1Password subscription
- Admin permissions to create service accounts

### Creating Service Accounts

Via CLI:

```bash
# Create with read-only access
op service-account create "CI/CD Pipeline" \
  --vault Production:read_items

# Create with write access
op service-account create "Deployment Bot" \
  --vault Production:read_items,write_items

# Create with vault creation permission
op service-account create "Provisioning Bot" \
  --vault Production:read_items,write_items \
  --can-create-vaults
```

### Using Service Accounts

Export the service account token:

```bash
export OP_SERVICE_ACCOUNT_TOKEN="ops_..."
```

Then use normal CLI commands - they automatically authenticate with the service account.

### Service Account Limitations

- Cannot access Personal, Private, Employee, or default Shared vaults
- Permissions cannot be modified after creation
- Limited to 100 service accounts per account
- Subject to rate limits

## CI/CD Integration

### GitHub Actions

```yaml
name: Deploy
on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install 1Password CLI
        uses: 1password/install-cli-action@v1

      - name: Load secrets
        uses: 1password/load-secrets-action@v2
        with:
          export-env: true
        env:
          OP_SERVICE_ACCOUNT_TOKEN: ${{ secrets.OP_SERVICE_ACCOUNT_TOKEN }}
          AWS_ACCESS_KEY_ID: op://CI-CD/AWS/access_key_id
          AWS_SECRET_ACCESS_KEY: op://CI-CD/AWS/secret_access_key

      - name: Deploy
        run: ./deploy.sh
```

### GitLab CI

```yaml
deploy:
  image: 1password/op:2
  variables:
    OP_SERVICE_ACCOUNT_TOKEN: $OP_SERVICE_ACCOUNT_TOKEN
  script:
    - export AWS_ACCESS_KEY_ID=$(op read "op://CI-CD/AWS/access_key_id")
    - export AWS_SECRET_ACCESS_KEY=$(op read "op://CI-CD/AWS/secret_access_key")
    - ./deploy.sh
```

### CircleCI

```yaml
version: 2.1
orbs:
  onepassword: onepassword/secrets@1

jobs:
  deploy:
    docker:
      - image: cimg/base:stable
    steps:
      - checkout
      - onepassword/exec:
          command: ./deploy.sh
          env:
            AWS_ACCESS_KEY_ID: op://CI-CD/AWS/access_key_id
            AWS_SECRET_ACCESS_KEY: op://CI-CD/AWS/secret_access_key
```

## External Secrets Operator Integration

External Secrets Operator (ESO) syncs secrets from 1Password to Kubernetes.

### Prerequisites

1. 1Password Connect Server (v1.5.6+)
2. Credentials file (`1password-credentials.json`)
3. Access token for authentication
4. External Secrets Operator installed in cluster

### Connect Server Setup

```bash
# Create automation environment and get credentials
# This generates 1password-credentials.json and an access token

# Create Kubernetes secret for Connect Server credentials
kubectl create secret generic onepassword-credentials \
  --from-file=1password-credentials.json

# Create secret for access token
kubectl create secret generic onepassword-token \
  --from-literal=token=your-access-token
```

### Deploy Connect Server

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: onepassword-connect
spec:
  replicas: 1
  selector:
    matchLabels:
      app: onepassword-connect
  template:
    metadata:
      labels:
        app: onepassword-connect
    spec:
      containers:
        - name: connect-api
          image: 1password/connect-api:latest
          ports:
            - containerPort: 8080
          volumeMounts:
            - name: credentials
              mountPath: /home/opuser/.op/1password-credentials.json
              subPath: 1password-credentials.json
      volumes:
        - name: credentials
          secret:
            secretName: onepassword-credentials
---
apiVersion: v1
kind: Service
metadata:
  name: onepassword-connect
spec:
  selector:
    app: onepassword-connect
  ports:
    - port: 8080
      targetPort: 8080
```

### ClusterSecretStore Configuration

```yaml
apiVersion: external-secrets.io/v1
kind: ClusterSecretStore
metadata:
  name: onepassword
spec:
  provider:
    onepassword:
      connectHost: http://onepassword-connect:8080
      vaults:
        production: 1
        staging: 2
      auth:
        secretRef:
          connectTokenSecretRef:
            name: onepassword-token
            namespace: external-secrets
            key: token
```

### ExternalSecret Examples

Basic secret retrieval:

```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: database-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    kind: ClusterSecretStore
    name: onepassword
  target:
    name: database-credentials
    creationPolicy: Owner
  data:
    - secretKey: username
      remoteRef:
        key: Database             # Item title in 1Password
        property: username        # Field label
    - secretKey: password
      remoteRef:
        key: Database
        property: password
```

Using dataFrom with regex:

```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: env-config
spec:
  refreshInterval: 1h
  secretStoreRef:
    kind: ClusterSecretStore
    name: onepassword
  target:
    name: app-env
  dataFrom:
    - find:
        path: app-config          # Item title
        name:
          regexp: "^[A-Z_]+$"     # Match all uppercase env vars
```

### PushSecret (Kubernetes to 1Password)

```yaml
apiVersion: external-secrets.io/v1alpha1
kind: PushSecret
metadata:
  name: push-generated-secret
spec:
  refreshInterval: 1h
  secretStoreRefs:
    - name: onepassword
      kind: ClusterSecretStore
  selector:
    secret:
      name: generated-credentials
  data:
    - match:
        secretKey: api-key
        remoteRef:
          remoteKey: generated-api-key
          property: password
      metadata:
        apiVersion: kubernetes.external-secrets.io/v1alpha1
        kind: PushSecretMetadata
        spec:
          vault: production
          tags:
            - generated
            - kubernetes
```

## 1Password Kubernetes Operator

The native 1Password Operator provides direct integration without External Secrets Operator.

### Installation via Helm

```bash
helm repo add 1password https://1password.github.io/connect-helm-charts
helm install connect 1password/connect \
  --set-file connect.credentials=1password-credentials.json \
  --set operator.create=true \
  --set operator.token.value=your-access-token
```

### OnePasswordItem CRD

```yaml
apiVersion: onepassword.com/v1
kind: OnePasswordItem
metadata:
  name: database-secret
spec:
  itemPath: "vaults/Production/items/Database"
```

This creates a Kubernetes Secret named `database-secret` with all fields from the 1Password item.

### Auto-Restart Configuration

Enable automatic deployment restarts when secrets change:

```yaml
# Operator-level (environment variable)
AUTO_RESTART=true

# Namespace-level (annotation)
apiVersion: v1
kind: Namespace
metadata:
  name: production
  annotations:
    operator.1password.io/auto-restart: "true"

# Deployment-level (annotation)
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    operator.1password.io/auto-restart: "true"
```

## Shell Plugins

Shell plugins enable automatic authentication for third-party CLIs.

### Available Plugins

```bash
# List available plugins
op plugin list

# Common plugins: aws, gh, stripe, vercel, fly, etc.
```

### Plugin Setup

```bash
# Initialize AWS plugin
op plugin init aws

# This configures shell aliases to use 1Password for AWS credentials
# Add to your shell profile as instructed
```

## Git Workflow with 1Password

Use 1Password to manage GitHub authentication for git operations (push, pull, clone).

### Quick Setup

Run the setup script to configure everything:

```bash
./scripts/setup-gh-plugin.sh
```

### Manual Setup

#### Step 1: Initialize the gh plugin

```bash
# Sign in to 1Password
op signin

# Initialize gh plugin (interactive - select your GitHub token)
op plugin init gh
```

#### Step 2: Configure git credential helper

```bash
# Remove any broken credential helpers
git config --global --unset-all credential.https://github.com.helper 2>/dev/null

# Set gh as the credential helper for GitHub
git config --global credential.https://github.com.helper '!/opt/homebrew/bin/gh auth git-credential'
git config --global credential.https://gist.github.com.helper '!/opt/homebrew/bin/gh auth git-credential'
```

#### Step 3: Add shell integration

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
# 1Password CLI plugins
source ~/.config/op/plugins.sh
```

### How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                        Git Push Workflow                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   git push                                                       │
│      │                                                           │
│      ▼                                                           │
│   Git credential helper                                          │
│      │                                                           │
│      ▼                                                           │
│   gh auth git-credential                                         │
│      │                                                           │
│      ▼                                                           │
│   1Password plugin (via op wrapper)                              │
│      │                                                           │
│      ▼                                                           │
│   1Password (biometric/password unlock)                          │
│      │                                                           │
│      ▼                                                           │
│   Token retrieved and passed to git                              │
│      │                                                           │
│      ▼                                                           │
│   Push completes successfully                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Multiple GitHub Accounts

If you work with multiple GitHub accounts, you can configure per-repo credentials:

```bash
# For a specific repo, use a different 1Password item
cd /path/to/work-repo
git config credential.https://github.com.helper '!/opt/homebrew/bin/gh auth git-credential'

# Or use includeIf in ~/.gitconfig for path-based selection
[includeIf "gitdir:~/work/"]
    path = ~/.gitconfig-work
```

### Fixing Common Issues

#### "Item not found in vault" error

This means the 1Password plugin is pointing to a deleted token:

```bash
# Remove the broken plugin configuration
rm ~/.config/op/plugins/used_items/gh.json

# Re-initialize
op plugin init gh
```

#### gh aliased to op plugin run

If `gh` is aliased to run through 1Password but failing:

```bash
# Check the alias
which gh  # Shows: gh: aliased to op plugin run -- gh

# Run gh directly to bypass the alias
/opt/homebrew/bin/gh auth status
```

#### Git prompting for username/password

Verify the credential helper is configured:

```bash
git config --list | grep credential
```

Should show:

```
credential.https://github.com.helper=!/opt/homebrew/bin/gh auth git-credential
```

## Troubleshooting

### Common Issues

**Authentication fails:**

```bash
# Check current session
op whoami

# Sign in again
op signin

# For service accounts, verify token
echo $OP_SERVICE_ACCOUNT_TOKEN | head -c 10
```

**Item not found:**

```bash
# List items in vault to verify name
op item list --vault "Vault Name"

# Use item ID instead of name for reliability
op item get --vault Development dh7fjsh3kd8fjs
```

**Permission denied in CI/CD:**

```bash
# Verify service account has access to vault
op vault list  # Should show accessible vaults

# Check rate limits
op service-account ratelimit
```

**External Secrets not syncing:**

```bash
# Check ExternalSecret status
kubectl describe externalsecret <name>

# Check Connect Server logs
kubectl logs -l app=onepassword-connect

# Verify SecretStore connection
kubectl describe secretstore <name>
```

## Best Practices

1. **Use secret references** (`op://`) instead of hardcoding vault/item names in scripts
2. **Prefer service accounts** over personal accounts for automation
3. **Scope permissions minimally** - grant only necessary vault access
4. **Use item IDs** in scripts for stability (names can change)
5. **Rotate service account tokens** when sign-in addresses change
6. **Enable auto-restart** in Kubernetes for seamless secret rotation
7. **Use separate vaults** per environment (dev, staging, prod)
8. **Tag items** for organization and filtering

## Resources

### References

- `references/cli-commands.md` - Complete CLI command reference
- `references/kubernetes-examples.md` - Kubernetes manifest examples

### Scripts

- `scripts/setup-gh-plugin.sh` - Setup GitHub CLI with 1Password integration
- `scripts/setup-service-account.sh` - Create and configure a service account
- `scripts/sync-check.sh` - Verify External Secrets synchronization

### External Documentation

- [1Password CLI Documentation](https://developer.1password.com/docs/cli/)
- [Service Accounts Guide](https://developer.1password.com/docs/service-accounts/)
- [Kubernetes Operator](https://developer.1password.com/docs/k8s/operator/)
- [External Secrets Provider](https://external-secrets.io/latest/provider/1password-automation/)
