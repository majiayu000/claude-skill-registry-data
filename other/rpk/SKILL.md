---
name: rpk
description: >-
  Install and configure the rpk CLI, the single binary for all Redpanda
  operations, including installing it on macOS, Linux, and Docker, and setting
  up profiles (rpk.yaml) and connection settings. Use when installing rpk,
  creating or switching rpk profiles, configuring broker/admin/registry
  endpoints or SASL/TLS credentials, using -X flags or RPK_ environment
  variables, connecting to self-hosted or Redpanda Cloud clusters, or
  checking/applying an Enterprise license. This is the hub skill for
  command-group discovery; for
  topic/cluster/security/cloud/registry/transform/debug work, see the matching
  /redpanda:rpk-* skill.
---


# rpk: Install, Profiles & Configuration

`rpk` is the Redpanda CLI and toolbox — a single binary that manages every
aspect of a Redpanda cluster from the command line. It handles topic management,
cluster operations, security, schema registry, data transforms, cloud
provisioning, and debugging. All commands share a unified configuration model
based on **profiles** (`rpk.yaml`) and **-X flags** that cover the Kafka API,
Admin API, and Schema Registry endpoints.

This is the hub skill. It covers install, config, and command discovery. For
depth on individual command groups, see the linked subskills in the Reference
Directory below.

## Quickstart

### 1. Install rpk

**macOS — Homebrew (recommended)**
```bash
brew install redpanda-data/tap/redpanda
```

**macOS — Apple Silicon (M1/M2/M3/M4), manual**
```bash
curl -LO https://github.com/redpanda-data/redpanda/releases/latest/download/rpk-darwin-arm64.zip \
  && mkdir -p ~/.local/bin \
  && export PATH="$HOME/.local/bin:$PATH" \
  && unzip rpk-darwin-arm64.zip -d ~/.local/bin/
```

**macOS — Intel, manual**
```bash
curl -LO https://github.com/redpanda-data/redpanda/releases/latest/download/rpk-darwin-amd64.zip \
  && mkdir -p ~/.local/bin \
  && export PATH="$HOME/.local/bin:$PATH" \
  && unzip rpk-darwin-amd64.zip -d ~/.local/bin/
```

**Linux — amd64**
```bash
curl -LO https://github.com/redpanda-data/redpanda/releases/latest/download/rpk-linux-amd64.zip \
  && mkdir -p ~/.local/bin \
  && export PATH="$HOME/.local/bin:$PATH" \
  && unzip rpk-linux-amd64.zip -d ~/.local/bin/
```

**Linux — arm64**
```bash
curl -LO https://github.com/redpanda-data/redpanda/releases/latest/download/rpk-linux-arm64.zip \
  && mkdir -p ~/.local/bin \
  && export PATH="$HOME/.local/bin:$PATH" \
  && unzip rpk-linux-arm64.zip -d ~/.local/bin/
```

Verify:
```bash
rpk --version
```

### 2. Connect to a self-hosted cluster with a profile

```bash
# Create a profile named "local" pointing at localhost
rpk profile create local \
  --set brokers=localhost:9092 \
  --set admin.hosts=localhost:9644 \
  --description "Local dev cluster"

# rpk automatically switches to the new profile.
# Confirm the active profile:
rpk profile current

# Now all commands use "local" without extra flags:
rpk topic list
rpk cluster health
```

**With SASL/SCRAM-256 and TLS:**
```bash
rpk profile create prod \
  --set brokers=broker1.example.com:9092,broker2.example.com:9092 \
  --set admin.hosts=broker1.example.com:9644,broker2.example.com:9644 \
  --set tls.enabled=true \
  --set sasl.mechanism=SCRAM-SHA-256 \
  --set user=alice \
  --set pass=s3cr3t \
  --description "Production cluster"
```

### 3. Connect to a Redpanda Cloud cluster

```bash
# Log in (opens browser for SSO)
rpk cloud login

# Create a profile from a Cloud cluster ID or name
rpk profile create --from-cloud <cluster-id-or-name>

# Or interactively pick a cluster:
rpk profile create --from-cloud

# The profile is now active and contains the broker/registry/admin URLs
# pulled from the Cloud control plane:
rpk topic list
```

