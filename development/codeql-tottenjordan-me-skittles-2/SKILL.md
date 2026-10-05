---
name: codeql
type: tool
description: >
  CodeQL is a static analysis framework that queries code as a database.
  Use when you need interprocedural analysis or complex data flow tracking.
---

# CodeQL

CodeQL is a powerful static analysis framework that allows developers and security researchers to query a codebase for specific code patterns. The CodeQL standard libraries implement support for both inter- and intraprocedural control flow and data flow analysis. However, the learning curve for writing custom queries is steep, and documentation for the CodeQL standard libraries is still scant.

## When to Use

**Use CodeQL when:**
- You need interprocedural control flow and data flow queries across the entire codebase
- Fine-grained control over the abstract syntax tree, control flow graph, and data flow graph is required
- You want to prevent introduction of known bugs and security vulnerabilities into the codebase
- You have access to source code and third-party dependencies (and can build compiled languages)
- The bug class requires complex analysis beyond single-file pattern matching

**Consider alternatives when:**
- Single-file pattern matching is sufficient → Consider Semgrep
- You don't have access to source code or can't build the project
- Analysis time is critical (complex queries may take a long time)
- You need to analyze a closed-source repository without a GitHub Advanced Security license
- The language is not supported by CodeQL

## Quick Reference

| Task | Command |
|------|---------|
| Create database (C/C++) | `codeql database create codeql.db --language=cpp --command='make -j8'` |
| Create database (Go) | `codeql database create codeql.db --language=go` |
| Create database (Java/Kotlin) | `codeql database create codeql.db --language=java` |
| Create database (JavaScript/TypeScript) | `codeql database create codeql.db --language=javascript` |
| Create database (Python) | `codeql database create codeql.db --language=python` |
| Analyze database | `codeql database analyze codeql.db --format=sarif-latest --output=results.sarif -- codeql/cpp-queries` |
| List installed packs | `codeql resolve qlpacks` |
| Download query pack | `codeql pack download trailofbits/cpp-queries` |
| Run custom query | `codeql query run --database codeql.db -- path/to/Query.ql` |
| Test custom queries | `codeql test run -- path/to/test/pack/` |

## Installation

### Installing CodeQL

CodeQL can be installed manually or via Homebrew on macOS/Linux.

