---
name: code-optimizer
description: Performance-focused code optimization covering algorithmic complexity, memory usage, I/O efficiency, caching, and concurrency. Use when code is slow, uses.
---

# Code Optimizer

Systematic performance optimization of code through profiling, algorithmic improvement, memory optimization, I/O efficiency, caching strategies, and concurrency patterns. This skill emphasizes measurement-driven optimization, targeting verified bottlenecks rather than applying premature optimizations.

## When to Use This Skill

Use this skill for:

- Code that is demonstrably too slow for its performance requirements
- Functions or endpoints that have been identified as bottlenecks through profiling
- Reducing memory consumption to stay within resource limits
- Optimizing I/O-bound operations (database queries, file processing, network calls)
- Improving response times for user-facing operations
- Reducing cloud infrastructure costs through more efficient resource usage
- Preparing code for higher scale (10x or 100x current load)
- Batch processing jobs that take too long to complete

**Trigger phrases**: "optimize", "performance", "slow code", "speed up", "bottleneck", "reduce memory", "cache", "too slow", "optimize query", "improve performance", "latency", "throughput"

## What This Skill Does

This skill provides a structured optimization methodology:

- **Profiling Guidance**: Identifies what to measure and how to find the actual bottleneck before optimizing
- **Algorithmic Optimization**: Reduces time complexity by selecting better algorithms and data structures
- **Memory Optimization**: Reduces memory footprint through data structure choices, lazy evaluation, and object reuse
- **I/O Optimization**: Minimizes I/O overhead through batching, connection pooling, and efficient serialization
- **Caching Strategies**: Applies appropriate caching at the right layer to eliminate redundant computation
- **Concurrency Patterns**: Leverages parallelism and asynchronous processing for CPU-bound and I/O-bound workloads
- **Trade-off Analysis**: Evaluates readability, maintainability, and correctness costs of each optimization

## Instructions

### Step 1: Profile Before Optimizing

Never optimize without data. Identify the actual bottleneck through measurement.

#### Profiling Tools by Language

| Language | CPU Profiler | Memory Profiler | I/O Profiler |
|----------|-------------|-----------------|-------------|
| Python | `cProfile`, `py-spy`, `scalene` | `tracemalloc`, `memory_profiler`, `scalene` | `strace`, `py-spy` |
| JavaScript | Chrome DevTools, `clinic.js` | Chrome DevTools Heap Snapshot, `memwatch` | `clinic.js bubbleprof` |
| Java | JFR (Java Flight Recorder), `async-profiler` | `jmap`, `MAT`, VisualVM | JFR I/O events, `strace` |

#### Python Example: Profile Before Optimizing

```python
import cProfile
import pstats
from io import StringIO


def profile_function(func, *args, **kwargs):
    """Profile a function and print the top 20 hotspots."""
    profiler = cProfile.Profile()
    profiler.enable()
    result = func(*args, **kwargs)
    profiler.disable()

    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats("cumulative")
    stats.print_stats(20)
    print(stream.getvalue())
    return result


# Profile the slow function to find the bottleneck
profile_function(process_large_dataset, dataset)
```

**Key rule**: the profile output tells you where the time is actually spent. Optimize the top entries, not what you assume is slow.

### Step 2: Optimize Algorithms and Data Structures

The highest-impact optimization is reducing algorithmic complexity.

#### Common Complexity Improvements

| Pattern | Before | After | Speedup (n=10,000) |
|---------|--------|-------|---------------------|
| Linear search to hash lookup | O(n) per lookup | O(1) per lookup | ~10,000x |
| Nested loops to hash join | O(n*m) | O(n+m) | ~10,000x |
| Repeated sorting to sorted insertion | O(n * n log n) | O(n log n) | ~10,000x |
| String concatenation in loop | O(n^2) | O(n) with join/builder | ~5,000x |
| Recomputing results | O(n * f(n)) | O(n) with memoization | Varies |

#### Python Example: O(n^2) to O(n) with Hash Lookup

```python
# BEFORE: O(n * m) -- nested loop to find matching records
def find_matching_orders(orders, customers):
    """Find orders with matching customer records."""
    results = []
    for order in orders:  # O(n)
        for customer in customers:  # O(m) for each order
            if order["customer_id"] == customer["id"]:
                results.append({**order, "customer_name": customer["name"]})
                break
    return results
# Total: O(n * m) -- with 10K orders and 10K customers: 100M comparisons


# AFTER: O(n + m) -- build lookup table first
def find_matching_orders(orders, customers):
    """Find orders with matching customer records."""
    customer_map = {c["id"]: c for c in customers}  # O(m) -- build once
    results = []
    for order in orders:  # O(n)
        customer = customer_map.get(order["customer_id"])  # O(1) lookup
        if customer:
            results.append({**order, "customer_name": customer["name"]})
    return results
# Total: O(n + m) -- with 10K orders and 10K customers: 20K operations
```

