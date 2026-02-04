---
name: hackage-read-docs
description: Retrieve documentation from Hackage. Use this Skill when you need a reference for Haskell packages, classes, or want to query package versions. (project)
---

# Hackage Read Docs

A CLI tool to query Hackage package documentation with filtering and display options.

## Instructions
1. use `bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- <package_name> --list-versions` to discover what package versions are there
2. then use `bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- <package_name> --version <version>` to discover the modules that are in the package
3. If the hackage tool isn't finding modules, then use web fetch to https://hackage.haskell.org/package/<package_name> to discover directly the modules
4. And follow up with one of:
   - bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- <package_name> --module <module> --filter-functions --with-comments --version <version>
   - bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- <package_name> --module <module> --filter-types --with-comments --version <version>
   - bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- <package_name> --module <module> --filter-classes --with-comments --version <version>

## Quick Start

### List all available versions
```bash
bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- aeson --list-versions
```

### Query a specific version (shows tree view)
```bash
bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- aeson --version 2.2.3.0
```

### Deep dive into a module
```bash
bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- aeson --module Data.Aeson
```

## Filter Options

Show only specific types of exports:

```bash
# Show only functions
bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- aeson --module Data.Aeson --filter-functions

# Show only types
bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- aeson --module Data.Aeson --filter-types

# Show only type classes
bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- aeson --module Data.Aeson --filter-classes

# Combine filters (e.g., show functions and types, exclude classes)
bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- aeson --module Data.Aeson --filter-functions --filter-types
```

## Documentation Display

Include Haddock documentation text alongside signatures:

```bash
# Show functions with their documentation
bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- aeson --module Data.Aeson --filter-functions --with-comments

# Show types with their documentation
bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- aeson --module Data.Aeson --filter-types --with-comments

# Show type classes with their documentation
bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- aeson --module Data.Aeson --filter-classes --with-comments
```

## Common Patterns

### Research a specific function
```bash
# Find a function and see its documentation
bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- aeson --module Data.Aeson --filter-functions --with-comments | grep -A 3 "decode"
```

### Explore all types in a module
```bash
# See all type definitions with documentation
bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- containers --module Data.Map --filter-types --with-comments
```

### Find available type classes
```bash
# List type classes with their documentation
bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- aeson --module Data.Aeson --filter-classes --with-comments
```

## Workflow

1. **Start with version listing**: Always list versions first, pick the latest if unclear
   ```bash
   bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- PACKAGE --list-versions
   ```

2. **Query package tree**: View the package structure and available modules
   ```bash
   bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- PACKAGE --version X.Y.Z
   ```

3. **Explore specific module**: Deep dive into a module with filters as needed
   ```bash
   bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- PACKAGE --module MODULE.NAME
   ```

4. **Apply filters**: Use `--filter-*` flags to focus on specific export types

5. **Include documentation**: Add `--with-comments` to see Haddock documentation

## Available Flags

- `--version, -v VERSION`: Query specific package version
- `--list-versions, -l`: List all available versions
- `--module, -m MODULE`: Query specific module (e.g., Data.Aeson)
- `--filter-functions`: Show only exported functions
- `--filter-types`: Show only exported types
- `--filter-classes`: Show only exported type classes
- `--with-comments`: Include Haddock documentation text alongside signatures

## Examples

```bash
# Research the aeson package's FromJSON class
bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- aeson --module Data.Aeson --filter-classes --with-comments | grep -A 10 "FromJSON"

# Find all functions in Data.List
bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- base --module Data.List --filter-functions

# Explore container types with documentation
bazel run //haskell/app/hackage-doc-cli:hackage-doc-cli -- containers --module Data.Map --filter-types --with-comments
```

## Notes

- Default behavior (no filters): Shows functions, types, and type classes
- Documentation is extracted from Haddock HTML pages
- Supports both PVP and Semantic Versioning formats
- Results are cached for performance (24h for metadata, 7d for versions)