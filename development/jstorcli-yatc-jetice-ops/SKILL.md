---
name: jstorcli-yatc-jetice-ops
description: Use when operating jstorcli with yatc and jetice/jetlake workflows, especially for VM lifecycle, image prep, deployment checks, and command lookup without hardcoded paths.
---

# jstorcli + yatc + jetice/jetlake Ops

## Overview
This skill is the first command reference for deployment and validation work involving `jstorcli`, `yatc`, `jetice-env`, and JetLake planes/profiles.

Use dynamic path discovery first. Do not hardcode project directories.

## Environment Discovery

```bash
# Project root (prefer current repo root)
export YATC_ROOT="${YATC_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"

# Compose directory (first compose.yaml under repo, override when needed)
export YATC_COMPOSE_DIR="${YATC_COMPOSE_DIR:-$(find "$YATC_ROOT" -maxdepth 3 -type f -name compose.yaml -print -quit | xargs -r dirname)}"

# jstorcli source root (contains src/jstorcli/__main__.py)
export JSTORCLI_ROOT="${JSTORCLI_ROOT:-$(find "$YATC_ROOT" -type f -path '*/jstorcli/src/jstorcli/__main__.py' -print -quit | sed 's#/src/jstorcli/__main__.py##')}"
export JSTORCLI_SRC="${JSTORCLI_SRC:-$JSTORCLI_ROOT/src}"

# Optional image URL input for local mirror/download
export YATC_IMAGE_URL="${YATC_IMAGE_URL:-http://factory.jetio.net/artifactory/packer-os-images/jetice/ubuntu/ubuntu-22.04.5-jetice-uefi-2507.2-2-amd64-20250724.qcow2}"
```

## yatc Build/Install/Deploy Flow

```bash
# 1) Build latest wheel
cd "$YATC_ROOT"
uv build

# 2) Install latest wheel to system python
sudo uv pip install --system "$(ls -t dist/*.whl | head -n 1)"

# 3) Register local images manifest (edit images.yaml path first)
sudo yatc images register -m "$YATC_ROOT/images.yaml"

# 4) Pull configured image name from images.yaml
sudo yatc pull ubuntu-22045-jetice

# 5) Start compose VM group
sudo yatc compose up --provider qemu --dir "$YATC_COMPOSE_DIR"

# 6) Check VM/IP
sudo yatc ps

# 7) Stop and remove compose resources when done
sudo yatc compose down --provider qemu --dir "$YATC_COMPOSE_DIR"
sudo yatc compose rm --dir "$YATC_COMPOSE_DIR"
```

## jstorcli Current Command Surface

Source of truth:
- `src/jstorcli/__main__.py`
- each sub-CLI parser file

Top-level multiplexer:
- `jstorcli drbd` (`drbd-cli`, `drbd_cli`)
- `jstorcli lvm` (`lvm-pool`, `lvm_pool` for legacy)
- `jstorcli jetlake`
- `jstorcli hagroup`
- `jstorcli zfs`
- `jstorcli bash-completion` (`bash-completetion` alias exists in code)

### DRBD
- `status`
- `prepare`
- `process`
- `delete`
- `adjust`
- `primary`
- `secondary`

### LVM
Group `pool`:
- `discover`
- `define`
- `create`
- `delete`
- `list`
- `show`

Group `lv`:
- `create`
- `resize`
- `delete`
- `rename`
- `snapshot`
- `restore`
- `rollback`

Legacy `lvm-pool` also exposes:
- `discover`, `define`, `create`, `delete`, `list`, `show`
- `lv-create`, `lv-resize`, `lv-delete`, `lv-rename`
- `lv-snapshot`, `lv-restore`, `lv-rollback`

### JetLake
Group `profile`:
- `define`
- `validate`
- `create`
- `destroy`
- `undef`

Group `plane`:
- `define`
- `create`
- `destroy`
- `list`
- `undef`

### HAGroup
- `define`
- `update`
- `create`
- `get`
- `list`
- `delete`
- `resolve`

### ZFS
Group `pool`:
- `list`
- `info`
- `create`
- `delete`

Group `volume`:
- `list`
- `create`
- `resize`
- `delete`
- `rename`

Group `snapshot`:
- `create`
- `delete`
- `clone`
- `rollback`

Group `profile`:
- `define`
- `list`
- `show`
- `validate`
- `apply`
- `init`

Also:
- `send`
- `receive`

## jetice-env Runtime Commands (inside VM)

`jetice-env` command family:
- `check`
- `pull`
- `config`
- `reconf`
- `init`
- `compose`
- `prep`
- `verify`
- `deploy`
- `state`
- `remove`

Common VM validation:

```bash
cloud-init status
cd /opt/jetice-vtl
./jetice_s3gw_acceptance jetice s3gw http://0.0.0.0:9000
```

## Recovery/Reset Operations

```bash
# Host key cleanup when VM IP changes
ssh-keygen -f ~/.ssh/known_hosts -R "192.168.122.2"

# Last-resort cleanup (destructive)
sudo rm -rf /opt/yatc/compute
```

## Maintenance: Keep This Skill Updated

When `jstorcli` changes, refresh this skill in the same commit:

1. Re-check parser definitions in:
   - `src/jstorcli/__main__.py`
   - `src/jstorcli/*_cli.py`
2. Re-run help snapshots:

```bash
cd "$JSTORCLI_ROOT"
export PYTHONPATH="$JSTORCLI_SRC"
python3 -m jstorcli --help
python3 -m jstorcli.drbd_cli --help
python3 -m jstorcli.lvm_cli --help
python3 -m jstorcli.lvm_pool_cli --help
python3 -m jstorcli.jetlake_cli --help
python3 -m jstorcli.hagroup_cli --help
python3 -m jstorcli.zfs_cli --help
```

3. Update this skill's command lists when any subcommand is added/removed/renamed.
4. Keep path handling dynamic (`YATC_ROOT`, `YATC_COMPOSE_DIR`, `JSTORCLI_ROOT`) and avoid fixed absolute paths.
