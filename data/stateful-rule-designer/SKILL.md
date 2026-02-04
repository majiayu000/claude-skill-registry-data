---
name: stateful-rule-designer
description: Use this skill when users need to create complex stateful D&R rules that correlate multiple events over time, track parent-child relationships, or count event occurrences within timeframes.
---

# Stateful Rule Designer

You are an expert in designing complex stateful Detection & Response rules in LimaCharlie. Help users create rules that correlate multiple events over time, track process tree relationships, and detect sophisticated attack patterns that require temporal or relational context.

## What are Stateful Rules?

Stateful rules track and remember the state of past events to make decisions based on historical context. Unlike stateless rules that evaluate events in isolation, stateful rules can detect patterns over time and relationships between events.

### When to Use Stateful Rules

Use stateful rules when you need to:

1. **Track Parent-Child Relationships**: Detect when a specific process spawns a particular child process
2. **Monitor Process Trees**: Identify malicious behavior across multiple generations of processes
3. **Count Event Occurrences**: Alert when an event happens N times within a timeframe
4. **Correlate Related Events**: Connect events that share a common ancestor or timeframe
5. **Detect Multi-Stage Attacks**: Identify attack chains that unfold over time

### When to Use Stateless Rules

Stateless rules are simpler and more performant. Use them when:

- A single event contains all the information needed for detection
- No temporal or relational context is required
- The detection criteria can be evaluated in isolation

**Performance Principle**: Always prefer stateless rules unless you specifically need stateful correlation.

## Core Stateful Operators

LimaCharlie provides three stateful operators, each designed for different correlation scenarios.

### with_child: Matching Immediate Children

The `with child` operator matches events that are **direct children** of the initial event.

#### Basic Example

```yaml
detect:
  event: NEW_PROCESS
  op: ends with
  path: event/FILE_PATH
  value: cmd.exe
  case sensitive: false
  with child:
    op: ends with
    event: NEW_PROCESS
    path: event/FILE_PATH
    value: calc.exe
    case sensitive: false
respond:
  - action: report
    name: CMD Spawning Calculator
```

**Detects**: `cmd.exe --> calc.exe` (direct child)
**Does NOT detect**: `cmd.exe --> firefox.exe --> calc.exe` (grandchild)

#### With Counting

```yaml
detect:
  event: NEW_PROCESS
  op: ends with
  path: event/FILE_PATH
  value: outlook.exe
  case sensitive: false
  with child:
    op: ends with
    event: NEW_DOCUMENT
    path: event/FILE_PATH
    value: .ps1
    case sensitive: false
    count: 5      # At least 5 PowerShell files
    within: 60    # Within 60 seconds
respond:
  - action: report
    name: Outlook Dropping Multiple PowerShell Scripts
    priority: 4
```

### with_descendant: Matching Any Descendant

The `with descendant` operator matches events that are **descendants at any depth** (children, grandchildren, great-grandchildren, etc.).

#### Basic Example

```yaml
detect:
  event: NEW_PROCESS
  op: ends with
  path: event/FILE_PATH
  value: cmd.exe
  case sensitive: false
  with descendant:
    op: ends with
    event: NEW_PROCESS
    path: event/FILE_PATH
    value: calc.exe
    case sensitive: false
respond:
  - action: report
    name: CMD Process Tree Contains Calculator
```

**Detects**:
- `cmd.exe --> calc.exe` (direct child)
- `cmd.exe --> firefox.exe --> calc.exe` (grandchild)
- `cmd.exe --> firefox.exe --> notepad --> calc.exe` (great-grandchild)

#### Real-World Example: Office Exploit Chain

```yaml
detect:
  event: NEW_PROCESS
  op: or
  rules:
    - op: ends with
      path: event/FILE_PATH
      value: winword.exe
      case sensitive: false
    - op: ends with
      path: event/FILE_PATH
      value: excel.exe
      case sensitive: false
  with descendant:
    event: NEW_PROCESS
    op: and
    rules:
      - op: ends with
        path: event/FILE_PATH
        value: powershell.exe
        case sensitive: false
      - op: or
        rules:
          - op: contains
            path: event/COMMAND_LINE
            value: -enc
            case sensitive: false
          - op: contains
            path: event/COMMAND_LINE
            value: downloadstring
            case sensitive: false
respond:
  - action: report
    name: Office Application Process Tree Contains Encoded PowerShell
    priority: 5
  - action: isolate network
```

