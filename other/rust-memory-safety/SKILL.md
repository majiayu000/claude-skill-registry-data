---
name: rust-memory-safety
description: "Rust memory safety, ownership and borrow checker patterns, error handling with Result/Option, and traits."
---

# Rust Architecture & Memory Safety Protocol

Author high-performance, memory-safe software with zero-cost abstractions.

---

## 1. Ownership & Borrowing

1. Prefer borrowing (`&T`, `&mut T`) over cloning (`.clone()`) unless transfer of ownership is explicitly required.
2. Structure data to avoid cyclic references that require `Rc<RefCell<T>>`.

---

## 2. Idiomatic Error Handling

Use `Result<T, E>` with the `?` operator. Create custom error enums with `thiserror` for internal crates.
