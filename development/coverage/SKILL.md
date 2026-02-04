---
name: coverage
description: Generate a code coverage report for the Pinhole Rust project. Use this when the user asks for coverage analysis, test coverage metrics, or wants to see which code is tested. Automatically runs tests with instrumentation, merges coverage data, and displays a detailed report.
---

# Coverage Report Skill

This skill generates a comprehensive code coverage report for the Pinhole project using Rust's built-in LLVM coverage tools.

## What This Skill Does

1. Cleans up any existing coverage files
2. Runs all tests with coverage instrumentation
3. Merges coverage data from all test runs
4. Generates and displays a coverage report showing:
   - Overall coverage percentage
   - Per-file coverage statistics
   - Functions and lines covered/missed
5. Cleans up temporary coverage files

## Implementation

Execute these steps in order:

### Step 1: Clean existing coverage files
```bash
cd /Users/michael/dev/pinhole
find . -name "*.profraw" -o -name "*.profdata" | xargs rm -f 2>/dev/null || true
echo "Cleaned up existing coverage files"
```

### Step 2: Run tests with coverage instrumentation
```bash
cd /Users/michael/dev/pinhole
RUSTFLAGS="-C instrument-coverage" LLVM_PROFILE_FILE="pinhole-%p-%m.profraw" cargo test --workspace 2>&1
```

**Important**: This step compiles all code with instrumentation and runs 113 tests. It may take 60-120 seconds. If it times out, run it in the background using `run_in_background: true`.

### Step 3: Find LLVM tools
```bash
LLVM_PROFDATA=$(find ~/.rustup/toolchains -name "llvm-profdata" -type f 2>/dev/null | head -1)
LLVM_COV=$(find ~/.rustup/toolchains -name "llvm-cov" -type f 2>/dev/null | head -1)
echo "Using LLVM tools:"
echo "  profdata: $LLVM_PROFDATA"
echo "  cov: $LLVM_COV"
```

### Step 4: Merge all profraw files
```bash
cd /Users/michael/dev/pinhole
LLVM_PROFDATA=$(find ~/.rustup/toolchains -name "llvm-profdata" -type f 2>/dev/null | head -1)
$LLVM_PROFDATA merge -sparse $(find . -name "*.profraw" -type f) -o pinhole-combined.profdata
echo "Merged $(find . -name "*.profraw" -type f | wc -l) profraw files"
```

### Step 5: Generate coverage report
```bash
cd /Users/michael/dev/pinhole
LLVM_COV=$(find ~/.rustup/toolchains -name "llvm-cov" -type f 2>/dev/null | head -1)

$LLVM_COV report \
  --use-color \
  --instr-profile=pinhole-combined.profdata \
  --object target/debug/deps/pinhole-f2d40409e97edad8 \
  --object target/debug/deps/pinhole_client-8357b1173bc4a611 \
  --object target/debug/deps/pinhole_protocol-87558801f9169407 \
  --object target/debug/deps/action_dispatch_test-01015fd0d88dfe14 \
  --object target/debug/deps/client_server_test-3352a4d0dd8268bc \
  --object target/debug/deps/concurrent_connections_test-c695af612c5195eb \
  --object target/debug/deps/malformed_messages_test-7bcae52bc4bb5be1 \
  --object target/debug/deps/route_matching_test-04f8290cb25818d9 \
  --object target/debug/deps/storage_corruption_test-b8e06c1d4322ae4e \
  --object target/debug/deps/error_handling_test-32f92ec7df6e739a \
  --object target/debug/deps/message_serialization_test-6ab18a04f316113a \
  --object target/debug/deps/message_size_limit_test-23701d252bc9cf3e \
  --object target/debug/deps/tls_integration_test-a042db6c8858784d \
  --ignore-filename-regex='/.cargo/registry' \
  --ignore-filename-regex='rustc/' 2>&1
```

**Note**: If test binary hashes have changed (after code modifications), you'll see warnings about missing objects. The report will still work with the available binaries.

### Step 6: Clean up coverage files
```bash
cd /Users/michael/dev/pinhole
find . -name "*.profraw" -o -name "*.profdata" | xargs rm -f 2>/dev/null || true
echo "Cleaned up coverage files"
```

## Expected Output

The final report shows a table with columns:
- **Filename**: Source file path
- **Regions / Cover**: Code regions and coverage percentage
- **Functions / Executed**: Functions and execution percentage  
- **Lines / Cover**: Lines of code and coverage percentage
- **Branches / Cover**: Branch coverage (if available)
- **TOTAL**: Overall coverage across all files

## Notes

- **Target**: 70%+ code coverage
- **Last known**: 87.73% overall coverage
- **Test count**: 113 tests across workspace
- **Workspace crates**: pinhole-framework, pinhole-client, pinhole-protocol, todomvc-example
- Binary hashes in step 5 may need updating after code changes
