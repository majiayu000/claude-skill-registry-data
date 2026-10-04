---
name: apptainer-images
description: Build and run Apptainer/Singularity images on HPC (PSC Bridges-2 and similar) when the host glibc or system ABI is too old for pip wheels (e.g. Isaac Sim manylinux_2_35). Use when creating .def files, building .sif images, binding ocean/scratch paths, wiring uv sync --locked inside containers, fixing UV_CACHE_DIR vs uv.toml conflicts, GPU passthrough with --nv, or non-interactive EULA prompts blocking imports.
argument-hint: [what to containerize or which failure to fix]
allowed-tools: Read, Write, Edit, Bash(singularity:*), Bash(apptainer:*), Bash(uv:*), Bash(interact:*), Bash(nvidia-smi:*)
---

# Apptainer / Singularity Images on HPC

Use a container when the **host userspace is the blocker** (glibc / manylinux tag), not when you just need Python packages. The image supplies system ABI + native libs; **`uv.lock` + `uv sync --locked`** supplies Python. Do not bake `.venv` or multi-GB wheels into the image.

## Core Recipe — minimal .def + build + run

**Definition** (`Bootstrap: docker`, Ubuntu 22.04 for glibc 2.35):

```def
Bootstrap: docker
From: ubuntu:22.04

%environment
    export LC_ALL=C.UTF-8
    export LANG=C.UTF-8
    export PATH="/usr/local/bin:${PATH}"
    export UV_LINK_MODE=copy
    export OMNI_KIT_ACCEPT_EULA=YES   # only if first import would prompt (Isaac/Omniverse)
    # Vulkan/EGL: point the loader at the NVIDIA ICDs we bake below (relative
    # library_path → resolves whatever `--nv` binds). REQUIRED for Isaac RTX.
    export VK_ICD_FILENAMES=/etc/vulkan/icd.d/nvidia_icd.json
    export __EGL_VENDOR_LIBRARY_FILENAMES=/usr/share/glvnd/egl_vendor.d/10_nvidia.json

%post
    export DEBIAN_FRONTEND=noninteractive
    apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl git git-lfs \
        python3.11 python3.11-dev python3.11-venv \
        build-essential cmake pkg-config \
        libgl1 libglu1-mesa libegl1 libgles2 libvulkan1 vulkan-tools \
        libx11-6 libxcb1 libxt6 libasound2
    # NVIDIA Vulkan + EGL ICDs. `--nv` binds the driver LIBS but in legacy mode
    # (use nvidia-container-cli = no) does NOT drop these JSONs where the loader
    # looks → Isaac fails with VkResult ERROR_INCOMPATIBLE_DRIVER / "GPU Foundation
    # not initialized". Bake them with RELATIVE library_path so the loader resolves
    # the lib `--nv` injected, regardless of host path.
    mkdir -p /etc/vulkan/icd.d /usr/share/glvnd/egl_vendor.d
    printf '%s\n' '{"file_format_version":"1.0.0","ICD":{"library_path":"libGLX_nvidia.so.0","api_version":"1.3.277"}}' \
        > /etc/vulkan/icd.d/nvidia_icd.json
    printf '%s\n' '{"file_format_version":"1.0.0","ICD":{"library_path":"libEGL_nvidia.so.0"}}' \
        > /usr/share/glvnd/egl_vendor.d/10_nvidia.json
    curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin sh
    apt-get clean && rm -rf /var/lib/apt/lists/*

%runscript
    exec "$@"
```

Then verify on a **GPU node**: `singularity exec --nv "$SIF" vulkaninfo --summary` must list the GPU
(GPU device, `driverName = NVIDIA`). If it says "no ICD" the JSON path/`VK_ICD_FILENAMES` is wrong;
if it lists only `llvmpipe`/mesa, `--nv` didn't bind `libGLX_nvidia` (check `nvliblist.conf`).

Install only what `%post` needs for the target app — no Python project deps.

**Build** on a **compute node** (PSC rejects container exec on login nodes):

```bash
cd <repo>
singularity build --force containers/app.sif containers/app.def
# apptainer build --force … works on the same .def
```

**Run** (GPU + workspace + ocean):

