---
name: tailscale-sshsync-agent
description: Manages distributed workloads and file sharing across Tailscale SSH-connected machines. Automates remote command execution, intelligent load balancing, file synchronization workflows, host health monitoring, and multi-machine orchestration using sshsync. Activates when discussing remote machines, Tailscale SSH, workload distribution, file sharing, or multi-host operations.
---

# Tailscale SSH Sync Agent

## When to Use This Skill

This skill automatically activates when you need to:

✅ **Distribute workloads** across multiple machines
- "Run this on my least loaded machine"
- "Execute this task on the machine with most resources"
- "Balance work across my Tailscale network"

✅ **Share files** between Tailscale-connected hosts
- "Push this directory to all my development machines"
- "Sync code across my homelab servers"
- "Deploy configuration to production group"

✅ **Execute commands** remotely across host groups
- "Run system updates on all servers"
- "Check disk space across web-servers group"
- "Restart services on database hosts"

✅ **Monitor machine availability** and health
- "Which machines are online?"
- "Show status of my Tailscale network"
- "Check connectivity to remote hosts"

✅ **Automate multi-machine workflows**
- "Deploy to staging, test, then production"
- "Backup files from all machines"
- "Synchronize development environment across laptops"

## How It Works

This agent provides intelligent workload distribution and file sharing management across Tailscale SSH-connected machines using the `sshsync` CLI tool.

**Core Architecture**:

1. **SSH Sync Wrapper**: Python interface to sshsync CLI operations
2. **Tailscale Manager**: Tailscale-specific connectivity and status management
3. **Load Balancer**: Intelligent task distribution based on machine resources
4. **Workflow Executor**: Common multi-machine workflow automation
5. **Validators**: Parameter, host, and connection validation
6. **Helpers**: Temporal context, formatting, and utilities

**Key Features**:

- **Automatic host discovery** via Tailscale and SSH config
- **Intelligent load balancing** based on CPU, memory, and current load
- **Group-based operations** (execute on all web servers, databases, etc.)
- **Dry-run mode** for preview before execution
- **Parallel execution** across multiple hosts
- **Comprehensive error handling** and retry logic
- **Connection validation** before operations
- **Progress tracking** for long-running operations

## Data Sources

### sshsync CLI Tool

**What is sshsync?**

sshsync is a Python CLI tool for managing SSH connections and executing operations across multiple hosts. It provides:

- Group-based host management
- Remote command execution with timeouts
- File push/pull operations (single or recursive)
- Integration with existing SSH config (~/.ssh/config)
- Status checking and connectivity validation

**Installation**:
```bash
pip install sshsync
```

**Configuration**:

sshsync uses two configuration sources:

1. **SSH Config** (`~/.ssh/config`): Host connection details
2. **sshsync Config** (`~/.config/sshsync/config.yaml`): Group assignments

**Example SSH Config**:
```
Host homelab-1
  HostName 100.64.1.10
  User admin
  IdentityFile ~/.ssh/id_ed25519

Host prod-web-01
  HostName 100.64.1.20
  User deploy
  Port 22
```

**Example sshsync Config**:
```yaml
groups:
  homelab:
    - homelab-1
    - homelab-2
  production:
    - prod-web-01
    - prod-web-02
    - prod-db-01
  development:
    - dev-laptop
    - dev-desktop
```

**sshsync Commands Used**:

| Command | Purpose | Example |
|---------|---------|---------|
| `sshsync all` | Execute on all hosts | `sshsync all "df -h"` |
| `sshsync group` | Execute on group | `sshsync group web "systemctl status nginx"` |
| `sshsync push` | Push files to hosts | `sshsync push --group prod ./app /var/www/` |
| `sshsync pull` | Pull files from hosts | `sshsync pull --host db /var/log/mysql ./logs/` |
| `sshsync ls` | List hosts | `sshsync ls --with-status` |
| `sshsync sync` | Sync ungrouped hosts | `sshsync sync` |

### Tailscale Integration

**What is Tailscale?**

Tailscale is a zero-config VPN that creates a secure network between your devices. It provides:

- **Automatic peer-to-peer connections** via WireGuard
- **Magic DNS** for easy host addressing (e.g., `machine-name.tailnet-name.ts.net`)
- **SSH capabilities** built-in to Tailscale CLI
- **ACLs** for access control

