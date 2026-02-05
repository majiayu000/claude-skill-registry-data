---
name: debug-haskell-bazel-targets
description: Diagnose and fix common Haskell Bazel build errors, especially dependency visibility issues
tags: [haskell, bazel, debugging, dependencies]
---

# Debug Haskell Bazel Targets

This skill helps diagnose and fix common Haskell Bazel build errors, particularly dependency visibility and configuration issues.

## Common Error Pattern: Dependency Visibility

### Symptom
```
ERROR: in _haskell_test rule //path/to:target: target '@@rules_haskell~~stack_snapshot~stackage//:base' is not visible from target '//path/to:target'
```

### Root Cause
Core Haskell packages (base, bytestring, containers, directory, filepath, text, time, etc.) should NOT be imported from `@stackage//`. They are part of the GHC distribution and must be referenced directly.

### Solution Pattern

**WRONG:**
```starlark
haskell_test(
    name = "unit-tests",
    srcs = glob(["test/**/*.hs"]),
    deps = [
        ":rpg-ruleset-core",
        "@stackage//:QuickCheck",
        "@stackage//:base",        # L WRONG
        "@stackage//:hspec",
        "@stackage//:text",        # L WRONG
    ],
)
```

**CORRECT:**
```starlark
haskell_test(
    name = "unit-tests",
    srcs = glob(["test/**/*.hs"]),
    deps = [
        ":rpg-ruleset-core",
        "//:base",                 #  CORRECT
        "//:text",                 #  CORRECT
        "@stackage//:QuickCheck",  #  Third-party packages use @stackage//
        "@stackage//:hspec",
    ],
)
```

## Core vs Third-Party Dependencies

### Core GHC Packages (use `//:package-name`)
- `//:base`
- `//:bytestring`
- `//:containers`
- `//:directory`
- `//:filepath`
- `//:text`
- `//:time`
- `//:array`
- `//:deepseq`
- `//:process`
- `//:mtl`
- `//:transformers`

### Third-Party Packages (use `@stackage//:package-name`)
- `@stackage//:aeson`
- `@stackage//:yaml`
- `@stackage//:cmark`
- `@stackage//:QuickCheck`
- `@stackage//:hspec`
- `@stackage//:http-conduit`
- `@stackage//:optparse-applicative`
- Any package not bundled with GHC

## Debugging Workflow

When encountering build errors:

1. **Identify the error type**
   - Visibility errors � Check dependency prefixes (`//:` vs `@stackage//`)
   - Missing dependencies � Check if package is in MODULE.bazel
   - Compilation errors � Check Haskell syntax and imports

2. **For visibility errors:**
   ```bash
   # Check which dependencies are causing issues
   grep -r "@stackage//:base" haskell/
   grep -r "@stackage//:text" haskell/
   grep -r "@stackage//:containers" haskell/
   ```

3. **Fix all BUILD.bazel files:**
   - Replace `@stackage//:base` � `//:base`
   - Replace `@stackage//:text` � `//:text`
   - Replace `@stackage//:containers` � `//:containers`
   - Keep `@stackage//` for third-party packages

4. **Verify consistency across library and test targets:**
   - `haskell_library` deps should match `haskell_test` deps for core packages
   - Both should use `//:` prefix for GHC-bundled packages

5. **Rebuild:**
   ```bash
   bazel clean
   bazel build //...
   bazel test //...
   ```

## Quick Reference

```starlark
# Template for Haskell library/binary/test
haskell_library(
    name = "my-lib",
    srcs = glob(["src/**/*.hs"]),
    src_strip_prefix = "src",
    visibility = ["//visibility:public"],
    deps = [
        # Core GHC packages (no @stackage)
        "//:base",
        "//:bytestring",
        "//:containers",
        "//:directory",
        "//:filepath",
        "//:text",
        "//:time",

        # Third-party packages (with @stackage)
        "@stackage//:aeson",
        "@stackage//:yaml",
        "@stackage//:cmark",
    ],
)

haskell_test(
    name = "unit-tests",
    srcs = glob(["test/**/*.hs"]),
    src_strip_prefix = "test",
    deps = [
        ":my-lib",

        # Core GHC packages
        "//:base",
        "//:text",

        # Test frameworks (third-party)
        "@stackage//:QuickCheck",
        "@stackage//:hspec",
    ],
)
```

## Common Error: Missing Test Files

### Symptom
```
ERROR: No source file defining the main module 'Main'.
You may need to set the 'main_file' attribute or the 'module_name' attribute in a 'haskell_module' rule.
```

### Root Cause
The `haskell_test` rule expects actual Haskell test files (*.hs) but the test directory may only contain fixtures or be empty.

### Solution
1. **Remove the test target if no tests exist yet:**
   ```starlark
   # Remove or comment out until tests are written
   # haskell_test(
   #     name = "unit-tests",
   #     srcs = glob(["test/**/*.hs"]),
   #     ...
   # )
   ```

2. **Or create a minimal test file (test/Main.hs):**
   ```haskell
   module Main where
   main :: IO ()
   main = putStrLn "Tests not implemented yet"
   ```

## Common Error: Custom Dependency Glob Pattern Mismatch

### Symptom
Build fails or can't find source files when using custom dependencies from `non_module_deps.bzl`

### Root Cause
The `strip_prefix` in `http_archive` changes the directory structure, but the glob pattern in `build_file_content` doesn't match the post-strip structure.

### Solution Pattern

**When using strip_prefix:**
```starlark
http_archive(
    name = "libyaml",
    urls = ["https://hackage.haskell.org/package/libyaml-0.1.4/libyaml-0.1.4.tar.gz"],
    strip_prefix = "libyaml-0.1.4",  # ← Directory is stripped
    build_file_content = """
haskell_cabal_library(
    name = "libyaml",
    srcs = glob(["**/*"]),  # ✓ Use glob without directory prefix
    ...
)
"""
)
```

**Without strip_prefix:**
```starlark
http_archive(
    name = "yaml",
    urls = ["https://hackage.haskell.org/package/yaml-0.11.11.2/yaml-0.11.11.2.tar.gz"],
    # No strip_prefix ← Directory preserved
    build_file_content = """
haskell_cabal_library(
    name = "yaml",
    srcs = glob(["yaml-0.11.11.2/**/*"]),  # ✓ Include directory in glob
    ...
)
"""
)
```

**Debugging tip:** Check the actual directory structure in the external repository:
```bash
ls -la ~/.bazel/external/_main~non_module_deps~<package-name>/
```

## Additional Notes

- The error message mentions `@@rules_haskell~~stack_snapshot~stackage` - this is Bazel's canonical repository name
- GHCi warnings about missing binary are informational and don't affect builds
- Use `--verbose_failures` flag for detailed error information
- After fixing deps, run `bazel clean` if caching causes issues
- For custom dependencies, verify glob patterns match the directory structure after `strip_prefix` is applied

## When to Use This Skill

Invoke this skill when:
- Encountering "not visible from target" errors with Haskell dependencies
- Setting up new `haskell_library`, `haskell_binary`, or `haskell_test` targets
- Migrating existing Haskell code to Bazel
- Debugging BUILD.bazel dependency configuration
