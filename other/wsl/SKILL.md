---
name: wsl
description: "Windows Subsystem for Linux (WSL) on Windows 10 and Windows 11: WSL1 vs WSL2 architecture, filesystem performance (ext4 VHD, 9P protocol), networking (NAT/mirrored mode, DNS tunneling, VPN compatibility), GPU passthrough, WSLg, systemd support, .wslconfig/wsl.conf, distro management, memory management (Vmmem), development workflows (VS Code Remote, Docker Desktop, Dev Containers), and enterprise deployment. Use when: \"WSL\", \"WSL2\", \"WSL1\", \"Windows Subsystem for Linux\", \"wsl.conf\", \".wslconfig\", \"WSLg\", \"wsl --install\", \"Linux on Windows\", \"Vmmem\", \"ext4.vhdx\", \"9P protocol\", \"mirrored networking WSL\", \"GPU WSL\", \"Docker WSL\". Do NOT use for general Windows Client administration — use the `windows-client` skill. Do NOT use for generic Ubuntu/Linux administration once inside the WSL guest and unrelated to the Windows integration layer (filesystem, networking mode, GPU passthrough) — use the `ubuntu` skill or the cli-scripting plugin."
license: MIT
---

# WSL (Windows Subsystem for Linux)

This skill covers Windows Subsystem for Linux (WSL) on Windows 10 and Windows 11. It provides deep knowledge of both WSL1 and WSL2 architectures, their tradeoffs, and how to configure, optimize, and troubleshoot WSL across all supported Windows versions. For general Windows Client administration, see the `windows-client` skill.

**Current state:** WSL2 is the default and recommended version. WSL went fully open-source in May 2025. The WSL kernel tracks the Linux LTS series, updated via Windows Update or `wsl --update`.

You have deep knowledge of:

- WSL1 (syscall translation via lxss.sys/lxcore.sys) vs WSL2 (lightweight Hyper-V utility VM with real Linux kernel)
- Filesystem architecture (ext4 VHD, VolFS, DrvFs, 9P protocol cross-filesystem overhead)
- Networking (NAT mode, mirrored mode, DNS tunneling, auto-proxy, localhost forwarding, VPN compatibility)
- GPU passthrough (GPU-PV, CUDA on NVIDIA, DirectML, OpenGL/Vulkan via translation layers)
- USB device passthrough via usbipd-win
- WSLg (Wayland compositor in-VM, XWayland, PulseAudio, GPU-accelerated rendering)
- systemd support (native since WSL 0.67.6, September 2022)
- Configuration files (.wslconfig global, wsl.conf per-distro)
- Distro management (install, list, import/export, version conversion, unregister)
- Memory management (Vmmem, dynamic balloon, autoMemoryReclaim, sparseVhd, swap)
- Development workflows (VS Code Remote WSL, Docker Desktop WSL2 backend, Git credential sharing, cross-compilation, Dev Containers)
- Enterprise deployment (Group Policy, Intune MDM, offline install, custom kernel, security considerations, DLP)
- Version-specific differences between Windows 10 and Windows 11 WSL capabilities

## How to Approach Tasks

Classify the request: installation, configuration, performance, networking, GPU, development workflow, enterprise management, or troubleshooting.

**Identify WSL1 vs WSL2 first** (`wsl --list --verbose`) — they behave fundamentally differently. **Identify the Windows build** — mirrored networking, WSLg, systemd, and memory reclaim require specific builds. Reason from the VM boundary, 9P overhead, filesystem location, and networking mode; recommend PowerShell commands for the Windows side and bash for the Linux side.

## Core Expertise

### WSL1 vs WSL2 Architecture

**WSL1** uses kernel-mode syscall translation (lxss.sys + lxcore.sys). ELF binaries execute natively but Linux syscalls are mapped to NT equivalents. No Linux kernel runs. Cross-filesystem I/O to Windows drives is fast (no VM boundary) but syscall coverage is ~80%. Does not support Docker daemon, kvm, full ebpf, or io_uring.

**WSL2** runs a genuine Linux kernel inside a lightweight Hyper-V utility VM. Each distro shares a single VM instance with isolated rootfs. The kernel is Microsoft-maintained (github.com/microsoft/WSL2-Linux-Kernel). Near-100% syscall compatibility. Supports Docker, kvm (nested virt), ebpf, io_uring. Linux-native I/O is significantly faster (ext4 on VHD), but cross-filesystem I/O is slower (9P protocol crosses VM boundary).

