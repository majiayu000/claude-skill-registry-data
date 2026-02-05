---
name: roslyn-source-generators
description: Create and maintain Roslyn source generators for compile-time code generation. Use when building incremental generators, designing pipelines with ForAttributeWithMetadataName, creating marker attributes, implementing equatable models, testing generators, or debugging generator performance issues.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(dotnet:*), WebFetch
---

# Roslyn Source Generators Skill

## Overview

Source generators enable **compile-time metaprogramming** in C# - code that generates additional C# source files during compilation. Generated code becomes part of the compilation and is available for use like any other code.

### Key Capabilities

- Generate C# source at compile time
- Introspect user code via Roslyn syntax/semantic models
- Access additional files (XML, JSON, etc.)
- Report diagnostics when generation fails
- **Additive only** - cannot modify existing user code

## CRITICAL: Old vs New API

| Aspect | ISourceGenerator (DEPRECATED) | IIncrementalGenerator (CURRENT) |
|--------|-------------------------------|----------------------------------|
| Status | **Deprecated** | **Recommended** |
| Performance | Poor - runs on every keystroke | Excellent - caches pipeline stages |
| Interface | `Initialize()` + `Execute()` | Single `Initialize()` with pipeline |
| Filtering | `ISyntaxReceiver` | `ForAttributeWithMetadataName()` |
| Memory | Creates new receiver each cycle | Memoized/cached transforms |

**Always use `IIncrementalGenerator`** - the old API causes IDE hangs and performance degradation.

## Quick Start

### 1. Create Generator Project

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>netstandard2.0</TargetFramework>
    <IncludeBuildOutput>false</IncludeBuildOutput>
    <Nullable>enable</Nullable>
    <LangVersion>Latest</LangVersion>
    <EnforceExtendedAnalyzerRules>true</EnforceExtendedAnalyzerRules>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.CodeAnalysis.CSharp" Version="4.3.0" PrivateAssets="all" />
    <PackageReference Include="Microsoft.CodeAnalysis.Analyzers" Version="3.3.4" PrivateAssets="all" />
  </ItemGroup>

  <ItemGroup>
    <None Include="$(OutputPath)\$(AssemblyName).dll" Pack="true"
          PackagePath="analyzers/dotnet/cs" Visible="false" />
  </ItemGroup>
</Project>
```

### 2. Implement the Generator

See [Incremental Generator Guide](incremental-generator-guide.md#complete-iincrementalgenerator-example) for the full implementation pattern with `ForAttributeWithMetadataName`.

### 3. Usage

```csharp
using MyGenerators;

[Generate]
public partial class MyClass
{
    // GeneratedMethod() available at compile time
}
```

See [Project Setup](project-setup.md#consuming-project-configuration) for project reference configuration.

## Pipeline Operators

| Operator | Purpose | Example |
|----------|---------|---------|
| `Select` | Transform each item | `.Select((item, ct) => Process(item))` |
| `Where` | Filter items | `.Where(item => item.IsValid)` |
| `Collect` | Batch into collection | `.Collect()` for `ImmutableArray<T>` |
| `Combine` | Merge two pipelines | `pipeline1.Combine(pipeline2)` |

## Model Design for Caching

**Critical rules:** Use records for value equality, never store `ISymbol` or `SyntaxNode`, extract primitives early, wrap arrays in `EquatableArray<T>`.

See [Incremental Generator Guide](incremental-generator-guide.md#caching-and-incrementality) for complete caching patterns and `EquatableArray<T>` implementation.

## Additional Resources

For detailed guidance, see:
- [Project Setup](project-setup.md) - Full .csproj configuration, consuming projects, NuGet packaging
- [Incremental Generator Guide](incremental-generator-guide.md) - Deep dive into API, ForAttributeWithMetadataName, caching
- [Patterns and Examples](patterns-and-examples.md) - Common implementation patterns
- [Testing](testing.md) - Unit and snapshot testing strategies
- [Troubleshooting](troubleshooting.md) - Common issues and solutions

## What Generators Cannot Do

Source generators are explicitly **additive only**:

- Cannot modify existing user code
- Cannot rewrite syntax trees
- Cannot perform IL weaving
- Cannot replace language features
- Cannot communicate between generators
- Cannot access other generators' output

For code rewriting, use Roslyn Analyzers with Code Fixes or IL weaving tools like Fody.
