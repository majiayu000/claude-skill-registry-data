---
name: kit-hardening
description: Harden the security configuration in the user's repository, including HTTP security headers and Content Security Policy, CORS, cookie flags, TLS and redirect settings, Dockerfiles, CI workflow permissions, dependency pinning, and secret handling, as a blue-team defensive task. Use when the user asks to harden, lock down, or secure an application's or repository's configuration, add security headers, or tighten CORS, cookies, containers, or CI permissions. Do not use for finding vulnerabilities in application logic (use kit-security-audit), for writing new Dockerfiles or pipelines without a security goal, or for changing live infrastructure.
---

# Hardening

Change files in the repository only; do not modify live systems, cloud settings, or secrets.

## 1. Inventory the configuration

Find the web framework and its security middleware (Helmet, `@fastify/helmet`, Django `SECURE_*` settings, Starlette middleware), CORS and cookie settings, reverse proxy configuration, Dockerfiles and compose files, CI workflows, dependency manifests, and how secrets reach the app.

## 2. Harden

- **Headers:** `Strict-Transport-Security` (with care for subdomains), `Content-Security-Policy` that starts strict and lists the sources the app actually uses, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, and frame protection (`frame-ancestors`). Remove `X-Powered-By` and version banners.
- **CORS:** an explicit origin allowlist; never reflect arbitrary origins together with credentials.
- **Cookies:** `Secure`, `HttpOnly` for session cookies, and `SameSite=Lax` or `Strict`; short session lifetimes where appropriate.
- **Errors and debug:** debug mode, stack traces, and docs endpoints disabled or protected in production configuration.
- **Containers:** pinned base images (digest or exact tag), a non-root `USER`, no secrets in layers or build args, a minimal runtime image, and a `.dockerignore` that excludes `.env` and `.git`.
- **CI:** least-privilege `permissions:` per workflow or job, third-party actions pinned to a commit SHA (if you cannot look the SHA up, keep the tag, mark it, and give the user the command to resolve it, such as `gh api repos/<owner>/<repo>/commits/<tag> --jq .sha`), never checking out or running pull request code under `pull_request_target` or `workflow_run` (use `pull_request` for untrusted code), `persist-credentials: false` on checkout, and untrusted input never interpolated into `run:` scripts.
- **Secrets and dependencies:** no committed secrets (`.env` in `.gitignore`, example files without real values); a secret that was already committed must be rotated by the user, because removing or untracking it does not revoke it; lockfiles committed, and automated dependency updates if the project uses them.

## 3. Verify

Run the app's tests, and add tests that assert important headers and cookie flags where the project has HTTP tests. Build the container if one changed. Check that a strict CSP does not break pages the project serves; relax it only for named sources.

## 4. Report

List each change with its reason, the checks run, every action still on a tag with the exact command that resolves its commit SHA (`gh api repos/<owner>/<repo>/commits/<tag> --jq .sha`), anything that could break clients (CSP, CORS, `SameSite`), and remaining items that need infrastructure changes outside the repository.

## Examples

- Use: "Add security headers to the Express app." "Lock down our GitHub Actions permissions." "Harden this Dockerfile."
- Skip: "Find vulnerabilities in the login code." (kit-security-audit) "Change the production firewall rules."
