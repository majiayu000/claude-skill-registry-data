---
name: lsp-enable
description: Use when navigating code, understanding unfamiliar functions, finding definitions or references, tracing call hierarchies, preparing for refactoring, or analyzing code impact. Enforces LSP-first semantic code intelligence with mandatory pre-edit checks, impact analysis before refactoring, and post-edit diagnostics. Provides IDE-like precision for code operations in large codebases. Covers navigation (goToDefinition, findReferences), understanding (hover, documentSymbol), and call analysis (incomingCalls, outgoingCalls).
---

# LSP-First Code Intelligence

## The Iron Laws

```
1. NO MODIFYING UNFAMILIAR CODE WITHOUT goToDefinition FIRST
2. NO REFACTORING WITHOUT findReferences IMPACT ANALYSIS FIRST
3. NO CLAIMING CODE WORKS WITHOUT LSP DIAGNOSTICS VERIFICATION
```

Violating these laws wastes tokens, introduces bugs, and produces incomplete changes.

## Trigger Phrases

Activate when user says:

- "find definition", "go to definition", "where is X defined"
- "find references", "who uses this", "what calls this function"
- "understand this code", "trace this function", "explore codebase"
- "before I refactor", "impact of changing", "safe to rename"
- "analyze dependencies", "call hierarchy", "incoming calls"
- "check this code", "verify implementation", "LSP diagnostics"

## Core Decision Tree

```
WHAT DO YOU NEED?
│
├─ Symbol definition or implementation
│  └─ USE LSP: goToDefinition, goToImplementation
│
├─ All usages of a symbol
│  └─ USE LSP: findReferences
│
├─ Type info, docs, or signatures
│  └─ USE LSP: hover
│
├─ File structure or symbol list
│  └─ USE LSP: documentSymbol
│
├─ Call graph or dependencies
│  └─ USE LSP: incomingCalls, outgoingCalls
│
├─ Symbol search across workspace
│  └─ USE LSP: workspaceSymbol
│
├─ Literal text search (TODOs, strings, config)
│  └─ USE: Grep (LSP doesn't do text matching)
│
└─ File discovery by pattern
   └─ USE: Glob
```

## The Nine LSP Operations

| Operation              | Purpose                         | Use Before                |
| ---------------------- | ------------------------------- | ------------------------- |
| `goToDefinition`       | Jump to where symbol is defined | Modifying unfamiliar code |
| `findReferences`       | Find all usages of a symbol     | Refactoring, renaming     |
| `goToImplementation`   | Find interface implementations  | Working with polymorphism |
| `hover`                | Get type info, docs, signatures | Understanding APIs        |
| `documentSymbol`       | List all symbols in a file      | Understanding large files |
| `workspaceSymbol`      | Search symbols across codebase  | Finding related code      |
| `prepareCallHierarchy` | Get call hierarchy info         | Analyzing call graphs     |
| `incomingCalls`        | Find callers of a function      | Impact analysis           |
| `outgoingCalls`        | Find functions called by target | Dependency tracing        |

**Required parameters for all operations:**

- `filePath` - Absolute path to file
- `line` - Line number (1-based)
- `character` - Column position (1-based)

**Full operation guide:** `references/lsp-operations-guide.md`

## Pre-Edit Protocol (Mandatory)

Before modifying ANY unfamiliar code:

```
1. NAVIGATE: LSP goToDefinition → understand implementation
2. ANALYZE: LSP findReferences → assess change impact
3. INSPECT: LSP hover → verify type signatures
4. THEN: Make changes
```

**Pre-Edit Checklist:**

- [ ] Used goToDefinition to understand implementation
- [ ] Used findReferences to identify all usages
- [ ] Reviewed type signatures via hover
- [ ] Understand interface/trait contracts
- [ ] Know what breaks if this changes

**Skip any step = incomplete understanding = bugs**

## Post-Edit Verification (Mandatory)

After code changes:

```
1. CHECK: LSP diagnostics for errors/warnings
2. VERIFY: No new type errors introduced
3. CONFIRM: Imports resolve correctly
4. VALIDATE: Interface contracts still satisfied
```

Do NOT claim code works without LSP diagnostics verification.

## LSP Availability Check

Before LSP operations, verify setup:

```bash
# Environment variable must be set
echo $ENABLE_LSP_TOOL  # Should output "1"

# If not set, add to shell profile:
export ENABLE_LSP_TOOL=1
```

**If LSP unavailable:**

1. **Warn user:** "LSP not available. Semantic operations will be less accurate."
2. **Suggest fix:** "Set `ENABLE_LSP_TOOL=1` in your shell profile"
3. **Fall back:** Use Grep/Read with documented limitation
4. **Note limitation:** "Used grep fallback - may include false positives"

**Full setup guide:** `references/lsp-setup-verification.md`

## Server Installation

If LSP servers are not installed, use `/lsp-tools:lsp-setup` for guided installation.