**Tailscale SSH**:

Tailscale includes SSH functionality that works seamlessly with standard SSH:

```bash
# Standard SSH via Tailscale
ssh user@machine-name

# Tailscale-specific SSH command
tailscale ssh machine-name
```

**Integration with sshsync**:

Since Tailscale SSH uses standard SSH protocol, it works perfectly with sshsync. Just configure your SSH config with Tailscale hostnames:

```
Host homelab-1
  HostName homelab-1.tailnet.ts.net
  User admin
```

**Tailscale Commands Used**:

| Command | Purpose | Example |
|---------|---------|---------|
| `tailscale status` | Show network status | Lists all connected machines |
| `tailscale ping` | Check connectivity | `tailscale ping machine-name` |
| `tailscale ssh` | SSH to machine | `tailscale ssh user@machine` |

## Workflows

### 1. Host Health Monitoring

**User Query**: "Which of my machines are online?"

**Workflow**:

1. Load SSH config and sshsync groups
2. Execute `sshsync ls --with-status`
3. Parse connectivity results
4. Query Tailscale status for additional context
5. Return formatted health report with:
   - Online/offline status per host
   - Group memberships
   - Tailscale connection state
   - Last seen timestamp

**Implementation**: `scripts/sshsync_wrapper.py` → `get_host_status()`

**Output Format**:
```
🟢 homelab-1 (homelab) - Online - Tailscale: Connected
🟢 prod-web-01 (production, web-servers) - Online - Tailscale: Connected
🔴 dev-laptop (development) - Offline - Last seen: 2h ago
🟢 prod-db-01 (production, databases) - Online - Tailscale: Connected

Summary: 3/4 hosts online (75%)
```

### 2. Intelligent Load Balancing

**User Query**: "Run this task on the least loaded machine"

**Workflow**:

1. Get list of candidate hosts (from group or all)
2. For each online host, check:
   - CPU load (via `uptime` or `top`)
   - Memory usage (via `free` or `vm_stat`)
   - Disk space (via `df`)
3. Calculate composite load score
4. Select host with lowest score
5. Execute task on selected host
6. Return result with performance metrics

**Implementation**: `scripts/load_balancer.py` → `select_optimal_host()`

**Load Score Calculation**:
```
score = (cpu_pct * 0.4) + (mem_pct * 0.3) + (disk_pct * 0.3)
```

Lower score = better candidate for task execution.

**Output Format**:
```
✓ Selected host: prod-web-02
  Reason: Lowest load score (0.32)
  - CPU: 15% (vs avg 45%)
  - Memory: 30% (vs avg 60%)
  - Disk: 40% (vs avg 55%)

Executing: npm run build
[Task output...]

✓ Completed in 2m 15s
```

### 3. File Synchronization Workflows

**User Query**: "Sync my code to all development machines"

**Workflow**:

1. Validate source path exists locally
2. Identify target group ("development")
3. Check connectivity to all group members
4. Show dry-run preview (files to be synced, sizes)
5. Execute parallel push to all hosts
6. Validate successful transfer on each host
7. Return summary with per-host status

**Implementation**: `scripts/sshsync_wrapper.py` → `push_to_group()`

**Supported Operations**:

- **Push to all**: Sync files to every configured host
- **Push to group**: Sync to specific group (dev, prod, etc.)
- **Pull from host**: Retrieve files from single host
- **Pull from group**: Collect files from multiple hosts
- **Recursive sync**: Entire directory trees with `--recurse`

**Output Format**:
```
📤 Syncing: ~/projects/myapp → /var/www/myapp
Group: development (3 hosts)

Preview (dry-run):
  - dev-laptop: 145 files, 12.3 MB
  - dev-desktop: 145 files, 12.3 MB
  - dev-server: 145 files, 12.3 MB

Execute? [Proceeding...]

✓ dev-laptop: Synced 145 files in 8s
✓ dev-desktop: Synced 145 files in 6s
✓ dev-server: Synced 145 files in 10s

Summary: 3/3 successful (435 files, 36.9 MB total)
```

### 4. Remote Command Orchestration

**User Query**: "Check disk space on all web servers"

**Workflow**:

