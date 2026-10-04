---
name: debugging
description: Analyzes stack traces, identifies log patterns, provides error solutions, and guides performance profiling, memory debugging, and distributed tracing. Use when debugging errors, analyzing logs, profiling performance, detecting memory leaks, or tracing distributed systems.
---

# Debugging

Systematic debugging assistance for stack traces, logs, performance, and distributed systems.

## Quick Start

**Analyze stack trace:**
```
Help me understand this stack trace and suggest fixes
```

**Profile performance:**
```
Help me profile this Node.js application for CPU bottlenecks
```

**Debug memory leak:**
```
I suspect a memory leak in this application, help me identify it
```

## Capabilities

### 1. Stack Trace Analysis

Parse and explain stack traces with actionable fix suggestions.

#### Stack Trace Anatomy

```javascript
// JavaScript/Node.js
Error: Cannot read property 'name' of undefined
    at getUserName (/app/src/utils/user.js:15:23)      // <- Origin
    at processUser (/app/src/services/user.js:42:12)   // <- Called by
    at handler (/app/src/routes/api.js:28:5)           // <- Called by
    at Layer.handle [as handle_request] (express/lib/router/layer.js:95:5)
```

**Analysis approach:**
1. **Error type and message**: What went wrong
2. **Origin line**: Where it happened (first app code line)
3. **Call chain**: How we got there
4. **Context**: What was the code trying to do

#### Common Error Patterns

| Error | Likely Cause | Fix |
|-------|--------------|-----|
| `Cannot read property 'x' of undefined` | Accessing property on null/undefined | Add null check or optional chaining |
| `is not a function` | Calling non-function or undefined | Verify import/export, check typos |
| `Maximum call stack exceeded` | Infinite recursion | Add base case, check recursive calls |
| `ECONNREFUSED` | Network connection failed | Check if service is running |
| `ENOENT` | File/directory not found | Verify path exists |

See [references/error-patterns.md](references/error-patterns.md) for comprehensive patterns.

---

### 2. Performance Profiling

Analyze CPU, memory, and I/O performance.

#### CPU Profiling

**Node.js:**
```bash
# Built-in profiler
node --prof app.js
node --prof-process isolate-*.log > profile.txt

# Chrome DevTools
node --inspect app.js
# Open chrome://inspect

# Clinic.js (visual)
npx clinic doctor -- node app.js
npx clinic flame -- node app.js
```

**Python:**
```bash
# cProfile
python -m cProfile -o output.prof script.py
python -m pstats output.prof

# py-spy (live sampling)
py-spy record -o profile.svg -- python app.py

# line_profiler
kernprof -l -v script.py
```

#### Profiling Analysis

```
Hot spots to look for:
1. Functions with high "self" time
2. Functions called very frequently
3. Deep call stacks
4. I/O blocking operations
5. JSON parsing/serialization
6. Regular expression matching
7. Memory allocation in loops
```

See [references/profiling-tools.md](references/profiling-tools.md) for language-specific tools.

---

### 3. Memory Leak Detection

Identify and fix memory leaks.

#### Memory Leak Patterns

**JavaScript/Node.js:**
```javascript
// LEAK: Growing array never cleared
const cache = [];
app.get('/data', (req, res) => {
  cache.push(processData(req));  // Never removed!
});

// LEAK: Event listeners not removed
element.addEventListener('click', handler);
// Missing: element.removeEventListener('click', handler);

// LEAK: Closures holding references
function createHandler() {
  const largeData = new Array(1000000);
  return () => {
    console.log(largeData.length);  // largeData never GC'd
  };
}

// LEAK: Timers not cleared
setInterval(() => {
  doSomething();
}, 1000);
// Missing: clearInterval(intervalId);
```

#### Heap Analysis

