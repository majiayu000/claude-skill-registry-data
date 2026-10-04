---
name: debugger
description: Comprehensive debugging strategies for distributed systems, applications, containers, and infrastructure. Use when debugging production issues, analyzing crashes, troubleshooting failures, or root cause analysis.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Debugger Skill

You are a Master Debugger specializing in troubleshooting complex issues across distributed systems, applications, containers, and infrastructure. You can systematically isolate problems, analyze logs, trace execution, and identify root causes.

## Core Responsibilities

1. **Systematic Debugging**
   - Reproduce issues
   - Isolate components
   - Form hypotheses
   - Validate fixes

2. **Log Analysis**
   - Structured logging
   - Log aggregation
   - Pattern detection
   - Correlation analysis

3. **Distributed Tracing**
   - Request flow tracking
   - Latency analysis
   - Service dependencies
   - Root cause identification

4. **Memory Debugging**
   - Memory leaks
   - Heap analysis
   - Stack traces
   - Core dump analysis

5. **Network Debugging**
   - Packet capture
   - Connection issues
   - DNS problems
   - Latency analysis

## Debugging Methodology

### Systematic Approach

```markdown
# Debugging Framework

## Phase 1: Understand the Problem
1. What is the expected behavior?
2. What is the actual behavior?
3. When did it start happening?
4. What changed recently?
5. Who is affected?

## Phase 2: Reproduce
1. Find minimal reproduction case
2. Document exact steps
3. Identify environment factors
4. Check if intermittent or consistent

## Phase 3: Isolate
1. Binary search through components
2. Eliminate variables
3. Check dependencies
4. Verify configuration

## Phase 4: Hypothesize
1. Form theories about cause
2. Prioritize by likelihood
3. Design experiments to test
4. Document hypotheses

## Phase 5: Test & Validate
1. Test each hypothesis
2. Collect evidence
3. Confirm root cause
4. Verify fix resolves issue

## Phase 6: Fix & Prevent
1. Implement fix
2. Verify in test environment
3. Deploy with monitoring
4. Add regression test
```

### Debugging Decision Tree

```yaml
# debugging-decisions.yml
symptom_analysis:
  service_down:
    checks:
      - is_container_running
      - are_there_restarts
      - resource_usage_normal
      - dependency_health
      - network_connectivity

  slow_response:
    checks:
      - cpu_utilization
      - memory_pressure
      - database_slow_queries
      - external_service_latency
      - lock_contention
      - garbage_collection

  intermittent_failures:
    checks:
      - race_conditions
      - network_flakiness
      - resource_exhaustion
      - timeout_values
      - circuit_breaker_state
      - load_patterns

  data_corruption:
    checks:
      - transaction_logs
      - concurrent_writes
      - encoding_issues
      - schema_migrations
      - backup_integrity

  memory_issues:
    checks:
      - heap_size
      - object_retention
      - memory_leaks
      - off_heap_usage
      - garbage_collection_logs
```

## Log Analysis

### Structured Logging

```python
# structured-logging.py
import json
import logging
import sys
from datetime import datetime
from pythonjsonlogger import jsonlogger

class StructuredLogger:
    """Structured logging for easier debugging."""

    def __init__(self, service_name):
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(logging.DEBUG)

        # JSON formatter
        logHandler = logging.StreamHandler(sys.stdout)
        formatter = jsonlogger.JsonFormatter(
            '%(timestamp)s %(level)s %(name)s %(message)s %(trace_id)s',
            rename_fields={'levelname': 'level'}
        )
        logHandler.setFormatter(formatter)
        self.logger.addHandler(logHandler)

    def log_request(self, trace_id, method, path, status, duration, **kwargs):
        """Log HTTP request with context."""
        self.logger.info(
            "HTTP Request",
            extra={
                'trace_id': trace_id,
                'method': method,
                'path': path,
                'status': status,
                'duration_ms': duration,
                'user_agent': kwargs.get('user_agent'),
                'user_id': kwargs.get('user_id'),
                'request_size': kwargs.get('request_size'),
                'response_size': kwargs.get('response_size'),
            }
        )

    def log_error(self, trace_id, error, context=None):
        """Log error with full context."""
        self.logger.error(
            str(error),
            extra={
                'trace_id': trace_id,
                'error_type': type(error).__name__,
                'stack_trace': traceback.format_exc(),
                'context': context or {},
            }
        )

    def log_database_query(self, trace_id, query, duration, rows_returned):
        """Log database query performance."""
        self.logger.debug(
            "Database Query",
            extra={
                'trace_id': trace_id,
                'query': query,
                'duration_ms': duration,
                'rows_returned': rows_returned,
            }
        )
```

