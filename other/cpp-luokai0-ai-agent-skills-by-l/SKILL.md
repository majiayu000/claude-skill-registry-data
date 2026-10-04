---
name: C++
slug: cpp
version: 1.0.1
description: Write safe C++ avoiding memory leaks, dangling pointers, undefined behavior, and ownership confusion.
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":["g++"]},"os":["linux","darwin","win32"]}}
---

## Quick Reference

| Topic | File |
|-------|------|
| RAII, smart pointers, new/delete | `memory.md` |
| Raw pointers, references, nullptr | `pointers.md` |
| Rule of 3/5/0, inheritance, virtual | `classes.md` |
| Containers, iterators, algorithms | `stl.md` |
| Templates, SFINAE, concepts | `templates.md` |
| Threads, mutex, atomics | `concurrency.md` |
| C++11/14/17/20, move semantics | `modern.md` |
| Undefined behavior traps | `ub.md` |

## Critical Rules

- Raw `new` without `delete` leaks — use `std::unique_ptr` or `std::make_unique`
- Returning reference to local — undefined behavior, object destroyed on return
- `==` for C-strings compares pointers — use `std::string` or `strcmp()`
- Signed integer overflow is UB — not wrap-around like unsigned
- Virtual destructor required in base class — otherwise derived destructor skipped
- `std::move` doesn't move — it casts to rvalue, enabling move semantics
- Moved-from object valid but unspecified — don't use without reassigning
- Data race on non-atomic is UB — use `std::mutex` or `std::atomic`
- `vector<bool>` is not a real container — returns proxy, use `deque<bool>`
- `map[key]` inserts default if missing — use `find()` or `contains()` to check
- Braced init `{}` prevents narrowing — `int x{3.5}` errors, `int x(3.5)` truncates
- Iterator invalidation on `push_back` — vector may relocate, invalidating iterators
- `string_view` doesn't own data — underlying string must outlive the view
