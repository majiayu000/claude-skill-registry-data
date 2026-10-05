---
name: ubuntu-nvidia-gpu-enablement
description: Enable NVIDIA GPUs on a Ubuntu server for compute/inference serving — install the open-kernel-module driver (required for Blackwell/Hopper), CUDA toolkit, turn on IOMMU (intel_iommu=on iommu=pt), set up nvidia-persistenced, and install/wire a container runtime (Docker + nvidia-container-toolkit, or the minimal CLI), then verify all GPUs, IOMMU groups, P2P, nvcc, and GPU containers. Use when asked to enable or set up NVIDIA GPUs, install the NVIDIA driver + CUDA on Ubuntu, install Docker + nvidia-container-toolkit for GPU containers, configure GPU IOMMU/passthrough, prepare a host for GPU serving (vLLM/PyTorch/TensorRT/NIM), or troubleshoot nouveau, persistence mode, GPU-in-container, or driver/CUDA/glibc problems.
---

# Ubuntu NVIDIA GPU Enablement

Bring a fresh UEFI Ubuntu server with NVIDIA GPUs to a serving-ready state. Order matters:
**driver → IOMMU cmdline → CUDA → persistence → container access → verify.** Driver and cmdline changes
each need a reboot — batch them (Steps 1 + 2 reboot together).

Run as a sudo user (over SSH is fine). [REFERENCE.md](REFERENCE.md) holds the *why*, GRUB/AMD variants,
and troubleshooting. Boot-affecting steps are deliberate — keep BMC/console access as a fallback.

## Pre-flight

