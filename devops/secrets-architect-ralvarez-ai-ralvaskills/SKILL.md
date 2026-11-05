---
name: secrets-architect
version: 1.1.1
description: Secret-handling standards for one external store consumed by reference — consumer decision matrix (Compose secrets, *_FILE, systemd LoadCredential, plain bind mount, CI), permission/uid rules, naming, migration workflow, live verification, pitfalls. Use when wiring a credential into a repo, container, systemd unit or CI job, migrating secrets out of .env or git, or auditing a secrets store.
---

# Secrets Architect

**Every credential lives in one secrets store, outside every repo. Consumers read it by reference — never a copied value.** No secret value in git, in a `.env`, or in a container environment.

Targets **`$SECRETS_DIR`** (default `~/Secrets`) as the store. The canonical long-form walkthrough — the full narrative, verification log and instance layout — lives in the chezmoi repo's `docs/secrets-methodology.md`; this skill is the portable, agent-facing core.

## 1. Principles

- **One store, many consumers.** `$SECRETS_DIR` is the single source of truth; repos reference paths, never values.
- **Match the mechanism to the consumer** (see §3). The consumer's shape — file reader, env app, oneshot, shell, writable state, CI — picks the mechanism.
- **Paths have a default.** Build from `${SECRETS_DIR:-$HOME/Secrets}` so a stack works without a per-secret variable being defined.
- **Least privilege, but respect the reader's uid.** Default `600`, except files a non-root process opens directly.
- **Verify against the running system, not just the source.** The deployed artifact can lag the repo.
- **Nothing changes without a live check.** Config-render, recreate, and prove the secret was actually used.

## 2. The store: layout and permissions

Layout is **by kind, then owner** (`<kind>/<owner>/<name>`):

```
$SECRETS_DIR/                  # 0700
├── cloudflare/
│   ├── api/ddns-token         # 0600  API tokens
│   ├── tunnels/<tunnel-name>  # 0644  tunnel tokens (non-root reader)
│   └── r2/<owner>/…
├── github/{contents-read,ci-modules}
├── finance-platform/{postgres-password,database-dsn,jwt-secret,…}
├── ssh/  gpg/  bitwarden/  vpn/wireguard/  ...
```

- **Dirs `700`, files `600`**, enforced by a `secrets:perms` task that walks the *whole* store (never a hardcoded list), then audits `find -perm /022` and `find -type f ! -name '*.pub' ! -name known_hosts -perm /044` — a clean store prints nothing.
- **Direct-open `644` exceptions** (enclosing `0700` dirs still contain them): public keys / `known_hosts`, and **any file a non-root container reads directly** through a Compose-secret bind mount. cloudflared (`65532`) and the finance-platform backend (`65532`) both read their secrets this way, so `600` is unreadable to them. Check the reader's uid (`docker inspect <ctr> --format '{{.Config.User}}'`) before choosing the mode, and list the directory in `secrets:perms`'s `644` set.
- **Verify a secret's content**, not its filename — a public key saved as the private key silently breaks push.

## 3. Consumer decision matrix

| Consumer | Mechanism | Key details |
|---|---|---|
| Container reads a file (runtime) | **Compose `secrets:`** | `secrets: <name> { file: ${SECRETS_DIR}/… }`; container sets `<VAR>_FILE: /run/secrets/<name>`. |
| Docker **build** reads a secret | Compose `build.secrets` → **`environment: VAR`** | **Never `file:` outside the build context** — BuildKit/Bake's `fs.read` sandbox refuses it on `docker compose build` (`additional privileges requested: pass --allow=fs.read=…`). Source from the environment. |
| App reads env vars, supports `_FILE` | **`<VAR>_FILE`** | Read `<VAR>_FILE` → set `<VAR>`. Verify the *image* supports it. |
| Postgres | `POSTGRES_PASSWORD_FILE` | Supported by the official / timescale image. |
| systemd oneshot | **`LoadCredential=`** | `LoadCredential=id:%h/Secrets/…`; script reads `$CREDENTIALS_DIRECTORY/id`. tmpfs, `0400`, unit-only. |
| Shell / go-task | `$SECRETS_DIR` path | go-task: `SECRETS_DIR: '{{.HOME}}/Secrets'`. |
| Writable runtime state | **Plain writable bind mount** | Compose `secrets:` and `LoadCredential` are read-only. |
| CI | Host repo secret | `docker/build-push-action` `secret-files:` / `--secret id=…,env=…`. |

**Compose secret shape:**

```yaml
services:
  cloudflared-shared:
    environment:
      TUNNEL_TOKEN_FILE: /run/secrets/homelab-shared-tunnel-token
    secrets:
      - homelab-shared-tunnel-token
secrets:
  homelab-shared-tunnel-token:
    file: ${SECRETS_DIR}/cloudflare/tunnels/homelab-shared
```

