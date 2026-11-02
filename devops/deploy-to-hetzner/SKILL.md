---
name: deploy-to-hetzner
description: Use when putting a containerized service on Hetzner Cloud with OpenTofu — a VM per environment, Cloud Firewall, private network, hardened cloud-init, Docker Compose with Traefik TLS, deploys by image digest, backups with a restore drill.
---

# Deploy to Hetzner

One VM per environment, hardened by cloud-init, serving a Compose stack behind Traefik. The image, the compose files and the deploy script all ship through the same reviewed pipeline. Contract: [environments.md](../_shared/environments.md), [deploy-script.md](../_shared/deploy-script.md).

## 1. Audit current state (change nothing)

```bash
cat .claude/stack-profile.md 2>/dev/null        # hosting, iac, database.host, ci
ls infra/modules/hetzner-host infra/modules/host-bootstrap deploy/ compose*.y*ml 2>/dev/null
ls deploy/stack deploy/host deploy/envs 2>/dev/null
hcloud context list 2>/dev/null                 # context names only, never token values
[[ -n "${HCLOUD_TOKEN:-}" ]] && echo "HCLOUD_TOKEN set" || echo "HCLOUD_TOKEN unset"
tofu version 2>&1 | head -1
```

Read from the profile: `hosting` (must list `hetzner`), `iac` (opentofu), `database.host`, `ci`. If there is no profile, detect from the `infra/` and `deploy/` trees above. Never ask what the profile already answers.

## 2. Decide

- Profile says `hosting` is `vercel` or `ionos` (and not `hetzner`): stop. Point to [deploy-to-vercel](../deploy-to-vercel/SKILL.md) or [deploy-to-ionos](../deploy-to-ionos/SKILL.md).
- No image yet (`containerize-service` has not produced a digest): run [containerize-service](../containerize-service/SKILL.md) first; this skill deploys a digest, not a build.
- No `infra/modules/hetzner-host` and no `deploy/`: full (steps 3 to 7).
- Modules exist but a piece is missing (no `deploy/stack/bin/backup.sh`, no `deploy/envs`): delta, add only the missing piece.
- Modules, deploy layout, GitHub environments, DNS and backups all present and verified: "already in place", run step 7, stop.

## 3. Detect the track

