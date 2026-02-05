---
name: dr-rule-builder
description: Use this skill when the user needs help creating, testing, validating, or troubleshooting Detection & Response (D&R) rules in LimaCharlie.
---

# LimaCharlie D&R Rule Builder

This skill helps you create, test, and validate Detection & Response (D&R) rules in LimaCharlie. Use this when users ask for help with rule creation, rule debugging, or understanding D&R rule syntax.

## What are D&R Rules?

Detection & Response (D&R) rules are serverless functions that run in the LimaCharlie cloud, applied in real-time to sensor data. They allow you to detect behaviors, automatically respond, create alerts, trigger remediation, and chain detections.

Rules are evaluated per-event. When a rule's detection component matches, the response component executes.

## Quick Start: Your First Rule

```yaml
detect:
  event: NEW_PROCESS
  op: ends with
  path: event/FILE_PATH
  value: calc.exe
  case sensitive: false
respond:
  - action: report
    name: Calculator Launched
```

**Key Components:**
- `detect`: What to look for
- `respond`: What to do when matched

## Rule Structure

```yaml
detect:
  event: EVENT_TYPE    # Event to monitor
  op: OPERATOR         # Matching logic
  # ... criteria
respond:
  - action: ACTION_TYPE
    # ... parameters
```

**Required:**
- `detect`: Must have `event` (or `target`) and `op`
- `respond`: Array of actions (minimum one)

## Core Operators

### Basic Comparison

**is** - Exact equality
```yaml
op: is
path: event/PROCESS_ID
value: 9999
```

**exists** - Element presence (optional `truthy: true` for non-null/non-empty)
```yaml
op: exists
path: event/PARENT
```

**contains** - Substring match (optional `count: N`)
```yaml
op: contains
path: event/COMMAND_LINE
value: powershell
```

**starts with / ends with** - Prefix/suffix match
```yaml
op: ends with
path: event/FILE_PATH
value: .exe
case sensitive: false
```

**matches** - Regular expression (Go syntax)
```yaml
op: matches
path: event/FILE_PATH
re: .*\\system32\\.*\.scr
case sensitive: false
```

**is greater than / is lower than** - Numeric comparison (optional `length of: true`)
```yaml
op: is greater than
path: event/NETWORK_ACTIVITY/BYTES_SENT
value: 1048576
```

### Boolean Logic

**and / or** - Combine rules
```yaml
op: and
rules:
  - op: ends with
    path: event/FILE_PATH
    value: /sshd
  - op: is public address
    path: event/NETWORK_ACTIVITY/SOURCE/IP_ADDRESS
```

**not** - Invert result (add `not: true` to any operator)
```yaml
op: is
not: true
path: event/PROCESS_ID
value: 9999
```

### Platform Checks

**is platform** - Platform detection
```yaml
op: is platform
name: windows  # windows, linux, macos, ios, android, chrome, etc.
```

**is windows / is 32 bit / is 64 bit / is arm** - Architecture shortcuts
```yaml
op: is windows
```

**is tagged** - Tag presence
```yaml
op: is tagged
tag: vip
```

### Network

**is public address / is private address** - RFC 1918 checks
```yaml
op: is public address
path: event/NETWORK_ACTIVITY/SOURCE/IP_ADDRESS
```

**cidr** - Network mask matching
```yaml
op: cidr
path: event/NETWORK_ACTIVITY/SOURCE/IP_ADDRESS
cidr: 10.16.1.0/24
```

### Advanced

**lookup** - Threat feed/resource lookup
```yaml
op: lookup
path: event/DOMAIN_NAME
resource: hive://lookup/malwaredomains
case sensitive: false
```

**scope** - Limit to sub-path (crucial for arrays)
```yaml
op: scope
path: event/NETWORK_ACTIVITY/
rule:
  op: and
  rules:
    - op: starts with
      path: event/SOURCE/IP_ADDRESS
      value: '10.'
    - op: is
      path: event/DESTINATION/PORT
      value: 445
```

