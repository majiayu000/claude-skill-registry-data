---
name: nix-flake-init
description: Initializes Nix flake.nix files for projects using flake-parts, automatically detecting programming languages (OpenSCAD, Python) and configuring appropriate development shells. Activates when user asks to create, initialize, or add a flake.nix, set up Nix development environment, or add direnv support.
allowed-tools: []
---

# Nix Flake Initialization Skill

## Purpose
Automatically create and configure `flake.nix` files for projects that don't have them yet, using flake-parts as the base template. The skill detects programming languages used in the project and extends the default devShell with necessary development packages.

## When to Activate
- User asks to "create a flake.nix" or "initialize a flake"
- User wants to "set up Nix development environment"
- User mentions "add flake support" or "nix-ify this project"
- User asks to "add direnv" or "create .envrc"
- Project lacks flake.nix and user asks about development setup

## Language Detection Strategy

### OpenSCAD
**Detection criteria:**
- Presence of `*.scad` files in the project
- File extensions: `.scad`

**DevShell packages:**
- `openscad-unstable` - Latest OpenSCAD version

### Python
**Detection criteria:**
- Presence of `*.py` files in the project
- Presence of `requirements.txt`, `pyproject.toml`, or `setup.py`

**DevShell packages:**
- If `requirements.txt` exists: Parse it and create `python3.withPackages` including all modules
- If no requirements file: Just include base `python3`

**Python module extraction:**
- Read `requirements.txt` line by line
- Extract package names (ignore version specifiers like `==7.4.2`)
- Convert package names to nixpkgs Python package names (usually lowercase, replace hyphens with underscores if needed)

## Flake Template Structure

Use this base template for all flakes:

```nix
{
  description = "PROJECT_DESCRIPTION";

  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.11";
  };

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [ "x86_64-linux" ];
      perSystem = { config, self', inputs', pkgs, system, ... }: {
        devShells.default = pkgs.mkShell {
          name = "default-dev-shell";
          meta.description = "Default development shell";
          packages = with pkgs; [
            LANGUAGE_SPECIFIC_PACKAGES
          ];
        };
      };
    };
}
```

## Implementation Steps

### Step 1: Check for Existing Flake
- Use Glob to check if `flake.nix` already exists
- If it exists, ask user if they want to modify or skip
- If it doesn't exist, proceed with creation

### Step 2: Detect Programming Languages
- Use Glob to search for language-specific files:
  - `**/*.scad` for OpenSCAD
  - `**/*.py` for Python
- Check for language-specific manifest files:
  - `requirements.txt` for Python dependencies
  - `pyproject.toml`, `setup.py` for Python projects

### Step 3: Build Package List
Based on detected languages, construct the packages list:

**For OpenSCAD:**
```nix
openscad-unstable
```

**For Python with requirements.txt:**
```nix
(python3.withPackages (ps: with ps; [ module1 module2 module3 ]))
```

**For Python without requirements:**
```nix
python3
```

### Step 4: Generate Project Description
- Use the project directory name as a basis
- If there's a README.md, read the first line or title
- Format as: "Development environment for [project-name]"

### Step 5: Create flake.nix
- Substitute PROJECT_DESCRIPTION with generated description
- Substitute LANGUAGE_SPECIFIC_PACKAGES with the constructed package list
- Write the file using the Write tool

### Step 6: Create .envrc and Update .gitignore
- **Always** create `.envrc` for direnv integration with content: `use flake`
- **IMPORTANT**: Ensure `.envrc` uses Unix line endings (LF, `\n`) NOT DOS line endings (CRLF, `\r\n`)
  - Use the Write tool with explicit LF line endings
  - The content should be exactly: `use flake\n` (with Unix newline)
- **Automatically** update `.gitignore` to include `.direnv/` if not already present
- If `.gitignore` doesn't exist, create it with `.direnv/` entry
- Inform user they need to run `direnv allow` to activate

### Step 7: Git Staging (If in Git Repo)
- **IMPORTANT**: Nix flakes require files to be tracked by Git before they can be evaluated
- If project is a git repository, stage the new files BEFORE running `nix flake check`:
  - Run `git add flake.nix`
  - Run `git add .envrc`
  - Run `git add .gitignore` (if modified or created)
- After staging, verify with `nix flake check`
- Remind user to run `git add flake.lock` after first `nix flake update`

## Example Outputs

### Example 1: OpenSCAD + Python Project

Detected files:
- `wifi-card.scad`, `qrcode-matrix.scad`
- `requirements.txt` with `qrcode==7.4.2`

Generated packages:
```nix
packages = with pkgs; [
  openscad-unstable
  (python3.withPackages (ps: with ps; [ qrcode ]))
];
```

### Example 2: Python-Only Project

Detected files:
- `main.py`, `utils.py`
- `requirements.txt` with `requests==2.31.0` and `flask==3.0.0`

Generated packages:
```nix
packages = with pkgs; [
  (python3.withPackages (ps: with ps; [ requests flask ]))
];
```

### Example 3: OpenSCAD-Only Project

Detected files:
- `model.scad`, `parts/base.scad`

Generated packages:
```nix
packages = with pkgs; [
  openscad-unstable
];
```

## Important Notes

1. **System Architecture**: Default template uses `x86_64-linux`. Ask user if they need other systems (e.g., `aarch64-linux`, `x86_64-darwin`, `aarch64-darwin`)

2. **nixpkgs Version**: Default uses `nixos-25.11`. User can modify this to `nixos-unstable` or other channels if needed

3. **Python Package Name Conversion**: Most Python packages have the same name in nixpkgs, but some differ:
   - `pillow` (PyPI) → `pillow` (nixpkgs) ✓
   - `beautifulsoup4` (PyPI) → `beautifulsoup4` (nixpkgs) ✓
   - Package names with hyphens often work as-is
   - If a package isn't found, suggest checking nixpkgs or using `buildPythonPackage`

4. **Post-Creation Steps**: Always inform the user to:
   - Files are automatically staged with `git add` if in a Git repo
   - Run `nix flake check` to verify the flake configuration
   - Run `nix flake update` to generate `flake.lock`
   - Run `direnv allow` to activate direnv (or use `nix develop` manually)
   - The `.envrc` and `.gitignore` updates are handled automatically

5. **Git Integration**: Automatically stage files if in a git repo:
   - `flake.nix`
   - `.envrc`
   - `.gitignore` (if modified/created)
   - Remind user to commit and to add `flake.lock` after generation

6. **Line Endings**: Always use Unix line endings (LF) for all generated files, especially `.envrc`. DOS line endings (CRLF) can cause issues with direnv and shell scripts on Unix systems.

## Error Handling

- If language detection finds no supported languages, create a minimal flake with empty packages list
- If requirements.txt parsing fails, use `python3.withPackages` with an empty list of packages.
- If user's system isn't `x86_64-linux`, ask which systems they need

## Future Extensions

The skill is designed to be easily extended with additional languages:
- Rust: detect `Cargo.toml`, add `cargo`, `rustc`
- Node.js: detect `package.json`, add `nodejs`, `nodePackages.npm`
- Go: detect `go.mod`, add `go`
- Java: detect `pom.xml` or `build.gradle`, add JDK

To extend, add new detection criteria and package mappings following the existing pattern.