1. Identify target group ("web-servers")
2. Validate group exists and has members
3. Check connectivity to group members
4. Execute command in parallel across group
5. Collect and parse outputs
6. Format results with per-host breakdown

**Implementation**: `scripts/sshsync_wrapper.py` → `execute_on_group()`

**Features**:

- **Parallel execution**: Commands run simultaneously on all hosts
- **Timeout handling**: Configurable per-command timeout (default 10s)
- **Error isolation**: Failure on one host doesn't stop others
- **Output aggregation**: Collect and correlate all outputs
- **Dry-run mode**: Preview what would execute without running

**Output Format**:
```
🔧 Executing on group 'web-servers': df -h /var/www

web-01:
  Filesystem: /dev/sda1
  Size: 100G, Used: 45G, Available: 50G (45% used)

web-02:
  Filesystem: /dev/sda1
  Size: 100G, Used: 67G, Available: 28G (67% used) ⚠️

web-03:
  Filesystem: /dev/sda1
  Size: 100G, Used: 52G, Available: 43G (52% used)

⚠️ Alert: web-02 is above 60% disk usage
```

### 5. Multi-Stage Deployment Workflow

**User Query**: "Deploy to staging, test, then production"

**Workflow**:

1. **Stage 1 - Staging Deploy**:
   - Push code to staging group
   - Run build process
   - Execute automated tests
   - If tests fail: STOP and report error

2. **Stage 2 - Validation**:
   - Check staging health endpoints
   - Validate database migrations
   - Run smoke tests

3. **Stage 3 - Production Deploy**:
   - Push to production group (one at a time for zero-downtime)
   - Restart services gracefully
   - Verify each host before proceeding to next

4. **Stage 4 - Verification**:
   - Check production health
   - Monitor for errors
   - Rollback if issues detected

**Implementation**: `scripts/workflow_executor.py` → `deploy_workflow()`

**Output Format**:
```
🚀 Multi-Stage Deployment Workflow

Stage 1: Staging Deployment
  ✓ Pushed code to staging-01
  ✓ Build completed (2m 15s)
  ✓ Tests passed (145/145)

Stage 2: Validation
  ✓ Health check passed
  ✓ Database migration OK
  ✓ Smoke tests passed (12/12)

Stage 3: Production Deployment
  ✓ prod-web-01: Deployed & verified
  ✓ prod-web-02: Deployed & verified
  ✓ prod-web-03: Deployed & verified

Stage 4: Verification
  ✓ All health checks passed
  ✓ No errors in logs (5min window)

✅ Deployment completed successfully in 12m 45s
```

## Available Scripts

### scripts/sshsync_wrapper.py

**Purpose**: Python wrapper around sshsync CLI for programmatic access

**Functions**:

- `get_host_status(group=None)`: Get online/offline status of hosts
- `execute_on_all(command, timeout=10, dry_run=False)`: Run command on all hosts
- `execute_on_group(group, command, timeout=10, dry_run=False)`: Run on specific group
- `execute_on_host(host, command, timeout=10)`: Run on single host
- `push_to_hosts(local_path, remote_path, hosts=None, group=None, recurse=False, dry_run=False)`: Push files
- `pull_from_host(host, remote_path, local_path, recurse=False, dry_run=False)`: Pull files
- `list_hosts(with_status=True)`: List all configured hosts
- `get_groups()`: Get all defined groups and their members
- `add_hosts_to_group(group, hosts)`: Add hosts to a group

**Usage Example**:
```python
from sshsync_wrapper import execute_on_group, push_to_hosts

# Execute command
result = execute_on_group(
    group="web-servers",
    command="systemctl status nginx",
    timeout=15
)

# Push files
push_to_hosts(
    local_path="./dist",
    remote_path="/var/www/app",
    group="production",
    recurse=True
)
```

### scripts/tailscale_manager.py

**Purpose**: Tailscale-specific operations and status management

**Functions**:

- `get_tailscale_status()`: Get Tailscale network status (all peers)
- `check_connectivity(host)`: Ping host via Tailscale
- `get_peer_info(hostname)`: Get detailed info about peer
- `list_online_machines()`: List all online Tailscale machines
- `get_machine_ip(hostname)`: Get Tailscale IP for machine
- `validate_tailscale_ssh(host)`: Check if Tailscale SSH is working

