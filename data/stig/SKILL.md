---
name: stig
description: Use Stig to generate documentation from C/C++ code with Doxygen-style comments
license: MIT
compatibility: opencode
metadata:
  audience: coders
---

## Purpose

Stig is a modern C/C++ documentation generator that parses Doxygen-style comments using tree-sitter and generates markdown/mdbook/JSON/HTML output. It provides Standardese-compatible features for advanced documentation control, cross-references, coverage reporting, and CI/CD integration.

**Key Features:**
- 🚀 Fast tree-sitter parsing (no libclang)
- 📚 Multiple output formats (markdown, mdbook, JSON, HTML)
- 🔗 Smart cross-references with `@ref` tags
- 📊 Coverage reports and linting
- 👀 Watch mode with live preview
- 🔧 CMake and GitHub Actions integration
- 🌐 Compiler Explorer (Godbolt) links

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
| `@details` | Detailed description |
| `@param name` | Parameter documentation |
| `@return` / `@returns` | Return value documentation |
| `@see` / `@sa` | Cross-reference to related items |
| `@note` | Important note |
| `@warning` | Warning message |
| `@attention` | Attention notice |
| `@important` | Important information |
| `@deprecated` | Deprecation notice |
| `@since` | Version when added |
| `@author` | Author information |
| `@version` | Version information |
| `@date` | Date information |
| `@copyright` | Copyright notice |

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

### Code Examples & Snippets

| Tag | Usage |
|-----|-------|
| `@code` / `@endcode` | Code example block |
| `@example` | Example usage |
| `@snippet file anchor` | Include external code snippet |

### Cross-References & Links

| Tag | Usage |
|-----|-------|
| `@ref target` | Cross-reference to symbol/page |
| `@ref target "text"` | Cross-reference with custom display text |

### Diagrams

| Tag | Usage |
|-----|-------|
| `@mermaid` / `@endmermaid` | Embed Mermaid diagram |

### Testing & Tracking

| Tag | Usage |
|-----|-------|
| `@test name` | Link to test case |
| `@todo` | TODO item (generates TODO.md) |
| `@bug` | Bug report (generates BUGS.md) |

### Entity Commands (Standardese-compatible)

| Tag | Usage |
|-----|-------|
| `@exclude` | Exclude entity from documentation |
| `@exclude return` | Hide return type (show `/* see below */`) |
| `@exclude target` | Hide alias target or enum underlying type |
| `@group name [heading]` | Group related entities together |
| `@synopsis text` | Override displayed signature |
| `@unique_name name` | Custom link target name for overloads |
| `@module name` | Logical module organization |
| `@entity target` | Remote documentation for another entity |
| `@file` | File-level documentation |
| `@output_section name` | Section header in synopsis |
| `@copydoc target` | Copy documentation from another entity |
| `@ingroup name` | Add entity to a group |
| `@defgroup name title` | Define a new group |
| `@page id title` | Create custom documentation page |
| `@mainpage title` | Create main page |

---

## Advanced Features

### Cross-References

Use `@ref` to create links to other symbols or pages:

```cpp
/**
 * @brief Processes a point
 * @param p A @ref Point to process
 * @return See @ref Result for details
 * 
 * This function uses @ref Point::transform() internally.
 * For more info, see @ref geometry_page "the geometry guide".
 */
Result process(Point p);
```

Generates: `[Point](#point)`, `[the geometry guide](geometry_page.md)`

### External Code Snippets

Include code from external files:

```cpp
/**
 * @brief Example usage
 * @snippet examples/basic.cpp basic_usage
 */
void example();
```

In `examples/basic.cpp`:
```cpp
//! [basic_usage]
Point p{10, 20};
p.transform(Matrix::identity());
//! [basic_usage]
```

### Custom Pages

Create standalone documentation pages:

```cpp
/**
 * @page getting_started Getting Started Guide
 * 
 * ## Installation
 * 
 * Download and install the library...
 * 
 * ## Basic Usage
 * 
 * See @ref Point and @ref Transform for core types.
 */
```

### TODO/Bug Tracking

Track issues directly in code:

```cpp
/// @brief Process data
/// @todo Optimize for large datasets
/// @bug Crashes with empty input (issue #123)
void process(const Data& data);
```

Generates separate `TODO.md` and `BUGS.md` pages.

### Test References

Link to test cases:

