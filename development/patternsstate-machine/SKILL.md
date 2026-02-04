---
name: patterns/state-machine
description: State Machine Pattern pattern for C development
---

# State Machine Pattern

Model system behavior as discrete states with defined transitions. Current state determines which actions are valid and what state comes next.

## ikigai Application

**Input parser:** Tracks escape sequence state (normal, escape, CSI, etc.) to interpret terminal input bytes.

**Streaming response:** States like idle → requesting → streaming → complete → idle.

**Implementation:** Enum for states, switch or function pointer table for transitions:
```c
typedef enum { STATE_IDLE, STATE_STREAMING, STATE_ERROR } stream_state_t;
```

**REPL states:** Input mode, scrolling mode, command mode.

**Benefit:** Complex input handling becomes manageable. Each state handles its valid inputs.
