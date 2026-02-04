---
# ═══════════════════════════════════════════════════════════════════════════════
# SKILL: Build Systems
# Version: 3.0.0 | SASMP v1.3.0 Compliant | Production-Grade
# ═══════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# IDENTITY
# ─────────────────────────────────────────────────────────────────────────────
name: build-systems
version: "3.0.0"
description: >
  Production-grade skill for C++ build infrastructure. Covers CMake, Make, Ninja,
  package managers (Conan, vcpkg), cross-platform builds, and CI/CD integration.

# ─────────────────────────────────────────────────────────────────────────────
# COMPLIANCE
# ─────────────────────────────────────────────────────────────────────────────
sasmp_version: "1.3.0"
skill_version: "3.0.0"

# ─────────────────────────────────────────────────────────────────────────────
# BONDING
# ─────────────────────────────────────────────────────────────────────────────
bonded_agent: 04-build-engineer
bond_type: PRIMARY_BOND
category: development

# ─────────────────────────────────────────────────────────────────────────────
# PARAMETERS
# ─────────────────────────────────────────────────────────────────────────────
parameters:
  build_system:
    type: string
    required: false
    enum: [cmake, make, ninja, meson, bazel]
    default: cmake
    description: "Build system to use"
  package_manager:
    type: string
    required: false
    enum: [conan, vcpkg, cpm, fetchcontent]
    description: "Package manager for dependencies"
  target_platform:
    type: array
    required: false
    items:
      type: string
      enum: [linux, windows, macos, ios, android]
    description: "Target platforms for build"
  project_type:
    type: string
    required: false
    enum: [executable, static_library, shared_library, header_only]
    description: "Type of project output"

# ─────────────────────────────────────────────────────────────────────────────
# ERROR HANDLING
# ─────────────────────────────────────────────────────────────────────────────
error_handling:
  retry_logic:
    max_attempts: 3
    backoff: exponential
    initial_delay_ms: 1000
    max_delay_ms: 16000
    jitter: true
  fallback:
    on_build_failure: "analyze_error_output"
    on_dependency_not_found: "try_alternative_package_manager"
    on_linker_error: "check_library_paths"
    on_cmake_error: "validate_configuration"
  validation:
    check_cmake_minimum_version: true
    verify_compiler_compatibility: true
    validate_target_dependencies: true
---

# Build Systems Skill

**Production-Grade Development Skill** | C++ Build Infrastructure

Master C++ build systems, package management, and CI/CD integration.

---

## Modern CMake Patterns

### Project Structure

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.20)
project(MyProject
    VERSION 1.0.0
    DESCRIPTION "A modern C++ project"
    LANGUAGES CXX
)

# ────────────────────────────────────────────────────────────────
# Global Settings
# ────────────────────────────────────────────────────────────────
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# ────────────────────────────────────────────────────────────────
# Options
# ────────────────────────────────────────────────────────────────
option(BUILD_TESTING "Build unit tests" ON)
option(BUILD_DOCS "Build documentation" OFF)
option(ENABLE_SANITIZERS "Enable sanitizers in debug builds" ON)
option(ENABLE_COVERAGE "Enable code coverage" OFF)

# ────────────────────────────────────────────────────────────────
# Compiler Warnings Interface
# ────────────────────────────────────────────────────────────────
add_library(project_warnings INTERFACE)
target_compile_options(project_warnings INTERFACE
    $<$<CXX_COMPILER_ID:GNU,Clang>:
        -Wall -Wextra -Wpedantic -Werror
        -Wshadow -Wnon-virtual-dtor -Wcast-align
        -Wunused -Woverloaded-virtual -Wconversion
    >
    $<$<CXX_COMPILER_ID:MSVC>:
        /W4 /WX /permissive-
    >
)

# ────────────────────────────────────────────────────────────────
# Sanitizers (Debug builds)
# ────────────────────────────────────────────────────────────────
add_library(project_sanitizers INTERFACE)
if(ENABLE_SANITIZERS AND CMAKE_BUILD_TYPE STREQUAL "Debug")
    target_compile_options(project_sanitizers INTERFACE
        -fsanitize=address,undefined
        -fno-omit-frame-pointer
    )
    target_link_options(project_sanitizers INTERFACE
        -fsanitize=address,undefined
    )
endif()
```

### Target-Based CMake

```cmake
# Library target
add_library(mylib
    src/core.cpp
    src/utils.cpp
)
target_include_directories(mylib
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src
)
target_link_libraries(mylib
    PUBLIC fmt::fmt
    PRIVATE project_warnings project_sanitizers
)

