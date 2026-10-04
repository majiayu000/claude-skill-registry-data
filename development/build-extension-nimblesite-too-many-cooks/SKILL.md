---
name: build-extension
description: Build, test, and package the Too Many Cooks VSCode extension
argument-hint: "[build|test|package|install]"
disable-model-invocation: true
allowed-tools: Bash
---

# Build VSCode Extension

Builds the Too Many Cooks VSCode extension (`too_many_cooks_vscode_extension/`).

## Full build (MCP server + extension + .vsix)

```bash
bash too_many_cooks_vscode_extension/build.sh
```

This does:
1. Builds MCP server: `npm run build`
2. Compiles extension: `npm run compile`
3. Packages: `vsce package` → `.vsix` file

## Build MCP server only

```bash
cd too-many-cooks && npm ci && npm run build
```

## Test

```bash
cd too_many_cooks_vscode_extension && npm run pretest && npm test
```
On headless Linux: `xvfb-run -a npm test`

## Install into VSCode

```bash
code --install-extension too_many_cooks_vscode_extension/*.vsix
```

## Architecture

TypeScript → `tsc` → VSCode-compatible JS module.
