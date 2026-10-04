---
name: source-explainer
description: |
  Analyze any codebase's source code in depth and produce structured analysis documents saved as markdown files.
  Use this skill whenever the user asks to understand how a codebase works — architecture, module design, call flows, data models, design patterns, performance characteristics, or any implementation detail.
  Trigger on phrases like "analyze the source", "explain this code", "how does X work", "where is Y implemented", "trace the flow of", "what happens when", "read through the code", "code walkthrough", "源码分析", "代码解读", "实现原理", "架构分析", "调用链路", "模块分析", or any code-exploration request.
  Works with any programming language: TypeScript/JavaScript, Java, Python, Go, Rust, C/C++, and more.
  Even if the user's question seems simple (e.g., "这个文件是干什么的"), use this skill — a thorough, source-backed analysis document is always more valuable than a surface-level guess.
---

## Workflow

Follow these steps in order. The goal is to produce a thorough, code-backed analysis document — not a quick guess.

### Step 0: Project reconnaissance (first time only)

When encountering an unfamiliar codebase for the first time, do a quick reconnaissance before diving into the specific question:

1. **Identify the language and framework**
   - Look for build/config files that reveal the tech stack:
     - `package.json` → Node.js / TypeScript / JavaScript
     - `pom.xml` / `build.gradle` / `build.gradle.kts` → Java / Kotlin
     - `pyproject.toml` / `setup.py` / `requirements.txt` → Python
     - `go.mod` → Go
     - `Cargo.toml` → Rust
     - `CMakeLists.txt` / `Makefile` → C / C++
   - Note the framework (React, Spring Boot, Django, Gin, Actix, Next.js, etc.)

2. **Map the directory structure**
   - Run `tree -L 2 -d` or `ls -R` to get an overview of the project layout
   - Identify: source root, entry points, core modules, config files, test directories

3. **Find the entry point**
   - Use the language-specific tips in the section below to locate the main entry point

4. **Check for existing documentation**
   - Look for README, ARCHITECTURE.md, CONTRIBUTING.md, docs/ directory, or inline module-level comments
   - These often contain architectural decisions and design rationale that save significant research time

Skip this step if you already have a good understanding of the project structure from previous interactions.

### Step 1: Locate relevant source files

Use multiple strategies to find the right files — don't rely on a single approach:

1. **Keyword search** — grep for function names, class names, error messages, or domain terms the user mentioned
2. **Import/dependency tracing** — find who imports the module in question, and what it imports
3. **Directory convention** — most projects follow conventions (`controllers/`, `services/`, `models/`, `utils/`, `handlers/`, `middleware/`, etc.)
4. **Test files** — test files often reveal the intended API, expected behavior, and edge cases of a module
5. **Git history** — if available, `git log --oneline -10 <file>` shows recent evolution and intent behind changes

### Step 2: Deep-read the source code

Research strategy — the order matters:

1. **Start specific.** If the question names a file or function, go there first.
2. **Trace the call chain.** Follow both upstream (who calls this?) and downstream (what does this call?) to understand the full picture.
3. **Read at least 2-3 related files.** A single file rarely tells the whole story. Cross-module boundaries are where the interesting design decisions live.
4. **Study the type system.** Interfaces, types, structs, traits, and abstract classes reveal the data model and contracts between modules — read them before diving into implementation details.
5. **Identify patterns.** Look for recurring patterns like dependency injection, middleware chains, event emitters, plugin systems, observer patterns, or strategy patterns. Naming the pattern helps the reader build a mental model faster.

### Step 3: Write the analysis document

Save the analysis as a markdown file following the document format and file output rules below.

### Step 4: Summarize in chat

After saving the document, give the user a concise summary (3-5 sentences) of the key findings and mention the file path so they can read the full analysis.

## Language-specific reading tips

Use these tips to navigate unfamiliar codebases more efficiently:

| Language                    | Entry point hints                                                            | Key things to read first                                                     | Common patterns to look for                                                                       |
| --------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **TypeScript / JavaScript** | `main.ts`, `index.ts`, `app.ts`, `package.json#main`                         | Interfaces, type aliases, `.d.ts` files, barrel exports (`index.ts`)         | Event emitters, middleware, hooks, decorators, module augmentation                                |
| **Java**                    | `*Application.java`, `public static void main()`, `pom.xml` / `build.gradle` | Interfaces, annotations (`@Service`, `@Controller`, `@Bean`), config classes | Dependency injection, AOP, Builder pattern, Factory pattern, Strategy pattern                     |
| **Python**                  | `__main__.py`, `app.py`, `manage.py`, `pyproject.toml#scripts`               | Type hints, `__init__.py` exports, decorators, ABC classes                   | Decorators, context managers, metaclasses, generator patterns, dataclasses                        |
| **Go**                      | `main.go`, `cmd/` directory, `internal/` for core logic                      | Interface definitions, struct methods, `init()` functions                    | Goroutines + channels, interface composition, functional options, middleware chains               |
| **Rust**                    | `main.rs`, `lib.rs`, `Cargo.toml`                                            | Trait definitions, `impl` blocks, `mod.rs`, error types                      | Ownership/borrowing, trait objects, `Result`/`Option` chains, builder pattern, `From`/`Into`      |
| **C / C++**                 | `main.c` / `main.cpp`, `CMakeLists.txt`, `Makefile`                          | Header files (`.h` / `.hpp`), struct/class definitions, `#include` graph     | RAII, virtual dispatch, preprocessor macros, callback function pointers, template metaprogramming |

