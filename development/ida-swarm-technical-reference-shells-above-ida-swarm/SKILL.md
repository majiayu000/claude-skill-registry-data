---
name: IDA Swarm Technical Reference
description: Technical reference for using IDA Swarm MCP tools. Covers system constraints, architecture, TRUE CONTEXT principle, result interpretation, and debugging. Use when analyzing binaries via IDA Swarm or troubleshooting sessions.
---

# IDA Swarm Technical Reference

## Critical Constraints

**ONE pending message per session**
- Cannot send second message while first is processing
- Error: "session is still processing previous message"
- Use `get_session_messages()` to poll or `wait_for_response()` to block

**Sessions are deterministic**
- session_id = "session_" + SHA256(binary_path)[:16]
- Same binary always gets same session_id
- Prevents duplicate sessions
- Must close existing session before creating new one for same binary

**Results are in response text**
- `start_analysis_session()` and `send_message()` return synthesized findings
- Orchestrator collects all agent work and returns coherent response

**extract_results.sh is DEBUG ONLY**
- Creates HUGE raw dump of all agent data
- Only use when debugging "why did orchestrator conclude X?"
- Not part of normal workflow
- Normal results come from response text

## TRUE CONTEXT Principle

### Why This Matters

Orchestrator **spawns specialized agents** based on task description. Task quality determines:
- What types of agents spawn (network analysis? crypto? vulnerability research?)
- How agents prioritize work
- Analysis depth
- Whether findings meet actual needs

### Deriving Effective Task Descriptions

**Reason through what orchestrator needs to understand:**

**1. What is the actual objective?**
- Not "analyze network code" → WHY: Extracting C2? Understanding protocol? Finding vulnerabilities?
- Objective determines agent specialization

**2. What form should results take?**
- Not "provide analysis" → Addresses with annotations? IOC list? Pseudocode? Detection signatures?
- Output format affects what agents extract

**3. What would make results unusable?**
- Missing function addresses? No proof? Incomplete spec?
- Understanding failure modes clarifies success criteria

### Cognitive Process

**Before sending task:**
- If agents only knew what I've written, could they derive what's actually needed?
- What decisions will agents make based on this description?
- Am I describing surface task ("find X") or underlying goal ("because I need Y")?

**Example reasoning:**

"Find network functions" → Agents don't know:
- WHY needed (IOC extraction vs protocol RE require different approaches)
- Platform specifics (WinSock vs POSIX)
- What constitutes completeness

**Derive:**
- WHY: C2 infrastructure for threat intel → Agents prioritize: IOCs, destinations, protocol patterns, evasion
- CONTEXT: Windows PE, APT, encrypted custom protocol → Agents look for: WinINet/WinSock, crypto on network data, DGA
- OUTPUT: IOC table, protocol structure, signatures → Agents extract: IPs/domains/ports, message format, detection patterns

**Result:** Agents spawn with APT C2 specialization, focus on actionable IOCs, extract detection-relevant patterns.

### Framework as Scaffold

**WHAT** - Technical task
**WHY** - Actual objective determining approach
**CONTEXT** - Information constraining/focusing analysis
**OUTPUT** - Form making results usable

Not rules. Questions to reason through what enables effective agent spawning.

**Orchestrator can't read your mind. It derives agent strategy from task description.**

## Architecture Essentials

**Communication flow:**
```
Claude Code → MCP Server → Orchestrator (IDA) → Agents (IDA instances)
```

**Two workspace locations:**

`/tmp/ida_swarm_sessions/{session_id}/`
- IPC files: request.json, response.json, sequence files
- ida.err - **check this for IDA errors**
- ida.out - IDA stdout

`/tmp/ida_swarm_workspace/{binary_name}/`
- agents/agent_N/ - agent databases, logs, memories
- orchestrator.log - **check for orchestrator errors**
- profiling/ - performance metrics (if enabled)
- extract_results.sh - debug tool (raw agent dump)

