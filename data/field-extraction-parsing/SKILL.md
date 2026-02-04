---
name: field-extraction-parsing
description: Extract structured fields from unstructured log data using OPAL parsing functions. Covers extract_regex() for pattern matching with type casting, split() for delimited data, parse_json() for JSON logs, and JSONPath for navigating parsed structures. Use when you need to convert raw log text into queryable fields for analysis, filtering, or aggregation.
---

# Field Extraction and Parsing

## Overview

This skill covers converting unstructured log data into structured, queryable fields using OPAL's extraction and parsing functions.

**Core Functions**:
- `extract_regex()` - Extract fields using regex patterns with named capture groups
- `split()` / `split_part()` - Split delimited strings
- `parse_json()` - Parse JSON strings into objects
- JSONPath / Array access - Navigate parsed structures

## When to Use This Skill

Use field extraction when you need to:
- **Parse log formats** - Extract timestamp, level, message from structured logs
- **Extract identifiers** - Pull out request IDs, trace IDs, user IDs for correlation
- **Parse metrics from text** - Extract numbers, durations, status codes from logs
- **Structure unstructured data** - Convert free-form text into queryable columns
- **Parse embedded JSON** - Extract fields from JSON-formatted log messages

## Function 1: extract_regex()

The most powerful extraction function. Uses POSIX regex with named capture groups to create new columns.

### Syntax

```opal
extract_regex source_column, /(?P<field_name>pattern)/
extract_regex source_column, /(?P<field_name::typecast>pattern)/
```

**Key Features**:
- Named capture groups create new columns: `(?P<column_name>pattern)`
- Type casting in capture group: `(?P<name::int64>pattern)`
- Multiple captures in one regex
- Regex uses forward slashes `/pattern/` not quotes

### Supported Type Casts

- `string` (default)
- `int64`, `float64`
- `parse_isotime` (for ISO timestamps)
- `duration`, `duration_ms`, `duration_sec`, `duration_min`, `duration_hr`
- `parse_json`

### Pattern 1: Extract Timestamp and Log Level

**Use Case**: Parse structured application logs

**Log Format**: `[2025-11-16 01:58:12,204] INFO [Component] Message...`

```opal
filter container = "kafka"
extract_regex body, /\[(?P<log_time>[\d\-: ,]+)\] (?P<level>\w+) /
```

**Creates Columns**:
- `log_time`: "2025-11-16 02:02:45,266"
- `level`: "INFO"

**Use For**: Java logs, Kafka logs, structured application logs

---

### Pattern 2: Extract with Type Casting

**Use Case**: Extract numeric values as integers

**Log Format**: `[SnapshotEmitter id=1] Message...`

```opal
extract_regex body, /\[(?P<component>\w+) id=(?P<component_id::int64>\d+)\]/
```

**Creates Columns**:
- `component`: "SnapshotEmitter" (string)
- `component_id`: 1 (int64)

**Key Point**: `::int64` casts the extracted value to integer immediately

---

### Pattern 3: Extract HTTP Request Details

**Use Case**: Parse access log patterns

**Log Format**: `GET /api/users/123 200 15ms`

```opal
extract_regex body, /(?P<method>\w+) (?P<path>[\w\/\-\.]+) (?P<status::int64>\d{3}) (?P<duration_ms::int64>\d+)ms/
```

**Creates Columns**:
- `method`: "GET"
- `path`: "/api/users/123"
- `status`: 200 (int64)
- `duration_ms`: 15 (int64)

**Use For**: Nginx, Apache, application access logs

---

### Pattern 4: Extract Request ID for Correlation

**Use Case**: Pull out trace/request IDs for distributed tracing

**Log Format**: `request_id=GHhaU0_7TcVSXpICZ9lh [info] GET /api`

```opal
extract_regex body, /request_id=(?P<request_id>[\w\-]+)/
```

**Creates Columns**:
- `request_id`: "GHhaU0_7TcVSXpICZ9lh"

**Then correlate**:
```opal
extract_regex body, /request_id=(?P<request_id>[\w\-]+) \[info\] (?P<method>\w+) (?P<path>[\w\/]+)/
statsby count(), group_by(request_id, method, path)
```

**Use For**: Request correlation, distributed tracing, debugging user sessions

---

### Pattern 5: Extract Key=Value Pairs

**Use Case**: Parse structured key=value log formats

**Log Format**: `user=john action=login result=success duration=150ms`

```opal
extract_regex body, /user=(?P<user>\w+) action=(?P<action>\w+) result=(?P<result>\w+) duration=(?P<duration_ms::int64>\d+)ms/
```

**Creates Columns**:
- `user`: "john"
- `action`: "login"
- `result`: "success"
- `duration_ms`: 150 (int64)