**Usage Example**:
```python
from tailscale_manager import get_tailscale_status, check_connectivity

# Get network status
status = get_tailscale_status()
print(f"Online machines: {status['online_count']}")

# Check specific host
is_online = check_connectivity("homelab-1")
```

### scripts/load_balancer.py

**Purpose**: Intelligent task distribution based on machine resources

**Functions**:

- `get_machine_load(host)`: Get CPU, memory, disk metrics
- `calculate_load_score(metrics)`: Calculate composite load score
- `select_optimal_host(candidates, prefer_group=None)`: Pick best host
- `get_group_capacity()`: Get aggregate capacity of group
- `distribute_tasks(tasks, hosts)`: Distribute multiple tasks optimally

**Usage Example**:
```python
from load_balancer import select_optimal_host

# Find best machine for task
best_host = select_optimal_host(
    candidates=["web-01", "web-02", "web-03"],
    prefer_group="production"
)

# Execute on selected host
execute_on_host(best_host, "npm run build")
```

### scripts/workflow_executor.py

**Purpose**: Common multi-machine workflow automation

**Functions**:

- `deploy_workflow(code_path, staging_group, prod_group)`: Full deployment pipeline
- `backup_workflow(hosts, backup_paths, destination)`: Backup from multiple hosts
- `sync_workflow(source_host, target_group, paths)`: Sync from one to many
- `rolling_restart(group, service_name)`: Zero-downtime service restart
- `health_check_workflow(group, endpoint)`: Check health across group

**Usage Example**:
```python
from workflow_executor import deploy_workflow, backup_workflow

# Deploy with testing
deploy_workflow(
    code_path="./dist",
    staging_group="staging",
    prod_group="production"
)

# Backup from all databases
backup_workflow(
    hosts=["db-01", "db-02"],
    backup_paths=["/var/lib/mysql"],
    destination="./backups"
)
```

### scripts/utils/helpers.py

**Purpose**: Common utilities and formatting functions

**Functions**:

- `format_bytes(bytes)`: Human-readable byte formatting (1.2 GB)
- `format_duration(seconds)`: Human-readable duration (2m 15s)
- `parse_ssh_config()`: Parse ~/.ssh/config for host details
- `parse_sshsync_config()`: Parse sshsync group configuration
- `get_timestamp()`: Get ISO timestamp for logging
- `safe_execute(func, *args, **kwargs)`: Execute with error handling
- `validate_path(path)`: Check if path exists and is accessible

### scripts/utils/validators/parameter_validator.py

**Purpose**: Validate user inputs and parameters

**Functions**:

- `validate_host(host, valid_hosts=None)`: Validate host exists
- `validate_group(group, valid_groups=None)`: Validate group exists
- `validate_path_exists(path)`: Check local path exists
- `validate_timeout(timeout)`: Ensure timeout is reasonable
- `validate_command(command)`: Basic command safety validation

### scripts/utils/validators/host_validator.py

**Purpose**: Validate host configuration and availability

**Functions**:

- `validate_ssh_config(host)`: Check host has SSH config entry
- `validate_host_reachable(host, timeout=5)`: Check host is reachable
- `validate_group_members(group)`: Ensure group has valid members
- `get_invalid_hosts(hosts)`: Find hosts without valid config

### scripts/utils/validators/connection_validator.py

**Purpose**: Validate SSH and Tailscale connections

**Functions**:

- `validate_ssh_connection(host)`: Test SSH connection works
- `validate_tailscale_connection(host)`: Test Tailscale connectivity
- `validate_ssh_key(host)`: Check SSH key authentication
- `get_connection_diagnostics(host)`: Comprehensive connection testing

## Available Analyses

### 1. Host Availability Analysis

**Function**: `analyze_host_availability(group=None)`

**Objective**: Determine which machines are online and accessible

**Inputs**:
- `group` (optional): Specific group to check (None = all hosts)

**Outputs**:
```python
{
    'total_hosts': 10,
    'online_hosts': 8,
    'offline_hosts': 2,
    'availability_pct': 80.0,
    'by_group': {
        'production': {'online': 3, 'total': 3, 'pct': 100.0},
        'development': {'online': 2, 'total': 3, 'pct': 66.7},
        'homelab': {'online': 3, 'total': 4, 'pct': 75.0}
    },
    'offline_hosts_details': [
        {'host': 'dev-laptop', 'last_seen': '2h ago', 'groups': ['development']},
        {'host': 'homelab-4', 'last_seen': '1d ago', 'groups': ['homelab']}
    ]
}
```

