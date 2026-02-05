---
name: nix
description: Develop with Nix including packages, flakes, NixOS, and derivations. Activate when working with .nix files, flake.nix, flake.lock, or user mentions Nix, nixpkgs, NixOS, derivations, flakes, nix-shell, nix develop, home-manager, or packaging.
---

# Nix Development

Research-first Nix development using **parallel DeepWiki queries** for accurate, up-to-date information.

## Workflow

```
1. IDENTIFY  → Match question to relevant repos
2. QUERY     → Launch parallel subagents to query DeepWiki
3. SYNTHESIZE → Combine results into actionable guidance
```

## Repo Routing

### Language & Concepts
| Topic | Repos to Query |
|-------|----------------|
| Nix language, builtins, syntax | `NixOS/nix.dev` |
| Attribute sets, functions, let bindings | `NixOS/nix.dev` |
| Lazy evaluation, recursion | `NixOS/nix.dev` |
| Derivations (concept) | `NixOS/nix.dev` |
| Nix store, paths, hashes | `NixOS/nix.dev` |
| String interpolation, multiline strings | `NixOS/nix.dev` |
| Path handling, ./. vs toString | `NixOS/nix.dev` |
| Import, imports, IFD | `NixOS/nix.dev` |
| lib functions (mkIf, mkOption, etc.) | `NixOS/nixpkgs`, `NixOS/nix.dev` |
| Nix REPL, nix eval | `NixOS/nix.dev` |

### Packaging
| Topic | Repos to Query |
|-------|----------------|
| stdenv, mkDerivation | `NixOS/nixpkgs` |
| Build phases (configure, build, install, check) | `NixOS/nixpkgs` |
| Fetchers (fetchFromGitHub, fetchurl, fetchgit) | `NixOS/nixpkgs` |
| Dependencies (buildInputs, nativeBuildInputs, propagatedBuildInputs) | `NixOS/nixpkgs` |
| Patches, substituteInPlace, patchShebangs | `NixOS/nixpkgs` |
| Wrappers (makeWrapper, wrapProgram, symlinkJoin) | `NixOS/nixpkgs` |
| Meta attributes, licenses, maintainers | `NixOS/nixpkgs` |
| Creating packages from URLs | `nix-community/nix-init`, `NixOS/nixpkgs` |
| Cross-compilation, pkgsCross | `NixOS/nixpkgs` |
| Static builds, pkgsStatic, pkgsMusl | `NixOS/nixpkgs` |
| Trivial builders (writeShellScript, writeText, runCommand) | `NixOS/nixpkgs` |
| Passthru attributes, tests | `NixOS/nixpkgs` |

### Language-Specific Builders
| Topic | Repos to Query |
|-------|----------------|
| Rust (buildRustPackage, cargoHash) | `NixOS/nixpkgs` |
| Go (buildGoModule, vendorHash) | `NixOS/nixpkgs` |
| Python (buildPythonPackage, buildPythonApplication) | `NixOS/nixpkgs` |
| Node.js (buildNpmPackage, node2nix) | `NixOS/nixpkgs` |
| Haskell (haskellPackages, cabal2nix) | `NixOS/nixpkgs` |
| Java, Maven, Gradle | `NixOS/nixpkgs` |
| C/C++ (cmake, meson, autotools) | `NixOS/nixpkgs` |

### Flakes
| Topic | Repos to Query |
|-------|----------------|
| Flake basics, inputs, outputs | `NixOS/nix.dev` |
| Flake templates, init | `NixOS/nix.dev` |
| Flake modules, composition | `hercules-ci/flake-parts` |
| perSystem, multi-platform | `hercules-ci/flake-parts` |
| Flake overlays | `hercules-ci/flake-parts`, `NixOS/nix.dev` |
| Flake checks, nix flake check | `NixOS/nix.dev`, `hercules-ci/flake-parts` |
| Flake apps, nix run | `NixOS/nix.dev` |
| Flake lock, updating inputs | `NixOS/nix.dev` |
| follows, input overrides | `NixOS/nix.dev` |
| Flake-compat (legacy support) | `NixOS/nix.dev` |

### Development
| Topic | Repos to Query |
|-------|----------------|
| Development shells (mkShell, devShells) | `NixOS/nixpkgs`, `NixOS/nix.dev` |
| nix develop, nix-shell | `NixOS/nix.dev` |
| direnv integration | `NixOS/nix.dev` |
| Environment variables | `NixOS/nixpkgs` |

### Overrides & Customization
| Topic | Repos to Query |
|-------|----------------|
| override, overrideAttrs | `NixOS/nixpkgs` |
| Overlays | `NixOS/nixpkgs`, `NixOS/nix.dev` |
| packageOverrides | `NixOS/nixpkgs` |
| Fixed-point evaluation | `NixOS/nix.dev` |

### NixOS & System Config
| Topic | Repos to Query |
|-------|----------------|
| NixOS modules, options | `NixOS/nix.dev` |
| NixOS configuration | `NixOS/nix.dev` |
| systemd services | `NixOS/nix.dev` |
| Users, groups, permissions | `NixOS/nix.dev` |
| Networking, firewall | `NixOS/nix.dev` |
| Boot, GRUB, systemd-boot | `NixOS/nix.dev` |
| Filesystems, partitions | `NixOS/nix.dev` |

