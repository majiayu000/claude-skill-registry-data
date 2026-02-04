---
name: Plexus Score Setup
description: Standard workflow for creating Plexus scorecard and score records via the GraphQL API. This is the administrative setup (name, external_id, description) - NOT guidelines or configuration work.
---

## Purpose

This skill provides the workflow for creating scorecard and score records in Plexus via the GraphQL API. This is the **administrative setup** - creating the records with metadata like names, external IDs, and descriptions. This is separate from content work like guidelines and configuration.

## When to Use This Skill

Use this skill when:
- User needs to create a new scorecard
- User needs to add a new score to an existing scorecard
- User needs to set up the records in Plexus before working on guidelines/config
- User says they need to "set up" or "create" a scorecard or score

## Important: What This Skill Does NOT Cover

This skill is ONLY about creating records via the GraphQL API. It does NOT cover:
- Guidelines development (use `plexus-score-guidelines-updater` agent for that)
- Score configuration/YAML (use `plexus-score-config-updater` agent for that)
- Classifier types, classes, labels, or any classification mechanics

Those are separate workflows that happen AFTER the basic records are created via the API.

## Complete Workflow

**Note**: All operations use the Plexus GraphQL API via MCP tools. Do NOT use the `plexus` CLI command.

### Phase 1: Information Gathering

Before doing ANY work, gather this basic metadata from the user:

#### If Creating a New Scorecard:

1. **Scorecard name** (human-readable, e.g., "Acme Content Quality")
2. **Scorecard key** (web slug: lowercase with hyphens, ideally starts with client name, e.g., "acme-content-quality")
3. **Scorecard external_id** (required, can be same as key)
4. **Scorecard description** (short description of what this scorecard is for)

#### If Creating a New Score:

1. **Which scorecard** does this score belong to?
   - If unsure, use `mcp__Plexus__plexus_scorecards_list` to list available scorecards
2. **Score name** (human-readable, e.g., "Medical Advice Detection")
3. **Score external_id** (kebab-case, e.g., "medical-advice")
4. **Score description** (short description of what this score measures)

**That's it!** Do NOT ask about:
- Classifier types (binary, multi-class, etc.)
- Valid classes or labels
- Target/default classes
- Classification mechanics
- Guidelines content

Those come later when working on guidelines and configuration.

**IMPORTANT**: Do NOT proceed until you have the basic metadata above. If information is missing, ask the user.

### Phase 2: Scorecard/Score Creation

#### If Creating a Scorecard:

1. **Check if scorecard already exists**
   ```
   Use mcp__Plexus__plexus_scorecards_list to see existing scorecards
   ```

