---
name: gke-cluster-lifecycle
description: GKE 集群生命周期管理 — 升级、版本追踪、操作记录查询、节点池运维。用于集群版本升级规划、操作历史审计、升级脚本编写、或对 GKE clusters/operations API 进行编程式调用。
---

# GKE Cluster Lifecycle

## When to Load This Skill

- Planning or executing a GKE cluster upgrade (master and/or node)
- Auditing cluster upgrade history (version change timeline)
- Writing GKE upgrade verification scripts
- Querying GKE operations API for past operations
- Understanding GKE release channels (REGULAR, RAPID, STABLE, etc.)

## Core Workflow

### 1. Pre-upgrade: Gather Current State

```bash
# 集群基本信息
gcloud container clusters describe <CLUSTER> \
  --region=<REGION> --project=<PROJECT> \
  --format="json(name,location,status,currentMasterVersion,currentNodeVersion,releaseChannel)"

# 推荐版本（通过 describe 无法直接拿到，需查 operations 或 ReleaseChannel）
gcloud container releases list --region=<REGION> --project=<PROJECT>  # or
gcloud container upgrade-list <CLUSTER> --region=<REGION> 2>/dev/null || true
```

### 2. Query Operation History

```bash
# 查询升级操作记录（最近 N 天）
gcloud container operations list \
  --region=<REGION> --project=<PROJECT> \
  --filter="targetLink~clusters/<CLUSTER> AND (operationType=UPGRADE_MASTER OR operationType=UPGRADE_NODES OR operationType=AUTO_UPGRADE_NODES)" \
  --format="json(name,operationType,status,startTime,endTime,detail)"

# 查询所有操作类型
gcloud container operations list \
  --region=<REGION> --project=<PROJECT> \
  --filter="targetLink~clusters/<CLUSTER>" \
  --format="json(name,operationType,status,startTime)"
```

### 3. Execute Upgrade

```bash
# 升级 Master
gcloud container clusters upgrade <CLUSTER> \
  --region=<REGION> --project=<PROJECT> \
  --master --cluster-version=<VERSION>

# 升级 Node Pool — 注意：gcloud 没有 node-pools upgrade 命令
# 正确：作为 clusters upgrade 的 --node-pool 参数（接值，不是 flag）
gcloud container clusters upgrade <CLUSTER> \
  --region=<REGION> --project=<PROJECT> \
  --cluster-version=<VERSION> \
  --node-pool=<POOL_NAME> \
  --async
```

#### Critical: `--node-pool` Is a Positional Argument (Not a Flag)

`--node-pool` is a **value-taking positional argument**, not a boolean flag. It must always be written as `--node-pool=<POOL_NAME>`:

```bash
# ✅ 正确 — --node-pool 接值
gcloud container clusters upgrade my-cluster \
  --node-pool=default-pool \
  --cluster-version=1.35.3-gke.1389002 \
  --async

# ❌ 错误 — --node-pool 不接值会报 "expected one argument"
gcloud container clusters upgrade my-cluster \
  --node-pool \
  --cluster-version=1.35.3-gke.1389002 \
  --quiet
```

**Common error this causes**: `argument --node-pool: expected one argument`. If you see this, check whether your script passed `--node-pool` without a value.

#### `--async` vs `--quiet` for Node Pool Upgrades