### Home Manager
| Topic | Repos to Query |
|-------|----------------|
| Home-manager basics, installation | `nix-community/home-manager` |
| User environment, dotfiles | `nix-community/home-manager` |
| Home-manager modules, options | `nix-community/home-manager` |
| Programs configuration (git, vim, etc.) | `nix-community/home-manager` |
| Home-manager + NixOS | `nix-community/home-manager`, `NixOS/nix.dev` |
| Home-manager + nix-darwin | `nix-community/home-manager`, `nix-darwin/nix-darwin` |
| Home-manager standalone | `nix-community/home-manager` |

### macOS (nix-darwin)
| Topic | Repos to Query |
|-------|----------------|
| nix-darwin basics, installation | `nix-darwin/nix-darwin` |
| macOS system configuration | `nix-darwin/nix-darwin` |
| Darwin modules, options | `nix-darwin/nix-darwin` |
| Homebrew integration | `nix-darwin/nix-darwin` |
| macOS services, launchd | `nix-darwin/nix-darwin` |
| Darwin + home-manager | `nix-darwin/nix-darwin`, `NixOS/nix.dev` |

### Contributing & Tooling
| Topic | Repos to Query |
|-------|----------------|
| Updating package versions/hashes | `Mic92/nix-update` |
| Testing nixpkgs changes | `Mic92/nixpkgs-review` |
| nixpkgs contribution workflow | `Mic92/nix-update`, `Mic92/nixpkgs-review` |
| pkgs/by-name structure | `NixOS/nixpkgs` |

### Testing & CI
| Topic | Repos to Query |
|-------|----------------|
| NixOS tests, nixosTest | `NixOS/nixpkgs`, `NixOS/nix.dev` |
| VM tests, runNixOSTest | `NixOS/nixpkgs` |
| Package tests, passthru.tests | `NixOS/nixpkgs` |
| Hydra CI | `NixOS/nix.dev` |
| GitHub Actions with Nix | `NixOS/nix.dev` |

### Containers & Images
| Topic | Repos to Query |
|-------|----------------|
| Docker images, dockerTools | `NixOS/nixpkgs` |
| OCI images, buildImage | `NixOS/nixpkgs` |
| Minimal Docker images, streamLayeredImage | `NixOS/nixpkgs` |
| VM images, disk images | `NixOS/nixpkgs` |
| ISO images | `NixOS/nixpkgs` |

### Debugging & Maintenance
| Topic | Repos to Query |
|-------|----------------|
| Build failures, debugging | `NixOS/nixpkgs`, `NixOS/nix.dev` |
| Garbage collection, nix-collect-garbage | `NixOS/nix.dev` |
| Binary caches, substituters, Cachix | `NixOS/nix.dev` |
| Nix profiles, generations | `NixOS/nix.dev` |
| Nix daemon, nix.conf | `NixOS/nix.dev` |
| Sandboxing, pure evaluation | `NixOS/nix.dev` |
| Reproducibility, content-addressing | `NixOS/nix.dev` |

**Query multiple repos when topics overlap.**

## Parallel DeepWiki Queries

Launch subagents to query relevant repos simultaneously:

```
// Single message with multiple parallel Task calls:
Task(
  subagent_type="Explore",
  model="haiku",
  prompt="Use mcp__deepwiki__ask_question to query repo 'NixOS/nixpkgs' with question: '<USER_QUESTION>'. Return the key findings."
)

Task(
  subagent_type="Explore",
  model="haiku",
  prompt="Use mcp__deepwiki__ask_question to query repo 'NixOS/nix.dev' with question: '<USER_QUESTION>'. Return the key findings."
)
```

### Example Query Patterns

**"How do I package a Rust CLI tool?"**
```
→ Query NixOS/nixpkgs: "How does buildRustPackage work? What attributes are required?"
→ Query nix-community/nix-init: "How to generate a Rust package derivation from a GitHub URL?"
```

**"How do I create a flake with multiple systems?"**
```
→ Query NixOS/nix.dev: "How do flakes handle multiple systems?"
→ Query hercules-ci/flake-parts: "How to use perSystem for multi-platform flakes?"
```

**"How do I update a package in nixpkgs?"**
```
→ Query Mic92/nix-update: "How to use nix-update to bump package versions?"
→ Query Mic92/nixpkgs-review: "How to test package changes with nixpkgs-review?"
```

**"How do I override a package?"**
```
→ Query NixOS/nixpkgs: "How do override and overrideAttrs work?"
→ Query NixOS/nix.dev: "What are overlays and how to use them?"
```

## DeepWiki Repos

| Repo | Best For |
|------|----------|
| `NixOS/nix.dev` | Nix language, tutorials, flake basics, NixOS |
| `NixOS/nixpkgs` | Package builders, stdenv, overrides, packaging patterns |
| `nix-community/nix-init` | Auto-generating derivations from URLs |
| `nix-community/home-manager` | User environment, dotfiles, program configs |
| `Mic92/nix-update` | Bumping versions and updating hashes |
| `Mic92/nixpkgs-review` | Testing PRs and local changes |
| `hercules-ci/flake-parts` | Modular flake configuration, perSystem |
| `nix-darwin/nix-darwin` | macOS system configuration, Darwin modules, launchd |
