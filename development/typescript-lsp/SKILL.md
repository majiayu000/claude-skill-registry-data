---
name: typescript-lsp
description: TypeScript Language Server Protocol capabilities for navigating TypeScript/JavaScript code. Resolves imported symbols to their definitions (including node_modules), finds all references to functions/classes/variables, gets type information and signatures, previews rename impacts, and checks TypeScript diagnostics. Use when you need to find where ToolLoopAgent or other imports are defined, locate all usages of a function, see TypeScript types, or get compiler errors.
allowed-tools: Bash, Read
---

# TypeScript LSP Skill

This skill provides full TypeScript Language Server Protocol capabilities for navigating and analyzing TypeScript/JavaScript code.

## When to Use This Skill

Use this skill when you need to:
- **Resolve imported symbols** - Find where `ToolLoopAgent`, `React.Component`, or other imported types are defined (including in node_modules)
- **Find all references** - Locate every place a function, class, or variable is used across the codebase
- **Get type information** - See TypeScript type signatures and documentation
- **Preview renames** - Check what would change when renaming a symbol
- **Check diagnostics** - Get TypeScript errors and warnings for a file

## Commands Available

### `typeDefinition` - Jump to Type Definition
Resolves imported symbols to their actual definitions (works with node_modules).

**Example:**
```bash
node .claude/skills/typescript-lsp/typescript-lsp.js typeDefinition src/lib/ai/agents/transaction-debugger.ts 4 30
```

**When to use:** Finding where `ToolLoopAgent` is defined, navigating to React types, or any imported symbol.

### `definition` - Jump to Definition
Standard go-to-definition (works for local symbols).

**Example:**
```bash
node .claude/skills/typescript-lsp/typescript-lsp.js definition src/lib/transaction.ts 10 15
```

### `references` - Find All References
Locates every usage of a symbol across the entire workspace.

**Example:**
```bash
node .claude/skills/typescript-lsp/typescript-lsp.js references src/lib/ai/agents/transaction-debugger.ts 9 37
```

**When to use:** Finding all places that call a function or use a variable.

### `hover` - Get Type Info
Shows TypeScript type information and JSDoc documentation.

**Example:**
```bash
node .claude/skills/typescript-lsp/typescript-lsp.js hover src/lib/transaction.ts 20 10
```

**When to use:** Understanding what type a variable has or seeing function signatures.

### `rename` - Preview Rename (Dry-Run)
Shows what would change when renaming a symbol.

**Example:**
```bash
node .claude/skills/typescript-lsp/typescript-lsp.js rename src/lib/transaction.ts 15 10 newFunctionName
```

**When to use:** Checking the impact of a rename before doing it.

### `diagnostics` - Get Errors/Warnings
Retrieves TypeScript compiler diagnostics for a file.

**Example:**
```bash
node .claude/skills/typescript-lsp/typescript-lsp.js diagnostics src/app/page.tsx
```

**When to use:** Checking for TypeScript errors before compiling.

## Position Parameters

All commands (except `diagnostics`) require line and character positions:
- **Line**: 0-indexed line number (first line is 0)
- **Character**: 0-indexed character offset in the line

**Tip:** When you see `import { ToolLoopAgent } from "ai"` on line 5, use line 4 (0-indexed) and count characters to find where "ToolLoopAgent" starts.

## Output Format

The skill outputs Claude Code-friendly format:
- File paths with line:column (e.g., `src/file.ts:10:5`)
- Code snippets in markdown fences
- Clear headings and formatting

## Limitations

- Requires `typescript-language-server` to be installed
- Works best when run from the project root
- Takes 1-3 seconds per query (single-query mode)
- Requires the file to exist on disk

## Examples for Common Tasks

**Find where ToolLoopAgent is defined:**
```bash
node .claude/skills/typescript-lsp/typescript-lsp.js typeDefinition src/lib/ai/agents/transaction-debugger.ts 4 30
```

**Find all uses of transactionDebugger:**
```bash
node .claude/skills/typescript-lsp/typescript-lsp.js references src/lib/ai/agents/transaction-debugger.ts 9 37
```

**Check if a file has TypeScript errors:**
```bash
node .claude/skills/typescript-lsp/typescript-lsp.js diagnostics src/app/page.tsx
```