- UEFI: `[ -d /sys/firmware/efi ]`.
- Secure Boot: `mokutil --sb-state`. **If enabled**, DKMS modules need MOK enrollment at the console — plan
  for it or disable SB. (Off is typical with a custom bootloader; verify, don't assume.)
- GPUs present: `sudo apt-get install -y pciutils && lspci -nn | grep -i nvidia`. Note the architecture.
- Bootloader = GRUB or ZFSBootMenu? (decides where the cmdline lives — Step 2.)
- Egress to `archive.ubuntu.com` (+ `nvidia.github.io` for the container repo).

## Step 1 — Driver (OPEN kernel module)

```bash
sudo apt-get update
sudo apt-get install -y nvidia-driver-580-server-open   # example version
```
- **Blackwell requires the open modules** (proprietary won't support it); Hopper too. Pick the right branch
  with `ubuntu-drivers devices`. Datacenter / "Server Edition" cards → `nvidia-driver-<ver>-server-open`.
- Auto-blacklists nouveau; needs a reboot (do it with Step 2).
- Fabric Manager is **only** for NVLink/NVSwitch systems — skip it if your GPUs have no NVLink.

## Step 2 — IOMMU kernel cmdline

Add `intel_iommu=on iommu=pt` (AMD: `amd_iommu=on iommu=pt`). `iommu=pt` = passthrough/identity DMA:
~zero bare-metal cost **and preserves GPU P2P** (full translation can disable P2P → NCCL falls back to SHM).

- **GRUB:** append to `GRUB_CMDLINE_LINUX_DEFAULT` in `/etc/default/grub`, then `sudo update-grub`.
- **ZFSBootMenu (no GRUB):** the cmdline is the ZFS property `org.zfsbootmenu:commandline` on the boot ROOT
  dataset. **Read-then-APPEND — never clobber** existing tokens (e.g. `zfs_force=1`):
  ```bash
  cur=$(zfs get -H -o value org.zfsbootmenu:commandline rpool/ROOT)
  sudo zfs set org.zfsbootmenu:commandline="$cur intel_iommu=on iommu=pt" rpool/ROOT
  ```
- **Reboot now** (applies Steps 1 + 2 together).

## Step 3 — CUDA toolkit

```bash
sudo apt-get install -y cuda-toolkit        # often already pulled by the driver
```
- `nvcc` is **not on PATH** by default — add it system-wide:
  ```bash
  printf 'export CUDA_HOME=/usr/local/cuda\nexport PATH=$CUDA_HOME/bin:$PATH\n' | sudo tee /etc/profile.d/cuda.sh
  ```
- ⚠️ On bleeding-edge Ubuntu (glibc ≥ 2.41), some CUDA versions **can't compile** C++ (rsqrt/rsqrtf header
  clash). **Serving is unaffected** — prebuilt wheels use the driver + libcudart, not nvcc. See REFERENCE §3.

## Step 4 — Persistence

```bash
sudo systemctl enable --now nvidia-persistenced
```
- ⚠️ Ubuntu ships the unit **`static`** → `enable` won't stick at boot. Force it:
  ```bash
  sudo install -d /etc/systemd/system/nvidia-persistenced.service.d
  printf '[Install]\nWantedBy=multi-user.target\n' | sudo tee /etc/systemd/system/nvidia-persistenced.service.d/install.conf
  sudo systemctl daemon-reload && sudo systemctl enable --now nvidia-persistenced
  ```
- ⚠️ `nvidia-smi` keeps showing **`Persistence-M: Disabled` — that is correct.** The daemon (not the
  deprecated flag) provides persistence; do **not** "fix" it with `nvidia-smi -pm 1`.

## Step 5 — Container access (optional)

**5a — Container engine.** The toolkit only *wires* an existing engine, so install one first. Docker's
official `docker-ce` repo lags new Ubuntu releases by months — if it has no suite for your codename
(`curl -fsI download.docker.com/linux/ubuntu/dists/$(. /etc/os-release; echo $VERSION_CODENAME)/Release`
→ 404/000, e.g. 26.04 `resolute`), install Ubuntu's own **`docker.io`** (current — 26.04 ships Docker 29.x).
Both provide `docker` + the `nvidia` runtime hook.
```bash
sudo apt-get install -y docker.io          # or docker-ce once the repo carries your codename
sudo usermod -aG docker "$USER"            # rootless docker CLI — re-login to take effect
```

**5b — NVIDIA repo + toolkit.** Add the repo (REFERENCE §5), then EITHER:
- **Full (required for Docker/containerd):** `sudo apt-get install -y nvidia-container-toolkit` → `nvidia-ctk`
  + an auto-generated CDI spec. Wire the engine, then restart it:
  ```bash
  sudo nvidia-ctk runtime configure --runtime=docker    # or containerd
  sudo systemctl restart docker
  ```
  Adds only a `runtimes.nvidia` block to `/etc/docker/daemon.json`; default runtime stays `runc` (opt in per
  container with `--gpus`). Podman needs no wiring (uses CDI directly).
- **Minimal (enumeration only):** `sudo apt-get install -y libnvidia-container-tools` → `nvidia-container-cli`.

**5c — Verify the GPU reaches a container:**
```bash
sudo docker run --rm --gpus all -e NVIDIA_DRIVER_CAPABILITIES=all ubuntu:24.04 nvidia-smi -L   # lists every GPU
```
`NVIDIA_DRIVER_CAPABILITIES=all` is what injects `nvidia-smi`/CUDA libs — `--gpus all` *selects* the GPUs but
caps decide the userspace, so bare `--gpus all` can return "executable not found". CDI path (Podman, or
Docker ≥ 25): `nvidia-ctk cdi list`; run with `--device nvidia.com/gpu=all`.

## Step 6 — BIOS (max serving perf / passthrough)

Generic GPU-serving profile: Above-4G + **Resize BAR** on, **Performance** power/EPP, disable deep
C-states / C1E-promotion / ASPM, **SR-IOV** on (for VM passthrough), VT-d/IOMMU available, ACS off for fast
bare-metal P2P (flip on only when isolating GPUs for VFIO), Sub-NUMA Clustering off. Full table in REFERENCE §6.
For **ASUS ESC8000-E12P** exact attribute tokens + apply/verify, use the `asus-esc8000-gpu-bios-tuning` skill.

## Verify (final)

```bash
nvidia-smi                                   # all GPUs, VRAM, ECC, driver ver
cat /proc/driver/nvidia/version              # "Open Kernel Module"
cat /proc/cmdline                            # iommu flags present (+ preserved tokens)
sudo dmesg | grep -iE 'DMAR|IOMMU'           # "IOMMU enabled"
ls /sys/kernel/iommu_groups | wc -l          # > 0
nvidia-smi topo -p2p r                        # P2P "OK" across GPUs (multi-GPU)
systemctl is-enabled nvidia-persistenced     # enabled
bash -lc 'nvcc --version'                      # runs (login shell)
```
