---
name: distributed-gummy
description: Orchestrate gummy-agents across distributed network using 'd' command for load-balanced, multi-host AI development
---

# Distributed Gummy Orchestrator

Coordinate gummy-agent tasks across your Tailscale network using the `d` command for intelligent load balancing and multi-host AI-powered development.

## When to Use

This skill activates when you want to:

✅ **Distribute gummy tasks across multiple hosts**
- "Run this gummy task on the least loaded host"
- "Execute specialist on optimal node"
- "Distribute testing across all machines"

✅ **Load-balanced AI development**
- "Which host should handle this database work?"
- "Run API specialist on best available node"
- "Balance gummy tasks across cluster"

✅ **Multi-host coordination**
- "Sync codebase andw run gummy on node-2"
- "Execute parallel specialists across network"
- "Run tests on all platforms simultaneously"

✅ **Network-wide specialist monitoring**
- "Show all running specialists across hosts"
- "What gummy tasks are active on my network?"
- "Status of distributed specialists"

## How It Works

### Architecture

```
[Main Claude] ──> [Orchestrator] ──> dw command ──> [Network Nodes]
                      │                                │
                      ├──> Load Analysis              ├──> gummy-agent
                      ├──> Host Selection             ├──> Specialists
                      ├──> Sync Management            └──> Tasks
                      └──> Task Distribution
```

### Core Workflows

**1. Load-Balanced Execution**
```bash
# User request: "Run database optimization on best host"
# Agent:
1. Execute: dw load
2. Parse metrics (CPU, memory, load average)
3. Calculate composite scores
4. Select optimal host
5. Sync codebase: dw sync <host>
6. Execute: dw run <host> "cd <project> && gummy task 'optimize database queries'"
```

**2. Parallel Distribution**
```bash
# User request: "Test on all platforms"
# Agent:
1. Get hosts: dw status
2. Filter by availability
3. Sync all: for host in hosts; do dw sync $host; done
4. Launch parallel: dw run host1 "test" & dw run host2 "test" & ...
5. Aggregate results
```

**3. Network-Wide Monitoring**
```bash
# User request: "Show all specialists"
# Agent:
1. Get active hosts: dw status
2. For each host: dw run <host> "gummy-watch status"
3. Parse specialist states
4. Aggregate and display
```

## Available Scripts

### orchestrate_gummy.py

Main orchestration logic - coordinates distributed gummy execution.

**Functions**:
- `select_optimal_host()` - Choose best node based on load
- `sync_and_execute_gummy()` - Sync code + run gummy task
- `parallel_gummy_tasks()` - Execute multiple tasks simultaneously
- `monitor_all_specialists()` - Aggregate specialist status across network

**Usage**:
```python
from scripts.orchestrate_gummy import select_optimal_host, sync_and_execute_gummy

# Find best host
optimal = select_optimal_host(task_type="database")
# Returns: {'host': 'node-1', 'score': 0.23, 'cpu': 15%, 'mem': 45%}

# Execute on optimal host
result = sync_and_execute_gummy(
    host=optimal['host'],
    task="optimize user queries",
    project_dir="/path/to/project"
)
```

### d_wrapper.py

Wrapper for `d` command operations.

**Functions**:
- `get_load_metrics()` - Execute `dwload` and parse results
- `get_host_status()` - Execute `dwstatus` and parse availability
- `sync_directory()` - Execute `dwsync` to target host
- `run_remote_command()` - Execute `dwrun` on specific host

## Workflows

### Workflow 1: Load-Balanced Task Distribution

**User Query**: "Run database optimization on optimal host"

**Agent Actions**:
1. Call `get_load_metrics()` to fetch cluster load
2. Call `select_optimal_host(task_type="database")` to choose best node
3. Call `sync_directory(host, project_path)` to sync codebase
4. Call `dwrun <host> "cd project && gummy task 'optimize database queries'"`
5. Monitor execution via `gummy-watch`
6. Return results

### Workflow 2: Parallel Multi-Host Execution

**User Query**: "Run tests across all available nodes"

**Agent Actions**:
1. Call `get_host_status()` to get available hosts
2. Filter hosts by availability and capability
3. For each host:
   - Sync codebase: `sync_directory(host, project)`
   - Launch test: `dwrun <host> "cd project && gummy task 'run test suite'" &`
