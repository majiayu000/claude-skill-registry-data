---
name: setup-dev
description: Install development tools (mcp | extension | playwright)
disable-model-invocation: true
allowed-tools: Bash
---

# Setup Development Tools

**Usage**: `/setup <tool>`
- `mcp` — Build the Too Many Cooks MCP server
- `extension` — Build the VSCode extension
- `playwright` — Install Chromium and Playwright for website E2E testing

---

## MCP Server Setup

```bash
cd too-many-cooks && npm ci && npm run build
```

Add to Claude Code:
```bash
claude mcp add --transport http too-many-cooks http://localhost:4040/mcp
```

---

## VSCode Extension Setup

Build the MCP server first (above), then:

```bash
cd too_many_cooks_vscode_extension
npm ci
npm run compile
npx @vscode/vsce package
code --install-extension *.vsix
```

---

## Playwright Setup

```bash
cd website && npm ci
cd website && npx playwright install --with-deps chromium
```

Run website tests:
```bash
cd website && npm test
```
