---
name: code-navigation
description: "Use when you need to understand the codebase structure, find definitions, or trace references without reading entire files."
version: 1.0.0
last_verified: 2025-12-31
author: system
tags: [lsp, codebase-exploration, architecture, efficiency]
allowed-tools: ["cclsp", "Glob", "Grep", "Read"]
---

# Code Navigation Standards

## 1. Context

This skill enforces "LSP First" - using the Language Server Protocol (`cclsp`) for code navigation instead of token-heavy text processing. This implements the "Precision and Parsimony" principle from the Flywheel architecture.

**Key Principle:** Do not read entire files to find a single definition. Use LSP to navigate like a Software Architect.

## 2. Verified Procedure

### Definition Lookup
```bash
# DO: Use LSP to jump directly to definition
cclsp definition <symbol>

# DON'T: Read the entire file searching for the definition
cat src/large_file.py | grep "def function_name"
```

### Finding References
```bash
# DO: Use LSP to find all usages
cclsp references <symbol>

# DON'T: Grep across the entire codebase
grep -r "function_name" .
```

### Type and Signature Information
```bash
# DO: Use LSP hover to see parameters and types
cclsp hover <symbol>

# DON'T: Read function definition to understand signature
Read src/file.py  # Then manually parse the function signature
```

### Codebase Structure Exploration
```bash
# DO: Use Glob for file discovery first, then LSP for details
Glob "**/*.py" | cclsp outline

# DON'T: Read every file to understand structure
for file in $(find . -name "*.py"); do cat $file; done
```

## 3. Negative Knowledge

### Failed Attempts

| Attempt | Why It Failed | Token Cost |
|---------|---------------|------------|
| Reading full files to find class definitions | Wasted 10,000+ tokens on a 500-line file when LSP would have returned the answer in <50 tokens | 200x overhead |
| Using `grep -r` across large codebases | Returned too many false positives, required reading multiple files to find the right reference | 50x overhead |
| Guessing import paths without LSP verification | Led to incorrect imports that failed at runtime | Required debugging iteration |
| Reading documentation files instead of using `cclsp hover` | Documentation was outdated; LSP provided current signature from source | Incorrect information |

### Anti-Patterns to Avoid

1. **Token Waste:** Reading entire files when you only need a single function signature.
2. **Grep Overuse:** Using `grep` for semantic queries that LSP can answer precisely.
3. **Path Guessing:** Assuming file locations instead of using `cclsp definition` to verify.
4. **Ignoring Type Information:** Not using `cclsp hover` to understand parameter types and return values.

## 4. Tool Selection Matrix

| Task | Tool | Rationale |
|------|------|-----------|
| Find where function is defined | `cclsp definition` | Direct, token-efficient |
| Find all usages of a class | `cclsp references` | Semantic understanding |
| Understand function signature | `cclsp hover` | Includes types and docs |
| Find files matching pattern | `Glob` | Fast file discovery |
| Search for string literal | `Grep` | Text search, not semantic |
| Read implementation details | `Read` | Only after LSP narrows scope |

## 5. Workflow Example

**Task:** "Find where `UserAuth` class is used and understand its constructor"

```bash
# Step 1: Find the definition
cclsp definition UserAuth

# Step 2: Get constructor signature
cclsp hover UserAuth.__init__

# Step 3: Find all references
cclsp references UserAuth

# Step 4: Only NOW read specific files if needed
Read src/auth/user_auth.py
```

**Token Savings:** ~90% compared to reading all files that might contain `UserAuth`.

## 6. Integration with Flywheel

- **Before:** Agent reads 5-10 files (2000+ lines) to understand a function.
- **After:** Agent uses LSP to get exact definition in <20 lines of output.
- **Result:** Faster responses, lower costs, more context budget for complex reasoning.

## 7. Verification Checklist

Before opening a file with `Read`, ask:
- [ ] Can `cclsp definition` answer this question?
- [ ] Can `cclsp references` show me where this is used?
- [ ] Can `cclsp hover` give me the signature/type?
- [ ] Have I used `Glob` to narrow down the file search first?

**If any answer is YES, use that tool FIRST.**

## 8. Maintenance Notes

- **LSP Availability:** Requires `cclsp.json` configuration in repository root.
- **Language Support:** Check which languages are supported by the LSP server in your environment.
- **Fallback:** If LSP fails, THEN use `Grep` + `Read`, but document the failure in this skill's Negative Knowledge.

---

*Last Updated: 2025-12-31*
*Source: The CLAUDE.md Blueprint - LSP First Principle*