4. Collect all background job PIDs
5. Wait for completion
6. Aggregate results from all hosts

### Workflow 3: Network-Wide Specialist Monitoring

**User Query**: "Show all running specialists across my network"

**Agent Actions**:
1. Get active hosts from `dwstatus`
2. For each host:
   - Check for gummy-agent: `dwrun <host> "command -v gummy"`
   - If present, get specialists: `dwrun <host> "ls -la ~/.gummy/specialists"`
3. Parse specialist metadata from each host
4. Create aggregated dashboard showing:
   - Host name
   - Active specialists
   - Session states (active/dormant)
   - Resource usage
5. Display unified network view

### Workflow 4: Intelligent Work Distribution

**User Query**: "I have database work and API work - distribute optimally"

**Agent Actions**:
1. Analyze tasks:
   - Task 1: database optimization (CPU-intensive)
   - Task 2: API development (I/O-intensive)
2. Get load metrics for all hosts
3. Select hosts using different criteria:
   - Database work → host with lowest CPU load
   - API work → host with lowest I/O wait
4. Sync to both hosts
5. Launch tasks in parallel:
   ```bash
   dw run <cpu-host> "gummy task 'optimize database queries'" &
   dw run <io-host> "gummy task 'build REST API endpoints'" &
   ```
6. Monitor both executions
7. Report when complete

## Error Handling

### Connection Issues
```python
try:
    result = d_run(host, command)
except SSHConnectionError:
    # Retry with different host
    fallback = select_optimal_host(exclude=[failed_host])
    result = d_run(fallback, command)
```

### Sync Failures
```python
if not sync_successful:
    # Fall back to local execution
    return execute_local_gummy(task)
```

### Load Metric Unavailable
```python
if not load_data:
    # Use round-robin distribution
    return round_robin_host_selection()
```

## Performance & Caching

**Load Metrics Caching**:
- Cache TTL: 30 seconds (load changes fast)
- Cache location: `/tmp/d-load-cache.json`
- Invalidate on manual request

**Host Availability**:
- Cache TTL: 60 seconds
- Cache location: `/tmp/d-status-cache.json`

**Specialist State**:
- Cache TTL: 5 seconds (near real-time)
- Only cached during active monitoring

## Keywords for Auto-Detection

This skill activates when user mentions:

**Distributed Operations**:
- distributed, cluster, network, multi-host, across hosts, all nodes, all machines
- remote, ssh, tailscale

**Gummy Integration**:
- gummy, specialist, agent, haiku, task
- execute gummy, run gummy, gummy task

**Load Balancing**:
- least loaded, best host, optimal node, load balance, best machine
- which host should, where should I run

**Coordination**:
- sync andw run, parallel, coordinate, orchestrate, distribute
- run on, execute on, send to

**Monitoring**:
- all specialists, network status, cluster status, show specialists
- what's running, active tasks

**Examples That Activate**:
- "Run database optimization on least loaded host"
- "Execute API specialist on optimal node"
- "Distribute tests across all machines"
- "Show all specialists across network"
- "Sync codebase andw run gummy on node-2"
- "Which host should handle this database work?"
- "Run parallel gummy tasks across cluster"

**Does NOT Activate** (local operations):
- "Run gummy task locally"
- "Execute specialist here"
- "/gummy-task add logging"

## Usage Examples

### Example 1: Simple Load-Balanced Execution

```
👤: "Run database optimization on the best available host"

🤖: I'll find the optimal host and execute the task there.

[Executes: dw load]
[Analysis: node-1 has lowest composite score (0.18)]
[Executes: dw sync node-1]
[Executes: dw run node-1 "cd ~/project && gummy task 'optimize database queries'"]

✅ Task launched on node-1 (CPU: 12%, Mem: 35%, Load: 0.18)

Monitor with: ssh node-1 'gummy-watch'
```

### Example 2: Parallel Multi-Platform Testing

```
👤: "Run tests across all available nodes"

🤖: I'll distribute test execution across your network.

[Executes: dw status]
[Found: 4 available hosts]
[Syncing codebase to all hosts...]
  ✓ node-1 synced
  ✓ node-2 synced
  ✓ node-3 synced
  ✓ node-4 synced

[Launching parallel test execution...]
  node-1: Running unit tests
  node-2: Running integration tests
  node-3: Running e2e tests
  node-4: Running performance tests

[All tests complete in 8 minutes (vs 32 minutes sequential)]

Results:
  ✅ unit: 1,247 passed
  ✅ integration: 89 passed
  ✅ e2e: 34 passed
  ⚠️  performance: 3 slow queries detected
```