**Interpretation**:
- **> 90%**: Excellent availability
- **70-90%**: Good availability, monitor offline hosts
- **< 70%**: Poor availability, investigate issues

### 2. Load Distribution Analysis

**Function**: `analyze_load_distribution(group=None)`

**Objective**: Understand resource usage across machines

**Inputs**:
- `group` (optional): Specific group to analyze

**Outputs**:
```python
{
    'hosts': [
        {
            'host': 'web-01',
            'cpu_pct': 45,
            'mem_pct': 60,
            'disk_pct': 40,
            'load_score': 0.49,
            'status': 'moderate'
        },
        # ... more hosts
    ],
    'aggregate': {
        'avg_cpu': 35,
        'avg_mem': 55,
        'avg_disk': 45,
        'total_capacity': 1200  # GB
    },
    'recommendations': [
        {
            'host': 'web-02',
            'issue': 'High CPU usage (85%)',
            'action': 'Consider migrating workloads'
        }
    ]
}
```

**Load Status**:
- **Low** (score < 0.4): Good capacity for more work
- **Moderate** (0.4-0.7): Normal operation
- **High** (> 0.7): May need to offload work

### 3. File Sync Status Analysis

**Function**: `analyze_sync_status(local_path, remote_path, group)`

**Objective**: Compare local files with remote versions

**Inputs**:
- `local_path`: Local directory to compare
- `remote_path`: Remote directory path
- `group`: Group to check

**Outputs**:
```python
{
    'local_files': 145,
    'local_size': 12582912,  # bytes
    'hosts': [
        {
            'host': 'web-01',
            'status': 'in_sync',
            'files_match': 145,
            'files_different': 0,
            'missing_files': 0
        },
        {
            'host': 'web-02',
            'status': 'out_of_sync',
            'files_match': 140,
            'files_different': 3,
            'missing_files': 2,
            'details': ['config.json modified', 'index.html modified', ...]
        }
    ],
    'sync_percentage': 96.7,
    'recommended_action': 'Push to web-02'
}
```

### 4. Network Latency Analysis

**Function**: `analyze_network_latency(hosts=None)`

**Objective**: Measure connection latency to hosts

**Inputs**:
- `hosts` (optional): Specific hosts to test (None = all)

**Outputs**:
```python
{
    'hosts': [
        {'host': 'web-01', 'latency_ms': 15, 'status': 'excellent'},
        {'host': 'web-02', 'latency_ms': 45, 'status': 'good'},
        {'host': 'db-01', 'latency_ms': 150, 'status': 'fair'}
    ],
    'avg_latency': 70,
    'min_latency': 15,
    'max_latency': 150,
    'recommendations': [
        {'host': 'db-01', 'issue': 'High latency', 'action': 'Check network path'}
    ]
}
```

**Latency Classification**:
- **Excellent** (< 50ms): Ideal for interactive tasks
- **Good** (50-100ms): Suitable for most operations
- **Fair** (100-200ms): May impact interactive workflows
- **Poor** (> 200ms): Investigate network issues

### 5. Comprehensive Infrastructure Report

**Function**: `comprehensive_infrastructure_report(group=None)`

**Objective**: One-stop function for complete infrastructure overview

**Inputs**:
- `group` (optional): Limit to specific group (None = all)

**Outputs**:
```python
{
    'report_timestamp': '2025-10-19T19:43:41Z',
    'group': 'production',  # or 'all'
    'metrics': {
        'availability': {...},  # from analyze_host_availability
        'load_distribution': {...},  # from analyze_load_distribution
        'network_latency': {...},  # from analyze_network_latency
        'tailscale_status': {...}  # from Tailscale integration
    },
    'summary': "Production infrastructure: 3/3 hosts online, avg load 45%, network latency 35ms",
    'alerts': [
        "⚠ web-02: High CPU usage (85%)",
        "⚠ db-01: Elevated latency (150ms)"
    ],
    'recommendations': [
        "Consider rebalancing workload from web-02",
        "Investigate network path to db-01"
    ],
    'overall_health': 'good'  # excellent | good | fair | poor
}
```

