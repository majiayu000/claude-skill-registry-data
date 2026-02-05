---
name: using-flake-parts
description: Expert guidance for using flake-parts framework in Nix flakes. Use when converting flakes to flake-parts, organizing modular flake configurations, working with perSystem, creating reusable flake modules, handling overlays, or debugging flake-parts issues.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Flake-Parts Expert

Specialized guidance for the flake-parts framework - a modular system for organizing Nix flakes.

## What is Flake-Parts?

Flake-parts is a framework that applies the NixOS module system to flake organization. It eliminates boilerplate for multi-system builds by generating per-system outputs automatically.

**Core benefit**: Define packages once in `perSystem`, automatically generated for all target systems.

## Structure with mkFlake

Flake-parts organizes flakes into logical sections:

```nix
{
  inputs.flake-parts.url = "github:hercules-ci/flake-parts";

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      # Target architectures - define once
      systems = [ "x86_64-linux" "aarch64-linux" ];

      # External modules
      imports = [ ./modules/packages.nix ];

      # Multi-system configuration (defined once, generated for all systems)
      perSystem = { config, pkgs, system, ... }: {
        packages.hello = pkgs.hello;
        devShells.default = pkgs.mkShell {
          packages = [ config.packages.hello ];
        };
      };

      # Traditional flake-level attributes (single-system)
      flake = {
        nixosConfigurations.machine = { };
      };
    };
}
```

**Generated structure:**
```nix
# Input:
perSystem.packages.hello = pkgs.hello;

# Output:
packages.x86_64-linux.hello = <derivation>;
packages.aarch64-linux.hello = <derivation>;
```

## perSystem vs flake

**Use `perSystem` for things that build across multiple platforms:**
- Packages, devShells, apps
- Formatters, checks
- Anything that should exist per-system

**Use `flake` for unique, non-system-specific outputs:**
- `nixosConfigurations` (each machine is unique)
- `homeConfigurations` (each config is unique)
- Custom flake outputs

### Standard perSystem Options

Flake-parts provides these standard options in `perSystem`:

- **`packages`** - Derivations to build (e.g., `packages.myapp = pkgs.hello;`)
- **`apps`** - Executable applications (for `nix run`)
- **`devShells`** - Development environments (for `nix develop`)
- **`checks`** - Tests and validation (run with `nix flake check`)
- **`formatter`** - Code formatter (single package, run with `nix fmt`)
- **`legacyPackages`** - Large package sets (not evaluated by default, for performance)

All are automatically generated for each system in the `systems` list.

## Module Arguments

Flake-parts provides special arguments to avoid repetitive `.${system}` interpolation.

### Per-System Arguments (in `perSystem`)

**`pkgs`** - nixpkgs for current system:
```nix
perSystem = { pkgs, ... }: {
  packages.myapp = pkgs.writeShellScriptBin "myapp" "echo hello";
};
```

**`system`** - Current architecture string:
```nix
perSystem = { system, ... }: {
  # system = "x86_64-linux", "aarch64-linux", etc.
};
```

**`inputs'`** (inputs prime) - Inputs with system auto-selected:
```nix
# Without inputs':
packages.bar = inputs.foo.packages.${system}.bar;

# With inputs':
perSystem = { inputs', ... }: {
  packages.bar = inputs'.foo.packages.bar;
};
```

**`self'`** (self prime) - This flake's outputs with system pre-selected:
```nix
perSystem = { self', ... }: {
  devShells.default = pkgs.mkShell {
    packages = [ self'.packages.myapp ];
  };
};
```

**`config`** - Per-system configuration values:
```nix
perSystem = { config, ... }: {
  packages.foo = ...;
  packages.bar = ... config.packages.foo ...;  # Reference other packages
};
```

**`final`** (with easyOverlay) - Package set after overlays:
```nix
perSystem = { pkgs, final, ... }: {
  imports = [ inputs.flake-parts.flakeModules.easyOverlay ];

  packages.lib = pkgs.callPackage ./lib.nix { };
  packages.app = pkgs.callPackage ./app.nix {
    my-lib = final.lib;  # Use overlaid version
  };
};
```

### Top-Level Arguments

**`withSystem`** - Enter a system's scope to access perSystem values:

This bridges single-system outputs (like NixOS configs) with multi-system packages:

```nix
flake.nixosConfigurations.machine = withSystem "x86_64-linux" (
  { config, ... }:
    # Now have access to all perSystem arguments
    nixpkgs.lib.nixosSystem {
      modules = [{
        environment.systemPackages = [
          config.packages.myapp    # Access perSystem packages
          config.packages.mytool
        ];
      }];
    }
);
```

Without `withSystem`: `self.packages.x86_64-linux.myapp` (repetitive and verbose).

**`getSystem`** - Function to retrieve per-system config:
```nix
let
  x86Packages = (getSystem "x86_64-linux").packages;
in
  # Use packages from specific system
```

**`moduleWithSystem`** - Brings perSystem arguments into top-level module scope (advanced).

### Function Signature Inspection

The module system uses `builtins.functionArgs` to determine which arguments to pass:

```nix
# ✅ CORRECT - explicitly name what you need
{ pkgs, system, config, ... }: { }

# ❌ WRONG - catch-all doesn't get special arguments
args: { }  # args won't contain pkgs, system, etc.
```

Only named parameters in your function signature receive values.

### The @ Pattern

Access multiple scopes without shadowing:

```nix
{ config, ... }: {
  myTopLevelOption = "foo";

  perSystem = toplevel@{ config, pkgs, ... }: {
    # config          = per-system config
    # toplevel.config = top-level config

    packages.example = pkgs.writeText "value"
      toplevel.config.myTopLevelOption;
  };
}
```

## Essential Patterns

### Convert Standard Flake to Flake-Parts

**Before:**
```nix
outputs = { nixpkgs, ... }:
  let
    systems = [ "x86_64-linux" "aarch64-linux" ];
    forAllSystems = nixpkgs.lib.genAttrs systems;
  in {
    packages = forAllSystems (system: {
      hello = nixpkgs.legacyPackages.${system}.hello;
    });
  };
```

**After:**
```nix
outputs = inputs@{ flake-parts, ... }:
  flake-parts.lib.mkFlake { inherit inputs; } {
    systems = [ "x86_64-linux" "aarch64-linux" ];
    perSystem = { pkgs, ... }: {
      packages.hello = pkgs.hello;
    };
  };
```

### Simple Module Import

```nix
# flake.nix
{
  imports = [ ./modules/packages.nix ];
}

# modules/packages.nix
{ perSystem = { pkgs, ... }: {
  packages.hello = pkgs.hello;
}; }
```

### importApply (pass flake-level context to modules)

Flake-parts-specific utility for passing arguments like `withSystem` to modules:

```nix
# flake.nix
{
  imports = [
    (inputs.flake-parts.lib.importApply ./modules/nixos.nix {
      inherit withSystem;
    })
  ];
}

# modules/nixos.nix
{ withSystem }: { inputs, ... }: {
  flake.nixosConfigurations.machine = withSystem "x86_64-linux" (
    { config, ... }:
      inputs.nixpkgs.lib.nixosSystem { ... }
  );
}
```

**Why importApply is needed**: Modules imported via `imports` don't have access to the flake's lexical scope (like `withSystem`). `importApply` lets you pass those as arguments.

### easyOverlay Module

Flake-parts module that auto-generates overlays from perSystem packages:

```nix
perSystem = { config, pkgs, final, ... }: {
  imports = [ inputs.flake-parts.flakeModules.easyOverlay ];

  packages = {
    mylib = pkgs.stdenv.mkDerivation { ... };
    myapp = pkgs.stdenv.mkDerivation {
      buildInputs = [ final.mylib ];  # Use overlaid version
    };
  };

  # Automatically generates overlays.default
  overlayAttrs = {
    inherit (config.packages) mylib myapp;
  };
};
```

**Key distinction**:
- `pkgs` = "previous" package set (before overlay)
- `final` = "final" package set (after overlay)

Use `final` when packages reference each other to get the overlaid versions.

### Reusable Flake Modules

Export modules for use in other flakes:

```nix
# your-tool/flake.nix
{
  flake.flakeModules.default = {
    perSystem = { config, lib, pkgs, ... }: {
      options.your-tool = {
        enable = lib.mkEnableOption "your-tool";
        package = lib.mkOption {
          type = lib.types.package;
          default = pkgs.your-tool;
        };
      };

      config = lib.mkIf config.your-tool.enable {
        packages.your-tool = config.your-tool.package;
      };
    };
  };
}

# consumer-flake/flake.nix
{
  inputs.your-tool.url = "github:you/your-tool";

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [ inputs.your-tool.flakeModules.default ];

      perSystem.your-tool.enable = true;
    };
}
```

## Best Practices

1. **Don't traverse inputs** - Never iterate through `inputs` with `mapAttrs` or similar (causes unnecessary fetching and evaluation)
2. **Namespace options** - Use `mymodule.foo` not just `foo` to avoid collisions
3. **Favor perSystem** - Most work happens there (packages, shells, checks)
4. **Use specific options** - Prefer `foo.package` over `foo.flake` for better granularity
5. **Use `'` suffixed arguments** - Prefer `inputs'` and `self'` over manual system selection

## Debugging

Enable debug mode:

```nix
{
  debug = true;
  # ... rest of config
}
```

Inspect with `nix repl`:
```bash
nix repl
:lf .
currentSystem.allModuleArgs.pkgs        # Inspect current system pkgs
debug.allSystems.x86_64-linux           # Inspect specific system
currentSystem.options.packages.files    # See where values are defined
debug.options.systems.declarations      # See where options are declared
```

## Common Issues

### "path does not exist" Error
Files must be git-tracked for flakes to see them:
```bash
git add .claude/skills/flake-parts/
# OR for quick testing:
git add -N file.nix  # Track without staging content
```

### Circular Dependency
Don't access `self` directly in modules. Use `self'` in `perSystem` or return functions from top-level.

### Wrong Module Context
Use `@` syntax to access both top-level and perSystem config:
```nix
perSystem = toplevel@{ config, ... }: {
  # config = perSystem config
  # toplevel.config = top-level config
}
```

### Undefined Variable in Module Argument
The module system only passes arguments you explicitly name:
```nix
# ✅ CORRECT
{ pkgs, system, config, ... }: { }

# ❌ WRONG
args: { }  # Won't receive special arguments
```

## Beyond the Basics

For specialized flake-parts features, load these guides:

- **[module-arguments.md](module-arguments.md)** - Complete reference for all module arguments, the @ pattern, and function signature inspection
- **[overlays.md](overlays.md)** - easyOverlay module details, final vs pkgs distinction
- **[modular-organization.md](modular-organization.md)** - importApply patterns, reusable flakeModules, dogfooding
- **[advanced.md](advanced.md)** - Partitions, custom outputs, debug mode, migration from standard flakes