| Scenario | WSL1 | WSL2 |
|---|---|---|
| `git status` on `/mnt/c/repo` | Fast | Slow (9P) |
| Compiling in `~/project` | Moderate | Fast (ext4) |
| Docker daemon | Not supported | Supported |
| Full syscall compat | ~80% | ~100% |
| Boot time | Instant | ~1-2 seconds |

**Rule of thumb:** Keep project files inside the WSL2 filesystem (`~/project`, not `/mnt/c/Users/...`) for build-intensive workloads.

### Filesystem Architecture

The WSL2 `ext4.vhdx` grows automatically up to the configured limit (default 1 TB) but does **not** automatically shrink when files are deleted. The ext4 layer frees blocks but the VHD file on NTFS retains size.

```powershell
# Compact VHD (distro must be shut down)
wsl --shutdown
Optimize-VHD -Path "$env:LOCALAPPDATA\Packages\<distro>\LocalState\ext4.vhdx" -Mode Full
```

**Cross-filesystem access:**
- Windows to Linux: `\\wsl.localhost\<distro-name>\` (9P server inside WSL2)
- Linux to Windows: `/mnt/c/`, `/mnt/d/` (DrvFs mounts, configured in wsl.conf)

The **9P2000.L** protocol incurs a context switch, message encode/decode, and NTFS operation for every file operation crossing the boundary. For projects with thousands of small files (node_modules, virtualenvs, cargo target), this overhead compounds significantly.

### Networking

**NAT mode (default):** WSL2 VM gets a private IP on `vEthernet (WSL)`. Host performs NAT. WSL IP changes on every restart. Localhost forwarding from Windows to WSL services is automatic in recent builds.

**Mirrored mode (Windows 11 22H2+):** WSL sees the same network interfaces as Windows. WSL IP matches host IP. IPv6 works correctly. Reduces VPN compatibility issues.

```ini
# ~/.wslconfig
[wsl2]
networkingMode=mirrored
dnsTunneling=true      # Routes DNS through Windows DNS client stack
autoProxy=true         # Applies Windows proxy settings to WSL env vars
```

**VPN compatibility:** VPN clients that modify routing or DNS can break WSL2 NAT networking. Mitigations: use mirrored mode, enable dnsTunneling, restart WSL after VPN connects.

### GPU Passthrough (GPU-PV)

WSL2 supports GPU acceleration via GPU-PV (paravirtualized driver). The guest `dxgkrnl` communicates with the Windows GPU driver through the hypervisor. No separate GPU driver install inside WSL.

- **CUDA (NVIDIA):** Install `cuda-toolkit` inside WSL; use host NVIDIA driver (470.76+)
- **DirectML:** AMD, Intel, NVIDIA via D3D12
- **OpenGL/Vulkan:** Via Mesa D3D12 translation layer

**Limitations:** Only one GPU visible inside WSL (primary adapter), multi-GPU not supported via GPU-PV.

### WSLg (GUI Applications)

WSLg runs a Wayland compositor (Weston) inside the WSL VM. X11 apps use XWayland. Audio streams through PulseAudio to Windows audio via RDP. GPU-accelerated compositing via D3D12/GPU-PV when available. Built-in on Windows 11; available on Windows 10 21H2+.

```bash
# No xming or VcXsrv needed
sudo apt install gedit && gedit &
```

Clipboard automatically shared between Windows and WSL GUI apps.

### systemd Support

Native systemd support since WSL 0.67.6 (September 2022). Enable per-distro:

```ini
# /etc/wsl.conf
[boot]
systemd=true
```

With systemd enabled: services start at distro boot, `snap` packages work, `systemctl enable` persists services, `journalctl` available. Without systemd, use `[boot] command = "service docker start"` for startup services.

### Configuration Files

**~/.wslconfig** (Windows-side, global, applies to all WSL2 distros):
```ini
[wsl2]
memory=8GB                    # Hard cap for VM
processors=4                  # vCPU limit
swap=2GB
networkingMode=mirrored
dnsTunneling=true
guiApplications=true          # WSLg
nestedVirtualization=true

[experimental]
autoMemoryReclaim=gradual     # Reclaim unused memory gradually
sparseVhd=true                # VHD auto-shrinks on host
```

**/etc/wsl.conf** (Linux-side, per-distro):
```ini
[automount]
options = "metadata,umask=22,fmask=11"

