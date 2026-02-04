---
name: csharp-decompile
description: Decompile .NET assemblies to inspect types, understand implementations, debug third-party libraries, and view IL code. Use when debugging NuGet dependency behavior, understanding compiled code, investigating runtime issues, or exploring unfamiliar assemblies.
---

# C# Decompilation with ilspycmd

Decompile .NET assemblies to C# source code or IL using `ilspycmd`.

## Setup

Ensure ilspycmd is installed:

```bash
ilspycmd --version || dotnet tool install --global ilspycmd
```

## Workflows

### List Types in an Assembly

Discover what's in an assembly before decompiling:

```bash
# List all types: classes, interfaces, structs, delegates, enums
ilspycmd -l cisde /path/to/assembly.dll
```

### Decompile to a Project

Generate a compilable C# project from an assembly:

```bash
ilspycmd --nested-directories -p -o /tmp/decompiled /path/to/assembly.dll
```

This creates a `.csproj` and source files organized by namespace.

*Important*: this lets Claude code bring its sophisticated code reading and exploration tools to bear.


### Decompile a Specific Type

Target a single type by its fully qualified name:

```bash
ilspycmd -t MyNamespace.MyClass /path/to/assembly.dll
```

The output goes to stdout. Use this to quickly inspect a type's implementation.

### View IL Code

For low-level analysis, view the intermediate language:

```bash
ilspycmd -il -t MyNamespace.MyClass /path/to/assembly.dll

# With sequence points (source line mappings)
ilspycmd --il-sequence-points -t MyNamespace.MyClass /path/to/assembly.dll
```

### Debug NuGet Dependencies

NuGet packages are at `~/.nuget/packages/<package-name>/<version>/lib/<tfm>/`. To inspect:

```bash
# Find the DLL
find ~/.nuget/packages/sixlabors.imagesharp -name "*.dll" | grep -v ref

# List types
ilspycmd -l cisde ~/.nuget/packages/sixlabors.imagesharp/3.1.11/lib/net6.0/SixLabors.ImageSharp.dll

# Decompile a specific type
ilspycmd -t "SixLabors.ImageSharp.Numerics" ~/.nuget/packages/sixlabors.imagesharp/3.1.11/lib/net6.0/SixLabors.ImageSharp.dll
```

### Generate Type Diagrams

Create an interactive HTML visualization of type relationships:

```bash
ilspycmd --generate-diagrammer -o /tmp/diagrammer /path/to/assembly.dll

# With filtering
ilspycmd --generate-diagrammer -o /tmp/diagrammer \
  --generate-diagrammer-include "MyNamespace\\..*" \
  --generate-diagrammer-exclude "MyNamespace\\.Internal\\..*" \
  /path/to/assembly.dll
```

These are mostly useful for the user. Let the user know that they're available.

## Tips

- Add `-r /path/to/deps` when the assembly has dependencies that aren't automatically resolved
- Use `--no-dead-code` and `--no-dead-stores` for cleaner output
- For tight loops or scripts, add `--disable-updatecheck`
- The `-lv Latest` flag is default; use `-lv CSharp9_0` etc for older language features

## Fixes

