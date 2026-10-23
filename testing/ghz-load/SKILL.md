---
name: ghz-load
description: "Wraps ghz, the gRPC load testing tool, for throughput and latency benchmarking. Covers test invocation (--proto + --call + host:port; or --protoset for compiled descriptors), load parameters (-n total requests, -c concurrency, -r RPS rate limit, -z duration), output formats (json/csv/html/influx-summary for CI consumption), the metrics reported (RPS achieved, latency p50/p95/p99, status-code distribution, errors), and CI integration patterns for regression gating. Use when benchmarking a gRPC service's throughput or detecting latency regressions in CI."
---

# ghz-load

## Overview

Per
[ghz.sh/docs/usage](https://ghz.sh/docs/usage), ghz accepts a
`.proto` (or compiled `protoset`), a method, a host:port, and
load parameters, and emits per-request metrics + a summary.
This skill wraps ghz for two use cases: ad-hoc throughput
measurement and CI regression gating.

## When to use

- New gRPC service - what's the throughput ceiling?
- Suspected latency regression - quantify before / after a
  change.
- CI gate: each PR runs a short ghz pass and fails if p99 exceeds
  the previous baseline.
- Capacity planning - at what concurrency does the service hit
  its CPU/memory ceiling?

## Authoring

### Install

Per [ghz.sh/docs/install](https://ghz.sh/docs/install):

```bash
# Homebrew
brew install ghz

# Go install
go install github.com/bojand/ghz/cmd/ghz@latest
```

Verify:

```bash
ghz --version
```

### Configure a `config.json`

Per ghz docs, `--config=path` reads a JSON / TOML config. For
reproducibility, commit it to the repo:

```json
{
  "proto": "./proto/user.proto",
  "import-paths": ["./proto", "./vendor"],
  "call": "user.v1.UserService/GetUser",
  "host": "localhost:8080",
  "insecure": true,
  "total": 10000,
  "concurrency": 50,
  "rps": 0,
  "data": {
    "id": "user-1"
  },
  "format": "json",
  "output": "ghz-report.json",
  "skipFirst": 100
}
```

`skipFirst: 100` discards the first 100 requests (cold-cache /
warmup). Set per-service.

## Running

### Basic load test

```bash
ghz --proto=./proto/user.proto \
    --call=user.v1.UserService/GetUser \
    --insecure \
    -n 10000 -c 50 \
    -d '{"id": "user-1"}' \
    localhost:8080
```

Per [ghz.sh/docs/usage](https://ghz.sh/docs/usage):

| Flag | Meaning |
|---|---|
| `--proto` | Path to the `.proto` file |
| `--protoset` | Path to a compiled descriptor set (alternative) |
| `--import-paths` | Comma-separated proto import paths |
| `--call` | `package.Service/Method` |
| `--insecure` | "Use plaintext and insecure connection" |
| `-n, --total=N` | "Number of requests to run. Default is 200" |
| `-c, --concurrency=N` | "Number of request workers to run concurrently" |
| `-r, --rps=N` | "Requests per second (RPS) rate limit"; 0 = unlimited |
| `-z, --duration=N` | Total duration (`30s`, `5m`) - alternative to `-n` |
| `-t, --timeout=N` | Per-request timeout (default `20s`) |
| `-d` | JSON message payload |
| `-D` | Path to a JSON file containing the payload |

### Rate-limited (RPS pinning)

```bash
ghz --proto=./proto/user.proto \
    --call=user.v1.UserService/GetUser \
    --insecure \
    -c 50 -z 60s -r 200 \
    -d '{"id":"user-1"}' \
    localhost:8080
```

Run for 60s, 50 concurrent workers, capped at 200 RPS. Useful
for confirming the service can sustain the target rate.

### Duration mode

```bash
ghz -z 5m -c 100 ...
```

When testing for stability / soak, `-z` beats `-n` - the test
ends after N minutes regardless of throughput.

### Streaming methods

Streaming RPCs aren't natively load-tested by ghz; it sends one
unary call per worker per request. For streaming load see
`grpc-streaming-test-author`.

## Parsing results

### Summary (default `summary` format)

```
Summary:
  Count:        10000
  Total:        20.45 s
  Slowest:      120.34 ms
  Fastest:      2.15 ms
  Average:      10.23 ms
  Requests/sec: 488.94
```

Status code distribution:

```
Status code distribution:
  [OK]            9983 responses
  [DeadlineExceeded] 17 responses
```

Per the status-code catalog in `grpc-streaming-test-author` (references/status-codes.md),
any non-`OK` is a flag for investigation.

### JSON output for CI consumption

```bash
ghz --config=ghz.config.json
# Writes ghz-report.json
```

Schema highlights:

```json
{
  "count": 10000,
  "total": 20450000000,
  "average": 10230000,
  "fastest": 2150000,
  "slowest": 120340000,
  "rps": 488.94,
  "latencyDistribution": [
    {"percentage": 50, "latency": 8000000},
    {"percentage": 95, "latency": 25000000},
    {"percentage": 99, "latency": 80000000}
  ],
  "statusCodeDistribution": {"OK": 9983, "DeadlineExceeded": 17},
  "errorDistribution": {}
}
```

Latencies are nanoseconds.

### Other formats

Per [ghz.sh/docs/usage](https://ghz.sh/docs/usage), `--format`
options: `summary` (default), `csv`, `json`, `pretty`, `html`,
`influx-summary`, `influx-details`. Use `html` for shareable
single-file reports; `influx-*` to ship metrics to InfluxDB.

## CI integration

### Baseline regression gate

```yaml
# .github/workflows/grpc-perf.yml
name: grpc-perf
on:
  pull_request:
    paths:
      - "service/**"
      - "proto/**"

jobs:
  ghz-baseline:
    runs-on: ubuntu-latest
    services:
      service-under-test:
        image: my-grpc-service:pr-${{ github.event.pull_request.number }}
        ports: [8080]
    steps:
      - uses: actions/checkout@v5
      - name: Install ghz
        run: |
          curl -L https://github.com/bojand/ghz/releases/download/v0.120.0/ghz-linux-x86_64.tar.gz | tar xz
          # user-owned bin dir on PATH: no sudo, no write to /usr/local/bin
          mkdir -p "$HOME/.local/bin" && mv ghz "$HOME/.local/bin/"
          echo "$HOME/.local/bin" >> "$GITHUB_PATH"
      - name: Warm + load
        run: |
          ghz --config=tests/perf/ghz.config.json
      - name: Restore baseline
        uses: actions/cache@v4
        with:
          path: baseline-ghz-report.json
          key: ghz-baseline-${{ github.base_ref }}
      - name: Compare
        run: python tests/perf/compare-ghz.py baseline-ghz-report.json ghz-report.json
```

`compare-ghz.py` checks p99 latency is within +10% of baseline;
fails otherwise:

```python
import json, sys

baseline = json.load(open(sys.argv[1]))
current = json.load(open(sys.argv[2]))

def p99(report):
    for entry in report["latencyDistribution"]:
        if entry["percentage"] == 99:
            return entry["latency"]
    return None

p99_baseline = p99(baseline) / 1_000_000  # ms
p99_current = p99(current) / 1_000_000
delta = (p99_current - p99_baseline) / p99_baseline

if delta > 0.10:
    print(f"❌ p99 regressed: {p99_baseline:.1f}ms → {p99_current:.1f}ms ({delta*100:.1f}%)")
    sys.exit(1)
print(f"✅ p99: {p99_baseline:.1f}ms → {p99_current:.1f}ms ({delta*100:+.1f}%)")
```

### Standalone benchmark report

```bash
ghz --config=ghz.config.json --format=html --output=ghz-report.html
```

Generate a single HTML report attached to the PR for human
review of distribution shape (long tail, bimodal, etc.).

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| `-n 100` for a "load test" | Sample size too small; metrics noisy | At least `-n 5000` or `-z 30s` |
| No `skipFirst` | Cold cache / JIT warmup inflates latencies | `skipFirst: ~5-10% of total` |
| Unbounded `--concurrency` | Tests the load generator, not the service | Match `-c` to expected production concurrency |
| Single-payload load test | Misses cache / branch-prediction noise | Vary `-d` payloads via `-D <file>` |
| Compare summary across runs without statistical context | Single-run noise → false regressions | Run N=3 times; compare distributions, not single numbers |
| `--insecure` against TLS-required services | Connection failure dominates results | Match prod TLS config |
| Treating non-OK as transport failure | Status codes have meaning per AIP-194 | Inspect distribution; classify per grpc-streaming-test-author references/status-codes.md |
| Load-testing on shared CI runner | Other jobs perturb CPU; noisy | Dedicated runner or isolate via Docker resource limits |

## Limitations

- **No streaming load.** ghz issues unary calls per worker. For
  server-streaming or bidi load, write a bespoke harness or use
  `grpc-streaming-test-author`.
- **No real-world workload mix.** All workers call the same
  method. For realistic load, run multiple ghz processes in
  parallel with different `--call` per process.
- **No replay from production traces.** ghz is generator-driven,
  not replay-driven. For replay see vegeta or k6.
- **Latency reported as one-way.** Network + serialisation +
  deserialisation included; can't isolate which dominates.
- **Auth tokens are static.** No token-refresh mid-test. Use
  long-lived test tokens.

## References

- ghz usage:
  [ghz.sh/docs/usage](https://ghz.sh/docs/usage).
- ghz install:
  [ghz.sh/docs/install](https://ghz.sh/docs/install).
- `$GITHUB_PATH` for a user-owned install dir in CI:
  [GitHub Actions: adding a system path](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands#adding-a-system-path).
- Status code interpretation:
  `grpc-streaming-test-author` (references/status-codes.md).
- Streaming load (sibling):
  `grpc-streaming-test-author`.
- Other load tools (cross-plugin, HTTP-focused; ghz is gRPC-specific):
  `k6-load-testing`,
  `jmeter-load-testing`.