[network]
generateResolvConf = true
hostname = my-wsl-machine

[interop]
enabled = true
appendWindowsPath = true

[boot]
systemd = true

[user]
default = myusername
```

Changes to .wslconfig require `wsl --shutdown` to take effect.

### Distro Management

```powershell
wsl --list --online             # Available distros from Store
wsl --install -d Ubuntu-24.04   # Install specific distro
wsl --list --verbose            # Installed distros with state/version
wsl --set-version Ubuntu 2      # Convert WSL1 to WSL2
wsl --set-default-version 2     # Default for new installs
wsl --export Ubuntu backup.tar  # Backup
wsl --import MyDistro C:\WSL\MyDistro backup.tar --version 2  # Restore/clone
wsl --import-in-place MyDistro C:\WSL\ext4.vhdx  # Import VHD directly (Win11)
wsl --unregister Ubuntu         # Delete (destructive)
wsl --shutdown                  # Stop all distros + VM
wsl --terminate Ubuntu          # Stop one distro
```

### Memory Management

WSL2 memory is dynamic via a VM balloon driver. The host sees this as the **Vmmem** process in Task Manager.

```ini
# ~/.wslconfig
[wsl2]
memory=8GB

[experimental]
autoMemoryReclaim=gradual    # gradual | dropcache | disabled
sparseVhd=true               # VHD sparse file (auto-shrinks)
```

Manual reclaim inside WSL: `sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'`

Swap is on a separate VHD (default 25% of memory limit). Disable with `swap=0`.

### Development Workflows

**VS Code Remote WSL:** `code .` from inside WSL connects VS Code on Windows to the WSL filesystem. Extensions and terminal run inside WSL.

**Docker Desktop WSL2 Backend:** Docker daemon runs inside a `docker-desktop` distro. Your distro gets access via mounted socket. No separate Hyper-V VM needed.

**Git credential sharing:**
```bash
git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe"
```

**Key rule:** Keep repos inside WSL filesystem (`~/projects`). Cross-filesystem Git operations on `/mnt/c/` are significantly slower due to 9P overhead.

### USB Device Passthrough

Physical USB devices can be attached to WSL2 using **usbipd-win** (USB/IP protocol):

```powershell
# Install on Windows
winget install usbipd

# List USB devices
usbipd list

# Attach device to WSL (run as admin)
usbipd attach --wsl --busid 1-7
```

Use cases: USB serial devices (Arduino, microcontrollers), smartcards, USB cameras, hardware security keys.

### Cross-Compilation

WSL2 provides full Linux toolchains for cross-compiling:

```bash
# Linux ARM64 cross-compilation
sudo apt install gcc-aarch64-linux-gnu
aarch64-linux-gnu-gcc -o myapp-arm64 main.c

# Windows EXE from Linux (MinGW)
sudo apt install mingw-w64
x86_64-w64-mingw32-gcc -o myapp.exe main.c
```

### Dev Containers

VS Code Dev Containers work natively with WSL2 -- the container runs inside WSL's Docker, and VS Code connects through the Remote WSL + Docker extension chain.

### Enterprise Deployment

**Group Policy / Intune** (ADMX templates available):
- **Allow WSL** -- enable/disable WSL entirely
- **Allow WSL1** -- prevent fallback to WSL1
- **Allowed distros** -- whitelist specific distros by name
- **Allow custom kernel** -- control kernel override capability
- **Allow kernel debugging** -- restrict debug access

Group Policy path: `Computer Configuration > Administrative Templates > Windows Components > Windows Subsystem for Linux`

**Custom kernel deployment:**
```ini
# ~/.wslconfig -- use organization-approved kernel
[wsl2]
kernel=C:\\IT\\WSL\\approved-kernel\\bzImage
```

**Security considerations:**
- Files inside `ext4.vhdx` are not scanned by most DLP tools by default -- assess data residency risk
- NAT mode provides some network isolation; mirrored mode exposes WSL to the host network
- Windows Defender scans `/mnt/` paths but not WSL native filesystem directly -- real-time protection inside WSL requires a Linux AV agent
- SSH keys and tokens in WSL are accessible to any process in that distro
- WSL kernel updates can be managed via custom kernel path or controlled Windows Update policies

**Offline / air-gapped install:**
```powershell
# Download on connected machine, transfer to air-gapped host
wsl --import UbuntuOffline C:\WSL\UbuntuOffline C:\offline\ubuntu-rootfs.tar --version 2
```

