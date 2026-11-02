---
name: deploy-to-ionos
description: Use when hosting on IONOS Cloud with the ionoscloud OpenTofu provider (datacenter, LAN, server or Managed Kubernetes, DBaaS Postgres, Object Storage), or picking IONOS Deploy Now for a static site.
---

# Deploy to IONOS

The same deploy contract as [deploy-to-hetzner](../deploy-to-hetzner/SKILL.md) on a different cloud: one VM per environment, the same Compose stack and Traefik, the same `deploy.sh` / `run.sh` interface ([deploy-script.md](../_shared/deploy-script.md)). Two things change: the infrastructure module (datacenter, LANs, ENTERPRISE server) and the database — DBaaS Postgres on a private LAN instead of Postgres in Compose. Why IONOS at all: [hosting-decision.md](../_shared/hosting-decision.md) (German contract, managed database, Managed Kubernetes). A flat-rate IONOS **VPS** from the Cloud Panel has no tofu provider: use [set-up-ionos-vps](../set-up-ionos-vps/SKILL.md).

## 1. Audit current state (change nothing)

```bash
cat .claude/stack-profile.md 2>/dev/null        # hosting, database.host, backend.track, languages
ls infra/modules/ionos-host infra/envs 2>/dev/null
ls deploy deploy/stack deploy/host deploy/envs 2>/dev/null
gh secret list --env dev 2>/dev/null            # names only: IONOS_TOKEN, IONOS_S3_ACCESS_KEY present?
tofu version 2>&1 | head -1
```

Token presence is checked by NAME only (`IONOS_TOKEN`, `IONOS_S3_ACCESS_KEY`, `IONOS_S3_SECRET_KEY`); never print a value. From the profile: `hosting` should include `ionos`; `database.host` says whether the database moves to DBaaS; `backend.track` plus `languages` decide static site vs container (step 3). The DBaaS password is write-only and fed by an ephemeral variable: OpenTofu >= 1.11 (use a supported line: 1.12 or 1.13).

## 2. Decide

- No `infra/modules/ionos-host` → full: steps 3 to 7.
- Module exists → delta: compare it against the files in [ionos-patterns.md](./ionos-patterns.md) — one inline NIC, the firewall rules' single `source_ip`, `ignore_changes` for cloud-init, the DBaaS settings — and fix only what differs.
- Module, env roots and the `deploy/` bundle present, `tofu validate` and `tofu plan` clean → "already in place"; run step 7 and stop.

## 3. Detect the track

| Evidence | Track | Action |
|---|---|---|
| Static site or SPA, no server (`backend.track: none`, frontend-only `languages`) | IONOS Deploy Now | Paragraph below, then stop — no tofu |
| Container service on one VM (default) | VM + Compose | Steps 4 to 7 |
| Several services, autoscaling, several teams | Managed Kubernetes | Not built here; see [ionos-patterns.md](./ionos-patterns.md) — unverified |
| Tiny fixed workload | Cube | `ionoscloud_cube_server` with a template; sizing rule in [ionos-patterns.md](./ionos-patterns.md) |

**Deploy Now.** GitHub-based hosting of static sites, SPAs and PHP on IONOS shared (Apache) webspace: connect the repository, Deploy Now generates a GitHub Actions workflow that builds and uploads the site, and branches deploy to staging. No containers, no Docker, no digest promotion — its build is not this pipeline's, and the environment contract (config.env, host secrets, health-gated deploys; [environments.md](../_shared/environments.md)) does not apply. Prices and quotas differ across IONOS pages: read the live page before quoting either. Right for a marketing site, docs, or a SPA whose API runs elsewhere. Wrong for SSR, background jobs, anything that needs the environment contract. Minimal steps: connect the repo in the Deploy Now dashboard, review the generated workflow, set the domain, confirm the quotas. Stop; there is no tofu and no deploy script to write.

## 4. Install only what is missing

- OpenTofu, if absent: [set-up-opentofu](../set-up-opentofu/SKILL.md) is the prerequisite (layout, remote state, encryption, CI).
- `ionosctl`, optional, to list locations, templates and DBaaS backup locations (version unverified); the provider does not need it.
- Nothing else. The Compose stack, Traefik and the deploy scripts belong to [compose-patterns.md](../deploy-to-hetzner/compose-patterns.md) and [deploy-script.md](../_shared/deploy-script.md); generate them there, not here. **Change for IONOS:** delete the `postgres` service and the app's `depends_on: postgres` from `compose.yaml`, and do not install the Postgres backup timer's script: DBaaS owns the database and its backups. The app stays on the `edge` network, which reaches the private NIC through the host; the internal `backend` network does not.

## 5. Generate the seams

