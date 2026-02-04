---
name: network-agent
description: Comprehensive network topology discovery, automated documentation generation, and root cause analysis for network issues using RouterCLI Pro. Use this skill when asked to map networks, discover device connections, create network documentation, troubleshoot connectivity issues, analyze network problems, or investigate network incidents. All workflows use the existing RouterCLI Pro CLI tool.
---

# Network Agent

Automated network topology discovery, comprehensive documentation generation, and intelligent root cause analysis using **RouterCLI Pro**.

## Core Capabilities

1. **Topology Discovery** - Map network connections, neighbors, and dependencies using RouterCLI Pro
2. **Documentation Generation** - Create detailed network documentation from RouterCLI Pro output
3. **Root Cause Analysis** - Investigate network issues with multi-device data collection

## Available RouterCLI Pro Commands

RouterCLI Pro provides these key commands for network operations:

- `routercli connect` - Test connectivity to devices
- `routercli exec` - Execute single commands
- `routercli run` - Execute preset command collections
- `routercli batch` - Execute multiple commands
- `routercli presets` - List available presets
- `routercli cache` - View cached connections

**Key Presets Available:**
- `health_check` - Basic device health (4 commands)
- `network_status` - Network connectivity (4 commands)
- `interface_check` - Interface details (4 commands)
- `routing_overview` - Routing protocols (4 commands)
- `security_audit` - Security config (4 commands)
- `troubleshoot_connectivity` - Network issues (5 commands)
- `full_status` - Comprehensive audit (9 commands)

## Workflows

### 1. Network Topology Discovery

Discover network topology by recursively querying devices for neighbor information.

**Step-by-Step Process:**

1. **Start with Seed Device(s)**
   ```bash
   routercli connect --device 192.168.1.1 --username admin
   ```

2. **Discover Neighbors via CDP**
   ```bash
   routercli exec --device 192.168.1.1 --username admin \
     --command "show cdp neighbors detail"
   ```

3. **Discover Neighbors via LLDP**
   ```bash
   routercli exec --device 192.168.1.1 --username admin \
     --command "show lldp neighbors detail"
   ```

4. **Parse Output and Extract:**
   - Neighbor hostnames
   - Neighbor IP addresses
   - Local interface connections
   - Remote interface connections
   - Connection protocols

5. **Recursively Query Each Discovered Neighbor**
   - Repeat steps 2-4 for each new device
   - Keep track of discovered devices to avoid loops
   - Build connection graph

6. **Enhance with Additional Data:**
   ```bash
   # Get interface details
   routercli exec --device <device> --command "show ip interface brief"
   
   # Get routing neighbors
   routercli exec --device <device> --command "show ip ospf neighbor"
   routercli exec --device <device> --command "show ip bgp summary"
   ```

**Output Structure:**
Store discovered topology as JSON:
```json
{
  "devices": {
    "device_id": {
      "hostname": "...",
      "management_ip": "...",
      "device_type": "...",
      "interfaces": [...]
    }
  },
  "connections": [
    {
      "source": "device1",
      "target": "device2",
      "source_interface": "...",
      "target_interface": "...",
      "protocol": "CDP"
    }
  ]
}
```

### 2. Network Documentation Generation

After discovering topology, generate comprehensive documentation using RouterCLI Pro.

**Collect Device Information:**

For each device in topology, use the `full_status` preset:
```bash
routercli run --device <device> --username admin \
  --preset full_status --json > device_data.json
```

This executes 9 commands comprehensively covering:
- Device version and hardware
- Interface status and configuration
- Memory and CPU usage
- Routing information
- And more

**Generate Documentation Sections:**

1. **Device Inventory**
   ```bash
   # For each device, collect:
   routercli exec --device <device> --command "show version"
   routercli exec --device <device> --command "show inventory"
   ```
   
   Extract: Model, Serial Number, IOS Version, Uptime

2. **Interface Documentation**
   ```bash
   routercli exec --device <device> --command "show interfaces"
   routercli exec --device <device> --command "show ip interface brief"
   routercli exec --device <device> --command "show interfaces description"
   ```
   
   Create interface table with: Name, IP, Status, Description

3. **Routing Information**
   ```bash
   routercli exec --device <device> --command "show ip route summary"
   routercli exec --device <device> --command "show ip protocols"
   ```

