---
name: code-consistency
description: >
  Enforce, review, and generate consistent code across registered languages: Python,
  Golang, Bash/Shell, Rust, PowerShell, Terraform, Ansible. Auto-expands when new
  languages are encountered. Includes inline quality triage (performance, security,
  testability, architecture smells). Trigger on: "consistency", "style", "conventions",
  "review my code", "refactor", "clean up", "idiomatic", "linting", "best practices",
  "code review", "code smell", or when code is present and a consistency/quality task
  is implied. Also trigger when generating code alongside existing snippets. Do not
  wait to be asked explicitly — if code is present, use this skill.
---

# Code Consistency Skill

Enforces, detects, reviews, and generates consistent code across all registered
languages. Includes inline quality triage — lightweight checks that flag issues
for deeper analysis via the `code-quality` skill when warranted.

---

## Language Registry

Each supported language has a reference file in `references/`. To add a new language,
create `references/<lang>.md` following the four-section template (see below).

| Language | Reference File | Status |
|---|---|---|
| Python | `references/python.md` | ✅ Active |
| Golang | `references/golang.md` | ✅ Active |
| Bash/Shell | `references/bash.md` | ✅ Active |
| Rust | `references/rust.md` | ✅ Active |
| PowerShell | `references/powershell.md` | ✅ Active |
| Terraform (HCL) | `references/terraform.md` | ✅ Active |
| Ansible (YAML) | `references/ansible.md` | ✅ Active |

### Adding a New Language

When encountering a language not in the registry:
1. Create `references/<lang>.md` with the four standard sections:
   - Naming Conventions
   - Error Handling
   - Project Structure & Packaging
   - Logging / Observability
2. Add a row to the registry table above
3. Update the skill description's language list
4. Use authoritative style guides as baseline (official lang docs, widely adopted
   community guides)

---

## Core Philosophy

- **Detect first, enforce second.** Never impose external style onto a codebase with
  its own conventions. Scan what's there and match it.
- **Pragmatic strictness.** Flag *critical* issues (bugs, ambiguity, maintenance traps).
  *Suggest* minor issues. Never block progress over cosmetics.
- **Quality triage.** Surface obvious performance, security, testability, and
  architecture smells inline. Recommend the `code-quality` skill for deep analysis.
- **Context-driven output.** Match format to task:
  - Inline comments → editing a specific file
  - Numbered violation report → broad review
  - Before/after diff → rewriting or refactoring
  - Style guide doc → reference material request

---

## Workflow

### Step 1 — Detect the Language(s)
Identify which language(s) the task involves. Check the registry. If the language
isn't registered and the task is substantial, offer to create a reference file.

### Step 2 — Load Reference Files
Before writing any code or review output, read the appropriate reference(s):
- Single language → read `references/<lang>.md`
- Multi-language (e.g., Terraform + Bash) → read both
- IaC + config tasks → check if Ansible or Terraform references apply

### Step 3 — Style Detection (when existing code is present)
Scan provided code to infer project conventions. Use the **Style Detection Checklist**
below. Record findings as a brief internal "style snapshot" before proceeding.

### Step 4 — Execute the Task

| Mode | When to use |
|---|---|
| **Review** | User pastes code and wants issues flagged |
| **Rewrite/Refactor** | User wants code cleaned up or made compliant |
| **Generate** | User wants new code written in the project's style |
| **Style Guide** | User wants a reference doc or cheat sheet |

### Step 5 — Quality Triage (inline)
While executing, flag any of these if spotted:
- 🔴 **Performance:** O(n²)+ in hot paths, unbounded allocations, blocking I/O
  in async contexts, missing index hints
- 🔴 **Security:** hardcoded secrets, injection vectors, path traversal,
  missing input validation, permissive CORS/auth
- 🟡 **Testability:** god functions (>50 LOC with multiple concerns), hidden
  dependencies, global state, untestable side effects
- 🟡 **Architecture:** circular imports, abstraction leaks, SRP violations,
  inappropriate coupling between layers

If more than 2 quality flags fire, recommend: *"Consider running the `code-quality`
skill for deep analysis on [performance|security|testability|architecture]."*

### Step 6 — Present Output
Use format appropriate to context. Always separate **critical** from **suggested**.

---

## Style Detection Checklist

Run this mentally when existing code is provided.

**Naming**
- [ ] Case convention per symbol type (snake_case, camelCase, PascalCase, kebab-case)
- [ ] Prefix/suffix patterns (e.g., `_internal`, `I`-prefix, `Err`-prefix, `$`-prefix)
- [ ] Constant casing
- [ ] Test naming patterns

**Error Handling**
- [ ] Errors wrapped with context? What mechanism?
- [ ] Sentinel/custom error types?
- [ ] Boundary behavior (panics, exceptions, exit codes, trap handlers)

**Project Structure**
- [ ] Flat vs nested layout
- [ ] Interface/trait placement
- [ ] Module system conventions
- [ ] Config file conventions

**Logging/Observability**
- [ ] Which logging library/mechanism?
- [ ] Structured vs unstructured?
- [ ] Log level conventions
- [ ] Trace/span propagation?

**IaC-Specific** (Terraform/Ansible)
- [ ] Resource naming conventions
- [ ] Module/role structure
- [ ] Variable/parameter organization
- [ ] State/inventory management patterns

---

## Severity Levels

| Level | Label | Meaning |
|---|---|---|
| 🔴 | **CRITICAL** | Bug risk, security issue, or serious maintainability problem. Must fix. |
| 🟡 | **SUGGEST** | Style deviation or improvement opportunity. Worth doing, not blocking. |
| 🔵 | **NOTE** | Observation or informational context. No action required. |

---

## Reference Files

Read before working on language-specific tasks:

- **`references/python.md`** — PEP 8 naming, error handling, packaging, logging, OpenTelemetry
- **`references/golang.md`** — Effective Go + Uber naming, error handling, module layout, logging, OpenTelemetry
- **`references/bash.md`** — Shell naming, error handling (set -euo, traps), script structure, logging
- **`references/rust.md`** — RFC 430 naming, Result/Error handling, Cargo layout, tracing crate
- **`references/powershell.md`** — Verb-Noun naming, error handling, module structure, logging
- **`references/terraform.md`** — HCL naming, error handling, module layout, state management
- **`references/ansible.md`** — YAML conventions, error handling, role structure, logging/verbosity
