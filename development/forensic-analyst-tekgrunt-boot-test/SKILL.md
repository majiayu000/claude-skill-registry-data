---
name: forensic-analyst
description: Use this skill when users need to conduct digital forensics investigations, perform timeline reconstruction, analyze memory dumps, examine artifacts, or build comprehensive forensic reports using LimaCharlie's forensic capabilities.
---

# LimaCharlie Forensic Analyst

This skill provides expert guidance for conducting comprehensive digital forensics investigations using LimaCharlie. Use this skill to help users perform deep forensic analysis, reconstruct attack timelines, analyze artifacts, and build evidence-based forensic reports.

## Quick Start Guide

**Need to investigate an incident? Start here:**

1. **Identify scope**: What systems? What timeframe? What type of incident?
2. **Preserve volatile data first**: Memory, running processes, network connections
3. **Collect evidence systematically**: Files, logs, artifacts
4. **Build timeline**: Reconstruct chronological sequence of events
5. **Analyze and correlate**: Test hypotheses with targeted queries
6. **Document findings**: Maintain chain of custody and report objectively

## Navigation

This skill is organized for progressive disclosure:

- **SKILL.md** (this file): Core methodology, quick start, common workflows
- **REFERENCE.md**: Complete sensor commands, LCQL syntax, artifact types, event types
- **EXAMPLES.md**: Complete investigation scenarios (ransomware, insider threat, web shell)
- **ADVANCED.md**: Deep-dive memory analysis, registry forensics, network analysis
- **TROUBLESHOOTING.md**: Common issues and solutions

## Digital Forensics Principles

### Core Principles

1. **Evidence Preservation**: Maintain integrity of evidence from collection to presentation
2. **Chain of Custody**: Document all evidence handling and access
3. **Non-Destructive Analysis**: Analyze without altering original evidence
4. **Repeatability**: Ensure investigations can be replicated with same results
5. **Documentation**: Maintain detailed records of all investigative steps
6. **Timeline Construction**: Establish chronological sequence of events
7. **Context Awareness**: Understand evidence within system and business context

### Types of Investigations

**Incident Response Forensics**: Active incident analysis, attack vector identification, threat containment

**Post-Incident Forensics**: Reconstruction of completed attacks, impact assessment, legal evidence

**Proactive Forensics**: Threat hunting, anomaly detection, baseline establishment

**Compliance Forensics**: Audit trails, policy violations, regulatory evidence

---

## Working with Timestamps

**IMPORTANT**: When users provide relative time offsets (e.g., "last hour", "past 24 hours", "last week"), you MUST dynamically compute the current epoch timestamp based on the actual current time. Never use hardcoded or placeholder timestamps.

### Computing Current Epoch

```python
import time

# Compute current time dynamically
current_epoch_seconds = int(time.time())
current_epoch_milliseconds = int(time.time() * 1000)
```

**The granularity (seconds vs milliseconds) depends on the specific API or MCP tool**. Always check the tool signature or API documentation to determine which unit to use.

### Common Relative Time Calculations

**Example: "Show me events from the last hour"**
```python
end_time = int(time.time())  # Current time
start_time = end_time - 3600  # 1 hour ago
```

**Common offsets (in seconds)**:
- 1 hour = 3600
- 24 hours = 86400
- 7 days = 604800
- 30 days = 2592000

**For millisecond-based APIs, multiply by 1000**.

### Critical Rules

**NEVER**:
- Use hardcoded timestamps
- Use placeholder values like `1234567890`
- Assume a specific current time

**ALWAYS**:
- Compute dynamically using `time.time()`
- Check the API/tool signature for correct granularity
- Verify the time range is valid (start < end)

---

## 6-Phase Forensic Methodology

### Phase 1: Identification

**Determine Investigation Scope**:
- What systems are affected?
- What is the suspected timeframe?
- What type of incident (malware, intrusion, data theft)?
- What evidence sources are available?

**Select Target Sensors**:
```
# Via LCQL: Filter by hostname, tags, or platform
routing/hostname == "compromised-host"
routing/tags contains "investigation"
plat == windows
```

### Phase 2: Preservation

**Collect Volatile Data First** (Order of Volatility):

1. System Memory
2. Running Processes: `os_processes`
3. Network Connections: `netstat`
4. Logged-in Users: `os_users` (Windows)
5. Command History: `history_dump`

**Document Chain of Custody**: Who, What, When, Where, Why, How

### Phase 3: Collection

**File System Evidence**:
```bash
dir_list C:\Users\victim\Downloads
file_info C:\path\to\suspicious.exe
file_hash C:\path\to\suspicious.exe
artifact_get C:\path\to\suspicious.exe
```

