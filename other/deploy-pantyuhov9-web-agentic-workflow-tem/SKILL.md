---
name: deploy
description: Deploy a site — local preview, pre-flight checks, or production push. Defaults to Hostinger git auto-deploy (push to main triggers Hostinger pull) with FTP fallback for non-Hostinger sites.
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - TodoWrite
model: sonnet
argument-hint: <"preview" | "check" | "push" | "setup-ci">
---

# Deploy — site deployment lifecycle (entry point)

This skill is the invocation handle for the deploy lifecycle. The full procedure — per-site deploy mechanism, pre-flight, approval gate, FTP fallback, CI setup, and the Cloud-Function redeploy note — is the **single source of truth** in the workflow. This file just routes you there.

## Sub-commands

- `deploy preview` — local preview server
- `deploy check` — pre-flight checks before pushing
- `deploy push` — production deploy (approval-gated)
- `deploy setup-ci` — generate GitHub Actions config (non-Hostinger sites)

## Begin

Read [workflows/site_deploy.md](../../../workflows/site_deploy.md) — authoritative SOP — and execute the section matching `$ARGUMENTS`. Defaults: site root = `--root` or cwd (`~/Sites/<name>/` convention); for sites on a git-auto-deploy host (e.g. Hostinger auto-pull, ~1–2 min), `git push origin main` IS the deploy.

**Non-negotiable** (also in the workflow): approval gate before every push (show diff + detected method) · pass pre-flight first · never force-push · git status clean.

## See also

- [tools/deploy_site.py](../../../tools/deploy_site.py) — FTP/SFTP/rsync deployer (fallback)
- [tools/site_audit.py](../../../tools/site_audit.py) — pre-flight checks
