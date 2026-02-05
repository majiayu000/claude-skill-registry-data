---
name: lcql-query-builder
description: Activate when the user needs help writing, optimizing, or understanding LimaCharlie Query Language (LCQL) queries for searching telemetry.
---

# LCQL Query Builder

You are an expert in LimaCharlie Query Language (LCQL), a powerful query language for searching and analyzing security telemetry. Help users write, optimize, and understand LCQL queries.

## What is LCQL?

LCQL (LimaCharlie Query Language) is a structured query language for searching historical telemetry across sensors and events in LimaCharlie. It enables threat hunting, investigation, and analysis of security data.

## Query Structure

LCQL queries follow a pipeline structure with four main components:

```
TIME_RANGE | SENSOR_SELECTOR | EVENT_TYPE | FILTER | PROJECTION
```

### 1. Time Range (Required)

Specify the time window using ParseDuration format:

**Syntax:**
- `-<duration>` where duration uses these units:
  - `h` = hours (e.g., `-3h` = last 3 hours)
  - `m` = minutes (e.g., `-30m` = last 30 minutes)
  - `d` = days (e.g., `-7d` = last 7 days)

**Examples:**
- `-1h` - Last 1 hour
- `-24h` - Last 24 hours
- `-10m` - Last 10 minutes
- `-12h` - Last 12 hours

### 2. Sensor Selector (Required)

Define which sensors to query using selector expressions.

**Available Fields:**
- `sid` - Sensor ID
- `oid` - Organization ID
- `iid` - Installation Key ID
- `plat` - Platform (windows, linux, macos, ios, android, chrome, github, office365, 1password, etc.)
- `ext_plat` - Extended Platform
- `arch` - Architecture
- `hostname` - Host name
- `mac_addr` - MAC address
- `alive` - Last connection time (epoch)
- `ext_ip` - External IP
- `int_ip` - Internal IP
- `isolated` - Network isolation status (boolean)
- `kernel` - Kernel visibility enabled (boolean)
- `did` - Device ID
- `tags` - List of sensor tags

**Operators:**
- `==` - Equals
- `!=` - Not equal
- `in` - Element in list or substring in string
- `not in` - Element not in list or substring not in string
- `matches` - Regex match (use backticks for regex: `` `^10\.3\..*` ``)
- `not matches` - Regex does not match
- `contains` - String contained within element

**Examples:**
- `plat == windows` - All Windows sensors
- `test in tags` - Sensors with "test" tag
- `plat == windows and int_ip matches `^10\.3\..*`` - Windows with IP 10.3.x.x
- `plat contains "azure"` - All Azure-related platforms
- `plat == linux or (isolated == true or evil in tags)` - Linux OR (isolated OR tagged "evil")

**Note:** Platform names starting with numbers need backticks: `` plat == `1password` ``

### 3. Event Type (Required)

Specify which event types to search. Use `*` for all events or space-separated event types.

**Common Event Types:**
- `NEW_PROCESS` - Process creation
- `EXISTING_PROCESS` - Existing processes
- `DNS_REQUEST` - DNS queries
- `NETWORK_CONNECTIONS` - Network connections
- `CODE_IDENTITY` - Code signing information
- `WEL` - Windows Event Logs
- `FILE_TYPE_ACCESSED` - File access
- `*` - All event types

**Examples:**
- `NEW_PROCESS` - Only new process events
- `NEW_PROCESS EXISTING_PROCESS` - Both new and existing processes
- `DNS_REQUEST` - DNS requests only
- `*` - All events

### 4. Filter (Optional)

Filter events based on field values using boolean logic.

**Field Paths:**
- `event/FIELD_NAME` - Access event fields
- `routing/FIELD_NAME` - Access routing metadata (sid, hostname, etc.)
- Nested fields use `/`: `event/PARENT/FILE_PATH`
- Wildcard matching: `event/*` matches any field

**Operators:**
- `==` - Equals
- `!=` - Not equals
- `contains` - Substring match
- `not contains` - Substring not present
- `starts with` - Prefix match
- `ends with` - Suffix match
- `is` - Equality check (alternative to ==)
- `is not` - Inequality check
- `and` - Logical AND
- `or` - Logical OR

**Examples:**
- `event/COMMAND_LINE contains "psexec"` - Command line contains "psexec"
- `event/SIGNATURE/FILE_IS_SIGNED != 1` - Unsigned files
- `event/DOMAIN_NAME contains 'google'` - Domains with "google"
- `event/EVENT/System/EventID == "4624"` - Windows Event ID 4624
- `event/FILE_PATH not contains "powershell"` - File path doesn't contain "powershell"
- `event/* contains 'suspicious'` - Any field contains "suspicious"

