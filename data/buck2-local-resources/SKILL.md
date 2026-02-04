---
name: buck2-local-resources
description: Create Buck2 tests with local resources (processes, services, databases) using LocalResourceInfo and ExternalRunnerTestInfo. Use when tests need external dependencies like databases, HTTP servers, message queues, or Unix sockets that Buck2 should manage automatically. (project)
---

# Buck2 Local Resources Skill

## Overview

This skill guides you through creating Buck2 tests that depend on external processes or services. Buck2's local resources pattern manages broker processes automatically: starting them before tests, providing connection info via environment variables, and cleaning up afterward.

## When to Use This Skill

Use this skill when:
- Creating integration tests that need databases (PostgreSQL, Redis, SQLite)
- Testing HTTP/REST APIs (need HTTP server running)
- Testing message queues (Kafka, RabbitMQ, NATS)
- Testing Unix socket communication
- Testing service orchestration (multiple services interacting)
- Any test requiring external processes that Buck2 should manage

**Don't use for:**
- Simple unit tests (no external dependencies)
- Tests with in-memory alternatives (prefer in-memory DBs)
- Heavy services like Docker-in-Docker (too slow for Buck2 tests)

## Core Concepts

### The Three Components

Every local resources test has three parts:

1. **Broker Script**: Shell script that starts the service and outputs JSON
2. **Broker Rule**: Buck2 rule providing `LocalResourceInfo`
3. **Test Rule**: Buck2 rule using `ExternalRunnerTestInfo` to consume the resource

### How It Works

```
Test execution:
1. Buck2 identifies test needs broker (via local_resources)
2. Buck2 runs broker script → service starts, JSON output
3. Buck2 parses JSON, sets environment variables
4. Buck2 runs test script with those env vars
5. Test completes → Buck2 kills broker process (automatic cleanup)
```

## Step-by-Step Implementation Guide

### Step 1: Identify Resource Requirements

Before writing code, answer:

1. **What service?** (HTTP server, database, message queue, etc.)
2. **What connection info?** (port, URL, socket path, credentials?)
3. **How to start it?** (command to run, config needed?)
4. **How to detect readiness?** (health check, file exists, port open?)
5. **Single or multiple resources?** (one service or several?)

**Example answers:**
- Service: HTTP server
- Connection: Port number and URL
- Start: `python3 -m http.server <port>`
- Readiness: Port responds to HTTP request
- Resources: Single (just HTTP)

### Step 2: Create Broker Script

Template:

```bash
#!/usr/bin/env bash
# SPDX-FileCopyrightText: © 2024-2026 Austin Seipp
# SPDX-License-Identifier: Apache-2.0

set -euo pipefail

# 1. Setup: Create temp directory for isolation
TMPDIR=${TMPDIR:-/tmp}
WORKDIR="$TMPDIR/my-service-$$"  # $$ = process ID for uniqueness
mkdir -p "$WORKDIR"

# 2. Start service in background
<command-to-start-service> &
SERVICE_PID=$!

# 3. Wait for service to be ready (CRITICAL!)
for i in {1..50}; do
    if <readiness-check>; then
        break
    fi
    sleep 0.1
done

# 4. Output JSON (ONLY this to stdout, everything else to stderr!)
echo "{\"pid\": $SERVICE_PID, \"resources\": [{\"<key1>\": \"<value1>\", \"<key2>\": \"<value2>\"}]}"
```

**Important:**
- Service MUST run in background (`&`)
- MUST output JSON to stdout
- JSON MUST include `pid` (Buck2 tracks this to kill process)
- JSON MUST include `resources` array with connection details
- Resource keys will map to environment variables
- ALL other output must go to stderr (`>&2`) or `/dev/null`

**Examples:**

<details>
<summary>HTTP Server Broker</summary>

```bash
#!/usr/bin/env bash
set -euo pipefail

TMPDIR=${TMPDIR:-/tmp}
WORKDIR="$TMPDIR/http-$$"
mkdir -p "$WORKDIR"

# Create test content
echo "Hello" > "$WORKDIR/index.html"

# Start server
cd "$WORKDIR"
python3 -m http.server 8080 > /dev/null 2>&1 &
PID=$!

# Wait for ready
for i in {1..30}; do
    if curl -s http://localhost:8080 > /dev/null 2>&1; then
        break
    fi
    sleep 0.1
done

echo "{\"pid\": $PID, \"resources\": [{\"port\": \"8080\", \"url\": \"http://localhost:8080\"}]}"
```
</details>

