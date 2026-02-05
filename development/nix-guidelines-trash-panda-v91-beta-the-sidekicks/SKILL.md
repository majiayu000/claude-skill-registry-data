---
name: nix-guidelines
description: Use when writing Nix code for flakes, modules, or packages
---

# Nix Guidelines

Guidelines for idiomatic Nix code with flakes and modules.

## When to Use

- Writing flake.nix files
- Creating NixOS/Home Manager modules
- Writing Nix packages
- Reviewing Nix code

## Critical Rule: No `with` Statements

**NEVER use `with` statements.** They:
- Break static analysis tools (nixd, nil)
- Create scope ambiguity
- Cripple IDE features

```nix
# ❌ WRONG
environment.systemPackages = with pkgs; [ git vim ];
meta = with lib; { license = licenses.mit; };

# ✅ CORRECT
environment.systemPackages = [ pkgs.git pkgs.vim ];
meta = { license = lib.licenses.mit; };
```

## Core Principles

1. **Explicit over Implicit** - Always use explicit attribute paths
2. **Declarative Design** - Think in systems, not scripts
3. **Pure Functions** - Leverage Nix's functional nature
4. **nixfmt-rfc-style** - Standard formatter

## Flake Structure

```nix
{
  description = "My project";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    home-manager = {
      url = "github:nix-community/home-manager";
      inputs.nixpkgs.follows = "nixpkgs";  # Deduplicate
    };
  };

  outputs = { self, nixpkgs, home-manager, ... }: {
    nixosConfigurations.myhost = nixpkgs.lib.nixosSystem {
      system = "x86_64-linux";
      modules = [
        ./configuration.nix
        home-manager.nixosModules.home-manager
      ];
    };
  };
}
```

## Module Structure

```nix
{
  lib,
  config,
  pkgs,
  ...
}:
let
  cfg = config.myNamespace.myModule;
in
{
  options.myNamespace.myModule = {
    enable = lib.mkEnableOption "my module";

    package = lib.mkOption {
      type = lib.types.package;
      default = pkgs.myPackage;
      description = "The package to use";
    };

    settings = lib.mkOption {
      type = lib.types.attrsOf lib.types.str;
      default = { };
      description = "Configuration settings";
    };
  };

  config = lib.mkIf cfg.enable {
    environment.systemPackages = [ cfg.package ];

    assertions = [
      {
        assertion = cfg.settings != { };
        message = "myModule.settings cannot be empty when enabled";
      }
    ];
  };
}
```

## Best Practices Checklist

- [ ] No `with` statements
- [ ] Explicit destructuring in function signatures
- [ ] nixfmt-rfc-style formatting
- [ ] Options properly namespaced
- [ ] Input follows optimized (for flakes)
- [ ] Prefer let-in over rec
- [ ] lib.mkIf for conditional config
- [ ] Assertions for validation
- [ ] Comments for complex logic

## Common Patterns

### Conditional Configuration
```nix
config = lib.mkMerge [
  (lib.mkIf cfg.enable {
    services.myService.enable = true;
  })

  (lib.mkIf (cfg.enable && cfg.monitoring.enable) {
    services.prometheus.exporters.myService.enable = true;
  })

  {
    # Always applied with lower priority
    services.myService.port = lib.mkDefault 8080;
  }
];
```

### Package Definition
```nix
{ lib, stdenv, fetchurl, openssl }:
stdenv.mkDerivation {
  pname = "mypackage";
  version = "1.0";

  src = fetchurl {
    url = "https://example.com/source.tar.gz";
    sha256 = lib.fakeSha256;
  };

  buildInputs = [ openssl ];

  meta = {
    description = "My package";
    license = lib.licenses.mit;
  };
}
```

### Script Wrapper
```nix
pkgs.writeShellApplication {
  name = "my-script";
  runtimeInputs = [ pkgs.jq pkgs.curl ];
  text = ''
    curl -s https://api.example.com | jq .
  '';
}
```

## Anti-Patterns to Avoid

### Don't Use rec
```nix
# ❌ Avoid rec
rec {
  a = 1;
  b = a + 1;
}

# ✅ Use let-in
let
  a = 1;
in {
  inherit a;
  b = a + 1;
}
```

### Explicit Destructuring
```nix
# ❌ Wrong
args: with args; stdenv.mkDerivation { ... }

# ✅ Correct
{ stdenv, fetchurl, lib }: stdenv.mkDerivation { ... }
```

## Performance Tips

- Use `inputs.nixpkgs.follows` to deduplicate inputs
- Split outputs for granular dependencies
- Profile with `NIX_SHOW_STATS=1 nix build`
- Consider `builtins.readFile` for large strings

## Validation Commands

```bash
# Check flake
nix flake check

# Format code
nixfmt-rfc-style .

# Evaluate without building
nix eval .#packages.x86_64-linux.default

# Show flake outputs
nix flake show
```

## Module Option Types

```nix
lib.types.bool           # Boolean
lib.types.str            # String
lib.types.int            # Integer
lib.types.path           # Path
lib.types.package        # Nix package
lib.types.listOf type    # List of type
lib.types.attrsOf type   # Attribute set of type
lib.types.nullOr type    # Type or null
lib.types.enum ["a" "b"] # Enumeration
lib.types.submodule { }  # Nested options
```

## Remember

> Minor verbosity from explicit patterns is a **feature** - it makes code self-documenting and machine-readable.