**Complex Filters:**
```
event/COMMAND_LINE contains "powershell" and event/FILE_PATH not contains "system32"
```

```
event/public_repo is false and event/actor_location/country_code is not "us"
```

### 5. Projection (Optional)

Control output format, extract fields, aggregate data, and sort results.

**Field Extraction:**
```
event/DOMAIN_NAME as domain
event/FILE_PATH as path
routing/hostname as host
```

**Aggregation Functions:**
- `COUNT(event)` - Count events
- `COUNT_UNIQUE(field)` - Count unique values
- `GROUP BY(field1 field2)` - Group by fields

**Sorting:**
- `ORDER BY(field)` - Sort by field

**Examples:**

Simple field extraction:
```
event/FILE_PATH as path event/COMMAND_LINE as cli routing/hostname as host
```

Count with grouping:
```
event/DOMAIN_NAME as domain COUNT(event) as count GROUP BY(domain)
```

Unique count (prevalence):
```
event/DOMAIN_NAME as domain COUNT_UNIQUE(routing/sid) as sensors GROUP BY(domain)
```

Multiple grouping fields:
```
event/repo as repo event/actor as actor COUNT(event) as count GROUP BY(repo actor)
```

## Complete Query Examples

### Basic Search

**Search for psexec across all Windows systems:**
```
-24h | plat == windows | * | event/* contains 'psexec'
```

### DNS Analysis

**Domain resolution count:**
```
-10m | plat == windows | DNS_REQUEST | event/DOMAIN_NAME contains 'google' | event/DOMAIN_NAME as domain COUNT(event) as count GROUP BY(domain)
```

**Domain prevalence (unique sensors):**
```
-10m | plat == windows | DNS_REQUEST | event/DOMAIN_NAME contains 'google' | event/DOMAIN_NAME as domain COUNT_UNIQUE(routing/sid) as count GROUP BY(domain)
```

### Process Monitoring

**Process command line search:**
```
-1h | plat == windows | NEW_PROCESS EXISTING_PROCESS | event/COMMAND_LINE contains "psexec" | event/FILE_PATH as path event/COMMAND_LINE as cli routing/hostname as host
```

**Unsigned binaries grouped:**
```
-24h | plat == windows | CODE_IDENTITY | event/SIGNATURE/FILE_IS_SIGNED != 1 | event/FILE_PATH as Path event/HASH as Hash event/ORIGINAL_FILE_NAME as OriginalFileName COUNT_UNIQUE(Hash) as Count GROUP BY(Path Hash OriginalFileName)
```

**Stack children by parent process:**
```
-12h | plat == windows | NEW_PROCESS | event/PARENT/FILE_PATH contains "cmd.exe" | event/PARENT/FILE_PATH as parent event/FILE_PATH as child COUNT_UNIQUE(event) as count GROUP BY(parent child)
```

### Windows Event Log (WEL)

**Specific Event ID:**
```
-24h | plat == windows | WEL | event/EVENT/System/EventID == "4624" AND event/EVENT/EventData/LogonType == "10"
```

**Stack logon types by user:**
```
-24h | plat == windows | WEL | event/EVENT/System/EventID == "4624" | event/EVENT/EventData/LogonType AS LogonType event/EVENT/EventData/TargetUserName as UserName COUNT_UNIQUE(event) as Count GROUP BY(UserName LogonType)
```

**Failed logons:**
```
-1h | plat==windows | WEL | event/EVENT/System/EventID == "4625" | event/EVENT/EventData/IpAddress as SrcIP event/EVENT/EventData/LogonType as LogonType event/EVENT/EventData/TargetUserName as Username event/EVENT/EventData/WorkstationName as SrcHostname
```

**Overpass-the-Hash detection:**
```
-12h | plat == windows | WEL | event/EVENT/System/EventID == "4624" and event/EVENT/EventData/LogonType == "9" and event/EVENT/EventData/AuthenticationPackageName == "Negotiate" and event/EVENT/EventData/LogonProcess == "seclogo"
```

### GitHub Telemetry

**Protected branch override from outside US:**
```
-12h | plat == github | protected_branch.policy_override | event/public_repo is false and event/actor_location/country_code is not "us" | event/repo as repo event/actor as actor COUNT(event) as count GROUP BY(repo actor)
```