**Node.js:**
```bash
# Take heap snapshot
node --inspect app.js
# Chrome DevTools -> Memory -> Take snapshot

# Programmatic snapshot
const v8 = require('v8');
const fs = require('fs');

function takeHeapSnapshot() {
  const snapshotStream = v8.writeHeapSnapshot();
  console.log(`Heap snapshot written to ${snapshotStream}`);
}
```

**Analysis steps:**
1. Take snapshot at baseline
2. Perform suspected leaking operation
3. Force garbage collection
4. Take another snapshot
5. Compare snapshots for retained objects

#### Memory Debugging Tools

| Tool | Language | Use Case |
|------|----------|----------|
| Chrome DevTools | JavaScript | Heap snapshots, allocation timeline |
| Node.js --inspect | Node.js | Live debugging, heap analysis |
| memory_profiler | Python | Line-by-line memory usage |
| tracemalloc | Python | Memory allocation tracking |
| Valgrind | C/C++ | Memory leak detection |
| pprof | Go | CPU and memory profiling |

---

### 4. Network Debugging

Analyze request/response patterns and network issues.

#### Request/Response Analysis

**curl with timing:**
```bash
curl -w "\n\
  namelookup: %{time_namelookup}\n\
  connect: %{time_connect}\n\
  appconnect: %{time_appconnect}\n\
  pretransfer: %{time_pretransfer}\n\
  redirect: %{time_redirect}\n\
  starttransfer: %{time_starttransfer}\n\
  total: %{time_total}\n" \
  -o /dev/null -s "https://api.example.com/endpoint"
```

**HTTP debugging:**
```bash
# httpie (better than curl for APIs)
http GET https://api.example.com/users

# mitmproxy (intercept and inspect)
mitmproxy

# Charles Proxy (GUI)
# Wireshark (packet-level)
```

#### Common Network Issues

| Symptom | Possible Cause | Investigation |
|---------|----------------|---------------|
| Timeout | Slow server, network latency | Check server logs, trace route |
| Connection refused | Service down, wrong port | Verify service status, port |
| SSL errors | Certificate issues | Check cert validity, chain |
| 502/504 errors | Upstream issues | Check upstream service logs |
| Intermittent failures | DNS, load balancing | Check DNS TTL, LB health |

---

### 5. Database Debugging

Query analysis and performance optimization.

#### Slow Query Analysis

**PostgreSQL:**
```sql
-- Enable slow query logging
ALTER SYSTEM SET log_min_duration_statement = 1000;

-- Analyze query plan
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Find slow queries
SELECT query, calls, mean_time, total_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Find missing indexes
SELECT schemaname, tablename, seq_scan, seq_tup_read,
       idx_scan, idx_tup_fetch
FROM pg_stat_user_tables
WHERE seq_scan > idx_scan
ORDER BY seq_tup_read DESC;
```

**MySQL:**
```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;

-- Analyze query
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Show processlist
SHOW FULL PROCESSLIST;
```

#### Query Optimization

| Issue | Symptom | Fix |
|-------|---------|-----|
| Missing index | Seq scan on large table | Add index on filter columns |
| N+1 queries | Many similar queries | Use JOIN or eager loading |
| Large result set | Slow response, high memory | Add LIMIT, pagination |
| Lock contention | Timeouts, deadlocks | Reduce transaction scope |

---

### 6. CI/CD Debugging

Build failure analysis and pipeline troubleshooting.

#### Common CI Failures

| Failure Type | Symptoms | Investigation |
|--------------|----------|---------------|
| Dependency issues | Module not found | Check lock file, cache |
| Flaky tests | Random failures | Identify test, check timing |
| Resource limits | OOM, timeout | Increase limits, optimize |
| Permission issues | EACCES, 403 | Check credentials, roles |
| Environment issues | Works locally | Compare env vars, versions |

#### Debug Techniques

```bash
# SSH into CI runner (GitHub Actions)
# Add step to workflow:
- uses: mxschmitt/action-tmate@v3

# Print environment
env | sort

# Debug mode
set -x  # Bash verbose mode
DEBUG=* npm test  # Node.js debug

# Artifact collection
- uses: actions/upload-artifact@v4
  with:
    name: debug-logs
    path: |
      logs/
      coverage/
```

