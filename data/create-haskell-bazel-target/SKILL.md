---
name: create-haskell-bazel-target
description: Create a target for haskell application. 
---

# Create Haskell Bazel Target

## Instruction
1. When creating a binary use haskell_binary
2. When creating a test use haskell_test
3. When creating a library use haskell_library
4. Always want to include //:base for dependencies
5. Any other 3rd party package from hackage, need to use either @stackage or @stackage_alt depending on the packages needed

## CRITICAL: Dependency Prefix Rules

**Core GHC packages MUST use `//:` prefix (NOT `@stackage//:`)**

### Core GHC Packages (use `//:package-name`)
- `//:base` - Always required
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
- `@stackage//:vector`
- `@stackage//:random`
- Any package not bundled with GHC

### Common Error
Using `@stackage//:base` or `@stackage//:text` will cause visibility errors:
```
ERROR: target '@@rules_haskell~~stack_snapshot~stackage//:base' is not visible from target
```

**Fix:** Replace `@stackage//:base` with `//:base` (same for text, containers, etc.)

## Custom Dependencies in non_module_deps.bzl

When configuring custom Hackage packages in `non_module_deps.bzl`, ensure glob patterns match the directory structure AFTER `strip_prefix` is applied:

**WRONG:**
```starlark
http_archive(
    name = "libyaml",
    urls = ["https://hackage.haskell.org/package/libyaml-0.1.4/libyaml-0.1.4.tar.gz"],
    strip_prefix = "libyaml-0.1.4",  # This strips the directory
    build_file_content = """
haskell_cabal_library(
    name = "libyaml",
    srcs = glob(["libyaml-0.1.4/**/*"]),  # ❌ WRONG - directory already stripped!
    ...
)
"""
)
```

**CORRECT:**
```starlark
http_archive(
    name = "libyaml",
    urls = ["https://hackage.haskell.org/package/libyaml-0.1.4/libyaml-0.1.4.tar.gz"],
    strip_prefix = "libyaml-0.1.4",  # This strips the directory
    build_file_content = """
haskell_cabal_library(
    name = "libyaml",
    srcs = glob(["**/*"]),  # ✓ CORRECT - files are at root after strip
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
    # No strip_prefix - directory preserved
    build_file_content = """
haskell_cabal_library(
    name = "yaml",
    srcs = glob(["yaml-0.11.11.2/**/*"]),  # ✓ CORRECT - directory exists
    ...
)
"""
)
```

## Checklist
1. Check if it is already declared in the MODULE.bazel
2. Check if the target is build clean
3. When adding custom dependencies to non_module_deps.bzl, ensure glob patterns match the post-strip_prefix directory structure
4. When adding data as a bazel dependencies, the relative path needs to be from the repository root, 
 
```
    haskell_test(
        name = "hackage-doc-cli-test",
        srcs = glob(["**/*.hs"]),
        data = glob(["Fixtures/**/*"])
    )
```

source code
```
haskell/app/hackage-doc-cli/test/Fixtures/aeson-package.json
```

## Examples of Bazel Target

### haskell_binary Example
```starlark
# Neural network from scratch application
haskell_binary(
    name = "neural-network",
    srcs = [":Main.hs"],
    deps = [
        "//:base",                           # Core GHC package
        "//haskell/libs/neural-network",     # Local library
        "@stackage//:random",                # Third-party package
    ],
)
```

### haskell_library Example
```starlark
haskell_library(
    name = "neural-network",
    srcs = glob(["src/**/*.hs"]),
    src_strip_prefix = "src",
    ghcopts = ["-XRecordWildCards"],
    visibility = ["//visibility:public"],
    deps = [
        "//:base",                # Core GHC package
        "@stackage//:vector",     # Third-party package
        "@stackage//:random",     # Third-party package
    ],
)
```

### haskell_test Example
```starlark
haskell_test(
    name = "unit-tests",
    srcs = glob(["test/**/*.hs"]),
    src_strip_prefix = "test",
    deps = [
        ":my-library",            # Local library being tested
        "//:base",                # Core GHC package
        "//:text",                # Core GHC package
        "//:containers",          # Core GHC package
        "@stackage//:QuickCheck", # Third-party test framework
        "@stackage//:hspec",      # Third-party test framework
    ],
)
```

### Library with Multiple Core Dependencies
```starlark
haskell_library(
    name = "rpg-ruleset-core",
    srcs = glob(["src/**/*.hs"]),
    src_strip_prefix = "src",
    visibility = ["//visibility:public"],
    deps = [
        # Core GHC packages (use //:)
        "//:base",
        "//:bytestring",
        "//:containers",
        "//:directory",
        "//:filepath",
        "//:text",
        "//:time",

        # Third-party packages (use @stackage//:)
        "@stackage//:aeson",
        "@stackage//:cmark",
        "@stackage//:yaml",
    ],
)
```