4. **Security Configuration**
   ```bash
   routercli run --device <device> --preset security_audit
   ```

**Output Format:**
Create markdown documentation for each device:
```markdown
# Device: Router1 (192.168.1.1)

## Hardware Information
- Model: Cisco ISR 4451
- Serial: ABC123456
- IOS Version: 17.3.4

## Interfaces
| Interface | IP Address | Status | Description |
|-----------|------------|--------|-------------|
| Gi0/0     | 10.1.1.1   | up/up  | To Core     |

## Routing
- OSPF: Enabled (Area 0)
- BGP: AS 65001

## Last Updated
2024-10-17 10:30:00
```

### 3. Root Cause Analysis (RCA)

When network issues are detected, perform systematic analysis using RouterCLI Pro.

**Phase 1: Problem Classification**

Classify the issue type:
- Connectivity issues (unreachable, packet loss)
- Performance issues (latency, bandwidth)
- Routing issues (route flaps, BGP down)
- Interface issues (link down, errors)
- Hardware issues (CPU, memory)
- Configuration issues

**Phase 2: Initial Data Collection**

Use the `troubleshoot_connectivity` preset for quick diagnostics:
```bash
routercli run --device <affected-device> --username admin \
  --preset troubleshoot_connectivity --json
```

This runs 5 troubleshooting commands automatically.

**Phase 3: Detailed Device Analysis**

Collect comprehensive data from affected devices:

```bash
# Device health
routercli run --device <device> --preset health_check

# Network status
routercli run --device <device> --preset network_status

# Interface details
routercli run --device <device> --preset interface_check

# Routing information
routercli run --device <device> --preset routing_overview
```

**Phase 4: Specific Issue Investigation**

Based on issue type, collect targeted data:

**For Connectivity Issues:**
```bash
routercli batch --device <device> \
  -c "show ip interface brief" \
  -c "show cdp neighbors" \
  -c "show interfaces" \
  -c "show ip route" \
  -c "show arp"
```

**For Performance Issues:**
```bash
routercli batch --device <device> \
  -c "show processes cpu sorted" \
  -c "show memory statistics" \
  -c "show interfaces counters errors" \
  -c "show interfaces counters" \
  -c "show queueing"
```

**For Routing Issues:**
```bash
routercli batch --device <device> \
  -c "show ip route summary" \
  -c "show ip protocols" \
  -c "show ip ospf neighbor" \
  -c "show ip bgp summary" \
  -c "show ip route <specific-network>"
```

**For Interface Issues:**
```bash
routercli batch --device <device> \
  -c "show interfaces <interface>" \
  -c "show controllers <interface>" \
  -c "show interfaces <interface> stats" \
  -c "show logging | include <interface>"
```

**Phase 5: Timeline Reconstruction**

Gather logs from all affected devices:
```bash
routercli exec --device <device> --command "show logging"
routercli exec --device <device> --command "show logging | include ERROR"
routercli exec --device <device> --command "show logging | include %"
```

Parse timestamps and correlate events across devices.

**Phase 6: Pattern Analysis**

Compare collected data against known patterns (see `references/network_patterns.md`):
- Interface flapping patterns
- Routing protocol instability
- Hardware degradation signs
- Configuration inconsistencies

**Phase 7: Generate RCA Report**

Compile findings into structured report:
```markdown
# Root Cause Analysis: <Issue Description>

## Executive Summary
- **Issue:** <Brief description>
- **Duration:** <Time range>
- **Impact:** <Affected services/users>
- **Root Cause:** <Identified cause>

## Timeline
- HH:MM:SS - [Device] Event description
- ...

## Detailed Findings
### Critical Issues
- Finding 1
- Finding 2

### Supporting Evidence
<Command outputs>

## Root Cause
<Detailed explanation>

## Remediation Steps
1. Step 1
2. Step 2

## Prevention Measures
- Measure 1
- Measure 2
```

## Key RouterCLI Pro Patterns

### Batch Operations for Efficiency

When analyzing multiple devices or executing multiple commands:

```bash
# Multiple commands on one device
routercli batch --device 192.168.1.1 --username admin \
  -c "show version" \
  -c "show ip interface brief" \
  -c "show ip route summary" \
  -c "show processes cpu"

# Commands from file
echo "show version" > commands.txt
echo "show interfaces" >> commands.txt
echo "show ip route" >> commands.txt

routercli batch --device 192.168.1.1 --username admin --file commands.txt
```

