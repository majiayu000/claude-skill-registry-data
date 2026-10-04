---
name: sops
description: "Expert agent for Mozilla SOPS (Secrets OPerationS). Covers file encryption (YAML/JSON/ENV/INI), AWS KMS, GCP KMS, Azure Key Vault, age, and PGP backends, partial file encryption, GitOps patterns, and Flux/ArgoCD integration. WHEN: \"SOPS\", \"Mozilla SOPS\", \"sops encrypt\", \"sops decrypt\", \"GitOps secrets\", \"age encryption\", \"SOPS ArgoCD\", \"SOPS Flux\", \"encrypted yaml git\"."
license: MIT
---

# Mozilla SOPS

This skill covers Mozilla SOPS (Secrets OPerationS). It has deep knowledge of SOPS file encryption, key provider integrations (AWS KMS, GCP KMS, Azure Key Vault, age, PGP), and GitOps workflows with Flux and ArgoCD.

## How to Approach Tasks

When you receive a request:

1. **Classify** the request:
   - **Key provider setup** — AWS KMS, GCP KMS, AKV, age, PGP configuration
   - **Encrypting files** — SOPS encrypt patterns, partial encryption
   - **Decrypting files** — Decrypt, exec-env, exec-file patterns
   - **GitOps** — Flux SOPS integration, ArgoCD Vault Plugin alternative
   - **CI/CD** — GitHub Actions, GitLab CI, Jenkins usage
   - **.sops.yaml config** — Creation rules, key groups, key rotation
   - **Key rotation** — SOPS `updatekeys` and re-encryption

## What SOPS Does

SOPS encrypts **values** in YAML/JSON/ENV/INI files while leaving **keys** (field names) visible. This allows diffs in version control to show which secrets changed without exposing values.

```yaml
# Plaintext
database:
  host: db.example.com
  password: s3cr3t
  username: app_user

# After SOPS encryption
database:
  host: db.example.com                  # NOT encrypted (not a secret)
  password: ENC[AES256_GCM,data=...,iv=...,tag=...,type=str]
  username: ENC[AES256_GCM,data=...,iv=...,tag=...,type=str]
sops:
  kms:
    - arn: arn:aws:kms:us-east-1:123456789:key/abc123
      created_at: '2025-01-01T00:00:00Z'
      enc: AQICAHh...
  lastmodified: '2025-01-01T00:00:00Z'
  mac: ENC[AES256_GCM,data=...,...]
  version: 3.9.0
```

SOPS uses **envelope encryption**: each file is encrypted with a unique DEK (AES-256-GCM), and the DEK is encrypted with each configured master key.

## Installation

```bash
# macOS
brew install sops

# Linux (download binary)
curl -LO https://github.com/getsops/sops/releases/download/v3.9.0/sops-v3.9.0.linux.amd64
chmod +x sops-v3.9.0.linux.amd64
sudo mv sops-v3.9.0.linux.amd64 /usr/local/bin/sops

# Windows (scoop)
scoop install sops

# Go install
go install github.com/getsops/sops/v3/cmd/sops@latest
```

## Key Providers

### AWS KMS

```bash
# Encrypt with AWS KMS key
sops --kms arn:aws:kms:us-east-1:123456789:key/abc123 -e secrets.yaml > secrets.enc.yaml

# Or set environment variable
export SOPS_KMS_ARN="arn:aws:kms:us-east-1:123456789:key/abc123"
sops -e secrets.yaml

# Use alias
sops --kms arn:aws:kms:us-east-1:123456789:alias/my-sops-key -e secrets.yaml
```

Required IAM permissions:
```json
{
  "Effect": "Allow",
  "Action": ["kms:GenerateDataKey", "kms:Decrypt"],
  "Resource": "arn:aws:kms:us-east-1:123456789:key/abc123"
}
```

### GCP KMS

```bash
# Encrypt with GCP KMS
sops --gcp-kms projects/my-project/locations/global/keyRings/my-ring/cryptoKeys/my-key \
    -e secrets.yaml

# Application Default Credentials must be configured
gcloud auth application-default login
```

### Azure Key Vault

