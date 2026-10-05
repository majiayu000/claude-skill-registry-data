---
name: nix
type: reference
description: Reference for Nix commands, nix-shell and nix shell patterns, package lookup, Nix string escaping, and Nix flakes (flake commands, devShell patterns, templates, path:. usage). ALWAYS read BEFORE running nix commands or modifying flake.nix.
---

## Nix Command Reference

### Modern Nix CLI (2.x / Flakes)

The modern `nix` CLI operates on installables (flake attributes, store paths, or expressions).

| Task | Command | Description |
| --- | --- | --- |
| Run ad-hoc command | `nix run nixpkgs#<pkg> -- <args>` | Run binary without installing |
| Temporary shell | `nix shell nixpkgs#<pkg1> nixpkgs#<pkg2>` | Add packages to current shell environment |
| Enter dev environment | `nix develop path:.` | Open bash shell with dev dependencies |
| Run in dev environment | `nix develop path:. -c <cmd>` | Execute command within devShell |
| Build flake package | `nix build path:.#<pkg>` | Build package (creates `./result` link) |
| Build without symlink | `nix build --no-link path:.#<pkg>` | Build package without creating `./result` |
| Build with logs | `nix build -L path:.#<pkg>` | Print build logs in real time |
| Select derivation output | `nix build 'path:.#<pkg>^dev,static'` | Select specific derivation outputs |
| Build all outputs | `nix build 'path:.#<pkg>^*'` | Select all derivation outputs |
| Search packages | `nix search nixpkgs <query>` | Search package names and descriptions |
| Evaluate expression | `nix eval path:.#<attr>` | Evaluate Nix attribute to value |
| Evaluate raw string | `nix eval --raw path:.#<attr>` | Output raw evaluated string without quotes |
| Evaluate JSON | `nix eval --json path:.#<attr>` | Output evaluated Nix structure as JSON |
| Interactive REPL | `nix repl --file '<nixpkgs>'` | Start REPL with nixpkgs |
| Interactive Flake REPL | `nix repl path:.` | Start REPL and inspect flake outputs |
| Format flake | `nix fmt` | Run configured flake formatter |

### Flake Operations

Always use `path:.` or `path:/path/to/repo` in local workspaces.

```bash
# Validate flake schema and outputs
nix flake check path:.

# Show flake outputs graph
nix flake show path:.

# Show flake metadata and locked inputs
nix flake metadata path:.

# Update all flake inputs
nix flake update

# Update a single input only
nix flake lock --update-input <input-name>

# Pin input to specific rev or branch
nix flake lock --override-input <input-name> github:nixos/nixpkgs/<rev>
```

#### Why `path:.` Matters

When referencing a local directory without the `path:` scheme (e.g. `.`), Nix defaults to Git-mode (`git+file:`), which **only includes files tracked by Git**. Untracked or newly created files are ignored. Using `path:.` tells Nix to read the filesystem directly, making untracked files immediately available.

---

### Store & Diagnostic Commands

```bash
# Show dependency path / why package is in closure
nix why-depends path:.#<pkg1> path:.#<pkg2>

# Print store path information and closure size
nix path-info -r -h /nix/store/<path>

# Compare store closures (diff two builds or profiles)
nix store diff-closures /nix/store/<pathA> /nix/store/<pathB>

# Garbage collect unreferenced store paths
nix store gc
nix-collect-garbage -d                 # Also delete old profile generations
```

---

### Script Interpreters & Shebangs

#### Modern `nix` Shebang (Recommended)

```bash
#!/usr/bin/env nix
#! nix shell nixpkgs#bash nixpkgs#curl nixpkgs#jaq --command bash

curl -s https://api.example.com | jaq .
```

#### Python with Modern `nix` Shebang

```python
#!/usr/bin/env nix
#! nix shell nixpkgs#python3 nixpkgs#python3Packages.requests --command python3

import requests
print(requests.get("https://api.example.com").json())
```

#### Legacy `nix-shell` Shebang

```bash
#!/usr/bin/env nix-shell
#! nix-shell -i bash --pure
#! nix-shell -p bash curl jaq
#! nix-shell -I nixpkgs=https://nixos.org/channels/nixos-26.05/nixexprs.tar.xz

curl -s https://api.example.com | jaq .
```

---

### String Escaping in Nix

When generating code or configuration containing string interpolations (e.g., TypeScript, Bash, JavaScript):

| Desired Output | Nix Syntax | Notes |
| --- | --- | --- |
| `${variable}` | `''${variable}` | Escape Nix interpolation with `''` |
| `$${variable}` | `$''${variable}` | Escape literal dollar before variable |
| `''${literal}` | `'''${literal}` | Three quotes for literal double-single-quote |
| `''` | `'''` | Escape literal double single quotes |

#### Example: Generating Script with Template Literals

```nix
{
  xdg.configFile."my-plugin.ts".text = ''
    function log(msg: string) {
      console.log(`[''${timestamp}] ''${msg}`);
    }
  '';
}
```

---

### Package Lookup & Verification

- Search packages using `nix search nixpkgs <query>`.
- Find packages providing a specific binary: `nix-locate bin/<command>` (from `nix-index`).
- **Never** use `nix-env -i`; prefer declarative configuration, `nix run`, `nix shell`, or `pkgs.mkShell`.

---

### devShell & Package Helper Patterns

#### `mkShell` vs `mkShellNoCC`

- **`pkgs.mkShell`**: Includes C/C++ compiler toolchain (gcc/clang, make, binutils) in standard environment. Use for native compilation or native C extensions.
- **`pkgs.mkShellNoCC`**: Omits C compiler. Use for pure scripting languages (Python, JavaScript, Go, Rust with rustup) where a C toolchain is unnecessary.

#### `pkgs.writeShellApplication`

Preferred helper for writing robust Bash scripts with automatic `shellcheck` validation and explicit runtime dependencies:

```nix
pkgs.writeShellApplication {
  name = "my-script";
  runtimeInputs = with pkgs; [ curl jaq ];
  text = ''
    curl -s "https://api.example.com" | jaq .
  '';
}
```

#### Templates & Examples

- Basic devShell flake: [examples/flake-basic.nix](examples/flake-basic.nix)
- Multi-repo devShell integration: [examples/flake-inputs-from.nix](examples/flake-inputs-from.nix)
- Python environment with uv: [examples/flake-python-uv.nix](examples/flake-python-uv.nix)
- Package overlay pattern: [examples/overlay-pattern.nix](examples/overlay-pattern.nix)

---

### Formatting

Check formatting:

```bash
nix run path:.#treefmt -- --ci
```

Apply formatting:

```bash
nix run path:.#treefmt
```
