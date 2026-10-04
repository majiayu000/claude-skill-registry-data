---
name: raycast
description: "Build Raycast extensions with React and TypeScript, create Script Commands, and troubleshoot URL schemes and extension execution on macOS."
category: macos
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["raycast", "macos-launcher", "raycast-api", "react-typescript", "script-commands", "accessibility-window", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Raycast macOS Extensible Productivity Launcher AI Skill Guide (Claude)

## Overview & Engine Architecture
Raycast is a high-speed, extensible macOS launcher engineered in native Swift with a **React/TypeScript Extension Runtime (`@raycast/api`)** running in a secure, embedded Node.js process. Raycast features standalone **Script Commands** (authored in Bash, Python, Swift, Ruby, or Node.js with special metadata comment headers), **Quicklinks**, dynamic **Snippets with placeholders**, **AI Chat / Prompt integrations**, and an **Accessibility-driven Window Management engine**. Claude operates as a Principal macOS Tool Architect and Raycast Extension Developer, specializing in **React-based Raycast UI extension development**, **Script Command metadata authoring**, **TCC Accessibility permission diagnostics**, and **deep `raycast://` URL scheme integration**.

### Raycast Multi-Tier Architecture & Extension Runtime Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Raycast Engine Architecture                 │
│                                                             │
│  Presentation & Native Swift Core                           │
│  ├── Low-Latency Swift HUD Window (Floating Global Launcher)│
│  ├── Spotlight Replacement & Global Hotkey Engine (⌘+Space) │
│  └── Accessibility Window Management (`AXUIElement` Engine) │
│                                                             │
│  Extension & React Runtime (`@raycast/api`)                 │
│  ├── Embedded Node.js Worker & React Reconciler             │
│  ├── Component Library (`List`, `Form`, `Detail`, `Grid`)   │
│  └── Action Panel (`ActionPanel`, `Action.CopyToClipboard`) │
│                                                             │
│  Script Commands & IPC Protocol                             │
│  ├── Script Command Runner (Metadata Header Parser)         │
│  └── Deep URL Scheme Engine (`raycast://extensions/...`)    │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **React / TypeScript Extension Authoring**: Develop modular Raycast extensions using `@raycast/api` and `@raycast/utils` implementing `List`, `Detail`, `Form`, and `ActionPanel` views with clean state management.
2. **Metadata Script Command Authoring**: Write standalone script commands in Bash, Python, or Swift with valid `@raycast.schemaVersion`, `@raycast.title`, `@raycast.mode`, and `@raycast.icon` headers.
3. **Accessibility Window Snapping Triage**: Remediate window management failures by verifying Raycast's `AXUIElement` Accessibility permissions in macOS System Settings.
4. **Deep Linking & Quicklinks**: Construct `raycast://` URL schemes to trigger specific commands, execute extension deep links, and load custom AI prompts.

---

## Production TypeScript Code: Custom Raycast Extension Command (`@raycast/api`)

Save this file as `src/search-repositories.tsx` inside a Raycast Extension project (`npm install @raycast/api @raycast/utils`):

```tsx
// ==============================================================================
// Raycast Extension Command (React / TypeScript): GitHub Repo Switcher
// Fetches, filters, and opens local git repositories in VS Code or Terminal.
// ==============================================================================
import { Action, ActionPanel, Icon, List, showToast, Toast } from "@raycast/api";
import { useExec } from "@raycast/utils";
import { useState } from "react";

interface RepoItem {
  name: string;
  path: string;
}

export default function Command() {
  const [searchText, setSearchText] = useState("");

  // Scan user Projects directory using fast find command
  const { isLoading, data, error } = useExec(
    "find",
    ["/Users/" + process.env.USER + "/Projects", "-maxdepth", "2", "-name", ".git"],
    {
      onError: (err) => {
        showToast({
          style: Toast.Style.Failure,
          title: "Failed to scan projects",
          message: err.message,
        });
      },
    }
  );

  const repos: RepoItem[] = (data || "")
    .split("\n")
    .filter((line) => line.length > 0)
    .map((gitDir) => {
      const repoPath = gitDir.replace(/\/\.git$/, "");
      const repoName = repoPath.split("/").pop() || "Unnamed";
      return { name: repoName, path: repoPath };
    });

  const filteredRepos = repos.filter((r) =>
    r.name.toLowerCase().includes(searchText.toLowerCase())
  );

  return (
    <List
      isLoading={isLoading}
      onSearchTextChange={setSearchText}
      searchBarPlaceholder="Filter local git repositories..."
    >
      {filteredRepos.map((repo) => (
        <List.Item
          key={repo.path}
          icon={Icon.Folder}
          title={repo.name}
          subtitle={repo.path}
          actions={
            <ActionPanel>
              <Action.Open
                title="Open in VS Code"
                target={repo.path}
                application="Visual Studio Code"
              />
              <Action.Open
                title="Open in Terminal"
                target={repo.path}
                application="Terminal"
              />
              <Action.CopyToClipboard title="Copy Path" content={repo.path} />
            </ActionPanel>
          }
        />
      ))}
    </List>
  );
}
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Window Management Commands (Snap/Resize) Fail** | Raycast lacks macOS Accessibility permissions to manipulate window bounds via `AXUIElement`. | 1. Open *System Settings $\rightarrow$ Privacy & Security $\rightarrow$ Accessibility*.<br>2. Toggle **Raycast** OFF and ON.<br>3. Restart Raycast. |
| **Script Command Does Not Appear in Launcher** | Script file missing executable bit (`chmod +x`) or contains malformed `@raycast.schemaVersion` header. | 1. In terminal, run: `chmod +x ~/.raycast-scripts/my_script.sh`.<br>2. Verify header format: `// @raycast.schemaVersion 1` and `// @raycast.title My Script`.<br>3. In Raycast Preferences $\rightarrow$ Extensions $\rightarrow$ Reload. |
| **`npm run dev` Fails with Node.js Version Error** | Raycast API requires Node.js version 18.0.0 or higher. | Update Node.js via Homebrew: `brew install node` or `nvm use 20`. |
| **`Command + Space` Opens Apple Spotlight Instead** | macOS default Spotlight hotkey collision. | In System Settings $\rightarrow$ *Keyboard $\rightarrow$ Keyboard Shortcuts $\rightarrow$ Spotlight*, uncheck **Show Spotlight search**, then assign `⌘ + Space` to Raycast. |

---

## Command Line Syntax & Raycast Script Command Header Template

```bash
#!/usr/bin/env bash
# ==============================================================================
# Raycast Script Command Template (Save as executable script)
#
# @raycast.schemaVersion 1
# @raycast.title System Memory Free
# @raycast.mode compact
# @raycast.icon 🚀
# @raycast.packageName Developer Utilities
# ==============================================================================
echo "Free Memory: $(vm_stat | grep 'Pages free' | awk '{print $3 * 4096 / 1024 / 1024}') MB"
```

### Essential File Locations
- **Raycast Application Support**: `~/Library/Application Support/com.raycast.macos`
- **Custom Script Commands**: `~/Library/Application Support/com.raycast.macos/script-commands`
- **Raycast Preferences**: `~/Library/Preferences/com.raycast.macos.plist`

---

## Agent Operational Directive
> **MANDATORY**: When authoring Raycast Script Commands, always specify `@raycast.schemaVersion 1`, assign an appropriate `@raycast.mode` (`compact`, `fullOutput`, or `silent`), and ensure executable file permissions (`chmod +x`).
