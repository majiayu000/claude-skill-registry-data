---
name: rt.safety.auditor
description: Analyze C++ code for real-time safety violations including heap allocations, locks, blocking calls, and unbounded operations in audio threads.
---

# Real-Time Safety Auditor

## Purpose

The Real-Time Safety Auditor enforces Orpheus SDK's critical real-time constraints by analyzing C++ code for violations that could cause audio dropouts, latency spikes, or non-deterministic behavior. This skill encodes deep domain knowledge about broadcast-safe audio programming and prevents common mistakes that would break professional-grade performance requirements.

**Core Requirements:**

- **No heap allocations** in audio threads (causes unbounded latency)
- **No locks** in audio threads (causes priority inversion, blocking)
- **No blocking I/O** in audio threads (unpredictable delays)
- **No unbounded operations** (ensure deterministic execution time)
- **Sample-accurate timing** (64-bit atomic counters only, no floating-point time)

This skill is the primary enforcement mechanism for maintaining Orpheus's "broadcast-safe" guarantee (24/7 reliability, <5ms latency, zero dropouts).

## When to Use

**Trigger Patterns:**

- Code review for audio thread functions (processBlock, audioCallback, render path)
- Pre-merge validation of changes to real-time code paths
- Refactoring audio processing modules
- Debugging audio dropouts or latency issues
- Keywords: "real-time", "audio thread", "process", "callback", "render", "transport"
- File patterns: `*_processor.cpp`, `*_audio.cpp`, `*Transport*.cpp`, `*Render*.cpp`

**Do NOT Use When:**

- Analyzing UI thread code (allocations and locks are acceptable there)
- Reviewing build scripts or test code
- Inspecting non-audio utilities (file I/O, networking, etc.)

**Use Alternative Skills:**

- For general C++ code quality → use standard linters (clang-tidy)
- For test output analysis → use `test.result.analyzer`
- For documentation → use `orpheus.doc.gen`

## Allowed Tools

- `read_file` - Read C++ source files and headers for analysis
- `bash` - Run static analysis tools (cppcheck, clang-check, grep for patterns)
- `grep` - Search for banned function calls and patterns

**Access Level:** 1 (Local Execution - read + command execution)

**Rationale:**

- Read-only analysis requires file access to C++ sources
- Static analysis tools (cppcheck, grep) provide automated detection
- No file modification needed (auditing only, not fixing)
- No network access required (offline analysis)

**Explicitly Denied:**

- `write_file`, `edit_file` - This skill audits, doesn't fix (suggest fixes in report)
- Network tools - No external dependencies

## Expected I/O

**Input:**

- **Type:** C++ source files (.cpp, .h, .hpp) or directory paths
- **Format:** File paths or code snippets
- **Constraints:**
  - Must be valid C++ code (compiles)
  - Focus on audio thread functions (processBlock, audioCallback, render methods)
  - Include sufficient context (function definitions, not just declarations)

**Output:**

- **Type:** Real-Time Safety Audit Report (Markdown)
- **Format:**

  ```markdown
  # Real-Time Safety Audit Report

  ## File: [filename]

  ### VIOLATIONS (Critical - must fix)

  - [Line X]: [Issue description]
    - **Problem:** [Why this breaks real-time safety]
    - **Fix:** [Specific solution]

  ### WARNINGS (Review recommended)

  - [Line Y]: [Potential issue]
    - **Concern:** [Why this might be problematic]
    - **Suggestion:** [How to verify or improve]

  ### PASSED

  - [Summary of correct patterns found]
  ```

- **Validation:**
  - Every violation must cite line number
  - Every violation must explain impact and provide fix
  - False positive rate <5% (high precision)
  - Report must distinguish critical violations from warnings

## Dependencies

**Required:**

- C++ source files (readable text files)
- Basic POSIX tools (grep, sed, awk)
- Optional: `cppcheck` (static analysis), `clang-check` (AST analysis)

**Optional:**

- `compile_commands.json` (CMake output) for precise analysis
- Orpheus real-time constraints documentation (reference/rt_constraints.md)

**Version Requirements:**

- bash 4.0+
- grep with PCRE support (or equivalent)
- cppcheck 2.0+ (if available)

## Examples

### Example 1: Detecting Heap Allocation Violation

**User:** "Audit src/modules/m1/transport_controller.cpp for real-time safety"

**Claude Process:**

1. Read file: `read_file src/modules/m1/transport_controller.cpp`
2. Search for banned patterns: `grep -n "new \|delete \|malloc\|calloc" file.cpp`
3. Analyze context around matches (is this in audio thread?)
4. Generate report with violations, explanations, fixes

**Output:**

````markdown
# Real-Time Safety Audit Report

## File: src/modules/m1/transport_controller.cpp

### VIOLATIONS

#### Line 156: Heap Allocation in Audio Thread

```cpp
float* buffer = new float[size]; // VIOLATION
```
````

**Problem:** Dynamic allocation in processBlock() causes unbounded latency.
Heap allocation may trigger system calls, memory page faults, or garbage collection,
leading to audio dropouts in real-time contexts.

**Fix:**

```cpp
// Pre-allocate in constructor
std::array<float, MAX_BUFFER_SIZE> buffer_;

// Or use fixed-size buffer
float buffer[kMaxFrames * kMaxChannels];
```

