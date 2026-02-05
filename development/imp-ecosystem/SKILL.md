---
name: imp-ecosystem
description: Work with imp.lib and imp.gits for Nix flake development. Use when working with imp.lib directory imports, imp.gits multi-repo injection, .d fragment directories, flake-parts integration, or when the user mentions imp, imp.lib, imp.gits, or asks about directory-based Nix configuration.
---

# imp Ecosystem

The imp ecosystem provides directory-based configuration for Nix flakes:

- **imp.lib** - Directory imports and tree building for flake-parts
- **imp.gits** - Multi-repo file injection via sparse checkout

## Core Workflow

### Project Structure

```
my-project/
├── .imp/
│   └── gits/
│       └── config.nix       # imp.gits injection config
├── nix/
│   └── outputs/
│       └── perSystem/
│           ├── packages.d/
│           │   ├── 00-core.nix      # Your packages
│           │   └── 10-injected.nix  # From injection
│           ├── devShells.nix        # Your devShell
│           └── devShells.d/
│               └── 10-injected.nix  # Injected devShell
└── flake.nix
```

### imp.lib: Directory → Attrset

imp.lib converts directory structures into nested attrsets:

```nix
# flake.nix
{
  inputs.imp.url = "github:imp-nix/imp.lib";
  outputs = { imp, ... }:
    imp ./nix/outputs;  # imports everything under nix/outputs/
}
```

Naming rules:

| Path              | Attribute                      |
| ----------------- | ------------------------------ |
| `foo.nix`         | `foo`                          |
| `foo/default.nix` | `foo`                          |
| `foo_.nix`        | `foo` (escapes reserved names) |
| `_foo.nix`        | ignored                        |
| `foo.d/`          | merged fragments               |

### imp.gits: Multi-Repo Injection

Inject files from other repos into your workspace:

```nix
# .imp/gits/config.nix
{
  injections = [
    {
      name = "lintfra";
      remote = "https://github.com/org/lintfra.git";
      use = [
        "lint/ast-rules"
        "nix/outputs/perSystem/packages.d/10-lint.nix"
        "nix/outputs/perSystem/devShells.d/10-lintfra.nix"
      ];
    }
  ];
}
```

Commands:

```bash
imp-gits init              # Clone and setup injections
imp-gits pull              # Update injections
imp-gits pull --force      # Force update (overwrites local changes to injected files)
imp-gits status            # Show injection status
eval "$(imp-gits use X)"   # Switch git context to injection X
```

## Fragment Directories (.d pattern)

### Auto-merged outputs

These `.d` directories are auto-merged by imp.lib's `tree`:

- `packages.d/`, `devShells.d/`, `checks.d/`, `apps.d/`
- `overlays.d/`, `nixosModules.d/`, `homeModules.d/`, `darwinModules.d/`
- `nixosConfigurations.d/`, `darwinConfigurations.d/`, `homeConfigurations.d/`

Files sorted by name (00 before 10), merged with `lib.recursiveUpdate`.

**Base + fragments merge**: If both `foo.nix` and `foo.d/` exist, they merge:

```
packages.nix          # { default = myPkg; }
packages.d/
  10-extra.nix        # { lint = lintPkg; }
# Result: { default = myPkg; lint = lintPkg; }
```

### Manual fragment directories

Other `.d` dirs (e.g., `shellHook.d/`) are consumed via `imp.fragments`:

```nix
{ imp, ... }:
let
  hooks = imp.fragments ./shellHook.d;  # collects .sh files
in
{
  shellHook = hooks.asString;  # concatenated
}
```

## Common Patterns

### Composable devShells (injection pattern)

**Injected library provides** (`devShells.d/10-lintfra.nix`):

```nix
{ pkgs, self', ... }:
{
  lintfra = pkgs.mkShell {
    packages = [ pkgs.ast-grep self'.packages.lint ];
    shellHook = "echo 'Lint available'";
  };
}
```

**Consumer uses** (`devShells.nix`):

```nix
{ pkgs, self', ... }:
{
  default = pkgs.mkShell {
    inputsFrom = [ self'.devShells.lintfra ];  # compose!
    packages = [ /* your packages */ ];
  };
}
```

### Injected packages

**Injected** (`packages.d/10-lint.nix`):

```nix
{ pkgs, ... }:
{ lint = pkgs.writeShellScriptBin "lint" "..."; }
```

**Result**: `self'.packages.lint` available automatically.

### File-level inputs

Declare flake inputs at file level with `__inputs`:

```nix
{
  __inputs = {
    rust-overlay.url = "github:oxalica/rust-overlay";
  };
  __functor = _: { pkgs, rust-overlay, ... }:
    { default = pkgs.rust-bin.stable.latest.default; };
}
```

## Troubleshooting

### "attribute X missing"

- Check if `.d/` file returns correct attrset shape
- Verify `imp-gits pull` synced the file
- Run `nix flake check` for detailed errors

### imp-gits pull deletes local files

- Only happens with `--force` on files not in injection's `use` list
- Fixed in imp.gits 0.2.1+ - update your flake

### Conflict: foo.nix and foo.d/ both exist

- This is allowed for mergeable outputs (packages.d, devShells.d, etc.)
- Base file imports first, then fragments merge on top

## References

- [fragment-directories.md](references/fragment-directories.md) - Full .d pattern documentation
- [gits-workflow.md](references/gits-workflow.md) - imp.gits commands and workflows