**Use For**: Audit logs, security logs, custom application logs

---

### Pattern 6: Extract IP Addresses

**Use Case**: Parse network information from logs

**Log Format**: `Connection from IP=192.168.1.100 to Destination="10.0.0.5"`

```opal
extract_regex body, /IP=(?P<source_ip>[\d\.]+) to Destination="(?P<dest_ip>[\d\.]+)"/
```

**Creates Columns**:
- `source_ip`: "192.168.1.100"
- `dest_ip`: "10.0.0.5"

**Use For**: Network logs, firewall logs, connection tracking

---

## Function 2: split() and split_part()

Split delimited strings into arrays or extract specific parts.

### Syntax

```opal
split(string, delimiter)           # Returns JSON array
split_part(string, delimiter, N)   # Returns Nth part (1-based)
```

**Key Differences**:
- `split()` returns entire array: `["a", "b", "c"]`
- `split_part()` returns single element (1-based indexing)
- Negative indices in `split_part()` count from end: `-1` = last

### Pattern 7: Split IP Address into Octets

**Use Case**: Parse IP address components

```opal
extract_regex body, /IP=(?P<ip>[\d\.]+)/
make_col octets:split(ip, ".")
make_col first_octet:split_part(ip, ".", 1)
make_col last_octet:split_part(ip, ".", -1)
```

**Results**:
- `ip`: "95.217.183.1"
- `octets`: `["95", "217", "183", "1"]`
- `first_octet`: "95"
- `last_octet`: "1"

**Use For**: Network analysis, IP classification

---

### Pattern 8: Parse Path Components

**Use Case**: Extract parts of file paths or URLs

```opal
make_col path_parts:split("/var/log/app/error.log", "/")
make_col filename:split_part("/var/log/app/error.log", "/", -1)
make_col directory:split_part("/var/log/app/error.log", "/", -2)
```

**Results**:
- `path_parts`: `["", "var", "log", "app", "error.log"]`
- `filename`: "error.log"
- `directory`: "app"

**Use For**: File path analysis, URL parsing

---

### Pattern 9: Parse CSV-Like Data

**Use Case**: Extract fields from comma-separated values in logs

```opal
extract_regex body, /data:(?P<csv_data>[\w,]+)/
make_col fields:split(csv_data, ",")
make_col field1:split_part(csv_data, ",", 1)
make_col field2:split_part(csv_data, ",", 2)
make_col field3:split_part(csv_data, ",", 3)
```

**Use For**: Legacy systems, CSV exports in logs

---

## Function 3: parse_json()

Parse JSON strings into queryable objects.

### Syntax

```opal
parse_json(json_string)
```

**Returns**: OPAL object that can be accessed with JSONPath

### Pattern 10: Parse JSON from Logs

**Use Case**: Extract fields from JSON-formatted log messages

**Log Format**: `MetricsExporter {"kind": "exporter", "data_type": "metrics", "metrics": 23, "data points": 61}`

```opal
filter body ~ /MetricsExporter/
extract_regex body, /MetricsExporter.(?P<json_data>\{.*\})/
make_col parsed:parse_json(json_data)
```

**Result**:
- `json_data`: `{"kind": "exporter", "data_type": "metrics", ...}` (string)
- `parsed`: `{"kind": "exporter", "data_type": "metrics", ...}` (object)

**Next**: Access fields using JSONPath (see below)

---

## Function 4: JSONPath and Array Access

Navigate parsed JSON objects and arrays.

### Syntax

```opal
object.field_name              # Simple field
object."field with spaces"     # Quoted for special chars
array[0]                       # Zero-based array indexing
object.nested.field           # Nested access
```

**Critical**: Field names with spaces or special characters MUST be quoted

### Pattern 11: Access JSON Fields

**Use Case**: Extract specific fields from parsed JSON

```opal
extract_regex body, /MetricsExporter.(?P<json_data>\{.*\})/
make_col parsed:parse_json(json_data)
make_col data_type:string(parsed."data_type")
make_col metrics_count:int64(parsed.metrics)
make_col data_points:int64(parsed."data points")
```

**Results**:
- `data_type`: "metrics" (string)
- `metrics_count`: 23 (int64)
- `data_points`: 61 (int64)

**Key Points**:
- Use quotes for `"data_type"` and `"data points"` (special chars/spaces)
- Type cast with `int64()`, `string()`, etc.

---

### Pattern 12: Array Access with Split

**Use Case**: Access specific array elements

```opal
extract_regex body, /IP=(?P<ip>[\d\.]+)/
make_col parts:split(ip, ".")
make_col first_octet:int64(parts[0])
make_col second_octet:int64(parts[1])
make_col third_octet:int64(parts[2])
make_col fourth_octet:int64(parts[3])
```

