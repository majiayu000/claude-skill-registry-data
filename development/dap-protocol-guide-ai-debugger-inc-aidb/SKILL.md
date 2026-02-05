---
name: dap-protocol-guide
description: Comprehensive guide for working with Debug Adapter Protocol in AIDB
version: 1.0.0
tags:
  - dap
  - protocol
  - debugging
  - requests
  - responses
---

# DAP Protocol Guide for AIDB

This skill provides comprehensive guidance for working with the Debug Adapter Protocol (DAP) in AIDB. Use this when implementing features that interact with debug adapters, analyzing DAP message flows, or troubleshooting protocol-level issues.

## Overview

The Debug Adapter Protocol (DAP) is a standardized protocol for communication between development tools and debug adapters. AIDB provides a fully-typed, authoritative implementation in `src/aidb/dap/protocol/`.

**For system-wide DAP architecture**, see `docs/developer-guide/overview.md` which includes:

- Complete data flow diagrams
- DAP client layer details
- Integration with adapters and session management

### Key Principles

1. **Always use existing protocol types** - Don't create dictionaries manually
1. **Follow established patterns** - Check adapter implementations before creating new request sequences
1. **Handle errors properly** - DAP has specific error response patterns
1. **Respect initialization sequence** - Initialize → Launch/Attach → ConfigurationDone
1. **Consider language differences** - Python, JavaScript, and Java adapters have different behaviors

## Authoritative Source

**`src/aidb/dap/protocol/` is THE authoritative reference for all DAP types and messages.**

This package contains:

- `types.py` - DAP data types (Breakpoint, StackFrame, Variable, etc.)
- `requests.py` - All request message classes
- `responses.py` - All response message classes
- `events.py` - All event message classes
- `bodies.py` - Request arguments and response bodies
- `base.py` - Base classes (Request, Response, Event, ProtocolMessage)

## Quick Reference

### Common DAP Operations

```python
# Import protocol types
from aidb.dap.protocol import (
    InitializeRequest,
    LaunchRequest,
    SetBreakpointsRequest,
    StackTraceRequest,
    ScopesRequest,
    VariablesRequest,
    ContinueRequest,
)
from aidb.dap.protocol.types import Source, SourceBreakpoint
from aidb.dap.protocol.bodies import (
    InitializeRequestArguments,
    LaunchRequestArguments,
    SetBreakpointsArguments,
    StackTraceArguments,
)

# Get next sequence number
seq = await client.get_next_seq()

# Build a request
request = SetBreakpointsRequest(
    seq=seq,
    arguments=SetBreakpointsArguments(
        source=Source(path="/path/to/file.py"),
        breakpoints=[
            SourceBreakpoint(line=10, condition="x > 5")
        ]
    )
)

# Send request and await response
response = await client.send_request(request)
```

### Client Constants

Always use constants from `src/aidb/dap/client/constants.py`:

```python
from aidb.dap.client.constants import (
    CommandType,
    EventType,
    StopReason,
)

# Check event type
if event.event == EventType.STOPPED.value:
    # Handle stopped event
    pass

# Check stop reason
if stopped_body.reason == StopReason.BREAKPOINT.value:
    # Handle breakpoint
    pass
```

## Protocol Flow Overview

### Standard Initialization Sequence

```
Client → Initialize Request
       ← Initialize Response (capabilities)
       ← Initialized Event
Client → SetBreakpoints (optional, multiple)
Client → SetExceptionBreakpoints (optional)
Client → ConfigurationDone Request
       ← ConfigurationDone Response
Client → Launch/Attach Request
       ← Launch/Attach Response
       [Debug session active]
```

### Introspection Flow

```
       ← Stopped Event
Client → Threads Request
       ← Threads Response
Client → StackTrace Request (threadId)
       ← StackTrace Response (stackFrames)
Client → Scopes Request (frameId)
       ← Scopes Response (scopes)
Client → Variables Request (variablesReference)
       ← Variables Response (variables)
```

### Execution Control

```
Client → Continue/Next/StepIn/StepOut Request
       ← Response (acknowledgement)
       ← Stopped Event (when execution stops again)
```

## Resource Files

This skill is organized into focused resource files, each under 500 lines:

### Core Protocol Operations

- **[initialization-sequence.md](resources/initialization-sequence.md)**

  - Initialize request/response
  - Attach vs Launch differences
  - Configuration done sequence
  - Language-specific initialization parameters

- **[breakpoint-operations.md](resources/breakpoint-operations.md)**

  - Setting source breakpoints
  - Conditional breakpoints
  - Hit conditions and log points
  - Breakpoint verification
  - Language-specific breakpoint quirks

- **[stack-inspection.md](resources/stack-inspection.md)**

  - Stack trace requests
  - Frame ID handling
  - Scope requests
  - Source references
  - Language-specific stack frame differences

- **[variable-evaluation.md](resources/variable-evaluation.md)**

  - Variables request
  - Variables reference tracking
  - Evaluate request
  - Expression contexts
  - Language-specific variable representations