**Overall Health Classification**:
- **Excellent**: All metrics green, no alerts
- **Good**: Most metrics healthy, minor alerts
- **Fair**: Some concerning metrics, action recommended
- **Poor**: Critical issues, immediate action required

## Error Handling

### Connection Errors

**Error**: Cannot connect to host

**Causes**:
- Host is offline
- Tailscale not connected
- SSH key missing/invalid
- Firewall blocking connection

**Handling**:
```python
try:
    execute_on_host("web-01", "ls")
except ConnectionError as e:
    # Try Tailscale ping first
    if not check_connectivity("web-01"):
        return {
            'error': 'Host unreachable',
            'suggestion': 'Check Tailscale connection',
            'diagnostics': get_connection_diagnostics("web-01")
        }
    # Then check SSH
    if not validate_ssh_connection("web-01"):
        return {
            'error': 'SSH authentication failed',
            'suggestion': 'Check SSH keys: ssh-add -l'
        }
```

### Timeout Errors

**Error**: Operation timed out

**Causes**:
- Command taking too long
- Network latency
- Host overloaded

**Handling**:
- Automatic retry with exponential backoff (3 attempts)
- Increase timeout for known slow operations
- Fall back to alternative host if available

### File Transfer Errors

**Error**: File sync failed

**Causes**:
- Insufficient disk space
- Permission denied
- Path doesn't exist

**Handling**:
- Pre-check disk space on target
- Validate permissions before transfer
- Create directories if needed
- Partial transfer recovery

### Validation Errors

**Error**: Invalid parameter

**Examples**:
- Unknown host
- Non-existent group
- Invalid path

**Handling**:
- Validate all inputs before execution
- Provide suggestions for similar valid options
- Clear error messages with corrective actions

## Mandatory Validations

### Before Any Operation

1. **Parameter Validation**:
   ```python
   host = validate_host(host, valid_hosts=get_all_hosts())
   group = validate_group(group, valid_groups=get_groups())
   timeout = validate_timeout(timeout)
   ```

2. **Connection Validation**:
   ```python
   if not validate_host_reachable(host, timeout=5):
       raise ConnectionError(f"Host {host} is not reachable")
   ```

3. **Path Validation** (for file operations):
   ```python
   if not validate_path_exists(local_path):
       raise ValueError(f"Path does not exist: {local_path}")
   ```

### During Operation

1. **Timeout Monitoring**: Every operation has configurable timeout
2. **Progress Tracking**: Long operations show progress
3. **Error Isolation**: Failure on one host doesn't stop others

### After Operation

1. **Result Validation**:
   ```python
   report = validate_operation_result(result)
   if report.has_critical_issues():
       raise OperationError(report.get_summary())
   ```

2. **State Verification**: Confirm operation succeeded
3. **Logging**: Record all operations for audit trail

## Performance and Caching

### Caching Strategy

**Host Status Cache**:
- **TTL**: 60 seconds
- **Why**: Host status doesn't change rapidly
- **Invalidation**: Manual invalidate when connectivity changes

**Load Metrics Cache**:
- **TTL**: 30 seconds
- **Why**: Load changes frequently
- **Invalidation**: Automatic on timeout

**Group Configuration Cache**:
- **TTL**: 5 minutes
- **Why**: Group membership rarely changes
- **Invalidation**: Manual when groups modified

### Performance Optimizations

1. **Parallel Execution**:
   - Commands execute concurrently across hosts
   - ThreadPoolExecutor with max 10 workers
   - Prevents sequential bottleneck

2. **Connection Pooling**:
   - Reuse SSH connections when possible
   - ControlMaster in SSH config

3. **Lazy Loading**:
   - Only fetch data when needed
   - Don't load all host status unless required

4. **Progressive Results**:
   - Stream results as they complete
   - Don't wait for slowest host

## Automatic Detection Keywords

This skill automatically activates when you mention:

**Hosts & Machines**:
- remote machine, remote host, remote server
- Tailscale machine, Tailscale host
- SSH host, SSH server
- homelab, servers, cluster

**Tools**:
- sshsync, ssh sync
- Tailscale, tailnet
- SSH, secure shell

