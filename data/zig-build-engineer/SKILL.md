---
name: zig-build-engineer
description: Expert guidance for Zig build system engineering. Use when working with build.zig files, including creating new build configurations, adding executables/libraries/tests, managing dependencies and modules, setting up cross-compilation, configuring build options, troubleshooting build issues, or any other Zig build system tasks. Provides patterns, API references, and best practices for the Zig build system's DAG-based architecture.
---

# Zig Build Engineer

Expert guidance for working with the Zig build system.

## Quick Start

The Zig build system uses `build.zig` to define a directed acyclic graph (DAG) of build steps. The most common pattern:

```zig
const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const exe = b.addExecutable(.{
        .name = "my-app",
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });

    b.installArtifact(exe);

    const run_cmd = b.addRunArtifact(exe);
    run_cmd.step.dependOn(b.getInstallStep());
    if (b.args) |args| run_cmd.addArgs(args);

    const run_step = b.step("run", "Run the app");
    run_step.dependOn(&run_cmd.step);
}
```

## Core Workflow

1. **Understand requirements** - Determine what artifacts need to be built (executables, libraries, tests)
2. **Set up standard options** - Use `standardTargetOptions()` and `standardOptimizeOption()`
3. **Create artifacts** - Use `addExecutable()`, `addLibrary()`, or `addTest()`
4. **Configure artifacts** - Add dependencies, modules, link libraries
5. **Set up steps** - Create install, run, and test steps
6. **Handle dependencies** - Configure imports and linking as needed

## Common Tasks

### Creating a New build.zig

For most projects, start with the minimal executable pattern from Quick Start. For libraries, replace `addExecutable` with `addLibrary`.

### Adding Tests

```zig
const unit_tests = b.addTest(.{
    .root_source_file = b.path("src/main.zig"),
    .target = target,
    .optimize = optimize,
});

const run_tests = b.addRunArtifact(unit_tests);
const test_step = b.step("test", "Run unit tests");
test_step.dependOn(&run_tests.step);
```

### Adding Dependencies

In `build.zig.zon`:
```zig
.dependencies = .{
    .mylib = .{
        .url = "https://github.com/user/mylib/archive/v1.0.0.tar.gz",
        .hash = "...",
    },
},
```

In `build.zig`:
```zig
const dep = b.dependency("mylib", .{
    .target = target,
    .optimize = optimize,
});
exe.root_module.addImport("mylib", dep.module("mylib"));
```

### Creating Modules

```zig
// Public module (exported to packages that depend on this)
const my_module = b.addModule("my-module", .{
    .root_source_file = b.path("src/module.zig"),
});

// Use in executable
exe.root_module.addImport("my-module", my_module);
```

### Linking C Libraries

```zig
exe.linkLibC();
exe.linkSystemLibrary("sqlite3");
exe.addIncludePath(b.path("include"));
```

### Custom Build Options

```zig
const enable_feature = b.option(bool, "feature", "Enable feature") orelse false;

const options = b.addOptions();
options.addOption(bool, "feature_enabled", enable_feature);
exe.root_module.addOptions("config", options);
```

Users can then run: `zig build -Dfeature`

## Key Concepts

### The DAG Model

All build operations are steps in a directed acyclic graph. Steps declare dependencies, and the build system executes them in parallel when possible.

```zig
step_a.dependOn(&step_b.step);
step_b.dependOn(&step_c.step);
// Execution order: step_c → step_b → step_a
```

### LazyPath

Represents paths that may not exist yet (e.g., generated files). Always use `b.path()` for source files and `addOutputFileArg()` for generated files.

### Install Step

By default, `b.getInstallStep()` is the main target. Most artifacts get added to it via `b.installArtifact(exe)`.

## Reference Documentation

When working on specific tasks, consult these references:

- **Core concepts and architecture**: See [references/build-system-concepts.md](references/build-system-concepts.md)
  - DAG model, step types, module system, dependency management
  - File generation patterns, testing strategies, best practices

- **Template examples**: See [references/common-patterns.md](references/common-patterns.md)
  - Minimal executable, library, tests
  - Multi-module projects, dependencies, cross-compilation
  - Code generation, custom options, multiple artifacts

- **API reference**: See [references/api-quick-reference.md](references/api-quick-reference.md)
  - Build instance methods, compilation artifacts, run steps
  - LazyPath, Options step, WriteFile step, Module APIs

## Best Practices

1. **Always use `b.path()` for source files** - Never hardcode paths
2. **Use standard options** - `standardTargetOptions()` and `standardOptimizeOption()` for consistency
3. **Separate test compilation from execution** - Create test artifact, then run it in a separate step
4. **Keep generated files ephemeral** - Don't commit build outputs to version control
5. **Use LazyPath correctly** - `b.path()` for source, `addOutputFileArg()` for generated
6. **Leverage the Options step** - For compile-time configuration instead of environment variables
7. **Structure dependencies properly** - Use `dependOn()` to establish correct build order

## Troubleshooting

**Build not finding source files**: Use `b.path("relative/to/build.zig")` instead of hardcoded paths

**Module not found**: Ensure `addImport()` is called before the artifact is built

**Dependency issues**: Check that dependency options match (target, optimize) and that module names are correct

**Cross-compilation fails**: Verify target is properly configured and required system libraries are available for that target

**Tests not running**: Ensure run step depends on test artifact: `run_tests = b.addRunArtifact(tests)`

## Running Builds

```bash
zig build                    # Build and install (default: install step)
zig build run                # Build and run (if run step exists)
zig build test               # Run tests (if test step exists)
zig build -Doptimize=ReleaseFast  # Build with optimization
zig build -Dtarget=x86_64-windows # Cross-compile
zig build --help             # Show all available options and steps
```