<details>
<summary>Unix Socket Broker</summary>

```bash
#!/usr/bin/env bash
set -euo pipefail

TMPDIR=${TMPDIR:-/tmp}
SOCKET="$TMPDIR/my-socket-$$"

# Start socket server (using socat or custom server)
socat UNIX-LISTEN:$SOCKET,fork EXEC:'/bin/cat' &
PID=$!

# Wait for socket file to exist
for i in {1..50}; do
    if [[ -S "$SOCKET" ]]; then
        break
    fi
    sleep 0.1
done

echo "{\"pid\": $PID, \"resources\": [{\"socket_path\": \"$SOCKET\"}]}"
```
</details>

<details>
<summary>Database Broker (SQLite)</summary>

```bash
#!/usr/bin/env bash
set -euo pipefail

TMPDIR=${TMPDIR:-/tmp}
DB_PATH="$TMPDIR/test-db-$$.sqlite"

# Initialize database
sqlite3 "$DB_PATH" "CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT);"

# No background process needed for SQLite, but we still need a PID
# Use sleep as a dummy process to keep broker alive
sleep infinity &
PID=$!

echo "{\"pid\": $PID, \"resources\": [{\"db_path\": \"$DB_PATH\"}]}"
```
</details>

### Step 3: Create Broker Rule (in `defs.bzl`)

Template:

```starlark
# SPDX-FileCopyrightText: © 2024-2026 Austin Seipp
# SPDX-License-Identifier: Apache-2.0

_<service>_broker_rule = rule(
    impl = lambda ctx: [
        DefaultInfo(),
        RunInfo(args = cmd_args(ctx.attrs._script[DefaultInfo].default_outputs[0])),
        LocalResourceInfo(
            setup = cmd_args(ctx.attrs._script[DefaultInfo].default_outputs[0]),
            resource_env_vars = {
                "<ENV_VAR_NAME>": "<json_key>",  # Map JSON key → env var
                # Add more mappings as needed
            },
        ),
    ],
    attrs = {
        "_script": attrs.default_only(
            attrs.exec_dep(default = "<cell>//<package>:<broker-script-target>")
        ),
    },
)
```

**Key points:**
- `LocalResourceInfo` is the provider that marks this as a broker
- `setup`: The command to run (the broker script)
- `resource_env_vars`: Dict mapping env var names (keys) to JSON keys (values)
  - Example: `{"HTTP_URL": "url"}` means JSON's `resources[0].url` → test's `$HTTP_URL`
- `_script`: Reference to the broker script target (defined in BUILD file)

**Example:**

```starlark
_http_broker_rule = rule(
    impl = lambda ctx: [
        DefaultInfo(),
        RunInfo(args = cmd_args(ctx.attrs._script[DefaultInfo].default_outputs[0])),
        LocalResourceInfo(
            setup = cmd_args(ctx.attrs._script[DefaultInfo].default_outputs[0]),
            resource_env_vars = {
                "HTTP_PORT": "port",
                "HTTP_URL": "url",
            },
        ),
    ],
    attrs = {
        "_script": attrs.default_only(
            attrs.exec_dep(default = "depot//my/package:http-broker-script")
        ),
    },
)
```

### Step 4: Create Test Script

Your test script will receive environment variables from the broker:

```bash
#!/usr/bin/env bash
# SPDX-FileCopyrightText: © 2024-2026 Austin Seipp
# SPDX-License-Identifier: Apache-2.0

set -euo pipefail

# Environment variables are automatically set by Buck2
echo "Service available at: $<ENV_VAR>"

# Run your tests
<test-commands-here>

# Exit with appropriate code
if <tests-passed>; then
    echo "✓ Tests passed"
    exit 0
else
    echo "✗ Tests failed"
    exit 1
fi
```

**Example:**

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "Testing HTTP server at $HTTP_URL"

# Make request
RESPONSE=$(curl -s "$HTTP_URL/index.html")

if [[ "$RESPONSE" == "Hello" ]]; then
    echo "✓ Test passed"
    exit 0
else
    echo "✗ Test failed"
    exit 1