**Event Logs (Windows)**:
```bash
log_get Security
log_get System
artifact_get C:\Windows\System32\winevt\Logs\Security.evtx
```

**Registry Artifacts**:
```bash
os_autoruns
artifact_get C:\Windows\System32\config\SYSTEM
```

See REFERENCE.md for complete command reference.

### Phase 4: Examination

**Timeline Analysis**:
```
# Process execution timeline
-24h | plat == windows | NEW_PROCESS | event/TIMESTAMP as time event/FILE_PATH as process event/COMMAND_LINE as cmdline routing/hostname as host

# File modification timeline
-24h | plat == windows | FILE_MODIFIED | event/TIMESTAMP as time event/FILE_PATH as file routing/hostname as host

# Network connection timeline
-12h | plat == windows | NETWORK_CONNECTIONS | event/TIMESTAMP as time event/NETWORK_ACTIVITY/DESTINATION/IP_ADDRESS as dst_ip event/FILE_PATH as process routing/hostname as host
```

**Pattern Detection**: Identify related events, correlate across event types, build process trees

### Phase 5: Analysis

**Hypothesis-Driven Analysis**:
1. Develop theories based on initial evidence
2. Test hypotheses with targeted queries
3. Validate or refute with additional evidence
4. Refine understanding iteratively

**Attribution Analysis**: Map to MITRE ATT&CK, identify TTPs, establish timeline of attacker actions

**Impact Assessment**: What data accessed? What systems compromised? What modifications made?

### Phase 6: Reporting

**Document Findings**: Executive summary, timeline of events, evidence inventory, analysis methodology, conclusions, recommendations, technical appendices

See TROUBLESHOOTING.md if you encounter issues during investigation.

---

## Most Common Investigations

### Investigating Suspicious Process

**Quick Workflow**:
```bash
# 1. Get current processes
os_processes

# 2. Get historical execution
history_dump

# 3. Timeline query
-24h | plat == windows | NEW_PROCESS | event/FILE_PATH contains "suspicious" | event/TIMESTAMP as time event/COMMAND_LINE as cmdline event/PARENT/FILE_PATH as parent routing/hostname as host

# 4. Check code signature
-24h | plat == windows | CODE_IDENTITY | event/FILE_PATH contains "suspicious" | event/SIGNATURE/FILE_IS_SIGNED as signed event/HASH as hash

# 5. Memory analysis (if still running)
mem_map --pid <pid>
mem_strings --pid <pid>
```

### Investigating Network Connections

**Quick Workflow**:
```bash
# 1. Current connections
netstat

# 2. Historical connections
-24h | routing/hostname == "target-host" | NETWORK_CONNECTIONS | event/TIMESTAMP as time event/NETWORK_ACTIVITY/DESTINATION/IP_ADDRESS as dst_ip event/NETWORK_ACTIVITY/DESTINATION/PORT as port event/FILE_PATH as process

# 3. DNS queries
-24h | routing/hostname == "target-host" | DNS_REQUEST | event/DOMAIN_NAME as domain event/TIMESTAMP as time

# 4. Suspicious patterns (beaconing, high volume)
-24h | plat == windows | NETWORK_CONNECTIONS | event/NETWORK_ACTIVITY/DESTINATION/IP_ADDRESS as dst COUNT(event) as conn_count GROUP BY(dst) | conn_count > 50
```

### Investigating File Activity

**Quick Workflow**:
```bash
# 1. File metadata
file_info C:\path\to\suspicious.exe
file_hash C:\path\to\suspicious.exe

# 2. File timeline
-24h | plat == windows | NEW_DOCUMENT FILE_MODIFIED FILE_DELETE | event/FILE_PATH contains "suspicious" | event/TIMESTAMP as time routing/event_type as activity

# 3. Hash correlation (find all instances)
-7d | plat == windows | CODE_IDENTITY | event/HASH == "abc123..." | event/FILE_PATH as path routing/hostname as host

# 4. Collect evidence
artifact_get C:\path\to\suspicious.exe
```

### Investigating User Activity

**Quick Workflow**:
```
# 1. All activity by user
-24h | plat == windows | NEW_PROCESS | event/USER_NAME == "DOMAIN\\user" | event/TIMESTAMP as time event/FILE_PATH as process event/COMMAND_LINE as cmdline routing/hostname as host

# 2. Login timeline
-24h | plat == windows | WEL | event/EVENT/System/EventID == "4624" and event/EVENT/EventData/TargetUserName == "user" | event/TIMESTAMP as time routing/hostname as host event/EVENT/EventData/LogonType as type

# 3. File access
-24h | routing/hostname == "user-workstation" | FILE_TYPE_ACCESSED | event/TIMESTAMP as time event/FILE_PATH as file
```

