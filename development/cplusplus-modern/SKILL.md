---
name: cplusplus-modern
description: "Modern C++ (C++20/23), RAII memory management, smart pointers, move semantics, and concepts."
---

# Modern C++ Protocol

Write memory-safe, high-speed C++ software.

---

## 1. RAII & Smart Pointers

1. Manage resource lifecycles with RAII.
2. Prefer `std::unique_ptr` for exclusive ownership and `std::shared_ptr` only when shared ownership is mandatory. Avoid raw `new` and `delete`.

---

## 2. Move Semantics & Concepts

Use `std::move` to avoid expensive deep copies. Constrain templates with C++20 `concepts` for clear compiler diagnostics.
