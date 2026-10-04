---
name: managing-grpc
description: |
  Use when working with Grpc — gRPC service management - service discovery via
  reflection, health checking, load balancing analysis, channelz diagnostics,
  and proto schema inspection. Use when debugging gRPC services, inspecting
  available methods, monitoring service health, or analyzing connection-level
  metrics.
connection_type: grpc
preload: false
---

# gRPC Management Skill

Manage and analyze gRPC services using reflection, health checks, channelz, and grpcurl.

## Core Helper Functions

```bash
#!/bin/bash

# gRPC target
GRPC_TARGET="${GRPC_TARGET:-localhost:50051}"
GRPC_PLAINTEXT="${GRPC_PLAINTEXT:---plaintext}"

# grpcurl wrapper
grpc_call() {
    grpcurl ${GRPC_PLAINTEXT} "$@" "$GRPC_TARGET" 2>&1
}

# List services via reflection
grpc_services() {
    grpc_call -list 2>/dev/null || echo "ERROR: Reflection not enabled or server unreachable"
}

# Describe a service or method
grpc_describe() {
    local symbol="$1"
    grpc_call -describe "$symbol" 2>/dev/null
}
```

## MANDATORY: Discovery-First Pattern

**Always discover available services and check health before performing operations.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Server Connectivity ==="
grpc_call -connect-timeout 5 grpc.health.v1.Health/Check 2>&1 | head -5
echo ""

echo "=== Available Services ==="
grpc_services

echo ""
echo "=== Service Details ==="
for svc in $(grpc_services | grep -v "^grpc\.\|^ERROR"); do
    echo "--- ${svc} ---"
    grpc_describe "$svc" | head -20
done

echo ""
echo "=== Health Status ==="
grpc_call grpc.health.v1.Health/Check 2>/dev/null \
    || echo "Health check service not available"
```

## Output Rules
- **TOKEN EFFICIENCY**: Target <=50 lines per output
- Summarize proto definitions; do not dump full message schemas
- Use grpcurl's JSON output format for structured data

## Common Operations

### Service Discovery and Inspection

```bash
#!/bin/bash

echo "=== All Services and Methods ==="
for svc in $(grpc_services | grep -v "^grpc\.\|^ERROR"); do
    echo "Service: ${svc}"
    grpc_describe "$svc" | grep "rpc " | sed 's/^/  /'
done

echo ""
echo "=== Message Types ==="
SERVICE="${1:-}"
if [ -n "$SERVICE" ]; then
    for method in $(grpc_describe "$SERVICE" | grep "rpc " | awk '{print $2}' | tr -d '('); do
        echo "--- ${method} ---"
        # Extract input/output types
        grpc_describe "${SERVICE}.${method}" 2>/dev/null | head -5
    done
fi

echo ""
echo "=== Proto File Reconstruction ==="
grpc_call -describe-all 2>/dev/null | head -50
```

### Health Checking

```bash
#!/bin/bash

echo "=== Overall Health ==="
grpc_call grpc.health.v1.Health/Check 2>/dev/null

echo ""
echo "=== Per-Service Health ==="
for svc in $(grpc_services | grep -v "^grpc\.\|^ERROR"); do
    status=$(grpc_call -d "{\"service\": \"${svc}\"}" grpc.health.v1.Health/Check 2>/dev/null | jq -r '.status // "UNKNOWN"')
    echo "${svc}: ${status}"
done

echo ""
echo "=== Health Watch (snapshot) ==="
timeout 3 grpcurl ${GRPC_PLAINTEXT} -d '{"service": ""}' "$GRPC_TARGET" grpc.health.v1.Health/Watch 2>/dev/null | head -10
```

### Load Balancing Analysis

```bash
#!/bin/bash

echo "=== DNS Resolution for Target ==="
HOST=$(echo "$GRPC_TARGET" | cut -d: -f1)
PORT=$(echo "$GRPC_TARGET" | cut -d: -f2)
echo "Target: ${HOST}:${PORT}"
dig +short "$HOST" 2>/dev/null || nslookup "$HOST" 2>/dev/null | grep "Address" | tail -n+2

