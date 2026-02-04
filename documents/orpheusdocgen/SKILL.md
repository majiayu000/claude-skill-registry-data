---
name: orpheus.doc.gen
description: Generate and maintain comprehensive documentation including Doxygen comments, progress reports, session notes, and API docs for Orpheus SDK.
---

# Orpheus Documentation Generator

## Purpose

The Orpheus Documentation Generator skill automates creation and maintenance of high-quality documentation for the Orpheus SDK, ensuring the 8000+ line documentation standard is maintained. This skill encodes documentation best practices, generates Doxygen-compliant API comments, and maintains progress tracking documents.

**Core Capabilities:**

- Generate Doxygen comments for C++ functions and classes
- Create progress reports and session notes
- Update implementation tracking documents
- Maintain consistent documentation style
- Include real-time safety and thread safety annotations
- Generate API reference documentation

**CRITICAL - Documentation File Naming:**

When creating new PREFIX-numbered documentation (ORP, OCC), files **MUST** follow this pattern:

**Format:** `{PREFIX###} {Descriptive Title}.md`

**Examples (CORRECT):**

- `ORP082 Session Performance Report.md`
- `OCC103 QA v020 Results.md`
- `ORP098 Real-time Safety Audit Results.md`

**Examples (WRONG - NEVER USE):**

- ❌ `ORP082.md` (missing descriptive title)
- ❌ `OCC-103-QA.md` (wrong separator format)

See `~/chrislyons/dev/CLAUDE.md` for complete naming conventions.

## When to Use

**Trigger Patterns:**

- After implementing new public APIs
- Updating progress documents (.claude/progress.md, SESSION\_\*.md)
- Generating Doxygen comments for code
- Creating session reports
- Keywords: "document", "Doxygen", "progress", "session report", "API docs"
- File patterns: `*.h`, `*.hpp`, `progress.md`, `SESSION_*.md`

**Do NOT Use When:**

- Writing actual code (use code generation skills)
- Testing code (use test.result.analyzer)
- Analyzing code quality (use rt.safety.auditor or linters)

**Use Alternative Skills:**

- For code quality → `rt.safety.auditor`, clang-tidy
- For test analysis → `test.result.analyzer`
- For general editing → Edit tool directly

## Allowed Tools

- `read_file` - Read existing code and documentation
- `write_file` - Create new documentation files
- `edit_file` - Update existing documentation

**Access Level:** 2 (File Modification - read + write + edit)

**Rationale:**

- Must read source code to generate accurate documentation
- Must write new documentation files (session reports, progress docs)
- Must edit existing documentation to keep it current
- No command execution needed (pure documentation)

**Explicitly Denied:**

- `bash` - No execution needed for documentation
- Network tools - Offline documentation only

## Expected I/O

**Input:**

- **Type:** C++ source files, existing documentation, or instructions
- **Format:** Code files (.cpp, .h), markdown files (.md), text instructions
- **Constraints:**
  - Valid C++ code for Doxygen generation
  - Existing documentation files for updates

**Output:**

- **Type:** Documentation (Doxygen comments, Markdown reports)
- **Format:**
  - Doxygen comments (Javadoc style)
  - Markdown progress reports
  - Session notes
  - API reference documents
- **Validation:**
  - All public APIs documented with @param, @return, @brief
  - Real-time safety and thread safety noted
  - Examples provided for complex functions
  - Progress reports include metrics and next steps

## Dependencies

**Required:**

- Source code files for API documentation
- Documentation style guide (reference/doc_style.md)

**Optional:**

- Doxygen (for generating HTML/PDF from comments)
- Existing progress reports (for updating)

**Version Requirements:**

- Markdown (CommonMark specification)
- Doxygen 1.9+ (if generating output)

## Examples

### Example 1: Generate Doxygen Comment for Function

**User:** "Generate Doxygen comments for the processBlock function"

**Input Code:**

```cpp
void AudioMixer::processBlock(float** outputs, int numFrames, int sampleRate);
```

**Claude Process:**

1. Read function signature
2. Infer parameters, purpose, behavior
3. Generate Doxygen comment using template
4. Include real-time safety notes
5. Add thread-safety annotation
6. Provide usage example

**Output:**

