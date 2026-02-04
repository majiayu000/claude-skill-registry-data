---
name: forensics:investigate
description: Guided workflow for reverse engineering black-box systems. Use when a user wants to decode a defunct API, replicate a competitor's feature, understand unfamiliar code, or crack a data format.
---

# Forensics Investigation (Subagent-Driven)

This skill orchestrates multi-phase investigations using fresh subagents per phase. Main context stays clean; subagents do heavy lifting.

## Architecture

```
You (Opus) → Dispatch Haiku subagent → Subagent uses tools → Returns summary
           ← 2-3 sentence summary   ← Full data in Mem0
```

## Available Tools

Use these forensics MCP tools (directly for guidance, via subagent for data-heavy ops):
- `explain_concept` - Explain technical concepts (direct - already concise)
- `analyze_capture` - Parse HAR/curl captures (via subagent - returns lots of data)
- `suggest_next_step` - Get context-aware guidance (direct - already concise)
- `build_spec` - Generate API spec (via subagent - returns full spec)
- `start_investigation` - Create new investigation
- `get_investigation` - Get current/specific investigation
- `list_investigations` - List all investigations

## Phase 1: Check for Existing Investigation

First, check if there's a resumable investigation:

```
Call get_investigation tool (no params = gets active investigation)
```

**If investigation exists:** Ask user "Found investigation '[name]' in progress. Resume or start new?"

**If no investigation:** Proceed to Phase 2.

## Phase 2: Start New Investigation

Ask ONE question: "What are we investigating today?"

From their answer, determine the mode:
- **protocol**: API, network traffic, REST endpoints, authentication
- **feature**: Competitor feature, UI behavior, product capability
- **codebase**: Legacy code, unfamiliar repo, architecture
- **decision**: Why was this built this way? Git archaeology
- **format**: Binary format, data structure, file format

Confirm: "This sounds like a [mode] investigation. Starting '[name]'..."

```
Call start_investigation with:
- name: descriptive name from user's answer
- mode: detected mode
- target: what they're investigating
```

## Phase 3: Mode-Specific Workflow

**Subagent usage varies by mode:**
- **Protocol/Feature**: Use subagents for data-heavy operations
- **Codebase/Decision/Format**: Direct tool calls only (guidance-focused)

### Protocol Mode

**Step 1: Capture Guidance (DIRECT)**

If user hasn't captured traffic yet:
```
Call suggest_next_step with mode='protocol', hasCapture=false
```
Return the guidance directly (it's already concise).

Use `explain_concept` for tools like "mitmproxy" or "HAR file" if user asks.

**Step 2: Analyze Capture (SUBAGENT)**

When user provides HAR/curl output, dispatch a Haiku subagent:

```
Use Task tool:
- subagent_type: "general-purpose"
- model: "haiku"
- prompt: "You are a forensics investigation assistant. Analyze this network capture using the analyze_capture tool. Return ONLY a 2-3 sentence summary of findings. Full data is stored automatically.

Investigation context: [name]

Capture data:
[user's HAR/curl content]"
```

**Tell the user:** The subagent's summary + "Full details stored in investigation."

**Step 3: Build Spec (SUBAGENT)**

After analysis, dispatch another Haiku subagent:

```
Use Task tool:
- subagent_type: "general-purpose"
- model: "haiku"
- prompt: "Generate an OpenAPI spec for the current forensics investigation using the build_spec tool with format='openapi'. Return a 2-3 sentence summary of what was generated."
```

**Tell the user:** The subagent's summary + offer to show spec or continue.

**Step 4: Implementation Guidance (DIRECT)**

```
Call suggest_next_step with mode='protocol', hasCapture=true, hasSpec=true
```

This returns implementation suggestions tailored to user's tech stack (fetched from profile automatically).

### Feature Mode

**Step 1: Research Phase (SUBAGENT)**

Dispatch Haiku subagent to research the feature:

```
Use Task tool:
- subagent_type: "general-purpose"
- model: "haiku"
- prompt: "Research the feature '[feature name]'. Use perplexity-search if available to find:
  - How competitors implement similar features
  - Common patterns and libraries used
  - Key technical components

Return a 2-3 sentence summary of findings. Full research data is stored automatically.

Feature context: [name]

Description: [user's description of feature]"
```

**Tell the user:** The subagent's summary of competitive landscape + "Research stored in investigation."

**Step 2: Component Mapping (DIRECT)**

```
Call suggest_next_step with mode='feature', hasResearch=true
```

Guide user to map feature components to their codebase and tech stack.

**Step 3: Implementation Guidance (DIRECT)**

Continue using `suggest_next_step` to provide step-by-step implementation guidance tailored to their tech stack.

### Codebase / Decision / Format Modes

For these modes, use suggest_next_step directly (responses are already concise).
No subagent needed - these are guidance-heavy, not data-heavy.

## Phase 4: Progress & Resume

Investigation state is persisted. When user returns:

1. `get_investigation` retrieves full state
2. `suggest_next_step` knows where they left off
3. Continue from current phase

## Error Handling

If a subagent dispatch fails or returns an error:

1. **Don't panic** - Tell user "Analysis encountered an issue, let me try again"
2. **Retry once** - Dispatch a fresh subagent with the same task
3. **Fall back to direct** - If retry fails, call the tool directly and summarize manually
4. **Report partial progress** - "I was able to find X but couldn't complete Y"

If investigation state is corrupted:

1. Offer to start fresh: "Your investigation state seems corrupted. Start a new one?"
2. Use `start_investigation` to create a clean state

## Key Principles

1. **Subagents for data-heavy operations** - HAR parsing, spec generation
2. **Direct tools for guidance** - suggest_next_step already returns concise output
3. **Main context gets summaries** - "Found 12 endpoints with OAuth2 auth"
4. **Full data in Mem0** - Investigation state has everything
5. **Fresh subagent per phase** - No context pollution between phases

## Key Behaviors

- **One question at a time** - Don't overwhelm
- **Adapt to skill level** - Let the tools handle verbosity
- **Announce subagent dispatch** - "Analyzing your capture..." before dispatching
- **Summarize subagent results** - Don't dump raw output
- **Offer to pause** - "Your progress is saved. We can continue later."

## Example Flow

```
User: I want to reverse engineer the Spotify API

You: This sounds like a protocol investigation - we'll capture and analyze
network traffic to document the API. Starting 'Spotify API' investigation...
[Call start_investigation]

First, we need to capture some traffic.
[Call suggest_next_step mode=protocol hasCapture=false]
Here's how to set up mitmproxy and capture requests...

User: [Provides HAR file]

You: Analyzing your capture...
[Dispatch Haiku subagent with analyze_capture]
Found 47 endpoints using Bearer token auth. Key APIs: /v1/me, /v1/playlists,
/v1/tracks. Full details stored in investigation.

Ready to generate an API spec?

User: Yes

You: Building OpenAPI specification...
[Dispatch Haiku subagent with build_spec]
Generated OpenAPI 3.0 spec with 47 endpoints. Includes OAuth2 security scheme.
Saved to investigation.

Would you like to see the spec, or discuss implementation?

User: How do I implement this?

You: [Call suggest_next_step mode=protocol hasCapture=true hasSpec=true]
Based on your profile (Python, FastAPI), I'd suggest using httpx for the client
and Pydantic models generated from the OpenAPI spec...
```