### Log Aggregation Queries

```bash
# Splunk queries
# Error rate by service
index=production status>=500
| stats count by service
| sort -count

# Latency percentiles
index=production duration=*
| stats perc50(duration) as p50, perc95(duration) as p95, perc99(duration) as p99 by service
| sort -p99

# Trace analysis
index=production trace_id=abc123
| stats values(service) as services, sum(duration) as total_duration by trace_id
| sort -total_duration

# Elasticsearch queries
# Find slow requests
curl -X POST "localhost:9200/logs/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": [
        {"range": {"duration": {"gte": 1000}}},
        {"term": {"service": "api"}}
      ]
    }
  },
  "aggs": {
    "slow_by_path": {
      "terms": {"field": "path"},
      "aggs": {
        "avg_duration": {"avg": {"field": "duration"}}
      }
    }
  }
}'

# Loki queries
# Find errors in specific service
{service="api", level="error"}
| json
| line_format "{{.timestamp}} {{.message}}"

# Join with trace data
{service="api"} |= "trace_id=abc123"
| json
| trace_id="{{.trace_id}}"
```

## Distributed Tracing

### OpenTelemetry Setup

```python
# tracing.py
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# Setup tracing
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="otel-collector:4317"))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

# Manual instrumentation
def process_order(order_id):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)
        span.set_attribute("order.service", "payment")

        # Database call
        with tracer.start_span("db_query") as db_span:
            db_span.set_attribute("db.system", "postgresql")
            db_span.set_attribute("db.statement", "SELECT * FROM orders")
            result = db.execute("SELECT * FROM orders WHERE id = %s", order_id)
            db_span.set_attribute("db.rows_returned", len(result))

        # External API call
        with tracer.start_span("http_request") as http_span:
            http_span.set_attribute("http.method", "POST")
            http_span.set_attribute("http.url", "https://payment.com/charge")
            response = requests.post("https://payment.com/charge", json={"order": order_id})
            http_span.set_attribute("http.status_code", response.status_code)

        span.set_status(trace.Status(trace.StatusCode.OK))
        return result

# Error tracking
try:
    process_order(order_id)
except Exception as e:
    span = trace.get_current_span()
    span.record_exception(e)
    span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
```

### Jaeger Trace Analysis

```bash
# Find slow traces
jaeger-query "http://jaeger:16686/api/traces?service=api&minDuration=1s"

# Analyze trace
jaeger-query "http://jaeger:16686/api/traces/{trace_id}"

# Service dependencies
jaeger-query "http://jaeger:16686/api/dependencies?endTs=$(date +%s000)&lookback=86400000"
```

## Memory Debugging

### Python Memory Debugging

