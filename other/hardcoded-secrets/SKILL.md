---
name: hardcoded-secrets
description: Detects API keys, passwords, tokens, and credentials embedded directly in
  source code. Use when writing code that contains API keys, passwords,
  tokens, connection strings, or private keys as string literals. Also invoke
  when embedding credentials in configuration files, environment setup
  scripts, or test fixtures that could be committed to version control.
---

# Hardcoded Secrets Security Check (CWE-798)

## What this checks

Protects against credentials, API keys, and secrets embedded directly in source code.
Hardcoded secrets end up in version control history, build artifacts, and container
images. Once committed, secrets are effectively public — even if the commit is reverted,
the secret remains in git history.

## Vulnerable patterns

- String literal that resembles a production API key, access token, or session secret assigned to a constant
- Hardcoded password or shared-secret literal used as the only credential check
- Connection string with embedded username and password committed to source
- Private key material (PEM, PKCS#8, SSH) pasted inline as a string literal
- Cloud-provider access keys, OAuth client secrets, or webhook signing keys in source or config files

## Fix immediately

Flag the hardcoded secret and explain the risk. Translate the principles below to the
audited file's language and deployment environment — use that stack's documented secret
loader, env-var helper, or secrets-manager client.

For each finding, establish these properties:

1. **Secrets are loaded from outside the source tree.** Environment variable,
   secrets manager (AWS Secrets Manager, HashiCorp Vault, 1Password), KMS, or OS
   keystore. No string literal that resembles a real credential appears in source
   — not in code, not in config files, not in test fixtures.
2. **Missing secrets fail loudly at load time, not silently at first use.** A
   required-env lookup with no fallback, a required-field check, or an early
   fatal log guarantees a misconfigured deploy crashes immediately rather than
   running with an empty string that mysteriously fails later.
3. **Test fixtures use obviously fake values** — placeholder strings that read as
   "do not use" — that cannot be mistaken for production credentials and will
   never unlock a real service if leaked.
4. **Rotation does not require a code change.** If rotating the credential means
   editing source and redeploying, the secret is effectively hardcoded even if
   it's technically loaded through a constant. Rotation happens by updating the
   external store and restarting.

## Verification

- [ ] No string literal in the code resembles a production API key, password, token, private key, or connection string with embedded credentials
- [ ] All credentials are loaded from environment variables, secrets managers, or encrypted configuration — never from source code
- [ ] Test fixtures use obviously fake values that cannot be mistaken for real credentials

## References

- CWE-798 ([Use of Hard-coded Credentials](https://cwe.mitre.org/data/definitions/798.html))
- CWE-259 ([Use of Hard-coded Password](https://cwe.mitre.org/data/definitions/259.html))