# Executable target
add_executable(myapp src/main.cpp)
target_link_libraries(myapp PRIVATE mylib project_warnings)
```

---

## Dependency Management

### FetchContent (CMake 3.14+)

```cmake
include(FetchContent)

FetchContent_Declare(
    fmt
    GIT_REPOSITORY https://github.com/fmtlib/fmt.git
    GIT_TAG 10.2.1
    GIT_SHALLOW TRUE
)

FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG v1.14.0
)

FetchContent_MakeAvailable(fmt googletest)

target_link_libraries(mylib PRIVATE fmt::fmt)
target_link_libraries(mytest PRIVATE GTest::gtest_main)
```

### Conan 2.x

```python
# conanfile.py
from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout

class MyProjectConan(ConanFile):
    name = "myproject"
    version = "1.0.0"
    settings = "os", "compiler", "build_type", "arch"

    requires = [
        "fmt/10.2.1",
        "spdlog/1.13.0",
        "nlohmann_json/3.11.3"
    ]

    generators = "CMakeDeps"

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
```

```bash
# Build with Conan
conan install . --output-folder=build --build=missing
cmake -B build -DCMAKE_TOOLCHAIN_FILE=build/conan_toolchain.cmake
cmake --build build
```

### vcpkg

```json
// vcpkg.json (manifest mode)
{
    "name": "myproject",
    "version": "1.0.0",
    "dependencies": [
        "fmt",
        "spdlog",
        {
            "name": "boost-filesystem",
            "platform": "!windows"
        },
        {
            "name": "gtest",
            "features": ["gmock"]
        }
    ]
}
```

```bash
# Build with vcpkg
cmake -B build \
    -DCMAKE_TOOLCHAIN_FILE=$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake
cmake --build build
```

---

## Cross-Platform Builds

### Toolchain Files

```cmake
# toolchain/linux-clang.cmake
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_C_COMPILER clang)
set(CMAKE_CXX_COMPILER clang++)

# toolchain/windows-mingw.cmake
set(CMAKE_SYSTEM_NAME Windows)
set(CMAKE_C_COMPILER x86_64-w64-mingw32-gcc)
set(CMAKE_CXX_COMPILER x86_64-w64-mingw32-g++)
set(CMAKE_RC_COMPILER x86_64-w64-mingw32-windres)

# Usage
cmake -B build -DCMAKE_TOOLCHAIN_FILE=toolchain/linux-clang.cmake
```

### Platform-Specific Code

```cmake
# Detect platform
if(WIN32)
    target_compile_definitions(mylib PUBLIC PLATFORM_WINDOWS)
    target_sources(mylib PRIVATE src/platform/windows.cpp)
elseif(APPLE)
    target_compile_definitions(mylib PUBLIC PLATFORM_MACOS)
    target_sources(mylib PRIVATE src/platform/macos.cpp)
else()
    target_compile_definitions(mylib PUBLIC PLATFORM_LINUX)
    target_sources(mylib PRIVATE src/platform/linux.cpp)
endif()
```

---

## CI/CD Configuration

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        build_type: [Debug, Release]
        compiler:
          - { cc: gcc, cxx: g++ }
          - { cc: clang, cxx: clang++ }
        exclude:
          - os: windows-latest
            compiler: { cc: gcc, cxx: g++ }

    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive

      - name: Install dependencies (Ubuntu)
        if: runner.os == 'Linux'
        run: |
          sudo apt-get update
          sudo apt-get install -y ninja-build lcov

      - name: Configure
        run: |
          cmake -B build \
            -G Ninja \
            -DCMAKE_BUILD_TYPE=${{ matrix.build_type }} \
            -DCMAKE_C_COMPILER=${{ matrix.compiler.cc }} \
            -DCMAKE_CXX_COMPILER=${{ matrix.compiler.cxx }} \
            -DBUILD_TESTING=ON

      - name: Build
        run: cmake --build build --parallel

      - name: Test
        run: ctest --test-dir build --output-on-failure --parallel

      - name: Upload coverage
        if: matrix.build_type == 'Debug' && matrix.os == 'ubuntu-latest'
        uses: codecov/codecov-action@v3
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - deploy

variables:
  GIT_SUBMODULE_STRATEGY: recursive

.build_template: &build_template
  stage: build
  script:
    - cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=${BUILD_TYPE}
    - cmake --build build --parallel
  artifacts:
    paths:
      - build/

build:debug:
  <<: *build_template
  variables:
    BUILD_TYPE: Debug

build:release:
  <<: *build_template
  variables:
    BUILD_TYPE: Release

test:
  stage: test
  needs: [build:debug]
  script:
    - ctest --test-dir build --output-on-failure
```

