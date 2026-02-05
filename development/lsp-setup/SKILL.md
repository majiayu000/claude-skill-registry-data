---
name: lsp-setup
description: Detects, installs, and configures LSP language servers for code intelligence. Use when setting up LSP, needing go-to-definition, find references, hover docs, symbols, diagnostics, or code navigation. Handles language server installation and troubleshooting.
allowed-tools: Bash(*), Read, Write, Edit, Glob, Grep, LSP
---

# LSP Agent Skill

You are an LSP (Language Server Protocol) configuration specialist. Your role is to ensure
optimal code intelligence for all languages in the project.

## Autonomy Level: Full

- Detect languages automatically
- Install LSP servers without asking
- Configure servers for optimal performance
- Use LSP for code navigation
- Notify after setup complete

---

## Installation Priority

**IMPORTANT**: Always prefer official Anthropic plugins over system installations.

### Priority Order:

1. **Anthropic Claude Code Plugins** (preferred)
   - Pre-configured for Claude Code integration
   - Install via: `/plugin install <name>@claude-plugins-official`

2. **System Package Managers** (fallback if no plugin)
   - npm, pip, brew, cargo, etc.
   - Only install binary if plugin requires it

### Available Anthropic Plugins:

| Language | Plugin Command |
|----------|---------------|
| TypeScript/JS | `/plugin install typescript-lsp@claude-plugins-official` |
| Python | `/plugin install pyright-lsp@claude-plugins-official` |
| Go | `/plugin install gopls-lsp@claude-plugins-official` |
| Rust | `/plugin install rust-analyzer-lsp@claude-plugins-official` |
| C/C++ | `/plugin install clangd-lsp@claude-plugins-official` |
| C# | `/plugin install csharp-lsp@claude-plugins-official` |
| Java | `/plugin install jdtls-lsp@claude-plugins-official` |
| PHP | `/plugin install php-lsp@claude-plugins-official` |
| Lua | `/plugin install lua-lsp@claude-plugins-official` |
| Swift | `/plugin install swift-lsp@claude-plugins-official` |
| Ruby | `/plugin install ruby-lsp@claude-plugins-official` |
| Kotlin | `/plugin install kotlin-lsp@claude-plugins-official` |

**Note**: Plugins require the binary to be installed on the system. Install the plugin first,
then install the binary if needed (the plugin will show an error if binary is missing).

---

## LSP Operations Available

Claude Code provides these LSP operations:

| Operation | Description |
|-----------|-------------|
| `goToDefinition` | Jump to where a symbol is defined |
| `findReferences` | Find all usages of a symbol |
| `hover` | Get documentation/type info for a symbol |
| `documentSymbol` | List all symbols in a file |
| `workspaceSymbol` | Search symbols across the workspace |
| `goToImplementation` | Find implementations of interface/abstract |
| `prepareCallHierarchy` | Get call hierarchy item at position |
| `incomingCalls` | Find functions that call this function |
| `outgoingCalls` | Find functions called by this function |

---

## Language Server Mappings

### JavaScript/TypeScript
```bash
# Server: typescript-language-server
npm install -g typescript-language-server typescript

# Alternatives:
# - vtsls (faster)
# - biome (linting + formatting + LSP)
```

### Python
```bash
# Server: pyright (recommended)
npm install -g pyright

# Alternatives:
# - pylsp (python-lsp-server)
# - jedi-language-server
pip install python-lsp-server
```

### Go
```bash
# Server: gopls (official)
go install golang.org/x/tools/gopls@latest
```

### Rust
```bash
# Server: rust-analyzer (official)
rustup component add rust-analyzer
# Or via brew:
brew install rust-analyzer
```

### Ruby
```bash
# Server: solargraph
gem install solargraph
```

### PHP
```bash
# Server: intelephense (recommended)
npm install -g intelephense

# Alternative: phpactor
```

### Java
```bash
# Server: jdtls (Eclipse JDT Language Server)
# Usually installed via IDE or:
brew install jdtls
```

### C/C++
```bash
# Server: clangd (recommended)
brew install llvm
# Or:
apt install clangd

# Alternative: ccls
```

### C#
```bash
# Server: omnisharp
brew install omnisharp/omnisharp-roslyn/omnisharp-mono
# Or via dotnet:
dotnet tool install -g omnisharp
```

### Lua
```bash
# Server: lua-language-server
brew install lua-language-server
```

### Bash/Shell
```bash
# Server: bash-language-server
npm install -g bash-language-server
```

### YAML
```bash
# Server: yaml-language-server
npm install -g yaml-language-server
```

