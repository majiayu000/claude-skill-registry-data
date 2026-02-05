---
name: vault-operations
description: HashiCorp Vault operations including secrets engines (KV, AWS, Azure, GCP, Database, PKI), auth methods (Token, AppRole, Kubernetes, OIDC, AWS), policies and ACLs, dynamic credentials, secret rotation, Terraform integration, agent sidecar patterns, audit logging, high availability, and disaster recovery. Activate for Vault secret management, credentials automation, and security configuration.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - WebFetch
  - WebSearch
dependencies:
  - terraform-enterprise
triggers:
  - vault
  - secrets
  - credentials
  - dynamic secrets
  - auth method
  - secret rotation
  - hashicorp vault
  - secret engine
  - vault policy
  - vault agent
---

# Vault Operations Skill

Comprehensive HashiCorp Vault administration for enterprise secret management with dynamic credentials, automated rotation, and multi-cloud integration.

## When to Use This Skill

Activate this skill when:
- Managing secrets engines (KV, Database, Cloud, PKI)
- Configuring authentication methods
- Creating and managing Vault policies
- Setting up dynamic credentials for AWS, Azure, GCP
- Implementing secret rotation
- Integrating Vault with Terraform
- Deploying Vault Agent sidecars
- Configuring audit logging
- Setting up high availability
- Performing disaster recovery operations

## Vault CLI Basics

### Authentication

```bash
# Login with token
export VAULT_ADDR='https://vault.example.com:8200'
export VAULT_TOKEN='s.xxxxxxxxxxxxxx'

# Login with AppRole
vault write auth/approle/login \
  role_id="xxx" \
  secret_id="yyy"

# Login with OIDC
vault login -method=oidc

# Login with Kubernetes
vault write auth/kubernetes/login \
  role="my-role" \
  jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)"
```

### Basic Operations

```bash
# Write a secret
vault kv put secret/myapp/config \
  api_key="abc123" \
  db_password="xyz789"

# Read a secret
vault kv get secret/myapp/config

# Read specific field
vault kv get -field=api_key secret/myapp/config

# List secrets
vault kv list secret/myapp

# Delete secret
vault kv delete secret/myapp/config

# Metadata operations
vault kv metadata get secret/myapp/config
vault kv metadata delete secret/myapp/config
```

## Secrets Engines

### KV v2 (Versioned Key-Value)

```bash
# Enable KV v2 engine
vault secrets enable -path=secret kv-v2

# Write versioned secret
vault kv put secret/myapp/config \
  username="admin" \
  password="secret123"

# Write new version
vault kv put secret/myapp/config \
  username="admin" \
  password="newsecret456"

# Read specific version
vault kv get -version=1 secret/myapp/config

# Get version metadata
vault kv metadata get secret/myapp/config

# Delete version
vault kv delete -versions=1,2 secret/myapp/config

# Undelete version
vault kv undelete -versions=1 secret/myapp/config

# Destroy version (permanent)
vault kv destroy -versions=1 secret/myapp/config

# Set max versions
vault kv metadata put -max-versions=5 secret/myapp/config
```

### AWS Secrets Engine

```bash
# Enable AWS secrets engine
vault secrets enable aws

# Configure AWS credentials
vault write aws/config/root \
  access_key="AKIAIOSFODNN7EXAMPLE" \
  secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" \
  region="us-west-2"

# Create role for dynamic credentials
vault write aws/roles/my-role \
  credential_type="iam_user" \
  policy_document=-<<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": "*"
    }
  ]
}
EOF

# Generate dynamic credentials
vault read aws/creds/my-role

# Create STS role
vault write aws/roles/sts-role \
  credential_type="assumed_role" \
  role_arns="arn:aws:iam::123456789012:role/MyRole" \
  default_sts_ttl="3600"

# Generate STS credentials
vault read aws/sts/sts-role
```

### Azure Secrets Engine

```bash
# Enable Azure secrets engine
vault secrets enable azure

# Configure Azure
vault write azure/config \
  subscription_id="xxx" \
  tenant_id="yyy" \
  client_id="zzz" \
  client_secret="aaa"

# Create role
vault write azure/roles/my-role \
  ttl="1h" \
  azure_roles=-<<EOF
[
  {
    "role_name": "Contributor",
    "scope": "/subscriptions/xxx/resourceGroups/my-rg"
  }
]
EOF

# Generate credentials
vault read azure/creds/my-role
```

### GCP Secrets Engine

