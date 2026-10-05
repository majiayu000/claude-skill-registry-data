---
name: vault-pki
description: Use when vault PKI secrets engine — certificate authority, dynamic certificates,
  certificate rotation. Use when working with vault pki.
domain: devops
author: oyi77
license: Apache-2.0
subdomain: devops
tags:
- ci-cd
- devops
- infrastructure
- pki
- vault
version: 1.0.0
category: devops
---



## Overview

HashiCorp Vault PKI secrets engine acts as a certificate authority (CA), issuing dynamic X.509 certificates on demand. Enables short-lived certificates with automatic rotation.

## Capabilities

- Root and intermediate CA generation
- Dynamic certificate issuance with configurable TTL
- Certificate revocation (CRL, OCSP)
- Role-based certificate policies
- Automatic rotation via Consul Template or sidecar
- Cross-signed intermediate CAs

## When to Use
**Trigger phrases:**
- "vault pki"
- "Vault PKI secrets engine — certificate authority, dynamic certificates, certific"


- Need internal PKI without managing a traditional CA
- Want short-lived certificates (hours, not years)
- Microservices need TLS certificates automatically
- Replacing self-signed certificates with a proper CA

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code

The vault-pki workflow follows a standard pipeline pattern.

Core flow:
```
# vault-pki primary flow
input = prepare(raw_data)
result = process(input, config={authority, certificate, certificates, dynamic, engine})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Enable PKI Backend
```bash
# Enable PKI engine
vault secrets enable pki
vault secrets tune -max-lease-ttl=87600h pki

# Generate root CA
vault write pki/root/generate/internal \
  common_name="My Root CA" \
  ttl=87600h

# Configure URLs
vault write pki/config/urls \
  issuing_certificates="http://vault:8200/v1/pki/ca" \
  crl_distribution_points="http://vault:8200/v1/pki/crl"
```

### Create Role
```bash
vault write pki/roles/web-server \
  allowed_domains="example.com" \
  allow_subdomains=true \
  max_ttl=72h \
  key_type=ec \
  key_bits=256
```

### Issue Certificate
```bash
# Request a certificate
vault write pki/issue/web-server \
  common_name="api.example.com" \
  ttl=24h

# Response includes: certificate, private_key, issuing_ca, serial_number
```

### Certificate Rotation Script
```bash
#!/bin/bash
CERT=$(vault write -format=json pki/issue/web-server common_name="api.example.com" ttl=1h)
echo "$CERT" | jq -r '.data.certificate' > /etc/ssl/cert.pem
echo "$CERT" | jq -r '.data.private_key' > /etc/ssl/key.pem
systemctl reload nginx
```

## Common Patterns

- **Short TTL**: Issue 1h-24h certs, automate rotation
- **Intermediate CA**: Create intermediate for signing, keep root offline
- **Consul Template**: Auto-rotate certs with `{{ with secret "pki/issue/..." }}`
- **Vault Agent**: Sidecar that auto-fetches and rotates certs
- **Role constraints**: `allowed_domains`, `allow_bare_domains`, `not_before_duration`

## How to Use

1. Define infrastructure as code (Terraform, CloudFormation, Pulumi)
2. Review changes through PR process before applying
3. Configure monitoring and alerting for critical paths
4. Set up secrets management (Vault, AWS Secrets Manager, etc.)
5. Document runbooks for deployment, rollback, and incident response
6. Test disaster recovery procedures regularly

## Red Flags

- **Infrastructure changes without review**: Unreviewed changes cause outages — use PRs for infra code
- **No rollback strategy**: Every deployment needs a tested rollback plan before it runs
- **Secrets in configuration files**: Secrets in YAML/JSON get committed to version control
- **Missing monitoring and alerting**: Without monitoring, outages go undetected until users report them
- **No documentation for runbooks**: Without runbooks, on-call engineers waste time re-discovering procedures

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Manual deployments are fine" | Manual deployments are error-prone and不可 repeatable. Automate. |
| "We do not need monitoring" | Without monitoring, you are flying blind. Add observability from day one. |
| "Infrastructure as code is overkill" | IaC enables reproducibility, version control, and disaster recovery. |