---
title: "Wiki Generator with LSP"
linkTitle: "wiki-generator-lsp"
weight: 10
name: wiki-generator-lsp
version: "1.0.0"
description: "Generate comprehensive WIKI.md documentation for any codebase using LSP for precise code analysis. Use when user asks to document a codebase, generate technical documentation, create architecture diagrams, or analyze code structure and dependencies. Supports TypeScript, JavaScript, Python, Go, Rust, Java, and C/C++ projects."
keywords: [documentation, wiki, lsp, code-analysis, mermaid, architecture]
category: documentation
status: tested
languages: [en]
author: s-celles
generated_by: "Claude Opus 4.5"
license: MIT
disclaimer: "Generated documentation should be reviewed for accuracy. AI may misinterpret code structure or produce incomplete analysis."
---

# Wiki Generator with LSP

## Usage

```bash
python scripts/generate_docs.py /path/to/project --output WIKI.md
```

## Workflow

1. **Detect language** from config files (`package.json`, `pyproject.toml`, `go.mod`, etc.)
2. **Start LSP server** for the detected language
3. **Query LSP** for symbols, references, types, and call hierarchy
4. **Generate WIKI.md** with Mermaid diagrams

## LSP Servers

| Language | Server |
|----------|--------|
| TypeScript/JS | `typescript-language-server` |
| Python | `pylsp` |
| Go | `gopls` |
| Rust | `rust-analyzer` |
| C/C++ | `clangd` |

If LSP unavailable, scripts fall back to AST/regex analysis.

## Output Sections

1. Project Overview (tech stack, dependencies)
2. Architecture (Mermaid flowchart)
3. Project Structure (directory tree)
4. Core Components (classes, functions, APIs)
5. Data Flow (Mermaid sequenceDiagram)
6. Data Model (Mermaid erDiagram, classDiagram)
7. API Reference
8. Configuration
9. Getting Started
10. Development Guide

See [references/wiki-template.md](references/wiki-template.md) for section templates.

## Tips

**Analysis:**
- Exclude: `node_modules/`, `venv/`, `.git/`, `dist/`, `build/`
- Prioritize entry points: `main.py`, `index.ts`, `App.tsx`
- For large codebases, focus on `src/` or `lib/`

**Formatting:**
- Use Mermaid diagrams extensively (flowchart, sequenceDiagram, classDiagram, erDiagram)
- Include code snippets where helpful
- Use tables for structured information
- Add navigation links between sections
- Keep explanations clear and concise

## Language Support Details

| Language | Config Files | Entry Points | LSP Server | Installation |
|----------|--------------|--------------|------------|--------------|
| TypeScript/JS | `package.json`, `tsconfig.json` | `index.ts`, `main.ts`, `App.tsx` | `typescript-language-server` | `npm i -g typescript-language-server typescript` |
| Python | `pyproject.toml`, `setup.py`, `requirements.txt` | `main.py`, `app.py`, `__main__.py` | `pylsp` | `pip install python-lsp-server` |
| Go | `go.mod` | `main.go`, `cmd/*/main.go` | `gopls` | `go install golang.org/x/tools/gopls@latest` |
| Rust | `Cargo.toml` | `main.rs`, `lib.rs` | `rust-analyzer` | `rustup component add rust-analyzer` |
| Java | `pom.xml`, `build.gradle` | `Main.java`, `Application.java` | `jdtls` | Eclipse JDT Language Server |
| C/C++ | `CMakeLists.txt`, `Makefile` | `main.c`, `main.cpp` | `clangd` | `apt install clangd` or `brew install llvm` |

## Fallback Analysis

When LSP is unavailable, the scripts use fallback analyzers:

1. **AST Parsing** - For Python (`ast` module) and JavaScript (regex-based)
2. **Regex Patterns** - For function/class detection in other languages
3. **Import Analysis** - Parse import statements for dependency graphs

Fallback provides ~70% of LSP accuracy but works without server setup.

## Troubleshooting

### LSP Server Not Found

```
Error: Could not start LSP server for TypeScript
```

**Solution:** Install the required LSP server globally. See Installation column in Language Support table.

### Timeout During Analysis

```
Error: LSP request timed out
```

**Solutions:**
- Increase timeout: `--timeout 120`
- Reduce scope: `--path src/` instead of entire project
- Check if LSP server is overloaded (large codebase)

### Empty or Incomplete Output

**Possible causes:**
- Project has no recognizable entry points
- LSP server crashed during analysis
- File permissions prevent reading

**Solutions:**
- Specify entry point: `--entry src/main.py`
- Check LSP server logs
- Run with `--verbose` for debug output

### Mermaid Diagrams Not Rendering

Mermaid diagrams require a compatible viewer:
- GitHub/GitLab markdown preview
- VS Code with Mermaid extension
- Mermaid Live Editor: https://mermaid.live

## Performance Considerations

| Project Size | Files | Estimated Time | Memory |
|--------------|-------|----------------|--------|
| Small | < 50 | < 30s | ~100MB |
| Medium | 50-500 | 1-5 min | ~500MB |
| Large | 500-5000 | 5-30 min | 1-2GB |
| Very Large | > 5000 | Consider splitting | 2GB+ |

**Tips for large codebases:**
- Analyze specific directories: `--path src/core`
- Skip test files: `--exclude "**/test/**"`
- Use incremental analysis if available
- Consider generating separate docs per module

## Known Limitations

- **Monorepos**: May need per-package analysis
- **Dynamic imports**: Not fully detected (Python `importlib`, JS `import()`)
- **Metaprogramming**: Dynamically generated code may be missed
- **Private symbols**: Some LSP servers don't expose private members
- **Cross-language projects**: Analyze each language separately

## Best Practices

1. **Run from project root** - Ensures correct path resolution
2. **Commit WIKI.md** - Track documentation changes with code
3. **Regenerate periodically** - Keep docs in sync with codebase
4. **Review output** - AI-generated docs may need human refinement
5. **Customize template** - Adapt `wiki-template.md` to your needs
