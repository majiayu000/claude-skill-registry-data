---
name: dotnet-techne-inspect
description: "Use when you need to inspect NuGet package APIs, list public types, or decompile method/property signatures. Keywords: inspect package API, list types, decompile type, method signatures, NuGet interface."
disable-model-invocation: false
user-invocable: true
license: MIT
compatibility: Requires dotnet-inspect OR ilspycmd global tool. Works with bash (Linux/macOS) or PowerShell (Windows).
metadata:
  author: Metalnib
  version: "1.2.0"
  trigger_keywords:
    - inspect package api
    - list types
    - decompile type
    - method signatures
    - nuget interface
---

# .NET NuGet Package Inspector

Inspect public APIs of .NET NuGet packages without writing throwaway C# code. Lists types (classes, interfaces, enums) and decompiles full type definitions with method signatures, properties, and attributes.

## Requirements

One of these .NET global tools must be installed:

- **`dotnet-inspect`** (preferred) — .NET 10+ SDK required
  ```bash
  dotnet tool install -g dotnet-inspect
  ```
- **`ilspycmd`** (fallback) — .NET 8+ SDK required
  ```bash
  dotnet tool install -g ilspycmd
  ```

The NuGet package you want to inspect must be restored locally (present in `~/.nuget/packages/`). If not, run `dotnet restore` in a project that references it.

## When to use this skill

Use when the user asks to:
- Inspect a NuGet package's public API
- List types/interfaces/classes in a .NET package
- View method signatures or properties of a NuGet type
- Understand what a .NET client library provides
- "What does IFooApi look like?" for a referenced NuGet

## Workflow

### Step 0: Detect available tool

**Always run this first** to determine which backend to use.

**Bash (Linux/macOS):**
```bash
./scripts/detect-tool.sh
```

**PowerShell (Windows):**
```powershell
.\scripts\detect-tool.ps1
```

Output: `dotnet-inspect` or `ilspycmd`. If neither is found, the script prints install instructions and exits with error.

### Step 1: List public types in a package

**Bash:**
```bash
./scripts/list-types.sh <package-name> <version> [tfm]
# Example:
./scripts/list-types.sh PrimeLabs.Service.Assets.Client 1.1.1
./scripts/list-types.sh Refit 8.0.0 net8.0
```

**PowerShell:**
```powershell
.\scripts\list-types.ps1 -PackageName <name> -Version <ver> [-Tfm <tfm>]
# Example:
.\scripts\list-types.ps1 -PackageName PrimeLabs.Service.Assets.Client -Version 1.1.1
```

The `tfm` parameter (target framework moniker) defaults to auto-detection (picks the highest available). Specify it explicitly if the package supports multiple frameworks (e.g., `net8.0`, `net6.0`, `netstandard2.0`).

### Step 2: Inspect a specific type

**Bash:**
```bash
./scripts/inspect-type.sh <full-type-name> <package-name> <version> [tfm]
# Example:
./scripts/inspect-type.sh PrimeLabs.Service.Assets.Client.IAssetsApi PrimeLabs.Service.Assets.Client 1.1.1
./scripts/inspect-type.sh Refit.HttpMethodAttribute Refit 8.0.0
```

**PowerShell:**
```powershell
.\scripts\inspect-type.ps1 -TypeName <full-type-name> -PackageName <name> -Version <ver> [-Tfm <tfm>]
# Example:
.\scripts\inspect-type.ps1 -TypeName PrimeLabs.Service.Assets.Client.IAssetsApi -PackageName PrimeLabs.Service.Assets.Client -Version 1.1.1
```

### Helper: Find DLL path (ilspycmd only)

If you need the raw DLL path for manual ilspycmd usage:

**Bash:**
```bash
./scripts/find-dll.sh <package-name> <version> [tfm]
```

**PowerShell:**
```powershell
.\scripts\find-dll.ps1 -PackageName <name> -Version <ver> [-Tfm <tfm>]
```

## Quick Reference

```bash
# === Full inspection workflow (Bash) ===
./scripts/detect-tool.sh                                    # 1. Which tool?
./scripts/list-types.sh MyPackage 2.0.0                     # 2. What types?
./scripts/inspect-type.sh MyNamespace.IMyApi MyPackage 2.0.0 # 3. Full API

# === Quick one-liner examples ===
./scripts/list-types.sh Refit 8.0.0
./scripts/inspect-type.sh Refit.IRequestBuilder Refit 8.0.0
./scripts/find-dll.sh Newtonsoft.Json 13.0.3 net6.0
```

```powershell
# === Full inspection workflow (PowerShell) ===
.\scripts\detect-tool.ps1
.\scripts\list-types.ps1 -PackageName MyPackage -Version 2.0.0
.\scripts\inspect-type.ps1 -TypeName MyNamespace.IMyApi -PackageName MyPackage -Version 2.0.0
```

## Notes

- **`dotnet-inspect`** works by package name directly — no DLL path resolution needed
- **`ilspycmd`** requires the DLL path; the scripts resolve it automatically from the NuGet cache (`~/.nuget/packages/`)
- If a package isn't in the local cache, run `dotnet restore` in a project that references it first
- The `list-types` output includes the type kind (Class, Interface, Struct, Enum) for easy filtering
- The `inspect-type` output is decompiled C# source — includes attributes, method signatures, properties, and inheritance