**Key Point**: Array indexing is **zero-based** (`[0]` = first element)

**Difference from split_part()**:
- `split_part()`: 1-based (first element = 1)
- Array `[N]`: 0-based (first element = 0)

---

## Complete Examples

### Example 1: Parse Application Errors

**Goal**: Extract error codes and messages from application logs

```opal
filter body ~ /ERROR/
extract_regex body, /\[(?P<log_time>[\d\-: ,]+)\] (?P<level>\w+) \[(?P<component>\w+)\] (?P<error_code>\w+): (?P<message>.*)/
statsby error_count:count(), sample:any(message), group_by(error_code, component)
sort desc(error_count)
```

**Use Case**: Error analysis, identifying most common errors

---

### Example 2: Parse and Analyze HTTP Status Codes

**Goal**: Analyze HTTP response codes and response times

```opal
filter body ~ /\d{3} \d+ms/
extract_regex body, /(?P<method>\w+) (?P<path>[\w\/\-\.]+) (?P<status::int64>\d{3}) (?P<duration_ms::int64>\d+)ms/
make_col status_class:if(status >= 500, "5xx",
                       if(status >= 400, "4xx",
                       if(status >= 300, "3xx",
                       if(status >= 200, "2xx", "other"))))
statsby request_count:count(),
        avg_duration:avg(duration_ms),
        p95_duration:percentile(duration_ms, 0.95),
        group_by(status_class, path)
sort desc(request_count)
```

**Use Case**: Performance analysis, identifying slow endpoints

---

### Example 3: Correlate Requests Across Services

**Goal**: Track requests through multiple services using request_id

```opal
filter body ~ /request_id=/
extract_regex body, /request_id=(?P<request_id>[\w\-]+) \[info\] (?P<method>\w+) (?P<path>[\w\/]+)/
make_col service:string(resource_attributes."k8s.deployment.name")
statsby services:count_distinct(service),
        total_logs:count(),
        group_by(request_id)
filter services > 1
sort desc(services)
```

**Use Case**: Distributed tracing, identifying cross-service requests

---

### Example 4: Parse JSON Metrics and Alert

**Goal**: Extract metrics from JSON logs and find anomalies

```opal
filter body ~ /MetricsExporter/
extract_regex body, /MetricsExporter.(?P<json_data>\{.*\})/
make_col parsed:parse_json(json_data)
make_col data_points:int64(parsed."data points")
make_col metrics_count:int64(parsed.metrics)
filter data_points > 200 or metrics_count > 50
statsby high_count:count(), avg_points:avg(data_points), group_by(metrics_count)
```

**Use Case**: Monitoring metric collection, detecting unusual activity

---

### Example 5: Network Traffic Analysis

**Goal**: Analyze network connections by IP range

```opal
filter body ~ /IP=/
extract_regex body, /IP=(?P<ip>[\d\.]+)/
make_col octets:split(ip, ".")
make_col network:split_part(ip, ".", 1)
make_col is_private:if(network = "10" or network = "172" or network = "192", true, false)
statsby connection_count:count(), unique_ips:count_distinct(ip), group_by(is_private, network)
sort desc(connection_count)
```

**Use Case**: Security analysis, network traffic patterns

---

## Decision Tree: Which Function to Use?

```
Need to extract data from logs?
│
├─ Data has clear pattern (timestamp, IP, ID)
│  └─ Use extract_regex() with named captures
│
├─ Data is delimited (CSV, path, separated values)
│  ├─ Need all parts → Use split()
│  └─ Need specific part → Use split_part()
│
├─ Data is JSON formatted
│  ├─ Extract JSON first → extract_regex()
│  ├─ Parse JSON → parse_json()
│  └─ Access fields → JSONPath (object.field)
│
└─ Data is mixed (pattern + delimited + JSON)
   └─ Combine: extract_regex() → split() → parse_json()
```

---

## Common Mistakes and Solutions

### Mistake 1: Using Reserved Column Names

**ERROR**:
```opal
extract_regex body, /(?P<timestamp>[\d\-:]+)/
# Error: regex capture group 1 overwrites 'valid from' column "timestamp"
```

**FIX**:
```opal
extract_regex body, /(?P<log_time>[\d\-:]+)/
```

**Reserved names**: `timestamp`, `valid_from`, `valid_to`, `_c_bucket`

---

### Mistake 2: Forgetting Timestamp in pick_col

**ERROR**:
```opal
extract_regex body, /(?P<field>\w+)/
pick_col field
# Error: need to pick 'valid from' column "timestamp"
```