For complete investigation scenarios, see EXAMPLES.md.

---

## Quick Command Reference

### Live Collection Commands

**Process Analysis**:
- `os_processes` - List running processes
- `history_dump` - Dump recent process history

**Network Analysis**:
- `netstat` - Current network connections
- Network timeline via LCQL (see REFERENCE.md)

**Memory Analysis**:
- `mem_map --pid <pid>` - Process memory map
- `mem_strings --pid <pid>` - Extract strings from memory
- `mem_find_string --pid <pid> --string "text"` - Search memory
- `mem_read --pid <pid> --base <addr> --size <bytes>` - Read memory region
- `mem_handles --pid <pid>` - List open handles (Windows)

**File Analysis**:
- `file_info <path>` - Get file metadata
- `file_hash <path>` - Calculate file hash
- `artifact_get <path>` - Collect file
- `dir_list <path>` - List directory contents
- `dir_find_hash <path> --hash <hash>` - Find files by hash

**System State**:
- `os_autoruns` - Get autorun entries
- `os_services` - List services
- `os_packages` - List installed packages
- `os_drivers` - List drivers (Windows)
- `os_users` - List logged-in users (Windows)
- `log_get <logname>` - Get Windows event log

For complete command syntax and options, see REFERENCE.md.

### Essential LCQL Patterns

**Time-Based Queries**:
```
-24h | <filters>          # Last 24 hours
-7d | <filters>           # Last 7 days
-30d | <filters>          # Last 30 days
```

**Event Type Filtering**:
```
| NEW_PROCESS              # Process creation
| NETWORK_CONNECTIONS      # Network activity
| FILE_MODIFIED            # File changes
| REGISTRY_WRITE           # Registry modifications
| DNS_REQUEST              # DNS queries
| WEL                      # Windows Event Logs
```

**Field Selection**:
```
| event/TIMESTAMP as time
| event/FILE_PATH as process
| event/COMMAND_LINE as cmdline
| routing/hostname as host
| routing/event_type as event_type
```

**Aggregation**:
```
| COUNT(event) as count
| COUNT_UNIQUE(routing/sid) as sensor_count
| GROUP BY(field1 field2)
```

For complete LCQL reference, see REFERENCE.md.

---

## Key Forensic Artifacts

### Windows Artifacts

**Execution Artifacts**:
- Prefetch files: `C:\Windows\Prefetch\*.pf`
- AmCache: `C:\Windows\AppCompat\Programs\Amcache.hve`
- Shimcache: Registry key `SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache`
- UserAssist: `NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist`

**Persistence Locations**:
- Registry Run keys: `HKLM\Software\Microsoft\Windows\CurrentVersion\Run`
- Services: `HKLM\System\CurrentControlSet\Services`
- Scheduled tasks: Windows Event ID 4698, Task Scheduler logs
- Startup folders: `C:\Users\*\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`

**User Activity**:
- Browser history: Chrome, Firefox, Edge (see REFERENCE.md for paths)
- Recent files: `C:\Users\*\AppData\Roaming\Microsoft\Windows\Recent\*`
- Jump lists: `C:\Users\*\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations\*`
- Shellbags: `NTUSER.DAT`, `UsrClass.dat`

**Event Logs**:
- Security: Authentication, privileges, account changes
- System: Services, drivers, system events
- Application: Application-specific events
- Sysmon: Process, network, file, registry events

### Linux Artifacts

**Command History**:
- `/home/*/.bash_history`
- `/root/.bash_history`
- `/home/*/.zsh_history`

**System Logs**:
- `/var/log/auth.log` (Debian/Ubuntu)
- `/var/log/secure` (RHEL/CentOS)
- `/var/log/syslog`
- `/var/log/messages`

**Persistence**:
- Cron jobs: `/etc/crontab`, `/var/spool/cron/crontabs/*`
- Systemd services: `/etc/systemd/system/*`, `/lib/systemd/system/*`
- SSH keys: `/home/*/.ssh/authorized_keys`, `/root/.ssh/authorized_keys`
- Shell profiles: `/etc/profile`, `~/.bashrc`, `~/.bash_profile`

For complete artifact reference, see REFERENCE.md.

---

## Evidence Preservation Best Practices

### Chain of Custody