```cpp
/**
 * @brief Process an audio block by mixing all active channels
 *
 * Processes numFrames samples from all active input channels, applies per-channel
 * gain, and outputs the mixed result to the output buffers. This method implements
 * real-time safe mixing using pre-allocated buffers and lock-free gain updates.
 *
 * @param[out] outputs Pointer to output buffer array (stereo: 2 channels)
 *                      Each channel must have space for numFrames samples
 * @param[in] numFrames Number of samples to process (must be ≤ kMaxFrames)
 * @param[in] sampleRate Sample rate in Hz (e.g., 44100, 48000)
 *
 * @return void
 *
 * @pre outputs != nullptr && numFrames > 0 && numFrames <= kMaxFrames
 * @post Output buffers contain mixed audio samples
 *
 * @note Real-time safe: No allocations, no locks, O(numFrames) bounded execution
 * @warning Buffer overflow if numFrames > kMaxFrames (checked with assertion)
 *
 * @thread_safety Thread-safe for concurrent calls with different output buffers.
 *                Not safe for concurrent modification of mixer state.
 * @real_time Yes - Safe for audio thread use
 *
 * @example
 * @code
 * AudioMixer mixer;
 * float* outputs[2] = {leftChannel, rightChannel};
 * mixer.processBlock(outputs, 512, 48000);
 * @endcode
 */
void AudioMixer::processBlock(float** outputs, int numFrames, int sampleRate);
```

### Example 2: Generate Progress Report

**User:** "Create a progress report for Module 3 implementation"

**Output:**

```markdown
# Module 3: Audio Mixer Implementation Progress

**Date:** 2025-10-18
**Status:** In Progress
**Completion:** 75% (3/4 tasks)

---

## Completed Tasks

### ✅ Task 1: Core AudioMixer Class

- **File:** `src/modules/m3/audio_mixer.h`, `src/modules/m3/audio_mixer.cpp`
- **Lines of Code:** 324
- **Tests:** 15 tests, 98.2% coverage
- **Key Features:**
  - Sample-accurate mixing algorithm
  - Lock-free gain updates
  - Pre-allocated channel buffers

### ✅ Task 2: Unit Tests

- **File:** `tests/modules/m3/audio_mixer_test.cpp`
- **Lines of Code:** 287
- **Coverage:** 98.2% (target: 98% - OK)
- **Test Cases:**
  - Stereo mixing
  - Mono to stereo
  - Gain application
  - Buffer overflow protection
  - Edge cases (silence, zero frames)

### ✅ Task 3: Doxygen Documentation

- **Lines:** 156 lines of Doxygen comments
- **APIs Documented:** All 12 public methods
- **Quality:** Thread-safety and real-time safety annotations complete

---

## In Progress

### ⏳ Task 4: Multi-Channel Support (>2 channels)

- **Current:** Stereo only (2 channels)
- **Target:** Up to 16 channels
- **Blockers:** None
- **ETA:** 2 days

---

## Metrics

- **Lines of Code:** 611 total (324 impl + 287 tests)
- **Test Coverage:** 98.2%
- **Documentation:** 156 lines Doxygen
- **Build Status:** All tests passing ✓
- **Sanitizers:** Clean (ASan/TSan/UBSan) ✓
- **Performance:** <0.5% CPU at 48kHz with 8 channels

---

## Technical Highlights

### Lock-Free Gain Updates

Implemented atomic gain updates using `std::atomic<float>` with acquire/release semantics.
No locks in audio thread, zero contention.

### Fixed-Size Pre-Allocation

All buffers allocated in constructor. Audio thread uses only stack allocation and
pre-allocated members. Real-time safe verified with ASan.

### Floating-Point Determinism

All gain calculations use `std::bit_cast` for bit-identical results across platforms.
Verified with cross-platform integration tests.

---

## Lessons Learned

1. **Epsilon Comparisons:** Floating-point equality tests failed with exact comparison.
   Solution: Use `EXPECT_NEAR` with 1e-6 tolerance.

2. **Atomic Ordering:** Initial implementation used `memory_order_relaxed` for gain updates.
   TSan detected potential race. Fixed with `acquire/release` ordering.

3. **Buffer Alignment:** SIMD mixing required 16-byte aligned buffers.
   Solution: Use `alignas(16)` for buffer members.

---

## Next Steps

1. Implement multi-channel mixing (≤16 channels)
2. Performance profiling with 16 concurrent clips
3. Integration with TransportController
4. Update AudioEngine to use AudioMixer

---

## References

- ORP068 Implementation Plan (v2.0)
- OCC027 API Contracts (Multi-Channel Routing Matrix)
- Module 3 specification (.claude/m2_implementation_progress.md)
```

### Example 3: Update Session Notes

**User:** "Document today's session accomplishments"

**Output:**