### Example 3: Intelligent Task Distribution

```
👤: "I need to optimize database queries and build new API endpoints"

🤖: I'll distribute these optimally based on task characteristics.

[Analyzing tasks...]
  - Database optimization: CPU-intensive
  - API development: I/O-bound

[Fetching cluster load...]
  node-1: CPU 15%, I/O 45%  → Best for database work
  node-2: CPU 65%, I/O 12%  → Best for API work

[Distributing tasks...]
  ✓ Database optimization → node-1
  ✓ API development → node-2

[Syncing and launching...]
  node-1: database-expert specialist active
  node-2: api-developer specialist active

Both tasks running in parallel. Expected completion: 15 minutes.

Monitor:
  ssh node-1 'gummy-watch'
  ssh node-2 'gummy-watch'
```

### Example 4: Network-Wide Specialist Status

```
👤: "Show all specialists running across my network"

🤖: Scanning network for active specialists...

[Checking all hosts...]

╔═══════════════════════════════════════════════════════╗
║  DISTRIBUTED SPECIALIST DASHBOARD                     ║
╚═══════════════════════════════════════════════════════╝

┌─ node-1 ──────────────────────────────────────────────┐
│ ⚡ database-expert     Sessions: 8  Cost: $0.02       │
│ 💤 testing-specialist  Sessions: 3  Cost: $0.01       │
└───────────────────────────────────────────────────────┘

┌─ node-2 ──────────────────────────────────────────────┐
│ ⚡ api-developer       Sessions: 5  Cost: $0.01       │
│ ⚡ frontend-specialist Sessions: 12 Cost: $0.03       │
└───────────────────────────────────────────────────────┘

┌─ node-3 ──────────────────────────────────────────────┐
│ 💤 security-specialist Sessions: 2  Cost: $0.01       │
└───────────────────────────────────────────────────────┘

Total: 5 active specialists across 3 hosts
Total cost today: $0.08
```

### Example 5: Sync-Before-Execute Workflow

```
👤: "Sync my codebase to node-3 andw run frontend specialist there"

🤖: I'll sync and execute on node-3.

[Current directory: ~/projects/myapp]

[Syncing to node-3...]
  Sending: src/ components/ lib/ package.json
  Excluding: node_modules .git dist
  ✓ Synced 1,247 files (45 MB) in 3 seconds

[Launching frontend specialist on node-3...]
  ✓ specialist created (session: abc123)
  ⚡ Working on task...

Task active on node-3. Monitor: ssh node-3 'gummy-watch'
```

## Configuration

### Required Tools

- ✅ `d` command (distributed CLI)
- ✅ `gummy-agent` installed on remote hosts
- ✅ Tailscale network configured
- ✅ SSH access via ~/.ssh/config
- ✅ rsync on all hosts

### Optional Configuration

Create `~/.config/distributed-gummy/config.yaml`:

```yaml
# Load balancing weights
load_weights:
  cpu: 0.4
  memory: 0.3
  load_average: 0.3

# Sync exclusions
sync_exclude:
  - node_modules
  - .git
  - dist
  - build
  - .DS_Store
  - "*.log"

# Host preferences for task types
host_preferences:
  database:
    - node-1  # High CPU
  frontend:
    - node-2  # High memory
  testing:
    - node-3  # Dedicated test node
```

## Troubleshooting

### "Host not responding"
```bash
# Check Tailscale connectivity
tailscale status

# Check SSH access
ssh <host> echo "OK"

# Verify dw command works
dw status
```

### "Sync failed"
```bash
# Manual sync test
dw sync <host>

# Check rsync
which rsync

# Check disk space on remote
dw run <host> "df -h"
```

### "Gummy not found on remote host"
```bash
# Check gummy installation
dw run <host> "which gummy"

# Install if needed
dw run <host> "brew install WillyV3/tap/gummy-agent"
```

## Limitations

- Requires gummy-agent installed on all target hosts
- Requires Tailscale network connectivity
- Load metrics only available from `dwload` command
- Sync uses current directory as base (change with cd first)

## Version

1.0.0 - Initial release
