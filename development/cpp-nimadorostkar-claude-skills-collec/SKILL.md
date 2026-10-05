---
name: cpp
description: Use when writing modern C++ (17/20/23). Covers RAII, smart-pointer ownership, move semantics, ranges, concepts, and eliminating undefined behavior with sanitizers.
metadata:
  category: languages
  version: 1.0.0
  tags: [cpp, raii, move-semantics, concepts, sanitizers]
---

# C++

## Purpose

Write C++ where resources are owned by objects, ownership is visible in the type, and undefined behavior is actively hunted with tooling rather than hoped away.

## When to Use

- Writing or reviewing C++17 and later.
- Modernizing code that uses raw `new`/`delete` or manual resource cleanup.
- Diagnosing memory corruption, leaks, or data races.
- Designing value types with correct copy/move semantics.
- Optimizing hot paths where allocation or copying dominates.

## Capabilities

- RAII and ownership modeling with `unique_ptr`, `shared_ptr`, and value semantics.
- Move semantics, the rule of zero/five, and copy elision.
- Ranges, views, and algorithm composition.
- Concepts for constrained templates and readable errors.
- Sanitizer-driven debugging: ASan, UBSan, TSan.

## Inputs

- Source, build system (CMake preferred), and target standard.
- Platform and toolchain constraints.
- Performance budget for hot paths.

## Outputs

- Code with no raw owning pointers and no manual `delete`.
- A CMake configuration with warnings-as-errors and sanitizer build types.
- Benchmarks for any change justified on performance grounds.

## Workflow

1. **Establish ownership** — Every resource has exactly one owner. Express it in the type: value, `unique_ptr`, or a documented non-owning `T*`/`span`.
2. **Apply the rule of zero** — If a class needs a destructor, it probably should not also hold business logic.
3. **Constrain templates** — Use concepts; unconstrained templates produce unreadable errors and accept nonsense.
4. **Sanitize** — Build and run the test suite under ASan+UBSan, then TSan separately.
5. **Measure before optimizing** — Profile, change one thing, benchmark again.

## Best Practices

- Prefer values and references. Reach for `shared_ptr` only when ownership is genuinely shared — it is not a default.
- Pass by `const&` for large read-only inputs; pass by value and `std::move` when you intend to store.
- Never return a reference or `string_view` to a temporary. This is the most common lifetime bug in modern C++.
- Compile with `-Wall -Wextra -Wpedantic -Werror`. Warnings in C++ are usually latent bugs.
- Use `std::span` instead of pointer+length parameter pairs.
- Mark single-argument constructors `explicit` unless implicit conversion is genuinely desired.

## Examples

**RAII wrapper with clear ownership:**

```cpp
class FileHandle {
public:
    explicit FileHandle(const std::filesystem::path& path)
        : file_(std::fopen(path.c_str(), "rb")) {
        if (!file_) {
            throw std::system_error(errno, std::generic_category(), path.string());
        }
    }

    FileHandle(FileHandle&&) noexcept = default;
    FileHandle& operator=(FileHandle&&) noexcept = default;
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;

    ~FileHandle() { if (file_) std::fclose(file_); }

    [[nodiscard]] std::FILE* get() const noexcept { return file_; }

private:
    std::FILE* file_;
};
```

**Constrained template with concepts:**

```cpp
template <std::ranges::input_range R>
    requires std::totally_ordered<std::ranges::range_value_t<R>>
auto median(R&& range) {
    std::vector values(std::ranges::begin(range), std::ranges::end(range));
    if (values.empty()) throw std::invalid_argument("median of empty range");
    auto mid = values.begin() + std::ssize(values) / 2;
    std::ranges::nth_element(values, mid);
    return *mid;
}
```

## Notes

- ASan and TSan cannot be combined in a single build. Run them as separate CI jobs.
- Copy elision is guaranteed for prvalues since C++17 — returning a local by value costs nothing.
- `shared_ptr` cycles leak. Break them with `weak_ptr` on the back-reference.
