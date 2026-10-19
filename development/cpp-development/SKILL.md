---
name: cpp-development
description: >
  Develop, review, and modernize idiomatic C++ applications (C++17/C++20/C++23)
  following the C++ Core Guidelines and RAII principles. Use when writing modern
  C++ classes, managing lifetimes with smart pointers, applying move and value
  semantics, writing generic templates/concepts, ensuring exception safety,
  or configuring modern CMake targets.
compatibility: >
  Agent Skills-compatible coding agents operating on C++ codebases with
  Clang, GCC, or MSVC toolchains.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "cpp, modern-cpp, raii, smart-pointers, cmake, templates, core-guidelines"
  topics: "programming-languages, software-development"
---

# Modern Idiomatic C++ Development

Modern C++ (C++17, C++20, C++23) emphasizes **Resource Acquisition Is Initialization (RAII)**, strict type safety, value semantics, and zero-cost abstractions. Avoid legacy C-style idioms such as raw `new`/`delete`, raw C-arrays, and manual error return codes.

Detailed reference guides:
- [RAII & Smart Pointer Lifetimes](references/raii-smart-pointers.md)
- [Modern C++ Standards (C++17 to C++23)](references/modern-cpp-standards.md)
- [C++ Core Guidelines & Exception Safety](references/core-guidelines.md)

---

## Core Rules

1. **RAII is mandatory**: Tie every system resource (heap memory, file handles, mutex locks, sockets) to the lifetime of an object on the stack.
2. **No manual `new` or `delete`**: Use `std::make_unique<T>()` and `std::make_shared<T>()`.
3. **Follow the Rule of Zero**: Design classes with member types that manage their own resources (e.g. `std::string`, `std::vector`, `std::unique_ptr`) so you don't need custom copy/move constructors or destructors.
4. **Const correctness**: Mark member functions `const` if they do not modify observable state. Mark variables `const` or `constexpr` by default.
5. **Pass large objects by `const&` or by value with `std::move`**: Never copy large collections unnecessarily.
6. **Use modern CMake targets**: Avoid global commands like `include_directories` or `link_libraries`. Always use `target_include_directories`, `target_link_libraries`, and target-based properties.

---

## 1. Resource Management: RAII and Smart Pointers

```cpp
#include <memory>
#include <string>
#include <fstream>
#include <stdexcept>

class FileLogger {
public:
    explicit FileLogger(const std::string& filepath)
        : file_stream_(filepath, std::ios::app) {
        if (!file_stream_.is_open()) {
            throw std::runtime_error("Failed to open log file: " + filepath);
        }
    }

    // Default destructor automatically closes file_stream_ (Rule of Zero)
    ~FileLogger() = default;

    void log(std::string_view message) {
        file_stream_ << message << '\n';
    }

private:
    std::ofstream file_stream_;
};

// Creating polymorphic objects with exclusive ownership
void process_logging() {
    auto logger = std::make_unique<FileLogger>("app.log");
    logger->log("Service initialized successfully.");
    // logger automatically freed when going out of scope - even if an exception is thrown!
}
```

---

## 2. Value Semantics and Move Semantics

Leverage move semantics to transfer expensive heap buffers without deep copies:

```cpp
#include <vector>
#include <string>
#include <utility>

class Document {
public:
    // Accept by value and move into internal storage
    Document(std::string title, std::vector<std::string> lines)
        : title_(std::move(title)), lines_(std::move(lines)) {}

    [[nodiscard]] const std::string& title() const noexcept { return title_; }
    [[nodiscard]] const std::vector<std::string>& lines() const noexcept { return lines_; }

private:
    std::string title_;
    std::vector<std::string> lines_;
};
```

---

## 3. Modern Concepts (C++20) vs Template SFINAE

Constrain template parameters with expressive concepts instead of complex `std::enable_if_t`:

```cpp
#include <concepts>
#include <iostream>

template <typename T>
concept Printable = requires(T a) {
    { std::cout << a } -> std::same_as<std::ostream&>;
};

template <Printable T>
void print_value(const T& val) {
    std::cout << "Value: " << val << '\n';
}
```

---

## 4. Modern Target-Based CMake

```cmake
cmake_minimum_required(VERSION 3.20)
project(EngineApp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(engine_core
    src/engine.cpp
    include/engine/engine.hpp
)

target_include_directories(engine_core PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

target_compile_options(engine_core PRIVATE
    $<$<CXX_COMPILER_ID:GNU,Clang>:-Wall -Wextra -Wpedantic -Werror>
    $<$<CXX_COMPILER_ID:MSVC>:/W4 /WX>
)

add_executable(app_cli src/main.cpp)
target_link_libraries(app_cli PRIVATE engine_core)
```

---

## 5. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| `T* ptr = new T()` | Memory leak on early return or exception | Use `auto ptr = std::make_unique<T>()` |
| Overusing `std::shared_ptr` | Overhead of atomic reference counting & circular leaks | Default to `std::unique_ptr`; share only when true shared ownership exists |
| Catching exceptions by value: `catch (std::exception e)` | Slicing bug (drops derived type details) | Catch by const reference: `catch (const std::exception& e)` |
| Calling virtual functions in constructors/destructors | Calls base class version, not derived (dynamic dispatch not active) | Avoid virtual calls during object construction/destruction |
| Missing `[[nodiscard]]` on pure getters/creators | Callers discard results, leading to silent bugs | Mark pure queries with `[[nodiscard]]` |

---

## 6. Verification Checklist

- [ ] Zero manual `new` or `delete` operators in codebase.
- [ ] Destructors in polymorphic base classes are `virtual` (`virtual ~Base() = default;`).
- [ ] Passed `-Wall -Wextra -Wpedantic` without compiler warnings.
- [ ] Tested with AddressSanitizer (`-fsanitize=address,undefined`).
- [ ] No circular references in `std::shared_ptr` graphs (use `std::weak_ptr` for back-references).