**Manual Installation:**
Navigate to the [CodeQL release page](https://github.com/github/codeql-action/releases) and download the latest bundle for your architecture. The bundle contains the `codeql` binary, query libraries for supported languages, and pre-compiled queries.

**Using Homebrew:**
```bash
brew install --cask codeql
```

### Keeping CodeQL Up to Date

CodeQL is under active development. Update regularly to benefit from improvements.

**Manual installation:** Download new updates from the [CodeQL release page](https://github.com/github/codeql-action/releases).

**Homebrew installation:**
```bash
brew upgrade codeql
```

### Verification

```bash
codeql --version
```

## Core Workflow

### Step 1: Build a CodeQL Database

To build a CodeQL database, you typically need to be able to build the corresponding codebase. Ensure the codebase is in a clean state (e.g., run `make clean`, `go clean`, or similar).

**For compiled languages (C/C++, Swift):**
```bash
codeql database create codeql.db --language=cpp --command='make -j8'
```

If using CMake or out-of-source builds, add `--source-root` to specify the source file tree root:
```bash
codeql database create codeql.db --language=cpp --source-root=/path/to/source --command='cmake --build build'
```

**For interpreted languages (Python, JavaScript):**
```bash
codeql database create codeql.db --language=python
```

**For languages with auto-detection (Go, Java):**
```bash
codeql database create codeql.db --language=go
```

For complex build systems, use the `--command` argument to pass the build command.

### Step 2: Analyze the Database

Run pre-compiled query packs on the database:

```bash
codeql database analyze codeql.db --format=sarif-latest --output=results.sarif -- codeql/cpp-queries
```

Output formats include SARIF and CSV. SARIF results can be viewed with the [VSCode SARIF Explorer extension](https://marketplace.visualstudio.com/items?itemName=trailofbits.sarif-explorer).

### Step 3: Review Results

SARIF files contain findings with location, severity, and description. Import into your IDE or CI/CD pipeline for review and remediation.

### Installing Third-Party Query Packs

Published query packs are identified by scope/name/version. For example:

```bash
codeql pack download trailofbits/cpp-queries trailofbits/go-queries
```

For Trail of Bits public CodeQL queries, see [trailofbits/codeql-queries](https://github.com/trailofbits/codeql-queries).

## Common Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---------|----------------|------------------|
| Not building project before creating database | CodeQL won't have complete information | Run `make clean` or equivalent, then build with CodeQL |
| Excluding third-party libraries from database | Prevents interprocedural analysis through library code | Include libraries, filter results by location |
| Using relative imports in query packs | Causes resolution issues | Use absolute imports from standard libraries |
| Not adding query metadata | SARIF output lacks severity, description | Always add metadata comment with required fields |
| Forgetting workspace file | CLI won't find query packs | Create `codeql-workspace.yml` in root directory |

## Limitations

- **Licensing:** Closed-source repositories require GitHub Enterprise or Advanced Security license
- **Build requirement:** Compiled languages must be buildable; no build = incomplete database
- **Performance:** Complex interprocedural queries can take a long time on large codebases
- **Language support:** Limited to CodeQL-supported languages and frameworks
- **Learning curve:** Steep learning curve for writing custom queries; documentation is scant
- **Single-language databases:** Each database is for one language; multi-language projects need multiple databases

## Reference material

**[references/customization.md](references/customization.md)** — writing custom queries and configuration

**[references/advanced.md](references/advanced.md)** — advanced usage and CI/CD integration

## Related Skills

| Skill | When to Use Together |
|-------|---------------------|
| **semgrep** | Use Semgrep first for quick pattern-based analysis, then CodeQL for deeper interprocedural analysis |
| **sarif-parsing** | For processing CodeQL SARIF output in custom CI/CD pipelines |

## Resources

### Trail of Bits Blog Posts on CodeQL

- [Look out! Divergent representations are everywhere!](https://blog.trailofbits.com/2022/11/10/divergent-representations-variable-overflows-c-compiler/)
- [Finding unhandled errors using CodeQL](https://blog.trailofbits.com/2022/01/11/finding-unhandled-errors-using-codeql/)
- [Detecting iterator invalidation with CodeQL](https://blog.trailofbits.com/2020/10/09/detecting-iterator-invalidation-with-codeql/)

### Learning Resources

- [CodeQL zero to hero part 1: The fundamentals of static analysis for vulnerability research](https://github.blog/2023-03-31-codeql-zero-to-hero-part-1-the-fundamentals-of-static-analysis-for-vulnerability-research/)
- [QL language tutorials](https://codeql.github.com/docs/writing-codeql-queries/ql-tutorials/)
- [GitHub Security Lab CodeQL CTFs](https://securitylab.github.com/ctf/)

### Writing Custom CodeQL Queries

- [Practical introduction to CodeQL](https://jorgectf.github.io/blog/post/practical-codeql-introduction/)
- [Sharing security expertise through CodeQL packs (Part I)](https://github.blog/2022-04-19-sharing-security-expertise-through-codeql-packs-part-i/)

### Video Resources

- [Trail of Bits: Introduction to CodeQL - Examples, Tools and CI Integration](https://www.youtube.com/watch?v=rQRlnUQPXDw)
- [Finding Security Vulnerabilities in C/C++ with CodeQL](https://www.youtube.com/watch?v=eAjecQrfv3o)
- [Finding Security Vulnerabilities in JavaScript with CodeQL](https://www.youtube.com/watch?v=pYzfGaLTqC0)
- [Finding Security Vulnerabilities in Java with CodeQL](https://www.youtube.com/watch?v=nvCd0Ee4FgE)

### Using CodeQL for Vulnerability Discovery

- [Clang checkers and CodeQL queries for detecting untrusted pointer derefs and tainted loop conditions](https://www.zerodayinitiative.com/blog/2022/2/22/clang-checkers-and-codeql-queries-for-detecting-untrusted-pointer-derefs-and-tainted-loop-conditions)
- [Heap exploitation with CodeQL](https://github.com/google/security-research/blob/master/analysis/kernel/heap-exploitation/README.md)
- [Interesting kernel objects dashboard](https://lookerstudio.google.com/reporting/68b02863-4f5c-4d85-b3c1-992af89c855c/page/n92nD)

### CodeQL in CI/CD

- [Blue-teaming for Exiv2: adding custom CodeQL queries to code scanning](https://github.blog/2021-11-16-adding-custom-codeql-queries-code-scanning/)
- [Best practices on rolling out code scanning at enterprise scale](https://github.blog/2022-09-28-best-practices-on-rolling-out-code-scanning-at-enterprise-scale/)
- [Fine tuning CodeQL scans using query filters](https://colinsalmcorner.com/fine-tuning-codeql-scans/)
