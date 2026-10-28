---
name: swamp
description: Model any API with Swamp, test it, and enrich *Claw with new capabilities — full lifecycle from idea to working integration
version: 0.1.0
metadata:
  openclaw:
    requires:
      bins:
        - swamp
    emoji: "🐊"
    homepage: https://github.com/systeminit/swamp
---

# Swamp — API Modeling & *Claw Enrichment

You are an AI agent that uses Swamp to model any API, test it, and turn it into a reusable *Claw capability. Swamp is an AI-native automation CLI that represents external resources (APIs, CLIs, cloud services) as typed models with executable methods and composable workflows.

## Repository Setup

Before any operation, check if the current directory is a swamp repository. If not, initialize one:

```bash
swamp repo init --tool claude
```

This creates a `.swamp/` directory with the necessary structure. Use `--tool claude` to set up the AI agent integration for Claude/OpenClaw.

## API Modeling Workflow

### Step 1: Discover Model Types

Find available model types to understand what kinds of resources can be modeled:

```bash
swamp model type search
swamp model type describe <type>
```

The `command/shell` type is the most versatile — it can model any API via shell commands (curl, httpie, CLI tools).

### Step 2: Create a Model

Create a new model definition for the API:

```bash
swamp model create <type> <name>
```

Example: `swamp model create command/shell github-issues`

### Step 3: Edit the Model Definition

Open and edit the model's YAML definition to configure endpoints, authentication, parameters, and methods:

```bash
swamp model edit <name>
```

When editing, define:
- **Methods**: The operations this API supports (list, create, update, delete)
- **Inputs**: Parameters each method accepts
- **Authentication**: Reference vault secrets via CEL expressions
- **Commands**: The actual shell commands (curl calls, CLI invocations) that execute each method

### Step 4: Validate

Ensure the model definition is well-formed:

```bash
swamp model validate <name>
```

Fix any validation errors before proceeding.

## Testing & Execution

### Run a Method

Execute a method on your model to test it:

```bash
swamp model method run <model_name> <method_name>
```

### Inspect Results

Check outputs, logs, and data from the execution:

```bash
swamp model output get <output_id_or_model_name>
swamp model output logs <output_id>
swamp model output data <output_id>
```

### Review History

See past executions:

```bash
swamp model method history search
swamp model method history get <output_id_or_model_name>
```

Iterate on the model definition until methods return the expected results.

## Workflow Orchestration

Chain multiple model methods into automated workflows with dependency ordering:

```bash
swamp workflow create <name>
swamp workflow edit <name>
swamp workflow validate <name>
swamp workflow run <name>
```

Workflows support:
- Parallel job execution
- Dependency ordering between jobs
- Trigger conditions via CEL expressions
- Cross-model references (one model's output feeds into another)

Check workflow results:

```bash
swamp workflow history get <name>
swamp workflow history logs <run_id>
```

## Vault & Credentials

Store API keys and secrets securely — never hardcode them:

```bash
swamp vault create <type> <name>
swamp vault put <vault_name> <KEY=value>
swamp vault list-keys <vault_name>
```

Reference secrets in model definitions using CEL expressions like `vault.get("my-vault", "API_KEY")`.

## Data Management

Inspect outputs and artifacts across models:

```bash
swamp data list <model_name>
swamp data get <model_name> <data_name>
swamp data search <query>
```

## Enriching *Claw with New Capabilities

Once a Swamp model is validated and working, turn it into a standalone *Claw skill:

1. **Export the model**: Use `swamp model get <name> --json` to extract the full definition
2. **Generate a SKILL.md**: Create a new skill file that wraps the Swamp model's methods as agent instructions
3. **Include setup instructions**: Document the required env vars, binaries, and vault configuration
4. **Publish to ClawHub**: Share the skill with the community via `clawhub publish`

The generated skill should:
- Require `swamp` in its `bins` dependency
- Reference the swamp repo and model by name
- Map each model method to a clear agent instruction
- Include examples of typical invocations

## Examples

### Model a REST API

> "Model the JSONPlaceholder API so I can list and create posts"

1. `swamp model create command/shell jsonplaceholder`
2. Edit to add methods: `list-posts` (GET /posts), `create-post` (POST /posts)
3. `swamp model method run jsonplaceholder list-posts`
4. Verify output, iterate

### Set Up a Weather Integration

> "Create a weather model that fetches forecasts by city"

1. `swamp model create command/shell weather`
2. Edit to add a `forecast` method using `curl -s "wttr.in/{city}?format=j1"`
3. Test with `swamp model method run weather forecast`

### Chain APIs in a Workflow

> "Create a workflow that fetches GitHub issues, summarizes them, and posts to Slack"

1. Create models: `github-issues`, `slack-webhook`
2. Create workflow: `swamp workflow create issue-digest`
3. Define jobs with dependencies: fetch issues -> format summary -> post to Slack
4. `swamp workflow run issue-digest`

### Graduate to a *Claw Skill

> "Turn my working weather model into a skill others can install"

1. `swamp model get weather --json` to export
2. Create a new `SKILL.md` wrapping the weather model commands
3. `clawhub publish ./weather-skill`

## Important Notes

- Always use `--json` flag when you need to parse Swamp output programmatically
- Use `swamp model validate` before running to catch definition errors early
- Store all credentials in vaults, never in model definitions
- Use `-v` (verbose) flag when debugging unexpected behavior
- All Swamp operations run locally — credentials stay on the user's machine
