---
name: style
description: Code Style skill for the ikigai project
---

# Code Style

## Description
Code style conventions for ikigai development.

## Details

### Comments

- Use `//` style only (never `/* ... */`)
- Comment why, not what
- Use sparingly

### Numeric Types

- Always use `<inttypes.h>` for numeric types and format specifiers
- Never use primitive types (`int`, `long`, etc.)
- Use explicit sized types: `int8_t`, `int16_t`, `int32_t`, `int64_t`, `uint8_t`, etc.
- Use `size_t` for sizes and counts
- Use `PRId32`, `PRIu64`, etc. for printf format specifiers
- Use `SCNd32`, `SCNu64`, etc. for scanf format specifiers

Example:
```c
#include <inttypes.h>

int32_t count = 42;
uint64_t size = 1024;
printf("Count: %" PRId32 ", Size: %" PRIu64 "\n", count, size);
```

### Include Order

Follow Google C++ style guide for #include ordering:

1. Own header first (e.g., `config.h` in `config.c`) - catches missing dependencies
2. Project headers (`"header.h"`) - alphabetically sorted
3. System/library headers (`<header.h>`) - alphabetically sorted

Example:
```c
#include "config.h"           // Own header

#include "json_allocator.h"   // Project headers (alphabetical)
#include "logger.h"
#include "panic.h"
#include "wrapper.h"

#include <errno.h>            // System headers (alphabetical)
#include <stdlib.h>
#include <string.h>
```

Rationale: Project headers before system headers catches non-self-contained headers early.

### Avoid Static Functions

Do not use `static` helper functions in implementation files. Instead, inline the code directly.

**Why:** LCOV exclusion markers (`LCOV_EXCL_BR_LINE`) on PANIC/assert calls inside static functions are not reliably honored, breaking 100% branch coverage requirements.

**Exception:** MOCKABLE wrapper functions (see `wrapper.h`) - these use static functions by design for the mocking interface.

**Instead of:**
```c
static yyjson_mut_val *build_param(yyjson_mut_doc *doc, const char *desc)
{
    yyjson_mut_val *p = yyjson_mut_obj(doc);
    if (p == NULL) PANIC("Out of memory"); // LCOV_EXCL_BR_LINE - NOT HONORED!
    return p;
}
```

**Do:**
```c
// Inline the code at each call site
yyjson_mut_val *p = yyjson_mut_obj(doc);
if (p == NULL) PANIC("Out of memory"); // LCOV_EXCL_BR_LINE - works
```

### Test Code Style

Always add a blank line between END_TEST and START_TEST.
