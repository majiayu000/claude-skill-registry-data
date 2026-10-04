---
name: migrate-bluejay
description: >
  Migrate configuration from Bluejay voice AI testing platform to Coval.
  Use when customer says "migrate from bluejay", "bluejay migration",
  "import bluejay config", or needs to transfer agents, simulations,
  metrics, and schedules from Bluejay to Coval.
disable-model-invocation: true
argument-hint: "[bluejay-api-key] [coval-api-key]"
---

# Bluejay → Coval Migration

Migrate all configuration from Bluejay to Coval for `$ARGUMENTS`.

## API References

- [references/bluejay-api.md](references/bluejay-api.md) — Bluejay endpoints, auth, pagination
- [references/coval-api.md](references/coval-api.md) — Coval endpoints, auth, request schemas
- [references/entity-mapping.md](references/entity-mapping.md) — Field-by-field mapping tables
- [references/metric-type-mapping.md](references/metric-type-mapping.md) — Bluejay response_type → Coval metric_type

## Step 0: Pre-flight

### Collect API Keys

Parse `$ARGUMENTS` for two positional args: `[bluejay-api-key] [coval-api-key]`.

If not provided, ask the user for each key individually.

### Validate Bluejay Key

```bash
curl -s -o /dev/null -w "%{http_code}" \
  -H "X-API-Key: <BLUEJAY_KEY>" \
  "https://api.getbluejay.ai/v1/all-agents"
```

Expect `200`. On `401`/`403`, tell user key is invalid.

### Validate Coval Key

```bash
curl -s -o /dev/null -w "%{http_code}" \
  -H "X-API-Key: <COVAL_KEY>" \
  "https://api.coval.dev/v1/agents?page_size=1"
```

Expect `200`. On `401`, tell user key is invalid.

### Fetch Coval Voice Catalog

```bash
curl -s -H "X-API-Key: <COVAL_KEY>" \
  "https://api.coval.dev/v1/personas/voices"
```

Store the voice list for persona mapping in Step 4. Response shape:
```json
{ "voices": [{ "voice_name": "aria", "supported_languages": ["en-US", ...] }] }
```

## Step 1: Inventory

Fetch all Bluejay entities. Use the endpoints in [references/bluejay-api.md](references/bluejay-api.md).

Fetch these in parallel where possible:

| Entity | Endpoint |
|--------|----------|
| Agents | `GET /v1/all-agents` |
| Simulations | `GET /v1/get-all-simulations` |
| Custom Metrics | `GET /v1/custom-metrics?page=1&page_size=100` (paginate) |
| Communities | `GET /v1/communities` |
| Schedules | Derive from simulations (no list-all endpoint — check each simulation) |
| Customer Personas | Fetch per agent: `GET /v1/customer-personas-by-agent/{agent_id}` |
| Folders | `GET /v1/all-folders` |

For each agent, also fetch:
- Latest prompt: `GET /v1/agents/{agent_id}/prompts/versions?page_size=1` (latest version)
- Latest knowledge base: `GET /v1/agents/{agent_id}/knowledge-bases/versions?page_size=1`
- Digital humans: Fetch per simulation: `GET /v1/digital-humans-by-simulation/{simulation_id}`

Present summary to user:

```
Found:
  - X agents
  - Y digital humans (across Z simulations)
  - N custom metrics
  - M communities
  - P customer personas
  - Q schedules
  - R folders

Proceed with migration?
```

Wait for user confirmation before continuing.

## Step 2: Check Existing Coval State

Fetch existing Coval entities to enable idempotency:

```bash
# Agents
curl -s -H "X-API-Key: <COVAL_KEY>" "https://api.coval.dev/v1/agents?page_size=100"

# Personas
curl -s -H "X-API-Key: <COVAL_KEY>" "https://api.coval.dev/v1/personas?page_size=100"

# Test Sets
curl -s -H "X-API-Key: <COVAL_KEY>" "https://api.coval.dev/v1/test-sets?page_size=100"

# Metrics
curl -s -H "X-API-Key: <COVAL_KEY>" "https://api.coval.dev/v1/metrics?page_size=100"

# Run Templates
curl -s -H "X-API-Key: <COVAL_KEY>" "https://api.coval.dev/v1/run-templates?page_size=100"

# Scheduled Runs
curl -s -H "X-API-Key: <COVAL_KEY>" "https://api.coval.dev/v1/scheduled-runs?page_size=100"
```

