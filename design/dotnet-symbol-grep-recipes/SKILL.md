---
name: dotnet-symbol-grep-recipes
description: Quick ripgrep recipes for common C# navigation tasks in this repo.
---

# dotnet-symbol-grep-recipes

Short, practical ripgrep commands for navigating the codebase.

## Find Type/Interface/Record Definition
```bash
rg -n "\b(class|interface|record|struct)\s+<Name>\b" -g "*.cs"
```

## Find Implementations of Interface
```bash
rg -n "\bclass\s+\w+\s*:\s*[^\n]*\b<Interface>\b" -g "*.cs"
```

## Find DI Registrations
```bash
rg -n "\b(AddSingleton|AddScoped|AddTransient)\b.*\b<Interface>\b" -g "*.cs"
```

## Find Handlers/Controllers/Endpoints
```bash
rg -n "\bclass\s+\w+(Handler|Controller)\b" -g "*.cs"
rg -n "\bMap(Get|Post|Put|Delete|Patch)\b" -g "*.cs"
```

## Find Tests Related to a Class
```bash
rg -n "\b<ClassName>(Tests|Test)\b" -g "*Tests*.cs"
rg -n "\b<ClassName>\b" -g "*Tests*.cs"
```

## MSTest Test Discovery
```bash
rg -n "\[TestClass\]|\[TestMethod\]|\[DataTestMethod\]|\[DataRow\]" -g "*.cs"
```

## Find Razor Pages
```bash
rg -n "\bclass\s+\w+Model\s*:\s*PageModel\b" -g "*.cs"
rg --files -g "*.cshtml"
```

## Find Module Marker Interfaces
```bash
rg -n "\bclass\s+\w+\s*:\s*[^\n]*\b(I|IFullStack|IBackground|IEngine|IApi)Module\b" -g "*.cs"
rg -n "\bIModuleDefinition\b|\bIIncursaNavModuleMetadata\b" -g "*.cs"
```

## Find Custom Generated File Definitions
```bash
rg --files -g "*.dto.json" -g "*.enum.json" -g "*.fastid.json"
```