**Required Documentation**:
- **Who**: Name and role of collector
- **What**: Specific evidence collected
- **When**: Date and time (UTC recommended)
- **Where**: Source system (hostname, IP, sensor ID)
- **Why**: Incident ID or case number
- **How**: Collection method and tools

**Investigation ID Tagging**:
```bash
artifact_get C:\malware.exe --investigation incident-2024-001
history_dump --investigation incident-2024-001
```

### Evidence Integrity

**Hash Verification Workflow**:
1. Hash file on endpoint: `file_hash C:\evidence\file.exe`
2. Document hash in evidence log
3. Collect: `artifact_get C:\evidence\file.exe`
4. Download from Artifact Collection
5. Verify hash matches original
6. Document verification

**Read-Only Analysis**: Never modify originals, work on copies, use write-blockers for disk images

### Storage and Retention

**LimaCharlie Artifact Storage**:
- Encrypted at rest and in transit
- Configurable retention periods
- Access logging and audit trail
- Role-based access control

**Retention Configuration**:
```yaml
# Set retention when collecting
- action: extension request
  extension name: ext-dumper
  extension action: request_dump
  extension request:
    target: memory
    sid: <<routing.sid>>
    retention: 90  # days
```

For detailed evidence preservation procedures, see REFERENCE.md.

---

## Common Suspicious Indicators

### Process Indicators

- Office apps (Word, Excel) spawning cmd.exe or powershell.exe
- Browser processes launching unusual children
- Processes running from temp directories
- Processes with no disk backing (memory-only malware)
- Unsigned or rarely seen executables
- Suspicious command-line arguments (encoded PowerShell, download cradles)

### Network Indicators

- Connections to non-RFC1918 addresses from unexpected processes
- Beaconing behavior (repetitive connections to same destination)
- Large outbound data transfers
- DNS tunneling (excessively long domain names)
- Connections to DGA domains or unusual TLDs
- Low prevalence domains (resolved by few systems)

### File Indicators

- Files in temp directories with executable extensions
- Hidden files or files with unusual attributes
- Double extensions (e.g., document.pdf.exe)
- Files created/modified outside business hours
- Mass file modifications (potential ransomware)
- Files with suspicious hashes (check threat intelligence)

### Registry Indicators (Windows)

- Modifications to Run/RunOnce keys
- Changes to Winlogon keys
- Service creation or modification
- AppInit DLL changes
- Image File Execution Options (debugger hijacking)

For detailed indicator analysis, see EXAMPLES.md.

---

## Investigation Tips

**Start Broad, Then Narrow**: Begin with wide time windows and broad queries, identify patterns, then drill down into specific timeframes.

**Correlate Multiple Data Sources**: Match process execution with network connections, correlate file creation with process execution, cross-reference findings.

**Think Like an Attacker**: Map findings to MITRE ATT&CK framework. Consider: Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection, Exfiltration.

**Document Everything**: Every command, query, finding, hypothesis, and conclusion for reproducibility and reporting.

---

## Integration with Forensic Tools

**Memory Analysis**: Collect via Dumper extension, analyze with Volatility, Rekall, WinDbg, GDB. See ADVANCED.md.

**Disk Forensics**: Collect MFT, analyze with MFTExplorer, analyzeMFT, NTFS Log Tracker, Plaso. See ADVANCED.md.

**Registry Analysis**: Collect hives, analyze with Registry Explorer, RegRipper, Registry Decoder. See ADVANCED.md.

**Network Analysis**: Collect PCAPs, analyze with Wireshark, tcpdump, NetworkMiner, Zeek. See ADVANCED.md.

---

## LimaCharlie Forensic Advantages

1. **Real-time and Historical Visibility**: 1 year telemetry retention
2. **Comprehensive Telemetry**: Process, file, network, registry, authentication events
3. **Powerful Query Language**: LCQL for flexible timeline reconstruction
4. **Automated Artifact Collection**: Files, logs, memory, MFT dumps
5. **Evidence Preservation**: Chain of custody, integrity verification, encrypted storage
6. **Integration Ready**: Export to external forensic tools
7. **Scalable**: Investigate across thousands of endpoints simultaneously

---

## Next Steps

**For detailed command reference**: See REFERENCE.md

**For investigation scenarios**: See EXAMPLES.md (ransomware, insider threat, web shell)

**For advanced techniques**: See ADVANCED.md (memory, registry, network analysis)

**For troubleshooting**: See TROUBLESHOOTING.md

**Need help?**
- Start with the quick workflows above for common investigations
- Reference the 6-phase methodology for systematic investigations
- Use LCQL patterns from REFERENCE.md for timeline queries
- Study complete scenarios in EXAMPLES.md for investigation approaches