```bash
# Enable GCP secrets engine
vault secrets enable gcp

# Configure GCP
vault write gcp/config \
  credentials=@service-account.json

# Create roleset
vault write gcp/roleset/my-roleset \
  project="my-project" \
  secret_type="access_token" \
  token_scopes="https://www.googleapis.com/auth/cloud-platform" \
  bindings=-<<EOF
resource "//cloudresourcemanager.googleapis.com/projects/my-project" {
  roles = ["roles/viewer"]
}
EOF

# Generate access token
vault read gcp/token/my-roleset

# Create service account key
vault write gcp/roleset/my-sa-roleset \
  project="my-project" \
  secret_type="service_account_key" \
  bindings=-<<EOF
resource "//cloudresourcemanager.googleapis.com/projects/my-project" {
  roles = ["roles/compute.instanceAdmin.v1"]
}
EOF

# Generate service account key
vault read gcp/key/my-sa-roleset
```

### Database Secrets Engine

```bash
# Enable database secrets engine
vault secrets enable database

# Configure PostgreSQL connection
vault write database/config/postgresql \
  plugin_name="postgresql-database-plugin" \
  allowed_roles="my-role" \
  connection_url="postgresql://{{username}}:{{password}}@localhost:5432/mydb" \
  username="vault" \
  password="vaultpass"

# Rotate root credentials
vault write -force database/rotate-root/postgresql

# Create role
vault write database/roles/my-role \
  db_name="postgresql" \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  default_ttl="1h" \
  max_ttl="24h"

# Generate dynamic database credentials
vault read database/creds/my-role

# MySQL configuration
vault write database/config/mysql \
  plugin_name="mysql-database-plugin" \
  connection_url="{{username}}:{{password}}@tcp(localhost:3306)/" \
  allowed_roles="mysql-role" \
  username="vault" \
  password="vaultpass"

# MongoDB configuration
vault write database/config/mongodb \
  plugin_name="mongodb-database-plugin" \
  allowed_roles="mongo-role" \
  connection_url="mongodb://{{username}}:{{password}}@localhost:27017/admin" \
  username="vault" \
  password="vaultpass"
```

### PKI Secrets Engine

```bash
# Enable PKI engine
vault secrets enable pki

# Set max lease TTL
vault secrets tune -max-lease-ttl=87600h pki

# Generate root CA
vault write -field=certificate pki/root/generate/internal \
  common_name="example.com" \
  ttl=87600h > CA_cert.crt

# Configure URLs
vault write pki/config/urls \
  issuing_certificates="https://vault.example.com:8200/v1/pki/ca" \
  crl_distribution_points="https://vault.example.com:8200/v1/pki/crl"

# Create role
vault write pki/roles/example-dot-com \
  allowed_domains="example.com" \
  allow_subdomains=true \
  max_ttl="720h"

# Generate certificate
vault write pki/issue/example-dot-com \
  common_name="test.example.com" \
  ttl="24h"

# Revoke certificate
vault write pki/revoke serial_number="xx:xx:xx:xx"
```

## Authentication Methods

### AppRole Auth

```bash
# Enable AppRole
vault auth enable approle

# Create AppRole
vault write auth/approle/role/my-role \
  token_ttl=1h \
  token_max_ttl=4h \
  secret_id_ttl=24h \
  token_policies="default,my-policy"

# Get Role ID
vault read auth/approle/role/my-role/role-id

# Generate Secret ID
vault write -f auth/approle/role/my-role/secret-id

# Login with AppRole
vault write auth/approle/login \
  role_id="xxx" \
  secret_id="yyy"
```

### Kubernetes Auth

```bash
# Enable Kubernetes auth
vault auth enable kubernetes

# Configure Kubernetes
vault write auth/kubernetes/config \
  kubernetes_host="https://kubernetes.default.svc:443" \
  kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt \
  token_reviewer_jwt=@/var/run/secrets/kubernetes.io/serviceaccount/token

# Create role
vault write auth/kubernetes/role/my-role \
  bound_service_account_names="vault-auth" \
  bound_service_account_namespaces="default" \
  policies="default,my-policy" \
  ttl=1h

# Login from pod
vault write auth/kubernetes/login \
  role="my-role" \
  jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)"
```

### OIDC Auth

```bash
# Enable OIDC
vault auth enable oidc

# Configure OIDC
vault write auth/oidc/config \
  oidc_discovery_url="https://accounts.google.com" \
  oidc_client_id="xxx" \
  oidc_client_secret="yyy" \
  default_role="default"

# Create role
vault write auth/oidc/role/default \
  bound_audiences="xxx" \
  allowed_redirect_uris="https://vault.example.com:8200/ui/vault/auth/oidc/oidc/callback" \
  user_claim="email" \
  policies="default"

# Login
vault login -method=oidc
```

### AWS Auth