Paginate if `next_page_token` is present.

Build a lookup map of `display_name → ID` for each entity type. When checking for duplicates:
- If entity exists with `bluejay_migration: true` in metadata → **skip** (already migrated)
- If name collision with non-migrated entity → **ask user** whether to skip or rename

## Phase 1: Independent Entities (Steps 3–5)

These have no cross-references. Execute in order but each step is independent.

### Step 3: Migrate Metrics

Map Bluejay Custom Metrics → Coval Metrics.

For each Bluejay metric, use the mapping in [references/metric-type-mapping.md](references/metric-type-mapping.md).

**For each metric:**

1. Determine `metric_type` from Bluejay `response_type`
2. Build `prompt` from Bluejay `scoring_guidance` + `description`
3. For `qualitative` → ask user for category list
4. For `quantitative` → use Bluejay `min_value`/`max_value` if present, else ask
5. For `enum` → use `enum_options` as `categories`
6. If `eval_route == "AUDIO"` → use `METRIC_AUDIO_LLM_*` variants
7. For `json` → use `METRIC_LLM_BINARY`, warn user this is an approximation

```bash
curl -s -X POST "https://api.coval.dev/v1/metrics" \
  -H "X-API-Key: <COVAL_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "metric_name": "<bluejay_metric_name>",
    "description": "<bluejay_description>",
    "metric_type": "<mapped_type>",
    "prompt": "<from_scoring_guidance>",
    "metadata": {
      "bluejay_migration": true,
      "bluejay_original_id": "<bluejay_metric_id>"
    }
  }'
```

Add type-specific fields (`categories`, `min_value`, `max_value`) per the mapping table.

Record: `bluejay_metric_id → coval_metric_id`

### Step 4: Migrate Personas

Map Bluejay Digital Humans (voice/behavior) AND Customer Personas → Coval Personas.

#### Digital Human → Persona

For each unique digital human:

1. **Voice mapping** — Present the Bluejay voice config to the user:
   ```
   Bluejay Digital Human: "<name>"
     Gender: <gender>
     Accent: <accent>
     Language: <language>

   Available Coval voices: aria, asteria, athena, luna, ...

   Which Coval voice should map to this configuration?
   ```
   Cache voice mappings — if same gender+accent+language combo appears again, reuse the mapping without asking.

2. Map `language` → `language_code` (e.g., `en` → `en-US`, `es` → `es-ES`)
3. Map `background_noise` → `background_sound` (see entity mapping reference)
4. Build `persona_prompt` from `role_description` + `traits` + behavioral fields

```bash
curl -s -X POST "https://api.coval.dev/v1/personas" \
  -H "X-API-Key: <COVAL_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "<digital_human_name>",
    "voice_name": "<mapped_coval_voice>",
    "language_code": "<mapped_language_code>",
    "persona_prompt": "<built_from_role_description_and_traits>",
    "background_sound": "<mapped_background_noise>",
    "conversation_initiation": "<from_speaks_first_config>",
    "metadata": {
      "bluejay_migration": true,
      "bluejay_original_id": "<digital_human_id>"
    }
  }'
```

Record: `bluejay_digital_human_id → coval_persona_id`

#### Customer Persona → Persona

For each Bluejay Customer Persona:

```bash
curl -s -X POST "https://api.coval.dev/v1/personas" \
  -H "X-API-Key: <COVAL_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "<customer_persona_name>",
    "voice_name": "aria",
    "language_code": "en-US",
    "persona_prompt": "Name: <name>\nDescription: <description>\nGoal: <goal>",
    "metadata": {
      "bluejay_migration": true,
      "bluejay_original_id": "<customer_persona_id>",
      "bluejay_entity_type": "customer_persona"
    }
  }'
```

Ask user which voice to use for customer personas (default to `aria`).

### Step 5: Migrate Agents

Map Bluejay Agents → Coval Agents.

For each Bluejay agent:

1. Determine `model_type`: Bluejay `mode=VOICE` → `MODEL_TYPE_VOICE`, `mode=TEXT` → `MODEL_TYPE_TEXT`
2. Build `prompt` from: latest Prompt version `prompt_text` + agent `goals` (append as numbered list)
3. If agent has a `system_prompt`, prepend it to the prompt
4. Store `knowledge_base` content in agent metadata
5. If agent has a `folder`, prefix `display_name` with folder name: `"[FolderName] AgentName"`

```bash
curl -s -X POST "https://api.coval.dev/v1/agents" \
  -H "X-API-Key: <COVAL_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "<folder_prefix><agent_name>",
    "model_type": "<MODEL_TYPE_VOICE|MODEL_TYPE_TEXT>",
    "prompt": "<system_prompt + latest_prompt + goals>",
    "metadata": {
      "bluejay_migration": true,
      "bluejay_original_id": "<bluejay_agent_id>",
      "knowledge_base": "<kb_text_content>",
      "bluejay_connection_type": "<connection_type>",
      "bluejay_phone_number": "<phone_number>"
    }
  }'
```

Record: `bluejay_agent_id → coval_agent_id`

## Phase 2: Dependent on Phase 1 (Steps 6–7)

### Step 6: Migrate Test Sets

Map Bluejay Simulations + Communities → Coval Test Sets.

#### Simulation → Test Set

For each Bluejay simulation:

```bash
curl -s -X POST "https://api.coval.dev/v1/test-sets" \
  -H "X-API-Key: <COVAL_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "<simulation_name>",
    "description": "Migrated from Bluejay simulation <simulation_id>",
    "test_set_type": "SCENARIO",
    "test_set_metadata": {
      "bluejay_migration": true,
      "bluejay_original_id": "<simulation_id>",
      "bluejay_entity_type": "simulation"
    }
  }'
```

Record: `bluejay_simulation_id → coval_test_set_id`

#### Community → Test Set

For each Bluejay community:

```bash
curl -s -X POST "https://api.coval.dev/v1/test-sets" \
  -H "X-API-Key: <COVAL_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "<community_title>",
    "description": "<community_description>",
    "test_set_type": "SCENARIO",
    "test_set_metadata": {
      "bluejay_migration": true,
      "bluejay_original_id": "<community_id>",
      "bluejay_entity_type": "community"
    }
  }'
```

Record: `bluejay_community_id → coval_test_set_id`

### Step 7: Migrate Test Cases

Map Bluejay Digital Human intents → Coval Test Cases.

For each digital human associated with a simulation:

1. Use `intent` → `input_str`
2. Use `success_criteria` → `expected_behaviors` (split into array if multi-line)
3. Look up `coval_test_set_id` from the simulation mapping (Step 6)
4. If `scripted_responses` present → set `input_type: "SCRIPT"` with `simulation_metadata_input.script_turns`

```bash
curl -s -X POST "https://api.coval.dev/v1/test-cases" \
  -H "X-API-Key: <COVAL_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "test_set_id": "<coval_test_set_id>",
    "input_str": "<digital_human_intent>",
    "expected_behaviors": ["<success_criteria_line_1>", "<success_criteria_line_2>"],
    "description": "<digital_human_name>: <digital_human_tag>",
    "input_type": "SCENARIO",
    "metadata": {
      "bluejay_migration": true,
      "bluejay_original_id": "<digital_human_id>"
    }
  }'
```

For scripted test cases:

```bash
curl -s -X POST "https://api.coval.dev/v1/test-cases" \
  -H "X-API-Key: <COVAL_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "test_set_id": "<coval_test_set_id>",
    "input_str": "<digital_human_intent>",
    "expected_behaviors": ["<success_criteria>"],
    "input_type": "SCRIPT",
    "simulation_metadata_input": {
      "script_turns": ["<turn_1>", "<turn_2>", "..."]
    },
    "metadata": {
      "bluejay_migration": true,
      "bluejay_original_id": "<digital_human_id>"
    }
  }'
```

Record: `bluejay_digital_human_id → coval_test_case_id`

## Phase 3: Depends on Phase 1 + 2 (Step 8)

### Step 8: Migrate Run Templates

Map Bluejay Simulations → Coval Run Templates.

For each Bluejay simulation, create a Run Template that ties together the migrated resources:

1. Look up `coval_agent_id` from `bluejay_agent_id` (the simulation's agent)
2. Pick the first persona mapped from a digital human in this simulation, or ask the user
3. Look up `coval_test_set_id` from the simulation mapping
4. Collect `coval_metric_ids` from the agent's associated metrics

```bash
curl -s -X POST "https://api.coval.dev/v1/run-templates" \
  -H "X-API-Key: <COVAL_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "<simulation_name> Template",
    "description": "Migrated from Bluejay simulation <simulation_id>",
    "agent_id": "<coval_agent_id>",
    "persona_id": "<coval_persona_id>",
    "test_set_id": "<coval_test_set_id>",
    "metric_ids": ["<coval_metric_id_1>", "<coval_metric_id_2>"],
    "iteration_count": 1,
    "concurrency": 5,
    "metadata": {
      "bluejay_migration": true,
      "bluejay_original_id": "<simulation_id>"
    }
  }'
```

Record: `bluejay_simulation_id → coval_run_template_id`

## Phase 4: Depends on Phase 3 (Step 9)

### Step 9: Migrate Scheduled Runs

Map Bluejay Schedules → Coval Scheduled Runs.

**All scheduled runs are created DISABLED for safety.** The customer must manually enable them after review.

For each Bluejay schedule:

1. Look up `coval_run_template_id` from the simulation mapping
2. Convert schedule format:
   - Bluejay `cron` expression → Coval `cron(...)` format
   - Bluejay `every_n_minutes` → `rate(<n> minutes)`
   - Bluejay `every_n_hours` → `rate(<n> hours)`
   - Bluejay `daily` at HH:MM → `cron(<MM> <HH> ? * * *)`
   - Bluejay `weekly` → `cron(<MM> <HH> ? * <DAY> *)`
   - Bluejay `monthly` → `cron(<MM> <HH> <DOM> * ? *)`

```bash
curl -s -X POST "https://api.coval.dev/v1/scheduled-runs" \
  -H "X-API-Key: <COVAL_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "<simulation_name> Schedule",
    "run_template_id": "<coval_run_template_id>",
    "schedule_expression": "<converted_schedule>",
    "enabled": false,
    "metadata": {
      "bluejay_migration": true,
      "bluejay_original_id": "<schedule_id>"
    }
  }'
```

Record: `bluejay_schedule_id → coval_scheduled_run_id`

## Step 10: Migration Report

Print a final summary:

```
## Migration Complete

### Created Entities

| Type | Count | Details |
|------|-------|---------|
| Metrics | N | bluejay_id → coval_id for each |
| Personas | N | ... |
| Agents | N | ... |
| Test Sets | N | ... |
| Test Cases | N | ... |
| Run Templates | N | ... |
| Scheduled Runs | N | (all disabled) |

### Skipped (Already Existed)
- List any entities skipped due to idempotency

### Warnings
- List any ambiguous mappings or approximations made
- Note any `json` metrics mapped to METRIC_LLM_BINARY
- Note any voice mappings that may need review

### Next Steps
1. Review migrated entities in the Coval dashboard: https://app.coval.dev
2. Enable scheduled runs after verifying configuration
3. Run a test evaluation from a migrated Run Template to verify
4. Review persona voice assignments and adjust if needed
```

## Error Handling

- **HTTP 429 (Rate Limited)**: Wait 5 seconds and retry. Max 3 retries per request.
- **HTTP 400 (Bad Request)**: Show the error details to the user. Ask whether to fix the input and retry, or skip this entity.
- **HTTP 401/403 (Auth Error)**: Stop and ask user to verify their API key.
- **HTTP 500 (Server Error)**: Show error, skip entity, continue with others.
- **Network Error**: Retry once after 3 seconds. If still failing, stop and report what was created so far.

After any failure, always show what has been successfully created so far so the user can resume.

## Idempotency Rules

1. Before creating any entity, check the name lookup from Step 2
2. If entity exists with `bluejay_migration: true` in metadata → skip silently
3. If name collision with non-migrated entity → ask user: "A Coval <entity_type> named '<name>' already exists but wasn't from a Bluejay migration. Skip, rename, or overwrite?"
4. All created entities get metadata: `{ "bluejay_migration": true, "bluejay_original_id": "<id>" }`
5. Re-running the migration should produce zero new entities if nothing changed