**FIX**:
```opal
extract_regex body, /(?P<field>\w+)/
pick_col timestamp, field
```

---

### Mistake 3: Wrong Regex Delimiters

**ERROR**:
```opal
extract_regex body, "pattern"     # Quotes don't work
```

**FIX**:
```opal
extract_regex body, /pattern/     # Forward slashes required
```

---

### Mistake 4: Tab Character in Regex

**ERROR**:
```opal
extract_regex body, /field\t(?P<value>.*)/
# Error: Unknown function 't()'
```

**FIX**:
```opal
extract_regex body, /field.(?P<value>.*)/        # Use . for any char
# OR
extract_regex body, /field[\t ](?P<value>.*)/    # Character class
```

---

### Mistake 5: JSONPath Without Quotes

**ERROR**:
```opal
string(parsed.data points)    # Syntax error (space in name)
```

**FIX**:
```opal
string(parsed."data points")  # Quote field names with spaces
```

---

### Mistake 6: Confusing split_part() vs Array Indexing

**Remember**:
- `split_part()` is **1-based** (first element = 1)
- Array `[N]` is **0-based** (first element = 0)

```opal
make_col parts:split("a.b.c", ".")
make_col using_split_part:split_part("a.b.c", ".", 1)  # "a" (1-based)
make_col using_array:parts[0]                          # "a" (0-based)
```

---

## Error Handling

### Regex Non-Matches

When regex doesn't match a log line:
- Extracted columns are **null** (not an error)
- Original data is preserved
- Filter nulls if needed: `filter extracted_field != null`

```opal
extract_regex body, /user=(?P<user>\w+)/
# Logs without "user=" will have user=null
filter user != null  # Keep only matched logs
```

---

### Invalid JSON

When `parse_json()` receives invalid JSON:
- Returns **null** (not an error)
- Check before accessing: `filter parsed != null`

```opal
make_col parsed:parse_json(maybe_json)
filter parsed != null
make_col field:string(parsed.field_name)
```

---

### Array Out of Bounds

When accessing `array[999]` on a smaller array:
- Returns **null** (not an error)
- No exception thrown

```opal
make_col parts:split("a.b.c", ".")  # ["a","b","c"]
make_col safe:parts[0]               # "a"
make_col oob:parts[999]              # null (no error)
```

---

## Performance Tips

### 1. Filter Before Extracting

Extract from relevant logs only:

```opal
# GOOD - Filter first
filter body ~ /ERROR/
extract_regex body, /ERROR: (?P<error_code>\w+)/

# BAD - Extract from all logs
extract_regex body, /ERROR: (?P<error_code>\w+)/
filter error_code != null
```

---

### 2. Single Regex with Multiple Captures

One regex is faster than multiple:

```opal
# GOOD - Single regex
extract_regex body, /\[(?P<time>[\d: ,]+)\] (?P<level>\w+) (?P<msg>.*)/

# BAD - Multiple regexes
extract_regex body, /\[(?P<time>.*)\]/
extract_regex body, /\] (?P<level>.*) /
extract_regex body, /(?P<msg>.*)/
```

---

### 3. Anchor Patterns When Possible

Anchored patterns (^, $) perform better:

```opal
# GOOD - Anchored
extract_regex body, /^(?P<timestamp>[\d\-:]+) /

# SLOWER - Unanchored (searches entire string)
extract_regex body, /(?P<timestamp>[\d\-:]+) /
```

---

### 4. Only Parse JSON When Needed

```opal
# GOOD - Filter, then parse
filter body ~ /\{.*"error"/
make_col parsed:parse_json(body)

# BAD - Parse everything
make_col parsed:parse_json(body)
filter parsed != null
```

---

## Related Skills

- **filtering-event-datasets** - Text search and filtering before extraction
- **aggregating-event-datasets** - Aggregating extracted fields with statsby
- **investigating-textual-data** - Error analysis workflows using extraction
- **analyzing-text-patterns** - Pattern discovery to identify what to extract

## Key Takeaways

1. **extract_regex()** is most powerful - supports type casting and multiple captures
2. **Forward slashes** required for regex: `/pattern/` not `"pattern"`
3. **Type cast in capture group**: `(?P<name::int64>pattern)` for immediate conversion
4. **split_part()** is 1-based, array `[N]` is 0-based
5. **Quote JSONPath fields** with spaces or special characters
6. **Reserved names**: Avoid `timestamp`, `valid_from`, `valid_to`
7. **Nulls not errors**: Non-matches return null, not exceptions
8. **Filter before extract**: Better performance

When in doubt about regex syntax or parsing functions, use `learn_observe_skill("OPAL extract_regex")` for official documentation.