#### JavaScript Example: String Concatenation Optimization

```javascript
// BEFORE: O(n^2) -- string concatenation creates new string each iteration
function buildHtmlTable(rows) {
    let html = "<table>";
    for (const row of rows) {
        html += "<tr>";  // Each += copies the entire string
        for (const cell of row) {
            html += `<td>${cell}</td>`;
        }
        html += "</tr>";
    }
    html += "</table>";
    return html;
}

// AFTER: O(n) -- array join builds string once
function buildHtmlTable(rows) {
    const parts = ["<table>"];
    for (const row of rows) {
        parts.push("<tr>");
        for (const cell of row) {
            parts.push(`<td>${cell}</td>`);
        }
        parts.push("</tr>");
    }
    parts.push("</table>");
    return parts.join("");
}
```

#### Java Example: Collection Choice Optimization

```java
// BEFORE: Using ArrayList for frequent contains() checks -- O(n) per check
List<String> processedIds = new ArrayList<>();

for (Event event : events) {
    if (!processedIds.contains(event.getId())) {  // O(n) scan each time
        processEvent(event);
        processedIds.add(event.getId());
    }
}
// Total: O(n^2) for n events

// AFTER: Using HashSet for O(1) contains() checks
Set<String> processedIds = new HashSet<>();

for (Event event : events) {
    if (processedIds.add(event.getId())) {  // O(1) check + add
        processEvent(event);
    }
}
// Total: O(n) for n events
```

### Step 3: Optimize Memory Usage

Reduce memory consumption when working with large datasets or resource-constrained environments.

#### Memory Optimization Techniques

| Technique | When to Use | Typical Savings |
|-----------|------------|-----------------|
| **Generators / Iterators** | Processing large sequences one element at a time | Memory proportional to one element vs. entire sequence |
| **Streaming I/O** | Reading large files | Constant memory vs. file-size memory |
| **Object pooling** | Frequent creation/destruction of expensive objects | Reduces GC pressure |
| **Data structure compaction** | Storing large numbers of small objects | 2-10x with slots, structs, typed arrays |
| **Lazy evaluation** | Computing values that may not be needed | Avoids unnecessary computation and allocation |
| **Weak references** | Caching objects that can be recreated | Prevents memory leaks in caches |

#### Python Example: Generator for Memory Efficiency

```python
# BEFORE: Loads entire dataset into memory
def process_large_csv(filepath):
    with open(filepath) as f:
        reader = csv.DictReader(f)
        rows = list(reader)  # Loads ALL rows into memory

    results = []
    for row in rows:
        if float(row["amount"]) > 1000:
            results.append(transform(row))
    return results
# Memory: O(n) for n rows -- 10M rows = several GB


# AFTER: Generator processes one row at a time
def process_large_csv(filepath):
    def row_generator():
        with open(filepath) as f:
            reader = csv.DictReader(f)
            for row in reader:  # Yields one row at a time
                if float(row["amount"]) > 1000:
                    yield transform(row)

    return row_generator()
# Memory: O(1) -- constant regardless of file size
```

#### Java Example: Memory-Efficient Data Structure

```java
// BEFORE: Each Point object has 16 bytes overhead (object header) + 16 bytes data
// For 10M points: ~320 MB
List<Point> points = new ArrayList<>();
for (int i = 0; i < 10_000_000; i++) {
    points.add(new Point(xValues[i], yValues[i]));
}

// AFTER: Parallel arrays eliminate per-object overhead
// For 10M points: ~80 MB (just the raw doubles)
double[] xCoords = new double[10_000_000];
double[] yCoords = new double[10_000_000];
System.arraycopy(xValues, 0, xCoords, 0, 10_000_000);
System.arraycopy(yValues, 0, yCoords, 0, 10_000_000);
```

### Step 4: Optimize I/O Operations

I/O is typically the largest bottleneck in real-world applications.

#### I/O Optimization Strategies

| Strategy | Technique | Impact |
|----------|----------|--------|
| **Batching** | Combine multiple small I/O operations into fewer large ones | 10-100x for database writes |
| **Connection pooling** | Reuse connections instead of creating new ones | 5-50x for database/HTTP |
| **Async I/O** | Overlap I/O operations instead of waiting sequentially | 2-10x for multiple independent I/O |
| **Compression** | Compress data before network transfer | 2-10x for text-heavy payloads |
| **Pagination** | Fetch data in pages instead of all at once | Bounded memory, better time-to-first-result |
| **Selective loading** | Load only needed fields (SELECT specific columns, GraphQL) | 2-5x for wide tables |

#### Python Example: Batch Database Operations