```bash
# Enable AWS auth
vault auth enable aws

# Configure AWS
vault write auth/aws/config/client \
  access_key="AKIAIOSFODNN7EXAMPLE" \
  secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# Create role for EC2 instances
vault write auth/aws/role/dev-role-ec2 \
  auth_type="ec2" \
  bound_ami_id="ami-xxx" \
  policies="default,dev-policy" \
  max_ttl=1h

# Create role for IAM
vault write auth/aws/role/dev-role-iam \
  auth_type="iam" \
  bound_iam_principal_arn="arn:aws:iam::123456789012:role/MyRole" \
  policies="default,dev-policy" \
  max_ttl=1h
```

## Policies and ACLs

### Basic Policy

```hcl
# my-policy.hcl
path "secret/data/myapp/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "secret/metadata/myapp/*" {
  capabilities = ["list"]
}

path "auth/token/renew-self" {
  capabilities = ["update"]
}

path "auth/token/lookup-self" {
  capabilities = ["read"]
}
```

### Create and Manage Policies

```bash
# Write policy
vault policy write my-policy my-policy.hcl

# Read policy
vault policy read my-policy

# List policies
vault policy list

# Delete policy
vault policy delete my-policy
```

### Advanced Policy Examples

```hcl
# Database credentials policy
path "database/creds/readonly" {
  capabilities = ["read"]
}

# AWS credentials with parameters
path "aws/creds/deploy" {
  capabilities = ["read"]
  allowed_parameters = {
    "ttl" = ["1h", "2h"]
  }
}

# Conditional access based on entity
path "secret/data/{{identity.entity.id}}/*" {
  capabilities = ["create", "read", "update", "delete"]
}

# PKI certificate issuance
path "pki/issue/example-dot-com" {
  capabilities = ["create", "update"]
  allowed_parameters = {
    "common_name" = ["*.example.com"]
    "ttl" = []
  }
  denied_parameters = {
    "ttl" = ["8760h"]
  }
}
```

## Vault Agent Sidecar Pattern

### Agent Configuration

```hcl
# vault-agent-config.hcl
pid_file = "/tmp/pidfile"

vault {
  address = "https://vault.example.com:8200"
}

auto_auth {
  method {
    type = "kubernetes"

    config = {
      role = "my-role"
    }
  }

  sink {
    type = "file"
    config = {
      path = "/vault/secrets/.vault-token"
    }
  }
}

template {
  source = "/vault/configs/config.tmpl"
  destination = "/vault/secrets/config.json"
}

template_config {
  static_secret_render_interval = "5m"
  exit_on_retry_failure = true
}
```

### Kubernetes Deployment with Vault Agent

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  serviceAccountName: vault-auth

  initContainers:
  - name: vault-agent-init
    image: vault:1.14.0
    args:
      - agent
      - -config=/vault/config/agent-config.hcl
      - -exit-after-auth
    env:
      - name: VAULT_ADDR
        value: https://vault.example.com:8200
    volumeMounts:
      - name: vault-config
        mountPath: /vault/config
      - name: vault-secrets
        mountPath: /vault/secrets

  containers:
  - name: app
    image: myapp:latest
    volumeMounts:
      - name: vault-secrets
        mountPath: /vault/secrets
        readOnly: true

  - name: vault-agent
    image: vault:1.14.0
    args:
      - agent
      - -config=/vault/config/agent-config.hcl
    env:
      - name: VAULT_ADDR
        value: https://vault.example.com:8200
    volumeMounts:
      - name: vault-config
        mountPath: /vault/config
      - name: vault-secrets
        mountPath: /vault/secrets

  volumes:
  - name: vault-config
    configMap:
      name: vault-agent-config
  - name: vault-secrets
    emptyDir:
      medium: Memory
```

## Terraform Integration

### Vault Provider

```hcl
terraform {
  required_providers {
    vault = {
      source  = "hashicorp/vault"
      version = "~> 3.20.0"
    }
  }
}

provider "vault" {
  address = "https://vault.example.com:8200"
  token   = var.vault_token
}
```

### Manage Vault with Terraform

```hcl
# Enable secrets engine
resource "vault_mount" "kv" {
  path        = "secret"
  type        = "kv-v2"
  description = "KV v2 secrets engine"
}

# Create policy
resource "vault_policy" "my_policy" {
  name = "my-policy"

  policy = <<EOT
path "secret/data/myapp/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}
EOT
}

# Enable auth method
resource "vault_auth_backend" "kubernetes" {
  type = "kubernetes"
}

# Configure Kubernetes auth
resource "vault_kubernetes_auth_backend_config" "kubernetes" {
  backend            = vault_auth_backend.kubernetes.path
  kubernetes_host    = "https://kubernetes.default.svc:443"
  kubernetes_ca_cert = file("/var/run/secrets/kubernetes.io/serviceaccount/ca.crt")
  token_reviewer_jwt = file("/var/run/secrets/kubernetes.io/serviceaccount/token")
}