```markdown
# Session Report: 2025-10-18

**Duration:** 3.5 hours
**Focus:** Real-time safety auditor skill implementation

---

## Accomplishments

### 1. rt.safety.auditor Skill Complete

Created comprehensive real-time safety auditing skill for Orpheus SDK:

**Files Created:**

- `.claude/skills/project/rt-safety-auditor/SKILL.md` (627 lines)
- `.claude/skills/project/rt-safety-auditor/reference/rt_constraints.md` (438 lines)
- `.claude/skills/project/rt-safety-auditor/reference/banned_functions.md` (342 lines)
- `.claude/skills/project/rt-safety-auditor/reference/allowed_patterns.md` (521 lines)
- `.claude/skills/project/rt-safety-auditor/scripts/check_rt_safety.sh` (189 lines, executable)
- 4 example files (safe + violation patterns)

**Total:** ~2,100 lines of documentation and tooling

**Key Features:**

- Detects heap allocations, locks, blocking I/O in audio code
- Comprehensive banned function list (9 categories, 50+ functions)
- Allowed pattern catalog (8 categories, 15+ safe patterns)
- Executable audit script with color-coded output
- Real-world violation and safe examples

### 2. test.result.analyzer Skill Complete

Created test output parsing and analysis skill:

**Files Created:**

- `SKILL.md` (542 lines)
- `reference/test_formats.md` (94 lines)
- `reference/sanitizer_formats.md` (127 lines)
- 2 example test output files

**Total:** ~800 lines

---

## Technical Decisions

### Real-Time Safety Enforcement

- Chose grep-based pattern matching for fast, dependency-free analysis
- Added escape hatches for safe patterns (SAFE: comments)
- Strict red/yellow/green reporting for clear actionability

### Documentation Quality

- All skills follow SKIL003 framework template
- Comprehensive examples (success + failure cases)
- Clear trigger patterns for Claude invocation

---

## Metrics

- **Files Created:** 13
- **Lines Written:** ~3,000
- **Skills Implemented:** 2/3 project-specific skills
- **Documentation Quality:** All skills follow SKIL003 standard

---

## Next Steps

1. Complete orpheus.doc.gen skill
2. Configure shared skills (test.analyzer, ci.troubleshooter)
3. Create manifest.json
4. Create validate.sh script
5. Update .claude/README.md

---

## Notes for Next Session

- orpheus.doc.gen templates nearly complete
- Shared skills just need config.json files
- manifest.json structure defined in SKIL003
- validate.sh based on rt.safety.auditor script pattern
```

## Limitations

**Known Edge Cases:**

- Cannot infer behavior from undocumented, uncommented code
- Doxygen generation requires valid C++ syntax
- Progress reports require manual input for metrics
- Cannot auto-generate usage examples without context

**Performance Constraints:**

- Large files (>10,000 LOC) may require chunked documentation
- Progress reports manual to ensure accuracy

**Security Boundaries:**

- Read-only for source code analysis
- Write access to documentation files only

**Scope Limitations:**

- Generates documentation, doesn't verify correctness
- Cannot replace human review for technical accuracy
- Does not build Doxygen output (use doxygen command for that)

## Validation Criteria

**Success Metrics:**

1. **Accuracy:** Generated documentation matches actual code behavior
2. **Completeness:** All required Doxygen tags present (@param, @return, @brief)
3. **Quality:** Thread-safety and real-time safety annotations included
4. **Style:** Matches existing Orpheus documentation conventions
5. **Usability:** Examples are clear and compilable

**Failure Modes:**

- **Incomplete docs:** Missing @param or @return tags (add validation)
- **Incorrect behavior:** Docs don't match code (manual review required)
- **Style mismatch:** Doesn't match conventions (update templates)

**Recovery:**

- For incomplete docs: Use validation checklist, iterate
- For incorrect docs: Request code review, clarify behavior
- For style issues: Update templates in reference/

## Related Skills

**Dependencies:**

- None (standalone skill)

**Composes With:**

- `rt.safety.auditor` - Include real-time safety analysis in docs
- `test.result.analyzer` - Document test coverage and results

**Alternative Skills:**

- Manual documentation - Human expertise for complex APIs
- Doxygen tool - Generate HTML/PDF from comments

## Maintenance

**Owner:** Orpheus Team
**Review Cycle:** Monthly (update templates as needed)
**Last Updated:** 2025-10-18
**Version:** 1.0

**Revision Triggers:**

- Documentation style guide changes
- New Doxygen features
- Progress tracking format changes
- Template improvements based on feedback