```bash
# Encrypt with Azure Key Vault key
sops --azure-kv https://myvault.vault.azure.net/keys/my-key/version-id \
    -e secrets.yaml

# Uses DefaultAzureCredential (managed identity, az login, env vars)
```

### age (Recommended for Simplicity)

age is a modern, simple encryption tool. No key server required — suitable for personal use, small teams, and CI/CD.

```bash
# Install age
brew install age
# or: go install filippo.io/age/cmd/...@latest

# Generate age key pair
age-keygen -o age.key
# Public key printed to stdout: age1xxxxxxxx...
# Private key in age.key: starts with AGE-SECRET-KEY-1

# Encrypt with age public key
sops --age age1xxxxxxxxxxxxxxxxxxxxxxxxxx -e secrets.yaml

# Decrypt (age.key must be accessible)
export SOPS_AGE_KEY_FILE=/path/to/age.key
sops -d secrets.enc.yaml
```

### PGP

```bash
# Encrypt with PGP fingerprint
sops --pgp FINGERPRINT1,FINGERPRINT2 -e secrets.yaml

# List available keys
gpg --list-keys

# Import a public key
gpg --import pubkey.asc
```

## .sops.yaml Configuration

The `.sops.yaml` file defines encryption rules for your repository so you don't need to pass key arguments every time:

```yaml
# .sops.yaml (place in repository root)
creation_rules:
  # Rule 1: Production secrets
  - path_regex: secrets/production/.*\.yaml$
    kms: arn:aws:kms:us-east-1:123456789:key/prod-key
    age: age1xxxxxxxxxxxxxxxxxxxxxxxxxxx  # backup key
    
  # Rule 2: Staging secrets
  - path_regex: secrets/staging/.*\.yaml$
    kms: arn:aws:kms:us-east-1:123456789:key/staging-key
    
  # Rule 3: Any other secrets file (default)
  - path_regex: .*\.enc\.yaml$
    kms: arn:aws:kms:us-east-1:123456789:key/default-key
    age: age1xxxxxxxxxxxxxxxxxxxxxxxxxxx
    
  # Rule 4: Environment files
  - path_regex: .*\.env$
    kms: arn:aws:kms:us-east-1:123456789:key/default-key
```

With `.sops.yaml`, simply run:
```bash
sops -e secrets/production/db.yaml  # Uses prod-key automatically
sops -d secrets/production/db.yaml
```

### Key Groups

Require multiple keys for decryption (Shamir-like threshold):

```yaml
creation_rules:
  - path_regex: secrets/production/.*\.yaml$
    key_groups:
      - kms:
          - arn: arn:aws:kms:us-east-1:123456789:key/key1
          - arn: arn:aws:kms:us-west-2:123456789:key/key2  # multi-region backup
        age:
          - age1xxxxxxxxxxxxxxxxxxxxxxxxxxx
    # shamir_threshold: 2  # (default: any one key group can decrypt)
```

## Basic Operations

```bash
# Encrypt a file (in-place)
sops -e -i secrets.yaml

# Encrypt to new file
sops -e secrets.yaml > secrets.enc.yaml

# Decrypt (to stdout)
sops -d secrets.enc.yaml

# Decrypt in-place (modifies file)
sops -d -i secrets.enc.yaml

# Edit encrypted file (opens in $EDITOR with decrypted content, re-encrypts on save)
sops secrets.enc.yaml

# Encrypt only specific keys (partial encryption)
sops --encrypted-regex "^(password|apiKey|secret)$" -e secrets.yaml

# Encrypt only a specific file format
sops -e --input-type json --output-type yaml secrets.json > secrets.enc.yaml
```

## Partial Encryption

By default, SOPS encrypts all string values in YAML/JSON. Control this with regexes:

```yaml
# .sops.yaml
creation_rules:
  - path_regex: configs/.*\.yaml$
    encrypted_regex: "^(password|apiKey|secretKey|token|privateKey)$"
    kms: arn:aws:kms:us-east-1:123456789:key/my-key
```

Or pass at command line:
```bash
# Only encrypt fields matching the regex
sops --encrypted-regex "^(password|secret)$" -e config.yaml

# Unencrypted suffix (leave .public fields unencrypted)
sops --unencrypted-suffix "_public" -e config.yaml
```