# Create Kubernetes role
resource "vault_kubernetes_auth_backend_role" "my_role" {
  backend                          = vault_auth_backend.kubernetes.path
  role_name                        = "my-role"
  bound_service_account_names      = ["vault-auth"]
  bound_service_account_namespaces = ["default"]
  token_ttl                        = 3600
  token_policies                   = ["default", vault_policy.my_policy.name]
}

# AWS secrets engine
resource "vault_aws_secret_backend" "aws" {
  path       = "aws"
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  region     = "us-west-2"
}

# AWS role
resource "vault_aws_secret_backend_role" "deploy" {
  backend         = vault_aws_secret_backend.aws.path
  name            = "deploy"
  credential_type = "iam_user"

  policy_document = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ec2:*",
      "Resource": "*"
    }
  ]
}
EOF
}
```

### Read Secrets from Vault in Terraform

```hcl
# Read KV secret
data "vault_kv_secret_v2" "config" {
  mount = "secret"
  name  = "myapp/config"
}

# Use secret in resource
resource "aws_db_instance" "default" {
  username = data.vault_kv_secret_v2.config.data["db_username"]
  password = data.vault_kv_secret_v2.config.data["db_password"]
}

# Generate dynamic AWS credentials
data "vault_aws_access_credentials" "creds" {
  backend = vault_aws_secret_backend.aws.path
  role    = vault_aws_secret_backend_role.deploy.name
}

provider "aws" {
  access_key = data.vault_aws_access_credentials.creds.access_key
  secret_key = data.vault_aws_access_credentials.creds.secret_key
}
```

## Audit Logging

### Enable Audit Device

```bash
# File audit
vault audit enable file file_path=/vault/logs/audit.log

# Syslog audit
vault audit enable syslog tag="vault" facility="LOCAL7"

# Socket audit
vault audit enable socket address="127.0.0.1:9090" socket_type="tcp"

# List audit devices
vault audit list

# Disable audit device
vault audit disable file/
```

## High Availability

### Raft Storage Configuration

```hcl
# vault-config.hcl
storage "raft" {
  path    = "/vault/data"
  node_id = "node1"

  retry_join {
    leader_api_addr = "https://vault-0.vault-internal:8200"
  }

  retry_join {
    leader_api_addr = "https://vault-1.vault-internal:8200"
  }

  retry_join {
    leader_api_addr = "https://vault-2.vault-internal:8200"
  }
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_cert_file = "/vault/tls/tls.crt"
  tls_key_file  = "/vault/tls/tls.key"
}

api_addr = "https://vault.example.com:8200"
cluster_addr = "https://vault-0.vault-internal:8201"
ui = true
```

### Check HA Status

```bash
# Check HA status
vault status

# List Raft peers
vault operator raft list-peers

# Join Raft cluster
vault operator raft join https://vault-0.vault-internal:8200
```

## Disaster Recovery

### Backup

```bash
# Take snapshot (Raft storage)
vault operator raft snapshot save backup.snap

# Automated backup script
#!/bin/bash
BACKUP_DIR="/vault/backups"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
vault operator raft snapshot save "$BACKUP_DIR/vault-backup-$TIMESTAMP.snap"

# Restore snapshot
vault operator raft snapshot restore backup.snap
```

### Recovery Keys

```bash
# Generate recovery keys
vault operator init -recovery-shares=5 -recovery-threshold=3

# Use recovery key to unseal
vault operator unseal -reset
vault operator unseal <recovery_key>
```

## Common Troubleshooting

### Issue: Vault Sealed

**Solution:** Unseal Vault with unseal keys

```bash
vault operator unseal <key1>
vault operator unseal <key2>
vault operator unseal <key3>
```

### Issue: Permission Denied

**Solution:** Check policy capabilities

```bash
vault token capabilities secret/data/myapp/config
```

### Issue: Token Expired

**Solution:** Renew or create new token

```bash
vault token renew
vault token create -policy=my-policy
```

### Issue: Secret Not Found

**Solution:** Verify path and KV version

```bash
# KV v2 requires /data/ in path
vault kv get secret/myapp/config

# Check mount path
vault secrets list
```

## Best Practices

1. **Enable audit logging** on all Vault clusters
2. **Use dynamic credentials** instead of static secrets
3. **Implement secret rotation** for all credentials
4. **Use Vault Agent** for application secret injection
5. **Never log or print** secret values
6. **Use short TTLs** for tokens and credentials
7. **Implement least privilege** with policies
8. **Enable MFA** for sensitive operations
9. **Backup Raft snapshots** regularly
10. **Monitor Vault metrics** and audit logs

## File References

- See `references/secrets-engines.md` for all secrets engine configurations
- See `references/auth-methods.md` for all auth method configurations
- See `references/policies.md` for policy patterns and examples
- See `references/terraform-integration.md` for Vault with Terraform
- See `examples/` for production-ready Vault configurations
