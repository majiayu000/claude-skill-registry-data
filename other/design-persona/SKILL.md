---
name: design-persona
description: Design and create a simulation persona for testing an AI agent. Guides through use case selection, voice and language configuration, behavior prompt crafting, and interruption calibration. Use when user says "create a persona", "design a persona", "set up a test persona", "configure simulation persona", or "build a caller profile".
argument-hint: "[use-case-or-agent-name]"
---

# Design Persona

Guide the user through designing and creating a simulation persona using the `coval` CLI. Follow the phases below in order, asking questions at each step.

If `$ARGUMENTS` contains a use case (e.g. "insurance_claims", "customer_support") or agent name, use it to skip or pre-fill relevant questions.

## Phase 0: Preflight + Inventory

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

### Step 2: Inventory existing resources

Run these in parallel:

```bash
coval personas list --format json
coval agents list --format json
```

**Decision matrix:**
- Has personas → present them as a numbered list: "You already have these personas. Want to reuse one, duplicate and modify, or create new?"
- No personas → proceed to Phase 1
- If `$ARGUMENTS` matches an existing agent name, pre-select that agent for Phase 1

## Phase 1: Agent Context

Ask: "Which agent will this persona test?"

- If agents exist, present them as a numbered list to pick from
- If no agents exist, say: "No agents found. You can still create a persona — just tell me what type of agent it will test (voice, outbound-voice, chat, sms, websocket)."

If the user selects an agent, fetch its details:

```bash
coval agents get <agent_id> --format json
```

Extract from the response:
- **Agent type** (`model_type`) — determines whether voice settings are relevant and conversation initiator direction
- **Agent name** — for context in prompts
- **Agent prompt** (if available) — helps craft a better persona

Key type mappings:
- `MODEL_TYPE_VOICE` / `MODEL_TYPE_OUTBOUND_VOICE` → voice settings matter, conversation initiator depends on direction
- `MODEL_TYPE_CHAT` / `MODEL_TYPE_WEBSOCKET` / `MODEL_TYPE_API` / `MODEL_TYPE_ENDPOINT` → voice settings are defaults only (won't affect simulation)

## Phase 2: Use Case Detection

Ask: "What does your agent do?"

Present the options:
- customer_support — Customer Support
- scheduling_booking — Scheduling & Booking
- sales — Sales
- insurance_claims — Insurance Claims
- healthcare_intake — Healthcare Intake
- restaurant_orders — Restaurant Orders
- debt_collection — Debt Collection
- it_helpdesk — IT Helpdesk
- other — Other (describe it)

Load `references/persona-templates.md` and select the template matching the chosen use case.

Present the template as a starting point:

```
Here's a starting persona for <use case>:

  Name:       <template name>
  Voice:      <voice>
  Language:   en-US
  Background: <background>
  Wait:       <wait seconds>s
  Prompt:     "<template description>"
```

Ask: "Use this as a starting point? (yes / customize name / start from scratch)"

## Phase 3: Voice + Language

Load `references/voice-options.md` for available options.

Ask these questions:

1. "What language should the persona speak?"
   - en-US — English (US)
   - es-ES — Spanish (Spain)
   - fr-FR — French (France)
   - de-DE — German
   - pt-BR — Portuguese (Brazil)
   - ja-JP — Japanese

2. "Voice preference?"
   - Female: aria (clear, professional)
   - Male: callum (clear, professional)

For non-voice agents (chat, websocket, API), explain: "Since your agent is text-based, voice and language are stored as defaults but won't affect the simulation."

## Phase 4: Environment + Behavior

### Background Sound

Present options with recommendations based on the use case:

| Value | Description | Recommended For |
|-------|-------------|-----------------|
| quiet | No background noise | Medical, legal, financial calls |
| office | Office ambient noise | Corporate, business, IT support |
| cafe | Restaurant/cafe noise | Casual, restaurant scenarios |
| airport | Airport/travel noise | Travel-related agents |

Say: "Based on your <use case> use case, I'd recommend **<recommended>**. Use that or pick another?"

### Wait Seconds

How long the persona waits before speaking after connection:

| Value | Style | Best For |
|-------|-------|----------|
| 0.3 | Fast responder | Restaurant orders, fast-paced interactions |
| 0.5 | Standard | Most inbound call scenarios |
| 1.0 | Slow / deliberate | Outbound calls, debt collection, elderly callers |

Say: "The template uses **<template wait>s**. Keep that or adjust?"

### Interruption Rate

How often the persona interrupts the agent mid-sentence:

| Rate | Behavior | Best For |
|------|----------|----------|
| NONE | Never interrupts | Compliance testing, scripted flows |
| LOW | Rare interruptions | Standard testing, polite callers |
| MEDIUM | Occasional interruptions | Realistic conversation simulation |
| HIGH | Frequent interruptions | Stress testing, impatient callers |

Explain: "NONE is best for validating scripted compliance flows. LOW is realistic for most callers. MEDIUM simulates natural conversation. HIGH stress-tests your agent's ability to handle interruptions."

Ask: "What interruption rate? (NONE / LOW / MEDIUM / HIGH)"

> **Note:** Interruption rate is not yet available as a CLI flag. To set it after creation, use the Coval API: `PATCH /v1/personas/{persona_id}` with `{"interruption_rate": "LOW"}`.

## Phase 5: Prompt Crafting

Start from the template's description as a base prompt.

Explain the key distinction: "The persona prompt defines WHO the caller is and HOW they behave — their personality, speaking style, and emotional state. It does NOT define what they ask about — that's handled by test cases."

Ask: "What specific behavior should this persona exhibit? For example:"
- "Speaks quickly and gets frustrated if put on hold"
- "Elderly caller who needs things repeated"
- "Non-native speaker who sometimes uses wrong words"
- "Aggressive caller who threatens to cancel"

Help the user refine the `simulated_user_prompt` by combining:
1. The template description as a foundation
2. The user's language choice applied to `{language}` placeholders
3. Any custom behavior the user describes

Present the final prompt for confirmation before proceeding.

## Phase 6: Create + Confirm

Present a full summary before creating:

```
Ready to create this persona:

  Name:              <name>
  Voice:             <voice>
  Language:          <language>
  Background:        <background>
  Wait Seconds:      <wait>
  Interruption Rate: <rate>
  Prompt:            "<final prompt>"
```

Ask: "Create this persona? (yes / edit)"

Create the persona:

```bash
coval personas create \
  --name "<name>" \
  --voice "<voice>" \
  --language "<language>" \
  --prompt "<final prompt>" \
  --background "<background>" \
  --wait-seconds <wait> \
  --format json
```

Capture `persona_id` from the JSON response.

Confirm success:

```
Persona created!

  ID:   <persona_id>
  Name: <name>

  View: https://app.coval.dev/personas/<persona_id>
```

## Phase 7: Next Steps

Suggest what the user can do next:

```
What's next?

  Build test cases for this persona:     /build-test-suite
  Configure evaluation metrics:          /configure-metrics
  Launch a quick evaluation:             /quick-eval

  Or manage this persona later:
  coval personas get <persona_id>
  coval personas update <persona_id> --prompt "new prompt"
```