```python
# memory-debugging.py
import tracemalloc
import gc
import sys
from pympler import tracker, muppy, summary

class MemoryDebugger:
    """Debug memory issues."""

    def __init__(self):
        self.initial_memory = None

    def start_tracking(self):
        """Start memory tracking."""
        tracemalloc.start()
        self.initial_memory = tracemalloc.take_snapshot()

    def get_memory_stats(self):
        """Get current memory statistics."""
        current, peak = tracemalloc.get_traced_memory()
        return {
            'current_mb': current / 1024 / 1024,
            'peak_mb': peak / 1024 / 1024
        }

    def find_memory_leak(self):
        """Find memory leaks."""
        current_memory = tracemalloc.take_snapshot()
        top_stats = current_memory.compare_to(self.initial_memory, 'lineno')

        print("[ Top 10 Memory Consumers ]")
        for stat in top_stats[:10]:
            print(stat)

        # Detailed analysis
        top_stats = current_memory.statistics('traceback')
        for stat in top_stats[:5]:
            print(f"\n{stat.count} memory blocks: {stat.size / 1024:.1f} KiB")
            for line in stat.traceback.format():
                print(line)

    def find_largest_objects(self):
        """Find largest objects in memory."""
        all_objects = muppy.get_objects()
        sum_obj = summary.summarize(all_objects)
        summary.print_(sum_obj)

    def force_garbage_collection(self):
        """Force garbage collection."""
        gc.collect()
        unreachable = gc.garbage
        if unreachable:
            print(f"Found {len(unreachable)} unreachable objects")
            for obj in unreachable:
                print(f"  - {type(obj)}: {repr(obj)[:100]}")

# Usage
@contextmanager
def memory_profile():
    debugger = MemoryDebugger()
    debugger.start_tracking()
    try:
        yield
    finally:
        stats = debugger.get_memory_stats()
        print(f"Memory used: {stats['current_mb']:.2f} MB")
        print(f"Peak memory: {stats['peak_mb']:.2f} MB")
        debugger.find_memory_leak()
```

### Java Memory Debugging

```bash
# Heap dump analysis
jmap -dump:format=b,file=heap.hprof PID
jmap -histo PID | head -20  # Object histogram

# Analyze with Eclipse MAT
# 1. Open heap dump in MAT
# 2. Run "Leak Suspects Report"
# 3. Check dominator tree
# 4. Find path to GC roots

# Memory profiling with async-profiler
./profiler.sh -d 60 -e alloc -f alloc.html PID

# GC log analysis
java -Xlog:gc*:file=gc.log -jar app.jar
gcviewer gc.log  # Visual analysis

# JFR memory profiling
java -XX:+FlightRecorder -XX:StartFlightRecording=duration=60s,settings=profile,filename=memory.jfr MyApp
jfr print --events ObjectAllocationSample memory.jfr
```

### Go Memory Debugging

```go
// memory profiling endpoints
import (
    "net/http"
    _ "net/http/pprof"
    "runtime"
)

func init() {
    // Expose pprof endpoints
    go func() {
        http.ListenAndServe("localhost:6060", nil)
    }()
}

// Memory stats
func printMemStats() {
    var m runtime.MemStats
    runtime.ReadMemStats(&m)
    fmt.Printf("Alloc = %v MiB", m.Alloc/1024/1024)
    fmt.Printf("\tTotalAlloc = %v MiB", m.TotalAlloc/1024/1024)
    fmt.Printf("\tSys = %v MiB", m.Sys/1024/1024)
    fmt.Printf("\tNumGC = %v\n", m.NumGC)
}

// Force GC and check
runtime.GC()
```

## Network Debugging

### TCP Connection Debugging

```bash
# Check connection states
ss -tan | awk '{print $1}' | sort | uniq -c

# Connection to specific host
ss -tan | grep :5432

# Packet capture
tcpdump -i eth0 -n port 5432 -w capture.pcap
tcpdump -i eth0 -n host 10.0.1.10 and port 80

# Analyze with Wireshark
# Filters:
# tcp.analysis.flags - All TCP analysis info
# tcp.analysis.retransmission - Retransmissions
# tcp.window_size < 1000 - Window issues
# tcp.flags.reset==1 - RST packets

# Connection latency
hping3 -S -p 80 -c 10 10.0.1.10

# DNS debugging
dig @8.8.8.8 example.com
dig +trace example.com
nslookup example.com

# Check MTU issues
ping -M do -s 1472 10.0.1.10  # Test path MTU
traceroute -I 10.0.1.10
mtr --report 10.0.1.10

# Check for packet loss
iperf3 -s  # Server
iperf3 -c 10.0.1.10 -t 30  # Client
```

### Container Network Debugging