1. **`infra/modules/ionos-host/`** — datacenter, IP block, public and private LAN, ENTERPRISE server with cloud-init from `modules/host-bootstrap` (`distro = "ubuntu"`; see [hetzner-patterns.md](../deploy-to-hetzner/hetzner-patterns.md)), private-LAN NIC, DBaaS cluster. All four files verbatim in [ionos-patterns.md](./ionos-patterns.md); the module passed `tofu validate` with provider 6.7.x.
2. **`infra/envs/<env>/`** — one root per environment: `main.tf` holds the provider block and the module call, `versions.tf` the full `required_providers` source. Point `run_script` at the repo's `deploy/host/run.sh` with `file(...)`.
3. **`deploy/`** — the bundle from [deploy-script.md](../_shared/deploy-script.md): `deploy.sh`, `host/run.sh`, `stack/` (with `stack/bin/backup.sh`), `envs/<env>/config.env`.
4. **Backup bucket** — `ionoscloud_s3_bucket` (region `eu-central-3`) and an `ionoscloud_object_storage_accesskey` for the nightly backup (rules in [ionos-patterns.md](./ionos-patterns.md)).

## 6. Wire

- **No OIDC for IONOS** (none found 2026-10-09): `IONOS_TOKEN` is a secret of the GitHub *environment*, one per environment. Object Storage keys (`IONOS_S3_ACCESS_KEY`, `IONOS_S3_SECRET_KEY`) likewise if CI touches buckets.
- **Deploy credentials** exactly as in [deploy-script.md](../_shared/deploy-script.md): `DEPLOY_SSH_KEY` (environment secret, forced command on the host), `DEPLOY_HOST` (tofu output `ipv4`), `DEPLOY_HOST_KEY` (pinned host key; no trust on first use).
- **DBaaS password:** export `TF_VAR_db_password` from the secret store ([manage-secrets](../manage-secrets/SKILL.md)) for every `plan` and `apply`. The variable is `ephemeral`, so the value never enters state; rotate by bumping `db_password_version` and updating the secret.
- **App runtime:** the app reads `DATABASE_URL` built from the `db_dns_name` output. It reaches the host through `run.sh`'s pre-up hook, which decrypts the sops secrets ([manage-secrets](../manage-secrets/SKILL.md); see the hook note in [deploy-to-hetzner](../deploy-to-hetzner/SKILL.md)) — never a tfvar, never image `ENV`.

## 7. Verify

```bash
cd infra/envs/dev && tofu init -input=false && tofu validate    # "The configuration is valid."
TF_VAR_db_password="<from the secret store>" tofu plan -input=false   # exit 2 = the stack to create
```

After `tofu apply` (first run — every check below is a first-run check; see the note at the end):

```bash
ssh admin@"$(tofu output -raw ipv4)" cloud-init status --wait    # status: done
ssh admin@"$(tofu output -raw ipv4)" ip -4 addr                  # second NIC (private LAN) has an address
```

If the private NIC has no address, configure it statically — whether IONOS DHCP serves a private LAN is unverified.

```bash
ssh admin@"$(tofu output -raw ipv4)" docker run --rm -it postgres:18.6-trixie psql "host=$(tofu output -raw db_dns_name) sslmode=require dbname=app user=app"
```

Runs on the server: DBaaS is reachable from the private LAN only. Use `sslmode=verify-full` with the ISRG Root X1 root certificate in production, as the IONOS docs describe (not run here).

First deploy and health:

```bash
deploy/deploy.sh dev <image@sha256:digest>        # prints: deployed dev <image@sha256:…>
curl -fsS https://dev.<app>.<domain>/healthz      # ok
```

**Exercised while writing this skill:** `tofu validate` of the module against provider 6.7.x, and the cloud-init template parse in `host-bootstrap`. **Not exercised** (no IONOS contract): no `apply`, no DHCP/NIC behaviour on a real private LAN, no DBaaS connection, no Object Storage write, no Deploy Now build.

## References
- [ionos-patterns.md](./ionos-patterns.md): rules; the module and env files verbatim; DBaaS, Object Storage and sizing specifics; the unverified list.
- [deploy-script.md](../_shared/deploy-script.md): the `deploy.sh` / `run.sh` contract and its secrets.
- [compose-patterns.md](../deploy-to-hetzner/compose-patterns.md): the shared Compose stack, Traefik and backups; [deploy-to-hetzner](../deploy-to-hetzner/SKILL.md): the same contract on Hetzner.
- [hosting-decision.md](../_shared/hosting-decision.md), [environments.md](../_shared/environments.md), [set-up-opentofu](../set-up-opentofu/SKILL.md), [manage-secrets](../manage-secrets/SKILL.md).
- [security-baseline.md](../../core/_shared/security-baseline.md).
