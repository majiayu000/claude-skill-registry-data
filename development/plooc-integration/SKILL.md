---
name: plooc-integration
description: Use when integrating, refactoring, or debugging PLOOC object-oriented C - def_class encapsulation, private_member protection, vtable dispatch, or inheritance-style structs
---

# PLOOC Integration

## Overview

Use this skill when PLOOC (Protected Low-overhead Object-Oriented Programming with ANSI-C, by GorgonMeducer) is used to structure embedded C code. PLOOC mimics classes with masked structures: outside the class `.c` file, `private_member`/`protected_member` regions appear as an opaque byte array, so the real work is getting the per-file `__<NAME>_CLASS_IMPLEMENT`/`__<NAME>_CLASS_INHERIT__` guards, member visibility, and vtable/interface dispatch correct. Apply it only where object-style boundaries reduce real complexity.

## When To Use

Use this skill when:

- The user mentions PLOOC, `def_class`/`end_def_class`, `private_member`/`protected_member`/`public_member`, `implement()`-style inheritance, or vtable-based dispatch (`def_interface`) in embedded C.
- A legacy driver/module is being wrapped into an encapsulated class with `plooc_class.h`.
- The issue involves the masked-struct layout, the `__..._CLASS_IMPLEMENT` guard, `__OOC_DEBUG__`, initialization order, object lifetime, or callback/vtable dispatch.

Do not use this skill for simple drivers where plain C structs and functions are clearer.

## First Questions

Ask for:

- PLOOC version (`private_method()`/`protected_method()`/`public_method()` were added in v4.6.4) and target compiler.
- C standard: PLOOC needs ANSI-C99; C90 requires `__OOC_DEBUG__` (private-member protection is disabled in that mode); overload/`_Generic` features need C11.
- Which template is selected: `__PLOOC_CLASS_USE_STRICT_TEMPLATE__` (strict), simple, simple_c90, or black_box.
- Module being refactored and whether it uses single or multiple inheritance (`implement()`).
- Memory policy: static objects vs `__new_class()`/`__free_class()` / `__plooc_malloc_align()`.

## Integration Checklist

1. Set up the header guard pattern.
   In the class header, map the module macro to the framework macro before including `plooc_class.h`, e.g. `#if defined(__BYTE_QUEUE_CLASS_IMPLEMENT) # define __PLOOC_CLASS_IMPLEMENT__ #elif defined(__BYTE_QUEUE_CLASS_INHERIT__) # define __PLOOC_CLASS_INHERIT__ #endif`.

2. Declare then define the class.
   Use `dcl_class(foo_t)` / `declare_class(foo_t)` (expands to `typedef struct foo_t foo_t;`), then `def_class(foo_t, ...)` ... `end_def_class(foo_t)`. Group members with `public_member(...)`, `protected_member(...)`, `private_member(...)` (any order allowed).

3. Define the implement macro in exactly one `.c` file.
   The class `.c` does `#define __BYTE_QUEUE_CLASS_IMPLEMENT` before `#include "./byte_queue.h"`, so only that file sees real private members; every other translation unit sees the masked byte array.

4. Access `this` inside methods correctly.
   Use `class_internal(ptObj, ptThis, foo_t)` to obtain the typed `ptThis`, and the `#define this (*ptThis)` convention for member access. Mark unused args with `PLOOC_UNUSED_PARAM`.

5. Handle inheritance explicitly.
   Embed a base with `implement(base_t)` in the derived `def_class`; the framework generates a `use_as__<base>` member for the embedded base. Define `__<NAME>_CLASS_INHERIT__` in a consumer that only needs to read the base's protected members. Access base functionality by passing the address of the `use_as__<base>` member to the base-class functions.

6. Keep dispatch inspectable.
   Define vtables with `def_interface(i_foo_t)` ... `end_def_interface(i_foo_t)` and a single const interface instance; verify each function pointer is assigned.

## Common Failures

- Forgetting `#define __<NAME>_CLASS_IMPLEMENT` in the class `.c`, so the implementation only sees the opaque mask and member access fails to compile.
- Defining the implement macro in more than one file, breaking encapsulation.
- Mismatched template selection: header uses `__PLOOC_CLASS_USE_STRICT_TEMPLATE__` but a consumer includes with a different template, corrupting struct layout.
- C90 or non-C99 toolchain without `__OOC_DEBUG__`, so masked structs do not size correctly.
- `implement(base_t)` omitted, so no `use_as__<base>` member is generated and base-class functions cannot be reached from the derived object.
- Private members invisible in the debugger because `__OOC_DEBUG__` is not defined for the debug build.
- Missing include order: `plooc.h`/`plooc_class.h` (and `<stdlib.h>` for `__new_class`) not reachable on the include path.

## Verification

Before claiming PLOOC integration works:

- State the PLOOC version, C standard, and which class template (`strict`/`simple`/`black_box`) is used.
- Confirm the header maps `__<NAME>_CLASS_IMPLEMENT`/`__<NAME>_CLASS_INHERIT__` before including `plooc_class.h`, and the implement macro is defined in exactly one `.c`.
- Confirm `sizeof(foo_t)` is identical inside and outside the implementing file (mask size matches real struct).
- Confirm methods resolve `this` via `class_internal(...)` and every vtable pointer in the `def_interface` instance is set.
- Confirm private members are visible in GDB with `__OOC_DEBUG__` in the debug build, and old behavior is preserved for the migrated module.

## Example

User:

```text
想用 PLOOC 重构几个传感器驱动。
```

Agent:

1. Asks the PLOOC version, C standard, and whether the sensors share a base class needing `implement()`.
1. Migrates one sensor family: `dcl_class`/`def_class` with `private_member`/`public_member`, sets `__<NAME>_CLASS_IMPLEMENT` in one `.c`, exposes ops via `def_interface`.
1. Verifies `sizeof` mask consistency, vtable wiring, and that private members are inspectable under `__OOC_DEBUG__`.