---

## Compiler Flags Reference

| Purpose | GCC/Clang | MSVC |
|---------|-----------|------|
| C++20 Standard | `-std=c++20` | `/std:c++20` |
| Optimize (Release) | `-O2`, `-O3` | `/O2` |
| Debug info | `-g` | `/Zi` |
| No optimization | `-O0` | `/Od` |
| Warnings | `-Wall -Wextra` | `/W4` |
| Errors on warnings | `-Werror` | `/WX` |
| AddressSanitizer | `-fsanitize=address` | `/fsanitize=address` |
| Link-time optimization | `-flto` | `/GL`, `/LTCG` |
| Position independent | `-fPIC` | (default) |
| Native CPU | `-march=native` | `/arch:AVX2` |

---

## Build Workflow

```
┌─────────────┐    ┌──────────────┐    ┌───────────────┐
│  CONFIGURE  │───▶│    BUILD     │───▶│     TEST      │
│   (cmake)   │    │   (ninja)    │    │   (ctest)     │
└─────────────┘    └──────────────┘    └───────────────┘
       │                  │                    │
       ▼                  ▼                    ▼
┌─────────────┐    ┌──────────────┐    ┌───────────────┐
│  INSTALL    │◀───│   PACKAGE    │◀───│    DEPLOY     │
│  (targets)  │    │   (cpack)    │    │    (ci/cd)    │
└─────────────┘    └──────────────┘    └───────────────┘
```

---

## Troubleshooting Decision Tree

```
Build error?
├── CMake configuration failed
│   ├── "Could not find package" → Check CMAKE_PREFIX_PATH
│   ├── "Unknown CMake command" → Upgrade CMake version
│   └── "Compiler not found" → Install compiler or set CC/CXX
├── Compilation failed
│   ├── Missing header → Add target_include_directories
│   ├── Syntax error → Check C++ standard flag
│   └── Undefined macro → Add target_compile_definitions
├── Linking failed
│   ├── "undefined reference" → Add target_link_libraries
│   ├── "multiple definition" → Check ODR violations
│   └── "cannot find -lxxx" → Add library path
└── Runtime error
    ├── "library not found" → Check LD_LIBRARY_PATH
    └── "symbol not found" → ABI mismatch, rebuild all
```

---

## Common Build Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `undefined reference to` | Missing library link | Add `target_link_libraries` |
| `file not found` | Wrong include path | Check `target_include_directories` |
| `CMake version too low` | Old CMake | Upgrade or lower `cmake_minimum_required` |
| `ABI incompatibility` | Mixed compiler versions | Use consistent toolchain |
| `multiple definition` | Header with implementation | Use inline or move to .cpp |

---

## Unit Test Template

```cpp
#include <gtest/gtest.h>

// Test that build configuration works
TEST(BuildSystemTest, CompilerFeatures) {
    // Verify C++ standard
    #if __cplusplus >= 202002L
    SUCCEED() << "C++20 or later";
    #else
    FAIL() << "Expected C++20 or later";
    #endif
}

TEST(BuildSystemTest, PlatformMacros) {
    #if defined(PLATFORM_WINDOWS)
    EXPECT_TRUE(true) << "Windows build";
    #elif defined(PLATFORM_LINUX)
    EXPECT_TRUE(true) << "Linux build";
    #elif defined(PLATFORM_MACOS)
    EXPECT_TRUE(true) << "macOS build";
    #else
    FAIL() << "Unknown platform";
    #endif
}

TEST(BuildSystemTest, DebugRelease) {
    #ifdef NDEBUG
    EXPECT_TRUE(true) << "Release build";
    #else
    EXPECT_TRUE(true) << "Debug build";
    #endif
}
```

---

## Integration Points

| Component | Interface |
|-----------|-----------|
| `performance-optimizer` | Optimization flags |
| `cpp-debugger-agent` | Debug build config |
| `modern-cpp-expert` | C++ standard flags |
| `memory-specialist` | Sanitizer configuration |

---

*C++ Plugin v3.0.0 - Production-Grade Development Skill*
