---
name: performance-profiling
description: Structured performance profiling and optimization skill for identifying and eliminating bottlenecks. Auto-triggers on slowness keywords.
---

# Performance Profiling & Optimization Skill

Systematic performance optimization framework for diagnosing bottlenecks, measuring improvements, and implementing optimizations with measurable results.

## Auto-Trigger Keywords

The skill activates when messages contain performance-related keywords:
- **Slowness**: "slow", "lag", "sluggish", "takes too long"
- **Timeout Issues**: "timeout", "hangs", "freezes"
- **Performance Concerns**: "performance", "speed", "optimize"
- **Scale Issues**: "10,000 records", "slow at scale", "doesn't scale"
- **Lock Issues**: "lock timeout", "can't acquire lock", "lock contention"
- **Specific Metrics**: "500ms", "5 seconds", "minutes to complete"

## Performance Optimization Workflow (6 Phases)

### Phase 1: Symptom & Scope Definition ✓

**Objective**: Clearly define what's slow and impact scope

1. **Gather Performance Complaint**
   - What operation is slow?
   - When did slowness occur?
   - How slow? (subjective vs measured time)
   - Is it reproducible?
   - What's the user's expectation vs reality?

2. **Ask Clarifying Questions**
   - How often does operation run? (per edit, batch operation, report)
   - How many records involved? (10, 100, 1,000, 10,000+?)
   - Is it consistently slow or intermittent?
   - Under what conditions is it slower?
   - Any recent changes before slowness appeared?

3. **Define Performance Target**
   - What's the current observed time?
   - What's the acceptable/target time?
   - What's the improvement needed? (50%, 10x faster, sub-second?)
   - Business impact if slow? (affects daily workflow, critical operation?)

4. **Identify Affected Module(s)**
   - Invoice creation/update?
   - Payment processing?
   - Balance calculation?
   - Cache operations?
   - Batch operations?
   - Query/lookup operations?

**Tools Used**: User description, Conversation analysis

---

### Phase 2: Baseline Measurement & Profiling ✓

**Objective**: Measure current performance and identify bottleneck

1. **Run Existing Benchmarks**
   ```bash
   # From Script Editor, run relevant test function
   runAllBenchmarks()           # All performance tests
   runQuickBenchmark()          # Essential tests only
   benchmarkQueryPerformance()  # Payment queries
   benchmarkCacheInitialization() # Cache loading
   ```

2. **Capture Baseline Metrics**
   - Operation execution time (ms)
   - How many sheet API calls made?
   - Lock duration (if applicable)
   - Memory usage estimate
   - Cache hit rate (if cache involved)
   - Scalability with different data sizes

3. **Identify Specific Bottleneck**
   - Is slowness in: sheet read, calculation, cache, lock, API calls?
   - At what data size does it become slow? (100, 1,000, 10,000 records?)
   - Single operation slow or accumulation of multiple operations?
   - Is lock contention involved?
   - Batch operation impact (N operations × M time each)?

4. **Add Detailed Tracing**
   ```javascript
   // Instrument function with timing
   function optimizeMe(data) {
     const timer1 = new BenchmarkUtils.Timer('Step 1: Read sheet');
     const rows = sheet.getRange(...).getValues();
     Logger.log(`⏱️  Step 1: ${timer1.stop()}ms`);

     const timer2 = new BenchmarkUtils.Timer('Step 2: Process data');
     const result = processData(rows);
     Logger.log(`⏱️  Step 2: ${timer2.stop()}ms`);

     const timer3 = new BenchmarkUtils.Timer('Step 3: Write results');
     sheet.getRange(...).setValues(result);
     Logger.log(`⏱️  Step 3: ${timer3.stop()}ms`);
   }
   ```

5. **Document Baseline**
   - Total time: X ms
   - Breakdown by step: [Step 1: Xms, Step 2: Yms, Step 3: Zms]
   - Bottleneck identified: [Step X accounts for 70% of time]
   - Data size used in test: [N records]
   - Expected improvement: [target time or 10x speedup]

**Tools Used**: Bash (run benchmarks), Edit (add logging), Logger (capture metrics)

---

### Phase 3: Optimization Pattern Identification ✓

**Objective**: Recognize which optimization pattern applies

Based on codebase history, check for these optimization patterns:

#### Pattern 1: **Reduce API Calls** (25-50% improvement common)
**Symptom**: Multiple `sheet.getRange()` calls in loop or function
**Example**: `buildUnpaidDropdown()` - reduced from 25-50 API calls to 10-20