### JSON Output for Processing

Use `--json` flag for programmatic processing:

```bash
routercli exec --device 192.168.1.1 --username admin \
  --command "show ip interface brief" --json > output.json
```

JSON structure:
```json
{
  "success": true,
  "data": {
    "hostname": "Router1",
    "command": "show ip interface brief",
    "output": "...",
    "output_summary": "3 interfaces up, 1 down",
    "execution_time_ms": 234.5
  }
}
```

### Connection Caching

RouterCLI Pro automatically caches connections for efficiency:

```bash
# First command establishes connection
routercli exec --device 192.168.1.1 --username admin --command "show version"

# Subsequent commands reuse cached connection (much faster)
routercli exec --device 192.168.1.1 --username admin --command "show interfaces"

# View cached connections
routercli cache

# Clear cache when done
routercli clear-cache
```

### Authentication Options

```bash
# Password-based
routercli connect --device 192.168.1.1 --username admin --password <pass>

# SSH key (preferred)
routercli connect --device 192.168.1.1 --username admin --ssh-key ~/.ssh/id_rsa

# Environment variables
export ROUTERCLI_USERNAME=admin
export ROUTERCLI_PASSWORD=<pass>
routercli connect --device 192.168.1.1
```

## Topology Discovery Algorithm

Use RouterCLI Pro commands in this sequence:

1. **Initialize with Seed Device**
   - Start with core router or distribution switch
   - Keep list of discovered devices and devices to process

2. **For Each Device to Process:**

   a. **Test Connectivity**
   ```bash
   routercli connect --device <device-ip> --username admin
   ```

   b. **Get Device Hostname**
   ```bash
   routercli exec --device <device-ip> --command "show running-config | include hostname"
   ```

   c. **Discover CDP Neighbors**
   ```bash
   routercli exec --device <device-ip> --command "show cdp neighbors detail"
   ```
   
   Parse output for:
   - Neighbor hostnames
   - Neighbor IP addresses
   - Local and remote interfaces
   
   d. **Discover LLDP Neighbors** (if CDP not available)
   ```bash
   routercli exec --device <device-ip> --command "show lldp neighbors detail"
   ```

   e. **Get Interface Status**
   ```bash
   routercli exec --device <device-ip> --command "show ip interface brief"
   ```

   f. **Get Routing Neighbors** (optional)
   ```bash
   routercli batch --device <device-ip> \
     -c "show ip ospf neighbor" \
     -c "show ip bgp summary" \
     -c "show ip eigrp neighbors"
   ```

3. **Process Discovered Neighbors**
   - Add new neighbor IPs to "devices to process" list
   - Skip already processed devices
   - Continue until all devices processed or limit reached

4. **Build Topology Graph**
   - Create nodes for each device
   - Create edges for each connection
   - Store as JSON or graph structure

5. **Enhance with Device Details**
   For each device, run:
   ```bash
   routercli run --device <device-ip> --preset health_check --json
   ```
   
   Extract: model, version, uptime, memory, CPU

## Root Cause Analysis Framework

### Systematic RCA Process Using RouterCLI Pro

**Phase 1: Problem Definition**
- Exact symptoms and error messages
- Time of onset and duration
- Scope (which devices/services affected)
- Recent changes in network

**Phase 2: Data Collection Using RouterCLI Pro**

**Quick Health Check:**
```bash
# Run on all suspected devices
routercli run --device <device> --preset health_check --json
```

**Detailed Diagnostics:**
```bash
# Logs and errors
routercli exec --device <device> --command "show logging"
routercli exec --device <device> --command "show logging | include ERROR"
routercli exec --device <device> --command "show logging | include %SYS-"

# Interface statistics
routercli exec --device <device> --command "show interfaces"
routercli exec --device <device> --command "show interfaces counters errors"

# Routing information  
routercli exec --device <device> --command "show ip route"
routercli exec --device <device> --command "show ip protocols"

# Neighbor status
routercli exec --device <device> --command "show cdp neighbors"
routercli exec --device <device> --command "show ip ospf neighbor"

# Resource usage
routercli exec --device <device> --command "show processes cpu sorted"
routercli exec --device <device> --command "show memory statistics"

# Configuration
routercli exec --device <device> --command "show running-config"
```