```bash
export WS=/ocean/projects/<grant>/<user>/refseg-workspace
export OCEAN=/ocean/projects/<grant>/<user>
export SIF="$WS/<repo>/containers/app.sif"

singularity exec --nv \
  --bind "$WS:/workspace" \
  --bind "$OCEAN:$OCEAN" \
  "$SIF" \
  bash -c 'cd /workspace/<repo> && uv sync --locked && uv run <entrypoint>'
```

On PSC, `singularity` and `apptainer` are the same engine; prefer `singularity` in docs.

## Separation of concerns (do not blur these)

| Layer | Owner | Where it lives |
|-------|--------|----------------|
| glibc, apt libs, `uv` binary | `.sif` image (~200–300 MB SquashFS) | `containers/*.sif` on ocean |
| Python packages | `uv.lock` | `.venv` under bound workspace |
| uv download cache | user `uv.toml` | large FS (ocean), **never** `$HOME/.cache/uv` |
| Render / job outputs | app config (`dataset_dir`, etc.) | ocean paths in YAML or under repo `datasets/` |

Mechanism (container ABI) ≠ policy (lockfile, cache path, output dirs).

## uv cache — the #1 footgun

**Correct:** persistent config in `$HOME/.config/uv/uv.toml` (on PSC: `/jet/home/<user>/.config/uv/uv.toml`):

```toml
cache-dir = "/ocean/projects/<grant>/<user>/.uv_cache"
```

**Wrong:**
- `UV_CACHE_DIR` in the image `%environment` — **overrides** `uv.toml` (precedence: CLI > env > file)
- Binding `$HOME/.cache/uv` — cache must not live on home quota
- Binding ocean to a *different* container path than the absolute path in `uv.toml`

**Required bind:** mount the ocean root at the **same absolute path** inside the container:

```bash
--bind "$OCEAN:$OCEAN"
```

Verify before a multi-GB sync:

```bash
singularity exec --bind "$OCEAN:$OCEAN" "$SIF" bash -c 'uv cache dir'
# must print the ocean path from uv.toml, not /tmp or ~/.cache
```

Singularity mounts `$HOME` on PSC, so `uv.toml` is picked up without an extra bind.

## GPU and non-interactive gotchas

- **`--nv`** passes host NVIDIA driver/libs; the image does not ship the driver.
- **Match the hardware's *capabilities* to what the process needs — not just count/memory.** Before requesting a GPU (or any node), ask what *features* the workload actually requires and confirm the requested SKU provides them: RT cores (hardware ray tracing), tensor cores, FP64, NVLink, a minimum CUDA compute capability, a display/graphics path, enough VRAM. A job can pass `nvidia-smi`, allocate fine, and still be fundamentally unable to run because the silicon lacks a needed capability. The error often masquerades as a driver/container bug (see case study 9), costing hours of chasing the wrong layer. Read the app's hardware requirements first; pick the SKU to match.
- **`bash -c`, NOT `bash -lc`, inside the container.** A *login* shell (`-l`) sources the host's bind-mounted `~/.bash_profile`/`~/.bashrc` (Singularity mounts `$HOME`), which (a) spams `module`/`conda`/`fzf: command not found` and (b) **prepends `~/.local/bin`, shadowing the image's `/usr/local/bin/uv` with the host's uv** — a silent version swap. The image already puts uv on `PATH` via `%environment`, so a plain `bash -c` is correct and hermetic.
- **Vulkan ICD for Isaac RTX (`ERROR_INCOMPATIBLE_DRIVER`).** `libvulkan1` (the loader) is necessary but **not sufficient**: the loader needs an NVIDIA *ICD JSON*, and **`--nv` does not inject one** — a documented Apptainer gap (apptainer#2210 for EGL; nvidia-container-toolkit#16/#1392 for Vulkan). `--nv` binds the CUDA libs only; the Vulkan/EGL ICDs are on you. So the loader finds no driver and Isaac dies at "GPU Foundation is not initialized." Two fixes: **(test, no rebuild)** bind the host's JSONs — `--bind /usr/share/vulkan/icd.d/nvidia_icd.json --bind /usr/share/glvnd/egl_vendor.d/10_nvidia.json --env VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/nvidia_icd.json`; **(durable)** bake them into the image with relative `library_path` + set the env in `%environment` (see Core Recipe — this is what NVIDIA's own Isaac Dockerfiles do). Verify with `vulkaninfo --summary` under `--nv`. `nvidia-smi` working proves CUDA, NOT Vulkan — they fail independently. NOT the same as the driver-version-misreport bug (`--/rtx/verifyDriverVersion/enabled=false`); that flag does **not** fix the missing-ICD case.
- **Isaac / Omniverse EULA:** first `import isaacsim` prompts `Do you accept the EULA? (Yes/No):` — hangs in batch/non-interactive. Set `OMNI_KIT_ACCEPT_EULA=YES` in `%environment` and in the app entrypoint **before** any Isaac import.
- **Editable path deps:** bind the **whole** meta-repo/workspace (`vision_core`, `reference_matching`, …), not just one sub-repo — AND make sure every sibling is checked out to a **commit compatible with the code you're running.** Editable deps import from source, so a sibling on a stale/detached HEAD throws `ImportError` on a renamed symbol or a *missing file* added in an unpulled commit (e.g. a proposer config the app's YAML references). Sync siblings (`git switch <branch> && git pull`, get them off detached HEADs) as a preflight.
- **`uv lock` on the host:** if host glibc is 2.28 and lock needs `manylinux_2_35` wheels, resolution fails on the host. Regenerate lock on glibc 2.35+ (local dev or inside this container), commit, then `uv sync --locked` in-container. Sibling-metadata changes (a renamed class in `vision_core`) also silently stale the lock → `uv sync --locked` refuses; regenerate it in-container.

