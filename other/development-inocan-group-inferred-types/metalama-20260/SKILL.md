---
name: metalama-2026.0
description: Complete Metalama documentation for aspect-oriented programming in C#. Use when writing aspects, templates, fabrics, or meta-programming code with Metalama.
---

# Metalama Documentation Skill

This skill contains the complete Metalama documentation including conceptual guides, API reference, and sample code.

This skill pertains to Metalama 2026.0.

## Directory Structure

| Directory | Contents |
|-----------|----------|
| `content/conceptual/` | Conceptual documentation (aspects, templates, fabrics, validation, etc.) |
| `content/patterns/` | Pattern libraries (contracts, caching, observability, memoization, DI) |
| `content/api/` | API documentation overview pages |
| `code/` | Sample code (`.cs` = source, `.t.cs` = transformed output, `.Aspect.cs` = aspect implementation) |
| `api/` | API reference YML files from DocFx |

## Finding Information

1. **Search the index**: Use grep with `-B3` to search [index.yml](index.yml) for keywords (each entry has: name, path, summary, keywords - so `-B3` captures the path):
   ```bash
   grep -i -B3 "caching" index.yml
   grep -i -B3 "BuildAspect" index.yml
   ```
2. **Browse by topic**: Navigate the `content/` directory structure.
3. **API lookup**: Use grep on `api/.manifest` to find API YML files by type or member name:
   ```bash
   grep -i "OverrideMethodAspect" api/.manifest
   ```

## Key Entry Points

| Topic | File | Description |
|-------|------|-------------|
| Getting Started | `content/conceptual/using/using-metalama.md` | How to use Metalama in your projects |
| Creating Aspects | `content/conceptual/aspects/aspects.md` | Overview of aspect creation |
| Overriding Methods | `content/conceptual/aspects/simple-aspects/overriding-methods.md` | Basic method interception |
| Templates | `content/conceptual/aspects/templates/templates.md` | T# template syntax and patterns |
| Fabrics | `content/conceptual/using/fabrics/fabrics.md` | Bulk aspect application |
| Contracts | `content/patterns/contracts/contract-patterns.md` | Parameter/property validation |
| Caching | `content/patterns/caching/caching.md` | Method result caching |
| Observability | `content/patterns/observability/observability.md` | INotifyPropertyChanged implementation |
| Debugging Aspects | `content/conceptual/aspects/testing/debugging-aspects.md` | Debug compile-time code, breakpoints, `meta.DebugBreak()` |
| Debugging User Code | `content/conceptual/using/debugging-aspect-oriented-code.md` | Debug run-time transformed code, LamaDebug configuration |

## Common Patterns

### Base Classes

| Base Class | Target | Key Override | Use When |
|------------|--------|--------------|----------|
| `OverrideMethodAspect` | Methods | `OverrideMethod()` | Wrap/intercept methods |
| `OverrideFieldOrPropertyAspect` | Fields/Properties | `OverrideProperty` | Wrap property access |
| `ContractAspect` | Parameters/Fields/Properties | `Validate(dynamic? value)` | Validate values |
| `TypeAspect` | Types | `BuildAspect()` | Introduce members, implement interfaces |
| `MethodAspect` | Methods | `BuildAspect()` | Programmatic method transformation |
| `TypeFabric` | Single type | `AmendType()` | Bulk changes to one type |
| `ProjectFabric` | Project | `AmendProject()` | Apply aspects across project |

### Template Fundamentals

> [!IMPORTANT]
> T# templates look like C# but have different semantics. Code that works in normal C# may not work identically in a template. Always read the full template documentation at `content/conceptual/aspects/templates/` before writing template code.

```csharp
public override dynamic? OverrideMethod()
{
    // Pre-logic
    try
    {
        return meta.Proceed();  // Calls original method
    }
    finally
    {
        // Post-logic (always runs)
    }
}
```

- `dynamic?` handles any return type (void returns null)
- `meta.Proceed()` auto-transforms to `await` for async targets
- Use `meta.Target.*` to access compile-time information about the target declaration
- To debug templates, use `meta.DebugBreak()` (not `Debugger.Break()`)

### Debugging Quick Reference

**Debugging compile-time code (aspects, fabrics, templates):**
1. Add `Debugger.Break()` in `BuildAspect`/fabrics, or `meta.DebugBreak()` in templates
2. Build with: `dotnet build -p:MetalamaDebugCompiler=True -p:MetalamaConcurrentBuildEnabled=False`
3. Attach debugger when prompted, then set breakpoints in transformed code (`obj/.../metalama/`)

**Debugging run-time code (transformed output):**
1. Create a `LamaDebug` build configuration in Visual Studio
1. Use `F11` to step into code, or add `Debugger.Break()`
1. Set breakpoints in transformed files under `obj/<Config>/<TFM>/metalama/`

### Common Pitfalls

| Mistake | Correct Approach |
|---------|------------------|
| Using `Debugger.Break()` in templates | Use `meta.DebugBreak()` in templates; `Debugger.Break()` only works in `BuildAspect` and fabrics |
| Setting breakpoints in source files | Breakpoints don't work in Metalama-transformed projects; use `Debugger.Break()`/`meta.DebugBreak()` then set breakpoints in transformed code |
| Using `nameof()` for introduced members | Use string literals; `nameof()` resolves at aspect compile-time, not target compile-time |
| Filtering all types by namespace in fabrics | Use `GlobalNamespace.GetDescendant("Ns")` or a `NamespaceFabric` instead of `SelectTypes().Where(t => t.Namespace...)` |
| Forgetting `partial` on target classes | Classes receiving introduced members need the `partial` modifier |

## Sample Code Conventions

