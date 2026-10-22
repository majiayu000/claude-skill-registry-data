---
name: generate-speakmanai-workflow
description: Design and generate a SPEAKMAN.AI workflow definition file ready for database import
---

# generate-speakmanai-workflow — SPEAKMAN.AI Workflow Creator

You are running the SPEAKMAN.AI Workflow Creator. You will orchestrate a SPEAKMAN.AI MCP session that designs a complete multi-agent workflow — agent structure, dependencies, and system prompts — and save the result as a JSON file ready for database import.

This skill is for internal use. The output is not a document — it is a workflow definition file.

Follow every step below exactly. Do not invent agent definitions or system prompts yourself.

---

## Step 0 — Check for Existing Session

Before collecting any input, ask the user:

> "Do you have an existing SPEAKMAN.AI session ID you want to use? If so, paste it and I'll skip straight to downloading the output. Otherwise, press Enter and I'll run a new session."

- If a session ID is provided: set `session_id` to that value and **skip to Step 3**.
- If no session ID is provided: continue to Step 1.

---

## Step 1 — Collect Workflow Intent

Ask the user:

> "Describe the workflow you want to build. Include:
> - What business goal or problem it solves
> - The key steps or processing stages (in rough order)
> - Any human review or approval points (where a person should review before continuing)
> - The expected final output (document, structured data, item library update, etc.)
> - Any specific agent types you need (e.g. item extraction, capabilities input, free-text input gate)"

Read and parse the response. Extract:
- Primary business goal
- Intended output format (document, JSON, items, etc.)
- Approximate step count and sequence
- Any MCP_PAUSE / HITL requirements described
- Any domain-specific context (regulatory, technical, creative, etc.)
- Whether parallel branches are needed (steps that can run independently)

Store this as **WORKFLOW_INTENT**.

---

## Step 2 — Run SPEAKMAN.AI Session

### 2a — Start session

Call `start_session`:
- `workflow_id`: `WORKFLOW_CREATOR_V1`
- `title`: Short title derived from the workflow being designed (max 60 chars, e.g. "Workflow Design — Customer Onboarding Analyser")
- `description`: Workflow intent from WORKFLOW_INTENT (max 3000 chars — include goal, steps, HITL requirements, and output format)

Poll every 30 seconds. The session may complete directly or pause for review.

### 2b — Handle review pause (if AWAITING_INPUT)

If the session reaches `AWAITING_INPUT`, the Workflow Analyst has produced a draft agent structure and is asking for review before the Prompt Engineer writes the system prompts.

When AWAITING_INPUT arrives:
1. Read `input_required.context` — this contains the draft workflow JSON with agent definitions and empty `systemPrompt` fields.
2. Display a summary table to the user:

| # | Agent ID | Type | Model | Dependencies |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

3. Say: "Here is the proposed agent structure — confirm to proceed to prompt generation, or describe any changes."

4. On confirmation (or with changes incorporated): call `submit_response(session_id, <reviewed or original JSON>)`. Also pass `executed_by`: the name of your tool and your model, for example `Claude Code, claude-opus-5-5` (say what you actually are and do not guess; it is recorded with the output).

Poll every 60 seconds until `status = COMPLETED`. Prompt generation takes 5–10 minutes.

---

## Step 3 — Download Workflow Output

Call `get_outputs(session_id)` to get the manifest.

Call `get_output` for `PROMPT_ENGINEER_V1` — this contains the complete workflow JSON with all `systemPrompt` fields populated.

> **This is the only output you need.** Do not download other agent outputs.

---

## Step 4 — Save Workflow JSON

Parse the output from `PROMPT_ENGINEER_V1`. It should be a JSON object with a `workflow` key and an `agents` array.

Create the output directory: `outputs/YYYY-MM-DD_{slug}/` where slug is a lowercase-hyphenated version of the workflow title and YYYY-MM-DD is today's date.

**Save using the `Write` tool directly** — the content is already in context from `get_output`. Do not use bash scripts or Python to write the file.

Save to: `outputs/YYYY-MM-DD_{slug}/{workflowId}.json`

