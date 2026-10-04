---
name: parallel-subagent
description: Eliminate a stubborn configuration bug by testing 8-10 fundamentally different fixes in parallel instead of one at a time. Use when the root cause is ambiguous and asked to "fix this stubborn bug", "we've tried everything", "run approaches in parallel", "use parallel subagents", or "find which config actually works". Builds a minimal test harness, evaluates every approach simultaneously, identifies the winners, and explains WHY they work.
---

# Fix Stubborn Bugs Fast By Parallelizing

<purpose>

**Eliminate ambiguous configuration bugs in hours, not days.** Test 8-10 fundamentally different solution approaches simultaneously to discover what works and understand why. Transforms trial-and-error into systematic exploration.

## Summary

**6-Step Process:** Read buggy code → Research 8-10 orthogonal approaches (document sources) → Build minimal harness → Implement all solutions → Test and identify winners → Apply fix with analysis + citations

**Best for:** Configuration/integration bugs in complex subsystems where root cause is ambiguous.

**Time:** 1-2 hours to build harness, saves hours/days of serial debugging.

**Success factors:** Platform compatibility, realistic test data with edge cases, comprehensive logging, matching production context, academic-quality documentation with cited sources.

**Research requirement:** Document all sources with URLs (GitHub issues, Stack Overflow, API docs, papers). Cite in code comments and README.

**Related methodologies:**
1. Binary Search Debugging (bisecting commits)
2. Fuzzing (input space exploration)
3. Property-Based Testing (behavior space)
4. A/B Testing (production comparison)
5. Ablation Testing (component removal)

This methodology is optimized for **configuration/integration debugging** where the challenge is finding the right way to wire components together.

---

## When to Use

**Good fit:**
1. Subsystem integration bugs
2. Framework configuration with multiple approaches possible
3. Ambiguous root cause
4. Slow iteration in main codebase
5. Reproducible behavior

**Poor fit:**
1. Obvious bugs (typos, logic errors)
2. Only 1-2 solutions exist
3. Good error messages
4. Time-critical hotfixes
5. Cannot isolate

</purpose>

---

<examples>

## Quick Example: UI Scrolling Bug

**Problem:** Table with 14 columns not showing horizontal scrollbar for long text (truncated with "...").

**10 Approaches:** BASELINE, SET_MAX_WIDTH, EXPAND_TO_INCLUDE_X, VSCROLL_FALSE, NO_CLIP, EXACT_COLUMNS, MIN_SCROLLED_WIDTH, SENSE_HOVER, NESTED_SCROLL, MANUAL_ALLOCATE

**Result:** Only Test 3 (expand_to_include_x) worked - forces UI to reserve space beyond viewport.

**Gotcha:** Applied fix → still broken! Logs showed data was empty (std::mem::take() moved it earlier). **Fix:** Calculate width BEFORE take() using available data. Production: 744 processes, 1609-char commands, 11,189px width (vs test: 50 processes, 150-char, 2000px).

</examples>

---

<workflow>

## The 6-Step Method

### Step 1: Read and Understand

**Do:**
1. [ ] Locate subsystem exhibiting problem
2. [ ] Document current configuration
3. [ ] Write precise expected vs actual behavior
4. [ ] List all configurable parameters
5. [ ] Review framework documentation (save links to relevant API pages)

**Output:** Clear understanding of broken state with documented references.

---

### Step 2: Research 8-10 Orthogonal Approaches

