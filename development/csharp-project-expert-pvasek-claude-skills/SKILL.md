---
name: csharp-project-expert
description: 'ALWAYS use for ANY C# operation: renaming (files/classes/methods/properties/namespaces), finding references/usages ("where is X used"), finding definitions ("where is X defined"), understanding code structure (hierarchies/dependencies/relationships). Roslyn-powered semantic analysis ensures all references are updated correctly across the entire solution.'
---

# C# Project Expert

Compiler-accurate semantic analysis for C# using Roslyn APIs. **Not text search** - understands C# semantics.

## When to Use

**Use this skill for:**
- Finding symbol definitions (classes, methods, interfaces, properties)
- Finding all references before refactoring
- Safe renaming across entire solution (always preview first!)
- Understanding method signatures and type hierarchies
- Checking compilation errors/warnings
- Finding interface implementations
- Analyzing method call chains (callers/callees)
- Finding unused code

**Don't use for:** Non-C# files, simple text/comment searches, projects without .sln/.csproj

## CLI Path (Cross-Platform)

| Platform | Path |
|----------|------|
| Linux x64 | `./scripts/linux-x64/csharp-skill` |
| macOS x64 | `./scripts/osx-x64/csharp-skill` |
| macOS ARM | `./scripts/osx-arm64/csharp-skill` |
| Windows x64 | `./scripts/win-x64/csharp-skill.exe` |

## Command Syntax

```
<cli-path> [-s <solution.sln> | -p <project.csproj>] [-o json|text|markdown] <command> [options]
```

**Auto-Discovery:** If `-s` or `-p` is not specified, the tool automatically searches the current directory for a `.sln` file (preferred) or `.csproj` file.

## All Commands (18)

| Command | Purpose | Key Options |
|---------|---------|-------------|
| `find-definition <name>` | Where is symbol defined | `--type class|method|property|interface` |
| `find-references <name>` | All usages of symbol | `--type`, `--in-namespace` |
| `rename <old> <new>` | Rename across solution | `--preview` (use first!), `--type`, `--rename-file` |
| `signature <name>` | Method/type signature | `--include-overloads`, `--include-docs` |
| `list-members <type>` | Members of a type | `--kind method|property|field`, `--accessibility` |
| `diagnostics` | Compilation errors/warnings | `--severity error|warning`, `--file`, `--code` |
| `check-symbol-exists <name>` | Verify symbol exists | `--type` |
| `find-implementations <name>` | Interface implementations | - |
| `inheritance-tree <type>` | Type hierarchy | `--direction ancestors|descendants|both` |
| `find-callers <method>` | Who calls this method | - |
| `find-callees <method>` | What does method call | - |
| `dependencies <target>` | Type/file dependencies | - |
| `unused-code` | Find dead code | - |
| `generate-interface <class>` | Extract interface | - |
| `implement-interface <iface>` | Generate stubs | - |
| `list-types` | Types in namespace/file | `--namespace` |
| `namespace-tree` | Namespace hierarchy | - |
| `analyze-file <path>` | Quick file analysis | - |

## Critical Workflows

### Safe Rename (Always Follow)
1. Check usage: `find-references OldName --type method`
2. Preview changes (REQUIRED): `rename OldName NewName --type method --preview`
3. Apply: `rename OldName NewName --type method`
4. **When renaming classes/types**: Add `--rename-file` to also rename the file
5. Verify: `diagnostics --severity error`

### Understand Unknown Code
1. What is it? `find-definition ClassName --type class`
2. What can it do? `list-members ClassName`
3. How does it fit? `inheritance-tree ClassName`
4. What does it need? `dependencies ClassName`

## Output Formats

- `json` (default) - Machine-readable
- `text` - Human-readable terminal
- `markdown` - Documentation format

## Requirements

- [.NET 10.0 runtime](https://dotnet.microsoft.com/download/dotnet/10.0)
- Valid .sln or .csproj file
- Solution must compile

## Exit Codes

- `0` Success | `1` Error | `2` Not found

## Detailed References

- [COMMANDS.md](references/COMMANDS.md) - Full command reference
- [WORKFLOWS.md](references/WORKFLOWS.md) - Step-by-step workflows
- [EXAMPLES.md](references/EXAMPLES.md) - Real-world scenarios