### 4. One-off override with -X (no profile change)

```bash
# Override brokers for a single command
rpk topic list -X brokers=myhost:9092

# SASL in one shot
rpk topic consume orders \
  -X brokers=myhost:9092 \
  -X tls.enabled=true \
  -X sasl.mechanism=SCRAM-SHA-256 \
  -X user=alice \
  -X pass=s3cr3t

# See all available -X keys
rpk -X list

# See detailed description of each -X key
rpk -X help
```

### 5. Switch between profiles

```bash
rpk profile list          # list all profiles
rpk profile current       # show active profile
rpk profile use prod      # switch to "prod"
rpk profile use local     # switch back to "local"

# Temporary override without switching:
rpk topic list --profile prod
# or via env var:
RPK_PROFILE=prod rpk topic list
```

---

## Configuration model

rpk resolves configuration in priority order (highest wins):

1. **-X flags** on the command line (current command only)
2. **RPK_* environment variables** (current shell session)
3. **rpk profile** in `rpk.yaml` (persistent, recommended)
4. **`redpanda.yaml` rpk section** (system-wide defaults, self-managed only)

### rpk.yaml location

- **Linux**: `~/.config/rpk/rpk.yaml`
- **macOS**: `~/Library/Application Support/rpk/rpk.yaml`

All profiles live in the same file. The `globals` section applies to all
profiles (timeouts, prompt format, etc.).

### -X flag → RPK_ env var conversion

Every `-X key=value` becomes `RPK_KEY=value` by uppercasing and replacing `.`
with `_`. Examples:

| `-X` option | Environment variable |
|---|---|
| `brokers` | `RPK_BROKERS` |
| `tls.enabled` | `RPK_TLS_ENABLED` |
| `tls.ca` | `RPK_TLS_CA` |
| `sasl.mechanism` | `RPK_SASL_MECHANISM` |
| `user` | `RPK_USER` |
| `pass` | `RPK_PASS` |
| `admin.hosts` | `RPK_ADMIN_HOSTS` |
| `registry.hosts` | `RPK_REGISTRY_HOSTS` |
| `cloud.client_id` | `RPK_CLOUD_CLIENT_ID` |
| `cloud.client_secret` | `RPK_CLOUD_CLIENT_SECRET` |

Profile selection: `RPK_PROFILE=<name>`

---

## Command groups at a glance

| Command group | What it does | Subskill |
|---|---|---|
| `rpk topic` | Create, describe, alter, delete topics; produce and consume records | `rpk-topic` |
| `rpk cluster` | Cluster health/metadata, config, partitions, maintenance, connections, quotas, self-test | `rpk-cluster` |
| `rpk group` | Consumer group list/describe/seek/delete | `rpk-group` |
| `rpk security` | SASL users, Kafka ACLs, RBAC roles, secrets | `rpk-security` |
| `rpk cloud` | Log in to Cloud, create profiles, BYOC provisioning | `rpk-cloud` |
| `rpk debug` | Collect debug bundles (local and remote), local process info | `rpk-debug` |
| `rpk registry` | Schema Registry subjects, schemas, compatibility, modes | `rpk-registry` |
| `rpk transform` | Build and deploy Wasm data transforms | `rpk-transform` |
| `rpk ai` | AI/MCP integration — MCP server for LLM agents | `ai` |
| `rpk connect` | Run Redpanda Connect (formerly Benthos) pipelines | `connect` |
| `rpk profile` | Manage rpk profiles (create/use/list/edit/set/delete) | this skill |
| `rpk acl` | Deprecated — use `rpk security acl` instead | `rpk-security` |
| `rpk generate` | Generate completions, app scaffolding, prometheus config | — |
| `rpk version` | Print rpk version | — |
| `rpk container` | Manage local Redpanda containers for dev | — |
| `rpk plugin` | Manage rpk plugins | — |
| `rpk redpanda` | Operate the local broker: start/stop, mode, tune, check, node config, admin (brokers decommission) — self-managed only | `rpk-redpanda` |
| `rpk iotune` | Benchmark disk I/O and write optimal io properties (Linux-only) | `rpk-redpanda` |
| `rpk oxla` | Redpanda Oxla SQL engine — "Coming Soon" CLI stub | `sql` skills |
| `rpk shadow` | Manage Redpanda Shadow Links (create/describe/update/delete/list/failover) | — |

