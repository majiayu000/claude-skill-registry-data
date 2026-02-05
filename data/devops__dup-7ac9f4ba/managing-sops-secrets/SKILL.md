---
name: managing-sops-secrets
description: Manages SOPS-encrypted Kubernetes secrets for Flux GitOps deployments using age encryption
---

# Managing SOPS Secrets

This skill handles creation, editing, and troubleshooting of SOPS-encrypted secrets in the Superbloom Flux repository.

## Capabilities

- Encrypt new secrets with SOPS
- Decrypt and edit existing secrets
- Troubleshoot encryption/decryption issues
- Manage .sops.yaml configuration

## Configuration

SOPS config location: `flux/.sops.yaml`

```yaml
creation_rules:
  - path_regex: 'clusters/superbloom/.*/secrets.yaml'
    encrypted_regex: '^(data|stringData)$'
    age: ['<your-age-public-key>']
```

This encrypts `data` and `stringData` fields in any `secrets.yaml` under `clusters/superbloom/`.

## Operations

### View Decrypted Secret
```bash
cd flux
sops -d clusters/superbloom/apps/<app>/secrets.yaml
```

### Edit Secret (Interactive)
```bash
cd flux
sops clusters/superbloom/apps/<app>/secrets.yaml
# Opens in $EDITOR, auto-encrypts on save
```

### Edit Secret (Scripted)
```bash
cd flux

# Decrypt to temp file
sops -d clusters/superbloom/apps/<app>/secrets.yaml > /tmp/secrets.yaml

# Edit
vim /tmp/secrets.yaml
# or: sed -i 's/old/new/' /tmp/secrets.yaml

# Copy back and encrypt
cp /tmp/secrets.yaml clusters/superbloom/apps/<app>/secrets.yaml
sops --encrypt --in-place clusters/superbloom/apps/<app>/secrets.yaml

# Clean up
rm /tmp/secrets.yaml
```

### Create New Encrypted Secret
```bash
cd flux

# Create plaintext
cat > clusters/superbloom/apps/<app>/secrets.yaml << 'EOF'
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
  namespace: my-app
type: Opaque
stringData:
  API_KEY: example-api-key-replace-me
  DATABASE_URL: postgres://user:example@host/db
EOF

# Encrypt in place
sops --encrypt --in-place clusters/superbloom/apps/<app>/secrets.yaml
```

## Secret Structures

### Simple Key-Value Secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-env
  namespace: app
type: Opaque
stringData:
  API_KEY: REPLACE_WITH_REAL_VALUE
  DB_PASSWORD: REPLACE_WITH_REAL_VALUE
```

### HelmRelease Values Secret (bjw-s app-template)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: app
type: Opaque
stringData:
  values.yaml: |
    controllers:
      main:
        serviceAccount:
          name: app
        containers:
          main:
            image:
              repository: ghcr.io/saavy1/app
              tag: latest
            env:
              SECRET_KEY: "REPLACE_WITH_REAL_VALUE"
    service:
      main:
        controller: main
        ports:
          http:
            port: 3000
```

### Multiple Documents
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-helm-values
  namespace: app
type: Opaque
stringData:
  values.yaml: |
    # helm values
---
apiVersion: v1
kind: Secret
metadata:
  name: app-env
  namespace: app
type: Opaque
stringData:
  API_KEY: REPLACE_WITH_REAL_VALUE
```

## Encrypted File Format

After encryption, files look like:
```yaml
stringData:
    API_KEY: ENC[AES256_GCM,data:...,iv:...,tag:...,type:str]
sops:
    age:
        - recipient: <your-age-public-key>
          enc: |
            -----BEGIN AGE ENCRYPTED FILE-----
            <encrypted-key-data>
            -----END AGE ENCRYPTED FILE-----
    lastmodified: "2025-12-14T01:00:00Z"
    mac: ENC[AES256_GCM,...]
    encrypted_regex: ^(data|stringData)$
    version: 3.11.0
```

## Troubleshooting

### "no matching creation rules found"

**Cause**: Running sops from wrong directory or path doesn't match regex

**Fix**: Run from `flux/` directory:
```bash
cd flux
sops --encrypt --in-place clusters/superbloom/apps/<app>/secrets.yaml
```

Or update `.sops.yaml` path_regex to match your file path.

### "could not decrypt" / Key not found

**Cause**: Age private key not available

**Fix**: Ensure key exists:
```bash
cat ~/.config/sops/age/keys.txt
# or
export SOPS_AGE_KEY_FILE=~/.config/sops/age/keys.txt
```

### Flux not decrypting secrets in cluster

**Cause**: Cluster missing sops-age secret

**Check**:
```bash
kubectl get secret sops-age -n flux-system
```

**Fix**: The sops-age secret must contain the private key for cluster-side decryption.

### Changes not reflected after push

**Cause**: Flux hasn't reconciled yet

**Fix**:
```bash
flux reconcile kustomization flux-system --with-source
```

### "expected string, got &value.valueUnstructured{Value:...}"

**Cause**: SOPS preserved a numeric type. Look for `type:int` in the encrypted value:
```yaml
DISCORD_CLIENT_ID: ENC[AES256_GCM,data:...,type:int]  # ← problem
```

When decrypted, this becomes a number, but `stringData` requires strings.

**Fix**: Re-encrypt as string:
```bash
cd flux
sops clusters/superbloom/apps/<app>/secrets.yaml
# In editor, ensure the value is quoted: "1234567890"
# Save - SOPS will re-encrypt with type:str
```

Or decrypt, fix, re-encrypt:
```bash
sops -d clusters/superbloom/apps/<app>/secrets.yaml > /tmp/secrets.yaml
# Edit /tmp/secrets.yaml - quote numeric values: "1234567890"
cp /tmp/secrets.yaml clusters/superbloom/apps/<app>/secrets.yaml
sops --encrypt --in-place clusters/superbloom/apps/<app>/secrets.yaml
rm /tmp/secrets.yaml
```

**Prevention**: Always quote values that look like numbers:
```yaml
stringData:
  DISCORD_CLIENT_ID: "1325902250497020000"  # ← quoted = string
  PORT: "3000"                               # ← quoted = string
```

## Security Notes

- Never commit plaintext secrets
- The age public key (in `.sops.yaml`) is safe to share
- The age private key must be kept secure
- Flux cluster has its own copy of private key
- Clean up temp files: `rm /tmp/secrets.yaml`

## Best Practices

1. Always work from `flux/` directory
2. Verify encryption: look for `ENC[AES256_GCM,...]` patterns
3. Test decryption before committing
4. Use temp files for complex edits
5. Clean up plaintext temp files immediately
