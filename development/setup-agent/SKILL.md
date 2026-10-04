---
name: setup-agent
description: Set up and connect a new Coval agent for evaluation. Guides through agent type selection, endpoint configuration, system prompt, and default resource attachment. Use when user says "set up an agent", "connect my agent", "create an agent", "add an agent", or "configure agent endpoint".
argument-hint: "[agent-name-or-url]"
---

# Agent Setup

Guide the user through connecting and configuring a new Coval agent for evaluation using the `coval` CLI. Follow the phases below in order, asking questions at each step.

If `$ARGUMENTS` contains an agent name or URL, use it to pre-fill the relevant field and skip that question.

## Phase 0: Preflight

### Step 1: Check authentication

```bash
coval whoami
```

If not authenticated, guide the user:
```bash
coval login
```
This prompts for an API key. Get one at https://app.coval.dev/settings (Organization > Manage > API Keys).

If the user doesn't have a Coval account, direct them to https://coval.dev to sign up.

### Step 2: Inventory existing agents

```bash
coval agents list --format json
```

**If agents exist**, present a numbered list:

```
Existing agents:

  1. My Voice Bot (voice) — +12345678901
  2. Support Chat (chat) — https://api.example.com/chat

  N. Create a new agent
```

Ask: "Would you like to configure an existing agent or create a new one?"

If the user picks an existing agent, skip to Phase 3 (System Prompt) to update it, or Phase 4 (Default Resources) if the prompt is already set.

**If no agents exist**, proceed to Phase 1.

## Phase 1: Agent Type Selection

Ask: "What type of AI agent do you have?"

Present the options:

- `voice` — Receives inbound phone calls (your agent picks up)
- `outbound-voice` — Your agent calls out (agent initiates the call)
- `chat` — Text/API endpoint (OpenAI-compatible format)
- `sms` — SMS-based agent
- `websocket` — WebSocket connection (ws:// or wss://)

Load `references/connection-types.md` for type-specific guidance on required fields, validation, and common pitfalls. Use this to inform the questions in Phase 2.

## Phase 2: Connection Configuration

Based on the selected type, collect the required connection details:

### For voice / sms agents:

Ask: "What is your agent's phone number? (E.164 format, e.g. +12345678901)"

Validate the input:
- Must start with `+`
- Must contain only digits after the `+`
- Must be 10-15 digits total (including country code)

### For chat / outbound-voice / websocket agents:

Ask: "What is your agent's endpoint URL?"

Validate the input:
- `chat` / `outbound-voice`: Must be a valid HTTP/HTTPS URL
- `websocket`: Must be a valid WebSocket URL (ws:// or wss://)

### Agent name:

Ask: "What would you like to name this agent?"

If `$ARGUMENTS` provided a name, confirm it: "I'll name this agent '<name>' — sound good?"

## Phase 3: System Prompt (Optional)

Ask: "Do you have your agent's system prompt? Pasting it helps generate better test cases and metrics later."

- If the user provides a prompt, store it as the `prompt` field.
- If the user skips, move on — this can be added later.

## Phase 4: Default Resources (Optional)

Inventory existing resources:

```bash
coval test-sets list --format json
coval metrics list --format json
```

If test sets or metrics exist, present them:

```
Available test sets:
  1. Customer Support Evaluation (3 cases)
  2. Edge Case Suite (5 cases)

Available metrics:
  1. Composite Evaluation
  2. Call Resolution
  3. Custom: Identity Verification
```

Ask: "Would you like to attach default test sets or metrics to this agent? These become the agent's default config for future runs."

If yes, collect the selected IDs and update the agent:

```bash
coval agents update <agent_id> --test-set-ids <id1>,<id2> --metric-ids <id1>,<id2>
```

If no resources exist, suggest creating them after setup:
- "You can create test sets with `/build-test-suite` and metrics with `/configure-metrics` after setup."

## Phase 5: Validation

### For endpoint-based agents (chat, outbound-voice, websocket):

Suggest testing connectivity: "Want me to verify your endpoint is reachable?"

If yes, attempt a basic connectivity check and report the result.

### For phone-based agents (voice, sms):

Confirm the E.164 format is correct and the number looks valid.

### Show agent summary before creation:

```
Agent Summary:
  Name:     <name>
  Type:     <type>
  <Phone/Endpoint>: <value>
  Prompt:   <first 80 chars or "Not set">
  Defaults: <test sets and metrics or "None">
```

Ask: "Create this agent? (yes / edit)"

Create the agent:

```bash
# For voice/sms:
coval agents create --name "<name>" --type <type> --phone-number "<number>" --format json

# For chat/outbound-voice/websocket:
coval agents create --name "<name>" --type <type> --endpoint "<url>" --format json
```

Capture `agent_id` from the JSON response.

If the user provided a system prompt, update the agent:

```bash
coval agents update <agent_id> --prompt "<prompt>"
```

If default resources were selected, attach them:

```bash
coval agents update <agent_id> --test-set-ids <ids> --metric-ids <ids>
```

Verify the created agent:

```bash
coval agents get <agent_id> --format json
```

## Phase 6: Summary + Next Steps

Present the created agent:

```
Agent created successfully!

  ID:       <agent_id>
  Name:     <name>
  Type:     <type>
  <Phone/Endpoint>: <value>

  View in dashboard: https://app.coval.dev/agents/<agent_id>
```

Suggest next steps based on what the user has set up:

- **Design a persona** for testing: `/design-persona`
- **Build test cases** for this agent: `/build-test-suite`
- **Configure metrics** to evaluate: `/configure-metrics`
- **Run a full onboarding** flow: `/onboard`
