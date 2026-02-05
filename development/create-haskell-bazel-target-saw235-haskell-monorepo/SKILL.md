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

## Checklist
1. Check if it is already declared in the MODULE.bazel
2. Check if the target is build clean
3. When adding data as a bazel dependencies, the relative path needs to be from the repository root, 
 
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
```
# Neural network from scratch application
haskell_binary(
    name = "neural-network",
    srcs = [":Main.hs"],
    deps = [
        "//:base",
        "//haskell/libs/neural-network",
        "@stackage//:mtl",
        "@stackage//:random",
    ],
)
```

```
haskell_library(
    name = "neural-network",
    srcs = glob(["src/**/*.hs"]),
    src_strip_prefix = "src",
    ghcopts = ["-XRecordWildCards"],
    deps = [
        "//:base",
        "@stackage//:vector",
        "@stackage//:random",
        "@stackage//:mtl",
    ],
    visibility = ["//visibility:public"],
)
```