### with_events: Counting Proximal Events

The `with events` operator detects **repetition of events** close together in time on the same sensor. Ideal for threshold-based detections.

#### Basic Example: Failed Login Attempts

```yaml
detect:
  event: WEL
  op: is windows
  with events:
    event: WEL
    op: is
    path: event/EVENT/System/EventID
    value: '4625'  # Failed logon
    count: 5
    within: 60
respond:
  - action: report
    name: Multiple Failed Login Attempts
    priority: 3
```

#### Port Scanning Detection

```yaml
detect:
  event: NEW_TCP4_CONNECTION
  op: is platform
  name: windows
  with events:
    event: NEW_TCP4_CONNECTION
    op: and
    rules:
      - op: exists
        path: event/DESTINATION/PORT
      - op: is private address
        path: event/DESTINATION/IP_ADDRESS
        not: true  # External IPs only
    count: 50
    within: 30
respond:
  - action: report
    name: Potential Port Scanning Activity
    priority: 3
    metadata:
      mitre: T1046
```

## Event Selection: Choosing What to Report

By default, stateful rules report the **parent event** (the initial event that triggered the stateful matching). Use `report latest event: true` to report the child/descendant instead.

### Default Behavior

```yaml
detect:
  event: NEW_PROCESS
  op: ends with
  path: event/FILE_PATH
  value: outlook.exe
  case sensitive: false
  with child:
    op: ends with
    event: NEW_PROCESS
    path: event/FILE_PATH
    value: chrome.exe
    case sensitive: false
respond:
  - action: report
    name: Outlook Spawning Chrome
```

**Reported event**: The `outlook.exe` NEW_PROCESS event

### Report Latest Event

```yaml
detect:
  event: NEW_PROCESS
  op: ends with
  path: event/FILE_PATH
  value: outlook.exe
  case sensitive: false
  report latest event: true  # Report the child event
  with child:
    op: ends with
    event: NEW_PROCESS
    path: event/FILE_PATH
    value: chrome.exe
    case sensitive: false
respond:
  - action: report
    name: Outlook Spawning Chrome
```

**Reported event**: The `chrome.exe` NEW_PROCESS event

**Important**: Response actions (like `task`) always use the **latest event** in the chain, regardless of the `report latest event` setting.

## Flipping Between Stateful and Stateless

Within a stateful context, all operators are **stateful by default**, meaning sub-rules can match across different events. Use `is stateless: true` to require that multiple conditions match **the same event**.

### The Problem

```yaml
detect:
  event: NEW_PROCESS
  op: ends with
  path: event/FILE_PATH
  value: outlook.exe
  case sensitive: false
  with child:
    op: and
    rules:
      - op: ends with
        event: NEW_PROCESS
        path: event/FILE_PATH
        value: evil.exe
        case sensitive: false
      - op: contains
        path: event/COMMAND_LINE
        value: malicious-flag
        case sensitive: false
```

**Problem**: This could match two different child events.

### The Solution

```yaml
detect:
  event: NEW_PROCESS
  op: ends with
  path: event/FILE_PATH
  value: outlook.exe
  case sensitive: false
  with child:
    op: and
    is stateless: true  # Both conditions must match the same child event
    rules:
      - op: ends with
        event: NEW_PROCESS
        path: event/FILE_PATH
        value: evil.exe
        case sensitive: false
      - op: contains
        path: event/COMMAND_LINE
        value: malicious-flag
        case sensitive: false
respond:
  - action: report
    name: Outlook Spawning Evil.exe with Malicious Flag
```

**Now requires**: A **single** child event that is both `evil.exe` AND has `malicious-flag` in the command line.

## Common Detection Patterns

### Pattern 1: Office Document Spawning Shells

```yaml
detect:
  event: NEW_PROCESS
  op: or
  rules:
    - op: ends with
      path: event/FILE_PATH
      value: winword.exe
      case sensitive: false
    - op: ends with
      path: event/FILE_PATH
      value: excel.exe
      case sensitive: false
  with child:
    event: NEW_PROCESS
    op: or
    rules:
      - op: ends with
        path: event/FILE_PATH
        value: cmd.exe
        case sensitive: false
      - op: ends with
        path: event/FILE_PATH
        value: powershell.exe
        case sensitive: false
respond:
  - action: report
    name: Office Application Spawning Shell
    priority: 4
  - action: task
    command: deny_tree <<routing/this>>
```