**Research sources (document all with links/citations):**
1. [ ] Framework API documentation (official docs, version-specific)
2. [ ] GitHub issues/bug reports (link to issue #, note workarounds)
3. [ ] Stack Overflow discussions (link to answers, cite voting/accepted status)
4. [ ] Academic papers/technical blogs (full citation: author, title, year, URL)
5. [ ] Related library source code (note file/line, link to specific commit)

**Citation standard:** Document all sources with URLs and context. Academic integrity: credit ideas, link to original discussions, note if approach is from specific issue/paper.

**Vary these dimensions:**
1. API Method (constructor/factory/builder)
2. Init Order (before/after deps)
3. Explicit vs Implicit
4. Delegation (parent/child)
5. Data Structure (mutable/immutable)
6. Sync vs Async
7. Config Location (inline/external)
8. Nested vs Flat
9. Direct vs Indirect
10. Pattern (pull/push)

**⚠️ Anti-Pattern:** Testing parameter values (100, 200, 300). **Do instead:** Test mechanisms (no buffering, fixed-size, dynamic, ring, double-buffer, memory-mapped, async, zero-copy, pooled, adaptive).

**Output:** List of 8-10 distinct approaches with hypotheses.

---

### Step 3: Build Minimal Test Harness

**Requirements:**
1. [ ] Same framework version (copy from dependencies)
2. [ ] Same data structures (representative sample)
3. [ ] Same execution context (threading, hierarchy, globals)
4. [ ] Minimal dependencies (strip business logic)
5. [ ] Fast build (<30 seconds)
6. [ ] Tabbed UI (macOS event loop limit: one per process)

**Platform decision:**

| UI Approach | Pros | Cons |
|-------------|------|------|
| Tabbed | Single window, easy switch, cross-platform | One at a time |
| Split view | See 2-4 at once | Limited number |
| Separate windows | All visible | macOS event loop limit |
| Separate executables | Guaranteed isolation | More overhead |

**Skeleton with edge cases (adapt to your language):**
```python
TEST_DATA = [
    {"name": "Normal", "value": "x"},        # Happy path
    {"name": "x" * 200, "value": "long"},    # Edge: very long
    {"name": "", "value": ""},               # Edge: empty
    {"name": None, "value": None},           # Edge: null
    {"name": "日本語", "value": "🚀"},        # Edge: unicode
    {"name": "  spaces  ", "value": "\n\t"}, # Edge: whitespace
]

tabs.add_tab("Test 1: Baseline", test_1(TEST_DATA))
tabs.add_tab("Test 2: Factory", test_2(TEST_DATA))
# ... tests 3-10
```

**⚠️ Gotcha 1:** Separate windows crash on macOS ("EventLoop can't be recreated"). Use tabs.

**⚠️ Gotcha 2:** Test data must match production scale. Profile production first (min/max/avg), use realistic sizes (not 10 items vs 700), include edge cases (empty, null, very long, unicode, whitespace).

**Output:** Harness where Test 1 (baseline) reproduces bug.

---

### Step 4: Implement All 10 Solutions

**Pattern (examples in Python, adapt to your language):**
```python
def test_1_baseline():
    """BASELINE: Current broken approach"""
    return Component(current_config).render(TEST_DATA)

def test_2_factory():
    """VARIATION: Factory vs constructor
    Hypothesis: Constructor skips registration"""
    return Factory.create(current_config).render(TEST_DATA)
```

**Rules:**
1. [ ] Each test is separate function (no shared state)
2. [ ] All use identical TEST_DATA
3. [ ] Only ONE thing varies per test
4. [ ] Comment: variation + hypothesis

**⚠️ Gotcha 3:** Global state pollution. Reset before/after each test:
```python
def run_test(test_func):
    reset_globals()
    result = test_func(TEST_DATA)
    reset_globals()
    return result
```

**Output:** Complete harness with all 10 solutions.

---

### Step 5: Test and Document Results

**Classify:**
1. **✅ WORKS** - Fixes bug, no side effects
2. **⚠️ PARTIAL** - Fixes but has issues
3. **❌ FAILS** - Doesn't fix
4. **💥 BREAKS** - Makes it worse

**Document:**
```
Test 3: EXPAND_TO_INCLUDE - ✅ WORKS
1. Observation: Horizontal scrollbar appears
2. Details: Width 11,189px, scrolls smoothly
3. Trade-offs: Need to calculate width in advance

Test 2: SET_MAX_WIDTH - ❌ FAILS
1. Why: Overridden by ScrollArea internally
```

**Output:** Documented results identifying winner(s).

---

### Step 6: Analyze and Apply

**Analysis (ask these 5 questions):**
1. What's minimal difference between working/broken?
2. Why does this succeed where others fail?
3. What does this reveal about framework internals?
4. Are there trade-offs or edge cases?
5. Is this the simplest working approach?

**Document pattern:**
```
## Why Test 3 Works
What it does: [one sentence]
Why it works: [mechanism explanation]
Why others failed:
  - Test 2: [reason]
  - Test 7: [reason]
Trade-offs: [any limitations]
```

**Apply to production:**
1. [ ] Locate corresponding code
2. [ ] Apply minimal change (exact approach from working test)
3. [ ] Match execution context (order, data availability)
4. [ ] Test with production data
5. [ ] Add comments explaining WHY + failed alternatives

**Comment template:**
```python
# Use [APPROACH] to fix [PROBLEM].
# Why alternatives failed:
# - set_max_width(): overridden by ScrollArea internally (egui docs v0.33)
# - min_scrolled_width(): doesn't adapt to content (GitHub issue #1234)
# Research: stackoverflow.com/a/789, framework docs at [URL]
# See tests/scroll_test for parallel approach comparison.
```

**If fix works in test but fails in production:**

**Add logging to both (Python shown, use console.log/System.out/etc for your language):**
```python
print(f"Data: {len(data)} rows")
print(f"First: {data[0] if data else 'EMPTY'}")
print(f"Result: {result}")
```

**Compare side-by-side:**
```
TEST:       Data: 50 rows
PRODUCTION: Data: 0 rows    ← FOUND PROBLEM (data moved/consumed)
```

**⚠️ Gotcha 4:** Data availability mismatch. Symptom: suspiciously small values (100px vs 2000px). **Fix:** Calculate BEFORE any take()/move().

**Debugging checklist:**
1. [ ] Log data count, intermediate steps, outputs
2. [ ] Run both, capture logs
3. [ ] Compare line-by-line
4. [ ] Identify first divergence
5. [ ] Fix root cause (not symptom)

**⚠️ Anti-Pattern:** Stopping at "it works". **Do instead:** Document WHY it works and WHY others failed.

**Output:** Working fix in production with clear analysis.

</workflow>

---

<rationale>

## Why This Works

**Efficiency:** Evaluates all approaches in single run (minutes vs hours/days). Fast iteration. Clear visual comparison eliminates guesswork.

**Thoroughness:** Systematic exploration discovers non-obvious solutions. Documents what doesn't work (valuable negative results).

**Knowledge:** Framework internals become clearer. Mental model improves. Future reference for similar issues.

**ROI:** Worthwhile when serial debugging would take >4 hours. Best for complex subsystems, multiple failed attempts, or when deep understanding needed.

</rationale>

---

<pitfalls>

## Critical Pitfalls

### Pitfall 1: Test Harness Doesn't Match Reality

**Symptoms:** Over-simplified test with `data=[1,2,3]` doesn't reproduce bug. Test passes, production fails. Different behavior in test vs production.

**Causes:**
1. Mock data instead of realistic
2. Skipped initialization
3. Different data types/threading/context
4. Framework version mismatch (test v2.0, production v1.8)
5. Async vs sync mismatch ("not initialized" errors)

**Fix:**
1. [ ] Copy EXACT framework version
2. [ ] Match: data types, threading, init sequence
3. [ ] Verify baseline test REPRODUCES bug
4. [ ] Profile production first, match scale
5. [ ] Include edge cases (empty, null, long, unicode)

---

### Pitfall 2: Incomplete Documentation

**Symptoms:** Only documenting working solution. Future developers try failed approaches again.

**Causes:**
1. Not documenting WHY it works
2. Not listing failed alternatives
3. Not testing edge cases
4. Not explaining trade-offs
5. Not citing research sources (GitHub issues, Stack Overflow, papers)

**Fix:** Document pattern of failures with sources:
```
✅ expand_to_include_x() - WORKS (forces layout)
❌ set_max_width() - FAILS (overridden internally)
   Source: egui issue #1234 (github.com/emilk/egui/issues/1234)
❌ min_scrolled_width() - FAILS (doesn't adapt)
   Source: Stack Overflow answer by user123 (stackoverflow.com/a/789)

Pattern: Framework needs explicit expansion API, not hints.
References: See tests/scroll_test, egui docs (egui.rs/api/v0.33/ScrollArea)
```

---

### Pitfall 3: Deleting Test Harness

**Symptom:** Fix works now, but breaks after framework update. Can't debug similar future bugs.

**Fix:** Commit harness to `tests/bug-fixes/YYYY-MM-DD-[name]/` with README explaining approaches tested, why winner worked, and citing all research sources (GitHub issues, Stack Overflow, papers, docs with URLs).

**Value:** Reference for similar bugs, verify fix survives updates, training material, academic integrity.

</pitfalls>

---

<reference>

## Quick Reference

### 10 Approach Categories

1. **API Method** - Constructor vs Factory.create() vs Builder
2. **Init Order** - setup_deps(); create() vs create(); setup_deps()
3. **Explicit vs Implicit** - size=1000 vs size=auto
4. **Delegation** - parent.layout(child) vs child.layout()
5. **Data Structure** - mutable list vs immutable tuple
6. **Sync vs Async** - blocking call vs await async_call()
7. **Config** - inline params vs load_config("file.json")
8. **Nested vs Flat** - deep.hierarchy.component vs flat_component
9. **Direct vs Indirect** - call() vs proxy.call()
10. **Pattern** - pull (get()) vs push (subscribe(listener))

### Result Classification

1. ✅ **WORKS** - Fixes bug completely, no side effects
2. ⚠️ **PARTIAL** - Fixes but has performance/edge case issues
3. ❌ **FAILS** - Doesn't fix the bug
4. 💥 **BREAKS** - Worse (crashes, corrupts, regresses)

### Common Failure Patterns

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Works in test, fails in production | Data empty (moved/taken) | Calculate before data consumption |
| Suspiciously small values (100 vs 2000) | Using empty data | Add logging, compare test vs prod |
| "Not initialized" errors | Async timing | Match async model, add delays |
| Order-dependent test results | Global state pollution | Reset state before/after each test |
| Different test/prod behavior | Version/context mismatch | Match framework version and execution context |

### Success Checklist

**Before:**
1. [ ] Bug reproducible and isolated
2. [ ] Root cause unclear (multiple possibilities)
3. [ ] Have 1-2 hours to invest

**During:**
1. [ ] 8-10 orthogonal approaches (not parameter tweaks)
2. [ ] Harness builds <30 seconds
3. [ ] Baseline test reproduces bug
4. [ ] All tests use identical data
5. [ ] Representative data (match production scale + edge cases)

**After:**
1. [ ] Analyzed WHY winner works
2. [ ] Documented failure patterns with research sources
3. [ ] Minimal change to production
4. [ ] Comments explain WHY + list failed alternatives + cite sources
5. [ ] Verified with production data
6. [ ] Committed test harness to repo with README citing all research

</reference>