fi
```

### Step 5: Create Test Rule (in `defs.bzl`)

Template:

```starlark
_<service>_test_rule = rule(
    impl = lambda ctx: [
        DefaultInfo(),
        RunInfo(args = cmd_args([ctx.attrs.script[DefaultInfo].default_outputs[0]])),
        ExternalRunnerTestInfo(
            type = "custom",
            command = [cmd_args([ctx.attrs.script[DefaultInfo].default_outputs[0]])],
            local_resources = {
                '<resource-name>': ctx.attrs.<broker_attr>.label,
                # Add more resources if needed
            },
            required_local_resources = [
                RequiredTestLocalResource("<resource-name>", listing = False, execution = True),
                # Add more if needed
            ],
        ),
    ],
    attrs = {
        "script": attrs.source(),
        "<broker_attr>": attrs.exec_dep(providers = [LocalResourceInfo]),
        # Add more broker attrs for multiple resources
    },
)
```

**Key points:**
- `ExternalRunnerTestInfo` marks this as a test with external dependencies
- `type`: Usually `"custom"` for local resources
- `command`: The test script to run
- `local_resources`: Dict of resource name → broker target label
  - Names are arbitrary (for reference)
  - Must match names in `required_local_resources`
- `required_local_resources`: List of resources needed
  - `listing`: Usually `False` (not needed during `buck2 targets`)
  - `execution`: Usually `True` (needed during test execution)

**Example:**

```starlark
_http_test_rule = rule(
    impl = lambda ctx: [
        DefaultInfo(),
        RunInfo(args = cmd_args([ctx.attrs.script[DefaultInfo].default_outputs[0]])),
        ExternalRunnerTestInfo(
            type = "custom",
            command = [cmd_args([ctx.attrs.script[DefaultInfo].default_outputs[0]])],
            local_resources = {
                'http': ctx.attrs.http_broker.label,
            },
            required_local_resources = [
                RequiredTestLocalResource("http", listing = False, execution = True),
            ],
        ),
    ],
    attrs = {
        "script": attrs.source(),
        "http_broker": attrs.exec_dep(providers = [LocalResourceInfo]),
    },
)
```

### Step 6: Wire Everything in BUILD File

Template:

```starlark
# SPDX-FileCopyrightText: © 2024-2026 Austin Seipp
# SPDX-License-Identifier: Apache-2.0

load("@root//buck/shims:shims.bzl", depot = "shims")
load(":defs.bzl", "<exports-struct>")

# 1. Export broker script
depot.export_file(
    name = "<broker-script-name>",
    src = "<broker-script-file>",
)

# 2. Create broker target
<exports-struct>.<broker_rule>(
    name = "<broker-resource-name>",
)

# 3. Create test target
<exports-struct>.<test_rule>(
    name = "<test-name>",
    script = "<test-script-file>",
    <broker_attr> = ":<broker-resource-name>",
)
```

**Example:**

```starlark
# SPDX-FileCopyrightText: © 2024-2026 Austin Seipp
# SPDX-License-Identifier: Apache-2.0

load("@root//buck/shims:shims.bzl", depot = "shims")
load(":defs.bzl", "my_resources")

# Export broker script
depot.export_file(
    name = "http-broker",
    src = "http-broker.sh",
)

# Create broker target
my_resources.http_broker(
    name = "http-broker-resource",
)

# Create test target
my_resources.http_test(
    name = "http-test",
    script = "http-test.sh",
    http_broker = ":http-broker-resource",
)
```

**Don't forget to export rules in `defs.bzl`:**

```starlark
my_resources = struct(
    http_broker = _http_broker_rule,
    http_test = _http_test_rule,
)
```

### Step 7: Test and Debug

1. **Test broker script standalone:**
```bash
bash <broker-script>.sh
```

Should output valid JSON. Validate:
```bash
bash <broker-script>.sh | jq .
```

2. **Test manually:**
```bash
# Run broker
bash <broker-script>.sh
# Note the PID and resource values

# Set env vars manually
export <ENV_VAR>=<value-from-json>

# Run test
bash <test-script>.sh