**Operations**:
- distribute workload, load balance
- file sharing, file sync, file transfer
- push files, pull files, sync files
- remote execution, execute remotely
- deploy to, deploy across
- backup from, sync to

**Groups**:
- host group, machine group, server group
- production servers, development machines
- web servers, database servers
- staging environment, production environment

**Actions**:
- check status, check connectivity
- run on all, execute on group
- sync across, distribute to
- deploy to, push to, pull from

**Monitoring**:
- which machines are online
- host availability, server status
- machine health, connectivity check
- network status, latency check

**Workflows**:
- multi-stage deployment
- rolling restart, zero-downtime
- backup workflow, sync workflow
- distributed task, parallel execution

## Usage Examples

### Example 1: Check Host Status

**User**: "Which of my Tailscale machines are online?"

**Agent Response**:
```
Checking Tailscale network status...

🟢 homelab-1 (homelab) - Online - Tailscale: Connected
  IP: 100.64.1.10 | Latency: 15ms

🟢 homelab-2 (homelab) - Online - Tailscale: Connected
  IP: 100.64.1.11 | Latency: 18ms

🔴 dev-laptop (development) - Offline
  Last seen: 2 hours ago | Tailscale: Not connected

🟢 prod-web-01 (production, web-servers) - Online - Tailscale: Connected
  IP: 100.64.1.20 | Latency: 25ms

🟢 prod-db-01 (production, databases) - Online - Tailscale: Connected
  IP: 100.64.1.30 | Latency: 30ms

Summary: 4/5 hosts online (80%)
Average latency: 22ms
```

### Example 2: Execute on Group

**User**: "Check disk space on all web servers"

**Agent Response**:
```
Executing on group 'web-servers': df -h /var/www

🔧 web-01:
  Filesystem: /dev/sda1
  Size: 100G | Used: 45G | Available: 50G (45% used)
  Status: ✓ Healthy

🔧 web-02:
  Filesystem: /dev/sda1
  Size: 100G | Used: 67G | Available: 28G (67% used)
  Status: ⚠ Warning - Above 60%

🔧 web-03:
  Filesystem: /dev/sda1
  Size: 100G | Used: 52G | Available: 43G (52% used)
  Status: ✓ Healthy

⚠️ Alert: web-02 is above 60% disk usage
Recommendation: Clear old logs or increase disk space
```

### Example 3: Load-Balanced Execution

**User**: "Run this npm build on the machine with most available resources"

**Agent Response**:
```
Analyzing resource availability across 5 machines...

Load Analysis:
  web-01: CPU 45%, Mem 60%, Disk 40% → Score: 0.49 (moderate)
  web-02: CPU 85%, Mem 70%, Disk 65% → Score: 0.75 (high load)
  web-03: CPU 20%, Mem 35%, Disk 30% → Score: 0.28 (low load) ✓

✓ Selected: web-03
  Reason: Lowest load score (0.28)
  Available: CPU 80%, Memory 65%, Disk 70%

Executing on web-03: npm run build

[Build output...]
  ✓ Build completed successfully
  Duration: 2m 15s
  Output: ./dist (145 files, 12.3 MB)

Final load: CPU 65%, Mem 50% (still below average)
```

### Example 4: File Sync

**User**: "Push my app directory to all production servers"

**Agent Response**:
```
📤 Syncing: ~/projects/myapp → /var/www/myapp
Target group: production (3 hosts)

Analyzing source...
  145 files, 12.3 MB total

Preview (dry-run):
  prod-web-01: 145 files → /var/www/myapp
  prod-web-02: 145 files → /var/www/myapp
  prod-db-01: Skipped (not in web-servers group)

Checking target capacity...
  ✓ prod-web-01: 50 GB available
  ✓ prod-web-02: 28 GB available

Executing push...

✓ prod-web-01: Synced 145 files in 8.2s
  Modified: 12 files
  Added: 3 files

✓ prod-web-02: Synced 145 files in 6.5s
  Modified: 12 files
  Added: 3 files

Summary: 2/2 successful (290 files, 24.6 MB total)
```

### Example 5: Multi-Stage Deployment

**User**: "Deploy this to staging, run tests, then push to production"

