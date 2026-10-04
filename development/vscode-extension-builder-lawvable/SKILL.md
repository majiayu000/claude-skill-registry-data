---
name: vscode-extension-builder-lawvable
description: Use when building, converting, testing, debugging, packaging, publishing, or reviewing VS Code extensions, including commands, webviews, custom editors, tree views, language features, AI/Language Model API integrations, Language Model Tools, extension host behavior, and .vsix distribution.
metadata:
  last_updated: "2026-06-01"
  author: Antoine Louis (Lawvable), expanded for Joe Black
  license: AGPL-3.0
---

# VS Code Extension Builder

Build production-quality VS Code extensions with a tight feedback loop. Do not stop at "it builds"; prove the extension behavior in the most relevant runtime surface.

## Core Behavior

When the user asks for VS Code extension work, the agent should choose the smallest fitting extension architecture, load only the relevant references, implement with TypeScript-first defaults, and verify behavior through a compile/Extension Host/test/UI loop even if the change looks obvious or time is short.

## First Decisions

1. Identify the extension surface:
   - Command-only action
   - Sidebar/tree view
   - Webview panel or webview view
   - Custom editor
   - Language feature or language server
   - Debug/task/notebook/test integration
   - AI integration with VS Code Language Model API or Language Model Tools
   - Conversion of an existing web app into an extension
2. Pick the closest template from `assets/` only if starting or restructuring a project.
3. Read the reference file for that surface. Do not load every reference.
4. Design activation, contribution points, state, disposal, and testability before coding.
5. After edits, run the relevant feedback loop from `references/testing-feedback-loop.md`.

## Architecture Defaults

- Extension host code runs in Node.js through VS Code's extension host.
- Webviews run in a sandboxed browser context and communicate through `postMessage`.
- Prefer TypeScript strict mode, small modules, explicit disposables, and Zod or narrow validators at external boundaries.
- Prefer `pnpm`, `@vscode/test-electron`, Vitest for pure logic, and esbuild or Vite depending on the surface.
- Keep `vscode` external in bundled extension code.
- Use VS Code APIs over raw Node APIs for workspace files when web/remote compatibility matters.
- Treat remote workspaces, web extensions, multi-root workspaces, and workspace trust as first-order constraints when relevant.

## Template Decision Tree

| Need | Template |
| --- | --- |
| Simple command/action | `assets/basic-command/` |
| Custom UI panel with React | `assets/webview-react/` |
| Sidebar file tree | `assets/tree-view/` |
| Custom file editor | `assets/custom-editor/` |
| AI agent file bridge | `assets/file-bridge/` |

## Required Feedback Loop

For any non-trivial extension change, choose and run the strongest applicable loop:

1. **Compile loop**: typecheck, bundle, lint/format if configured.
2. **Extension Host loop**: launch a disposable Extension Development Host, invoke commands/views/editors against a fixture workspace, and inspect Output/Developer Tools/log evidence.
3. **Automated loop**: run `@vscode/test-electron` integration tests plus Vitest for pure logic.
4. **UI/webview loop**: test webview UI in a browser harness or Extension Host, capture screenshot/snapshot evidence, and verify message passing.
5. **Packaging loop**: run `.vsix` package validation before claiming publishability.

Read `references/testing-feedback-loop.md` before implementing or verifying meaningful behavior.

## Reference Router

Load only the files needed for the current task:

| File | When to Read |
| --- | --- |
| `references/testing-feedback-loop.md` | Always read before verifying meaningful extension behavior |
| `references/patterns.md` | Architecture selection, extension lifecycle, state, disposables, remote/web compatibility |
| `references/cookbook.md` | Copyable recipes for commands, settings, tree views, webviews, custom editors, diagnostics, status bars |
| `references/footguns.md` | Common failure modes, caveats, and "looks fine but breaks" traps |
| `references/test-harnesses.md` | `@vscode/test-electron`, fixture workspaces, CLI-driven checks, CI |
| `references/webview-verification.md` | React/Vite webview testability, CSP, message contracts, browser-style checks |
| `references/debugging-extension-host.md` | Output channels, logs, Developer Tools, activation timing, extension bisect-style debugging |
| `references/ai-lm-tools.md` | Language Model API, Language Model Tool API, Copilot/model-provider boundaries |
| `references/security.md` | Workspace trust, secrets, command injection, webview CSP, file/network boundaries |
| `references/build-config.md` | Bundling, TypeScript, package scripts, watch mode |
| `references/contribution-points.md` | `package.json` `contributes`, activation events, menus, views, settings |
| `references/webview-patterns.md` | Existing detailed webview implementation patterns |
| `references/tree-view-patterns.md` | Existing detailed TreeDataProvider patterns |
| `references/custom-editor-patterns.md` | Existing detailed custom editor patterns |
| `references/conversion-guide.md` | Converting JS/React/Vue apps into VS Code extensions |
| `references/ai-integration.md` | File-bridge integration with external AI agents |
| `references/generated/manifest.json` | Current generated official-doc snapshot inventory |

## Generated Official Docs

Official VS Code developer docs are snapshotted into `references/generated/` by `scripts/update.js`.

Use generated docs when API details, activation behavior, publishing rules, or newer AI APIs may have changed. Prefer generated docs over memory for current syntax and caveats.

Refresh docs with:

```bash
node scripts/update.js
```

Each generated Markdown file includes source URL, fetch timestamp, and content hash.

## Verification Before Completion

Before saying work is done:

1. State which feedback loop applies.
2. Run or inspect the command/artifact that proves that loop.
3. Read the result.
4. Report observed evidence, not assumptions.

If a loop cannot run in the current environment, say exactly why and provide the closest runnable substitute.

## Red Flags

Stop and re-check the relevant reference if you think:

- "The TypeScript build passed, so the extension works."
- "The command is registered, so activation must be fine."
- "The webview renders in Vite, so it will render inside VS Code."
- "This only needs a quick package.json contribution edit."
- "The VS Code API is probably the same as last time."
- "The Extension Host is too hard to automate, so no runtime check is needed."
