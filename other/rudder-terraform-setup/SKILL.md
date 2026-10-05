---
name: rudder-terraform-setup
description: Installs Terraform and configures the RudderStack provider. Use when setting up terraform for rudderstack, installing terraform-provider-rudderstack, or terraform provider not found errors
allowed-tools: "Bash(which, curl, terraform *, uname), Read, Write, Edit"
---

# RudderStack Terraform Setup

Install Terraform (if missing), configure the RudderStack provider, and verify setup.

## Setup Workflow

```
1. Check Terraform ──► terraform version
         │
         ├── Found ──► Skip to Provider Setup
         │
         └── Not Found ──► Guide Installation
                                    │
2. Configure Provider ◄─────────────┘
         │
         └── Add required_providers block

3. Initialize ──► terraform init
         │
         └── Downloads provider from registry

4. Configure Auth ──► Check RUDDERSTACK_ACCESS_TOKEN
         │
         └── Verify with terraform plan
```

## Step 1: Check Terraform Installation

```bash
terraform version
```

**If found:** Shows version. Skip to Step 2.

**If not found:** Install Terraform.

### Install Terraform

#### macOS (Homebrew)

```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

#### Linux (apt)

```bash
# Add HashiCorp GPG key
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

# Add repository
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

# Install
sudo apt update && sudo apt install terraform
```

#### Alternative: tfenv (Version Manager)

```bash
# macOS
brew install tfenv

# Then install Terraform
tfenv install latest
tfenv use latest
```

#### Verify Installation

```bash
terraform version
```

Expected: `Terraform v1.x.x`

## Step 2: Configure RudderStack Provider

### Create or Update versions.tf

In your Terraform project directory, create `versions.tf`:

```hcl
terraform {
  required_version = ">= 1.0"

  required_providers {
    rudderstack = {
      source  = "rudderlabs/rudderstack"
      version = "~> 4.3.1"
    }
  }
}

provider "rudderstack" {
  # access_token read from RUDDERSTACK_ACCESS_TOKEN env var
}
```

### Check Provider Latest Version

Visit https://registry.terraform.io/providers/rudderlabs/rudderstack/latest for the current version.

## Step 3: Initialize Provider

```bash
terraform init
```

Expected output:
```
Initializing provider plugins...
- Finding rudderlabs/rudderstack versions matching "~> 4.3.1"...
- Installing rudderlabs/rudderstack v4.3.1...
- Installed rudderlabs/rudderstack v4.3.1

Terraform has been successfully initialized!
```

### Verify Provider Installed

```bash
terraform providers
```

Should show `rudderlabs/rudderstack` in the list.

## Step 4: Configure Authentication

### Set Access Token

Get your access token from RudderStack dashboard: **Settings → Access Tokens**

```bash
export RUDDERSTACK_ACCESS_TOKEN="your-token-here"
```

For permanent setup, add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
echo 'export RUDDERSTACK_ACCESS_TOKEN="your-token-here"' >> ~/.zshrc
source ~/.zshrc
```

### Verify Authentication

Create a minimal `main.tf` to test:

```hcl
# main.tf - minimal test configuration
data "rudderstack_source" "test" {
  # This will fail if auth is wrong
}
```

Then run:

```bash
terraform plan
```

**If authenticated:** Shows "No changes" or data source info.

**If not authenticated:** Shows authentication error.

## Credential Security

- **Never hardcode tokens** in `.tf` files
- Use environment variable `RUDDERSTACK_ACCESS_TOKEN`
- Add `.env` and `*.tfvars` containing secrets to `.gitignore`
- For CI/CD, use repository secrets or vault
- **Never commit `.tfstate`** without encryption (contains sensitive data)

## Provider Configuration Options

```hcl
provider "rudderstack" {
  # Token from env var (recommended)
  # access_token = var.rudderstack_token  # Alternative: use variable

  # Optional: Override API URL (default: https://api.rudderstack.com/v2)
  # api_url = "https://api.rudderstack.com/v2"
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `provider not found` | Run `terraform init` |
| `unauthorized` | Check RUDDERSTACK_ACCESS_TOKEN is set correctly |
| `version constraints` | Update version in required_providers block |
| `init fails` | Check network; try with `-upgrade` flag |

## Next Steps

After setup completes:
- Run `/rudder-environment-check` to verify full environment
- Use `/rudder-terraform-workflow` for plan/apply cycles