- `Name.cs` - Target code receiving the aspect
- `Name.Aspect.cs` - Aspect implementation
- `Name.t.cs` - Transformed output (what the compiler generates)
- `Name.Dependency.cs` - Referenced project code for multi-project examples

## Metalama Markdown Directives

The documentation uses custom `[!metalama-*]` directives to include code samples. These are processed at build time to generate HTML, but **in the skill files you see the raw directives**.

### Reading Directive References

When you see a directive in a Markdown file, extract the file path and read the referenced file directly.

| Directive | Purpose | Example |
|-----------|---------|---------|
| `[!metalama-file PATH]` | Shows a single source file | `[!metalama-file ~/code/Project/File.cs]` |
| `[!metalama-test PATH]` | Shows test with input/output | `[!metalama-test ~/code/Project/Test.cs]` |
| `[!metalama-compare PATH]` | Shows side-by-side diff | `[!metalama-compare ~/code/Project/File.cs]` |
| `[!metalama-vimeo ID]` | Embeds Vimeo video | `[!metalama-vimeo 842168905]` |

### Path Resolution

- `~/` resolves to the SKILLS.md directory
- Example: `~/code/Metalama.Documentation.SampleCode.AspectFramework/GettingStarted/GettingStarted.cs`
  → Read `code/Metalama.Documentation.SampleCode.AspectFramework/GettingStarted/GettingStarted.cs`

### How to Read Referenced Code

When you encounter a directive like `[!metalama-file ~/code/Project/File.cs]`:

1. **Read the main file**: `code/Project/File.cs`
2. **Check for related files** (same name, different suffix):
   - `File.Aspect.cs` - Aspect implementation
   - `File.t.cs` - Transformed output
   - `File.Fabric.cs` - Fabric code

**Markers**: If you see `marker="NAME"`, look for code between `// [<snippet NAME>]` and `// [<endsnippet NAME>]` in the file.

## API Reference

The `api/` directory contains DocFx-generated YML files for all public APIs.

### Finding API Documentation

**Use `api/.manifest`** - a JSON index mapping all UIDs (types, members, overloads) to their YML files.

1. **Search the manifest** for the type or member name:
   ```json
   "Metalama.Framework.Aspects.OverrideMethodAspect": "Metalama.Framework.Aspects.OverrideMethodAspect.yml"
   "Metalama.Framework.Aspects.OverrideMethodAspect.OverrideMethod": "Metalama.Framework.Aspects.OverrideMethodAspect.yml"
   "Metalama.Framework.Code.IMethod": "Metalama.Framework.Code.IMethod.yml"
   ```

2. **Read the corresponding YML file** to get full documentation.

3. **Naming conventions**:
   - Types: `Namespace.TypeName.yml`
   - Generic types: backtick becomes dash, e.g., `IAspectBuilder<T>` → `Metalama.Framework.Aspects.IAspectBuilder-1.yml`
   - All members of a type are in the same YML file as the type

### YML File Structure

Each type's YML file contains **all members** of that type in a single file:

```yaml
items:
- uid: Namespace.TypeName           # Type definition
  commentId: T:Namespace.TypeName
  type: Class|Interface|Enum|...
  summary: Type description
  remarks: Detailed explanation
  syntax:
    content: public class TypeName : BaseClass
  children:                         # List of member UIDs
  - Namespace.TypeName.Method1
  - Namespace.TypeName.Property1

- uid: Namespace.TypeName.Method1   # Member definition
  commentId: M:Namespace.TypeName.Method1
  type: Method|Property|Field|...
  summary: Member description
  syntax:
    content: public void Method1()
  parameters: [...]                 # For methods
  return: { type: ..., description: ... }
```

### Key Namespaces

| Namespace | Purpose |
|-----------|---------|
| `Metalama.Framework.Aspects` | Aspect base classes, attributes, `meta` API |
| `Metalama.Framework.Code` | Code model interfaces (`IMethod`, `IType`, `IParameter`, etc.) |
| `Metalama.Framework.Advising` | Advice APIs for introducing members, implementing interfaces |
| `Metalama.Framework.Eligibility` | Eligibility builders for aspect targeting |
| `Metalama.Framework.Diagnostics` | Reporting warnings and errors |
| `Metalama.Framework.Fabrics` | Fabric base classes |
| `Metalama.Patterns.Contracts` | Contract validation aspects |
| `Metalama.Patterns.Caching` | Caching aspects and configuration |
| `Metalama.Patterns.Observability` | INotifyPropertyChanged implementation |
| `Metalama.Extensions.DependencyInjection` | Dependency injection |
| `Metalama.Extensions.Architecture` | Architecture enforcement/validation |

## Linking to Documentation

When referencing documentation articles, provide links to the live documentation at `https://doc.metalama.net`.

**URL format**: `https://doc.metalama.net/<path>` where `<path>` is derived from the file path under `content/`:
- Remove `content/` prefix
- Remove `.md` suffix
- For index files where the filename matches the parent folder (e.g., `path/leaf/leaf.md`), use just `path/leaf`

**Examples**:
| File Path | URL |
|-----------|-----|
| `content/conceptual/aspects/aspects.md` | `https://doc.metalama.net/conceptual/aspects` |
| `content/conceptual/aspects/templates/templates.md` | `https://doc.metalama.net/conceptual/aspects/templates` |
| `content/patterns/caching/caching.md` | `https://doc.metalama.net/patterns/caching` |
| `content/conceptual/aspects/simple-aspects/overriding-methods.md` | `https://doc.metalama.net/conceptual/aspects/simple-aspects/overriding-methods` |

## External Resources

- Live documentation: https://doc.metalama.net
- Source repository: https://github.com/metalama/Metalama
- Samples repository: https://github.com/metalama/Metalama.Samples