**Agent Response**:
```
🚀 Multi-Stage Deployment Workflow

Stage 1: Staging Deployment
  📤 Pushing to staging-01...
    ✓ Code synced (145 files, 12.3 MB) - 8s

  🔨 Running build...
    $ npm run build
    ✓ Build completed - 2m 15s

  🧪 Running tests...
    $ npm test
    ✓ All tests passed (145/145) - 45s

Stage 2: Staging Validation
  ✓ Health endpoint: 200 OK
  ✓ Database migrations: Up to date
  ✓ Smoke tests: 12/12 passed

Stage 3: Production Deployment
  Rolling deployment to 3 hosts...

  ⏳ prod-web-01:
    ✓ Code synced
    ✓ Build completed
    ✓ Service restarted gracefully
    ✓ Health check passed
    Duration: 3m 10s

  ⏳ prod-web-02:
    ✓ Code synced
    ✓ Build completed
    ✓ Service restarted gracefully
    ✓ Health check passed
    Duration: 3m 5s

  ⏳ prod-web-03:
    ✓ Code synced
    ✓ Build completed
    ✓ Service restarted gracefully
    ✓ Health check passed
    Duration: 3m 12s

Stage 4: Production Verification
  ✓ All health checks passed (3/3)
  ✓ No errors in logs (5min window)
  ✓ Response times normal (avg 45ms)

✅ Deployment completed successfully!
  Total duration: 12m 45s
  Hosts updated: 3
  Zero downtime: ✓
```

### Example 6: Comprehensive Infrastructure Report

**User**: "Give me a complete status report of my infrastructure"

**Agent Response**:
```
📊 Infrastructure Report
Generated: 2025-10-19 19:43:41

=== AVAILABILITY ===
Total Hosts: 10
Online: 8 (80%)
Offline: 2

By Group:
  production: 3/3 (100%) ✓
  development: 2/3 (66.7%) ⚠
  homelab: 3/4 (75%)

Offline Hosts:
  • dev-laptop (development) - Last seen: 2h ago
  • homelab-4 (homelab) - Last seen: 1d ago

=== LOAD DISTRIBUTION ===
Average Load: 45% CPU, 55% Memory, 45% Disk

Top 3 Loaded Hosts:
  1. web-02: 85% CPU, 70% Mem, 65% Disk (Score: 0.75) ⚠
  2. db-01: 60% CPU, 75% Mem, 55% Disk (Score: 0.65)
  3. web-01: 45% CPU, 60% Mem, 40% Disk (Score: 0.49)

Top 3 Available Hosts:
  1. web-03: 20% CPU, 35% Mem, 30% Disk (Score: 0.28) ✓
  2. homelab-1: 25% CPU, 40% Mem, 35% Disk (Score: 0.33)
  3. homelab-2: 30% CPU, 45% Mem, 40% Disk (Score: 0.38)

=== NETWORK LATENCY ===
Average: 35ms
Range: 15ms - 150ms

Excellent (< 50ms): 6 hosts
Good (50-100ms): 1 host
Fair (100-200ms): 1 host (db-01: 150ms) ⚠

=== TAILSCALE STATUS ===
Network: Connected
Peers Online: 8/10
Exit Node: None
MagicDNS: Enabled

=== ALERTS ===
⚠ web-02: High CPU usage (85%) - Consider load balancing
⚠ db-01: Elevated latency (150ms) - Check network path
⚠ dev-laptop: Offline for 2 hours - May need attention

=== RECOMMENDATIONS ===
1. Rebalance workload from web-02 to web-03
2. Investigate network latency to db-01
3. Check status of dev-laptop and homelab-4
4. Consider scheduling maintenance for web-02

Overall Health: GOOD ✓
```

## Installation

See INSTALLATION.md for detailed setup instructions.

Quick start:
```bash
# 1. Install sshsync
pip install sshsync

# 2. Configure SSH hosts
vim ~/.ssh/config

# 3. Sync host groups
sshsync sync

# 4. Install agent
/plugin marketplace add ./tailscale-sshsync-agent

# 5. Test
"Which of my machines are online?"
```

## Version

Current version: 1.0.0

See CHANGELOG.md for release history.

## Architecture Decisions

See DECISIONS.md for detailed rationale behind tool selection, architecture choices, and trade-offs considered.