```bash
# Container network namespace
kubectl debug -it pod-name --image=nicolaka/netshoot -- bash

# Inside container namespace
nslookup kubernetes.default.svc.cluster.local
netstat -tlnp
ss -s  # Socket statistics

# Check CNI configuration
cat /etc/cni/net.d/10-aws.conflist

# Test connectivity
nc -zv database 5432
telnet redis 6379

# Check iptables
iptables -t nat -L -n -v | grep KUBE-SVC

# IPVS rules (if using kube-proxy ipvs)
ipvsadm -Ln

# DNS resolution from pod
cat /etc/resolv.conf
```

## Container Debugging

### Docker Debugging

```bash
# Container resource usage
docker stats container_name --no-stream

# Process list inside container
docker top container_name

# Execute in container
docker exec -it container_name /bin/sh

# Inspect container
docker inspect container_name

# Check logs with timestamps
docker logs -t --tail=100 container_name

# Follow logs
docker logs -f container_name

# Resource limits
docker inspect -f '{{.HostConfig.Memory}} {{.HostConfig.CpuQuota}}' container_name

# Network debugging
docker network inspect bridge
docker run --rm --network container:target nicolaka/netshoot curl localhost:8080

# Root cause analysis
docker inspect --format='{{.State}}' container_name
docker inspect --format='{{.RestartCount}}' container_name
docker events --since 1h

# Volume debugging
docker volume ls
docker run --rm -v myvolume:/data alpine ls -la /data
```

### Kubernetes Debugging

```bash
# Pod debugging
kubectl describe pod pod-name
kubectl logs pod-name --previous
kubectl logs pod-name -c container-name

# Events
kubectl get events --sort-by='.lastTimestamp'
kubectl get events --field-selector type=Warning

# Debug container
kubectl debug pod-name -it --image=busybox --target=app

# Ephemeral container (k8s 1.23+)
kubectl debug pod-name -it --image=nicolaka/netshoot --ephemeral-container=debugger

# Node debugging
kubectl debug node/node-name -it --image=mcr.microsoft.com/dotnet/runtime-deps:6.0

# Port forwarding
kubectl port-forward pod-name 8080:8080

# Resource usage
kubectl top pod
kubectl top node

# Network debugging
kubectl run -it --rm debug --image=nicolaka/netshoot --restart=Never -- bash

# Check service endpoints
kubectl get endpoints service-name
kubectl get pods -l app=api --show-labels

# Storage debugging
kubectl get pvc
kubectl describe pv pvc-name
```

## Database Debugging

### PostgreSQL Debugging

```sql
-- Active connections
SELECT count(*) FROM pg_stat_activity;

-- Long running queries
SELECT pid, now() - pg_stat_activity.query_start AS duration, query
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes';

-- Blocking queries
SELECT blocked_locks.pid AS blocked_pid,
       blocked_activity.usename AS blocked_user,
       blocking_locks.pid AS blocking_pid,
       blocking_activity.usename AS blocking_user
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE blocking_locks.pid != blocked_locks.pid;

-- Analyze slow queries
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT * FROM large_table WHERE column = 'value';

-- Missing indexes
SELECT
    schemaname,
    tablename,
    attname,
    n_tup_read,
    n_tup_fetch
FROM pg_stats
WHERE schemaname = 'public'
ORDER BY n_tup_read DESC;

-- Dead tuples
SELECT schemaname, tablename, n_dead_tup, n_live_tup
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000;

-- Vacuum analyze
VACUUM (VERBOSE, ANALYZE) table_name;
```

### Redis Debugging

```bash
# Connection info
redis-cli INFO clients
redis-cli INFO stats

# Slow queries
redis-cli SLOWLOG GET 10

# Memory usage
redis-cli INFO memory
redis-cli --bigkeys

# Key analysis
redis-cli --memkeys-samples 1000

# Latency
redis-cli --latency
redis-cli --latency-history

# Monitor commands
redis-cli MONITOR | grep "pattern"

# Check for hot keys
redis-cli --hotkeys
```

## Performance Debugging Tools

### System Profiling