---

## Enterprise features and the license

Redpanda's key differentiators are Enterprise Edition features. They require a
valid Enterprise license — new clusters (v24.3+) automatically get a 30-day trial
license on first start. Most are enabled/configured through `rpk cluster config`
(cluster-wide keys) or `rpk topic create -c` / `rpk topic alter-config --set`
(topic properties); a few have dedicated command groups (`rpk shadow`,
`rpk security role`, `rpk cluster license`).

```bash
# Check license + whether you are in violation (enterprise features without a license)
rpk cluster license info            # alias: status; supports --format json
rpk cluster license set --path /etc/redpanda/redpanda.license
rpk generate license --apply        # generate + apply a 30-day trial
```

Enterprise features operated via rpk, with their primary control:

| Feature | rpk control (primary key/command) |
|---|---|
| Tiered Storage | `cloud_storage_enabled`; topic `redpanda.remote.read/write/delete`, `retention.local.target.ms/bytes` |
| Cloud Topics | `cloud_topics_enabled`; topic `redpanda.storage.mode=cloud` |
| Iceberg Topics | `iceberg_enabled`; topic `redpanda.iceberg.mode` (+ `.target.lag.ms`, `.partition.spec`, `.invalid.record.action`, `.delete`) |
| Continuous Data Balancing | `partition_autobalancing_mode=continuous` (+ `partition_autobalancing_*`, `core_balancing_continuous`) |
| Shadow Linking / DR | `rpk shadow create/status/update/failover/delete`, `rpk shadow config generate` |
| Remote Read Replicas | `cloud_storage_enable_remote_read`; topic `redpanda.remote.readreplica=<bucket>` |
| Leadership Pinning | topic `redpanda.leaders.preference`; cluster `default_leaders_preference` |
| Audit Logging | `audit_enabled` (+ `audit_*` keys) |
| RBAC / GBAC | `rpk security role ...`; `rpk security acl create --allow-principal Group:...` |
| OIDC / Kerberos auth | cluster `sasl_mechanisms` (`OAUTHBEARER`/`GSSAPI`), `http_authentication` |
| Schema ID Validation | `enable_schema_id_validation`; topic `redpanda.{key,value}.schema.id.validation` |
| FIPS | node `fips_mode` (`rpk redpanda config set redpanda.fips_mode enabled`) |

Full nested config keys, topic properties, accepted values, and the
disable-to-exit-violation commands for each feature are in
[enterprise-features.md](references/enterprise-features.md).

---

## Reference Directory

- [install.md](references/install.md): Installing rpk on macOS (Homebrew and manual), Linux (amd64/arm64), verifying the install, and keeping rpk up to date.
- [profiles.md](references/profiles.md): Full rpk profile reference — rpk.yaml location, profile create/use/list/current/edit/set/delete/rename, --from-cloud, RPK_PROFILE env var, and the profile data structure.
- [x-flags-and-config.md](references/x-flags-and-config.md): Every -X option with type, default, and example; RPK_* env var mapping; configuration priority; globals settings; and rpk.yaml vs redpanda.yaml.
- [command-map.md](references/command-map.md): One-line description of every top-level rpk command group with a pointer to the dedicated subskill for each.
- [enterprise-features.md](references/enterprise-features.md): Redpanda Enterprise differentiators operated through rpk — license management (`rpk cluster license`), Tiered Storage, Cloud Topics, Iceberg Topics, Continuous Data Balancing, Shadow Linking/DR (`rpk shadow`), Remote Read Replicas, Audit Logging, RBAC, OIDC/Kerberos/FIPS auth, Schema ID Validation, and Leadership Pinning — with their nested cluster-config keys, topic properties, accepted values, and disable-to-exit-violation commands. All require an Enterprise license.