**Phase 3: Pattern Analysis**

Compare collected data against known patterns in `references/network_patterns.md`:

**Link Flapping:**
- Look for repeated "line protocol up/down" messages
- Check interface error counters
- Verify physical layer (show controllers)

**Routing Issues:**
- Verify neighbor relationships are up
- Check route count changes
- Look for route flapping in logs

**Hardware Failures:**
- Check CPU usage (sustained >80%)
- Check memory usage (>90%)
- Look for hardware error messages

**Configuration Errors:**
- Compare configs across devices
- Check for recent changes
- Verify interface assignments

**Capacity Issues:**
- Check interface utilization
- Verify bandwidth consumption
- Review queue drops

**Phase 4: Multi-Device Correlation**

Collect same data from multiple devices and correlate:

```bash
# Create list of devices to check
devices="192.168.1.1 192.168.1.2 192.168.1.3"

# Collect logs from all devices
for device in $devices; do
  routercli exec --device $device --command "show logging | include <time-range>"
done
```

Build timeline from all device logs to identify:
- Event sequence
- Propagation pattern
- Root source of issue

**Phase 5: Hypothesis Testing**

Based on evidence, test likely root causes:

```bash
# Test hypothesis: Interface flapping due to errors
routercli exec --device <device> --command "show interfaces <interface>"

# Test hypothesis: Routing loop
routercli exec --device <device> --command "show ip route <destination>"
routercli exec --device <device> --command "traceroute <destination>"

# Test hypothesis: High CPU due to process
routercli exec --device <device> --command "show processes cpu sorted"
routercli exec --device <device> --command "show processes | include <process-name>"
```

**Phase 6: Documentation**

Generate report with:
- Executive summary
- Detailed timeline (from correlated logs)
- Root cause identification
- Supporting evidence (command outputs)
- Remediation steps
- Prevention measures

## Advanced Use Cases

### Topology Change Detection

**Baseline Collection:**
```bash
# Collect initial topology snapshot
routercli exec --device <device> --command "show cdp neighbors" > baseline_cdp.txt
routercli exec --device <device> --command "show ip interface brief" > baseline_interfaces.txt
```

**Periodic Comparison:**
```bash
# Collect current state
routercli exec --device <device> --command "show cdp neighbors" > current_cdp.txt

# Compare
diff baseline_cdp.txt current_cdp.txt
```

Look for:
- New devices appeared
- Devices disappeared
- Interface changes
- Connection changes

### Network Path Tracing

Trace path between two endpoints:

```bash
# Start from source device
routercli exec --device <source-device> --command "show ip route <destination-ip>"

# Check each hop
routercli exec --device <hop-device> --command "show ip route <destination-ip>"
routercli exec --device <hop-device> --command "show ip cef <destination-ip>"

# Verify ARP
routercli exec --device <device> --command "show arp | include <ip>"

# Check interface status at each hop
routercli exec --device <device> --command "show interfaces <interface>"
```

### Configuration Backup

Collect configurations from all devices:

```bash
# For each device
routercli exec --device <device> --command "show running-config" > config_<device>_<date>.txt
routercli exec --device <device> --command "show startup-config" > startup_<device>_<date>.txt

# Also backup version info
routercli exec --device <device> --command "show version" > version_<device>_<date>.txt
```

Store in version control system for change tracking.

### Compliance Checking

Verify network against security baseline:

**Check Security Configurations:**
```bash
routercli run --device <device> --preset security_audit --json
```

**Verify Specific Settings:**
```bash
# Check if SSH is enabled
routercli exec --device <device> --command "show ip ssh"

# Verify ACLs
routercli exec --device <device> --command "show access-lists"

# Check logging configuration
routercli exec --device <device> --command "show logging"

# Verify NTP
routercli exec --device <device> --command "show ntp status"

# Check SNMP configuration
routercli exec --device <device> --command "show snmp"
```

Compare output against security baseline defined in `references/security_baseline.md`.

### Batch Device Operations

**Health Check All Devices:**
```bash
# Read device list
devices=$(cat device_list.txt)

# Run health check on all
for device in $devices; do
  echo "Checking $device..."
  routercli run --device $device --preset health_check --json > health_$device.json
done
```