### Patterns & Best Practices

## Language-Specific Differences

### Python (debugpy)

- Uses `launch` or `attach` request types
- `justMyCode` controls whether to step into library code
- Variable inspection is straightforward
- Stack frames include Python-specific metadata
- Supports `showReturnValue` option

### JavaScript/TypeScript (vscode-js-debug)

- Uses child sessions for subprocess debugging
- Source maps for TypeScript
- Async stack traces supported
- `console` option controls console API redirection
- Runtime executable can be node, npm, yarn, pnpm

### Java (java-debug-server)

- Requires classpath or module path configuration
- May use Eclipse JDT LS for code intelligence
- Main class specification required
- Can auto-compile .java files
- Supports JVM arguments (vmargs)

## Code Reuse Checklist

Before writing new DAP code, check these locations:

1. **Protocol Types**: `src/aidb/dap/protocol/types.py`

   - Breakpoint, StackFrame, Variable, Source, Thread, Scope, etc.

1. **Request/Response Classes**: `src/aidb/dap/protocol/requests.py`, `responses.py`

   - All request and response types fully typed

1. **Event Classes**: `src/aidb/dap/protocol/events.py`

   - StoppedEvent, ThreadEvent, BreakpointEvent, etc.

1. **Client Constants**: `src/aidb/dap/client/constants.py`

   - CommandType, EventType, StopReason enums

1. **Adapter Implementations**:

   - Python: `src/aidb/adapters/lang/python/python.py`
   - JavaScript: `src/aidb/adapters/lang/javascript/javascript.py`
   - Java: `src/aidb/adapters/lang/java/java.py`

1. **Session Management**: `src/aidb/session/`

   - connector.py - Connection sequences
   - session_breakpoints.py - Breakpoint management
   - child_manager.py - Child session patterns

## Common Pitfalls

### 1. Wrong Sequence Number

```python
# ❌ Bad: reusing or hardcoding seq
request = InitializeRequest(seq=1, arguments=args)

# ✅ Good: always get fresh seq
seq = await client.get_next_seq()
request = InitializeRequest(seq=seq, arguments=args)
```

### 2. Missing Required Fields

```python
# ❌ Bad: missing required fields
breakpoint = SourceBreakpoint(line=10)  # Error if other required fields

# ✅ Good: use protocol types correctly
from aidb.dap.protocol.types import SourceBreakpoint
breakpoint = SourceBreakpoint(line=10)  # All defaults handled
```

### 3. Ignoring Initialization Sequence

```python
# ❌ Bad: launching before configuration
await client.connect()
await client.send_request(LaunchRequest(...))  # Will fail

# ✅ Good: follow proper sequence
await client.connect()
await client.send_request(InitializeRequest(...))
# Wait for initialized event
await client.send_request(SetBreakpointsRequest(...))
await client.send_request(ConfigurationDoneRequest(...))
await client.send_request(LaunchRequest(...))
```

### 4. Not Handling Language Differences

```python
# ❌ Bad: assuming all adapters work the same
launch_config = {"program": "/path/to/file"}

# ✅ Good: use language-specific configuration
# Note: Launch arguments are implementation-specific dicts, not typed objects
# Adapters provide get_launch_configuration() that returns language-specific config

from aidb_common.constants import Language

if language == Language.PYTHON:
    # Python adapter provides debugpy-specific configuration
    launch_config = adapter.get_launch_configuration()
    # Typically includes: program, justMyCode, console, etc.
elif language == Language.JAVASCRIPT:
    # JavaScript adapter provides vscode-js-debug configuration
    launch_config = adapter.get_launch_configuration()
    # Typically includes: program, runtimeExecutable, console, etc.
elif language == Language.JAVA:
    # Java adapter provides java-debug-server configuration
    launch_config = adapter.get_launch_configuration()
    # Typically includes: mainClass, classpath, vmArgs, etc.
```

### 5. Creating Dictionaries Instead of Using Protocol Types

```python
# ❌ Bad: manual dictionary construction
source = {"path": "/path/to/file.py"}  # Type unsafe, error prone

# ✅ Good: use protocol types
from aidb.dap.protocol.types import Source
source = Source(path="/path/to/file.py")  # Type safe, IDE support
```

## When to Use This Skill

Invoke this skill ONLY when working directly with:

1. **DAP Protocol Types** - Creating/modifying protocol message classes in `src/aidb/dap/protocol/`
1. **DAP Client** - Implementing DAP client message handling in `src/aidb/dap/client/`
1. **Protocol Specification** - Understanding DAP spec, message flows, sequence numbers
1. **Protocol-Level Debugging** - Issues with DAP message encoding/decoding/parsing

**DO NOT use for:**

- Adapter implementation (use `adapter-development` skill instead)
- Breakpoint logic in adapters (use `adapter-development` skill)
- Session management (use `adapter-development` skill)
- General debugging questions (use `adapter-development` skill)