## Validate cheaply before spending GPU SUs

A containerized GPU job pays SU while it boots and `uv sync`s. Catch failures on a **CPU node** (the container runs there too) before allocating a GPU — each rung exits in seconds and isolates one failure class:

```bash
# CPU node, no --nv needed:
singularity exec --bind "$WS:/workspace" --bind "$OCEAN:$OCEAN" "$SIF" bash -c '
  cd /workspace/<repo> && uv sync --locked'                                  # 1. lock matches deps?
singularity exec --bind ... "$SIF" bash -c '
  cd /workspace/<repo>/<srcdir> && uv run --no-sync python -c "import <pkg>"' # 2. sibling imports resolve?
singularity exec --bind ... "$SIF" bash -c '
  cd ... && uv run --no-sync python -c "from app.config import load; load(\"cfg.yaml\", [...])"'  # 3. config path asserts pass?
```

Pre-warming `.venv` on the CPU node also makes the GPU job's `uv sync --locked` a fast no-op (it reuses the `.venv` on shared storage), so you don't pay GPU SU for the multi-GB install.

## Diagnostic preamble (run after build)

```bash
singularity exec "$SIF" bash -c 'ldd --version | head -1'          # expect 2.35 for Ubuntu 22.04
singularity exec --nv "$SIF" nvidia-smi                             # GPU node only
singularity exec --bind "$OCEAN:$OCEAN" "$SIF" bash -c 'uv cache dir'
singularity exec --nv --bind "$WS:/workspace" --bind "$OCEAN:$OCEAN" "$SIF" \
  bash -c 'cd /workspace/<repo> && uv run python -c "import <pkg>"'
```

## Case studies (real failures → fix)