## Query Execution Modes

### CLI Usage

When using the Python CLI (`limacharlie query`), set context first:

```bash
set_time -3h                           # Set time range
set_sensors plat == windows            # Set sensor selector
set_events NEW_PROCESS DNS_REQUEST     # Set event types (space-separated)
```

Then run queries:

**Paged mode (recommended):**
```bash
q event/DOMAIN_NAME contains 'google' | event/DOMAIN_NAME as domain COUNT_UNIQUE(routing/sid) as count GROUP BY(domain)
```
Use `n` command to fetch next page.

**Full query (all results):**
```bash
qa event/DOMAIN_NAME contains 'google' | event/DOMAIN_NAME as domain COUNT_UNIQUE(routing/sid) as count GROUP BY(domain)
```

**Dry run (cost estimation):**
```bash
dryrun event/COMMAND_LINE contains "powershell" and event/FILE_PATH not contains "powershell"
```

**Additional commands:**
- `set_limit_event <number>` - Limit events scanned
- `set_output <file>` - Mirror queries/results to file
- `set_format json|table` - Set output format
- `stats` - Show total query costs

### UI Usage

In the web console:
1. Select data source (Events, Detections, or Platform Audit)
2. Enter LCQL query in editor
3. Set time period:
   - Last [time period]: `-3h`, `-7d`
   - Around [timestamp] +- [duration]: `2025-01-16 08:52:54 +- 15 minutes`
   - Absolute: `From 10am to 1:30pm`
4. View query cost estimation
5. Run query and view results in Timeline or Table view

## Query Optimization

### Performance Tips

1. **Be specific with sensor selection**
   - Use `plat == windows` instead of no filter
   - Filter by tags, IPs, or hostnames when possible
   - More specific = faster and cheaper

2. **Limit event types**
   - Use specific event types instead of `*`
   - Example: `DNS_REQUEST` vs `*`

3. **Use narrow time windows**
   - `-1h` is cheaper than `-7d`
   - Only query the time range needed

4. **Filter early**
   - Put restrictive filters first
   - Filter before projection/aggregation

5. **Limit event scanning**
   - Use `set_limit_event` in CLI to cap scanned events

### Cost Management

**Queries are charged by events evaluated** (per million events)

- Cost estimation shown before running query
- "At most" cost for full time range
- Only retrieved data is billed
- Better targeting = lower cost

**Use `dryrun` to estimate costs before running expensive queries**

## Common Use Cases

### Threat Hunting

**Search for suspicious command lines:**
```
-24h | plat == windows | NEW_PROCESS | event/COMMAND_LINE contains "powershell" and event/COMMAND_LINE contains "bypass" | event/COMMAND_LINE as cli event/FILE_PATH as path routing/hostname as host
```

**Hunt for lateral movement (psexec):**
```
-12h | plat == windows | NEW_PROCESS | event/COMMAND_LINE contains "psexec" | event/FILE_PATH as path event/COMMAND_LINE as cli routing/hostname as host
```

### Investigation

**Find all activity from specific host:**
```
-24h | hostname == "WORKSTATION-01" | * | routing/hostname as host event/* as data
```

**Trace process ancestry:**
```
-6h | plat == windows | NEW_PROCESS | event/PARENT/FILE_PATH contains "cmd.exe" | event/PARENT/FILE_PATH as parent event/FILE_PATH as child COUNT_UNIQUE(event) as count GROUP BY(parent child)
```

### Baseline Analysis

**Count logon types:**
```
-7d | plat == windows | WEL | event/EVENT/System/EventID == "4624" | event/EVENT/EventData/LogonType AS LogonType COUNT(event) as Count GROUP BY(LogonType)
```

**Network connection frequency:**
```
-24h | plat == windows | NETWORK_CONNECTIONS | event/NETWORK_ACTIVITY/DESTINATION/IP_ADDRESS as ip COUNT(event) as count GROUP BY(ip)
```

## Data Structure Reference

LCQL can query three primary data streams in LimaCharlie, each with a different structure. Understanding these structures is essential for writing effective queries.

### Queryable Streams

LCQL can query three different data streams by selecting the appropriate source in the Query Console interface:

| Stream | Purpose | Structure Type |
|--------|---------|----------------|
| `event` | Real-time telemetry from sensors/adapters | Event structure |
| `detect` | D&R rule alerts and detections | Detection structure |
| `audit` | Platform management actions | Audit structure |

