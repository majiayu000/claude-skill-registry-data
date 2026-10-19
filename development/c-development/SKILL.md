---
name: c-development
description: >
  Develop, review, and secure robust C applications (C11/C17/C23) with explicit
  memory management, boundary checks, and sanitizer verification. Use when
  writing C modules, designing clean C APIs, managing pointers and object lifetimes,
  preventing buffer overflows and undefined behavior, or configuring compiler warnings.
compatibility: >
  Agent Skills-compatible coding agents operating on C codebases with
  GCC or Clang toolchains.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "c, memory-safety, pointers, sanitizers, clang, gcc, undefined-behavior"
  topics: "programming-languages, software-development, security"
---

# Defensive C Development

C provides low-level control over hardware and memory without runtime abstraction. Because C lacks automatic memory management and bounds checking, developers and agents must adopt rigorous defensive patterns, explicit ownership conventions, and automated sanitizer instrumentation to prevent security vulnerabilities and undefined behavior.

Detailed reference guides:
- [Memory Safety & Allocation Patterns](references/memory-safety.md)
- [Undefined Behavior Traps & Prevention](references/undefined-behavior.md)
- [Sanitizers & Compiler Warnings](references/sanitizers-warnings.md)

---

## Core Rules

1. **Every allocation must have a single clear owner**: Pair every `malloc`/`calloc` with a dedicated free function or cleanup block.
2. **Always validate buffer bounds before writing**: Never use unbounded functions like `strcpy`, `strcat`, `sprintf`, or `gets`. Use `snprintf`, `strncpy`, or bounded buffer abstractions.
3. **Check allocation return values**: `malloc` can return `NULL` on memory exhaustion. Always check `if (ptr == NULL)` before dereferencing.
4. **Set pointers to `NULL` after freeing**: Prevent use-after-free bugs by clearing pointers immediately upon deallocation (`free(p); p = NULL;`).
5. **Compile with maximum warnings**: Always build with `-Wall -Wextra -Wpedantic -Werror -Wconversion`.
6. **Instrument with Sanitizers**: Test all test suites with AddressSanitizer (`-fsanitize=address`) and UndefinedBehaviorSanitizer (`-fsanitize=undefined`).

---

## 1. Header Design and C API Encapsulation

### Header Guards and Opaque Structs (Data Hiding)
Hide struct definitions inside `.c` files to prevent callers from depending on internal layout:

```c
/* buffer.h */
#ifndef BUFFER_H
#define BUFFER_H

#include <stddef.h>
#include <stdbool.h>

/* Opaque struct pointer: implementation details hidden */
typedef struct ByteBuffer ByteBuffer;

ByteBuffer* byte_buffer_create(size_t initial_capacity);
void byte_buffer_destroy(ByteBuffer* buf);

bool byte_buffer_append(ByteBuffer* buf, const uint8_t* data, size_t length);
size_t byte_buffer_size(const ByteBuffer* buf);
const uint8_t* byte_buffer_data(const ByteBuffer* buf);

#endif /* BUFFER_H */
```

### Implementation (`buffer.c`)
```c
#include "buffer.h"
#include <stdlib.h>
#include <string.h>

struct ByteBuffer {
    uint8_t* data;
    size_t size;
    size_t capacity;
};

ByteBuffer* byte_buffer_create(size_t initial_capacity) {
    if (initial_capacity == 0) {
        initial_capacity = 64;
    }
    ByteBuffer* buf = malloc(sizeof(ByteBuffer));
    if (!buf) {
        return NULL;
    }
    buf->data = malloc(initial_capacity);
    if (!buf->data) {
        free(buf);
        return NULL;
    }
    buf->size = 0;
    buf->capacity = initial_capacity;
    return buf;
}

void byte_buffer_destroy(ByteBuffer* buf) {
    if (!buf) return;
    free(buf->data);
    buf->data = NULL;
    free(buf);
}
```

---

## 2. Integer Overflow Checks

Integer overflow in signed types is **Undefined Behavior** in C and frequently leads to remote code execution when sizing memory allocations:

```c
#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>

void* safe_alloc_array(size_t count, size_t element_size) {
    /* Check for multiplication overflow: count * element_size > SIZE_MAX */
    if (count != 0 && element_size > SIZE_MAX / count) {
        return NULL; /* Overflow detected */
    }
    return malloc(count * element_size);
}
```

Or using modern compiler built-ins (GCC / Clang):
```c
size_t total_bytes;
if (__builtin_mul_overflow(count, element_size, &total_bytes)) {
    return NULL; /* Arithmetic overflow prevented */
}
void* ptr = malloc(total_bytes);
```

---

## 3. Common Mistakes and Anti-Patterns

| Anti-Pattern | Vulnerability / Bug | Correct Practice |
| :--- | :--- | :--- |
| `strcpy(dest, src)` | Buffer overflow (CWE-120) | Use `snprintf(dest, sizeof(dest), "%s", src)` |
| `free(ptr);` without `ptr = NULL;` | Use-after-free (CWE-416) | Set pointer to `NULL` or adopt RAII/cleanup macros |
| Dereferencing without `NULL` check | Null pointer dereference crash (CWE-476) | Always check `if (ptr == NULL)` immediately |
| `sizeof(pointer)` instead of `sizeof(*pointer)` | Allocates 8 bytes instead of struct size | Use `malloc(sizeof(*ptr))` idiom |
| Signed integer overflow | Undefined behavior; compiler may optimize away checks | Use unsigned arithmetic or `__builtin_add_overflow` |

---

## 4. Compilation Flags and Sanitizers

```bash
# Recommended production build flags
gcc -std=c17 -O2 -Wall -Wextra -Wpedantic -Wconversion -Wformat=2 -D_FORTIFY_SOURCE=2 -fstack-protector-strong

# Recommended debug / testing build flags with Sanitizers
clang -std=c17 -g -O1 -fsanitize=address,undefined -fno-omit-frame-pointer -Wall -Wextra
```

---

## 5. Verification Checklist

- [ ] All allocated memory is freed along every error code path.
- [ ] No unbounded string functions (`strcpy`, `strcat`, `sprintf`, `gets`) are used.
- [ ] Return values of `malloc`, `calloc`, and `realloc` are validated against `NULL`.
- [ ] Code compiles without warnings with `-Wall -Wextra -Wpedantic`.
- [ ] Test suite executes under AddressSanitizer (ASan) and UBSan with zero violations.
