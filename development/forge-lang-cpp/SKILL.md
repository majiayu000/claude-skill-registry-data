---
name: forge-lang-cpp
description: C++ development standards including make/cmake, g++/clang++, and static analysis. Use when working with C++ files (.cpp, .hpp, .cc, .hh).
---

# C++ Development

## Building

```bash
# With Make
make

# With CMake
mkdir -p build && cd build
cmake ..
make

# Direct compilation
g++ -std=c++20 -Wall -Wextra -Werror -o program main.cpp
```

## Testing

```bash
# With Makefile test target
make test

# With CTest (CMake)
cd build && ctest -V

# With Google Test
./build/tests/run_tests
```

## Static Analysis

```bash
# Cppcheck
cppcheck --enable=all --std=c++20 --error-exitcode=1 src/

# Clang-tidy
clang-tidy src/*.cpp -- -std=c++20

# Clang static analyzer
scan-build make
```

## Memory Checking

```bash
# Valgrind
valgrind --leak-check=full ./program

# AddressSanitizer
g++ -fsanitize=address -g -o program main.cpp

# UndefinedBehaviorSanitizer
g++ -fsanitize=undefined -g -o program main.cpp
```

## Formatting

```bash
# Format with clang-format
clang-format -i src/*.cpp include/*.hpp

# Check without changing
clang-format --dry-run --Werror src/*.cpp include/*.hpp
```

## Project Structure

```
project/
├── src/
│   ├── main.cpp
│   └── module.cpp
├── include/
│   └── module.hpp
├── tests/
│   └── test_module.cpp
├── CMakeLists.txt
└── README.md
```

## CMakeLists.txt Template

```cmake
cmake_minimum_required(VERSION 3.20)
project(MyProject VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_compile_options(-Wall -Wextra -Werror -pedantic)

add_executable(program src/main.cpp src/module.cpp)
target_include_directories(program PRIVATE include)

enable_testing()
add_subdirectory(tests)
```

## TDD Cycle Commands

```bash
# RED: Write test, run to see it fail
cd build && make && ctest -V

# GREEN: Implement, run to see it pass
cd build && make && ctest -V

# REFACTOR: Clean up, ensure tests still pass
cd build && make clean && cmake .. && make && ctest -V
clang-format --dry-run --Werror src/*.cpp
```