- `--async` makes the command return immediately with an operation ID (non-blocking). **Required** for scripting node pool upgrades since they are long-running.
- `--quiet` suppresses confirmation prompts but has no effect when `--async` is used (the operation runs asynchronously and doesn't block to prompt).
- For script automation: always use `--async --format="value(operation.name)"` to get the operation ID for subsequent polling.

#### `--cluster-version` Is Required for Node Pool Upgrades

When upgrading a node pool (not master), `--cluster-version` is **mandatory**. GKE does not auto-select the target version for node pool upgrades — you must pin it explicitly. Typically set to the current Master version.

### 4. Monitor Progress

```bash
# 轮询操作状态
gcloud container operations list --region=<REGION> --project=<PROJECT>
watch -n 10 'gcloud container operations list --region=<REGION> --project=<PROJECT>'

# 查看单个操作详情
gcloud container operations describe <OPERATION_NAME> --region=<REGION> --project=<PROJECT>
```

#### `operations wait` Does Not Support `--timeout`

`gcloud container operations wait --timeout=<N>s` is **not a valid flag** — it will error with `unrecognized arguments: --timeout=<N>s`.

**Correct polling pattern** for long-running operations:

```bash
# Start wait in background, poll status from main process
op_id=<OPERATION_ID>
gcloud container operations wait "$op_id" \
  --region=<REGION> --project=<PROJECT> &

# Poll in foreground loop
while true; do
  status=$(gcloud container operations describe "$op_id" \
    --region=<REGION> --project=<PROJECT> \
    --format="value(status)")
  echo "[$(date '+%H:%M:%S')] status=$status"
  [[ "$status" == "DONE" ]] && break
  sleep 20
done
```

#### Upgrade Conflict: Only One Upgrade at a Time Per Cluster

A GKE cluster can only have **one active upgrade operation** at a time (RUNNING). If you attempt a second upgrade while one is running, you get:

```
ERROR: Cluster is running incompatible operation operation-XXXXX
```

**Solution**: Wait for the current operation to reach DONE status before issuing a new one. Check with:

```bash
gcloud container operations list \
  --region=<REGION> --project=<PROJECT> \
  --filter='status=RUNNING'
```

---

## Critical Implementation Details

### Regional vs Zonal — Location Flag Mismatch (Major Bug Pattern)

`gcloud container clusters list` returns clusters with a `location` field that may be a **region** (e.g., `europe-west2`) or a **zone** (e.g., `europe-west2-a`).

| Cluster type | Correct gcloud flag |
|---|---|
| Regional | `--region=<REGION>` |
| Zonal | `--zone=<ZONE>` |

**Wrong approach**: Using `--zone=-` for a regional cluster returns empty results. The operations list API similarly requires the correct location flag.

**Fix pattern**: Read `location` from `gcloud container clusters list` output, then branch:

```bash
LOC=$(gcloud container clusters list --project=$PROJECT --format="value(location)")
if [[ "$LOC" =~ ^[a-z]+-[a-z]+\d+-[a-z]$ ]]; then
    LOC_FLAG="--zone=$LOC"
else
    LOC_FLAG="--region=$LOC"
fi
```

**In scripts**: Always resolve cluster location before calling `describe` or `operations list`. Do not assume `--zone=-` works universally.

### Using jq for JSON Parsing (Prefer Over awk)

The `gcloud --format="value(...)"` with multi-field output uses tab separation, which is fragile when fields themselves may contain tabs or complex data. **Always prefer `jq`** for JSON parsing:

```bash
# Good
INFO=$(gcloud container clusters describe $CLUSTER --region=$REGION --project=$PROJECT --format="json(currentMasterVersion,currentNodeVersion,location,status)")
MASTER_VER=$(echo "$INFO" | jq -r '.currentMasterVersion')

# Fragile (don't do this)
INFO=$(gcloud container clusters describe $CLUSTER --region=$REGION --project=$PROJECT --format="value(currentMasterVersion,currentNodeVersion,location,status)")
MASTER_VER=$(echo "$INFO" | awk 'NR==1')  # breaks if field contains whitespace
```

### macOS jq -r Carriage Return Bug

On macOS, `jq -r` appends a carriage return (`\r`) to each output line. This causes:
- `[[ -z "$var" ]]` to fail on seemingly empty values (the `\r` is invisible but present)
- String comparisons to silently miscompare

**Fix**: Always pipe through `tr -d '\r'`:
```bash
VALUE=$(echo "$JSON" | jq -r '.field' | tr -d '\r')
```

### Shell Pitfalls: set -e, pipefail, and while read

When scripting with `set -euo pipefail`, beware of two patterns that cause silent premature exit:

**Pattern 1 — `while read` + `set -e`**: `read` returns exit code 1 at EOF. In `set -e` mode, this kills the script even when EOF is expected:
```bash
# WRONG — exits non-zero at EOF
operations=$(gcloud container operations list ... --format="json")
echo "$operations" | jq -r '.[] | "\(.startTime)\t\(.operationType)\t\(.status)"' | while read -r start_time op_type status; do
    [[ "$status" == "DONE" ]] || continue
done

# CORRECT — use process substitution so read's exit code doesn't propagate
while read -r start_time op_type status; do
    [[ "$status" == "DONE" ]] || continue
done < <(gcloud container operations list ... --format="json" | jq -r '.[] | ...')
```

**Pattern 2 — `grep -F` with `^` anchor**: `grep -F` treats `^` as a literal character, not a regex anchor:
```bash
# WRONG — ^ treated as literal, pattern never matches
cluster="dev-lon-cluster-xxxxxx"
gcloud container clusters list | grep -F "^${cluster}"

# CORRECT — use plain grep (ERE, ^ is an anchor)
gcloud container clusters list | grep "^${cluster}"

# ALTERNATIVE — use -E for extended regex
gcloud container clusters list | grep -E "^${cluster}"
```

### Project ID Discovery

If `--project` is not provided, fall back to `gcloud config get-value project`. Note: the display name (e.g., `aibang`) often differs from the actual project ID (e.g., `aibang-12345678-ajbx-dev`). Always verify with `gcloud config list project`.

---

## Key API Fields

### clusters describe (json)
- `currentMasterVersion` — Master version
- `currentNodeVersion` — Node version
- `location` — region or zone
- `status` — RUNNING / RECONCILING / ERROR / etc.
- `releaseChannel.channel` — REGULAR / RAPID / STABLE / etc.

### operations list (filter)
- `operationType=UPGRADE_MASTER` — Master upgrade
- `operationType=UPGRADE_NODES` — Manual node upgrade
- `operationType=AUTO_UPGRADE_NODES` — GKE-initiated node upgrade
- `operationType=AUTO_REPAIR_NODES` — Node auto-repair
- `operationType=SET_NODE_POOL_SIZE` — Node pool resize
- `targetLink~clusters/<NAME>` — Filter to specific cluster

### operations describe
- `status` — DONE / RUNNING / ABORTING / FAILED
- `detail` — Human-readable version change string, e.g., `Master version: "1.28.3-gke.100" -> "1.29.1-gke.1589001"`. **Often empty for UPGRADE_MASTER** — GCP does not store version-from/to in operation records.
- `statusMessage` — Error details if failed
- `startTime` / `endTime` — ISO 8601 timestamps; `endTime` is empty ("") until operation completes

### GCP API Limitation: Version-from/to Not in Operation Records

The `operations describe` detail field for `UPGRADE_MASTER` operations frequently comes back **empty** — GCP does not persist version-from/to in operation records. The `detail` field only captures a human-readable string at operation creation time.

**Workaround**: To capture version transitions reliably, you must compare cluster describe snapshots:
```bash
# Before upgrade
before=$(gcloud container clusters describe $CLUSTER --region=$REGION --project=$PROJECT --format="json(currentMasterVersion,currentNodeVersion)")

# After upgrade
after=$(gcloud container clusters describe $CLUSTER --region=$REGION --project=$PROJECT --format="json(currentMasterVersion,currentNodeVersion)")

# Parse
echo "$before" | jq -r '.currentMasterVersion'
echo "$after"  | jq -r '.currentMasterVersion'
```

**In scripts**: Always display current cluster versions from `clusters describe` as the source of truth. Do not rely on operation record `detail` field for version-from/to — treat it as supplemental at best.

### Upgrade Order
## Upgrade Order

1. **Master first** — GKE upgrades master automatically; master upgrade triggers node drain and upgrade
2. **Node upgrade follows** — can be done separately with `--node-pool` flag
3. **Node version can be == master version** after full upgrade (not necessarily higher)
4. **Node version must ≤ Master version** — enforced by GKE (Node cannot be newer than Master)

---

## Scripts Reference
## Scripts Reference

This skill ships with two reference scripts in `~/.hermes/profiles/architecture/skills/gcp/gke-cluster-lifecycle/references/`:

| Script | Purpose | Verified |
|--------|---------|----------|
| `references/verify-gke-cluster-upgrade.sh` | Query and display cluster upgrade history, version changes, current versions. Supports multi-cluster polling, table output, `--days` filter. Handles regional clusters, macOS `\r` fix, `set -uo pipefail` safe mode. | v2.1 ✅ |
| `references/upgrade-gke-cluster.sh` | Execute cluster upgrade with dry-run preview (`--dry-run`), confirmation prompt (`--yes`), optional `--version`, and upgrade progress monitoring. | v1.0 ✅ |
| `references/upgrade-gke-node.sh` | Execute node pool upgrade using Surge Upgrade strategy. Auto-detects target version from Master if not specified, pre-flight checks cluster status, version compatibility, and optional PDB state. Supports `--dry-run`, `--yes`, `--node-pool`, `--cluster-version`. | v1.1 ✅ |

Both scripts are verified working against `aibang-12345678-ajbx-dev / dev-lon-cluster-xxxxxx / europe-west2`.

## References
- `references/regional-vs-zonal-operations-list.md` — Bug analysis: why `--zone=-` fails for regional clusters, the correct fix, gcloud location flag reference table
- `references/upgrade-node-pool-verified-commands.md` — Verified node pool upgrade commands, `operations wait --timeout` error, `--node-pool` value-taking argument, upgrade conflict resolution (2026-05-30 session)
- `references/verify-gke-cluster-upgrade.sh` — Verified working upgrade verification script (v2.1)
- `references/upgrade-gke-cluster.sh` — Verified working upgrade execution script (v1.0)
- `references/upgrade-gke-node.sh` — Verified working node pool upgrade script (v1.1, supports Surge strategy, auto-detects target version, PDB pre-flight)
- `references/upgrade-scripts-session-notes.md` — Implementation notes, common bug patterns, version constraints, color code syntax