2. **Create the scorecard record** (if it doesn't exist)
   ```
   Use mcp__Plexus__plexus_scorecard_create with:
   - scorecard_name: the human-readable name
   - key: the web slug (lowercase with hyphens)
   - external_id: required identifier
   - description: short description
   ```

3. **Verify creation**
   ```
   Use mcp__Plexus__plexus_scorecard_info to confirm the scorecard was created
   ```

#### If Creating a Score:

1. **Check if score already exists**
   ```
   Use mcp__Plexus__plexus_scorecard_info with the scorecard name
   Review the list of scores to see if this score already exists
   ```

2. **Create the score record** (if it doesn't exist)
   ```
   Use mcp__Plexus__plexus_score_create with:
   - scorecard_name: the scorecard name
   - score_name: the human-readable name
   - score_external_id: the kebab-case identifier
   - description: short description
   ```

3. **Verify creation**
   ```
   Use mcp__Plexus__plexus_score_info to confirm the score was created
   ```

### Phase 3: Handoff

After creating the records via the API:

1. **Summarize what was created**
   - Scorecard name, key, external_id (if applicable)
   - Score name, external_id (if applicable)
   - What records now exist in Plexus

2. **Next steps** (inform user of options):
   - They can now work on guidelines (use `plexus-score-guidelines-updater` agent)
   - After guidelines, they can work on configuration (use `plexus-score-config-updater` agent)
   - Or they can leave them as stubs for now and return to them later
   - Guidelines and config can be created separately from this setup

## Critical Rules

### Scope: This is Administrative Setup Only
- This skill ONLY covers creating records via the GraphQL API
- Do NOT gather information about classification mechanics
- Do NOT create guidelines or configuration as part of this workflow
- Guidelines and config are separate workflows that happen later (or never, if just doing stub setup)

### Do Not Skip Steps
- Always gather basic metadata BEFORE creating anything
- Always verify creation after using create tools
- If user wants guidelines/config too, create the records FIRST, then hand off to agents

### Use the Right Tools
- **Scorecard creation**: Use `mcp__Plexus__plexus_scorecard_create` MCP tool (you, the main agent)
- **Score creation**: Use `mcp__Plexus__plexus_score_create` MCP tool (you, the main agent)
- **DO NOT** use the `plexus` CLI command - only use MCP tools which call the GraphQL API

### Information Management
- Only ask for the basic metadata listed in Phase 1
- Do NOT ask about classifier types, classes, or classification logic
- If you're missing basic metadata, stop and ask the user

## Common Mistakes to Avoid

1. **Asking about classification details** - This workflow only needs basic metadata (name, external_id, description)
2. **Trying to create guidelines/config immediately** - Those are separate workflows; just create the records
3. **Using CLI instead of MCP** - Always use MCP tools
4. **Assuming guidelines/config must be complete** - They can be stubs initially
5. **Conflating setup with content work** - Setup = database records, Content = guidelines + config

## Example Session Flow

### Example 1: Creating Just the Score Record

```
User: "I need to set up a new score for medical advice detection in the content-quality scorecard"

Claude: I'll help you create the score record. I need some basic information:

1. Which scorecard? (you said content-quality - I'll verify it exists)
2. Score name? (e.g., "Medical Advice Detection")
3. Score external_id? (e.g., "medical-advice")
4. Short description? (what does this score measure?)

User: [Provides: "Medical Advice Detection", "medical-advice", "Detects if content contains medical advice"]

Claude: Great! Let me create the score record.
[Uses mcp__Plexus__plexus_score_create]
[Uses mcp__Plexus__plexus_score_info to verify]

Done! The score "Medical Advice Detection" has been created in the content-quality scorecard with external_id "medical-advice".

Next steps (when you're ready):
- Create guidelines using the plexus-score-guidelines-updater agent
- Create configuration using the plexus-score-config-updater agent
- Or leave as a stub for now
```

### Example 2: Creating a New Scorecard

```
User: "I need to create a new scorecard for the Acme client"

Claude: I'll help you create the scorecard. I need:

1. Scorecard name? (e.g., "Acme Content Quality")
2. Scorecard key? (web slug, ideally starts with client name, e.g., "acme-content-quality")
3. External_id? (can be same as key)
4. Short description?

User: [Provides information]

Claude: Perfect! Let me create the scorecard.
[Uses mcp__Plexus__plexus_scorecard_create]
[Uses mcp__Plexus__plexus_scorecard_info to verify]

Done! The scorecard "Acme Content Quality" has been created with key "acme-content-quality".

You can now add scores to this scorecard when you're ready.
```

## Troubleshooting

### Scorecard Already Exists
If `plexus_scorecard_create` fails because the scorecard exists:
- Use `mcp__Plexus__plexus_scorecard_info` to check current state
- Inform the user the scorecard already exists
- Ask if they want to update it or create scores within it instead

### Score Already Exists
If `plexus_score_create` fails because the score exists:
- Use `mcp__Plexus__plexus_score_info` to check current state
- Inform the user the score already exists
- Ask if they want to update metadata or work on guidelines/config instead

### Missing Information
If you realize you're missing basic metadata:
- STOP and ask the user for the specific fields (name, external_id, description, key)
- Do not make assumptions about naming or identifiers
- Do not proceed without the required metadata

## Working on Score Configuration (YAML)

**CRITICAL**: If the user wants to work on score configuration YAML code (creating or editing), you MUST use the `plexus-score-config-updater` agent. Do NOT attempt to edit score configuration YAML yourself.

### When to Use the Config Updater Agent

Use `plexus-score-config-updater` agent when:
- User wants to create initial YAML configuration for a score
- User wants to update/modify existing score configuration
- User wants to sync configuration with updated guidelines
- User mentions "score config", "score YAML", "configuration code"

### Why This Agent is Required

The score configuration YAML is complex and requires:
- Understanding of Plexus data source configurations
- Knowledge of classifier/extractor structures
- Proper YAML formatting and validation
- Running evaluations to verify changes

**The agent MUST load comprehensive Plexus documentation** before working on any configuration. The documentation explains data sources, classifier structures, YAML formatting, and scoring logic.

### How to Use It

```
Use Task tool with subagent_type="plexus-score-config-updater"
The agent will:
1. FIRST: Load documentation using get_plexus_documentation(filename="score-yaml-format")
2. Pull current configuration (or create from scratch)
3. Make changes based on guidelines and requirements
4. Validate with a 10-sample evaluation
5. Push only if evaluation passes
```

The agent knows to load the documentation automatically - you don't need to specify this.

**Never edit score configuration YAML directly in the main conversation** - always delegate to this agent.

### Basic Score YAML Configuration Template

Most scores follow this basic structure using a LangGraphScore with a single Classifier node:

```yaml
name: Score Name
id: "score-id-from-api"
description: Brief description of what this score measures
class: LangGraphScore
model_provider: ChatOpenAI
model_name: gpt-4o-mini-2024-07-18
graph:
  - name: score_check
    class: Classifier
    valid_classes:
      - Yes
      - No
      # Add "NA" for binary with abstentions
    system_message: >
      System prompt that sets the context and role for the classifier.
    user_message: >
      User prompt that provides the specific task and instructions.

      CALL TRANSCRIPT: <transcript> {{text}} </transcript>

      [Detailed instructions about when to mark each class]

      Answer with the appropriate class.
    parse_from_start: true
output:
  value: classification
  explanation: explanation
data:
  class: FeedbackItems
  scorecard: scorecard-id-number
  score: Score Name
  days: 90
  limit: 200
  limit_per_cell: 50
  balance: false
key: score-key-kebab-case
```

**Key Components:**
- **LangGraphScore**: The main score class for most classifiers
- **Classifier node**: Single node that runs the classification
- **valid_classes**: List of classes (Yes/No for binary, add NA for abstentions, or multiple classes)
- **system_message & user_message**: The prompts (can reference existing prompts from legacy scores)
- **data.FeedbackItems**: Standard data source configuration for evaluation
- **{{text}}**: Template variable that gets replaced with the transcript

When creating configuration, provide this template to the config-updater agent as a reference.

## Related Skills and Agents

- **plexus-guidelines skill**: Format and validation rules for guidelines documents
- **plexus-score-guidelines-updater agent**: Creates/updates guidelines
- **plexus-score-config-updater agent**: Creates/updates YAML configuration (USE THIS FOR ALL CONFIG WORK)
- **plexus-alignment-analyzer agent**: Analyzes feedback to improve configs (used later for iteration)

## Success Criteria

You've successfully completed this workflow when:
1. Scorecard/score record exists in Plexus (via GraphQL API) with correct metadata (name, external_id, description, key if scorecard)
2. Creation is verified using the MCP info tools
3. User is informed what was created
4. User knows the next steps (guidelines/config work) is separate and optional