**string distance** - Levenshtein distance for typosquatting
```yaml
op: string distance
path: event/DOMAIN_NAME
value: example.com
max: 2
```

For complete operator reference, see [REFERENCE.md](REFERENCE.md).

## Event Paths

**Event Data** (use `event/` prefix):
```yaml
path: event/FILE_PATH
path: event/COMMAND_LINE
path: event/PROCESS_ID
path: event/DOMAIN_NAME
```

**Routing Metadata** (use `routing/` prefix):
```yaml
path: routing/sid          # Sensor ID
path: routing/hostname     # Host name
path: routing/event_type   # Event type
path: routing/event_time   # Timestamp
```

**Array Navigation** (use `?` wildcard):
```yaml
path: event/NETWORK_ACTIVITY/?/IP_ADDRESS  # any element
path: event/NETWORK_ACTIVITY/0/IP_ADDRESS  # first element
```

## Response Actions

**report** - Create detection/alert
```yaml
- action: report
  name: my-detection-name
  priority: 3              # 1-5 severity
  metadata:                # optional context
    author: security-team
    mitre: T1059.001
  detect_data:             # optional structured extraction
    domain: "{{ .event.DOMAIN_NAME }}"
```

Template support: `"{{ .event.FILE_PATH }}"`
Internal only (D&R chaining): prefix name with `__`

**task** - Send sensor command
```yaml
- action: task
  command: history_dump
  investigation: inv-id
```

Common commands: `history_dump`, `deny_tree <<routing/this>>`, `segregate_network`, `yara_scan hive://yara/rule --pid "{{ .event.PROCESS_ID }}"`

**add tag / remove tag** - Tag management
```yaml
- action: add tag
  tag: vip
  ttl: 30  # optional expiration
```

**isolate network / rejoin network** - Network isolation (persists across reboots)
```yaml
- action: isolate network
```

For complete action reference, see [REFERENCE.md](REFERENCE.md).

## Stateful Rules

Track relationships between events over time.

**with child** - Direct children only
```yaml
event: NEW_PROCESS
op: ends with
path: event/FILE_PATH
value: cmd.exe
with child:
  op: ends with
  event: NEW_PROCESS
  path: event/FILE_PATH
  value: calc.exe
```
Detects: `cmd.exe -> calc.exe` (NOT `cmd.exe -> firefox.exe -> calc.exe`)

**with descendant** - Any descendant
```yaml
with descendant:
  # same syntax as with child
```
Detects: `cmd.exe -> calc.exe` AND `cmd.exe -> firefox.exe -> calc.exe`

**with events** - Event repetition
```yaml
event: WEL
op: is windows
with events:
  event: WEL
  op: is
  path: event/EVENT/System/EventID
  value: '4625'  # failed login
  count: 5       # occurrences
  within: 60     # seconds
```

**Counting**: Add `count` and `within` parameters to stateful rules
**Report Control**: Add `report latest event: true` to report child instead of parent
**Stateless Mode**: Add `is stateless: true` inside stateful context to require all conditions match same event

## Common Patterns

**Example Patterns:**

1. **Suspicious Location** - Detect execution from Downloads folder
2. **Threat Intelligence** - DNS lookup against malware domain feed
3. **Failed Logins** - Multiple failed logins (brute force detection)
4. **Office + PowerShell** - Office apps spawning encoded PowerShell
5. **Network Beaconing** - Repeated connections to same external IP

For 25+ complete rule examples with full code, see [EXAMPLES.md](EXAMPLES.md).

## Suppression

Control action execution frequency.

**Limit Frequency**
```yaml
- action: report
  name: my-detection
  suppression:
    max_count: 1      # execute max once
    period: 1h        # per hour
    is_global: true   # across org (false = per sensor)
    keys:
      - '{{ .event.FILE_PATH }}'
```

