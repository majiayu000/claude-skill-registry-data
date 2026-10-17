---
name: environments
description: Set up reproducible robotics environments with uv, Docker, or GPU hosts.
---

# Environments

Define the runtime contract before writing around machine-specific accidents.
Local and remote runs should differ only where the hardware genuinely differs.

## Choose the smallest sufficient boundary

- **uv:** pure-Python robotics, ML, data, and tooling without required system
  packages. Commit the lockfile and run project commands through `uv run`.
- **Docker:** ROS 2, native libraries, apt packages, an exact Linux userspace,
  or deployment as a container.
- **Docker plus uv:** use Docker for the system layer and a project environment
  for substantial Python dependencies; do not turn the image's system Python
  into an untracked package set.
- **Remote GPU host:** use when the workload has no viable local hardware path.
  Record this as a deliberate exception to local/remote symmetry.

Preflight the actual machine before deciding. Confirm architecture, OS, Docker
daemon, accelerator, driver, disk, and available Python tooling. Use the Robium
doctor if present; fall back to direct probes when it is not.

## Keep the contract reproducible

- Pin Python and dependency resolution with a lockfile, or pin the container
  base and build inputs. Avoid `latest` for reproducible applications.
- Keep dependency declarations in one source of truth; do not preserve manual
  installation steps as hidden prerequisites.
- Match container CUDA/runtime requirements to the target host driver rather
  than the developer laptop.
- Design remote work as headless first. Use web visualization instead of making
  X forwarding part of the normal workflow.
- Test the same entry command in the target environment and prove important
  hardware, file, device, network, and display assumptions.
- Before claiming first-run reproducibility, run the complete setup from a
  clean project copy with the relevant package, model, and asset caches empty.
  A warm development checkout can hide broken fetch and bootstrap behavior.

## Go deeper only when needed

- Pure Python and lockfiles: [uv patterns](references/uv-patterns.md).
- ROS/system images, build layout, and parity: [Docker patterns](references/docker-patterns.md).
- NVIDIA passthrough and headless operation: [GPU and remote](references/gpu-and-remote.md).
- Real-robot LAN, Wi-Fi, DDS/NAT, and Mac host issues: [robot networking](references/robot-networking.md).
- Workloads that can exist only on cloud GPUs: [GPU cloud](references/gpu-cloud.md),
  then the relevant provider skill for provisioning.
- macOS, Apple Silicon, arm64, and cold-build evidence: [platform notes](PLATFORM-NOTES.md).
- Use the bundled examples only as starting shapes; verify all tags and install
  steps against current upstream documentation.

Cross into `integration` when multiple modules, containers, or transports must
be wired together. Cross into a deployment skill only after the image and
runtime contract work locally or in an equivalent target environment.

## Done

- A fresh machine can reproduce the environment from committed inputs.
- The same documented command starts the workload locally and remotely, except
  for named hardware flags.
- GPU, devices, network, files, and display behavior are verified on the target.
- Current details match official [uv](https://docs.astral.sh/uv/),
  [Docker](https://docs.docker.com/), ROS image, and
  [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/)
  documentation.