**Build vs runtime secrets.** A `file:` secret works at *runtime* (the daemon bind-mounts the host file) but not as a *build* secret when the path is outside the build context — Bake refuses to read it. For `build.secrets`, use `environment: VAR` and have the caller export `VAR` (chezmoi's shell does). Two scopes are usually needed: Go modules want `contents:read` (`GH_PRIVATE_MODULES_TOKEN`), npm `@scope/*` packages want `read:packages` (`NODE_AUTH_TOKEN`) — separate secrets.

**Path preference:** put the default in the compose file (`${SECRETS_DIR}/…`) and keep `SECRETS_DIR=${SECRETS_DIR:-$HOME/Secrets}` once in the stack `.env` — then `.env` needs no per-secret variable. Nested defaults `${A:-${B:-C}}` work in Compose.

**systemd unit shape:**

```ini
[Service]
LoadCredential=ddns-token:%h/Secrets/cloudflare/api/ddns-token
# script: TOKEN_FILE="${CREDENTIALS_DIRECTORY:-}/ddns-token" (fallback to $SECRETS_DIR for ad-hoc runs)
```

## 4. Naming conventions

- Path-holding variables end in **`_FILE`**; the container variable mirrors the app's expectation (`TUNNEL_TOKEN_FILE`, `POSTGRES_PASSWORD_FILE`).
- Prefer a **specific** name over a generic one (`CLOUDFLARE_HOMELAB_SHARED_TUNNEL_TOKEN_FILE`, not `CLOUDFLARE_TUNNEL_TOKEN`).
- Secret file names are lowercase, hyphenated, no extension (`postgres-password`, `jwt-secret`, `access-key-id`).

## 5. Migration workflow (per secret)

1. **Inventory the consumer** — `git grep` the token/var; classify: container file / env app / systemd / shell / writable state / CI.
2. **Place the secret** under `<kind>/<owner>/<name>`, `600`.
3. **Decide the mechanism** from §3. For a container, check the reader's uid (`docker inspect <ctr> --format '{{.Config.User}}'`) → choose `600` or `644`. For a *build* secret, never `file:` outside the context — source from the environment.
4. **Wire the consumer** to `${SECRETS_DIR}/…` (Compose secret / `LoadCredential` / `*_FILE`).
5. **Remove the value** from `.env` / repo; leave only the path (or nothing, if compose has the default).
6. **Verify** (§6). **Document** in the repo's Secrets section. **Commit** per repo.

## 6. Verification checklist

- **Config renders:** `docker compose -f <stack>/compose.yml config` (with `SECRETS_DIR` unset) → `file:` resolves to the store path, container `*_FILE` is set.
- **Permissions suffice for the reader:** the container uid can open the file (`600` needs owner uid; non-root → `644`).
- **Recreate + observe:** `up -d` → logs show `Registered tunnel connection`, `listening`, healthy.
- **Prove the credential path, not a fallback:** run under systemd with the fallback pointed at `/nonexistent` — success means the credential path was taken.
- **Compare store vs live without printing values:** `sha256sum` of the trimmed file vs the container env var.
- **Round-trip the data path:** run the real job and confirm the off-box upload.
- **Build secret reachable:** run `docker compose build` (not just `config`) — a `file:` build secret outside the context fails with `additional privileges requested`, an `environment:`-sourced one succeeds.

## 7. Pitfalls

1. **The deployed image can lag the repo.** `_FILE` support in the working tree but in no tag / published image means it isn't there. Check the artifact (`git tag --contains`, image symbols). If it lags, keep a transitional inline fallback and mark it for removal.
2. **Compose `secrets:` on non-swarm is a bind mount.** The container reads the host file *directly* with its own uid; `mode:`/`uid:`/`gid:` are ignored — only the host file mode matters.
3. **systemd `EnvironmentFile` does not expand variables.** `$SECRETS_DIR` stays literal — use `%h/Secrets/…`, or `LoadCredential`.
4. **`LoadCredential` specifiers:** `%h` expands in a real unit but *not* via `systemd-run -p LoadCredential=…` ("Credential source is invalid").
5. **Moving a bind-mounted file doesn't affect a running container** — it keeps the pinned inode until recreated, so "it still works" is not proof.
6. **Don't blanket `chmod 600`.** One non-root reader (cloudflared `65532`) breaks.
7. **`.env` interpolation is inconsistent.** Compose expands `${VAR}` (and nested defaults); go-task supports `{{.HOME}}`; systemd does not expand at all.
8. **Verify secret content** — a public key saved as the private key silently breaks push.
9. **CI ≠ local.** CI uses `docker/build-push-action`/`buildx`, not Compose; changing a Compose `file:` doesn't touch CI.
10. **Editing discipline.** Exact-match edits + `git diff` verification; never edit the same file in parallel; re-read after every structural edit.
11. **Build secrets and the fs.read sandbox.** A `file:` build secret (Compose `build.secrets`) whose path is outside the build context fails on `docker compose build` — Bake wants `--allow=fs.read=…`. Source it from the environment (`environment: VAR`) instead; runtime `file:` secrets are unaffected.
12. **Go modules and npm packages are different tokens.** `contents:read` for the Go module fetch, `read:packages` for `@scope/*` npm packages; one token can't serve both. Wire `github_token` and `packages_token` separately.
13. **A Dockerfile's `go build` step needs the token too.** The `go mod download` cache mount isn't shared with a later `go build` run, so mount the secret on both or the build fetches anonymously and fails.
14. **An `environment:`-sourced secret needs the caller to export the var.** chezmoi's shell exports `GH_PRIVATE_MODULES_TOKEN` / `NODE_AUTH_TOKEN`; a bare `docker compose build` outside that shell needs them set.

## 8. Out of scope

- **Container / Compose mechanics** → [`docker-architect`](../docker-architect/SKILL.md).
- **CI secret injection, OIDC over long-lived secrets** → [`ci-cd-architect`](../ci-cd-architect/SKILL.md).
- **Detecting leaked secrets in a diff** → [`security-reviewer`](../../quality/security-reviewer/SKILL.md).
- **Task runner / dotenv wiring** → [`repo-tooling-architect`](../../tooling/repo-tooling-architect/SKILL.md).
