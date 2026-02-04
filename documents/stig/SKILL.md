---
name: stig
description: Use Stig to generate documentation from C/C++ code with Doxygen-style comments
license: MIT
compatibility: opencode
metadata:
  audience: coders
---

## Purpose

Stig is a C/C++ documentation generator that parses Doxygen-style comments using tree-sitter and generates markdown/mdbook output. It provides Standardese-compatible features for advanced documentation control.

---

## Comment Formats

### Block Comments (Preferred for complex docs)

```c
/**
 * @brief Brief one-line description.
 * 
 * Detailed description spanning multiple lines.
 * Explain the purpose, behavior, and usage.
 * 
 * @param name Description of parameter
 * @return Description of return value
 */
```

### Triple-Slash (Preferred for simple docs)

```c
/// Brief description of the function.
/// @param x Description of x
/// @return Description of return
int square(int x);
```

### Inline Comments (For struct/enum members)

```c
struct Point {
    int x;  /**< X coordinate */
    int y;  ///< Y coordinate
};

enum Color {
    RED = 0,    /**< Red color */
    GREEN = 1,  ///< Green color
};
```

### Command Prefix

Both `@command` and `\command` syntax are supported:

```c
/// \brief Brief description
/// \param x The input value
/// \return The result
```

---

## Supported Tags

### Basic Tags

| Tag | Usage |
|-----|-------|
| `@brief` | Brief one-line description |
| `@param name` | Parameter documentation |
| `@return` / `@returns` | Return value documentation |
| `@see` / `@sa` | Cross-reference to related items |
| `@note` | Important note |
| `@warning` | Warning message |
| `@deprecated` | Deprecation notice |
| `@since` | Version when added |
| `@author` | Author information |
| `@version` | Version information |

### Exception & Condition Tags

| Tag | Usage |
|-----|-------|
| `@throw` / `@throws` / `@exception` | Exception documentation |
| `@pre` | Precondition |
| `@post` | Postcondition |

### Template & Return Value Tags

| Tag | Usage |
|-----|-------|
| `@tparam name` | Template parameter documentation |
| `@retval value` | Specific return value documentation |

### C++ Standard-Style Sections

| Tag | Usage |
|-----|-------|
| `@effects` | Effects of the function |
| `@requires` | Semantic preconditions |
| `@complexity` | Time/space complexity |
| `@remarks` | Additional remarks |
| `@sync` / `@threadsafety` | Thread safety information |
| `@invariant` | Class invariants |

### Code Examples

| Tag | Usage |
|-----|-------|
| `@code` / `@endcode` | Code example block |
| `@example` | Example usage |

### Entity Commands (Standardese-compatible)

| Tag | Usage |
|-----|-------|
| `@exclude` | Exclude entity from documentation |
| `@exclude return` | Hide return type (show `/* see below */`) |
| `@exclude target` | Hide alias target or enum underlying type |
| `@group name [heading]` | Group related entities together |
| `@synopsis text` | Override displayed signature |
| `@unique_name name` | Custom link target name |
| `@module name` | Logical module organization |
| `@entity target` | Remote documentation for another entity |
| `@file` | File-level documentation |
| `@output_section name` | Section header in synopsis |
| `@copydoc target` | Copy documentation from another entity |
| `@ingroup name` | Add entity to a group |
| `@defgroup name title` | Define a new group |

---

## Entity Command Examples

### Grouping Functions

```cpp
/// @group getters Getter Functions
/// @brief Gets the X coordinate
/// @return The X value
int get_x();

/// @group getters
/// @brief Gets the Y coordinate
int get_y();

/// @group setters Setter Functions
/// @brief Sets the X coordinate
/// @param x The new X value
void set_x(int x);
```

### Synopsis Override

```cpp
/// @brief Process variadic arguments
/// @synopsis void process(Args... args)
/// @tparam Args Variadic template arguments
template<typename... Args>
void process(Args&&... args);
```

### Excluding Entities

```cpp
/// @exclude
void internal_helper();  // Not in documentation

/// @exclude return
/// @brief Factory function
/// @return Implementation-defined type
auto create_widget();  // Return type shown as "/* see below */"
```

### Copying Documentation

```cpp
/// @brief Base implementation
/// @param x Input value
/// @return Processed result
int base_function(int x);

/// @copydoc base_function
/// Additional notes for this variant.
int derived_function(int x);
```

### File-Level Documentation

```cpp
/**
 * @file geometry.hpp
 * @brief Core geometry types and algorithms.
 * @author John Doe
 * @since 1.0.0
 *
 * This file provides fundamental geometry primitives.
 */
```

### Output Sections

```cpp
/// @output_section Getter Functions
int get_x();
int get_y();

/// @output_section Setter Functions  
void set_x(int x);
void set_y(int y);
```

---

## Docstring Guidelines for AI Agents

When adding docstrings to C/C++ code, follow these rules:

### 1. What to Document

- **ALL** public functions, methods, classes, structs, enums, typedefs, and macros
- **ALL** struct/enum members with inline comments
- File headers with `@file` and `@brief`
- Template parameters with `@tparam`

### 2. Comment Placement

- Place docstrings **immediately before** the declaration
- No blank lines between docstring and declaration
- Use inline comments (`/**< */` or `///<`) for struct/enum members

### 3. Required Tags

**Functions/Methods:**
```c
/**
 * @brief What the function does (one line)
 * @param name Description for each parameter
 * @return What is returned (if not void)
 */
```

