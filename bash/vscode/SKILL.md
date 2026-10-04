---
name: vscode
description: "Configure VS Code tasks, debugging, settings, and extensions, and automate editor workflows with the code CLI."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["vscode", "extensions-api", "tasks", "launchjson", "settings", "cli", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Visual Studio Code Editor Automation AI Skill Guide (Claude)

## Overview & Engine Architecture
Visual Studio Code is an Electron-based editor with a **workspace model**, **extension host**, and JSON-driven **tasks / launch / settings**. Automation spans the **`code` CLI**, workspace files (`.vscode/`), and the **Extension API** (`vscode` module). Claude operates as a Principal Developer Experience Engineer, specializing in **task runners**, **debug configurations**, **workspace settings hygiene**, and **extension commands**.

### VS Code Workspace & Extension Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 VS Code Architecture                        │
│                                                             │
│  Workbench & Editor                                         │
│  ├── Windows / Editors / Terminals                          │
│  ├── Settings (user / workspace / folder)                   │
│  └── Keybindings / Snippets                                 │
│                                                             │
│  Automation                                                 │
│  ├── tasks.json / launch.json / extensions.json             │
│  ├── code CLI (open, diff, install extension)               │
│  └── Extension Host (vscode.* API)                          │
│                                                             │
│  Language Services                                          │
│  ├── LSP servers via extensions                             │
│  ├── Debug adapters                                         │
│  └── Task problem matchers                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Workspace over User Settings**: Prefer `.vscode/settings.json` for project-specific rules.
2. **Tasks for Repeatable Commands**: Encode build/test/lint in `tasks.json` with problem matchers.
3. **Launch Configs**: Keep `launch.json` aligned with actual package scripts and ports.
4. **Extension Recommendations**: Use `extensions.json` recommendations, not forced silent installs.
5. **CLI Automation**: Use `code` for open/diff/install in scripts; respect Remote/WSL contexts.

---

## Production Config + Extension Sample

`.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "test",
      "type": "npm",
      "script": "test",
      "group": { "kind": "test", "isDefault": true },
      "problemMatcher": ["$tsc"]
    },
    {
      "label": "lint",
      "type": "shell",
      "command": "npm run lint",
      "group": "build",
      "presentation": { "reveal": "silent", "panel": "shared" }
    }
  ]
}
```

Minimal extension command (`extension.ts`):

```typescript
// ==============================================================================
// VS Code Extension API: register a command that inserts a dated stub
// ==============================================================================
import * as vscode from "vscode";

export function activate(context: vscode.ExtensionContext) {
  const disposable = vscode.commands.registerCommand(
    "howto.insertDatedStub",
    async () => {
      const editor = vscode.window.activeTextEditor;
      if (!editor) {
        vscode.window.showWarningMessage("No active editor");
        return;
      }
      const stamp = new Date().toISOString().slice(0, 10);
      await editor.edit((b) =>
        b.insert(editor.selection.active, `// TODO(${stamp}): \n`)
      );
    }
  );
  context.subscriptions.push(disposable);
}

export function deactivate() {}
```

CLI:

```bash
code .
code --diff a.ts b.ts
code --install-extension esbenp.prettier-vscode
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Task not found** | Wrong label / folder not workspace root. | Open folder root; verify `.vscode/tasks.json`. |
| **Launch attaches wrong port** | Stale `launch.json`. | Sync with app listen port / `serverReadyAction`. |
| **Extension command missing** | Not contributed in `package.json`. | Add `contributes.commands` + activationEvents. |
| **Settings ignored** | Multi-root / language-specific override. | Check folder scope and `[language]` blocks. |

---

## Best Practices

1. Commit `.vscode/tasks.json`, `launch.json`, `extensions.json`; avoid personal keybindings in repo.
2. Use `inputs` in tasks/launch for parameterization.
3. Prefer workspace Trust awareness when recommending tasks that run shell.

### Essential Paths
- **Workspace**: `.vscode/`
- **User settings**: OS-specific User `settings.json`
- **CLI**: `code` on PATH (Shell Command: Install in PATH)

---

## Agent Operational Directive
> **MANDATORY**: Prefer workspace `.vscode` configs for project automation. Register extension commands in both code and `package.json` contributes. Never commit machine-local absolute paths in launch configs when relative alternatives exist.