### JSON
```bash
# Server: vscode-json-languageserver
npm install -g vscode-json-languageserver
```

### HTML/CSS
```bash
# Server: vscode-langservers-extracted
npm install -g vscode-langservers-extracted
```

### Markdown
```bash
# Server: marksman
brew install marksman
```

### SQL
```bash
# Server: sql-language-server
npm install -g sql-language-server
```

### Dockerfile
```bash
# Server: dockerfile-language-server
npm install -g dockerfile-language-server-nodejs
```

### Terraform
```bash
# Server: terraform-ls
brew install terraform-ls
```

### Zig
```bash
# Server: zls
brew install zls
```

### Svelte
```bash
# Server: svelte-language-server
npm install -g svelte-language-server
```

### Vue
```bash
# Server: vue-language-server (Volar)
npm install -g @vue/language-server
```

### GraphQL
```bash
# Server: graphql-lsp
npm install -g graphql-language-service-cli
```

---

## Auto-Detection Process

### Step 1: Detect Languages

Run tech detection or analyze file extensions:

```bash
# Get unique file extensions
find . -type f -name "*.*" \
  ! -path "./node_modules/*" \
  ! -path "./.git/*" \
  ! -path "./vendor/*" \
  ! -path "./venv/*" \
  | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -20
```

### Step 2: Map to LSP Servers

Use `assets/lsp-mappings.json` to determine required servers.

### Step 3: Check Installed Servers

```bash
# Check each required server
which typescript-language-server
which pyright
which gopls
# etc.
```

### Step 4: Install Missing Servers

For each missing server:
1. Determine installation method (npm, pip, brew, etc.)
2. Run installation command
3. Verify installation
4. Log result

### Step 5: Configure Project

Create/update `.claude/lsp-config.json`:

```json
{
  "servers": {
    "typescript": {
      "command": "typescript-language-server",
      "args": ["--stdio"],
      "installed": true,
      "version": "4.3.0"
    },
    "python": {
      "command": "pyright",
      "args": ["--stdio"],
      "installed": true,
      "version": "1.1.350"
    }
  },
  "last_check": "2026-01-03T15:00:00Z"
}
```

---

## Using LSP for Navigation

When working on code, proactively use LSP:

### Go to Definition
```
When user asks "where is X defined" or needs to understand a symbol:
1. Use LSP goToDefinition
2. Navigate to the definition
3. Explain what you found
```

### Find References
```
When user asks "where is X used" or needs to understand impact:
1. Use LSP findReferences
2. List all usages
3. Group by file/context
```

### Hover Information
```
When user asks "what is X" or needs type information:
1. Use LSP hover
2. Show documentation and type info
```

### Document Symbols
```
When user asks "what's in this file" or needs overview:
1. Use LSP documentSymbol
2. List all functions, classes, variables
```

### Call Hierarchy
```
When user asks "what calls X" or "what does X call":
1. Use prepareCallHierarchy
2. Use incomingCalls or outgoingCalls
3. Show the call tree
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/lsp` | Auto-detect and install LSP servers |
| `/lsp:status` | Show installed/available LSP servers |
| `/lsp:install <server>` | Manually install a specific server |
| `/lsp:test` | Test LSP functionality |

---

## Integration with Tech Detection

When `/claudenv` or tech-detection runs:

1. Receive detected languages from `project-context.json`
2. Look up required LSP servers
3. Check installation status
4. Install missing servers (with notification)
5. Update `lsp-config.json`
6. Report status

---

## Proactive LSP Usage

**Always use LSP when:**
- Navigating to symbol definitions
- Finding where something is used
- Understanding function signatures
- Exploring code structure
- Debugging type issues
- Refactoring code

**Don't rely on grep when LSP is available** - LSP understands code semantically.

---

## Delegation

Hand off to other skills when:

| Condition | Delegate To |
|-----------|-------------|
| New language detected | `tech-detection` for full analysis |
| Unfamiliar language needs skill | `meta-agent` to create specialist |
| UI/styling work | `frontend-design` |
| Iterative development needed | `loop-agent` |

---

## Troubleshooting

### LSP Not Working

1. Check if server is installed:
   ```bash
   which <server-command>
   ```

2. Check server can run:
   ```bash
   <server-command> --version
   ```

3. Enable LSP logging:
   ```bash
   claude --enable-lsp-logging
   ```

4. Check logs at `~/.claude/debug/`

### Common Issues

| Issue | Solution |
|-------|----------|
| "Server not found" | Run `/lsp:install <server>` |
| "Connection refused" | Server may need restart |
| "No response" | Check file is saved, server supports language |
| "Wrong definitions" | Clear LSP cache, restart server |
