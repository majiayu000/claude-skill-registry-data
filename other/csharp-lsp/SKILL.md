---
name: csharp-lsp
description: >-
  Set up and verify C# language intelligence in Cursor (extensions, .NET SDK)
  or Claude Code (csharp-ls LSP plugin). Use when editing .cs files, setting up
  C# projects, diagnosing missing completions/diagnostics, or asking about csharp-lsp.
---

# C# LSP (csharp-lsp)

C# language server integration for code intelligence on `.cs` files.

**Source:** [anthropics/claude-plugins-official — csharp-lsp](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/csharp-lsp) (adapted for Cursor).

## Important: Cursor vs Claude Code

| Environment | How C# intelligence works |
|-------------|---------------------------|
| **Cursor IDE** | VS Code–compatible **extensions** (C# / C# Dev Kit); not the Claude LSP plugin protocol |
| **Claude Code** | Official `csharp-lsp` plugin + `csharp-ls` binary on PATH + LSP enabled |

In **Cursor**, this skill guides extension + SDK setup. It does **not** spawn `csharp-ls` for the Agent unless you separately configure MCP or terminal workflows.

## Supported extensions

`.cs` (and with C# Dev Kit: `.csx`, `.cshtml` in some setups)

## Requirements

- [.NET SDK 6.0+](https://dotnet.microsoft.com/download) (SDK 8+ recommended for current Roslyn tooling)

## Cursor setup (recommended)

### 1. Install .NET SDK

**Windows (PowerShell):**

```powershell
dotnet --version
```

If missing, install from https://dotnet.microsoft.com/download or `winget install Microsoft.DotNet.SDK.8`.

### 2. Install a Cursor / VS Code extension

Pick one:

| Extension | ID | Notes |
|-----------|-----|--------|
| C# | `ms-dotnettools.csharp` | OmniSharp; lighter |
| C# Dev Kit | `ms-dotnettools.csdevkit` | Roslyn; fuller solution support |

Install via Cursor Extensions UI, or:

```powershell
cursor --install-extension ms-dotnettools.csdevkit
# or: ms-dotnettools.csharp
```

### 3. Open the correct workspace root

- Open the folder containing `.sln` or `.csproj`, not a parent repo with only vendored `.cs` files.
- For multi-project solutions, use the solution root.

### 4. Verify in the editor

- Open a `.cs` file → completions, go-to-definition, diagnostics should appear after project load.
- Check **Output** panel → **C#** or **OmniSharp** / **Roslyn** for errors.

### 5. Optional project settings (`.vscode/settings.json`)

```json
{
  "dotnet.defaultSolution": "YourSolution.sln",
  "omnisharp.useModernNet": true
}
```

## Claude Code setup (if also using Claude Code CLI)

### 1. Install language server

```powershell
dotnet tool install --global csharp-ls
```

Ensure `%USERPROFILE%\.dotnet\tools` is on PATH.

**macOS alternative:** `brew install csharp-ls`

### 2. Enable LSP and install plugin

- Set `ENABLE_LSP_TOOL=1` (shell or `~/.claude/settings.json`)
- Install marketplace plugin `csharp-lsp` via `/plugin` in Claude Code

See [csharp-ls on GitHub](https://github.com/razzmatazz/csharp-language-server).

**Note:** Community reports packaging/protocol issues with the official plugin; alternative: [burhancetinkaya/csharp-roslyn-lsp](https://github.com/burhancetinkaya/csharp-roslyn-lsp) with `roslyn-language-server`.

## Troubleshooting

| Symptom | Cursor fix |
|---------|------------|
| No IntelliSense | Open `.sln`/`.csproj` root; reload window; check SDK `dotnet --version` |
| Wrong project loaded | Set `dotnet.defaultSolution` |
| Only stray `.cs` in a C++ repo | C# LSP not needed; focus on clangd/CMake for C++ |
| Agent lacks symbol info | Agent uses codebase index + file reads; use editor LSP for precise symbols |

| Symptom | Claude Code fix |
|---------|-----------------|
| Plugin installed, no LSP | Verify `csharp-ls` on PATH; enable LSP; restart; open solution root |
| Hangs on init | Try `roslyn-language-server`; see community plugins |

## When helping the user

1. Detect environment: Cursor-only vs Claude Code vs both.
2. Run readonly checks: `dotnet --version`, presence of `.sln`/`.csproj`, extension recommendation.
3. Do **not** install global tools or extensions without user approval.
4. For mixed repos (e.g. C++ engine + vendored `.cs`), state that C# LSP applies only to real C# projects.
