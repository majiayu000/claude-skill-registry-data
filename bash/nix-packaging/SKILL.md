---
name: nix-packaging
description: Flake structure, Home Manager module, nixGL wrapper. Load when touching flake.nix, packaging, or NixOS integration.
triggers:
  - nix
  - flake
  - "home-manager"
  - nixos
  - "nixGL"
  - packaging
  - derivation
---

# Nix packaging

Target: `nyxterm` available as a Nix flake. Linux first. Reproducible. Works on NixOS and on non-NixOS via [nixGL](https://github.com/nix-community/nixGL) for GPU drivers (same pattern Ghostty uses).

## Flake outputs

```nix
{
  outputs = { self, nixpkgs, ... }: {
    packages.${system}.default = nyxterm-bin;
    packages.${system}.nyxterm = nyxterm-bin;

    homeManagerModules.default = ./nix/hm-module.nix;
    nixosModules.default = ./nix/nixos-module.nix;  # optional, for system-level install

    devShells.${system}.default = ...;  # rust + node + tauri toolchain
    formatter.${system} = pkgs.nixfmt;
  };
}
```

## The derivation (Rust + Node)

Two-stage:

1. **Frontend build**: pnpm install + pnpm build → `dist/`. Vendor `pnpm-lock.yaml` with `pnpm fetch` for reproducibility. Use `pnpm.fetchDeps` (nixpkgs helper).
2. **Tauri build**: `cargo tauri build --no-bundle` (or specific bundle target).

Pin everything: Rust toolchain via `rust-overlay`, Node version, pnpm version, Tauri CLI version.

## nixGL wrapper

On non-NixOS distros, OpenGL/Vulkan drivers come from the host. Without wrapping, Tauri (which uses WebKitGTK with GPU acceleration) fails to find Mesa.

Wrapper pattern (from Ghostty's overlay):

```nix
nyxterm-wrapped = pkgs.runCommand "nyxterm" {} ''
  mkdir -p $out/bin
  cat > $out/bin/nyxterm <<EOF
  #!/usr/bin/env bash
  exec ${nixGL.nixGLMesa}/bin/nixGLMesa ${nyxterm}/bin/nyxterm "\$@"
  EOF
  chmod +x $out/bin/nyxterm
'';
```

User opts in via flake input. On NixOS, the wrapper is a no-op (drivers found via standard FHS).

## Home Manager module

`nix/hm-module.nix` exposes declarative config:

```nix
{ config, lib, ... }: {
  options.programs.nyxterm = with lib; {
    enable = mkEnableOption "nyxterm";
    theme = mkOption {
      type = types.str;
      default = "tokyo-night-night";
    };
    keybinds = mkOption {
      type = types.attrsOf types.str;
      default = {};
    };
    aiProviders = mkOption {
      type = types.attrsOf (types.submodule { ... });
      default = {};
    };
    # ... more
  };

  config = mkIf config.programs.nyxterm.enable {
    home.packages = [ pkgs.nyxterm ];
    xdg.configFile."nyxterm/config.toml".source = ...;  # generated from options
  };
}
```

User writes:

```nix
programs.nyxterm = {
  enable = true;
  theme = "tokyo-night-night";
  keybinds.prefix = "Ctrl+Space";
};
```

## AppImage / standalone

For non-Nix users, ship an AppImage with bundled webview runtime where possible. Linux only initially.

## macOS / Windows

Phase 2.5 or later. Tauri makes this technically free, but signing/notarization is a chore. Worth tracking under epic #22.

## CI for Nix

- `nix flake check` in GitHub Actions on every PR.
- `nix build .#default` builds the package.
- Cache via Cachix or Garnix.

## What we DON'T do

- Don't ship `nix run github:FullFran/nyxterm` that downloads on every run — too slow. Recommend `nix profile install` or HM install.
- Don't depend on `unstable` channel without pinning a specific rev in `flake.lock`.
- Don't auto-update the flake lock in CI. User-driven only.