```javascript
// ❌ BAD: 50+ API calls
for (let i = 0; i < 1000; i++) {
  const val = sheet.getRange(i, 1).getValue();  // 1000 calls
}

// ✅ GOOD: 1 API call
const allValues = sheet.getRange(1, 1, 1000, 1).getValues();
for (let i = 0; i < allValues.length; i++) {
  const val = allValues[i][0];  // Memory access
}
```

#### Pattern 2: **Lock Scope Reduction** (75% improvement possible)
**Symptom**: Lock held during entire function including reads and calculations
**Example**: PaymentManager - moved locks inside critical section

```javascript
// ❌ BAD: Lock held for 100-200ms
lock.acquire();
const data = readData();  // 50ms
const result = calculate(data);  // 50ms
writeData(result);  // 20ms
lock.release();

// ✅ GOOD: Lock held for 20-50ms
const data = readData();  // 50ms
const result = calculate(data);  // 50ms
lock.acquire();
writeData(result);  // 20ms
lock.release();
```

#### Pattern 3: **Caching/Indexing** (170x-340x improvement possible)
**Symptom**: Linear scan O(n) for lookups on large datasets
**Example**: PaymentCache quad-index structure

```javascript
// ❌ BAD: O(n) lookup - 340ms for 1000 payments
function findPayment(invoiceNo) {
  for (let i = 0; i < payments.length; i++) {
    if (payments[i].invoiceNo === invoiceNo) return payments[i];
  }
}

// ✅ GOOD: O(1) lookup - <1ms with index
const invoiceIndex = new Map();  // "INV-001" → [row indices]
function findPayment(invoiceNo) {
  return invoiceIndex.get(invoiceNo);  // Hash lookup
}
```

#### Pattern 4: **Batched Writes** (100-200ms improvement)
**Symptom**: Multiple single-cell writes in loop, no batching
**Example**: Batch operation UI updates

```javascript
// ❌ BAD: 100 API calls
for (let i = 0; i < 100; i++) {
  sheet.getRange(i, 1).setValue(status[i]);  // 1 cell at a time
}

// ✅ GOOD: 1 API call
const updates = status.map(s => [s]);  // 100×1 array
sheet.getRange(startRow, 1, 100, 1).setValues(updates);
```

#### Pattern 5: **Cache Invalidation Timing** (Prevents data corruption)
**Symptom**: Cache cleared before sheet write, or stale data after updates
**Example**: PaymentManager cache update timing

```javascript
// ❌ BAD: Cache cleared before data written
PaymentCache.clear();  // Cache cleared
paymentLog.appendRow(data);  // Data added after clear

// ✅ GOOD: Correct order
paymentLog.appendRow(data);  // Write first
PaymentCache.clear();  // Then invalidate cache
```

#### Pattern 6: **Algorithm Complexity** (Significant improvements)
**Symptom**: Calculation or processing takes O(n) when O(1) possible
**Example**: Incremental cache update (250x faster)

```javascript
// ❌ BAD: O(n) - reload all 1000 invoices: 500ms
CacheManager.getInvoiceData();  // Clear and reload

// ✅ GOOD: O(1) - update single invoice: 1ms
CacheManager.updateSingleInvoice(supplier, invoiceNo);
```

#### Pattern 7: **Partition/Segmentation** (70-90% reduction in active cache)
**Symptom**: Iterating over full dataset when subset is needed
**Example**: Cache partitioning (active vs inactive invoices)

```javascript
// ❌ BAD: Iterate 10,000 invoices for 500 unpaid ones
const unpaid = allInvoices.filter(inv => inv.balance > 0.01);

// ✅ GOOD: Iterate only 500 active invoices
const unpaid = activeInvoices.filter(inv => inv.balance > 0.01);
```

3. **Select Optimization Pattern**
   - What pattern matches this bottleneck?
   - What's the typical improvement? (25% to 340x)
   - Does similar optimization exist elsewhere in codebase?
   - Are there code examples to follow?

**Tools Used**: Grep (find similar patterns), Read (review existing optimizations)

---

### Phase 4: Implementation & Validation ✓

**Objective**: Implement optimization and verify improvement

1. **Implement Optimization**
   - Use pattern identified in Phase 3
   - Apply minimal, focused change
   - Keep related logic together
   - Add comments explaining optimization
   - Maintain code consistency

2. **Add Performance Logging**
   ```javascript
   // Add before/after timing to validate optimization
   const timerBefore = new BenchmarkUtils.Timer('Operation');
   // ... optimization code ...
   Logger.log(`⏱️  Optimized operation: ${timerBefore.stop()}ms`);
   ```