# Kill broker
kill <pid-from-json>
```

3. **Run with Buck2:**
```bash
buck2 test //<package>:<test-name>
```

4. **Debug failures:**
- Check broker output: `buck2 test ... -v 2`
- Validate JSON: `bash broker.sh | jq .`
- Check env vars: Add `env | grep <PREFIX>` to test script
- Check processes: `ps aux | grep <service>`
- Clean up leaked processes: `pkill -f <service>`

## Multiple Resources Pattern

For tests needing multiple services:

### Broker Rules

Create separate broker rules for each service (as shown above).

### Test Rule

```starlark
_multi_test_rule = rule(
    impl = lambda ctx: [
        DefaultInfo(),
        RunInfo(args = cmd_args([ctx.attrs.script[DefaultInfo].default_outputs[0]])),
        ExternalRunnerTestInfo(
            type = "custom",
            command = [cmd_args([ctx.attrs.script[DefaultInfo].default_outputs[0]])],
            local_resources = {
                'http': ctx.attrs.http_broker.label,
                'db': ctx.attrs.db_broker.label,
                'redis': ctx.attrs.redis_broker.label,
            },
            required_local_resources = [
                RequiredTestLocalResource("http", listing = False, execution = True),
                RequiredTestLocalResource("db", listing = False, execution = True),
                RequiredTestLocalResource("redis", listing = False, execution = True),
            ],
        ),
    ],
    attrs = {
        "script": attrs.source(),
        "http_broker": attrs.exec_dep(providers = [LocalResourceInfo]),
        "db_broker": attrs.exec_dep(providers = [LocalResourceInfo]),
        "redis_broker": attrs.exec_dep(providers = [LocalResourceInfo]),
    },
)
```

### BUILD File

```starlark
my_resources.multi_test(
    name = "integration-test",
    script = "integration-test.sh",
    http_broker = ":http-broker-resource",
    db_broker = ":db-broker-resource",
    redis_broker = ":redis-broker-resource",
)
```

Test script will have access to all environment variables from all brokers.

## Common Patterns and Templates

### Dynamic Port Allocation

Avoid hardcoded ports by using port 0 (OS assigns random port):

```bash
# Start with port 0
python3 -m http.server 0 &
PID=$!

# Discover assigned port
sleep 0.2
PORT=$(lsof -ti -sTCP:LISTEN -a -p $PID)

echo "{\"pid\": $PID, \"resources\": [{\"port\": \"$PORT\"}]}"
```

### Unix Socket Pattern

Avoids port allocation entirely:

```bash
SOCKET="$TMPDIR/service-$$"
my_service --socket="$SOCKET" &
PID=$!

# Wait for socket file
for i in {1..50}; do
    if [[ -S "$SOCKET" ]]; then
        break
    fi
    sleep 0.1
done

echo "{\"pid\": $PID, \"resources\": [{\"socket_path\": \"$SOCKET\"}]}"
```

### Health Check Patterns

**Port-based:**
```bash
for i in {1..30}; do
    if curl -s http://localhost:$PORT/health > /dev/null 2>&1; then
        break
    fi
    sleep 0.1
done
```

**Socket-based:**
```bash
for i in {1..50}; do
    if [[ -S "$SOCKET" ]]; then
        break
    fi
    sleep 0.1
done
```

**Process-based:**
```bash
for i in {1..30}; do
    if kill -0 $PID 2>/dev/null; then
        break
    fi
    sleep 0.1