**Note:** The stream is selected via the Query Console UI (Events/Detections/Audit dropdown), not via LCQL syntax.

### Event Stream Structure

Events are telemetry from sensors and adapters. They have two top-level objects:

```json
{
  "routing": {
    "sid": "bb4b30af-...",
    "hostname": "workstation-01",
    "event_type": "NEW_PROCESS",
    "event_time": 1656959942437,
    "event_id": "8cec565d-...",
    "oid": "8cbe27f4-...",
    "plat": 268435456,
    "this": "a443f9c4...",
    "parent": "42217cb0..."
  },
  "event": {
    "FILE_PATH": "C:\\Windows\\System32\\cmd.exe",
    "COMMAND_LINE": "cmd.exe /c whoami",
    "PROCESS_ID": 4812
  }
}
```

**routing/** fields (consistent across all events):
- `routing/sid` - Sensor ID (UUID)
- `routing/hostname` - Hostname
- `routing/event_type` - Event type (NEW_PROCESS, DNS_REQUEST, etc.)
- `routing/event_time` - Unix timestamp in milliseconds
- `routing/oid` - Organization ID
- `routing/plat` - Platform (Windows=268435456, Linux, macOS)
- `routing/this` - Current process/object hash
- `routing/parent` - Parent process hash
- `routing/tags` - Sensor tags (array)

**event/** fields (varies by event_type):
- Process events: `event/FILE_PATH`, `event/COMMAND_LINE`, `event/PROCESS_ID`
- DNS events: `event/DOMAIN_NAME`, `event/IP_ADDRESS`
- Network events: `event/NETWORK_ACTIVITY/?/IP_ADDRESS`

**Query Example:**
```
-24h | * | NEW_PROCESS | event/COMMAND_LINE contains 'powershell'
```

### Detection Stream Structure

Detections are alerts created when D&R rules match. They inherit event routing and add detection metadata:

```json
{
  "cat": "Suspicious PowerShell",
  "source": "dr-general",
  "routing": { /* same as event routing */ },
  "detect": { /* copy of event data */ },
  "detect_id": "f1e2d3c4-...",
  "priority": 7,
  "detect_data": {
    "suspicious_file": "C:\\Windows\\System32\\powershell.exe",
    "encoded_command": "SGVsbG8="
  }
}
```

**Top-level detection fields:**
- `cat` - Detection name/category
- `source` - Rule source (dr-general, dr-managed, fp)
- `detect_id` - Unique detection ID
- `priority` - Priority 0-10 (higher = more critical)
- `detect_data` - Structured IOCs extracted by rule
- `source_rule` - Name of the rule that created this
- `rule_tags` - Tags from the rule

**routing/** fields - Same as event routing (sid, hostname, event_time, etc.)

**detect/** fields - Access the original event data:
- `detect/FILE_PATH` - File path from triggering event
- `detect/COMMAND_LINE` - Command line from event
- `detect/DOMAIN_NAME` - Domain from DNS event

**Query Examples:**

*Note: Select "Detections" in the Query Console UI source dropdown, then use these queries:*

Query high-priority detections from all sensors:
```
-7d | * | * | priority > 5
```

Query specific detection category with event data filter:
```
-24h | * | "Suspicious PowerShell" | detect/COMMAND_LINE contains '-enc'
```

Query extracted IOCs from detect_data across all detections:
```
-24h | * | * | detect_data/suspicious_file ends with '.exe'
```

### Audit Stream Structure

Audit logs track platform management actions. They have a flat structure:

```json
{
  "oid": "8cbe27f4-...",
  "ts": "2024-06-05T14:23:18Z",
  "etype": "config_change",
  "msg": "D&R rule created",
  "ident": "user@company.com",
  "entity": {
    "type": "dr_rule",
    "name": "detect-encoded-powershell"
  },
  "mtd": {
    "action": "create",
    "source_ip": "203.0.113.10"
  }
}
```

**Top-level audit fields:**
- `oid` - Organization ID
- `ts` - ISO 8601 timestamp string
- `etype` - Event type (config_change, api_call, user_action)
- `msg` - Human-readable message
- `ident` - Identity performing action (email, API key)
- `origin` - Origin of action (api, ui, cli)

**entity/** fields - Object affected:
- `entity/type` - Type of object (dr_rule, sensor, output)
- `entity/name` - Object name
- `entity/sid` - Sensor ID (for sensor actions)

**mtd/** fields - Action characteristics:
- `mtd/action` - Action type (create, update, delete)
- `mtd/source_ip` - Source IP address

**Query Examples:**

*Note: Select "Audit" in the Query Console UI source dropdown, then use these queries:*

Track configuration changes:
```
-7d | * | config_change
```

Find who modified D&R rules:
```
-30d | * | * | entity/type == 'dr_rule' and mtd/action == 'update'
```

Monitor specific user actions:
```
-7d | * | * | ident == 'admin@company.com'
```

### Cross-Stream Queries

LCQL can't JOIN across streams, but you can correlate data by querying each stream separately:

1. Query detections (select "Detections" source), note the sensor ID:
```
-24h | * | "Malware Detected" | | routing/sid
```

2. Query events from that sensor (select "Events" source):
```
-24h | sid == 'bb4b30af-...' | NEW_PROCESS
```

### Field Access Patterns

**Nested fields** use `/` separator:
- `event/PARENT/FILE_PATH` - Parent process path
- `detect_data/suspicious_file` - IOC from detection
- `entity/name` - Entity name in audit log

**Array access** uses `?` wildcard:
- `event/NETWORK_ACTIVITY/?/IP_ADDRESS` - Any IP in array
- `routing/tags/?` - Any tag value

**Windows Event Logs** have deep nesting:
- `event/EVENT/System/EventID` - Windows Event ID
- `event/EVENT/EventData/Data/?/@Name` - Event data field names

## Field Path Reference

### Common Event Fields

**Process Events:**
- `event/FILE_PATH` - Executable path
- `event/COMMAND_LINE` - Command line arguments
- `event/HASH` - File hash
- `event/PARENT/FILE_PATH` - Parent process path
- `event/PARENT/PROCESS_ID` - Parent PID
- `event/SIGNATURE/FILE_IS_SIGNED` - Code signing status

**DNS Events:**
- `event/DOMAIN_NAME` - Queried domain
- `event/DNS_TYPE` - Query type

**Network Events:**
- `event/NETWORK_ACTIVITY/SOURCE/IP_ADDRESS` - Source IP
- `event/NETWORK_ACTIVITY/DESTINATION/IP_ADDRESS` - Destination IP
- `event/NETWORK_ACTIVITY/DESTINATION/PORT` - Destination port

**Windows Event Log:**
- `event/EVENT/System/EventID` - Event ID
- `event/EVENT/EventData/*` - Event-specific data

### Routing Fields

- `routing/sid` - Sensor ID
- `routing/hostname` - Hostname
- `routing/event_time` - Event timestamp
- `routing/event_type` - Event type
- `routing/plat` - Platform

## Important Notes

1. **String quotes:** Use single quotes `'value'` or double quotes `"value"` for string values
2. **Regex syntax:** Use backticks for regex patterns: `` matches `^10\.3\..*` ``
3. **Case sensitivity:** Most operators are case-sensitive unless specified otherwise
4. **Wildcards:** Use `event/*` to match any field in an event
5. **Paging:** Aggregation queries (GROUP BY, COUNT) compute all results automatically
6. **Tab completion:** CLI supports tab completion for field names and event types

## When to Use LCQL

- Threat hunting across historical telemetry
- Investigating security incidents
- Building baselines and detecting anomalies
- Searching for specific indicators
- Analyzing patterns across sensors
- Validating detection rules before deployment

## Query Building Workflow

1. **Define scope:** What are you looking for?
2. **Set time range:** How far back to search?
3. **Select sensors:** Which systems are relevant?
4. **Choose events:** Which event types contain the data?
5. **Build filter:** What conditions must match?
6. **Add projection:** What fields do you need? Any aggregation?
7. **Test with dry run:** Check cost estimate
8. **Run query:** Execute and refine as needed

## Best Practices

1. Start with narrow time ranges and expand if needed
2. Use specific sensor selectors to reduce scope
3. Filter by event type before using wildcards
4. Test queries with `dryrun` to estimate costs
5. Use projections to extract only needed fields
6. Leverage aggregation for pattern analysis
7. Save frequently used queries for reuse
8. Document complex queries for team knowledge sharing

---

When helping users build queries:
- Ask clarifying questions about their investigation goals
- Suggest appropriate time ranges based on use case
- Recommend sensor selectors to narrow scope
- Provide examples similar to their needs
- Explain cost implications of broad queries
- Offer optimization suggestions for expensive queries
- Show both simple and aggregated query options
