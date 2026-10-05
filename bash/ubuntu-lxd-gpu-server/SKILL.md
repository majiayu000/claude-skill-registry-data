---
name: ubuntu-lxd-gpu-server
description: 'Install LXD on an Ubuntu server and pass all NVIDIA GPUs into LXD system containers via CDI — install snapd+LXD (snap), run `lxd init` with a ZFS or dir storage pool, set up a host CDI spec at /etc/cdi and wire the nvidia-container-toolkit auto-refresh units so it stays fresh across driver upgrades, and grant every GPU to every instance through the default profile, then verify nvidia-smi inside a container. Use when asked to install or set up LXD/lxc on a GPU host, give LXD containers GPU access, do LXD NVIDIA GPU passthrough, share all GPUs across LXD instances, when `nvidia.runtime=true` fails with "driver rpc error: timed out" (use CDI instead), or when LXD GPU containers break after a host driver upgrade (stale or duplicate CDI spec). Assumes the host NVIDIA driver + nvidia-container-toolkit are already installed (see ubuntu-nvidia-gpu-enablement).'
---

# Ubuntu LXD GPU Server

Install LXD on an Ubuntu host and expose **all** NVIDIA GPUs to LXD system containers via **CDI**, granted
through the `default` profile so every instance inherits them. Assumes the host driver + `nvidia-container-toolkit`
(`nvidia-ctk`) are already in place — if not, run the **`ubuntu-nvidia-gpu-enablement`** skill first.

⚠️ **Use CDI, not `nvidia.runtime=true`.** LXD's legacy libnvidia-container hook hangs at container start with
`nvidia-container-cli: initialization error: driver rpc error: timed out` on recent kernels / Blackwell GPUs.
CDI uses the host's `nvidia-ctk` and a static spec — no driver RPC, no timeout. (Why: [REFERENCE.md](REFERENCE.md) §4.)

## Quick start

```bash
# 1. install LXD + wire all GPUs into the default profile. Storage: zfs:<pool>/lxd | dir | zfs-loop:50GiB
sudo LXD_STORAGE=zfs:rpool/lxd bash scripts/install-lxd.sh
# 2. verify a fresh container sees every GPU (launches a throwaway container, asserts the count, cleans up)
bash scripts/verify-gpu.sh
```

## Pre-flight

- Sudo user (SSH fine). `nvidia-smi -L` lists the GPUs on the **host**.
- `nvidia-ctk --version` works (host CDI toolkit). Missing → `ubuntu-nvidia-gpu-enablement` Step 5.
- Egress to snap + the image server (`images.lxd.canonical.com`).
- Storage decision: a ZFS pool (redundant root mirror, or a data pool) is ideal; otherwise `dir` works anywhere.
  Redundant pool → containers survive a disk loss; big stripe → more space. See REFERENCE §2.

## Steps (what `install-lxd.sh` does)

1. **snapd + LXD.** Minimal/debootstrap bases ship no snapd: `apt-get install -y snapd && snap wait system seed.loaded`,
   then `snap install lxd`. ⚠️ sudo's `secure_path` lacks `/snap/bin` **and** the `lxd` group needs a re-login —
   so this session, call `lxc`/`lxd` by absolute path (`sudo /snap/bin/lxc …`).
2. **`lxd init`** (preseed): one storage pool + `lxdbr0` NAT bridge. ZFS source `<pool>/lxd` puts rootfs on your
   chosen pool; `dir` is filesystem-agnostic. Full preseed + backends in REFERENCE §2.
3. **CDI spec at `/etc/cdi/nvidia.yaml`** (declares each GPU + an `all` device). If the host toolkit ships
   `nvidia-cdi-refresh.{path,service}` (≥1.17), the script pins them to `/etc/cdi` — they default to the tmpfs
   `/var/run/cdi` — so they auto-refresh the spec on every driver/toolkit upgrade *and* at boot; an older toolkit
   instead gets a one-off spec + a `lxd-nvidia-cdi-refresh.service` boot unit. Either way LXD reads one persistent
   spec and there's nothing to do on driver upgrades. (Why, and the don't-keep-two-copies gotcha: REFERENCE §5.)
4. **Grant all GPUs to all instances** via the default profile:
   ```bash
   sudo /snap/bin/lxc profile device add default gpu0 gpu gputype=physical id=nvidia.com/gpu=all
   ```
   Per-instance instead: `lxc config device add <inst> gpu0 gpu gputype=physical id=nvidia.com/gpu=all`.
   A single GPU: `id=nvidia.com/gpu=0` or `id=nvidia.com/gpu=<UUID>` (REFERENCE §3).

## Verify

```bash
sudo /snap/bin/lxc launch ubuntu:24.04 g1
sudo /snap/bin/lxc exec g1 -- nvidia-smi -L      # must list every host GPU
sudo /snap/bin/lxc exec g1 -- nvidia-smi         # full table; libcuda is injected too (CUDA works)
sudo /snap/bin/lxc delete -f g1
```
`scripts/verify-gpu.sh` automates this and fails loudly if the container's GPU count ≠ the host's.

## Maintenance

The CDI spec hardcodes the running driver's library paths, so it must be regenerated after every host driver
upgrade or GPU containers break with a missing-library / NVML version-mismatch error. **The install script makes
this automatic:** on a modern toolkit it pins the packaged `nvidia-cdi-refresh.{path,service}` to `/etc/cdi` (they
fire on any driver/toolkit change and at boot); on an older toolkit it installs a `lxd-nvidia-cdi-refresh.service`
boot unit. **So normally there's no manual step on a driver upgrade.** Force a refresh by hand with
`sudo systemctl start nvidia-cdi-refresh.service` (or `sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml`).
⚠️ Don't *also* leave a spec in `/var/run/cdi` — LXD scans both dirs, and two specs collide as duplicate devices
(REFERENCE §5).

Deep dives — storage backends & preseed, GPU selection, CDI-vs-runtime diagnosis, moving the pool between ZFS
pools, troubleshooting, uninstall — in [REFERENCE.md](REFERENCE.md).
