---
name: developing-bazel-rules
description: Use when creating custom Bazel rules, toolchains, providers, or aspects. Use when extending Bazel for new languages, build systems, or custom actions. Use when debugging Starlark rule implementations or understanding Bazel build phases.
---

# Developing Bazel Rules

## Overview

Bazel rules define how to transform inputs into outputs through actions. A rule has an implementation function executed during analysis phase that registers actions for execution phase.

**Core principle:** Rules don't execute commands directly - they register actions that Bazel executes later based on dependency analysis.

## When to Use

- Creating rules for new languages or tools
- Building custom toolchains
- Implementing providers for dependency propagation
- Creating aspects for cross-cutting concerns
- Wrapping existing tools with Bazel

## Build Phases

| Phase | What Happens | Rule Author's Role |
|-------|--------------|-------------------|
| **Loading** | `BUILD` files evaluated, rules instantiated | Define rule with `rule()`, macros expand |
| **Analysis** | Implementation functions run | Register actions, return providers |
| **Execution** | Actions run (if needed) | Actions produce outputs |

## Quick Start: Minimal Rule

```python
# my_rules.bzl
def _my_compile_impl(ctx):
    output = ctx.actions.declare_file(ctx.label.name + ".out")
    ctx.actions.run(
        mnemonic = "MyCompile",
        executable = ctx.executable._compiler,
        arguments = ["-o", output.path] + [f.path for f in ctx.files.srcs],
        inputs = ctx.files.srcs,
        outputs = [output],
    )
    return [DefaultInfo(files = depset([output]))]

my_compile = rule(
    implementation = _my_compile_impl,
    attrs = {
        "srcs": attr.label_list(allow_files = True),
        "_compiler": attr.label(
            default = "//tools:compiler",
            executable = True,
            cfg = "exec",
        ),
    },
)
```

## Core Concepts

### Providers - Passing Data Between Rules

Providers are the mechanism for rules to communicate:

```python
MyInfo = provider(
    doc = "Information from my_library targets",
    fields = {
        "files": "depset of output files",
        "transitive_files": "depset of all transitive files",
    },
)

def _impl(ctx):
    # Collect from dependencies
    transitive = [dep[MyInfo].transitive_files for dep in ctx.attr.deps]

    # Return new provider
    return [
        DefaultInfo(files = depset([output])),
        MyInfo(
            files = depset([output]),
            transitive_files = depset([output], transitive = transitive),
        ),
    ]
```

**Require providers in deps:**
```python
"deps": attr.label_list(providers = [MyInfo])
```

### Depsets - Efficient Transitive Collections

Use depsets to avoid quadratic complexity:

```python
# GOOD: O(1) per target
transitive_srcs = depset(
    direct = ctx.files.srcs,
    transitive = [dep[MyInfo].srcs for dep in ctx.attr.deps],
)

# BAD: O(n) copying - becomes O(n^2) across graph
transitive_srcs = list(ctx.files.srcs)
for dep in ctx.attr.deps:
    transitive_srcs.extend(dep[MyInfo].srcs.to_list())
```

**Only call `.to_list()` in binary rules, never in libraries.**

### Actions - Registering Work

```python
# Run executable (preferred)
ctx.actions.run(
    mnemonic = "Compile",
    executable = ctx.executable._tool,
    arguments = [args],
    inputs = inputs,
    outputs = [output],
)

# Use args builder for large inputs
args = ctx.actions.args()
args.add("-o", output)
args.add_all(srcs)  # Deferred expansion - efficient!

# Write file content
ctx.actions.write(output, content, is_executable = True)
```

### Attributes - Rule Parameters

| Type | Use Case |
|------|----------|
| `attr.label_list` | File/target inputs (`srcs`, `deps`) |
| `attr.label` | Single target (`_compiler`) |
| `attr.string` | Config value (`importpath`) |
| `attr.bool` | Toggle (`cgo = True`) |

**Private attributes** (underscore prefix) for implicit deps:
```python
"_stdlib": attr.label(default = "//go:stdlib")
```

**cfg for tools:**
```python
"_compiler": attr.label(executable = True, cfg = "exec")
```

## Implementation Checklist

1. Get toolchain (if using): `ctx.toolchains["//my:type"]`
2. Access inputs: `ctx.files.srcs`, `ctx.attr.deps`
3. Declare outputs: `ctx.actions.declare_file()`
4. Build depsets for transitive data
5. Register actions: `ctx.actions.run()`
6. Return providers: `[DefaultInfo(...), MyInfo(...)]`

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Flattening depsets in library | Keep as depset, flatten only in binary |
| Missing `cfg = "exec"` for tools | Add `cfg = "exec"` to tool attributes |
| Not returning DefaultInfo | Always return DefaultInfo with files |
| Reading files in analysis | Files can only be read by actions |
| Action without outputs | All actions must produce output files |

## Reference Files

See `references/` for detailed guides:
- `api-reference.md` - Starlark API quick reference
- `providers.md` - Provider design patterns
- `toolchains.md` - Toolchain development
- `testing.md` - Testing Bazel rules
- `go-patterns.md` - Patterns from rules_go