echo ""
echo "=== Connection Test to Multiple Backends ==="
for ip in $(dig +short "$HOST" 2>/dev/null); do
    echo "--- ${ip}:${PORT} ---"
    grpcurl ${GRPC_PLAINTEXT} -connect-timeout 3 "${ip}:${PORT}" grpc.health.v1.Health/Check 2>/dev/null \
        && echo "  Status: REACHABLE" || echo "  Status: UNREACHABLE"
done

echo ""
echo "=== Load Balancing Config (if using xDS) ==="
echo "Check service mesh or load balancer configuration for gRPC-aware routing."
echo "Common LB policies: round_robin, pick_first, grpclb, xds"
```

### Channelz Diagnostics

```bash
#!/bin/bash

echo "=== Top Channels ==="
grpc_call grpc.channelz.v1.Channelz/GetTopChannels 2>/dev/null \
    | jq '{channels: [.channel[] | {
        ref: .ref.name,
        state: .data.state.state,
        target: .data.target,
        calls_started: .data.callsStarted,
        calls_succeeded: .data.callsSucceeded,
        calls_failed: .data.callsFailed,
        last_call: .data.lastCallStartedTimestamp
    }]}' 2>/dev/null || echo "Channelz not enabled on this server"

echo ""
echo "=== Servers ==="
grpc_call grpc.channelz.v1.Channelz/GetServers 2>/dev/null \
    | jq '{servers: [.server[] | {
        id: .ref.serverId,
        calls_started: .data.callsStarted,
        calls_succeeded: .data.callsSucceeded,
        calls_failed: .data.callsFailed,
        last_call: .data.lastCallStartedTimestamp
    }]}' 2>/dev/null || echo "Channelz not available"

echo ""
echo "=== Socket Details ==="
grpc_call grpc.channelz.v1.Channelz/GetTopChannels 2>/dev/null \
    | jq '[.channel[].subchannel[]?.ref.subchannelId // empty]' 2>/dev/null | head -10
```

### Method Invocation (Read-Only)

```bash
#!/bin/bash
SERVICE="${1:?Service name required}"
METHOD="${2:?Method name required}"

echo "=== Method Description ==="
grpc_describe "${SERVICE}/${METHOD}"

echo ""
echo "=== Input Message Schema ==="
input_type=$(grpc_describe "${SERVICE}/${METHOD}" | grep "input type" | awk '{print $NF}' | tr -d '.')
if [ -n "$input_type" ]; then
    grpc_describe "$input_type" 2>/dev/null
fi

echo ""
echo "=== Dry Run (empty request) ==="
echo "Command: grpcurl ${GRPC_PLAINTEXT} -d '{}' ${GRPC_TARGET} ${SERVICE}/${METHOD}"
echo "NOTE: Only execute after confirming the method is read-only (not a mutating RPC)"
```

## Safety Rules
- **Read-only by default**: Only use reflection, health checks, and channelz for inspection
- **Never invoke** mutating RPCs (Create, Update, Delete methods) without explicit user confirmation
- **Identify method semantics**: Check method names and descriptions before invocation; treat unknown methods as potentially mutating
- **Connection limits**: Avoid opening excessive connections; reuse grpcurl sessions where possible
- **TLS verification**: In production, never use `--plaintext`; always verify certificates

## Output Format

Present results as a structured report:
```
Managing Grpc Report
════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls
- **Reflection disabled**: Many production servers disable reflection for security; use proto files instead
- **Streaming RPCs**: Server-streaming and bidirectional RPCs require special handling with grpcurl (`-d @` for client streaming)
- **Deadline/timeout**: Always set deadlines; gRPC calls without deadlines can hang indefinitely
- **Status codes**: gRPC status codes differ from HTTP; UNAVAILABLE (14) means transient failure, NOT_FOUND (5) means the resource does not exist
- **Binary encoding**: gRPC uses protobuf binary format; raw packet inspection requires protobuf decoding tools
