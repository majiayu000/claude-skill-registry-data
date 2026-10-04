---
name: C
description: Avoid common C mistakes — memory leaks, buffer overflows, undefined behavior, and pointer traps.
metadata: {"clawdbot":{"emoji":"🔧","requires":{"bins":["gcc"]},"os":["linux","darwin","win32"]}}
---

## Memory Management
- Every `malloc` needs a `free` — track ownership, free once only
- `free(ptr); ptr = NULL;` — prevents use-after-free
- Check `malloc` return — can return NULL on failure
- `calloc` zeros memory — `malloc` leaves garbage
- Memory leaks on early return — ensure cleanup path for all exits

## Buffer Overflows
- `strcpy` doesn't check bounds — use `strncpy` or `snprintf`
- `gets` is never safe — removed in C11, use `fgets`
- `sprintf` can overflow — use `snprintf` with buffer size
- Array index not checked — manual bounds checking required
- Stack buffer overflow corrupts return address — security vulnerability

## Strings
- Strings need null terminator `\0` — `strncpy` may not add it if truncated
- `strlen` doesn't count null — allocate `strlen(s) + 1`
- String literals are immutable — modifying causes undefined behavior
- `sizeof(str)` vs `strlen(str)` — sizeof includes null, strlen doesn't
- `char str[]` copies, `char *str` points to literal — different behavior

## Pointers
- Uninitialized pointer is garbage — always initialize or set to NULL
- Dereferencing NULL is undefined — check before use
- Pointer arithmetic in bytes vs elements — `p + 1` advances by sizeof(*p)
- Array decays to pointer — `sizeof(arr)` in function gives pointer size
- Returning pointer to local — stack frame gone, dangling pointer

## Undefined Behavior
- Signed integer overflow is undefined — not wrap-around like unsigned
- Uninitialized variable read — garbage value, unpredictable
- Modifying variable twice between sequence points — `i++ + i++` undefined
- Null pointer dereference — crash or worse
- Shift by negative or >= width — undefined

## Integer Gotchas
- Integer promotion in expressions — small types promote to int
- Unsigned vs signed comparison — signed converted to unsigned, negative becomes large
- `sizeof` returns `size_t` (unsigned) — subtraction can wrap
- Division truncates toward zero — `-7 / 2` is `-3`, not `-4`

## Arrays
- Array size must be constant (before C99 VLAs) — use malloc for dynamic
- VLAs can stack overflow — no size limit check, avoid for large/variable sizes
- `arr[i]` is `*(arr + i)` — pointer arithmetic under the hood
- Multidimensional arrays contiguous — `arr[i][j]` is `arr[i * cols + j]` equivalent
- Can't return array — return pointer to static or allocated memory

## Preprocessor
- Macro arguments evaluated multiple times — `MAX(i++, j)` increments i multiple times
- Wrap macro body in `do { ... } while(0)` — for statement-like macros
- Wrap arguments in parentheses — `#define SQ(x) ((x) * (x))`
- `#include` order matters — headers may depend on prior includes

## Common Mistakes
- `=` vs `==` in conditions — `if (x = 5)` assigns, always true
- Missing `break` in switch — falls through to next case
- `sizeof(ptr)` gives pointer size — not array or allocated size
- Forgetting to flush stdout — `printf` without `\n` may not appear
- `fopen` returns NULL on failure — always check before using file pointer
