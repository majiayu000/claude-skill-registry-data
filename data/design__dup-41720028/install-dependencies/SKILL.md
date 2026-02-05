---
name: install-dependencies
description: Use when adding project dependencies. Defines dependency management rules and language-specific patterns.
---

# Install Dependencies

## Philosophy

**Core Principle**: Let package managers handle version resolution automatically. Never specify version numbers unless absolutely necessary.

## Why This Approach

1. **Package managers are smarter**: Modern package managers (uv, npm, cargo) resolve compatible versions automatically
2. **Avoid version conflicts**: Manual version specifications often create dependency hell
3. **Get latest features**: Always use the newest compatible versions
4. **Simpler maintenance**: No need to manually track and update versions
5. **Trust the ecosystem**: Package managers understand semver and compatibility better than manual pinning

## Universal Rules

### ✅ DO:
- Add dependency names without version numbers
- Let the package manager resolve versions
- Trust the lock file (package-lock.json, Cargo.lock, uv.lock)
- Update dependencies regularly through the package manager

### ❌ DON'T:
- Specify version numbers (>=, ^, ~, =)
- Manually pin versions without good reason
- Override package manager decisions
- Commit version specifications to dependency files

## Exception Case

The ONLY time to specify a version is when there's a **known breaking change** or **compatibility issue** that requires pinning to a specific version.

**Requirements for version pinning:**
- Must be documented with a comment explaining why
- Must be treated as temporary until the issue is resolved
- Should include link to issue/ticket tracking the problem

**Example:**
```toml
dependencies = [
    "problematic-lib",  # Pinned to v1.2.3 due to breaking change in v1.3.0 (see issue #123)
]
```

## Language-Specific Details

For language-specific syntax and examples:
- Python: See [PYTHON.md](PYTHON.md)
- TypeScript/JavaScript: See [TYPESCRIPT.md](TYPESCRIPT.md)
- Rust: See [RUST.md](RUST.md)

## Workflow

1. **Add dependency**: Add dependency name only (no version)
2. **Let package manager resolve**: Run the appropriate install/sync command
3. **Verify**: Check that dependency was resolved and installed
4. **Commit lock file**: Always commit the updated lock file
