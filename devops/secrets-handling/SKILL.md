---
name: secrets-handling
description: "What never enters a repository, a log, a transcript, an issue or a pull request, and how a leaked secret gets handled. Use when touching a credential, a token, a kubeconfig, a state file or anything a secret manager should hold instead."
---

# Secrets handling

A secret never enters a repository, a log, a commit message, an issue, a pull request or a
chat answer.

## When to use

- Before adding configuration that carries a credential.
- Wiring authentication for a tool, a workflow or a cluster.
- A secret may have leaked.

## Rules

### Never commit

- Tokens, passwords, private keys, certificates with their key, kubeconfigs, talosconfigs.
- `.env` files. Commit `.env.example` with empty or obviously fake values instead.
- `secrets.tfvars`, `secrets.auto.tfvars` and their `.json` forms. Every other tfvars file
  holds configuration and may be read, edited and committed.
- OpenTofu state and state backups. State lives in a remote backend.
- Anything a secret scanner would flag. A fake value looks fake, for example `token: changeme`.

### Where secrets live

- Clusters and infrastructure: OpenBao or Vault is the source of truth for a key value secret.
  Kubernetes Secrets are populated from it, never hand written into a values file.
- Local development and shared credentials: the organisation's Bitwarden vault, read through its
  CLI, never pasted into a file.
- CI: repository secrets or OIDC federation. Prefer OIDC and short lived credentials over a long
  lived token.
- OpenTofu: a secret input is a variable marked `sensitive = true`, supplied from the environment
  or the secret store, never a default in code. Wrap a derived secret value in `sensitive()` and
  mark the output `sensitive = true` too. A secret never reaches a plain state output.
- Deployed application config: the environment and flags, no dedicated config file format, no
  remote config client.
- Secret-carrying variables: every one has a `_FILE` twin, for example `DATABASE_PASSWORD` and
  `DATABASE_PASSWORD_FILE`. A set `_FILE` variable wins: read the value from that path. The
  plain variable stays the local development fallback.
- Secret manager clients: application code never links a secret manager SDK or client library.
  The backend stays an infrastructure concern. OpenBao, External Secrets, a Kubernetes secret
  mount and a compose `.env` file all satisfy the same `_FILE` contract with no code change.

### Handling them in a session

- Do not read a secret into context when a reference suffices. Pass it through the environment.
- A command that only prints a secret is denied by the sandbox. Use a tool that consumes the
  secret internally instead of one that echoes it for a human to copy.
- Do not print a secret for confirmation and do not include it in a diff summary.
- Mask or truncate anything credential shaped when quoting command output.
- When a secret is needed and none is available through the secret manager, ask for it through
  the tool that will use it. Never paste it into the chat.
- Declining to touch a secret is better than handling it carelessly.

### If a secret leaked

1. Rotate it first. The secret is compromised the moment it reached git, independent of history.
2. Remove it from the code and from every value still derived from it.
3. Decide about rewriting history separately. Rotation is mandatory, rewriting is its own call
   and needs confirmation, since it rewrites published commits.
4. Record what leaked, where it was used, and when it was rotated.

## Guardrails

- Never print, log or paste a secret, in any tool, for any reason.
- Never commit a state file, a kubeconfig, a talosconfig or an `.env` file.
- Never give an OpenTofu secret input a default value in code.
- A leaked secret gets rotated before anything else happens to it.

## References

- `git-conventions` for what a commit or a pull request must otherwise follow.
- `opentofu-conventions` for sensitive variables and outputs in detail.
