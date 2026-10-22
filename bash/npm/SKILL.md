---
name: npm
description: >-
  Handles npm registry and account tasks: npm whoami, package availability, reserving names,
  publishing, org checks, and auth debugging, with 1Password and tmux for credentials. Use when
  publishing to npm or diagnosing npm login problems.
source: "https://github.com/steipete/agent-scripts"
attribution: "steipete/agent-scripts by Peter Steinberger"
version: "1.0.0"
license: MIT
---

# npm

> **Attribution:** Sourced from [steipete/agent-scripts](https://github.com/steipete/agent-scripts) by [Peter Steinberger](https://github.com/steipete).

## When to Use

- Checking npm login status, package availability, or org membership
- Publishing packages to the npm registry
- Managing npm auth with 1Password/tmux integration

Use for npm registry/account tasks: `npm whoami`, package availability, package reservation, publish, org checks, and auth debugging.

## Auth

- Use 1Password skill first for secret rules.
- Never run `op` directly in the shell tool.
- Known npm 1Password item: `npmjs` on `my.1password.com`.
- The item may contain username/password/TOTP, not a stored npm token.
- Explicit user requests to `release`, `publish`, or `npm publish` are consent to complete npm auth.
- Still stop and ask if the `npmjs` item is missing, the account/vault is ambiguous, credentials are malformed, npm denies package access, or the requested package/version does not match the repo release target.
- Run npm auth work inside one persistent tmux session. Reuse it on failure.
- Keep npm auth in a temp npmrc; delete it after the command.

## Package Reservation

What a reservation script does:
- reads npm credentials once via `op`
- creates an npm registry session from username/password/TOTP
- publishes `0.0.0` placeholder packages with a generic README
- continues after per-package publish failures
- redacts tokens/OTP in logs
- cleans temp npmrc/work dirs

Notes:
- npm may reject names as too similar to already-published names. Treat that as a registry policy result, not an auth failure.
- npm CLI prompt piping is brittle on npm 11. Prefer the helper's registry API login path over scripted `npm login`.
- For scoped packages, `npm view` can lag/404 even when the package exists. Check `npm access get status <pkg>`; `public` or a publish failure saying `previously published versions` means the name is reserved.

## Common Commands

```bash
npm whoami
npm view <package-name>
npm access get status <package-name>
npm publish --access public
```
