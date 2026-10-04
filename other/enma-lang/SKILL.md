---
name: enma-lang
description: "Enma language and embedding SDK reference: syntax, types, functions, pointers, classes, inheritance, templates, exceptions, modules, compiler semantics, native type/function registration, safety, and standard addons. Use when writing Enma code or embedding/extending the Enma engine; use perception-api for Perception-specific host functions."
---

# Enma Language

Authoritative local snapshot of `https://docs.perception.cx/perception/enma-lang`.

## Workflow

1. Read [references/INDEX.md](references/INDEX.md), then open only the language, SDK, or addon pages needed.
2. Search exact syntax and signatures locally before coding; Enma resembles C++ but is not interchangeable with it.
3. Distinguish script-language code from C++ host SDK code. State which side a snippet targets when it is not obvious.
4. Check `references/language-guide/semantics-and-limits.md` before assuming a C++ feature exists.
5. For embedding work, begin with `references/sdk-guide/quick-start.md`, then consult the focused SDK page and API reference.
6. For library calls, consult the relevant page under `references/addons/`; do not infer APIs from C++ STL names.

## Reference routing

- Syntax and control flow: `references/language-guide/basics.md`
- Functions, lambdas, references, variadics: `references/language-guide/functions.md`
- Pointers and allocation: `references/language-guide/pointers.md`
- Types, layout, operators: `references/language-guide/structs-and-classes.md`, `references/language-guide/operators.md`
- Inheritance/interfaces/access: `references/language-guide/inheritance.md`
- Templates and compile-time behavior: `references/language-guide/templates.md`, `references/language-guide/compile-time.md`
- Exceptions, annotations, builtins: `references/language-guide/exceptions.md`, `references/language-guide/annotations.md`, `references/language-guide/builtin-instructions.md`
- Modules and preprocessing: `references/language-guide/modules.md`, `references/language-guide/pre-processor.md`
- Embedding and registration: `references/sdk-guide/`
- Core and standard libraries: `references/addons/`

## Boundaries

This skill covers Enma itself and its embedding SDK/addons. For APIs that Perception.cx registers for process memory, drawing, GUI, input, networking, Windows interaction, emulation, or disassembly, load the `perception-api` skill.
