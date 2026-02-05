---
name: compiler-explorer
description: Optimize functions by generating and analyzing compiler assembly output. Use when asked to optimize a function, analyze generated assembly, or improve performance by examining what the compiler produces.
---

# Compiler Explorer

Optimize functions by analyzing compiler-generated assembly. This replicates the workflow of godbolt.org locally.

## Workflow

### 1. Isolate the Function

Create a standalone file with the function to optimize. Export it to prevent inlining:

```zig
export fn targetFunction(x: i64) i64 {
    // function body
}
```

```c
__attribute__((noinline)) int targetFunction(int x) {
    // function body
}
```

### 2. Generate Assembly

```bash
# Zig
zig build-obj src/target.zig -femit-asm -fno-emit-bin -O ReleaseFast

# C/C++ (clang)
clang -S -O3 -fno-inline -o target.s target.c

# Rust
rustc --emit=asm -C opt-level=3 target.rs
```

### 3. Locate and Read the Function

```bash
# Find the assembly file
find . -name "*.s" -newer src/target.zig

# Find function boundaries
grep -n "_targetFunction" output.s

# Count instructions
sed -n 'START,ENDp' output.s | grep -E '^\s+\w' | wc -l
```

### 4. Analyze and Iterate

Read through the assembly looking for:
- Unexpected instructions (type conversions, bounds checks, function calls)
- Repeated patterns that could be simplified
- Instructions that don't map to obvious source operations

Make a targeted change, regenerate assembly, compare instruction counts.

### 5. Benchmark

Always benchmark—fewer instructions ≠ always faster:

```bash
zig build-exe bench.zig -O ReleaseFast -o bench_v1
time ./bench_v1
```

Keep assembly outputs for comparison: `function_v1.s`, `function_v2.s`, etc.
