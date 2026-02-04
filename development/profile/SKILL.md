---
name: profile
description: Analyzes CPU profiles to identify performance bottlenecks and generate optimization recommendations
---

# Profile Skill

Investigate performance bottlenecks through CPU profiling and benchmark analysis.

## Quick Start

### 1. Collect CPU Profiles

```bash
SCENARIO=simple-object npm run profile:cpu         # Runs scenario + captures CPU profile
SCENARIO=simple-object npm run profile:detailed      # With deopt/opt analysis

# Or run directly with tsx
PROFILE_ITERATIONS=5000 node ./node_modules/tsx/dist/cli.mjs benchmark/scenarios/complex-object.ts
```

These scripts automatically build with debug symbols and run the specified scenario file while capturing profiles to `/profiles/*.cpuprofile`.

**Two-Phase Profiling:**

Scenarios generate two separate `.cpuprofile` files per run:

- `{scenario-name}-schema-building-{timestamp}.cpuprofile` - Schema creation profiling
- `{scenario-name}-parsing-{timestamp}.cpuprofile` - JSON parsing profiling

**Available Scenarios:**

- `simple-object` - Simple 4-field user object (default: 50,000 iterations)
- `complex-object` - 100 users with nested structures (default: 5,000 iterations)
- `1000-number-objects` - 1000 objects with 3 number fields (default: 5,000 iterations)
- `10000-number-objects` - 10,000 objects with 3 number fields (default: 1,000 iterations)
- `1000-user-objects-fail-fast` - 1000 user objects with validation failures (default: 500 iterations)
- `fail-fast-user` - User validation that fails fast (default: 5,000 iterations)
- `1000-simple-objects-70-30-valid` - 1000 simple objects (70% valid, default: 5,000 iterations)
- `1000-simple-objects-90-10-valid` - 1000 simple objects (90% valid, default: 5,000 iterations)
- `1000-nested-user-objects-70-30-valid` - 1000 nested user objects (70% valid, default: 1,000 iterations)
- `1000-nested-user-objects-90-10-valid` - 1000 nested user objects (90% valid, default: 1,000 iterations)

**Note:** The SCENARIO environment variable is required. Each scenario runs multiple iterations for profiling.

### Configuring Iteration Counts

All scenarios support environment variables to customize iteration counts:

```bash
# Run with custom iteration count
PROFILE_ITERATIONS=100000 SCENARIO=simple-object npm run profile:cpu

# For parsing-overhead scenario, customize both small and large payloads separately
PROFILE_ITERATIONS=100000 PROFILE_ITERATIONS_LARGE=10000 SCENARIO=parsing-overhead npm run profile:cpu

# Run fewer iterations for quick profiling (less CPU time)
PROFILE_ITERATIONS=1000 SCENARIO=large-array npm run profile:cpu
```

**Default Iteration Counts by Scenario:**

| Scenario                              | Default | Use Case                                       |
| ------------------------------------- | ------- | ---------------------------------------------- |
| `simple-object`                       | 50,000  | High iteration count for sampling granularity  |
| `complex-object`                      | 5,000   | Medium iteration count for nested structures   |
| `1000-number-objects`                 | 5,000   | Medium iteration count for number parsing      |
| `10000-number-objects`                | 1,000   | Lower count due to large payload size          |
| `1000-user-objects-fail-fast`         | 500     | Lower count, error path overhead analysis      |
| `fail-fast-user`                      | 5,000   | Medium count for both early/late failure paths |
| `1000-simple-objects-70-30-valid`     | 5,000   | Mixed valid/invalid simple objects             |
| `1000-simple-objects-90-10-valid`     | 5,000   | Mixed valid/invalid simple objects             |
| `1000-nested-user-objects-70-30-valid`| 1,000   | Mixed valid/invalid nested objects             |
| `1000-nested-user-objects-90-10-valid`| 1,000   | Mixed valid/invalid nested objects             |

**Tips for Iteration Counts:**

- **Quick profiling** (2-5 sec): Use `PROFILE_ITERATIONS=1000` for faster turnaround
- **Production-like** (30+ sec): Use defaults or increase to 100,000+ for stable profiles
- **Memory pressure testing**: Increase iterations to stress allocation patterns
- **Boundary crossing analysis**: Lower iterations (1,000-5,000) to focus on call overhead

### 2. Verify Profile Quality

Before analyzing, check that the profile has good quality:

```bash
# Find the latest profile
ls -lt profiles/*.cpuprofile | head -1
```

Read the .cpuprofile file and verify:

**Quality Checklist:**

- ✓ Profile has `nodes` array with function names (not just addresses)
- ✓ WASM function names are demangled (e.g., `atchara_wasm::lexer::parse` not just `wasm-function[123]`)
- ✓ Profile has `samples` array with sufficient data points (>1000 samples)
- ✓ `timeDeltas` are present and reasonable (microseconds)
- ✓ Top functions show recognizable names from Atchara codebase