```python
# BEFORE: Individual inserts -- 10K round trips to the database
def save_records(records, db):
    for record in records:
        db.execute(
            "INSERT INTO events (id, type, data) VALUES (?, ?, ?)",
            (record["id"], record["type"], json.dumps(record["data"]))
        )
    db.commit()
# 10K records = 10K round trips, ~30 seconds


# AFTER: Batch insert -- 1 round trip
def save_records(records, db):
    values = [
        (record["id"], record["type"], json.dumps(record["data"]))
        for record in records
    ]
    db.executemany(
        "INSERT INTO events (id, type, data) VALUES (?, ?, ?)",
        values
    )
    db.commit()
# 10K records = 1 round trip, ~0.3 seconds
```

#### JavaScript Example: Parallel Async I/O

```javascript
// BEFORE: Sequential fetches -- total time = sum of all fetch times
async function enrichUserProfiles(userIds) {
    const profiles = [];
    for (const id of userIds) {
        const user = await fetchUser(id);          // Wait for each one
        const orders = await fetchOrders(id);      // Then wait for this
        const preferences = await fetchPrefs(id);  // Then wait for this
        profiles.push({ ...user, orders, preferences });
    }
    return profiles;
}
// 100 users x 3 sequential calls x 100ms each = 30 seconds

// AFTER: Parallel fetches -- total time = max of all fetch times
async function enrichUserProfiles(userIds) {
    const profiles = await Promise.all(
        userIds.map(async (id) => {
            // All three fetches for each user run in parallel
            const [user, orders, preferences] = await Promise.all([
                fetchUser(id),
                fetchOrders(id),
                fetchPrefs(id),
            ]);
            return { ...user, orders, preferences };
        })
    );
    return profiles;
}
// 100 users x 1 parallel batch x 100ms = ~1 second (with connection pool)
```

### Step 5: Implement Caching

Caching eliminates redundant computation and I/O by storing and reusing results.

#### Caching Strategy Selection

| Cache Type | Use When | Invalidation Strategy |
|-----------|----------|----------------------|
| **In-memory (function-level)** | Pure function called repeatedly with same inputs | LRU eviction, TTL |
| **Application-level** | Expensive computation shared across requests | TTL, event-based invalidation |
| **Distributed (Redis, Memcached)** | Shared state across multiple server instances | TTL, explicit invalidation |
| **HTTP caching** | API responses or static assets | ETag, Cache-Control headers |
| **Query result cache** | Expensive database queries with stable results | TTL, write-through invalidation |

#### Python Example: Memoization with LRU Cache

```python
from functools import lru_cache
import time


# BEFORE: Recomputes expensive result every call
def get_exchange_rate(from_currency, to_currency):
    # Calls external API -- 200ms per call
    response = requests.get(f"https://api.rates.com/{from_currency}/{to_currency}")
    return response.json()["rate"]

def convert_prices(products, target_currency):
    for product in products:
        rate = get_exchange_rate(product.currency, target_currency)  # API call each time
        product.converted_price = product.price * rate
# 1000 products with 5 source currencies = 1000 API calls (but only 5 unique)


# AFTER: Cache exchange rates (TTL via maxsize, refresh externally)
@lru_cache(maxsize=128)
def get_exchange_rate(from_currency, to_currency):
    response = requests.get(f"https://api.rates.com/{from_currency}/{to_currency}")
    return response.json()["rate"]

def convert_prices(products, target_currency):
    for product in products:
        rate = get_exchange_rate(product.currency, target_currency)  # Cached after first call
        product.converted_price = product.price * rate
# 1000 products with 5 source currencies = 5 API calls (cache hits for rest)
```

#### Java Example: Application-Level Cache

```java
import com.github.benmanes.caffeine.cache.Cache;
import com.github.benmanes.caffeine.cache.Caffeine;
import java.time.Duration;

public class ProductService {
    private final Cache<String, ProductDetails> productCache = Caffeine.newBuilder()
        .maximumSize(10_000)
        .expireAfterWrite(Duration.ofMinutes(5))
        .recordStats()
        .build();

    public ProductDetails getProductDetails(String productId) {
        return productCache.get(productId, this::loadProductDetails);
    }

    private ProductDetails loadProductDetails(String productId) {
        // Expensive: joins 4 tables, calls pricing service, fetches inventory
        Product product = productRepository.findById(productId);
        Pricing pricing = pricingService.getPrice(productId);
        Inventory inventory = inventoryService.getStock(productId);
        return new ProductDetails(product, pricing, inventory);
    }

    // Invalidate on write
    public void updateProduct(String productId, ProductUpdate update) {
        productRepository.save(update);
        productCache.invalidate(productId);
    }
}
```

### Step 6: Leverage Concurrency

Use parallelism for CPU-bound work and async I/O for I/O-bound work.

#### Concurrency Decision Matrix

