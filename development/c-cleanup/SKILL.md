---
name: c-cleanup
description: Fix memory leaks, apply MISRA guidelines, remove dead code, and clean up C codebases. Use when cleaning up C projects, embedded systems code, addressing.
---

# C Code Cleanup

Systematically identify and remove dead code, fix memory management issues, and apply best practices for safety-critical and embedded C codebases.

## When to Use This Skill

Use this skill when you need to:

- Remove unused includes and dead code
- Fix memory leaks and resource management
- Apply MISRA-C or CERT-C guidelines
- Address static analysis warnings
- Clean up embedded systems code
- Clean up before code review

**Trigger phrases**: "cleanup C", "fix memory leaks", "MISRA C", "remove dead code C", "embedded C cleanup", "C refactor"

## What This Skill Does

### Cleanup Areas

1. **Dead Code Removal**
   - Unused #include directives
   - Unused functions and variables
   - Unreachable code
   - Redundant code

2. **Memory Safety**
   - Memory leaks
   - Buffer overflows
   - Use after free
   - Double free

3. **Style Compliance**
   - MISRA-C rules
   - CERT-C guidelines
   - Project coding standards

## Instructions

### Step 1: Run Static Analysis Tools

```bash
# Run cppcheck for common issues
cppcheck --enable=all --inconclusive .

# Run clang static analyzer
scan-build make

# Run clang-tidy
clang-tidy *.c -- -I./include

# Check with compiler warnings
gcc -Wall -Wextra -Wpedantic -Werror *.c

# Run Valgrind for memory issues
valgrind --leak-check=full --show-leak-kinds=all ./program
```

### Step 2: Fix Common Issues

#### Include Organization

```c
// Standard order: own header, system, third-party, project
#include "mymodule.h"       // Own header first

#include <stdio.h>          // Standard library
#include <stdlib.h>
#include <string.h>

#include <libfoo/foo.h>     // Third-party

#include "config.h"         // Project headers
#include "utils.h"
```

#### Include Guards

```c
// Every header file needs include guards
#ifndef MYMODULE_H
#define MYMODULE_H

// Header contents

#endif /* MYMODULE_H */
```

#### Unused Variables

```c
// Before - compiler warning
void process(int value) {
    int unused = 0;
    // unused is never used
}

// After - mark intentionally unused
void process(int value) {
    (void)value;  // Explicitly mark unused parameter
}

// Or use __attribute__ for GCC/Clang
void callback(int value __attribute__((unused))) {
    // Parameter intentionally unused
}
```

### Step 3: Memory Management

#### Prevent Memory Leaks

```c
// Before - memory leak
char* process_data(const char* input) {
    char* buffer = malloc(256);
    if (input == NULL) {
        return NULL;  // Leak! buffer not freed
    }
    // ...
}

// After - proper cleanup
char* process_data(const char* input) {
    char* buffer = malloc(256);
    if (buffer == NULL) {
        return NULL;
    }
    if (input == NULL) {
        free(buffer);  // Free before return
        return NULL;
    }
    // ...
}
```

#### Check malloc Return Value

```c
// Before - no check
void* ptr = malloc(size);
memcpy(ptr, data, size);  // Crash if malloc failed

// After - always check
void* ptr = malloc(size);
if (ptr == NULL) {
    return ERROR_NO_MEMORY;
}
memcpy(ptr, data, size);
```

#### Prevent Double Free

```c
// Before - potential double free
void cleanup(struct Resource* res) {
    free(res->data);
    // Later code might free again
}

// After - NULL after free
void cleanup(struct Resource* res) {
    free(res->data);
    res->data = NULL;  // Prevent double free
}
```

#### Use After Free Prevention

```c
// Before - use after free
void process(void) {
    char* data = malloc(100);
    free(data);
    printf("%s\n", data);  // Use after free!
}

// After - NULL and check
void process(void) {
    char* data = malloc(100);
    // ... use data ...
    free(data);
    data = NULL;  // Prevent use after free
}
```

### Step 4: Buffer Safety

#### Safe String Operations

```c
// Before - buffer overflow risk
char buffer[64];
strcpy(buffer, user_input);  // No bounds checking!

// After - use safe alternatives
char buffer[64];
strncpy(buffer, user_input, sizeof(buffer) - 1);
buffer[sizeof(buffer) - 1] = '\0';  // Ensure null termination

// Or use snprintf
char buffer[64];
snprintf(buffer, sizeof(buffer), "%s", user_input);
```

#### Safe sprintf

```c
// Before - buffer overflow
char msg[100];
sprintf(msg, "User: %s, ID: %d", username, id);

// After - use snprintf
char msg[100];
int written = snprintf(msg, sizeof(msg), "User: %s, ID: %d", username, id);
if (written >= sizeof(msg)) {
    // Handle truncation
}
```

#### Array Bounds Checking

```c
// Before - no bounds check
void process_array(int* arr, int index) {
    arr[index] = 0;  // May be out of bounds
}

// After - bounds checking
void process_array(int* arr, size_t size, size_t index) {
    if (index < size) {
        arr[index] = 0;
    }
}
```

### Step 5: Modern C Patterns (C99+)

#### Fixed-Width Integer Types

