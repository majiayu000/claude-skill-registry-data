---
name: buck2-new-project
description: Scaffolds new Buck2 projects with proper BUILD/PACKAGE files, SPDX headers, and depot shims. Use when creating new Rust binaries/libraries, Deno tools, or C++ projects in the monorepo. Ensures consistent structure and metadata from the start.
---

# Buck2 New Project

## Overview

This skill scaffolds new Buck2 projects with all required boilerplate: BUILD files with proper `depot.*` shims, PACKAGE files with metadata, SPDX license headers, and language-specific source templates. It saves time and ensures consistency across the monorepo.

**Use this skill when:**
- Creating a new Rust binary, library, or test crate
- Setting up a new Deno/TypeScript tool under `src/tools/`
- Starting a new C++ project or library
- Adding a new component to the monorepo that needs its own BUILD file

**This skill provides:**
- Automated project scaffolding with `scripts/new_project.py`
- Language-specific templates (Rust, Deno, C++)
- Proper SPDX headers and copyright notices
- Correct use of `depot.*` shim wrappers
- PACKAGE file with metadata

## Quick Start

The fastest way to create a new project:

```bash
# Run the scaffolding script
python3 /path/to/skills/buck2-new-project/scripts/new_project.py \
  --type rust_binary \
  --name my-tool \
  --path src/tools/my-tool \
  --description "My awesome new tool" \
  --author "Your Name"

# This creates:
# - src/tools/my-tool/BUILD (with depot.rust_binary())
# - src/tools/my-tool/PACKAGE (with metadata)
# - src/tools/my-tool/src/main.rs (with SPDX headers)
```

### Supported Project Types

- `rust_binary` - Rust executable with main.rs
- `rust_library` - Rust library with lib.rs
- `deno_binary` - Deno/TypeScript tool with main.ts

## Creating Different Project Types

### Rust Binary

For standalone executables and CLI tools:

```bash
python3 scripts/new_project.py \
  --type rust_binary \
  --name quicktd \
  --path src/tools/quicktd \
  --description "Fast target determination for Buck2" \
  --author "Austin Seipp"
```

**Generated BUILD file:**
```python
load("@root//buck/shims:shims.bzl", depot = "shims")

depot.rust_binary(
    name = "quicktd",
    srcs = glob(["src/**/*.rs"]),
    deps = [
        "third-party//mimalloc:rust",
    ],
    visibility = ["PUBLIC"],
)
```

**Generated main.rs:**
```rust
// SPDX-FileCopyrightText: © 2024-2026 Austin Seipp
// SPDX-License-Identifier: Apache-2.0

fn main() {
    println!("Hello from quicktd!");
}
```

### Rust Library

For reusable code libraries:

```bash
python3 scripts/new_project.py \
  --type rust_library \
  --name common-utils \
  --path src/lib/common-utils \
  --description "Common utility functions" \
  --author "Austin Seipp"
```

**Generated BUILD file:**
```python
load("@root//buck/shims:shims.bzl", depot = "shims")

depot.rust_library(
    name = "common-utils",
    srcs = glob(["src/**/*.rs"]),
    visibility = ["PUBLIC"],
)
```

**Generated lib.rs:**
```rust
// SPDX-FileCopyrightText: © 2024-2026 Austin Seipp
// SPDX-License-Identifier: Apache-2.0

pub fn example() {
    println!("Example function");
}
```

### Deno Binary

For TypeScript-based tools:

```bash
python3 scripts/new_project.py \
  --type deno_binary \
  --name formatter \
  --path src/tools/formatter \
  --description "Code formatting tool" \
  --author "Austin Seipp"
```

**Generated BUILD file:**
```python
load("@root//buck/shims:shims.bzl", depot = "shims")
load("@toolchains//deno:defs.bzl", deno = "rules")

deno.binary(
    name = "formatter",
    main = "main.ts",
    permissions = ["read", "write"],
    visibility = ["PUBLIC"],
)
```

**Generated main.ts:**
```typescript
// SPDX-FileCopyrightText: © 2024-2026 Austin Seipp
// SPDX-License-Identifier: Apache-2.0

function main() {
  console.log("Hello from formatter!");
}

if (import.meta.main) {
  main();
}
```

## Understanding Generated Files

### BUILD File Structure

All BUILD files follow this pattern:

1. **Import shims**: `load("@root//buck/shims:shims.bzl", depot = "shims")`
2. **Use depot wrappers**: `depot.rust_binary()` NOT `rust_binary()`
3. **Set visibility**: Usually `["PUBLIC"]` for reusable components
4. **Include dependencies**: Always add `third-party//mimalloc:rust` for Rust binaries

### PACKAGE File Metadata

Generated PACKAGE files include:

```python
load("@root//buck/shims:package.bzl", pkg = "package")

pkg.info(
    copyright = ["© 2024-2026 Austin Seipp"],
    license = "Apache-2.0",
    description = "Fast target determination for Buck2",
    version = "1.0.0",
)
```

This enables:
- OSV (Open Source Vulnerability) tracking
- License compliance
- Version management
- Documentation generation

### SPDX Headers

All source files include mandatory SPDX headers:

```rust
// SPDX-FileCopyrightText: © 2024-2026 Austin Seipp
// SPDX-License-Identifier: Apache-2.0
```

These are required by monorepo policy and enable automated license tracking.

## Customizing Generated Projects

### Adding Dependencies

After generation, edit the BUILD file to add dependencies:

```python
depot.rust_binary(
    name = "my-tool",
    srcs = glob(["src/**/*.rs"]),
    deps = [
        "third-party//mimalloc:rust",
        "third-party//clap:clap",  # Add CLI argument parser
        "//src/lib/common-utils",  # Add internal library
    ],
    visibility = ["PUBLIC"],
)
```

### Setting Visibility

Control who can depend on your target:

```python
# Public - anyone can use it
visibility = ["PUBLIC"]

# Private - only this package
visibility = []

# Specific targets
visibility = ["//src/tools/...", "//src/lib/..."]
```

### Adding Tests

Extend the BUILD file with test targets:

```python
depot.rust_test(
    name = "test",
    srcs = glob(["src/**/*.rs"]),
    deps = [":my-tool"],
)
```

## Common Patterns

### Multi-Binary Project

Create a project with both a library and binary:

```bash
# Create library first
python3 scripts/new_project.py \
  --type rust_library \
  --name myapp \
  --path src/myapp

# Then manually add a binary target to BUILD:
depot.rust_binary(
    name = "myapp-cli",
    srcs = ["src/bin/main.rs"],
    deps = [":myapp", "third-party//mimalloc:rust"],
)
```

### Tool with Configuration

For tools that need config files:

```bash
# Generate base project
python3 scripts/new_project.py --type deno_binary --name tool --path src/tools/tool

# Add config.jsonc manually
echo '{"version": "1.0"}' > src/tools/tool/config.jsonc

# Update BUILD to include config:
deno.binary(
    name = "tool",
    main = "main.ts",
    data = ["config.jsonc"],
    permissions = ["read", "write"],
)
```

## Script Reference

### new_project.py Options

```
--type TYPE           Project type: rust_binary, rust_library, deno_binary
--name NAME           Target name (used in BUILD file)
--path PATH           Directory path relative to repo root
--description DESC    Brief description for PACKAGE metadata
--author AUTHOR       Copyright holder name
--license LICENSE     SPDX license ID (default: Apache-2.0)
--version VERSION     Initial version (default: 1.0.0)
--visibility VIS      Visibility list (default: ["PUBLIC"])
```

### Example Invocations

```bash
# Minimal - uses defaults
python3 scripts/new_project.py --type rust_binary --name tool --path src/tools/tool

# Full customization
python3 scripts/new_project.py \
  --type rust_library \
  --name mylib \
  --path src/lib/mylib \
  --description "My awesome library" \
  --author "Jane Doe" \
  --license "MIT" \
  --version "0.1.0" \
  --visibility '["//src/..."]'

# Deno project with specific permissions
python3 scripts/new_project.py \
  --type deno_binary \
  --name webserver \
  --path src/tools/webserver \
  --description "HTTP server tool"
```

## Troubleshooting

### "Directory already exists"

The script won't overwrite existing directories. Either:
- Choose a different path
- Remove the existing directory first
- Manually create files in the existing location

### "Invalid project type"

Ensure `--type` is one of: `rust_binary`, `rust_library`, `deno_binary`

### BUILD file doesn't work

Common issues:
- Forgot to use `depot.*` shims instead of native rules
- Missing `load("@root//buck/shims:shims.bzl", depot = "shims")`
- Incorrect visibility syntax (should be list: `["PUBLIC"]`)

Verify with:
```bash
buck2 build //path/to/project:name
```

### Tests aren't found

Tests need explicit targets in BUILD:

```python
depot.rust_test(
    name = "test",
    srcs = glob(["src/**/*.rs"]),
)
```

Then run:
```bash
buck2 test //path/to/project:test
```

## Next Steps After Scaffolding

1. **Build the project**: `buck2 build //path/to/project`
2. **Add actual implementation**: Edit the generated source files
3. **Add dependencies**: Update BUILD file with required deps
4. **Write tests**: Add test targets and test files
5. **Run tests**: `buck2 test //path/to/project:test`
6. **Commit with jj**: Follow conventional commit format

```bash
jj new -m "feat: add new project"
# Make changes...
jj describe -m "feat(myapp): add initial implementation"
jj commit
```