Where `{workflowId}` is the value of `workflow.workflowId` from the JSON.

---

## Step 4b — Pre-Import Safety Check

Before importing, scan every agent in the `agents` array for the agent ID `GENERIC_WORKFLOW_PLANNER`.

**If `GENERIC_WORKFLOW_PLANNER` is not present:** the generated workflow is missing its planner — this is a generation error. Flag it to the user before proceeding.

**If `GENERIC_WORKFLOW_PLANNER` is present:** it must be a **minimal stub, nothing else**:
```json
{ "agentId": "GENERIC_WORKFLOW_PLANNER", "workflows": ["<this workflow's ID>"] }
```
No `systemPrompt`, `agentType`, `model`, `temperature`, `mimeType`, `executionMode`, or any other field. `GENERIC_WORKFLOW_PLANNER` is a single agent document shared by every workflow on the platform — its real `systemPrompt`/config lives once, centrally, in the database (canonically mirrored in `speakmanai_lite/WorkflowsAndAgents/MCP_SOLUTION_ARCHITECTURE_V1.json`). The import tool (`import_agent`/`import_architecture_plan`) merges the `workflows` field into that shared document safely via `$addToSet` — but any other field present in this agent's JSON gets `$set` directly onto that same shared document, silently overwriting the real planner's prompt and config for every other workflow that depends on it.

If the Analyst generated a full agent block here (a `systemPrompt`, its own `model`/`temperature`, etc. — this can happen if the model didn't fully apply its instructions), **do not "fix" it by writing in a canonical prompt.** Strip it down to just `{ "agentId": "GENERIC_WORKFLOW_PLANNER", "workflows": ["<this workflow's ID>"] }`, re-save with the `Write` tool, and report: "Reduced `GENERIC_WORKFLOW_PLANNER` to a minimal stub — the shared planner's real config lives centrally and must never be overwritten per-workflow."

If it's already a minimal stub, proceed directly to Step 5.

---

## Step 5 — Report

Report the following to the user:

```
Session ID     : {session_id}
Credits used   : {session_cost}   (only if a tool reported a cost; leave this line out otherwise)
Workflow ID    : {workflowId}
Agents         : {agent_count} ({ai_count} AI, {mcp_count} MCP/HITL, {validator_count} validators)
Output file    : outputs/{slug}/{workflowId}.json
```

Then say:

"Your workflow definition is ready. To import it into SPEAKMAN.AI:

1. Review `{workflowId}.json` — check agent IDs, dependencies, and system prompts before importing.
2. Import using the MCP tools:
   - **Try first:** call `import_architecture_plan(plan_json)` with the full JSON string — imports the workflow and all agents in one call.
   - **If the file is too large** (typically >30KB): call `import_workflow(workflow_json)` with the `workflow` object, then call `import_agent(agent_json)` once per agent in the `agents` array. Both tools are idempotent — safe to re-run.
3. The workflow will appear in `list_workflows` immediately after import."

---

## Notes

- The `systemPrompt` fields are generated by the AI. Review them before importing — especially validators, HITL agents, and any agent handling sensitive data.
- `AI_VALIDATOR` agents appear in the `agents` array but are **not** workflow steps — they are attached to their primary agent via `validatorAgentId`.
- If a `systemPrompt` field is empty string `""`, the Prompt Engineer did not populate it. Flag these before import — except on `GENERIC_WORKFLOW_PLANNER`, which should have no `systemPrompt` field at all (see Step 4b), not an empty one.
- **`GENERIC_WORKFLOW_PLANNER` is required and must never be renamed or given its own content.** It's a single shared agent document every workflow on the platform reuses — its real `systemPrompt`/config lives once, centrally, in the database (canonically mirrored in `speakmanai_lite/WorkflowsAndAgents/MCP_SOLUTION_ARCHITECTURE_V1.json`). This workflow's own JSON must reference it only as a minimal `{ "agentId": "GENERIC_WORKFLOW_PLANNER", "workflows": [...] }` stub (see Step 4b) — never with its own `systemPrompt` or config, which would overwrite the shared document for every other workflow on import.