- **Single VM Compose (default):** one VM per environment, one Compose project on it. Use this unless a trigger below is met.
- **Graduate to k3s:** do not build k3s here. The triggers (more than one VM per environment behind a load balancer, rolling zero-downtime needs, several teams, node-level failure tolerance) and the k3s target (`v1.37.1+k3s1`) are in [hetzner-patterns.md](./hetzner-patterns.md#rule-graduate-to-k3s-only-on-these-triggers). This skill stops at the Compose host.

## 4. Install only what is missing

```bash
brew install hcloud        # 1.70.1; or mise use hcloud@1.70.1
```

OpenTofu 1.13.1 through [set-up-opentofu](../set-up-opentofu/SKILL.md) — run it first, or in the same change. It writes the `infra/` roots, encrypted remote state, `TF_ENCRYPTION`, the CI gate and drift detection. This skill adds the Hetzner modules on top.

## 5. Generate the seams

1. **Modules** `infra/modules/hetzner-host` and `infra/modules/host-bootstrap`, plus one environment root (`infra/envs/<env>/`) that instantiates the module. Every file, verbatim, in [hetzner-patterns.md](./hetzner-patterns.md). The module holds the `environment` validation, the firewall, the private network, the primary IP and the volume.
2. **`deploy/` layout** exactly as [deploy-script.md](../_shared/deploy-script.md) shows: `deploy/deploy.sh`, `deploy/host/run.sh`, `deploy/stack/bin/backup.sh`, `deploy/stack/bin/restore-drill.sh`, `deploy/stack/compose.yaml`, `deploy/stack/traefik/`, `deploy/envs/<env>/config.env`. Link `deploy.sh` and `run.sh` to [deploy-script.md](../_shared/deploy-script.md); do not restate their bodies. The stack files are in [compose-patterns.md](./compose-patterns.md).
3. **`deploy/stack/compose.yaml`** and the two Traefik files, verbatim from [compose-patterns.md](./compose-patterns.md).
4. **Backups:** `deploy/stack/bin/backup.sh` and `deploy/stack/bin/restore-drill.sh`, verbatim from [compose-patterns.md](./compose-patterns.md). The systemd timer comes from cloud-init.
5. **Host config** `deploy.conf` and the deploy key's forced command: written by cloud-init, so nothing to hand-edit on the host.

## 6. Wire

- **GitHub environments** (`dev`, `stg`, `prd`). Secrets: `DEPLOY_SSH_KEY`, `HCLOUD_TOKEN`, state credentials (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) and `TF_ENCRYPTION` — the last three per [set-up-opentofu](../set-up-opentofu/SKILL.md). Variables: `DEPLOY_HOST`, `DEPLOY_HOST_KEY`, `APP_URL`, `HEALTH_URL`. `DEPLOY_HOST_KEY` is the pinned host key; no trust on first use.
- **No OIDC for Hetzner** (none found 2026-10-09): `DEPLOY_SSH_KEY` and `HCLOUD_TOKEN` are long-lived. Scope the key to one environment's forced command and the token to one project; rotate both on a schedule. Say this in the README.
- **DNS:** an A record and an AAAA record to the primary IP (`tofu output ipv4` / `ipv6`). The IP outlives the server, so DNS survives a rebuild.
- **Host secrets** (Postgres password, any app secret): the integration point is the optional hook `HOOK_PRE_UP` in `/etc/deploy/deploy.conf` (add `HOOK_PRE_UP=/opt/deploy/hooks/pre-up.sh`), which `run.sh` calls before `compose up`. The hook is written per [manage-secrets](../manage-secrets/SKILL.md) (sops+age, one age key per host) and must create `/opt/app/secrets/postgres_password` (mode 0400, on disk: the file is bind-mounted, so it has to survive the unattended 04:30 reboot). Plaintext is never in the repo and never in the bundle. The hook script is in [manage-secrets](../manage-secrets/SKILL.md) (run locally against sops + age; not yet on a live host).
- **Logs and traces:** [deploy-otel-collector](../deploy-otel-collector/SKILL.md) adds the collector service to the same Compose project.
- **Approval:** `prd` deploy and apply behind the environment's required reviewers ([environments.md](../_shared/environments.md)); `dev` on merge to `main`.

## 7. Verify

```bash
cd infra/envs/dev
tofu fmt -check -recursive ../.. ; tofu init -lockfile=readonly ; tofu validate   # valid; init succeeded
tofu plan -input=false                                                            # exit 0/2, the planned diff
tofu apply -input=false                                                           # creates server, firewall, network, IP, volume
ssh admin@<IP> 'cloud-init status --wait'                                          # "status: done"
ssh -o BatchMode=yes deploy@<IP> 'id'                                             # refused: forced command only accepts "<env> <image>"
deploy/deploy.sh dev ghcr.io/acme/shop@sha256:<digest>                             # "deployed dev ghcr.io/acme/shop@sha256:…"
curl -fsS https://<host>/healthz                                                    # "ok"
ssh admin@<IP> 'docker compose --project-directory /opt/app -f /opt/app/compose.yaml ps'   # every service: healthy
ssh admin@<IP> 'sudo bash /opt/app/bin/backup.sh'                                  # exit 0; restic snapshots lists one
ssh admin@<IP> 'sudo bash /opt/app/bin/restore-drill.sh'                           # "restore drill ok" (needs PG_IMAGE; see compose-patterns.md)
```

What was exercised during research, and what was not, is split in [hetzner-patterns.md](./hetzner-patterns.md#unverified-on-a-live-host): the compose stack, the deploy script, the backup and restore drill, `tofu validate`/`test` of the modules and the cloud-init YAML parse were run locally; no real Hetzner project existed, so server creation, firewall effect, volume-mount timing, cloud-init on a live host and ACME issuance were not.

## References

- [hetzner-patterns.md](./hetzner-patterns.md): the module files (verbatim) and the rules that justify each resource.
- [compose-patterns.md](./compose-patterns.md): the stack, Traefik and backup files (verbatim) and the rules.
- [../_shared/deploy-script.md](../_shared/deploy-script.md): the deploy/run script contract this host honours.
- [../_shared/environments.md](../_shared/environments.md), [../_shared/hosting-decision.md](../_shared/hosting-decision.md), [../_shared/stack-versions.md](../_shared/stack-versions.md).
- [../set-up-opentofu/SKILL.md](../set-up-opentofu/SKILL.md), [../manage-secrets/SKILL.md](../manage-secrets/SKILL.md), [../deploy-otel-collector/SKILL.md](../deploy-otel-collector/SKILL.md), [../set-up-delivery-pipeline/SKILL.md](../set-up-delivery-pipeline/SKILL.md).
- [../../core/_shared/security-baseline.md](../../core/_shared/security-baseline.md), [../../core/_shared/engineering-principles.md](../../core/_shared/engineering-principles.md).
