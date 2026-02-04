---
name: benchmark
description: Benchmark HBF performance using Apache Bench (ab). Measures static asset serving, versioned filesystem operations, and QuickJS runtime routes. Maintains historical data for performance tracking over time.
---

# HBF Benchmark Skill

This skill provides reproducible performance benchmarking for HBF using Apache Bench (ab). It tests three main categories of operations and maintains historical data for comparison over time.

## Benchmark Categories

### 1. Static Assets (latest_fs reads)
Tests serving static files from the embedded SQLite database via the `latest_files` view.

**Endpoints:**
- `/static/style.css` - Small CSS file
- `/static/favicon.ico` - Empty file

### 2. QuickJS Runtime Routes
Tests endpoints that require QuickJS execution and JSON serialization.

**Endpoints:**
- `/hello` - Simple JSON response
- `/user/42` - Parameterized route with path parsing
- `/echo` - Echo endpoint reflecting request details

## Benchmark Parameters

Default test parameters (configurable):
- **Requests:** 1,000 requests per endpoint
- **Concurrency:** 10 concurrent connections
- **Port:** 5309 (HBF default)

These defaults provide faster test runs while maintaining statistical validity.

## Historical Data Storage

Results are stored in `/workspaces/hbf/.benchmark/results.db` using SQLite:

```sql
CREATE TABLE IF NOT EXISTS benchmark_runs (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    git_commit TEXT,
    git_branch TEXT,
    build_mode TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS benchmark_results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    requests INTEGER NOT NULL,
    concurrency INTEGER NOT NULL,
    time_taken REAL NOT NULL,
    requests_per_sec REAL NOT NULL,
    time_per_request REAL NOT NULL,
    transfer_rate REAL NOT NULL,
    failed_requests INTEGER NOT NULL,
    FOREIGN KEY (run_id) REFERENCES benchmark_runs(run_id)
);
```

## Usage

When you invoke this skill, it will:

1. **Build HBF binary** (optimized release mode by default)
2. **Start server** in background on port 5309
3. **Run benchmarks** for all endpoints across three categories
4. **Store results** in historical database
5. **Display summary** with comparison to previous runs
6. **Clean up** (stop server, save results)

## Commands

### Run Full Benchmark Suite

```bash
# Default: 1k requests, concurrency 10
./benchmark.sh

# Custom parameters
./benchmark.sh --requests 50000 --concurrency 50

# With build mode specification
./benchmark.sh --build-mode opt --requests 10000

# Add notes for this run
./benchmark.sh --notes "After QuickJS optimization"
```

### View Historical Results

```bash
# Show recent benchmark runs
./show_results.sh

# Compare specific runs
./show_results.sh --compare run1 run2

# Show trend for specific endpoint
./show_results.sh --trend /hello
```

## Benchmark Script Implementation

The main `benchmark.sh` script performs:

1. **Environment setup**
   - Check prerequisites (ab, sqlite3)
   - Initialize results database
   - Get git metadata (commit, branch)

2. **Build binary**
   - `bazel build //:hbf --compilation_mode=opt`
   - Use consistent build flags for reproducibility

3. **Start server**
   - Launch in background with `--port 5309`
   - Wait for health check

4. **Run benchmarks**
   - Category 1: Static assets
   - Category 2: QuickJS routes

5. **Parse results**
   - Extract key metrics from ab output
   - Store in SQLite database

6. **Generate report**
   - Summary table with all endpoints
   - Comparison with previous run (if available)
   - Highlight regressions/improvements

7. **Cleanup**
   - Kill background servers
   - Save database

## Output Format

The skill generates a markdown-formatted report:

```
# HBF Benchmark Results

**Run ID:** 42
**Timestamp:** 2025-01-15 10:30:00
**Commit:** abc1234
**Branch:** main
**Build Mode:** opt

## Summary

| Category | Endpoint | Req/sec | Avg Time (ms) | Failed |
|----------|----------|---------|---------------|--------|
| Static | /static/style.css | 45,230 | 0.22 | 0 |
| Runtime | /hello | 38,500 | 0.26 | 0 |
| Runtime | /user/42 | 37,800 | 0.26 | 0 |
| FS Write | PUT /__dev/api/file | 8,500 | 1.18 | 0 |

## Comparison with Previous Run

| Endpoint | Previous | Current | Change |
|----------|----------|---------|--------|
| /hello | 38,200 | 38,500 | +0.8% 📈 |
| /static/style.css | 44,800 | 45,230 | +1.0% 📈 |

## Recommendations

✅ All endpoints performing within expected ranges
⚠️  Consider investigating if any regressions > 5%
```

## Files

This skill includes:

- `SKILL.md` (this file) - Skill documentation
- `benchmark.sh` - Main benchmark runner script
- `show_results.sh` - Historical results viewer
- `lib/db.sh` - Database operations helper
- `lib/server.sh` - Server lifecycle management
- `lib/parser.sh` - Apache Bench output parser

## Prerequisites

- Apache Bench (`ab`) installed (included in apache2-utils)
- SQLite3 CLI (`sqlite3`)
- Bazel build system
- Git (for commit metadata)

## Reproducibility

For reproducible benchmarks:

1. **Consistent environment:** Run on same hardware/VM
2. **Isolated execution:** Close other applications
3. **Fixed parameters:** Use same request count and concurrency
4. **Build mode:** Use `--compilation_mode=opt` for release builds
5. **System state:** Run when system is idle (low load)

## Tips

- Run benchmarks multiple times and average results
- Use `--notes` to document changes between runs
- Compare similar build modes (opt vs opt, dbg vs dbg)
- Watch for failed requests (should always be 0)
- Monitor system resources during benchmark

## Example Workflow

```bash
# Initial baseline
./benchmark.sh --notes "Baseline before optimization"

# Make code changes...
# (edit versioned filesystem code)

# Run new benchmark
./benchmark.sh --notes "After index optimization"

# Compare results
./show_results.sh --compare $(sqlite3 .benchmark/results.db "SELECT run_id FROM benchmark_runs ORDER BY run_id DESC LIMIT 2")
```

## Performance Expectations

Typical performance on modern hardware (2020+ CPU):

- **Static assets:** 40,000-60,000 req/sec
- **QuickJS routes:** 30,000-50,000 req/sec
- **FS writes:** 5,000-10,000 req/sec (limited by SQLite WAL)
- **FS reads:** 35,000-50,000 req/sec

Lower performance may indicate:
- Debug build mode (use `--compilation_mode=opt`)
- High system load
- Disk I/O bottlenecks
- Memory pressure

## Limitations

- Tests only GET and PUT operations (no DELETE benchmarks)
- Single-threaded HBF server (one core utilized)
- Local benchmarking only (no network latency)
- SQLite WAL mode may affect write performance
- Apache Bench limitation: cannot test SSE endpoints

## Future Enhancements

Potential improvements:
- Add percentile latency measurements (p50, p95, p99)
- Test different concurrency levels automatically
- Add memory profiling integration
- Support custom pod benchmarking
- Add warmup phase before measurements
- Export results to CSV/JSON for external analysis