**Interface Status Across Network:**
```bash
for device in $devices; do
  routercli exec --device $device --command "show ip interface brief"
done
```

**Collect Logs from All Devices:**
```bash
for device in $devices; do
  routercli exec --device $device \
    --command "show logging | include ERROR" > logs_$device.txt
done
```

## Best Practices

### Topology Discovery
- Start with core/distribution devices as seeds
- Use read-only credentials when possible
- Run during maintenance windows for production networks
- Validate discovered topology against documentation
- Store topology snapshots with timestamps
- Re-discover periodically (daily/weekly)

### Documentation
- Keep documentation in version control
- Update after network changes
- Include contact information for device owners
- Document non-standard configurations
- Link to vendor documentation
- Include troubleshooting runbooks

### Root Cause Analysis
- Gather data quickly before logs rotate
- Preserve evidence (save all outputs)
- Document timeline accurately
- Involve relevant teams early
- Test remediation in lab if possible
- Conduct post-incident review

## Error Handling with RouterCLI Pro

RouterCLI Pro provides rich error context and suggestions when issues occur.

### Common Error Scenarios

**Connection Timeout:**
```bash
routercli connect --device 192.168.1.1 --username admin
```

If timeout occurs, RouterCLI Pro suggests:
- Check network connectivity to device
- Verify IP address or hostname
- Check if SSH/Telnet service is running
- Try increasing timeout value
- Test manual connection

**Authentication Failed:**
```bash
routercli connect --device 192.168.1.1 --username admin --password wrong
```

RouterCLI Pro suggests:
- Verify username and password
- Try SSH key authentication
- Check if account is locked
- Verify enable password if needed

**Command Not Supported:**
```bash
routercli exec --device <device> --command "unsupported command"
```

RouterCLI Pro suggests:
- Check device type compatibility
- Try alternative command
- Verify command syntax

### Recovery Strategies

**Strategy 1: Fallback to Telnet**
```bash
# Try SSH first
routercli connect --device <device> --connection-type ssh

# If fails, try Telnet
routercli connect --device <device> --connection-type telnet
```

**Strategy 2: Adjust Timeout**
```bash
# For slow devices, increase timeout
routercli connect --device <device> --timeout 60
```

**Strategy 3: Use Alternative Commands**
```bash
# If "show cdp neighbors detail" fails, try:
routercli exec --device <device> --command "show cdp neighbors"

# Or try LLDP instead:
routercli exec --device <device> --command "show lldp neighbors"
```

**Strategy 4: Check Device Type**
```bash
# Explicitly specify device type
routercli connect --device <device> --device-type juniper
```

### JSON Output for Error Handling

When using `--json` flag, errors are structured:

```json
{
  "success": false,
  "error_code": "CONNECTION_TIMEOUT",
  "error_message": "Connection timeout to 192.168.1.1",
  "context": {
    "device": "192.168.1.1",
    "timeout_seconds": 30,
    "suggestions": [
      "Check network connectivity to device",
      "Verify host IP address or hostname",
      "Try increasing timeout value"
    ]
  }
}
```

This allows programmatic error handling and automated retry logic.

## Integration Patterns

### Automation Scripts

RouterCLI Pro can be called from shell scripts for automation:

```bash
#!/bin/bash
# Daily network health check

DEVICES="192.168.1.1 192.168.1.2 192.168.1.3"
DATE=$(date +%Y%m%d)
OUTPUT_DIR="./reports/$DATE"

mkdir -p $OUTPUT_DIR

for device in $DEVICES; do
    echo "Checking $device..."
    
    # Run health check
    routercli run --device $device --username admin \
        --preset health_check --json > "$OUTPUT_DIR/${device}_health.json"
    
    # Check for errors
    routercli exec --device $device --username admin \
        --command "show logging | include ERROR" > "$OUTPUT_DIR/${device}_errors.txt"
done

echo "Health check complete. Reports in $OUTPUT_DIR"
```

### Monitoring Integration

**Export to Monitoring Systems:**
```bash
# Collect interface status
routercli exec --device <device> --command "show ip interface brief" --json

# Parse JSON and send to monitoring (Prometheus, Nagios, etc.)
```

**Alert on Issues:**
```bash
# Check for down interfaces
output=$(routercli exec --device <device> --command "show ip interface brief")

if echo "$output" | grep -q "down.*down"; then
    # Send alert
    curl -X POST https://alerts.company.com/network \
        -d '{"device": "router1", "alert": "Interface down"}'
fi
```