1. **`uv sync` fails on host with manylinux_2_35 wheel.** Host glibc 2.28 (PSC). → Ubuntu 22.04 container; sync inside with `--locked`.
2. **Container creation failed: mount source … doesn't exist.** Bound `$HOME/.cache/uv` but dir missing. → don't use home cache; use `uv.toml` on ocean; `mkdir -p` only if you truly need a bind target.
3. **`uv cache dir` → `/tmp/uv-cache` in container but correct on host.** Old image had `UV_CACHE_DIR=/tmp/...` in `%environment`. → remove it; rebuild with `--force`; env beats `uv.toml`.
4. **`import isaacsim` hangs forever.** EULA prompt with no TTY. → `OMNI_KIT_ACCEPT_EULA=YES` before import.
5. **Bind `$OCEAN:/scratch/$USER` but cache path is `/ocean/...`.** Absolute cache-dir in `uv.toml` not visible in container. → bind `$OCEAN:$OCEAN` at same path.
6. **Build fails: target already exists.** → `singularity build --force …`.
7. **Isaac boots then dies: `VkResult: ERROR_INCOMPATIBLE_DRIVER` / `Vulkan 1.1 is not supported` / `GPU Foundation is not initialized` / `CUDA libs present, but no suitable CUDA GPU was found`.** `nvidia-smi` worked, so CUDA was fine — but the image had `libvulkan1` yet **no NVIDIA Vulkan ICD JSON** (`/etc/vulkan/icd.d/` empty, `VK_ICD_FILENAMES` unset), and the host ran `--nv` in legacy mode (no nvidia-container-cli), which doesn't inject the ICD. The loader found no driver. **Confirmed by the community as a known `--nv` limitation** (apptainer#2210, nvidia-container-toolkit#16/#1392): `--nv` injects CUDA libs but not the Vulkan/EGL ICD JSONs. → **Test without rebuilding** by binding the host JSONs: `--bind /usr/share/vulkan/icd.d/nvidia_icd.json --bind /usr/share/glvnd/egl_vendor.d/10_nvidia.json --env VK_ICD_FILENAMES=...`. → **Make it durable** by baking them with relative `library_path` + env (Core Recipe); rebuild; verify `vulkaninfo --summary` lists the GPU under `--nv`. Red herring: the identical message also comes from a driver>535.255 Vulkan-version-misreport bug whose flag is `--/rtx/verifyDriverVersion/enabled=false` — but isaac-sim#357 shows that flag does NOT fix the containerized missing-ICD case (same `no suitable CUDA GPU found` tell). (Symptom is render-fatal even though extension startup continues past the error — it later emits black frames or crashes at RTX capture, so cancel early to save SU.)
8. **`ImportError: cannot import name 'Foo' from 'sibling_pkg'` (or a missing config file) inside the container — but the package is installed.** Editable sibling repos (`vision_core`, `reference_matching`) were on stale **detached HEADs**: one lacked a renamed symbol the app now imports; the other lacked a proposer-config YAML added in an unpulled commit that the app's config referenced. The lockfile/venv were fine — editable deps load from source. → `git switch master && git pull` each sibling (off detached HEAD, onto a compatible commit); re-run the CPU-side import + config-load smoke before resubmitting.
9. **`Skipping unsupported non-RTX GPU` / `No device could be created` after the Vulkan ICD was fixed — the hardware can't do what the app needs.** Isaac Sim's RTX renderer requires **hardware ray tracing (RT cores)**. A Tesla **V100** (Volta) — and compute GPUs like **A100/H100** — have none, so Isaac enumerates the GPU then rejects it (`Your GPUs do not support RayTracing: DXR or Vulkan ray_tracing`). `nvidia-smi` worked and CUDA was fine; the GPU was simply the wrong *class*. → request an **RT-core GPU**: on PSC Bridges-2 that's the **L40S** (`--gpus=l40s-48:1`), not v100/h100. General lesson (above): verify the SKU's *capabilities* match the workload before blaming the driver/container — this surfaced only after the ICD fix peeled back the outer error.

## When Applying This Skill

1. Confirm the failure is **ABI/userspace** (check `ldd --version` vs wheel manylinux tag), not a missing Python pin.
2. Write a minimal `.def`: Ubuntu 22.04 (or matching glibc), system libs only, `uv` in `%post`, no `UV_CACHE_DIR`.
3. Put uv cache in **`~/.config/uv/uv.toml`** on ocean; bind ocean at the same absolute path.
4. Build `.sif` on a compute node; smoke-test glibc, `--nv`, `uv cache dir`, then `uv sync --locked`.
5. Set EULA env if the workload uses Omniverse/Isaac.
6. Document binds + run command in the project README; move the plan to `plans/completed/` when verified.

## Reference implementation

`isaac_datagen/containers/` in refseg-workspace: `isaac_datagen.def`, `isaac_datagen.sif`, `containers/README.md`, project `README.md` PSC section.
