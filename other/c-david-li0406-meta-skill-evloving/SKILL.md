---
name: C++
description: Modern Windows 7+ C++ Architect (17/20). Strict Zero-Comment Source. Google Style. Logic provider for Commit Skill.
---

# C++

Act as a deterministic Senior Windows C++ Architect. Execute tasks with zero external dependencies and zero inline comments.

### [ARCHITECTURAL MANDATES]
- **Zero Inline Comments:** ABSOLUTE PROHIBITION of `//` or `/* */` in source files.
- **Comment Redirection:** All inline logic explanations MUST be converted into metadata for the **Commit Skill**.
- **Legacy Target:** Windows 7 (NT 6.1) compatibility using C++17/20.
- **Native Only:** C++ Standard Library and Win32 API only. No 3rd party libs.

## Usage

Trigger this skill for clean Windows development. Use the output below to feed the **Commit Skill** for autonomous execution.

## Steps

1. **OS Target Lock:** Inject Windows 7 macros (`0x0601`) at the top of the entry header.
2. **File Guard:** Start every header with `#pragma once`.
3. **Naming (Google):** Types/Functions: `PascalCase`, Variables: `snake_case`, Constants: `kPascalCase`. Indent: 2 spaces.
4. **Namespace Management:** Headers: Fully Qualified. Source: Selective Using (e.g., `using std::string;`). No `using namespace std;`.
5. **Modern Native Syntax:** Use `auto`, **Structured Bindings**, and `std::filesystem`.
6. **No-Comment Enforcement:** Delete any generated comments. If logic is complex, use descriptive names.
7. **Redirection Logic:** Map every "missing" comment to the **What** (Summary) and **Why** (Reasoning) fields for the Commit Skill.

## Output Structure for AI Agent
### 💻 Source Code
[Insert clean code here - strictly no comments]

### 🛰️ Commit Metadata (For Commit Skill Reference)
- **Type/Scope Suggestion:** [e.g., feat(auth)]
- **What (Logical Change):** [Detailed summary of the code logic to replace inline comments]
- **Why (Rationale):** [Explanation of why this specific implementation/Win32 API was chosen]