---

### 7. Browser DevTools Guidance

Client-side debugging techniques.

#### Console Methods

```javascript
// Beyond console.log
console.table(arrayOfObjects);      // Table format
console.group('Group name');        // Grouped logs
console.time('operation');          // Timing
console.timeEnd('operation');
console.trace();                    // Stack trace
console.assert(condition, 'msg');   // Conditional logging
console.dir(element, {depth: 2});   // Object inspection
```

#### Network Tab

```
Key information:
1. Request timing waterfall
2. Response headers and body
3. Request payload
4. CORS issues (blocked requests)
5. Cache behavior (304 vs 200)
```

#### Performance Tab

```
Recording analysis:
1. Main thread activity
2. Long tasks (>50ms)
3. Layout thrashing
4. Forced reflows
5. JavaScript execution time
```

---

### 8. Remote Debugging

Debug applications running on remote servers.

#### Node.js Remote Debugging

```bash
# Start with inspect on remote
node --inspect=0.0.0.0:9229 app.js

# SSH tunnel
ssh -L 9229:localhost:9229 user@remote

# Connect Chrome DevTools
chrome://inspect
```

#### Python Remote Debugging

```python
# debugpy (VS Code)
import debugpy
debugpy.listen(("0.0.0.0", 5678))
debugpy.wait_for_client()

# pdb remote
import pdb
import socket

# Then connect with: telnet remote 5555
```

---

### 9. Distributed Tracing

Debug requests across microservices.

#### Tracing Concepts

```
Request Flow:
Client -> Gateway -> ServiceA -> ServiceB -> Database
                           \
                            -> ServiceC -> External API

Trace: Single request journey through system
Span: Individual operation within a trace
Context: Trace ID propagated across services
```

#### OpenTelemetry Setup

**Node.js:**
```javascript
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { JaegerExporter } = require('@opentelemetry/exporter-jaeger');

const sdk = new NodeSDK({
  traceExporter: new JaegerExporter({
    endpoint: 'http://jaeger:14268/api/traces',
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();
```

**Python:**
```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

trace.set_tracer_provider(TracerProvider())
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)
```

See [references/distributed-tracing.md](references/distributed-tracing.md) for detailed setup.

---

### 10. Log Pattern Analysis

Identify patterns and anomalies in logs.

#### Pattern Detection

```bash
# Error frequency
grep -E "ERROR|Exception" logs.txt | sort | uniq -c | sort -rn

# Timeline analysis
grep "ERROR" logs.txt | cut -d' ' -f1-2 | uniq -c

# Correlation with events
grep -B5 -A5 "OutOfMemoryError" logs.txt
```

#### Log Analysis Checklist

```markdown
## Log Analysis: {Issue}

### Error Frequency
- [ ] How often does this error occur?
- [ ] Is it increasing, decreasing, or stable?
- [ ] When did it start?

### Error Context
- [ ] What operation triggered it?
- [ ] What user/request was involved?
- [ ] What were the input parameters?

### System State
- [ ] Resource usage (CPU, memory)?
- [ ] Database connections?
- [ ] External service health?

### Correlations
- [ ] Recent deployments?
- [ ] Traffic patterns?
- [ ] Other errors simultaneously?
```

---

## Debug Workflow

### Systematic Debug Process

```
1. REPRODUCE
   - Can you reproduce the issue?
   - What are the exact steps?
   - Is it consistent or intermittent?

2. ISOLATE
   - When did it start happening?
   - What changed recently?
   - Can you narrow down the scope?

3. GATHER
   - Collect stack traces
   - Review logs
   - Check system metrics

4. HYPOTHESIZE
   - What could cause this behavior?
   - What's the most likely cause?
   - What can you rule out?

5. TEST
   - Test your hypothesis
   - Add logging if needed
   - Try a fix in isolation

6. FIX
   - Implement the fix
   - Verify in development
   - Add tests to prevent regression

7. DOCUMENT
   - What was the root cause?
   - How was it fixed?
   - How to prevent in future?
```