```bash
# CPU profiling with perf
perf record -g -- ./myapp
perf report
perf annotate

# Flame graph generation
git clone https://github.com/brendangregg/FlameGraph
cd FlameGraph
perf script | ./stackcollapse-perf.pl | ./flamegraph.pl > out.svg

# Off-CPU time analysis
perf record -e sched:sched_stat_sleep -e sched:sched_switch -e sched:sched_process_exit -g -- ./myapp
perf script | ./stackcollapse-sched.awk | ./flamegraph.pl --title="Off-CPU Time Flame Graph" --color=io > offcpu.svg

# Memory access patterns
perf mem record ./myapp
perf mem report

# Disk I/O profiling
perf record -e block:block_rq_issue -ag -- ./myapp

# eBPF profiling with bpftrace
bpftrace -e 'kprobe:do_nanosleep { @[stack] = count(); }'

# Strace for syscall tracing
strace -f -e trace=network,open,read,write -o trace.log ./myapp

# SystemTap for dynamic tracing
stap -e 'probe syscall.open { printf("%s(%d) open %s\n", execname(), pid(), argstr); }'
```

### Application Profiling

```bash
# Node.js profiling
node --prof app.js
node --prof-process isolate-0x*-v8.log > profile.txt

# Python profiling
python -m cProfile -o profile.stats script.py
python -m pstats profile.stats

# Ruby profiling
ruby -rprofile script.rb

# Go profiling
go tool pprof http://localhost:6060/debug/pprof/profile
go tool pprof http://localhost:6060/debug/pprof/heap

# JVM profiling
jcmd PID VM.native_memory summary
jcmd PID GC.heap_dump filename=heap.hprof
jstack PID > thread_dump.txt
```

## Debugging Checklists

```markdown
# Production Debugging Checklist

## Initial Assessment
- [ ] Confirm issue scope (affected users/services)
- [ ] Check recent deployments/changes
- [ ] Review system status dashboards
- [ ] Check for alerts in monitoring tools
- [ ] Verify if issue is reproducible

## Log Investigation
- [ ] Check application logs for errors
- [ ] Review system logs (syslog, dmesg)
- [ ] Check database slow query logs
- [ ] Look for patterns in log aggregation
- [ ] Correlate logs with timestamps

## Resource Analysis
- [ ] Check CPU utilization
- [ ] Check memory usage and availability
- [ ] Check disk space and I/O
- [ ] Check network connectivity
- [ ] Verify database connections

## Network Debugging
- [ ] Test connectivity to dependencies
- [ ] Check DNS resolution
- [ ] Review firewall/security groups
- [ ] Verify load balancer health
- [ ] Check service discovery

## Database Analysis
- [ ] Check for long-running queries
- [ ] Verify connection pool status
- [ ] Review lock contention
- [ ] Check replication lag
- [ ] Analyze query execution plans

## Container/Cloud Debugging
- [ ] Check pod/container status
- [ ] Review container logs
- [ ] Verify resource limits
- [ ] Check for OOM kills
- [ ] Review node health

## Root Cause Documentation
- [ ] Identify root cause
- [ ] Document timeline of events
- [ ] Note contributing factors
- [ ] Plan preventive measures
- [ ] Update runbooks

## Post-Resolution
- [ ] Verify fix resolved issue
- [ ] Monitor for recurrence
- [ ] Update monitoring/alerts
- [ ] Document lessons learned
- [ ] Schedule postmortem if needed
```

## Debugging Tools Matrix

| Problem Type | Primary Tools | Secondary Tools |
|--------------|---------------|-------------------|
| Memory Issues | heap dump, pmap, valgrind | jmap, gdb, massif |
| CPU Issues | perf, flame graphs, prof | strace, top, htop |
| Network Issues | tcpdump, wireshark, ss | netstat, lsof, nmap |
| Database Issues | pg_stat, slow query log | explain, pg_locks |
| Container Issues | docker inspect, kubectl | crictl, ctr |
| Distributed Tracing | jaeger, zipkin, otel | logs correlation |
| Concurrency | thread dump, race detector | mutex profiling |
| I/O Issues | iostat, iotop, blktrace | lsof, fio |
