---
name: anti-phantom-symbols
description: Prevents invented APIs, imports, methods, and class members that don't exist. Verifies every symbol against the project's actual codebase and framework docs before writing it.
---

# Anti-Phantom Symbols Skill

## Problem

LLMs routinely fabricate method names, imports, constructor signatures, and constants that look plausible but don't exist. These pass syntax checking, linting, and even import-time checks — they only crash at runtime on the specific code path. This is called **Scaffolding Hallucination**.

Common patterns:
- Calling `session.execution_options(...)` when `AsyncSession` has no such method
- Writing `from pkg.subpkg import Thing` when `Thing` doesn't exist in that module
- Using constructor args that the class doesn't accept
- Calling chained methods where one link in the chain doesn't exist

## Detection triggers

Activate when generating or editing code that:
- Calls a method on a framework object (SQLAlchemy, Django, FastAPI, etc.)
- Imports from a third-party library
- Chains multiple method calls
- Uses a constructor with specific arguments
- References an enum, constant, or config value

## Protocol

### 1. Before writing any method call
Ask: "Have I verified this method exists on this class in the version being used?"

If unsure:
- Check the project's dependency versions (requirements.txt, pyproject.toml, Cargo.toml, etc.)
- Constrain API knowledge to those versions
- Look at existing usage in the project for the correct patterns

### 2. For every import
Verify the import path is real:
- Does the module actually export this symbol?
- Check existing imports in the project for the same library
- If the import has multiple parts (from x.y.z import W), verify each part

### 3. After writing code
Do a **runtime verification pass**:
- Does every method call in the generated code have a corresponding definition?
- Are the argument names and types correct?
- Would this crash if executed right now?

### 4. When uncertain
Add an explicit note: "I used `X.Y()` — please verify this exists in version Z."

## When NOT to use
- Standard library builtins (these are stable)
- Methods you've verified exist via existing project usage
- Code in the same file you're editing (self-referential is fine)

## Bundled Script

Copy `verify-symbols.ps1` to your project's `.ai_scripts/` directory:

```powershell
cp <skill-path>/anti-phantom-symbols/scripts/verify-symbols.ps1 .ai_scripts/
```

Scans project source files to confirm a symbol exists before writing code that depends on it:

```powershell
# Check symbols listed in a file
.ai_scripts\verify-symbols.ps1 -SymbolsFile symbols.txt -ProjectPath src/
```

## Cross-references

- **verify-and-cite** — Both verify existence before referencing.

- **anti-library-hallucination** — Both prevent fabrication. This one covers internal symbols; anti-library-hallucination covers package names.

- **safe-code-modifications** — Verifying symbol usage overlaps with safe removal checks.
- **skill-loader** — Apply the capped selection policy when deciding which verification and safety skills should also be active.
