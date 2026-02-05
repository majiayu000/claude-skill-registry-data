---
name: lean-build
description: Build, test, and debug Lean 4 projects using Lake. Use when building the ComputationalPaths project, checking for errors, running tests, cleaning artifacts, or debugging Lean 4 compilation issues.
---

# Lean 4 Build & Debug

This skill covers building, testing, and debugging the ComputationalPaths Lean 4 project using Lake (Lean's build system).

## Project Configuration

**Toolchain**: `leanprover/lean4:v4.24.0` (see `lean-toolchain`)

**Build file**: `lakefile.toml`
```toml
name = "computational_paths"
version = "0.1.0"
defaultTargets = ["computational_paths"]

[[lean_lib]]
name = "ComputationalPaths"

[[lean_exe]]
name = "computational_paths"
root = "Main"
```

## Essential Commands

### Building

```bash
# Build entire project (default targets)
lake build

# Build specific library
lake build ComputationalPaths

# Build specific module
lake build ComputationalPaths.Path.HIT.Circle

# Build executable
lake build computational_paths

# Build with verbose output
lake build -v
```

### Running

```bash
# Run the executable
lake exe computational_paths
```

### Cleaning

```bash
# Clean build artifacts
lake clean

# Full clean (removes .lake directory)
rm -rf .lake && lake build
```

### Updating Dependencies

```bash
# Update lake-manifest.json
lake update

# Resolve and fetch dependencies
lake exe cache get  # if using Mathlib cache
```

## Common Build Errors & Solutions

### 1. Type Mismatch

```
type mismatch
  h
has type
  Path a b
but is expected to have type
  Path a' b'
```

**Solution**: Check that terms have the expected types. Use `@` for explicit arguments or add type annotations.

### 2. Unknown Identifier

```
unknown identifier 'foo'
```

**Solution**:
- Check imports at the top of the file
- Verify the definition exists in the imported module
- Use fully qualified name: `ComputationalPaths.Path.foo`

### 3. Failed to Synthesize Instance

```
failed to synthesize instance
  Decidable (RwEq p q)
```

**Solution**: RwEq is not decidable. Use axioms or `noncomputable` where needed.

### 4. Universe Issues

```
universe level mismatch
```

**Solution**: Ensure consistent universe variables. HITs typically use `Type u`.

```lean
axiom MyHIT : Type u  -- not Type or Type*
```

### 5. Noncomputable Definition

```
'foo' depends on 'axiom', and therefore must be marked as 'noncomputable'
```

**Solution**: Add `noncomputable` keyword:

```lean
noncomputable def foo := ...
```

### 6. Missing Hypothesis

```
invalid 'exact' tactic, term has type ... but is expected to have type ...
```

**Solution**: The proof term doesn't match the goal. Check:
- Argument order
- Implicit vs explicit arguments
- Use `@` to make implicits explicit

### 7. Ambiguous Notation

```
ambiguous, possible interpretations: ...
```

**Solution**: Use qualified names or local `open` with hiding:

```lean
open Path hiding trans  -- if 'trans' conflicts
```

## Debugging Techniques

### Check Types

```lean
#check myTerm
#check @myFunction  -- show all arguments
#check (myTerm : ExpectedType)  -- verify type
```

### Print Definitions

```lean
#print myDefinition
#print axioms myTheorem  -- show axioms used
```

### Reduce Terms

```lean
#reduce myTerm  -- fully normalize
#eval myTerm    -- for decidable terms only
```

### Trace Tactics

```lean
set_option trace.Meta.Tactic.simp true in
theorem foo : ... := by simp
```

### Show Goals

```lean
theorem foo : ... := by
  show_term exact?  -- suggests exact term
  trace "{goal}"    -- print current goal
```

## Project Structure Validation

### Check Module Imports

Ensure `ComputationalPaths/Path.lean` imports all submodules:

```lean
import ComputationalPaths.Path.Basic
import ComputationalPaths.Path.Rewrite
import ComputationalPaths.Path.Groupoid
import ComputationalPaths.Path.Homotopy.FundamentalGroup
import ComputationalPaths.Path.HIT.Circle
-- etc.
```

### Verify File Locations

```
ComputationalPaths/
├── Basic.lean                 → import ComputationalPaths.Basic
├── Path.lean                  → import ComputationalPaths.Path
└── Path/
    ├── Basic/
    │   └── Core.lean          → import ComputationalPaths.Path.Basic.Core
    └── HIT/
        └── Circle.lean        → import ComputationalPaths.Path.HIT.Circle
```

## CI Integration

The project uses GitHub Actions with `leanprover/lean-action@v1`:

```yaml
# .github/workflows/lean_action_ci.yml
name: Lean Action CI
on: [push, pull_request, workflow_dispatch]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: leanprover/lean-action@v1
```

### Running CI Locally

Simulate CI by running:

```bash
lake clean && lake build
```

## Performance Tips

### Incremental Builds

Lake caches compilation. After changes, only affected files rebuild:

```bash
lake build  # rebuilds only changed modules
```

### Parallel Builds

Lake builds independent modules in parallel by default.

### Avoiding Recompilation

- Don't modify imports unnecessarily
- Keep module dependencies minimal
- Use `private` for internal definitions

## Lake Commands Reference

| Command | Description |
|---------|-------------|
| `lake build` | Build default targets |
| `lake build <target>` | Build specific target |
| `lake clean` | Remove build artifacts |
| `lake update` | Update dependencies |
| `lake exe <name>` | Run executable |
| `lake env <cmd>` | Run command in Lake environment |
| `lake --version` | Show Lake version |
| `lake --help` | Show help |

## Toolchain Management

### Check Current Toolchain

```bash
cat lean-toolchain
# leanprover/lean4:v4.24.0
```

### Update Toolchain

Edit `lean-toolchain`:
```
leanprover/lean4:v4.XX.Y
```

Then rebuild:
```bash
lake clean && lake build
```

## Quick Diagnostic Checklist

When builds fail:

1. **Check toolchain**: `cat lean-toolchain`
2. **Clean and rebuild**: `lake clean && lake build`
3. **Check imports**: Ensure all needed modules are imported
4. **Check file paths**: Module path must match filesystem
5. **Look for typos**: Lean is case-sensitive
6. **Check universe levels**: Ensure consistency
7. **Add `noncomputable`**: If using axioms
8. **Check CI**: Push to see if CI passes
