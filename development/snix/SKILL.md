---
name: snix
description: Rust Nix reimplementation for content-addressed rootfs builds. Minimal VM images for boxxy/codex-rs/toad agent runtimes.
version: 1.0.0
---


# snix Skill

> *"Nix, reimplemented in Rust."* -- snix.dev

> **Trit**: -1 (MINUS) - Build validation and rootfs construction

## Overview

**snix** is a Rust reimplementation of Nix (forked from Tvix) with a bytecode VM evaluator, content-addressed store, and library-oriented architecture. It provides the build layer for the Minimum Viable Runtime (MVR) — creating minimal Linux rootfs images that run AI agent TUIs inside boxxy (Apple Virtualization.framework) VMs.

```
┌─────────────────────────────────────────────────────┐
│                    snix BUILD LAYER                  │
│              (content-addressed store)              │
└──────────────────────┬──────────────────────────────┘
                       │
       ┌───────────────┼───────────────┐
       │               │               │
┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
│  Evaluate   │ │   Build     │ │   Store     │
│  (bytecode) │ │   (daemon)  │ │   (CAS)     │
│  trit: -1   │ │   trit: 0   │ │   trit: +1  │
└─────────────┘ └─────────────┘ └─────────────┘
       │               │               │
       └───────────────┼───────────────┘
                       │
               ┌───────▼───────┐
               │   rootfs.img  │
               │   (~75-130MB) │
               └───────────────┘
```

## Why snix

| Property | Nix (C++) | snix (Rust) |
|----------|-----------|-------------|
| Language | C++ | Rust |
| Evaluator | AST walker | Bytecode VM |
| Store | Monolithic | Content-addressed, granular |
| Library use | CLI only | Library-first |
| License | LGPL-2.1 | GPL-3.0 |
| macOS CI | Community | Dedicated |
| nixpkgs compat | Native | Yes (growing) |

