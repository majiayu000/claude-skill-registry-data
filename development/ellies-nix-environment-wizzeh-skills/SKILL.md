---
name: ellies-nix-environment
description: Nix environment patterns for Ellie's projects. Use when (1) a tool or command is not available on the system, or (2) setting up a new project that needs a development environment. Provides patterns for ad-hoc tool execution and flake-based devShells with direnv.
---

# Ellie's Nix Environment

## When a Tool Isn't Available

If a command fails because a tool isn't installed, use `nix run` to execute it:

```bash
nix run nixpkgs#<tool> -- <args>
```

Examples:
```bash
nix run nixpkgs#python3 -- script.py
nix run nixpkgs#jq -- '.field' file.json
nix run nixpkgs#ffmpeg -- -i input.mp4 output.gif
nix run nixpkgs#ripgrep -- "pattern" .
```

Do not suggest installing tools globally. Use `nix run` for one-off commands.

## Setting Up a New Project

When a project needs a development environment, create a flake with direnv:

### 1. Create `flake.nix`

```nix
{
  description = "Project description";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            # Add project dependencies here
          ];
        };
      });
}
```

### 2. Create `.envrc`

```bash
use flake .
```

### 3. Activate direnv

```bash
direnv allow
```

### 4. Add to `.gitignore`

```
.direnv/
```

## Rust Projects

For Rust projects, use rust-overlay to get the toolchain:

```nix
{
  description = "Rust project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    rust-overlay = {
      url = "github:oxalica/rust-overlay";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, rust-overlay }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        overlays = [ (import rust-overlay) ];
        pkgs = import nixpkgs { inherit system overlays; };
        rust = pkgs.rust-bin.nightly.latest.default.override {
          extensions = [ "rust-src" "rust-analyzer" ];
        };
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            rust
          ];
        };
      });
}
```

