---
name: c99-code-review
description: Review C99 code for compliance with HBF's strict coding standards including compiler warnings, Linux kernel style, and licensing constraints. Use when reviewing or writing C code in this project.
allowed-tools: Read, Grep, Glob
---

# C99 Code Review Skill

This skill helps review C code against HBF's strict C99 coding standards.

## Review Checklist

When reviewing C99 code for this project, verify compliance with:

### 1. Language Standard: Strict C99

**Requirements:**
- Pure C99 only - NO C++ features or extensions
- NO GNU extensions (use `-std=c99`, not `-std=gnu99`)
- NO inline assembly unless absolutely necessary
- NO VLAs (variable-length arrays) - use fixed-size or malloc

**Common violations:**
```c
// BAD: GNU extension
typeof(x) y = x;

// BAD: C++ style comments (use sparingly, prefer /* */)
int x = 42; // This is bad

// GOOD: C-style comments
int x = 42; /* This is acceptable */
```

### 2. Compiler Warnings (Zero Tolerance)

All code MUST compile with `-Werror` and these flags:

```
-std=c99 -Wall -Wextra -Werror -Wpedantic
-Wconversion -Wdouble-promotion -Wshadow
-Wformat=2 -Wstrict-prototypes -Wold-style-definition
-Wmissing-prototypes -Wmissing-declarations
-Wcast-qual -Wwrite-strings -Wcast-align
-Wundef -Wswitch-enum -Wswitch-default
-Wbad-function-cast
```

**Critical checks:**

- **-Wconversion**: Flag implicit type conversions that may lose data
  ```c
  // BAD: Implicit conversion
  uint8_t x = 256; // Warning: overflow

  // GOOD: Explicit cast after validation
  uint8_t x = (uint8_t)val; // Only if val <= 255
  ```

- **-Wshadow**: No variable shadowing
  ```c
  // BAD: Shadows outer 'i'
  int i = 0;
  for (int i = 0; i < 10; i++) { }

  // GOOD: Use different names
  int outer = 0;
  for (int i = 0; i < 10; i++) { }
  ```

- **-Wstrict-prototypes**: All functions must have prototypes
  ```c
  // BAD: K&R style
  void foo();

  // GOOD: C99 prototype
  void foo(void);
  ```

- **-Wmissing-prototypes**: Declare before define
  ```c
  // BAD: No prototype
  static void helper() { }

  // GOOD: Prototype in header or before use
  static void helper(void);
  static void helper(void) { }
  ```

### 3. Code Style: Linux Kernel Conventions

**Indentation:**
- Use TABS (not spaces) for indentation
- Tab width = 8 characters
- Maximum line length: 100 characters (prefer 80)

**Bracing:**
```c
// GOOD: Opening brace on same line
if (condition) {
	do_something();
} else {
	do_other();
}

// GOOD: Functions have brace on new line
int foo(void)
{
	return 42;
}
```

**Naming:**
- Functions/variables: `snake_case`
- Macros/constants: `UPPER_SNAKE_CASE`
- Type names: `snake_case_t` (with _t suffix)

**Function declarations:**
```c
// GOOD: Return type on same line if it fits
static int calculate_hash(const char *str, size_t len);

// GOOD: Return type on separate line if too long
static struct my_very_long_struct_name *
create_instance(int param1, int param2, int param3);
```

### 4. Security & Safety

**Buffer safety:**
- Always validate buffer sizes before copy/write
- Use `snprintf`, not `sprintf`
- Check return values from all I/O operations

**Integer overflow:**
- Validate arithmetic operations that could overflow
- Use explicit checks before operations

**Null pointer checks:**
```c
// GOOD: Always check malloc/calloc returns
void *ptr = malloc(size);
if (ptr == NULL) {
	return -1;
}
```

**String handling:**
```c
// BAD: Unbounded copy
strcpy(dest, src);

// GOOD: Size-limited with null termination
strncpy(dest, src, sizeof(dest) - 1);
dest[sizeof(dest) - 1] = '\0';
```

### 5. Licensing Constraints

**CRITICAL: No GPL dependencies**

Only these licenses are permitted:
- MIT
- BSD (2-clause, 3-clause)
- Apache 2.0
- Public Domain (SQLite)

**Before adding any third-party code:**
1. Verify license compatibility
2. Document in CLAUDE.md if new dependency
3. Add SPDX header to all new files

**SPDX Headers:**
```c
// SPDX-License-Identifier: MIT
```

### 6. Common Issues to Flag

**Missing error handling:**
```c
// BAD: Ignoring return value
sqlite3_exec(db, sql, NULL, NULL, NULL);

// GOOD: Check and handle errors
int rc = sqlite3_exec(db, sql, NULL, NULL, &err_msg);
if (rc != SQLITE_OK) {
	log_error("SQL error: %s", err_msg);
	sqlite3_free(err_msg);
	return -1;
}
```

**Magic numbers:**
```c
// BAD: Magic number
if (len > 4096) { }

// GOOD: Named constant
#define MAX_BUFFER_SIZE 4096
if (len > MAX_BUFFER_SIZE) { }
```

**Uninitialized variables:**
```c
// BAD: May be uninitialized
int result;
if (condition) {
	result = 42;
}
return result; // Undefined if !condition

// GOOD: Always initialize
int result = 0;
if (condition) {
	result = 42;
}
return result;
```

## Review Process

When reviewing code:

1. **Compile test:** Verify it builds with all warning flags
2. **Style check:** Run through clang-tidy or manual review
3. **Security scan:** Look for common vulnerabilities
4. **License check:** Verify no GPL code introduced
5. **Test coverage:** Ensure new code has tests

## Quick Reference Files

This skill includes reference documentation:
- `COMPILER_FLAGS.md` - Complete list of required compiler flags
- `STYLE_GUIDE.md` - Detailed style guide with examples
- `LICENSES.md` - Approved licenses and checking process

## Testing Integration

All new C code must include tests using minunit-style assertions:

```c
#include <assert.h>

void test_my_function(void)
{
	int result = my_function(42);
	assert(result == expected);
}
```

Run tests via:
```bash
bazel test //hbf/module:my_test
```

## Build Verification

Before approving code:

```bash
# Build with full warnings
bazel build //...

# Run all tests
bazel test //...

# Run linter
bazel run //:lint
```