**Template Functions:**
```cpp
/**
 * @brief What the function does
 * @tparam T Description of template parameter
 * @param value Description of parameter
 * @return What is returned
 */
template<typename T>
T process(T value);
```

**Classes/Structs:**
```cpp
/**
 * @brief What this type represents
 * @tparam T Template parameter description (if templated)
 */
template<typename T>
class Container { };
```

**File Headers:**
```c
/**
 * @file filename.h
 * @brief What this file contains
 * @author Author Name
 * @since 1.0.0
 */
```

### 4. Style Rules

- Start `@brief` with a verb (Computes, Returns, Creates, Initializes)
- Keep `@brief` to one line
- Add detailed description after blank line if needed
- Use `@code` blocks for usage examples on complex APIs
- Add `@see` for related functions/types
- Use `@note` for important behavior details
- Use `@warning` for dangerous operations
- Use `@deprecated` with replacement suggestion
- Use `@group` to organize related functions
- Use `@exclude` for internal helpers

### 5. Examples

**Simple function:**
```c
/// Computes the absolute value of an integer.
/// @param n Input integer
/// @return Absolute value of n
int abs_value(int n);
```

**Complex function with return values:**
```c
/**
 * @brief Searches for an element in the container.
 * 
 * @param container The container to search
 * @param value The value to find
 * @return Iterator to the element
 * @retval end() If element not found
 * @retval begin() If container is empty
 * 
 * @complexity O(n) linear search
 * @threadsafety Safe for concurrent reads
 */
iterator find(const Container& container, const T& value);
```

**Struct with members:**
```c
/**
 * @brief A rectangle defined by position and size.
 */
struct Rectangle {
    int x;      /**< X position of top-left corner */
    int y;      /**< Y position of top-left corner */
    int width;  ///< Width of the rectangle
    int height; ///< Height of the rectangle
};
```

**Template class:**
```cpp
/**
 * @brief A 2D point in Cartesian coordinates.
 * @tparam T The scalar type (float, double, int)
 * 
 * @code
 * Point2<float> p{1.0f, 2.0f};
 * @endcode
 * 
 * @see Vec2, Point3
 */
template<typename T>
class Point2 { };
```

---

## Configuration (stig.toml)

Create a `stig.toml` in your project root:

```toml
title = "My Library API"
output = "docs"
format = "mdbook"
inputs = ["include/*.h", "include/*.hpp"]
language = "en"
generate_intro = true
grouping = "by_header"  # by_header, by_prefix, or flat
authors = ["Author Name"]

# Filtering options
blacklist_namespace = ["detail", "internal", "impl"]
blacklist_pattern = ["*_impl", "test_*"]
extract_private = false
extract_protected = true

# Output customization
[output_options]
show_source_location = true
show_access_specifiers = true
code_language = "cpp"
synopsis_style = "full"  # full, compact, minimal

# Custom section names (for localization)
[section_names]
parameters = "Parameters"
returns = "Returns"
throws = "Throws"
template_parameters = "Template Parameters"

# External documentation links
[[external_docs]]
prefix = "std::"
url_template = "https://en.cppreference.com/w/cpp/$$"
```

### Configuration Options

| Option | Description |
|--------|-------------|
| `title` | Documentation title |
| `output` | Output directory (mdbook) or file (markdown) |
| `format` | `mdbook` or `markdown` |
| `inputs` | Array of glob patterns for source files |
| `generate_intro` | Generate introduction page |
| `grouping` | `by_header`, `by_prefix`, or `flat` |
| `authors` | List of authors |
| `language` | Language code (e.g., `en`) |
| `blacklist_namespace` | Namespaces to exclude (default: detail, internal, impl) |
| `blacklist_pattern` | Entity name patterns to exclude |
| `extract_private` | Include private members (default: false) |
| `extract_protected` | Include protected members (default: true) |
| `external_docs` | External documentation URL templates |

### Running Stig

```bash
# Use stig.toml in current directory
stig

# Specify config file
stig -c path/to/stig.toml

# Watch with live preview
stig --serve

# Override config with CLI
stig -f mdbook -o docs/ --title "Custom Title"
```

---

## Automatic Filtering

Stig automatically excludes entities based on configuration:

### Namespace Blacklist

By default, entities in `detail`, `internal`, and `impl` namespaces are excluded:

```cpp
namespace mylib::detail {
    void helper();  // Excluded from docs
}

namespace mylib {
    void public_api();  // Included in docs
}
```

### Pattern Blacklist

Entity names matching glob patterns are excluded:

```toml
blacklist_pattern = ["*_impl", "test_*", "internal_*"]
```

```cpp
void process_impl();     // Excluded (matches *_impl)
void test_function();    // Excluded (matches test_*)
void process();          // Included
```

### @exclude Tag

Use `@exclude` for fine-grained control:

```cpp
/// @exclude
void internal_helper();  // Excluded

/// @exclude return
auto factory();  // Included, but return type hidden
```

---

## Rules

1. Every public API element MUST have a docstring
2. Use `@brief` for the first line description
3. Document ALL parameters with `@param`
4. Document ALL template parameters with `@tparam`
5. Document return values with `@return` (unless void)
6. Use `@retval` for specific return value meanings
7. Use inline comments for struct/enum members
8. Add `@code` examples for complex APIs
9. Use `@see` to link related items
10. Mark deprecated items with `@deprecated` and suggest alternatives
11. Use `@group` to organize related functions
12. Use `@exclude` for internal implementation details
13. Use `@synopsis` to simplify complex template signatures
14. Add `@complexity` and `@threadsafety` for performance-critical code