**File-based IPC**
- Orchestrator polls sequence files for changes
- Atomic writes via tmp+rename
- Response text contains orchestrator's synthesis

**Agent coordination**
- Agents work on isolated database copies
- IRC for conflict resolution when agents disagree
- Orchestrator merges findings after agents complete
- Response text contains merged result

## Tool Usage Patterns

**start_analysis_session**
- Spawns IDA
- Returns session_id and initial findings in response text
- `run_in_background=true` returns immediately (use for parallel analysis)

**send_message**
- Orchestrator maintains full context from previous messages
- Can reference previous findings naturally
- Returns synthesized response text
- `run_in_background=true` requires retrieving response later

**close_session**
- 60-second graceful shutdown (IDA database save)
- Cleans workspace directory
- Orphaned files (created by orchestrator) remain where they were written

**get_session_messages**
- Non-blocking poll for background mode
- Returns empty if still processing
- Clears message queue when retrieved

**wait_for_response**
- Blocking wait for background mode
- Returns when response available
- Use for parallel analysis coordination

## Background Mode (Parallel Analysis)

**When to use `run_in_background=true`:**
- Analyzing multiple binaries simultaneously
- Long analysis + other work needed

**Pattern:**
```
s1 = start_analysis_session(bin1, task1, run_in_background=true)
s2 = start_analysis_session(bin2, task2, run_in_background=true)
s3 = start_analysis_session(bin3, task3, run_in_background=true)

r1 = wait_for_response(s1)
r2 = wait_for_response(s2)
r3 = wait_for_response(s3)
```

## Orchestrator Capabilities

**File writing**
- Can create files (scripts, reports, configs)
- Default location: next to binary
- Can specify custom paths in request

**Binary patching**
- Agents can modify binaries via Keystone assembler
- Patches applied to both IDA database and actual binary file

**Multi-agent decomposition**
- Orchestrator spawns specialized agents based on task
- Quality of task description determines agent specialization
- Agents work in parallel, findings merged

## Common Issues

**"Session started but no response"**
- Check `/tmp/ida_swarm_sessions/{session_id}/ida.err`
- Verify IDA process: `ps aux | grep ida64`
- Check orchestrator log: `tail /tmp/ida_swarm_workspace/{binary}/orchestrator.log`

**"Cannot send message: still processing"**
- ONE pending message constraint
- Use `get_session_messages()` to check status
- Wait for response before next message

## Optimization

**Reuse sessions**
- Multiple follow-up questions in same session
- Much faster than closing and reopening

## Debugging Checklist

- [ ] IDA process running? `ps aux | grep ida64`
- [ ] IDA errors? `cat /tmp/ida_swarm_sessions/{session_id}/ida.err`
- [ ] Orchestrator errors? `grep -i error /tmp/ida_swarm_workspace/{binary}/orchestrator.log`
- [ ] Agent logs? `ls /tmp/ida_swarm_workspace/{binary}/agents/`
- [ ] Sequence files? `cat /tmp/ida_swarm_sessions/{session_id}/*_seq`

## Configuration

**MCP Server:** `~/.ida_swarm_mcp/server_config.json`
```json
{
    "max_sessions": 25,
    "ida_path": "/Applications/IDA Professional 9.0.app/Contents/MacOS/ida64"
}
```

**Orchestrator:** `~/.idapro/llm_re_config.json`
```json
{
    "api": {"auth_method": "api_key", "api_key": "sk-ant-..."},
    "profiling": {"enabled": true}
}
```

## Key Takeaways

1. **Sessions are deterministic** (same binary = same session_id)
2. **Results in response text**, not extract_results.sh (debug only)
3. **ONE pending message** per session at a time
4. **TRUE CONTEXT** determines agent spawning quality
5. **10+ minutes is normal**, not hung
6. **Two workspace directories** for debugging
7. **extract_results.sh = debug tool** for raw agent data
8. **60-second shutdown** is graceful IDA database save