### PASSED

- All atomic operations use std::memory_order_seq_cst or stronger
- No mutex locks detected in audio thread functions
- Buffer sizes are bounded by compile-time constants

````

### Example 2: Detecting Mutex Lock Violation

**User:** "Check if AudioMixer uses locks in the process method"

**Claude Process:**
1. Read file
2. Search for mutex patterns: `grep -n "std::mutex\|lock_guard\|unique_lock\|pthread_mutex" file.cpp`
3. Verify if usage is in audio thread
4. Report violation with lock-free alternative

**Output:**
```markdown
# Real-Time Safety Audit Report

## File: src/modules/m3/audio_mixer.cpp

### VIOLATIONS

#### Line 89: Mutex Lock in Audio Thread
```cpp
void AudioMixer::process(float** outputs, int numFrames) {
    std::lock_guard<std::mutex> lock(gainMutex_); // VIOLATION
    // ... processing code
}
````

**Problem:** Mutex locking in audio callback can cause priority inversion.
If a lower-priority thread holds the lock, the audio thread will block indefinitely,
causing audible glitches, dropouts, or complete audio failure.

**Fix:** Use lock-free atomic operations or single-producer-single-consumer queue:

```cpp
// Option 1: Atomic for simple values
std::atomic<float> targetGain_;

void process(float** outputs, int numFrames) {
    float gain = targetGain_.load(std::memory_order_acquire);
    // ... use gain
}

// Option 2: Lock-free SPSC queue for complex updates
// (Use juce::AbstractFifo or boost::lockfree::spsc_queue)
```

### WARNINGS

#### Line 112: Vector push_back may allocate

```cpp
activeChannels_.push_back(channelId); // WARNING
```

**Concern:** std::vector::push_back() may trigger reallocation.

**Suggestion:** Use `reserve()` in constructor to pre-allocate, or use fixed-size array.

```cpp
// In constructor
activeChannels_.reserve(kMaxChannels);
```

````

### Example 3: Clean Code (No Violations)

**User:** "Audit the sample counter implementation for real-time safety"

**Output:**
```markdown
# Real-Time Safety Audit Report

## File: src/modules/m2/sample_counter.cpp

### VIOLATIONS
None detected.

### WARNINGS
None detected.

### PASSED ✓

- **Atomic operations:** All sample count updates use std::atomic<uint64_t> with proper memory ordering
- **No allocations:** All buffers are stack-allocated or pre-allocated members
- **No locks:** No mutex, condition variables, or blocking primitives detected
- **Bounded operations:** All loops have compile-time bounds (kMaxFrames)
- **Deterministic:** Function execution time is O(1) with respect to sample count

**Real-Time Safety: VERIFIED**

This module follows all Orpheus real-time safety requirements and is safe for use in audio threads.
````

## Limitations

**Known Edge Cases:**

- Cannot detect allocations hidden in third-party library calls (manual review needed)
- May flag false positives for placement new (safe if pre-allocated)
- Cannot verify lock-free algorithm correctness (only absence of locks)
- Requires human judgment for complex lock-free patterns

**Performance Constraints:**

- Large files (>10,000 LOC) may require chunked analysis
- AST-based analysis (clang-check) slower but more accurate than grep

**Security Boundaries:**

- Read-only access to source code
- Executes local static analysis tools (cppcheck, grep)
- No modification of source files
- No network access

**Scope Limitations:**

- Analyzes C++ syntax, not runtime behavior
- Cannot detect allocations in deeply nested call chains without whole-program analysis
- Does not verify performance characteristics (use profiling for that)

## Validation Criteria

**Success Metrics:**

1. **Accuracy:** Correctly identify all banned functions in audio thread code paths
2. **Precision:** False positive rate <5% (don't flag safe code as violations)
3. **Completeness:** Detect heap allocations, locks, blocking I/O, unbounded operations
4. **Actionability:** Every violation includes line number, explanation, and fix suggestion
5. **Performance:** Audit 1000 LOC in <10 seconds

**Failure Modes:**

- **Miss violations:** Fails to detect banned patterns (update reference/banned_functions.md)
- **False positives:** Flags safe code (refine detection patterns, add allowlist)
- **Incomplete reports:** Missing line numbers or fixes (improve report template)
- **Tool unavailable:** cppcheck not installed (gracefully degrade to grep-based analysis)

**Recovery:**

- For missed violations: Update banned function list and re-audit
- For false positives: Add comments to source code explaining safety (e.g., `// SAFE: pre-allocated`)
- For tool failures: Fall back to manual grep patterns

## Related Skills

**Dependencies:**

- None (standalone skill)

**Composes With:**

- `test.result.analyzer` - Combine with sanitizer output to catch runtime violations
- `orpheus.doc.gen` - Document real-time safety guarantees in Doxygen comments

**Alternative Skills:**

- `clang-tidy` - General C++ linting (not real-time specific)
- Manual code review - Human expertise for complex lock-free algorithms

## Maintenance

**Owner:** Orpheus Team
**Review Cycle:** Weekly (update banned function list as needed)
**Last Updated:** 2025-10-18
**Version:** 1.0

**Revision Triggers:**

- New banned patterns discovered
- False positives reported
- Orpheus real-time requirements change
- Static analysis tool updates
