---
name: vault
description: "Configure Vault secret engines, policies, AppRole or Kubernetes authentication, and dynamic credential leases."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["vault", "hashicorp", "secrets", "approle", "kv", "encryption"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# HashiCorp Vault Secrets AI Skill Guide

## Overview

Vault centralizes secrets, encryption keys, and dynamic credentials behind authenticated policies. Clients authenticate (token, AppRole, Kubernetes, cloud IAM), then read paths allowed by **ACL policies**. Agents must never log secret values, prefer short-lived dynamic credentials, and treat root tokens as break-glass only.

```
Auth method (AppRole / K8s / OIDC)
        |
        v
+----------------+     ACL policy      +------------------+
| Vault token    | ------------------> | KV / DB / PKI    |
| + lease        |                     | Transit encrypt  |
+----------------+                     +------------------+
```

## When to use

- Designing KV v2 layouts and least-privilege policies
- Wiring AppRole or Kubernetes auth for apps and CI
- Issuing dynamic database credentials or PKI certificates
- Rotating secrets and revoking leases during incidents

## Operational directives

1. Never paste root tokens, unseal keys, or secret payloads into chat.
2. Prefer KV v2 with versioning; use `cas` when concurrent writers exist.
3. Grant capabilities (`read`, `list`, `create`) on the narrowest path prefixes.
4. Renew/revoke leases explicitly for dynamic secrets; do not orphan credentials.
5. Use namespaces (Enterprise) or path prefixes for team isolation in OSS designs.

## Concrete examples

### KV v2 write/read

```bash
vault secrets enable -path=secret kv-v2
vault kv put secret/api/prod DATABASE_URL=postgres://...
vault kv get -format=json secret/api/prod
vault kv metadata get secret/api/prod
```

### Minimal policy

```hcl
path "secret/data/api/prod" {
  capabilities = ["read"]
}
path "secret/metadata/api/prod" {
  capabilities = ["read"]
}
```

```bash
vault policy write api-prod api-prod.hcl
```

### AppRole for CI

```bash
vault auth enable approle
vault write auth/approle/role/ci \
  token_policies="api-prod" \
  token_ttl=15m \
  token_max_ttl=1h
vault read auth/approle/role/ci/role-id
vault write -f auth/approle/role/ci/secret-id
```

### Kubernetes auth sketch

```bash
vault auth enable kubernetes
vault write auth/kubernetes/role/api \
  bound_service_account_names=api \
  bound_service_account_namespaces=api \
  policies=api-prod \
  ttl=20m
```

## Incident table

| Event | Response |
| :--- | :--- |
| Leaked token | `vault token revoke` / orphan revoke; rotate |
| Leaked static KV | Write new version; purge dependents; audit |
| DB lease abuse | `vault lease revoke -prefix` for path |
| Sealed vault | Controlled unseal by operators only |

## Best practices

1. Enable audit devices early; protect audit logs from secret echo where possible.
2. Prefer dynamic DB secrets over long-lived passwords in KV.
3. Automate rotation drills; document break-glass without storing root in Git.
4. Use Transit for application-level encryption when you need crypto without owning keys.

## Limitations

- Vault availability is critical path - plan HA/storage backend carefully.
- Mis-scoped policies are common; always test with a non-admin token.
- Agents must not invent production unseal or recovery key procedures casually.

## Related skills

- `kubernetes` - K8s auth and secret injector patterns
- `consul` - often paired for service discovery / storage discussions
- `mysql` - dynamic DB credential backends
- `lets-encrypt` - PKI alternative for public TLS (Vault PKI for internal)