| Workload Type | Single-Threaded Bottleneck | Solution |
|--------------|---------------------------|---------|
| **CPU-bound, independent tasks** | One core idle per task | Multi-processing / thread pool |
| **I/O-bound, multiple sources** | Waiting for one I/O blocks others | Async I/O / event loop |
| **Mixed CPU + I/O** | Either CPU or I/O blocks | Async I/O for I/O, thread pool for CPU |
| **Pipeline processing** | Each stage waits for previous | Pipeline parallelism (producer-consumer) |

#### Python Example: Parallel Processing with ProcessPoolExecutor

```python
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing


def analyze_file(filepath):
    """CPU-intensive analysis of a single file."""
    with open(filepath) as f:
        content = f.read()
    # Expensive computation: parsing, analysis, etc.
    return {"file": filepath, "lines": content.count("\n"), "score": compute_score(content)}


# BEFORE: Sequential processing
def analyze_all_files(filepaths):
    return [analyze_file(fp) for fp in filepaths]
# 1000 files x 500ms each = 500 seconds


# AFTER: Parallel processing across CPU cores
def analyze_all_files(filepaths):
    results = []
    num_workers = multiprocessing.cpu_count()

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = {executor.submit(analyze_file, fp): fp for fp in filepaths}
        for future in as_completed(futures):
            results.append(future.result())

    return results
# 1000 files x 500ms / 8 cores = ~63 seconds
```

### Step 7: Measure and Validate

After optimizing, measure the improvement and verify correctness.

#### Optimization Report Template

```
## Optimization Report

### Target
- **Function/Module**: {name}
- **Problem**: {what was slow or resource-heavy}
- **Requirement**: {target latency, throughput, or memory limit}

### Profiling Results (Before)
- **Execution time**: {time}
- **Memory usage**: {peak memory}
- **I/O operations**: {count and total time}
- **Bottleneck**: {specific hotspot identified by profiler}

### Optimization Applied
- **Technique**: {what was changed and why}
- **Complexity change**: O({before}) to O({after})

### Results (After)
- **Execution time**: {time} ({percentage improvement})
- **Memory usage**: {peak memory} ({percentage change})
- **I/O operations**: {count and total time}
- **Correctness verified**: {test suite passed, output comparison}

### Trade-offs
- **Readability impact**: {none / minor / significant}
- **Maintenance cost**: {none / minor / significant}
- **Additional dependencies**: {none / list}
```

## Best Practices

- **Always profile first**: intuition about performance bottlenecks is wrong more often than it is right; measure to find the actual hotspot before changing any code
- **Optimize the bottleneck, not the whole program**: Amdahl's law dictates that optimizing code that accounts for 5% of execution time can yield at most a 5% improvement; focus on the dominant term
- **Prefer algorithmic improvements over micro-optimizations**: reducing O(n^2) to O(n log n) dwarfs any constant-factor improvement; always consider algorithmic complexity first
- **Benchmark with realistic data**: performance behavior often changes with data size and distribution; use production-representative data for benchmarks, not toy inputs
- **Keep the original code as a reference**: maintain the unoptimized version (commented or in version control) so that correctness can be verified by comparing outputs
- **Document why the optimization was necessary**: record the profiling results, the requirement that was not met, and the improvement achieved; without this context, future developers may simplify away the optimization
- **Set performance budgets**: define explicit latency, throughput, and memory targets before optimizing; stop when the target is met rather than pursuing diminishing returns
- **Test edge cases after optimization**: optimized code often handles edge cases differently; verify with empty inputs, single-element inputs, maximum-size inputs, and error conditions

## Common Pitfalls

- **Premature optimization**: optimizing code before profiling it wastes effort on non-bottlenecks and reduces readability for no measurable benefit; profile first, always
- **Optimizing for the wrong metric**: reducing CPU time when the bottleneck is I/O, or reducing latency when the requirement is throughput; clarify which metric matters before optimizing
- **Breaking correctness for performance**: an optimization that produces wrong results faster is not an optimization; always verify outputs match the original after optimizing
- **Ignoring cache invalidation**: caching without a clear invalidation strategy leads to stale data bugs that are difficult to reproduce and diagnose; define invalidation rules before implementing the cache
- **Over-parallelizing**: adding more threads or processes than available CPU cores causes context-switching overhead that can make performance worse; match parallelism to available resources
- **Micro-benchmarking without warm-up**: JIT-compiled languages (Java, JavaScript) need warm-up iterations before benchmark measurements are representative; cold-start times are misleading
- **Optimizing dead code paths**: spending time optimizing error handlers, admin endpoints, or rarely-executed branches has negligible impact on real-world performance; focus on hot paths
- **Not considering memory/CPU trade-offs**: caching reduces CPU time but increases memory; parallelism reduces wall-clock time but increases total CPU time; understand and accept the trade-off
- **Losing readability without measurement**: if the "optimized" code is harder to understand but benchmarks show no significant improvement, revert to the readable version
