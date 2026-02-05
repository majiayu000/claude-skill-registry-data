---
name: test-stages
description: Staged test organization and testing guidelines for Mycelia
---

# Mycelia Test Stage Organization

The test suite is tiered by workflow stage.

## Test Stage Directories

1. `test/1_data_acquisition/` - Data loading and acquisition
2. `test/2_preprocessing_qc/` - Quality control and preprocessing
3. `test/3_feature_extraction_kmer/` - K-mer analysis and feature extraction
4. `test/4_assembly/` - Assembly algorithms
5. `test/5_validation/` - Validation and verification
6. `test/6_annotation/` - Annotation workflows
7. `test/7_comparative_pangenomics/` - Comparative and pangenomic analysis
8. `test/8_tool_integration/` - External tool integration

Additional directories:
- `test/in_development/` - Opt-in experimental tests
- `test/deprecated/` - Legacy tests (do not use)

## Adding New Tests

1. Place tests in the relevant stage directory
2. Name files after the feature (e.g., `assembly_merging.jl`)
3. Use `Test.@testset` with descriptive labels
4. Use small fixtures from `assembly_test_data/`
5. Use `StableRNGs` for deterministic seeds

Example:
```julia
import Test
import StableRNGs

Test.@testset "Assembly Merging" begin
    rng = StableRNGs.StableRNG(42)
    # Test code with deterministic randomness
end
```

## Test Commands

```bash
# Core tests (Aqua + optional JET)
julia --project=. -e "import Pkg; Pkg.test()"

# Full pipeline tests
MYCELIA_RUN_ALL=true julia --project=. -e "import Pkg; Pkg.test()"

# External tool tests
MYCELIA_RUN_EXTERNAL=true julia --project=. -e "import Pkg; Pkg.test()"

# Coverage
julia --project=. --code-coverage=user -e "import Pkg; Pkg.test()"

# Static analysis
julia --project=. test/jet.jl
```

## Testing Rules

- **NEVER disable tests because functionality is broken** - fix the implementation first
- Use `Test.@test_skip` ONLY for explicitly planned but unimplemented features
- External tool tests must run with `MYCELIA_RUN_EXTERNAL=true` without extra flags
- Use simulated inputs and default database paths where possible
- Extended tutorials/benchmarks are opt-in; note runtime or external-tool requirements