## Running Commands with Decrypted Secrets

```bash
# exec-env: decrypt and inject as environment variables, then run command
sops exec-env secrets.enc.yaml 'node server.js'

# exec-file: decrypt to temp file, pass filename to command, delete after
sops exec-file secrets.enc.yaml 'app --config {}'
# {} is replaced with the temp file path

# Decrypt to env and run with shell
sops -d --output-type dotenv secrets.enc.yaml | source /dev/stdin && node server.js
```

## GitOps Integration

### Flux SOPS Integration

Flux has native SOPS support. Flux decrypts SOPS-encrypted files at apply time.

```bash
# Create Flux secret with age private key
kubectl create secret generic sops-age \
    --namespace flux-system \
    --from-file=age.agekey=/path/to/age.key

# Add decryption config to Flux Kustomization
```

```yaml
# flux-kustomization.yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: apps
  namespace: flux-system
spec:
  sourceRef:
    kind: GitRepository
    name: flux-system
  path: ./apps/production
  decryption:
    provider: sops
    secretRef:
      name: sops-age  # Secret containing age.agekey
```

Files in `./apps/production` that are SOPS-encrypted with the corresponding age public key will be automatically decrypted by Flux.

### ArgoCD Integration

ArgoCD does not have native SOPS support, but supports it via:

**ArgoCD Vault Plugin (AVP)**: AVP supports SOPS as a backend — annotate manifests with SOPS references.

**KSOPS (Kustomize + SOPS)**: A Kustomize exec plugin that decrypts SOPS files during Kustomize rendering.

```yaml
# kustomization.yaml with KSOPS
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
generators:
  - ./secrets-generator.yaml
  
---
# secrets-generator.yaml
apiVersion: viaduct.ai/v1
kind: ksops
metadata:
  name: secret-generator
  annotations:
    config.kubernetes.io/function: |
      exec:
        path: ksops
files:
  - ./secrets.enc.yaml
```

## Key Rotation

When a key is compromised or a team member leaves:

```bash
# Update to new key (re-encrypts all DEKs without touching ciphertext)
sops updatekeys secrets.enc.yaml

# Remove old key, add new key in .sops.yaml first, then:
sops rotate secrets.enc.yaml

# Rotate all files matching a pattern
find . -name "*.enc.yaml" -exec sops rotate {} \;
```

`updatekeys` re-reads the current `.sops.yaml` creation rules and re-encrypts the file's DEK with the new set of keys. The actual encrypted data is not changed.

## CI/CD Patterns

### GitHub Actions with AWS OIDC

```yaml
name: Deploy
on: [push]
permissions:
  id-token: write  # OIDC token for AWS auth
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure AWS credentials (OIDC)
      uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: arn:aws:iam::123456789:role/github-actions-role
        aws-region: us-east-1
    
    - name: Install SOPS
      run: |
        curl -LO https://github.com/getsops/sops/releases/latest/download/sops-linux-amd64
        sudo install sops-linux-amd64 /usr/local/bin/sops
    
    - name: Decrypt and deploy
      run: |
        sops exec-env secrets/production/app.enc.yaml './deploy.sh'
```

### GitHub Actions with age

```yaml
- name: Decrypt secrets
  env:
    SOPS_AGE_KEY: ${{ secrets.SOPS_AGE_KEY }}  # age private key stored in GitHub secrets
  run: |
    echo "$SOPS_AGE_KEY" > /tmp/age.key
    export SOPS_AGE_KEY_FILE=/tmp/age.key
    sops exec-env secrets/production/app.enc.yaml 'node deploy.js'
    rm -f /tmp/age.key
```

## Common Mistakes

| Mistake | Fix |
|---|---|
| Committing unencrypted secrets | Add `*.yaml` to `.gitignore`, only commit `*.enc.yaml` |
| Using PGP with expired keys | Prefer age (no expiry concept) or KMS |
| Encrypting entire file including field names | Use `--encrypted-regex` to only encrypt values |
| No `.sops.yaml` | Create one so team doesn't need to remember key ARNs |
| Losing the age private key | Store in a separate secrets manager (1Password, Vault) |
| Not rotating after team member leaves | Run `sops rotate` on all encrypted files after key rotation |
