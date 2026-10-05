---
name: performance-testing
description: Implement load testing, stress testing, benchmarking, and performance validation. Use when validating system performance, identifying bottlenecks.
---

# Performance Testing

Create comprehensive performance tests including load testing, stress testing, and benchmarking to validate system behavior under various conditions. This skill implements **Phase 5** of the 8-phase testing methodology.

## When to Use This Skill

Use this skill when you need to:

- Validate system performance requirements
- Identify performance bottlenecks
- Establish performance baselines
- Test system behavior under load
- Benchmark critical algorithms
- Measure response times and throughput
- Test scalability limits

**Trigger phrases**: "performance test", "load test", "stress test", "benchmark", "measure performance", "test throughput", "response time", "scalability test"

## What This Skill Does

### Performance Testing Types

| Type | Purpose | Duration | Load Pattern |
|------|---------|----------|--------------|
| **Load Testing** | Validate under expected load | Minutes-hours | Constant/stepped |
| **Stress Testing** | Find breaking points | Until failure | Increasing |
| **Spike Testing** | Handle sudden surges | Seconds-minutes | Sharp peaks |
| **Soak Testing** | Long-term stability | Hours-days | Constant |
| **Benchmark** | Compare implementations | Seconds | Fixed iterations |

### Language-Specific Examples

#### Python (pytest-benchmark + locust)

```python
import pytest
from myapp.algorithms import sort_data, search_data, process_batch

# ==================== BENCHMARKS ====================

class TestAlgorithmBenchmarks:
    """Benchmark tests for critical algorithms."""

    def test_sort_small_dataset(self, benchmark):
        """Benchmark sorting with small dataset."""
        data = list(range(1000, 0, -1))
        result = benchmark(sort_data, data)
        assert result == sorted(data)

    def test_sort_large_dataset(self, benchmark):
        """Benchmark sorting with large dataset."""
        data = list(range(100000, 0, -1))
        result = benchmark(sort_data, data)
        assert len(result) == 100000

    @pytest.mark.parametrize("size", [100, 1000, 10000])
    def test_search_performance(self, benchmark, size):
        """Benchmark search across different sizes."""
        data = list(range(size))
        target = size // 2
        result = benchmark(search_data, data, target)
        assert result == target

    def test_batch_processing_throughput(self, benchmark):
        """Measure batch processing throughput."""
        items = [{"id": i, "data": f"item_{i}"} for i in range(1000)]

        def process_all():
            return [process_batch(items[i:i+100]) for i in range(0, len(items), 100)]

        benchmark.pedantic(process_all, iterations=10, rounds=5)


# ==================== LOCUST LOAD TEST ====================
# locustfile.py

from locust import HttpUser, task, between

class APIUser(HttpUser):
    """Simulated API user for load testing."""
    wait_time = between(1, 3)

    def on_start(self):
        """Login at start of session."""
        response = self.client.post("/api/auth/login", json={
            "email": "loadtest@example.com",
            "password": "testpass123"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(3)
    def get_users(self):
        """Frequent: List users."""
        self.client.get("/api/users", headers=self.headers)

    @task(2)
    def get_user_detail(self):
        """Common: Get specific user."""
        self.client.get("/api/users/1", headers=self.headers)

    @task(1)
    def create_user(self):
        """Rare: Create new user."""
        self.client.post("/api/users", headers=self.headers, json={
            "name": "Load Test User",
            "email": f"loadtest_{time.time()}@example.com"
        })

    @task(1)
    def search_users(self):
        """Search with query parameter."""
        self.client.get("/api/users?q=test", headers=self.headers)
```

#### JavaScript/TypeScript (Artillery + Jest)