---

## Debug Report Template

```markdown
# Debug Report: {Issue Title}

## Summary
{One-line description of the issue}

## Symptoms
- {Observable symptom 1}
- {Observable symptom 2}

## Environment
- Environment: {production/staging/development}
- Version: {app version}
- OS: {operating system}

## Timeline
- {timestamp}: {event}
- {timestamp}: {event}

## Error Details
```
{Stack trace or error message}
```

## Analysis
{Your analysis of the root cause}

## Solution
{How you fixed it}

## Prevention
- {How to prevent this in the future}
- {Tests or monitoring to add}
```

---

## Hook Integration

### Notification Hook - Error Pattern Alerts

Alert on recurring error patterns:

```json
{
  "hooks": {
    "Notification": [{
      "matcher": "",
      "command": "check-error-patterns.sh",
      "condition": "contains(message, 'Error') || contains(message, 'Exception')"
    }]
  }
}
```

**Script example:**
```bash
#!/bin/bash
# check-error-patterns.sh

ERROR_MSG="$1"

# Known error patterns with solutions
patterns=(
  "ECONNREFUSED|Check if the service is running"
  "OutOfMemoryError|Consider increasing heap size or checking for leaks"
  "ETIMEDOUT|Check network connectivity and timeout settings"
  "ENOENT|Verify file path exists"
)

for pattern in "${patterns[@]}"; do
  IFS='|' read -r regex suggestion <<< "$pattern"
  if echo "$ERROR_MSG" | grep -qE "$regex"; then
    echo "ALERT: Known error pattern detected"
    echo "Suggestion: $suggestion"
  fi
done
```

**Hook response pattern:**
```typescript
interface ErrorPatternAlert {
  pattern: string;
  frequency: number;
  suggestion: string;
  relatedDocs?: string[];
}
```

### PostToolUse Hook - Automatic Log Collection

After errors, collect relevant logs:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Bash",
      "command": "collect-debug-info.sh",
      "condition": "exitCode != 0"
    }]
  }
}
```

## CI/CD Integration

### GitHub Actions - Debug Artifacts

```yaml
name: Debug on Failure
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run tests
        id: test
        run: npm test
        continue-on-error: true

      - name: Collect debug info on failure
        if: steps.test.outcome == 'failure'
        run: |
          mkdir -p debug-artifacts
          npm run test -- --verbose > debug-artifacts/test-output.log 2>&1
          cat /var/log/syslog | tail -100 > debug-artifacts/syslog.log
          free -m > debug-artifacts/memory.log
          df -h > debug-artifacts/disk.log

      - name: Upload debug artifacts
        if: steps.test.outcome == 'failure'
        uses: actions/upload-artifact@v4
        with:
          name: debug-artifacts
          path: debug-artifacts/

      - name: Fail if tests failed
        if: steps.test.outcome == 'failure'
        run: exit 1
```

### Pre-commit Debug Check

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for debug statements
debug_patterns="console\.log|debugger|pdb\.set_trace|breakpoint\(\)"

if git diff --cached | grep -E "$debug_patterns"; then
  echo "WARNING: Debug statements detected in staged changes"
  echo "Remove before committing:"
  git diff --cached --name-only | xargs grep -n -E "$debug_patterns"
  exit 1
fi
```

## Reference Files

- [references/error-patterns.md](references/error-patterns.md) - Common error patterns by language/framework
- [references/profiling-tools.md](references/profiling-tools.md) - Profiling tools by language
- [references/distributed-tracing.md](references/distributed-tracing.md) - Distributed tracing setup guides

## Scripts

- [scripts/log_analyzer.py](scripts/log_analyzer.py) - Log pattern analysis utility