**Quick verification:**
```bash
# Run verification script
bash "${CLAUDE_PLUGIN_DIR}/scripts/bash/verify-lsp-servers.sh"
```

**Per-language installation scripts are available:**

| Language | Server | Install Script |
|----------|--------|----------------|
| TypeScript/JS | vtsls | `scripts/bash/install-typescript-lsp.sh` |
| Python | pyright | `scripts/bash/install-python-lsp.sh` |
| Rust | rust-analyzer | `scripts/bash/install-rust-lsp.sh` |
| Go | gopls | `scripts/bash/install-go-lsp.sh` |
| Java | jdtls | `scripts/bash/install-java-lsp.sh` |
| Kotlin | kotlin-language-server | `scripts/bash/install-kotlin-lsp.sh` |
| C/C++ | clangd | `scripts/bash/install-cpp-lsp.sh` |
| C# | OmniSharp | `scripts/bash/install-csharp-lsp.sh` |
| PHP | phpactor | `scripts/bash/install-php-lsp.sh` |
| Ruby | ruby-lsp | `scripts/bash/install-ruby-lsp.sh` |
| HTML/CSS | vscode-langservers | `scripts/bash/install-html-css-lsp.sh` |
| LaTeX | texlab | `scripts/bash/install-latex-lsp.sh` |

**Windows users:** Use corresponding PowerShell scripts in `scripts/powershell/`.

**Server registry with full details:** `references/lsp-server-registry.md`

## Why LSP Over Grep

| Metric                     | LSP                         | Grep                               |
| -------------------------- | --------------------------- | ---------------------------------- |
| **Speed (large codebase)** | ~50ms                       | 45+ seconds                        |
| **Accuracy**               | Exact semantic matches      | Text patterns (false positives)    |
| **Token usage**            | ~500 tokens (worth it)      | Burns tokens on irrelevant matches |
| **Type resolution**        | Follows aliases, re-exports | Text only                          |
| **Scope awareness**        | Understands variable scope  | Matches all text                   |

**Example:**

```
Grep "getUserById" → 500+ matches (comments, strings, similar names)
LSP findReferences → 23 matches (exact function usages only)
```

## Red Flags - STOP and Use LSP

If you catch yourself:

- "I'll just grep for the function name"
- "Quick refactor, don't need to check references"
- "Code looks fine, probably works"
- "I know what this function does" (without reading it)
- Proposing changes to unfamiliar code without navigation
- Claiming refactor is complete without impact analysis

**ALL of these mean: STOP. Use LSP first.**

## Token Optimization Awareness

**LSP is more expensive per-call but cheaper overall:**

| Scenario                               | Grep Cost                      | LSP Cost                   |
| -------------------------------------- | ------------------------------ | -------------------------- |
| Find method usages in 100-file project | 2000+ tokens (scanning output) | 500 tokens (exact matches) |
| Navigate to definition                 | Multiple grep attempts         | Single LSP call            |
| Understand type signatures             | Read multiple files            | Single hover call          |

**Rule:** When codebase > 20 files, LSP saves tokens vs grep.

## Language-Specific Guidance

Use language-specific LSP sections for tooling and quality gates:

| Language              | Reference File                         |
| --------------------- | -------------------------------------- |
| TypeScript/JavaScript | `references/typescript-lsp-section.md` |
| Python                | `references/python-lsp-section.md`     |
| Go                    | `references/go-lsp-section.md`         |
| Rust                  | `references/rust-lsp-section.md`       |
| Java                  | `references/java-lsp-section.md`       |
| Kotlin                | `references/kotlin-lsp-section.md`     |
| C/C++                 | `references/cpp-lsp-section.md`        |
| C#                    | `references/csharp-lsp-section.md`     |
| PHP                   | `references/php-lsp-section.md`        |
| Ruby                  | `references/ruby-lsp-section.md`       |
| HTML/CSS              | `references/html-css-lsp-section.md`   |
| LaTeX                 | `references/latex-lsp-section.md`      |

Each file includes:

- Navigation and verification workflows
- Pre-edit checklists
- Language-specific quality gates
- Hooks for automated formatting/linting

## Enforcement Protocol Summary

**Reference:** `references/lsp-enforcement-protocol.md`

1. **Pre-Edit:** LSP navigation is MANDATORY before modifying unfamiliar code
2. **Pre-Refactor:** findReferences impact analysis is MANDATORY
3. **Post-Edit:** LSP diagnostics check is MANDATORY before claiming success
4. **Fallback:** When LSP unavailable, warn → suggest fix → document limitation
5. **Token awareness:** Prefer LSP over grep for semantic operations

## Quick Reference

**Before modifying code:**

```
LSP goToDefinition → Understand implementation
LSP findReferences → Know what breaks
LSP hover → Verify types
```

**After modifying code:**

```
LSP diagnostics → Check for errors
Build/typecheck → Verify compilation
Tests → Confirm behavior
```

**Decision matrix:** `references/lsp-decision-matrix.md`
