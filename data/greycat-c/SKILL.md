---
name: greycat-c
description: "GreyCat C API and GCL Standard Library reference. Use for: (1) Native C development with gc_machine_t context, tensors, objects, memory management, HTTP, crypto, I/O; (2) GCL Standard Library modules - std::core (Date/Time/Tuple/geospatial types), std::runtime (Scheduler/Task/Logger/User/Security/System/OpenAPI/MCP), std::io (CSV/JSON/XML/HTTP/Email/FileWalker), std::util (Queue/Stack/SlidingWindow/Gaussian/Histogram/Quantizers/Random/Plot). Keywords: GreyCat, GCL, native functions, tensors, task automation, scheduler."
---

# GreyCat SDK - C API & Standard Library

Comprehensive reference for GreyCat native development (C API) and the GCL Standard Library.

## Contents

1. **C API** - Native function implementation, tensor operations, object manipulation
2. **Standard Library (std)** - GCL runtime features, I/O, collections, and utilities

---

# GreyCat C API

## Core Concepts

**gc_machine_t** - Execution context passed to all native functions. Use to get parameters, set results, report errors, and create objects.

**gc_slot_t** - Universal value container (union type) holding any GreyCat value: integers, floats, bools, objects, etc.

**gc_type_t** - Type system enum defining all GreyCat types (null, bool, int, float, str, object, static_field, etc.).

## Common Operations

**Parameter handling:**
```c
gc_slot_t param = gc_machine__get_param(ctx, offset);
gc_type_t type = gc_machine__get_param_type(ctx, offset);
```

**Object field access:**
```c
gc_slot_t value = gc_object__get_at(obj, field_offset, &type, ctx);
```

**Tensor operations:**
```c
gc_core_tensor_t *tensor = gc_core_tensor__create(ctx);
gc_core_tensor__init_2d(tensor, rows, cols, gc_core_TensorType_f32, ctx);
f32_t val = gc_core_tensor__get_2d_f32(tensor, row, col, ctx);
```

**Memory management:**
```c
char *temp = (char *)gc_gnu_malloc(size);      // Per-worker allocator
double *shared = (double *)gc_global_gnu_malloc(size);  // Global allocator
```

## Detailed Reference

**File:** [references/api_reference.md](references/api_reference.md) (1,461 lines)

**Load when implementing:**
- Native C functions with gc_machine_t
- Tensor operations (multi-dimensional arrays)
- Object/field manipulation, type introspection
- Buffer building, string operations
- HTTP client, cryptography, I/O operations

**Contains:** Complete function signatures, real production examples, and documentation for Machine API, Object API, Tensor API, Array/Table APIs, Buffer/String APIs, Memory Allocation, Program/Type System, HTTP Client, Cryptography, and I/O.

---

# GreyCat Standard Library (std)

## Module Organization

- **std::core** - Fundamental types (Date, Time, Duration, Tuple, Error, geospatial types, enumerations)
- **std::runtime** - Scheduler, Task, Job, Logger, User/Security, System, ChildProcess, License, OpenAPI, MCP
- **std::io** - Text/Binary I/O, CSV, JSON, XML, HTTP client, Email/SMTP, FileWalker
- **std::util** - Collections (Queue, Stack, SlidingWindow, TimeWindow), Statistics (Gaussian, Histogram), Quantizers, Assert, ProgressTracker, Crypto, Random, Plot

## Detailed Reference

**File:** [references/standard_library.md](references/standard_library.md) (957 lines)

**Load when working with:**
- Task scheduling and automation (Scheduler with periodicities)
- File I/O operations (CSV, JSON, XML, binary files)
- HTTP integration and REST APIs
- Statistical analysis and data processing
- Security, authentication, and user management
- System operations and logging

**Contains:** Complete documentation for all four standard library modules with code examples, usage patterns, and best practices.