### Documentation in Version Control

```bash
#!/bin/bash
# Automated documentation update

# Discover topology
# (use RouterCLI Pro commands as shown in Topology Discovery section)

# Generate markdown docs for each device
# (use RouterCLI Pro commands as shown in Documentation Generation section)

# Commit to git
git add network-docs/
git commit -m "Update network documentation $(date)"
git push
```

## Reference Material

For detailed information on common network issues and patterns:
- **Network Patterns**: See `references/network_patterns.md` for common failure modes and solutions
- **Security Baseline**: See `references/security_baseline.md` for security configuration standards
- **Troubleshooting Guide**: See `references/troubleshooting_guide.md` for systematic troubleshooting procedures

## Complete Workflow Example

Full workflow for discovering and documenting a new network:

### Step 1: Test Initial Connectivity

```bash
routercli connect --device 192.168.1.1 --username admin
```

### Step 2: Discover Topology

```bash
# Get seed device neighbors
routercli exec --device 192.168.1.1 --username admin \
    --command "show cdp neighbors detail" > neighbors.txt

# Parse neighbors.txt to extract IP addresses
# For each discovered IP, repeat:
routercli exec --device <neighbor-ip> --username admin \
    --command "show cdp neighbors detail"

# Continue recursively until all devices discovered
```

### Step 3: Collect Device Details

```bash
# For each discovered device
routercli run --device <device-ip> --username admin \
    --preset full_status --json > device_<name>.json
```

### Step 4: Generate Documentation

Create markdown files from collected data:
- Parse JSON outputs
- Extract hostname, version, interfaces
- Build device inventory tables
- Create topology diagram from connections
- Generate per-device documentation

### Step 5: Set Up Monitoring

Create scheduled health checks:

```bash
#!/bin/bash
# /etc/cron.daily/network-health-check

devices="192.168.1.1 192.168.1.2 192.168.1.3"

for device in $devices; do
    routercli run --device $device --username admin \
        --preset health_check --json
done
```

### Step 6: Root Cause Analysis (When Issues Occur)

```bash
# Identify affected device
affected_device="192.168.1.2"

# Run troubleshooting preset
routercli run --device $affected_device --username admin \
    --preset troubleshoot_connectivity

# Collect detailed diagnostics
routercli batch --device $affected_device --username admin \
    -c "show logging" \
    -c "show interfaces" \
    -c "show processes cpu sorted" \
    -c "show memory statistics"

# Check neighbors
routercli exec --device $affected_device --username admin \
    --command "show cdp neighbors"

# Analyze and document findings
```

## Output Examples

All scripts produce structured output optimized for both human reading and programmatic processing.

**Topology JSON structure:**
```json
{
  "discovered_at": "2024-10-17T10:30:00Z",
  "seed_devices": ["192.168.1.1"],
  "devices": {
    "router1": {
      "hostname": "R1-Core",
      "management_ip": "192.168.1.1",
      "device_type": "router",
      "model": "Cisco ISR 4451",
      "os_version": "IOS-XE 17.3.4",
      "interfaces": [...],
      "neighbors": [...]
    }
  },
  "connections": [
    {
      "source": "router1",
      "source_interface": "GigabitEthernet0/0/0",
      "target": "switch1",
      "target_interface": "GigabitEthernet1/0/1",
      "protocol": "CDP"
    }
  ],
  "metadata": {
    "total_devices": 45,
    "device_types": {"routers": 5, "switches": 38, "firewalls": 2},
    "discovery_duration_seconds": 234.5
  }
}
```

**RCA Report structure:**
```markdown
# Root Cause Analysis: Connectivity Loss Site A to Site B

**Incident Date:** 2024-10-17 14:23:00 UTC
**Duration:** 23 minutes
**Severity:** P1 - Critical
**Affected Services:** VoIP, ERP application

## Executive Summary
[Concise summary of issue, root cause, and resolution]

## Timeline
[Detailed event timeline]

## Root Cause
[Identified root cause with evidence]

## Impact Assessment
[Quantified impact]

## Remediation
[Steps taken to resolve]

## Prevention
[Measures to prevent recurrence]

## Appendix
[Supporting data and evidence]
```