## Version-Specific Differences

| Windows Version | Key WSL Milestone |
|---|---|
| 1607 (Anniversary) | WSL1 introduced |
| 2004 (20H1) | WSL2 GA, `wsl --install` |
| Win11 21H2 | WSLg built-in |
| Win11 22H2 | Mirrored networking, systemd support |
| 2023 builds | Memory reclaim improvements, sparseVhd |
| 2024 builds | DNS tunneling, auto-proxy, firewall improvements |
| May 2025 | WSL goes fully open-source |

Features available only on Windows 11: mirrored networking, DNS tunneling, auto-proxy, `wsl --import-in-place`, improved WSLg integration. WSL2 core functionality works on both Windows 10 and 11.

## Troubleshooting Quick Reference

| Symptom | Likely Cause | Resolution |
|---|---|---|
| No internet from WSL | VPN or DNS misconfiguration | Enable mirrored networking + dnsTunneling; restart WSL after VPN connects |
| Vmmem using excessive RAM | No memory cap; aggressive page caching | Set `memory=` in .wslconfig; enable `autoMemoryReclaim=gradual` |
| Slow builds / git in WSL | Project files on `/mnt/c/` (9P overhead) | Move project to `~/` inside WSL filesystem |
| DNS resolution failure | Auto-generated resolv.conf unreachable | Set `generateResolvConf=false`, create manual `/etc/resolv.conf` |
| systemd not starting | Missing wsl.conf setting | Add `[boot] systemd=true` in `/etc/wsl.conf`, run `wsl --shutdown` |
| GPU/CUDA not working | NVIDIA driver installed inside WSL | Remove nvidia-driver from WSL; only install cuda-toolkit |
| VHD file growing forever | ext4 frees blocks but VHD retains size | Enable `sparseVhd=true` or manually `Optimize-VHD` |
| `wsl --install` fails | Windows features not enabled | Manually enable VirtualMachinePlatform and Microsoft-Windows-Subsystem-Linux |

## Common Pitfalls

1. **Project files on /mnt/c/** -- 9P overhead makes builds, git operations, and package installs dramatically slower. Always clone repos into `~/`.
2. **Vmmem consuming all RAM** -- Set `memory=` in .wslconfig and enable `autoMemoryReclaim=gradual`. Older builds had aggressive page caching without reclaim.
3. **VHD never shrinking** -- Enable `sparseVhd=true` in .wslconfig for automatic shrink, or manually `Optimize-VHD` after `wsl --shutdown`.
4. **VPN breaks WSL networking** -- Use mirrored networking + dnsTunneling on Windows 11. On Windows 10, restart WSL after VPN connects.
5. **DNS failures** -- If auto-generated resolv.conf points to an unreachable gateway, set `generateResolvConf=false` in wsl.conf and create manual `/etc/resolv.conf`.
6. **systemd not starting** -- Ensure `[boot] systemd=true` in `/etc/wsl.conf` (inside the distro, not .wslconfig) and `wsl --shutdown` to restart.
7. **NVIDIA driver inside WSL** -- Do NOT install nvidia-driver inside WSL2. GPU-PV uses the host driver. Only install cuda-toolkit inside WSL.
8. **DLP blind spot** -- Files in ext4.vhdx bypass most Windows DLP agents. Enterprise environments should assess data residency risk.
9. **WSL1 to WSL2 conversion failure** -- Requires VirtualMachinePlatform feature enabled. Check with `Get-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform`.
10. **appendWindowsPath bloat** -- Windows PATH appended to Linux PATH can cause slow command lookup. Set `appendWindowsPath=false` in wsl.conf if not needed.

## Diagnostic Scripts

Run these for rapid WSL assessment:

| Script | Purpose |
|---|---|
| `scripts/01-wsl-health.ps1` | WSL version, distros, kernel, WSLg, systemd, VHD sizes, .wslconfig |
| `scripts/02-wsl-network.ps1` | Networking mode, DNS, port forwarding, firewall, VPN detection, connectivity |

## Reference Files

Load these for deep knowledge:
- `references/architecture.md` -- WSL1 vs WSL2 internals, filesystem, networking, GPU-PV, WSLg, systemd
- `references/best-practices.md` -- .wslconfig/wsl.conf tuning, distro management, memory, dev workflows, enterprise deployment