3. **Test Implementation**
   - Verify functionality still works correctly
   - Check that fix doesn't break related features
   - Run relevant unit tests
   - Verify with sample data

4. **Measure Improvement**
   ```javascript
   // Compare with baseline
   // Before: 500ms
   // After: 2ms
   // Improvement: 250x faster
   ```

5. **Document Change**
   - What was the bottleneck?
   - What optimization pattern was used?
   - What's the measured improvement? (X% or Yx faster)
   - Code size impact (added/removed lines)

**Tools Used**: Read (understand current code), Edit (implement), Bash (test)

---

### Phase 5: Benchmarking & Scalability Testing ✓

**Objective**: Prove improvement holds at scale and doesn't regress

1. **Run Performance Benchmarks**
   ```bash
   # Run comprehensive benchmark suite
   runAllBenchmarks()

   # Compare results with baseline from Phase 2
   ```

2. **Test at Multiple Scales**
   ```javascript
   // Test with different data sizes to verify O(1) vs O(n)

   // With 100 records: optimized = 10ms, baseline = 50ms
   // With 1,000 records: optimized = 10ms, baseline = 500ms
   // With 10,000 records: optimized = 10ms, baseline = 5000ms

   // ✓ O(1) behavior confirmed (constant time regardless of scale)
   // ✓ Baseline is O(n) behavior (scales linearly with data)
   ```

3. **Memory Impact Check**
   ```javascript
   // Verify memory overhead acceptable
   // - Cache structure: ~450KB per 1,000 records
   // - Index overhead: <10% additional memory
   // - No memory leaks or uncleared references
   ```

4. **Regression Testing**
   - Run all related unit tests
   - Verify batch operations work
   - Check cache synchronization
   - Test with Master Database mode (if applicable)
   - Concurrent operation testing

5. **Performance Report**
   ```
   OPTIMIZATION REPORT
   ═════════════════════════════════════════════════════
   Operation: [Operation name]
   Pattern Used: [Pattern name]
   Baseline: [time before] ms
   Optimized: [time after] ms
   Improvement: [X% reduction] or [Yx faster]
   Scale Tested: [records tested]
   Status: ✅ VERIFIED
   ```

**Tools Used**: Bash (run benchmarks), Logger (capture results), Bash (regression tests)

---

### Phase 6: Commit, Documentation & Prevention ✓

**Objective**: Finalize optimization and prevent regressions

1. **Create Comprehensive Commit**
   ```
   perf(<module>): <optimization pattern> for [X%] improvement

   Optimization: [Brief description of what changed]
   - [Specific change 1]
   - [Specific change 2]

   Results:
   - Baseline: XXXms
   - Optimized: XXms
   - Improvement: XXx faster or XX% reduction
   - Scales to: N+ records with O(1) behavior
   ```

2. **Add Benchmark Test Case**
   - If optimization is significant, add to benchmark suite
   - Test case should verify improvement remains
   - Document expected performance
   - Add comments explaining what's being measured

3. **Update CLAUDE.md**
   - Add to Performance Optimization History section
   - Document pattern used
   - Record improvement metrics
   - Link to commit hash

4. **Add Prevention Test Case**
   - Create unit test that would catch regression
   - Test should verify O(1) behavior or expected time
   - Include comments about what it prevents
   - Run test to confirm it passes

5. **Documentation**
   - Code comments explaining why optimization done
   - Any important notes about edge cases
   - Related optimizations or dependencies
   - Future optimization opportunities

**Tools Used**: Bash (git commits), Edit (add tests), Write (documentation)

---

## Common Performance Patterns from History

### Verified Optimizations in Codebase

| Optimization | Location | Before | After | Improvement |
|--------------|----------|--------|-------|-------------|
| Lock Scope Reduction | PaymentManager | 100-200ms | 20-50ms | 75% reduction |
| Cache Indexing (Quad-Index) | PaymentCache | 340ms | 2ms | 170x faster |
| Duplicate Detection Hash | PaymentCache | 340ms | <1ms | 340x faster |
| Batched Writes | UIMenu batch ops | 100 calls | 1 call | 100x fewer API calls |
| Incremental Cache Update | CacheManager | 500ms | 1ms | 250x faster |
| Cache Partitioning | CacheManager | Full 1000 invoices | Active 100-300 | 70-90% reduction |
| API Call Reduction | InvoiceManager | 50 calls | 20 calls | 60% reduction |
| Balance Calculation Optimization | BalanceCalculator | Variable | Constant | In-memory speed |

---