```cpp
/**
 * @brief Validates input
 * @test test_validate_basic
 * @test test_validate_edge_cases
 */
bool validate(const Input& input);
```

Generates `TESTS.md` with links to test files.

### Mermaid Diagrams

Embed diagrams directly in documentation:

```cpp
/**
 * @brief State machine implementation
 * 
 * @mermaid
 * stateDiagram-v2
 *     [*] --> Idle
 *     Idle --> Processing
 *     Processing --> Done
 *     Done --> [*]
 * @endmermaid
 */
class StateMachine { };
```

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
- Add `@see` or `@ref` for related functions/types
- Use `@note` for important behavior details
- Use `@warning` for dangerous operations
- Use `@deprecated` with replacement suggestion
- Use `@group` to organize related functions
- Use `@exclude` for internal helpers
- Use `@ref` for cross-references instead of plain text

### 5. Examples

**Simple function:**
```c
/// Computes the absolute value of an integer.
/// @param n Input integer
/// @return Absolute value of n
int abs_value(int n);
```

**Complex function with cross-references:**
```c
/**
 * @brief Searches for an element in the container.
 * 
 * Uses binary search algorithm. See @ref sort() for sorting requirements.
 * 
 * @param container The @ref Container to search
 * @param value The value to find
 * @return Iterator to the element
 * @retval end() If element not found
 * @retval begin() If container is empty
 * 
 * @complexity O(log n) binary search
 * @threadsafety Safe for concurrent reads
 * @see sort, find_if
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

**Template class with example:**
```cpp
/**
 * @brief A 2D point in Cartesian coordinates.
 * @tparam T The scalar type (float, double, int)
 * 
 * @code{.cpp}
 * Point2<float> p{1.0f, 2.0f};
 * auto dist = p.distance(Point2<float>{3.0f, 4.0f});
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
format = "mdbook"  # markdown, mdbook, json, html
inputs = ["include/*.h", "include/*.hpp"]
language = "en"
generate_intro = true
grouping = "by_module"  # by_header, by_prefix, by_module, or flat
authors = ["Author Name"]

# Filtering options
blacklist_namespace = ["detail", "internal", "impl"]
blacklist_pattern = ["*_impl", "test_*"]
extract_private = false
extract_protected = true

# Output customization
[output]
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

# Coverage options
[coverage]
min_coverage = 80
require_param_docs = true
require_return_docs = true

# Module organization
[[modules]]
name = "Core"
patterns = ["include/core/*.hpp"]
title = "Core Components"

[[modules]]
name = "Utils"
patterns = ["include/util/*.hpp"]
title = "Utility Functions"
```

### Configuration Options

| Option | Description |
|--------|-------------|
| `title` | Documentation title |
| `output` | Output directory (mdbook) or file (markdown) |
| `format` | `markdown`, `mdbook`, `json`, or `html` |
| `inputs` | Array of glob patterns for source files |
| `generate_intro` | Generate introduction page |
| `grouping` | `by_header`, `by_prefix`, `by_module`, or `flat` |
| `authors` | List of authors |
| `language` | Language code (e.g., `en`) |
| `blacklist_namespace` | Namespaces to exclude (default: detail, internal, impl) |
| `blacklist_pattern` | Entity name patterns to exclude |
| `extract_private` | Include private members (default: false) |
| `extract_protected` | Include protected members (default: true) |
| `external_docs` | External documentation URL templates |

### Running Stig

```bash
# Use stig.toml in current directory (generate is default)
stig

# Specify config file
stig -c path/to/stig.toml

# Generate specific format
stig generate -f mdbook -o docs/ --title "My API"

# Watch with live preview
stig generate --serve

# Check documentation (human-readable report)
stig check include/*.h

# Check with CI/CD-friendly output (file:line:col: severity: message)
stig check -f compiler include/*.h

# Check with minimum coverage threshold
stig check --min-coverage 80 include/*.h

# Check with strict mode (warnings as errors)
stig check --strict include/*.h

# Override config with CLI
stig generate -f mdbook -o docs/ --title "Custom Title"
```

---

## CLI Reference

```
stig <COMMAND> [OPTIONS] <INPUT_FILES>...

COMMANDS:
    generate        Generate documentation (default if no subcommand)
    check           Check documentation coverage and quality
    preprocessor    Run as mdbook preprocessor
    help            Show help message
    version         Show version information

GENERATE OPTIONS:
    -o, --output <PATH>    Output file or directory (default: stdout)
    -f, --format <FMT>     Output format: markdown, mdbook, json, html
    --title <TITLE>        Book title (for mdbook/html format)
    -c, --config <FILE>    Config file path (default: stig.toml)
    -w, --watch            Watch for file changes and regenerate
    --serve                Watch mode + spawn mdbook serve for live preview
    --force                Force full rebuild, ignore cache
    -h, --help             Show help message

CHECK OPTIONS:
    -c, --config <FILE>    Config file path (default: stig.toml)
    -f, --format <FMT>     Output format: human, compiler, json
    --min-coverage <N>     Minimum coverage percentage (0-100)
    --strict               Treat warnings as errors
    -h, --help             Show help message

GLOBAL OPTIONS:
    -h, --help             Show help (use 'stig <command> --help' for details)
    -v, --version          Show version information
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

## Documentation Checking

The `stig check` command combines coverage analysis and linting into a single command with multiple output formats, designed for CI/CD integration.

### Human-Readable Report (default)

```bash
stig check include/*.h
```

Output:
```
Documentation Coverage Report
=============================
Overall: 85% (42/50 entities documented)

By Type:
  Functions:    90% (27/30) [3 missing params, 2 missing returns]
  Classes:      80% (8/10)

Missing Documentation:
  include/api.h:
    - process() [line 42] - missing @param for 'flags'
    - validate() [line 58] - missing @return
```

### Compiler-Style Output (for CI/CD)

```bash
stig check -f compiler include/*.h
```

Output (compatible with most IDEs and CI tools):
```
include/api.h:42:1: warning: missing @param for 'flags' 'process' (function)
include/api.h:58:1: warning: missing @return 'validate' (function)
include/api.h:75:1: warning: no documentation 'helper' (function)

stig: 3 documentation issue(s) found
stig: coverage 85% (42/50 entities documented)
```

### JSON Output (for tooling)

```bash
stig check -f json include/*.h
```

### Additional Options

```bash
# Set minimum coverage threshold (exit code 2 if below)
stig check --min-coverage 80 include/*.h

# Treat warnings as errors (exit code 2 if warnings found)
stig check --strict include/*.h
```

### Exit Codes

- `0` - All checks passed
- `1` - Errors found (invalid references, etc.)
- `2` - Warnings found (with `--strict`) or coverage below threshold

### What It Checks

- Missing `@brief` descriptions
- Undocumented parameters (`@param`)
- Missing return documentation (`@return`)
- Undocumented template parameters (`@tparam`)
- Broken cross-references (`@see`, `@copydoc`)
- Brief description length

---

## Integration

### CMake

```cmake
find_package(Stig REQUIRED)

stig_add_docs(
    TARGET my_docs
    SOURCES include/*.hpp
    OUTPUT docs
    FORMAT mdbook
    TITLE "My Library API"
)
```

See `cmake/README.md` for details.

### GitHub Actions

```yaml
- name: Generate Documentation
  uses: ./.github/actions/stig-docs
  with:
    input: 'include/*.hpp'
    output: 'docs'
    format: 'mdbook'
    coverage: 'true'
```

See `.github/actions/stig-docs/README.md` for details.

### mdbook Preprocessor

Add to `book.toml`:
```toml
[preprocessor.stig]
command = "stig preprocessor"
```

Use in markdown:
```markdown
{{#stig api ../include/mylib.h}}
{{#stig function my_function}}
```

---

## Rules for AI Agents

1. Every public API element MUST have a docstring
2. Use `@brief` for the first line description (start with a verb)
3. Document ALL parameters with `@param`
4. Document ALL template parameters with `@tparam`
5. Document return values with `@return` (unless void)
6. Use `@retval` for specific return value meanings
7. Use inline comments for struct/enum members
8. Add `@code` examples for complex APIs
9. Use `@ref` to link related items (not plain text)
10. Mark deprecated items with `@deprecated` and suggest alternatives
11. Use `@group` to organize related functions
12. Use `@exclude` for internal implementation details
13. Use `@synopsis` to simplify complex template signatures
14. Add `@complexity` and `@threadsafety` for performance-critical code
15. Use `@test` to link to test cases
16. Use `@todo` and `@bug` for tracking issues
17. Use `@snippet` for external code examples
18. Create `@page` for conceptual documentation
19. Add `@mermaid` diagrams for complex relationships
20. Use `@copydoc` to avoid documentation duplication