```c
// Before - platform-dependent sizes
int counter;
unsigned long value;

// After - explicit sizes (C99)
#include <stdint.h>
int32_t counter;
uint64_t value;
```

#### Boolean Type

```c
// Before - int as boolean
int is_valid = 1;

// After - proper bool (C99)
#include <stdbool.h>
bool is_valid = true;
```

#### Variable Declarations

```c
// Before - all declarations at top (C89)
void function(void) {
    int i;
    int j;
    int result;

    for (i = 0; i < 10; i++) {
        // ...
    }
}

// After - declare at point of use (C99)
void function(void) {
    for (int i = 0; i < 10; i++) {
        int result = compute(i);
        // ...
    }
}
```

#### Designated Initializers

```c
// Before - positional initialization
struct Config cfg = { 100, 200, "default", NULL };

// After - designated initializers (C99)
struct Config cfg = {
    .width = 100,
    .height = 200,
    .name = "default",
    .callback = NULL
};
```

### Step 6: Embedded Systems Best Practices

#### Volatile for Hardware Registers

```c
// Before - may be optimized away
uint32_t* status_reg = (uint32_t*)0x40001000;
while (*status_reg & BUSY_FLAG) {
    // Wait for ready
}

// After - prevent optimization
volatile uint32_t* status_reg = (volatile uint32_t*)0x40001000;
while (*status_reg & BUSY_FLAG) {
    // Compiler won't optimize this away
}
```

#### Static Allocation for Embedded

```c
// Avoid dynamic allocation in embedded systems
// Before
char* buffer = malloc(256);

// After - static allocation
static char buffer[256];

// Or use memory pool
#define POOL_SIZE 10
static struct Object object_pool[POOL_SIZE];
static bool object_used[POOL_SIZE];
```

#### Interrupt Safety

```c
// Shared variable between ISR and main code
static volatile bool flag = false;

// ISR
void Timer_ISR(void) {
    flag = true;
}

// Main code - atomic read
void main_loop(void) {
    // Disable interrupts for atomic access
    DISABLE_INTERRUPTS();
    bool local_flag = flag;
    flag = false;
    ENABLE_INTERRUPTS();

    if (local_flag) {
        process_timer_event();
    }
}
```

### Step 7: Error Handling

```c
// Before - no error handling
FILE* f = fopen(filename, "r");
fread(buffer, 1, size, f);
fclose(f);

// After - proper error handling
FILE* f = fopen(filename, "r");
if (f == NULL) {
    return ERROR_FILE_OPEN;
}

size_t read = fread(buffer, 1, size, f);
if (read != size) {
    fclose(f);
    return ERROR_FILE_READ;
}

if (fclose(f) != 0) {
    return ERROR_FILE_CLOSE;
}

return SUCCESS;
```

### Step 8: MISRA-C Key Rules

```c
// Rule 11.3: No casts between pointer and integer
// Bad
int addr = (int)ptr;

// Rule 14.4: Controlling expression must have boolean type
// Before
if (ptr) { ... }
// After
if (ptr != NULL) { ... }

// Rule 15.5: Function should have single exit point
// Before
int process(int x) {
    if (x < 0) return -1;
    if (x > 100) return -2;
    return x * 2;
}
// After
int process(int x) {
    int result;
    if (x < 0) {
        result = -1;
    } else if (x > 100) {
        result = -2;
    } else {
        result = x * 2;
    }
    return result;
}

// Rule 17.7: Return value should not be discarded
// Before
memcpy(dest, src, n);  // Return value ignored
// After
(void)memcpy(dest, src, n);  // Explicitly ignored
```

## Tools

- **cppcheck**: Static analysis
- **clang-tidy**: Linting and fixes
- **Clang Static Analyzer**: Bug detection
- **Valgrind**: Memory debugging
- **PC-lint/Flexelint**: Commercial linter
- **Coverity**: Commercial analysis
- **gcov**: Code coverage

## Quality Checklist

- [ ] Unused includes removed
- [ ] Unused functions removed
- [ ] All malloc checked for NULL
- [ ] All malloc has matching free
- [ ] No buffer overflows
- [ ] No use after free
- [ ] Static analysis clean
- [ ] Valgrind clean
- [ ] Build clean with -Wall -Wextra
- [ ] Tests pass

## Common Issues and Solutions

### Issue: Memory leak detected
**Solution**: Track allocations and ensure matching frees:
```c
// Use cleanup labels
void function(void) {
    char* buf1 = malloc(100);
    if (!buf1) goto cleanup;

    char* buf2 = malloc(100);
    if (!buf2) goto cleanup_buf1;

    // Use buffers...

    free(buf2);
cleanup_buf1:
    free(buf1);
cleanup:
    return;
}
```

### Issue: Format string vulnerability
**Solution**: Always use format strings with printf family:
```c
// Before - vulnerable
printf(user_string);

// After - safe
printf("%s", user_string);
```

### Issue: Integer overflow
**Solution**: Check before arithmetic:
```c
if (a > INT_MAX - b) {
    // Overflow would occur
    return ERROR;
}
int result = a + b;
```

## Related Skills

- `code-review-security` - Security analysis
- `code-review-quality` - Code quality assessment

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates code_cleanup/c_cleanup.md


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