## Performance Measurement Tools & Methods

### Timer Pattern (from BenchmarkUtils)
```javascript
const timer = new BenchmarkUtils.Timer('Operation name');
// ... code to measure ...
const duration = timer.stop();
Logger.log(`⏱️  Operation: ${duration}ms`);
```

### Comparison Metrics
```javascript
// Calculate speedup
const speedup = (beforeTime / afterTime).toFixed(1);
Logger.log(`${speedup}x faster`);

// Calculate percentage improvement
const improvement = (1 - (afterTime / beforeTime)) * 100;
Logger.log(`${improvement.toFixed(1)}% improvement`);
```

### Scalability Testing
```javascript
// Test at multiple scales to verify complexity
for (let size of [100, 1000, 10000]) {
  // Run operation and measure time
  // If time stays constant: O(1) ✓
  // If time increases with size: O(n) - investigate further
}
```

---

## Investigation Checklist

Before assuming operation is slow:

- [ ] Measured current time with actual data
- [ ] Ran relevant benchmark tests
- [ ] Identified specific bottleneck (sheet read, calc, cache, lock?)
- [ ] Recognized optimization pattern that applies
- [ ] Found similar pattern in codebase to follow
- [ ] Implemented minimal change
- [ ] Verified functionality still works
- [ ] Ran full test suite - all pass
- [ ] Measured improvement vs baseline
- [ ] Tested at multiple scales
- [ ] Checked for memory leaks
- [ ] Verified no side effects
- [ ] Added benchmark/prevention test case
- [ ] Updated documentation
- [ ] Committed with clear message

---

## Anti-Patterns to Avoid

❌ **Don't:**
- Assume you know where time is spent without measuring
- Over-engineer solution for marginal gains (<5%)
- Add complexity to reduce time from 100ms to 50ms
- Skip testing at scale (data size optimization depends on)
- Cache everything indiscriminately (memory impact)
- Hold locks longer than necessary
- Make individual API calls in loops
- Ignore side effects of optimization

✅ **DO:**
- Measure first, optimize second
- Target bottlenecks that matter (70% of time)
- Follow proven patterns from codebase history
- Test at multiple scales
- Measure memory impact
- Release locks as soon as possible
- Batch API calls (read and write)
- Verify no data corruption from optimization

---

## Related Functions in Codebase

### Benchmark Suite (Benchmark.Performance.gs)
- `runAllBenchmarks()` - Full suite (~5-10 seconds)
- `runQuickBenchmark()` - Essential tests (~2-3 seconds)
- `benchmarkCacheInitialization()` - Cache load time
- `benchmarkQueryPerformance()` - Payment queries
- `benchmarkDuplicateDetection()` - Hash lookup performance
- `benchmarkCacheTTL()` - Expiration behavior
- `benchmarkDashboardSimulation()` - Real-world scenario
- `testCacheMemory()` - Memory analysis

### Cache Operations (CacheManager.gs)
- `getInvoiceData()` - Load with TTL
- `updateSingleInvoice()` - Incremental update (250x faster)
- `invalidate()` - Smart invalidation
- `getPartitionStats()` - Monitor active/inactive split

### Payment Operations (PaymentManager.gs)
- `getHistoryForInvoice()` - O(1) cached query
- `getHistoryForSupplier()` - O(1) cached query
- `isDuplicate()` - O(1) hash lookup
- `getStatistics()` - O(1) cached aggregation

### Batch Operations (UIMenu.gs)
- `batchPostAllRows()` - Batch post with performance tracking
- `batchValidateAllRows()` - Batch validation
- Shows performance metrics in results dialog

---

## Output Format

For each performance optimization, provide:

1. **Current Performance** - Measured baseline
2. **Bottleneck Analysis** - Where time is spent
3. **Optimization Pattern** - Which pattern applies
4. **Implementation** - Code changes made
5. **Measured Improvement** - Baseline vs optimized
6. **Scalability** - Tested at N records, behavior O(1) or O(n)
7. **Verification** - Tests pass, no side effects
8. **Memory Impact** - Overhead if any
9. **Documentation** - What to reference in future

---

## Key Principles

- **Measure First** - Don't assume where time is spent
- **Target Bottlenecks** - Fix the 70% that matters
- **Proven Patterns** - Use patterns from codebase history
- **Verify at Scale** - Performance claims depend on data size
- **Test Thoroughly** - All tests pass, no regressions
- **Document Results** - Help future optimization efforts
- **Prevent Regression** - Add tests to catch slowdowns
- **Minimal Changes** - Simplest solution that works