**Threshold Activation**
```yaml
suppression:
  min_count: 3   # must match 3 times
  max_count: 3   # then execute once
  period: 24h
```

**Practical: Prevent Duplicate Sensor Commands**
```yaml
- action: task
  command: yara_scan hive://yara/rule --pid "{{ .event.PROCESS_ID }}"
  suppression:
    is_global: false
    keys:
      - '{{ .event.PROCESS_ID }}'
    max_count: 1
    period: 1m
```

Time formats: `ns`, `us`, `ms`, `s`, `m`, `h`

## Testing Rules

```bash
# Validate syntax
limacharlie replay --validate --rule-content my-rule.yaml

# Test with events
limacharlie replay --rule-content my-rule.yaml --events test-event.json

# Test historical (single sensor)
limacharlie replay --sid SENSOR_ID --last-seconds 3600 --rule-content my-rule.yaml

# Test historical (org-wide)
limacharlie replay --entire-org --last-seconds 604800 --rule-content my-rule.yaml
```

Add unit tests in rule file under `tests:` section with `match:` and `non_match:` arrays.

For complete testing guide including trace mode and debugging, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## Best Practices

**Performance**
1. Filter by event type at top level
2. Put most restrictive conditions first
3. Use simple operators over regex when possible
4. Always suppress sensor commands

**False Positive Management**
1. Set `case sensitive: false` for paths/domains
2. Use `not: true` to exclude known good paths
3. Create FP rules for organization-specific exclusions

**Rule Organization**
1. Use descriptive, actionable detection names
2. Add metadata: MITRE ATT&CK, severity, author
3. Use `detect_data` to extract key fields

## Quick Reference

**Common Event Types**: `NEW_PROCESS`, `NETWORK_CONNECTIONS`, `DNS_REQUEST`, `FILE_TYPE_ACCESSED`, `CODE_IDENTITY`, `WEL`

**Operator Categories**:
- Comparison: `is`, `exists`, `contains`, `starts with`, `ends with`, `matches`
- Logic: `and`, `or`, `not`
- Numeric: `is greater than`, `is lower than`
- Network: `is public address`, `is private address`, `cidr`
- Platform: `is platform`, `is windows`, `is tagged`
- Stateful: `with child`, `with descendant`, `with events`

**Action Types**: `report`, `task`, `add tag`, `remove tag`, `isolate network`, `rejoin network`, `output`

**Template Variables**: `{{ .event.* }}`, `{{ .routing.* }}`, `{{ .detect.* }}` (in reports)

## CLI Commands

```bash
limacharlie dr list                                    # List rules
limacharlie dr add --rule-name NAME --rule-file FILE   # Add rule
limacharlie dr delete --rule-name NAME                 # Delete rule
limacharlie replay --validate --rule-content FILE      # Validate
limacharlie replay --rule-content FILE --events FILE   # Test
```

## Development Workflow

1. **Draft** - Write YAML rule
2. **Validate** - Check syntax
3. **Test** - Create test events
4. **Replay** - Test against historical data
5. **Deploy** - Add to test environment
6. **Monitor** - Watch for issues
7. **Iterate** - Refine based on feedback

## Navigation

- **[REFERENCE.md](REFERENCE.md)** - Complete operator/action reference, transforms, event paths, templates
- **[EXAMPLES.md](EXAMPLES.md)** - 25+ complete rule examples across all use cases
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Testing, debugging, performance tuning, validation

## Key Reminders

1. Always test rules before production deployment
2. Use suppression with sensor commands
3. Add unit tests to catch regressions
4. Include metadata for SOC context
5. Use case-insensitive matching for paths/domains
6. Put restrictive conditions first for performance
7. Use stateful rules for behavior-based detections
8. Create FP rules for organization exclusions
9. Monitor rule performance with replay metrics
10. Document rules with clear names and metadata

This skill provides comprehensive guidance for creating effective D&R rules. Always encourage testing and validation before production deployment.