done
```

## Best Practices

1. **Isolation via $TMPDIR**
   - Use `$TMPDIR` for all temp files
   - Add `$$` (PID) to paths for uniqueness
   - Example: `$TMPDIR/my-service-$$`

2. **Always wait for readiness**
   - Don't output JSON until service is ready
   - Use health checks, file existence, port listening
   - Timeout after reasonable attempts

3. **Dynamic resource allocation**
   - Port 0 for random ports
   - Unix sockets with unique paths
   - Avoid hardcoded ports/paths

4. **Clean JSON output**
   - Only JSON to stdout
   - All logs to stderr or `/dev/null`
   - Validate with `jq .`

5. **Error handling**
   - `set -euo pipefail` in all bash scripts
   - Check service started successfully
   - Output error messages to stderr

6. **Testing**
   - Test broker standalone first
   - Test script manually with env vars
   - Run with Buck2 last

## Troubleshooting Guide

### "Invalid JSON from broker"

**Cause**: Broker outputs non-JSON or malformed JSON.

**Fix**:
```bash
bash broker.sh | jq .
```

Look for error messages. Ensure only JSON on stdout.

### "Environment variable not set"

**Cause**: Mismatch between JSON keys and `resource_env_vars`.

**Fix**: Check mapping:
- Broker: `{"resources": [{"my_key": "value"}]}`
- Rule: `resource_env_vars = {"MY_VAR": "my_key"}`
- Test: `$MY_VAR` should be `value`

### "Resource not available"

**Cause**: Name mismatch in `local_resources` and `required_local_resources`.

**Fix**:
```starlark
local_resources = {
    'myservice': ctx.attrs.broker.label,  # Name must match below
},
required_local_resources = [
    RequiredTestLocalResource("myservice", ...),  # Must match above
],
```

### "Process already running" or port conflicts

**Cause**: Previous test didn't clean up or hardcoded ports conflict.

**Fix**:
- Use dynamic ports (port 0)
- Use Unix sockets
- Add `$$` to temp directories
- Manually kill: `pkill -f my-service`

### Test hangs

**Cause**: Broker never becomes ready (infinite wait loop).

**Fix**: Add timeout to health check:
```bash
for i in {1..30}; do  # Max 3 seconds
    if <ready>; then
        break
    fi
    sleep 0.1
done

# Verify ready
if ! <ready>; then
    echo "Service failed to start" >&2
    kill $PID 2>/dev/null
    exit 1
fi
```

## Examples

See:
- `buck/tests/local-resources/` - Simple examples (HTTP, socket, multi-resource)
- `buck/third-party/qemu-static/` - Real-world example (QEMU with TPM)
- `docs/buck2.md` - Comprehensive documentation

## Quick Reference

### Broker Script Checklist

- [ ] SPDX headers
- [ ] `set -euo pipefail`
- [ ] Use `$TMPDIR/service-$$` for isolation
- [ ] Start service in background (`&`)
- [ ] Capture PID (`$!`)
- [ ] Wait for service ready (health check)
- [ ] Output ONLY JSON to stdout
- [ ] JSON includes `pid` and `resources` array
- [ ] Resource keys will become env var names

### Broker Rule Checklist

- [ ] SPDX headers
- [ ] Provides `LocalResourceInfo`
- [ ] `setup` points to broker script
- [ ] `resource_env_vars` maps JSON keys → env vars
- [ ] `_script` references broker script target

### Test Rule Checklist

- [ ] SPDX headers
- [ ] Provides `ExternalRunnerTestInfo`
- [ ] `type = "custom"`
- [ ] `local_resources` dict with broker labels
- [ ] `required_local_resources` list matches dict keys
- [ ] Attributes for script and broker(s)

### BUILD File Checklist

- [ ] SPDX headers
- [ ] Load defs.bzl and shims
- [ ] `export_file` for broker script
- [ ] Broker target using broker rule
- [ ] Test target using test rule
- [ ] Test script passed as `script =`
- [ ] Broker passed as `<broker_attr> = :<broker-target>`

## Command Reference

```bash
# Test broker script
bash <broker>.sh
bash <broker>.sh | jq .

# Test manually
bash <broker>.sh  # Note PID and resources
export VAR=value  # Set env vars from JSON
bash <test>.sh
kill <pid>

# Run with Buck2
buck2 test //<package>:<test>
buck2 test //<package>:<test> -v 2  # Verbose

# Debug
buck2 targets //<package>:  # List targets
buck2 build //<package>:<broker>  # Build broker
ps aux | grep <service>  # Find processes
pkill -f <service>  # Kill leaked processes
```

## Related Skills

- `buck2-test-workflow` - Testing workflows and best practices
- `buck2-build-troubleshoot` - Debugging Buck2 build failures
- `buck2-query-helper` - Querying Buck2 build graph

## Summary

Creating local resource tests:
1. Write broker script (outputs JSON with PID and connection info)
2. Create broker rule (`LocalResourceInfo` with `resource_env_vars`)
3. Create test rule (`ExternalRunnerTestInfo` with `local_resources`)
4. Wire in BUILD file (export script, create broker, create test)
5. Test standalone, then with Buck2

Key principles:
- Broker manages service lifecycle
- Buck2 handles cleanup
- Environment variables pass connection info
- Isolation via temp directories and dynamic allocation
- Hermetic and parallel-safe