**Red Flags:**

- ✗ Most functions are anonymous or numeric IDs only
- ✗ No WASM function names visible
- ✗ Very few samples (<100)
- ✗ Missing `nodes` or `samples` arrays

If profile quality is poor, rebuild with debug symbols:

```bash
npm run build:profile
SCENARIO=simple-object npm run profile:cpu
```

### 3. Analyze the Profile

```bash
# Basic analysis with WASM symbol enrichment
node .claude/skills/profile/analyze-profile.mjs profiles/simple-object-parsing-*.cpuprofile

# With WASM function disassembly
node .claude/skills/profile/analyze-profile.mjs profiles/simple-object-parsing-*.cpuprofile --disassemble

# JSON output for programmatic analysis
node .claude/skills/profile/analyze-profile.mjs profiles/simple-object-parsing-*.cpuprofile --json

# Help
node .claude/skills/profile/analyze-profile.mjs --help
```

The analyzer script automatically:

- Extracts WASM function symbols from the binary using `wasm-objdump`
- Categorizes functions (WASM, GC, boundary crossing, string ops, etc.)
- Calculates CPU time percentages and identifies hotspots
- Flags performance issues (high GC, excessive boundary crossing)
- Suggests specific optimization opportunities
- Optionally disassembles hot WASM functions with `wasm2wat`

## Performance Targets

- **Parsing Logic**: <55% (WASM functions, tokens, validation)
- **Garbage Collection**: <15% (allocation pressure)
- **Boundary Crossing**: <2% (JS/WASM marshaling)
- **String Operations**: <10% (UTF-8 encoding/decoding)

### Red Flags (Automatic detection by analyzer)

- GC > 25% = Memory allocation crisis
- Boundary crossing > 5% = Excessive marshaling overhead
- `Reflect` API in hot path = Expensive property lookups
- String cloning in loops = Redundant copies

## Commands Reference

```bash
# Build and profile
npm run build:profile                                             # Build with debug symbols
SCENARIO=<name> npm run profile:cpu                              # Capture CPU profile
PROFILE_ITERATIONS=<count> SCENARIO=<name> npm run profile:cpu   # Custom iteration count

# Analyze profiles
node .claude/skills/profile/analyze-profile.mjs <profile.cpuprofile>              # Basic analysis
node .claude/skills/profile/analyze-profile.mjs <profile.cpuprofile> --disassemble # With disassembly
node .claude/skills/profile/analyze-profile.mjs <profile.cpuprofile> --json       # JSON output
node .claude/skills/profile/analyze-profile.mjs <profile.cpuprofile> --top 30     # Show top 30 functions

# Find latest profile
ls -lt profiles/*.cpuprofile | head -1

# Example workflow
SCENARIO=1000-number-objects npm run profile:cpu
node .claude/skills/profile/analyze-profile.mjs profiles/1000-number-objects-parsing-*.cpuprofile
```

## Profile Analyzer

The `analyze-profile.mjs` script enriches .cpuprofile files with WASM debugging information.

**Features:**

- Extracts WASM function symbols (names, sizes) using `wasm-objdump`
- Categorizes functions (WASM/Rust, GC, boundary crossing, string ops)
- Calculates CPU time percentages and identifies hotspots
- Detects red flags (high GC, excessive boundary crossing)
- Provides optimization recommendations
- Optional WASM disassembly with `wasm2wat`

**Options:**

- `--top <n>` - Show top N functions (default: 20)
- `--disassemble` - Include WASM disassembly for hot functions
- `--threshold <n>` - Disassemble functions >n% CPU time (default: 5)
- `--json` - Output as JSON
- `--wasm <path>` - Custom WASM binary location

**Dependencies:** `brew install wabt binaryen`

## Related Files

- **profiles/\*.cpuprofile** - CPU profile data files
- **benchmark/scenarios/** - Profiling scenario files
- **benchmark/profiler.ts** - Profiler utility and API
- **.claude/skills/profile/analyze-profile.mjs** - Profile analyzer script with WASM debugging
- **package.json** - Benchmark and profiling npm scripts
- **pkg/atchara_wasm_bg.wasm** - WASM binary with debug symbols
- **wasm/src/lexer/** - Parsing implementation (optimization targets)
- **wasm/src/parser/** - Schema validation (optimization targets)

## Troubleshooting

**No WASM symbols in profile:**

```bash
npm run build:profile  # Rebuild with debug symbols
SCENARIO=<name> npm run profile:cpu
```

**Missing SCENARIO variable:**

```bash
SCENARIO=large-array npm run profile:cpu  # Must specify scenario
```

**Profile has few samples (<100):**

```bash
PROFILE_ITERATIONS=50000 SCENARIO=<name> npm run profile:cpu  # Increase iterations
```