### Pattern 2: Brute Force with User Context

```yaml
detect:
  event: WEL
  op: is windows
  with events:
    event: WEL
    op: and
    rules:
      - op: is
        path: event/EVENT/System/EventID
        value: '4625'
      - op: exists
        path: event/EVENT/EventData/TargetUserName
        truthy: true
    count: 10
    within: 300
respond:
  - action: report
    name: "Brute Force Attack - {{ .event.EVENT.EventData.TargetUserName }}"
    priority: 4
    metadata:
      mitre: T1110
    suppression:
      is_global: false
      keys:
        - '{{ .event.EVENT.EventData.TargetUserName }}'
        - '{{ .routing.sid }}'
      max_count: 1
      period: 1h
```

### Pattern 3: Suspicious Process Tree

```yaml
detect:
  event: NEW_PROCESS
  op: ends with
  path: event/FILE_PATH
  value: explorer.exe
  case sensitive: false
  with descendant:
    event: NETWORK_CONNECTIONS
    op: is public address
    path: event/NETWORK_ACTIVITY/SOURCE/IP_ADDRESS
    count: 10
    within: 300
respond:
  - action: report
    name: Explorer Process Tree Making Many External Connections
    priority: 3
```

## Performance Best Practices

Stateful rules consume more resources than stateless rules because they maintain state in memory.

### Key Guidelines

1. **Filter Early**: Put the most restrictive conditions in the parent event
2. **Use Specific Event Types**: Always specify the `event` type to avoid matching all events
3. **Limit Time Windows**: Keep `within` parameters as short as possible
4. **Use Platform Filters**: Filter by platform early to reduce the event set
5. **Avoid Deep Nesting**: Limit nesting to 2-3 levels maximum
6. **Use Suppression**: Always use suppression when triggering sensor commands

### Example: Good vs Bad Filtering

**Good**: Filters to specific process immediately
```yaml
detect:
  event: NEW_PROCESS
  op: ends with
  path: event/FILE_PATH
  value: outlook.exe  # Very specific
  case sensitive: false
  with child:
    event: NEW_PROCESS  # Specific event type
    op: ends with
    path: event/FILE_PATH
    value: calc.exe
```

**Bad**: Matches all processes
```yaml
detect:
  event: NEW_PROCESS
  op: exists
  path: event/FILE_PATH  # Matches everything!
  with child:
    # Missing event type - will check ALL child events!
    op: ends with
    path: event/FILE_PATH
    value: outlook.exe
```

## Key Reminders

1. Stateful rules are **forward-looking only** - state starts when the rule is active
2. Modifying a rule **resets all state** - parent processes must restart
3. Response actions always use the **latest event** in the chain
4. Use `is stateless: true` to require conditions match the **same event**
5. Always use **suppression** with sensor commands
6. **Test thoroughly** with unit tests before deploying
7. Keep time windows **short** to minimize memory usage
8. **Filter early** with specific parent event criteria

## Navigation & Additional Resources

- **[REFERENCE.md](REFERENCE.md)**: Complete operator syntax, all parameters, nested logic details
- **[EXAMPLES.md](EXAMPLES.md)**: 5+ complete attack detection scenarios (ransomware, credential dumping, lateral movement, etc.)
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**: Testing workflows, performance tuning, debugging tips

## Quick Reference

| Operator | Use Case | Example |
|----------|----------|---------|
| `with child` | Direct parent-child | Office app spawning CMD |
| `with descendant` | Any depth in tree | Office app spawning PowerShell (via intermediaries) |
| `with events` | Event repetition | Multiple failed logins, port scanning |
| `count` | Threshold detection | 5+ occurrences |
| `within` | Time window | Within 60 seconds |
| `report latest event` | Report child/descendant | Report the malicious child instead of parent |
| `is stateless` | Same-event matching | All conditions on single event |

---

This skill provides comprehensive guidance for creating sophisticated stateful detection rules. When helping users, always emphasize testing, performance considerations, and the importance of understanding the attack chain they're trying to detect. For complete details, examples, and troubleshooting, refer to the additional documentation files linked above.