- Pure Rust embeds into boxxy's Go/Rust toolchain without C++ dependency
- Bytecode VM evaluator is faster than Nix's AST walker
- Content-addressed store enables deduped, granular rootfs images
- Library-oriented — callable from Rust code, not just CLI
- [Fork of Tvix](https://snix.dev/blog/announcing-snix/) with dedicated CI and macOS support
- [devenv switching to snix eval](https://github.com/cachix/devenv/issues/1548) — ecosystem momentum

## Installation

```bash
# Clone from Forgejo
git clone https://git.snix.dev/snix/snix ~/i/snix

# Or from GitHub mirror
git clone https://github.com/cachix/snix ~/i/snix

# Build from source (Rust toolchain required)
cd ~/i/snix
cargo build --release

# Components
ls target/release/snix-*
# snix-eval      -- Nix expression evaluator (bytecode VM)
# snix-build     -- Build orchestrator
# snix-store     -- Content-addressed store daemon
# snix-cli       -- Unified CLI
```

## Minimal Rootfs Build

### Flake for codex-rs VM

```nix
# flake.nix — snix-evaluable minimal codex-rs VM rootfs
{
  description = "Minimal aarch64-linux rootfs for codex-rs in boxxy";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }: let
    system = "aarch64-linux";
    pkgs = import nixpkgs {
      inherit system;
      crossSystem = { config = "aarch64-unknown-linux-musl"; };
    };
  in {
    packages.${system} = {
      rootfs = pkgs.dockerTools.buildImage {
        name = "codex-minimal";
        tag = "latest";
        copyToRoot = pkgs.buildEnv {
          name = "codex-rootfs";
          paths = [
            pkgs.busybox          # shell + coreutils (~1.5MB)
            pkgs.gitMinimal       # git without docs/perl (~15-30MB)
            pkgs.cacert           # TLS root certificates (~0.2MB)
          ];
        };
        runAsRoot = ''
          mkdir -p /tmp /proc /dev
          mknod -m 666 /dev/null c 1 3
          mknod -m 666 /dev/urandom c 1 9
        '';
      };

      diskImage = pkgs.vmTools.runInLinuxVM (pkgs.runCommand "codex-disk" {} ''
        mkdir -p $out
        dd if=/dev/zero of=$out/rootfs.img bs=1M count=256
        mkfs.ext4 $out/rootfs.img
      '');
    };
  };
}
```

### Build with snix

```bash
# Evaluate the flake
snix eval .#packages.aarch64-linux.rootfs

# Build rootfs image
snix build .#packages.aarch64-linux.rootfs

# Inspect store paths
snix store ls /snix/store/<hash>-codex-rootfs
```

## Rootfs Composition

| Component | Size | Purpose |
|-----------|------|---------|
| Linux kernel (minimal, aarch64) | ~8-15 MB | Landlock 6.7+, seccomp-BPF |
| codex-rs + codex-linux-sandbox | ~50-80 MB | MUSL static binary |
| busybox | ~1.5 MB | Shell + coreutils |
| git (minimal) | ~15-30 MB | Source control |
| ca-certificates | ~0.2 MB | TLS roots |
| **Total rootfs** | **~75-130 MB** | |

## Kernel Requirements (codex-rs sandbox)

| Feature | Minimum | Ideal | Config Flag |
|---------|---------|-------|-------------|
| Landlock LSM | Linux 5.13 | Linux 6.7+ | CONFIG_SECURITY_LANDLOCK=y |
| Landlock ABI | V1 | V5 | (kernel version dependent) |
| seccomp-BPF | Linux 3.5 | - | CONFIG_SECCOMP_FILTER=y |
| User namespaces | Linux 3.8 | - | CONFIG_USER_NS=y |
| Mount namespaces | Linux 3.8 | - | CONFIG_NAMESPACES=y |
| Architecture | - | aarch64 | (Apple Silicon native) |

### Sandbox Layers (defense-in-depth)

1. macOS Virtualization.framework hypervisor (boxxy)
2. Landlock filesystem ACLs (/ = ro, writable_roots = rw)
3. seccomp-BPF syscall filter (blocks connect/accept/bind/listen/ptrace)
4. Mount namespace (.git dirs bind-mounted read-only)
5. User namespace (unprivileged, UID/GID mapping)
6. Process hardening (PR_SET_DUMPABLE=0, RLIMIT_CORE=0, LD_* stripped)

## boxxy Boot Integration

```clojure
;; ~/i/boxxy/examples/codex-vm.joke
;; Boot snix-built rootfs via Apple Virtualization.framework

(def codex-vm
  (vz/new-linux-vm-config
    {:kernel   "vmlinuz-6.7-aarch64"
     :initrd   "initrd-codex.img"
     :cmdline  "console=hvc0 root=/dev/vda rw quiet"
     :disk     "codex-rootfs.img"       ;; snix-built rootfs
     :memory   2                        ;; GB
     :cpus     4
     :network  {:nat true}}))           ;; NAT for API access

(println "Booting codex-rs VM...")
(vz/start-vm! codex-vm)
```

## Agent TUI Matrix (toad)

Agents running inside snix-built rootfs, driven by toad:

| Agent | Command | Trit | Role |
|-------|---------|------|------|
| claude | `toad -a claude` | 0 | Coordinator |
| codex | `toad -a codex` | -1 | Validator |
| goose | `toad -a goose` | +1 | Generator |
| copilot | `toad -a copilot` | 0 | Coordinator |
| gemini | `toad -a gemini` | +1 | Generator |

GF(3) check: `0 + (-1) + 1 + 0 + 1 = 1` — needs balancing validator agent per session.

## GF(3) Triads

```
snix (-1) ⊗ world-runtime (0) ⊗ agent-o-rama (+1) = 0 ✓  [MVR Core]
snix (-1) ⊗ flox (0) ⊗ hvm-runtime (+1) = 0 ✓  [Build Chain]
snix (-1) ⊗ nix-acset-worlding (-1) ⊗ codex-self-rewriting (+1+1) — needs split
nix-acset-worlding (-1) ⊗ snix (-1) ⊗ true-alife (+1) — rebalance via:
  snix (-1) ⊗ acsets (0) ⊗ hvm-runtime (+1) = 0 ✓  [Store Verification]
```

### MVR Triad (Minimum Viable Runtime)

```
         snix (-1)
        /         \
       /    MVR    \
      /      0      \
world-runtime (0) --- agent-o-rama (+1)
     BUILD ←→ RUN ←→ ORCHESTRATE
```

## Content-Addressed Store

```
/snix/store/
├── <hash>-busybox-1.36.1/
│   └── bin/
│       └── busybox              # 1.5MB static binary
├── <hash>-git-minimal-2.43.0/
│   └── bin/
│       └── git                  # 15-30MB
├── <hash>-ca-certificates/
│   └── etc/ssl/certs/
│       └── ca-bundle.crt        # 0.2MB
└── <hash>-codex-rootfs/
    └── ...                      # Composed rootfs
```

Key properties:
- **Content-addressed**: paths keyed by cryptographic hash
- **Deduplication**: identical content shared across builds
- **Reproducibility**: same inputs always produce same outputs
- **Granularity**: individual packages, not monolithic images

## Commands

```bash
# Build minimal rootfs
snix build .#packages.aarch64-linux.rootfs

# Evaluate without building
snix eval .#packages.aarch64-linux.rootfs

# Inspect store
snix store ls /snix/store/

# GC dead paths
snix store gc

# Boot in boxxy
cd ~/i/boxxy && ./boxxy boot codex-rootfs.img

# Run agents via toad
toad -a claude ~/i/soft-machine
toad -a codex ~/i/soft-machine
toad -a goose ~/i/soft-machine
```

## See Also

- [Minimum Viable Runtime](resources/mvr.md) — full MVR specification
- [nix-acset-worlding](../nix-acset-worlding/SKILL.md) — Nix store as ACSet
- [flox](../flox/SKILL.md) — Nix environment management
- [world-runtime](../world-runtime/SKILL.md) — VM lifecycle coordination
- [agent-o-rama](../agent-o-rama/SKILL.md) — Agent orchestration
- [codex-self-rewriting](../codex-self-rewriting/SKILL.md) — Codex behavior patterns
- [goose-introspection](../goose-introspection/SKILL.md) — Goose behavior analysis

## References

1. **snix** — https://snix.dev / https://git.snix.dev/snix/snix
2. **Tvix** — https://tvix.dev (upstream before fork)
3. **boxxy** — https://github.com/bmorphism/boxxy (Apple Virtualization.framework)
4. **codex-rs** — https://github.com/openai/codex (Rust Codex CLI)
5. **toad** — https://github.com/batrachianai/toad (Agent TUI driver)
6. **Landlock** — https://landlock.io (Linux security module)



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Systems Programming
- **nix-acset-worlding** [-1] via store semantics
  - Nix store modeled as Attributed C-Set
- **flox** [0] via environment management
  - Nix-based dev environments
- **world-runtime** [0] via VM lifecycle
  - Firecracker + Morph Infinibranch execution substrate

### Runtime Composition
- **hvm-runtime** [+1] via parallel reduction
  - GPU-accelerated interaction nets
- **kinfer-runtime** [-1] via inference
  - K-Scale robot inference runtime
- **agent-o-rama** [+1] via orchestration
  - Multi-agent coordination

### Agent Behaviors
- **codex-self-rewriting** [0] via codex-rs integration
  - OpenAI Codex behavior patterns
- **goose-introspection** [0] via behavior analysis
  - Block/Goose agent introspection

### Graph Theory
- **networkx** [0] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 2. Domain-Specific Languages

**Concepts**: embedded DSL, combinator, wrapper, Nix expression language

### GF(3) Balanced Triad

```
snix (-) + SDF.Ch2 (-) + [balancer] (+) — rebalance needed
snix (-) + SDF.Ch7.Propagators (0) + hvm-runtime (+) = 0 ✓
```

**Skill Trit**: -1 (MINUS - build validation)

### Secondary Chapters

- Ch1: Flexibility through Abstraction
- Ch8: Degeneracy (fallback build strategies)

### Connection Pattern

DSLs embed domain knowledge. snix embeds Nix semantics in Rust for reproducible builds.

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: -1 (MINUS)
Home: Prof
Poly Op: ⊗
Kan Role: Ran (right Kan extension - verification)
Color: #D89B73
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

Example balanced triads:
```
snix (-1) + world-runtime (0) + agent-o-rama (+1) = 0 ✓
snix (-1) + flox (0) + hvm-runtime (+1) = 0 ✓
snix (-1) + acsets (0) + true-alife (+1) = 0 ✓
```

This ensures compositional coherence in the Cat# equipment structure.