## Analysis depth

Automatically choose the right depth based on the user's question:

### Level 1: Project overview

- **Triggers**: "这个项目是做什么的", "architecture overview", "项目结构", "give me an overview", "what does this project do"
- **Output**: High-level architecture diagram, module map with responsibilities, tech stack summary, entry points, key design decisions
- **Scope**: Read directory structure, entry points, README, and top-level module files. No need to trace deep call chains.

### Level 2: Module / feature analysis

- **Triggers**: "how does auth work", "explain the caching layer", "XX模块的实现", "walk me through the payment flow"
- **Output**: Module internals, key classes/functions with signatures, call chains within the module, data flow, interaction with adjacent modules
- **Scope**: Read all files in the relevant module/directory, plus the interfaces it exposes and consumes.

### Level 3: Deep trace

- **Triggers**: "trace the request from X to Y", "why does line 42 do this", "这个函数的完整调用链", "debug this behavior"
- **Output**: Line-by-line analysis of the critical path, full call chain with precise line numbers, edge cases, error handling paths, performance implications
- **Scope**: Follow the execution path across all module boundaries. Read every file the code touches.

When in doubt, default to Level 2. The user can always ask for more or less depth.

## Document format

The document structure adapts to the analysis depth, but follows this general template:

```markdown
# [Question or Topic as Title]

## Overview

A 2-3 sentence summary of the answer for readers who want the quick version.

## Relevant files

- `path/to/file.ext` — one-line description of this file's role in the analysis
- (list all relevant files, sorted by importance)

## Core analysis

The main explanation. Use sub-headings to organize long answers.

Include:

- Core mechanism explained clearly (what it does and why it's designed this way)
- Key function signatures, call chains, and data flow
- Precise line-number references (format: `path/to/file.ext:123`)
- Relationships with other modules

## Key code snippets

For core logic, quote annotated code (keep each snippet under 20 lines):

(code block with language tag and file:line annotation)

## Diagrams

Use mermaid diagrams to visualize complex flows. Choose the right type:

- Call chains / temporal interactions → sequenceDiagram
- Decision flows / processing pipelines → flowchart TD
- Component relationships / module dependencies → graph LR
- State transitions → stateDiagram-v2

Keep diagrams focused — under 20 nodes when possible.

## Design decisions

(Optional) Explain why the code is structured this way. What tradeoffs were made? What alternatives were considered or rejected?

## Potential issues

(Optional) Note any bugs, tech debt, performance concerns, or improvement opportunities spotted during analysis.
```

Sections marked (Optional) should only be included when there is something meaningful to say. Don't pad the document with empty observations.

## File output

- **Default location**: Ask the user where to save, or default to an `analysis/` directory under the project root
- **Filename format**: `{number}-{english-slug}.md` (e.g., `01-authentication-flow.md`, `02-database-connection-pool.md`)
- **Auto-increment**: Check the highest existing number in the output directory and increment by 1
- **Slug**: Convert the question/topic to a lowercase English slug with hyphens
- **Language**: Match the document content language to the user's question language (Chinese question → Chinese document, English question → English document)

## Quality standards

### Accuracy

- **Verify, don't guess.** Every claim must be backed by code you've actually read. If something is uncertain, explicitly say so (e.g., "根据代码推测" / "This appears to be...") and explain your reasoning.
- **Cite precisely.** Use `path/to/file.ext:lineNumber` format. When referencing a function, always include its full file path.
- **Flag uncertainty.** If you can't verify something from the code, say so. A confident wrong answer is worse than an honest "I'm not sure — here's what the code suggests."

### Depth

- **Explain the why.** Design intent and tradeoffs matter more than surface-level description. Understanding _why_ a decision was made is more valuable than knowing _what_ it does.
- **Go deep on the interesting parts.** Not every line of code deserves equal attention. Spend more time on clever algorithms, non-obvious design patterns, and architectural decisions. Skim over boilerplate.
- **Connect the dots.** Show how the piece the user asked about fits into the larger system. A function doesn't exist in isolation — explain its role in the bigger picture.
- **Spot and name patterns.** Identify design patterns (Observer, Strategy, Middleware, Factory, etc.) and name them explicitly. This helps the reader build a mental model faster and connect the code to well-known concepts.

### Practical value

- **Answer "so what?"** After explaining how something works, always explain what that means for the reader. A mechanism description without practical implications is incomplete.
- **Ground usage guidance in real code.** "How to use it" examples should come from actual callers, tests, or configs found in the codebase — not invented from scratch. If no real examples exist, say so and provide a minimal synthetic example clearly labeled as such.
- **Derive best practices from evidence.** Every recommendation in "Best practices" must trace back to a specific code pattern, comment, error handler, or test case. Do not include generic software engineering advice (e.g., "write tests", "use meaningful names") unless the codebase demonstrates a specific, noteworthy approach to it.
- **Distinguish must-do from nice-to-have.** When listing best practices, clearly separate hard constraints (will break if violated) from soft recommendations (improves quality but not required).
- **Include the failure mode.** For each "don't" in best practices, briefly explain what goes wrong if the advice is ignored — ideally citing the defensive code or error handling that reveals the failure path.