**Rule of thumb:** If you're working in `src/aidb/dap/protocol/` or `src/aidb/dap/client/`, use this skill. Otherwise, use `adapter-development`.

## Related Skills

When working with DAP protocol, you may also need:

- **adapter-development** - Adapters implement language-specific DAP patterns
- **mcp-tools-development** - MCP tools use DAP types for all debugging operations
- **testing-strategy** - Framework tests validate DAP flows end-to-end

## Related Documentation

**Internal Documentation**:

- **Architecture**: `docs/developer-guide/overview.md` - Overall system architecture with DAP layer details
- **Adapter Base**: `src/aidb/adapters/base/` - Base adapter classes
- **Session Management**: `src/aidb/session/` - Session lifecycle
- **Testing**: `src/tests/aidb/` - Example usage patterns

**External References**:

- **DAP Specification**: [Microsoft DAP Spec](https://microsoft.github.io/debug-adapter-protocol/specification) - Official protocol specification

## Verifying This Skill

To verify the code examples in this skill are current and accurate, check these files:

- **Protocol definitions**: `src/aidb/dap/protocol/` - Authoritative source for all types
- **Client implementation**: `src/aidb/dap/client/client.py` - Client methods and signatures
- **Real initialization flows**: `src/aidb/session/connector.py` - Production initialization sequences
- **Real breakpoint handling**: `src/aidb/session/session_breakpoints.py` - Production breakpoint patterns
- **Framework tests**: Working examples of complete flows:
  - Python: `src/tests/frameworks/python/pytest/e2e/test_pytest_debugging.py`
  - JavaScript: `src/tests/frameworks/javascript/jest/e2e/test_jest_debugging.py`
  - Java: `src/tests/frameworks/java/junit/e2e/test_junit_debugging.py`

## Example: Complete Debugging Flow

**Note**: This is a conceptual example showing the typical request sequence. For working examples, see the framework tests listed in "Verifying This Skill" above.

```python
from aidb.dap.protocol import (
    InitializeRequest,
    LaunchRequest,
    SetBreakpointsRequest,
    ConfigurationDoneRequest,
    ContinueRequest,
    StackTraceRequest,
    ScopesRequest,
    VariablesRequest,
)
from aidb.dap.protocol.types import Source, SourceBreakpoint
from aidb.dap.protocol.bodies import (
    InitializeRequestArguments,
    SetBreakpointsArguments,
    StackTraceArguments,
    ScopesArguments,
    VariablesArguments,
    ContinueArguments,
)

# 1. Initialize
seq = await client.get_next_seq()
init_response = await client.send_request(
    InitializeRequest(
        seq=seq,
        arguments=InitializeRequestArguments(
            clientID="aidb",
            adapterID="python",
            linesStartAt1=True,
            columnsStartAt1=True,
        )
    )
)

# 2. Wait for initialized event
await client.wait_for_event("initialized")

# 3. Set breakpoints
seq = await client.get_next_seq()
bp_response = await client.send_request(
    SetBreakpointsRequest(
        seq=seq,
        arguments=SetBreakpointsArguments(
            source=Source(path="/path/to/file.py"),
            breakpoints=[SourceBreakpoint(line=10)]
        )
    )
)

# 4. Configuration done
seq = await client.get_next_seq()
await client.send_request(ConfigurationDoneRequest(seq=seq))

# 5. Launch
seq = await client.get_next_seq()
launch_response = await client.send_request(
    LaunchRequest(seq=seq, arguments=launch_args)
)

# 6. Wait for stopped event
await client.wait_for_event(EventType.STOPPED.value)
thread_id = client.state.current_thread_id

# 7. Get stack trace
seq = await client.get_next_seq()
stack_response = await client.send_request(
    StackTraceRequest(
        seq=seq,
        arguments=StackTraceArguments(threadId=thread_id)
    )
)
frame_id = stack_response.body.stackFrames[0].id

# 8. Get scopes
seq = await client.get_next_seq()
scopes_response = await client.send_request(
    ScopesRequest(
        seq=seq,
        arguments=ScopesArguments(frameId=frame_id)
    )
)
vars_ref = scopes_response.body.scopes[0].variablesReference

# 9. Get variables
seq = await client.get_next_seq()
vars_response = await client.send_request(
    VariablesRequest(
        seq=seq,
        arguments=VariablesArguments(variablesReference=vars_ref)
    )
)

# 10. Continue execution
seq = await client.get_next_seq()
await client.send_request(
    ContinueRequest(
        seq=seq,
        arguments=ContinueArguments(threadId=thread_id)
    )
)
```

## Summary

This skill provides comprehensive DAP protocol guidance for AIDB development. Always:

1. Use protocol types from `src/aidb/dap/protocol/`
1. Check adapter implementations for patterns
1. Follow initialization sequences
1. Handle language-specific differences
1. Use constants from `client/constants.py`
1. Refer to resource files for detailed guidance

For deep dives into specific operations, see the resource files listed above.