```javascript
// benchmark.test.ts
import { performance } from 'perf_hooks';
import { sortData, searchData, processBatch } from '../src/algorithms';

describe('Algorithm Benchmarks', () => {
  const benchmark = (fn: () => void, iterations: number = 1000): number => {
    const start = performance.now();
    for (let i = 0; i < iterations; i++) {
      fn();
    }
    return (performance.now() - start) / iterations;
  };

  it('sorts small dataset under 1ms', () => {
    const data = Array.from({ length: 1000 }, (_, i) => 1000 - i);
    const avgTime = benchmark(() => sortData([...data]), 100);
    expect(avgTime).toBeLessThan(1);
  });

  it('searches large dataset under 0.1ms', () => {
    const data = Array.from({ length: 100000 }, (_, i) => i);
    const avgTime = benchmark(() => searchData(data, 50000), 1000);
    expect(avgTime).toBeLessThan(0.1);
  });

  it('processes batch with acceptable throughput', () => {
    const items = Array.from({ length: 1000 }, (_, i) => ({ id: i }));
    const start = performance.now();
    processBatch(items);
    const duration = performance.now() - start;
    const throughput = items.length / (duration / 1000);
    expect(throughput).toBeGreaterThan(10000); // 10k items/sec
  });
});

// artillery.yml - Load test configuration
/*
config:
  target: "http://localhost:3000"
  phases:
    - duration: 60
      arrivalRate: 10
      name: "Warm up"
    - duration: 120
      arrivalRate: 50
      name: "Sustained load"
    - duration: 60
      arrivalRate: 100
      name: "Peak load"

scenarios:
  - name: "User workflow"
    flow:
      - post:
          url: "/api/auth/login"
          json:
            email: "test@example.com"
            password: "test123"
          capture:
            - json: "$.token"
              as: "authToken"
      - get:
          url: "/api/users"
          headers:
            Authorization: "Bearer {{ authToken }}"
      - get:
          url: "/api/users/1"
          headers:
            Authorization: "Bearer {{ authToken }}"
*/
```

#### Java (JMH)

```java
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.runner.Runner;
import org.openjdk.jmh.runner.options.Options;
import org.openjdk.jmh.runner.options.OptionsBuilder;
import java.util.concurrent.TimeUnit;

@State(Scope.Benchmark)
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MICROSECONDS)
@Warmup(iterations = 3, time = 1)
@Measurement(iterations = 5, time = 1)
@Fork(1)
public class AlgorithmBenchmark {

    @Param({"100", "1000", "10000"})
    private int size;

    private int[] data;

    @Setup
    public void setup() {
        data = new int[size];
        for (int i = 0; i < size; i++) {
            data[i] = size - i;
        }
    }

    @Benchmark
    public int[] benchmarkSort() {
        return Algorithms.sort(data.clone());
    }

    @Benchmark
    public int benchmarkSearch() {
        return Algorithms.binarySearch(data, size / 2);
    }

    @Benchmark
    @BenchmarkMode(Mode.Throughput)
    @OutputTimeUnit(TimeUnit.SECONDS)
    public void benchmarkBatchProcessing() {
        Algorithms.processBatch(data);
    }

    public static void main(String[] args) throws Exception {
        Options opt = new OptionsBuilder()
            .include(AlgorithmBenchmark.class.getSimpleName())
            .build();
        new Runner(opt).run();
    }
}
```

## Prerequisites

- Functional tests passing
- Understanding of performance requirements
- Production-like test environment
- Baseline metrics established

## Instructions

### Step 1: Define Performance Requirements

1. **Response Time Targets**
   - P50, P95, P99 latency
   - Maximum acceptable latency

2. **Throughput Targets**
   - Requests per second
   - Transactions per minute

3. **Resource Limits**
   - CPU utilization
   - Memory usage
   - Connection pools

### Step 2: Create Benchmarks

1. **Identify Critical Paths**
   - Hot code paths
   - Frequently called functions
   - Data processing algorithms

2. **Write Benchmark Tests**
   - Measure execution time
   - Track memory allocation
   - Compare implementations

### Step 3: Implement Load Tests

1. **Define Scenarios**
   - User workflows
   - API call patterns
   - Realistic data volumes

2. **Configure Load Profiles**
   - Ramp-up period
   - Sustained load
   - Peak scenarios

## Quality Checklist

- [ ] Performance requirements documented
- [ ] Critical paths benchmarked
- [ ] Load test scenarios defined
- [ ] Baseline metrics established
- [ ] Bottlenecks identified
- [ ] Results documented with graphs

## Related Skills

- `unit-tests` - Unit testing (Phase 2)
- `cicd-integration` - CI/CD setup (Phase 6)
- `code-coverage` - Coverage analysis (Phase 7)

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates tests_generation/performance_testing/


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
