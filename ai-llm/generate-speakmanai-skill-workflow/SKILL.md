---
name: generate-speakmanai-skill-workflow
description: Design and generate a delegate-first SPEAKMAN.AI "skill workflow" — a workflow whose agents execute directly via the connected coding agent's own tools (filesystem, APIs, MCP servers, email, web search/scraping) instead of a background LLM — ready for database import
---

# generate-speakmanai-skill-workflow — SPEAKMAN.AI Skill Workflow Creator

You are running the SPEAKMAN.AI **Skill Workflow** Creator. Unlike `generate-speakmanai-workflow` (which designs a "remote" workflow — every AI step runs on a hosted background model, and any external data has to be pasted in by a human at an `MCP_INPUT_REQUIRED` pause), this skill designs a **delegate-first** workflow: agents that need real data or system access are set to `executionMode: "delegate"`, so at runtime they pause and hand execution directly to you (or whichever coding agent is connected) — you fetch the data yourself using your own tools and submit the result. Background execution is reserved for pure-reasoning steps (validators, aggregators, drafting).

This skill also has a second, unusual property: the meta-workflow that builds the design (`CLAUDE_SKILL_WORKFLOW_CREATOR_V1`) is itself fully delegate — all three of its own steps (planner, analyst, prompt engineer) are `executionMode: "delegate"`. That means **you** perform the planning, architecture, and prompt-engineering work directly, in character as instructed by each step's prompt, rather than waiting on a hosted model to do it. Follow every step below exactly.

---

## Step 0 — Check for Existing Session

Ask the user:

> "Do you have an existing SPEAKMAN.AI session ID you want to use? If so, paste it and I'll skip straight to downloading the output. Otherwise, press Enter and I'll run a new session."

- If a session ID is provided: set `session_id` to that value and **skip to Step 3**.
- Otherwise: continue to Step 1.

---

## Step 1 — Collect Workflow Intent

Ask the user:

> "Describe the skill workflow you want to build. Include:
> - What business goal or problem it solves
> - The key steps or processing stages (in rough order)
> - Which steps need real data or system access — and from where: a website/API, an internal database or CRM, the local filesystem/repo, email, or another MCP-connected tool. Be as specific as you can (exact URLs, table/entity names, file paths, tool names) — the more concrete, the more useful the generated agent will be.
> - Any points where only a human can decide (an approval, a subjective judgment call, a preference) — as opposed to data a tool could fetch
> - The expected final output (document, structured data, file written to disk, email sent, etc.)"

Extract and store as **WORKFLOW_INTENT**:
- Primary business goal
- Step sequence, and which steps are data/tool-dependent vs pure reasoning
- Concrete data sources / systems named for each tool-dependent step
- True human-decision points (if any)
- Output format
- Whether parallel branches are needed

---

## Step 2 — Run the Meta-Workflow Session

### 2a — Start session

Call `start_session`:
- `workflow_id`: `CLAUDE_SKILL_WORKFLOW_CREATOR_V1`
- `title`: Short title for the workflow being designed (max 60 chars)
- `description`: WORKFLOW_INTENT (max 3000 chars — goal, steps, data sources/tools per step, human-decision points, output format)

### 2b — Drive the delegate loop

Poll every 15–20 seconds (this session resolves as fast as you complete each step — there is no background model to wait on). Every step in this meta-workflow is delegated to you. On each `AWAITING_INPUT`:

1. Confirm `input_required.agent_type` is `MCP_LLM_DELEGATE`. If it is instead a human-facing type (`MCP_REVIEWER`/`MCP_APPROVER`/`MCP_INPUT_REQUIRED`), the platform's execution mode isn't set to delegate — tell the user and ask whether to proceed with human input or have them enable delegate mode, then handle accordingly.
2. Read `input_required.prompt` — these are **your operating instructions** for this step (they come from the corresponding agent's `systemPrompt`/description in the database: the Planner, the Skill Workflow Analyst, or the Skill Workflow Prompt Engineer).
3. Read `input_required.context` — this is your input data for the step (the business requirement and agent roster on the first pause; the prior step's output on later passes) and `input_required.schema` if present.
4. Perform the task **exactly as instructed** — you are acting as that role, not summarizing or shortcutting it:
   - **Planner pause**: build the `WORKFLOW_EVENT` JSON that sequences the Analyst then the Prompt Engineer (per the prompt's structure).
   - **Analyst pause**: act as the Workflow Architect — produce the full `{workflow, agents}` JSON, deciding `executionMode: "delegate"` vs background per agent per the delegation rule in the prompt, and include exactly one `AI_PLANNER` agent as the minimal `GENERIC_WORKFLOW_PLANNER` stub (see Step 4b) — no `systemPrompt` field on it at all.
   - **Prompt Engineer pause**: act as the Prompt Engineer — write every `systemPrompt`, tool-aware for delegate agents, pure-reasoning for background agents, leaving the `AI_PLANNER` (`GENERIC_WORKFLOW_PLANNER`) stub untouched — do not add a `systemPrompt` to it.
5. Call `submit_response(session_id, <your result>)` with the result (stringified JSON where the step expects JSON). Also pass `executed_by`: the name of your tool and your model, for example `Claude Code, claude-opus-5-5` (say what you actually are and do not guess; it is recorded with the output).

Continue until `status = COMPLETED`.

---

## Step 3 — Retrieve the Final Output

Call `get_outputs(session_id)` for the manifest, then `get_output(session_id, "CLAUDE_SKILL_PROMPT_ENGINEER_V1")` for the complete workflow JSON with every `systemPrompt` populated. This should match what you generated during the Prompt Engineer pause in Step 2b — use the stored version as the source of truth.

> **This is the only output you need.**

---

## Step 4 — Save Workflow JSON

Parse the `CLAUDE_SKILL_PROMPT_ENGINEER_V1` output — a JSON object with a `workflow` key and an `agents` array.

Create the output directory: `outputs/YYYY-MM-DD_{slug}/` where slug is a lowercase-hyphenated version of the workflow title and YYYY-MM-DD is today's date.

**Save using the `Write` tool directly.** Save to: `outputs/YYYY-MM-DD_{slug}/{workflowId}.json`.

---

## Step 4b — Pre-Import Safety Check

Scan the `agents` array for an agent with `agentType == "AI_PLANNER"`.

**If no `AI_PLANNER` agent is present:** this is a generation error — the workflow has no entry point and will fail at runtime. Flag it to the user before proceeding; do not attempt to fabricate one yourself.

**If an `AI_PLANNER` agent is present:** every workflow on the platform shares a single planner document, `GENERIC_WORKFLOW_PLANNER` — its `systemPrompt`/`model`/`temperature`/`executionMode`/etc. live once, centrally, in the database (canonically mirrored in `speakmanai_lite/WorkflowsAndAgents/MCP_SOLUTION_ARCHITECTURE_V1.json`). This workflow's own JSON must reference it only as a **minimal stub**:
```json
{ "agentId": "GENERIC_WORKFLOW_PLANNER", "workflows": ["<this workflow's ID>"] }
```
No other fields — no `systemPrompt` (not even `""`), no `agentType`, `model`, `temperature`, `mimeType`, `executionMode`, `dependencies`, `inputSchema`. This matters: the import tool merges `workflows` into the existing shared document safely via `$addToSet`, but any other field present here gets `$set` directly onto that same shared document — silently overwriting the real planner's config for every other workflow that depends on it, including whether it delegates. (The planner's own execution mode is controlled by the platform's *global* execution-mode setting, not by anything set per-workflow — flipping that global setting to `force_delegate` before running this workflow puts the planning step on the connected coding agent too, without needing a workflow-specific override here.)

If the agent has any other field (the Analyst/Prompt Engineer didn't fully apply this rule), strip it down to just the two-field stub above, re-save with `Write`, and report what you changed.

---

## Step 5 — Report

Report the following to the user:

```
Session ID     : {session_id}
Workflow ID    : {workflowId}
Agents         : {agent_count} total — {delegate_count} delegate (run on your tools), {background_count} background (validators/aggregators/drafting)
Output file    : outputs/{slug}/{workflowId}.json
```

Then say:

"Your delegate-first workflow definition is ready. To import it into SPEAKMAN.AI:

1. Review `{workflowId}.json` — check which agents are delegate vs background, and that each delegate agent's `systemPrompt` correctly names the tool/data source it should use.
2. Import using the MCP tools:
   - **Try first:** call `import_architecture_plan(plan_json)` with the full JSON string — imports the workflow and all agents in one call.
   - **If the file is too large** (typically >30KB): call `import_workflow(workflow_json)` with the `workflow` object, then call `import_agent(agent_json)` once per agent in the `agents` array. Both tools are idempotent — safe to re-run.
3. The workflow will appear in `list_workflows` immediately after import.
4. Before running it for real, make sure the platform's execution mode allows delegation for the agents marked `executionMode: \"delegate\"` — either the global setting is `auto` (default, per-agent field respected) or `force_delegate`. If it's `force_background`, delegate steps will run on a background model with no tools instead, which defeats the point of this design — call `set_execution_mode` to fix it if needed."

---

## Notes

- The `systemPrompt` fields are generated by you, in character as the Analyst/Prompt Engineer roles — review them with the user before import, especially any delegate agent touching sensitive systems (email, internal APIs, databases) or any validator/approval gate.
- `AI_VALIDATOR` agents appear in the `agents` array but are **not** workflow steps — they attach to their primary agent via `validatorAgentId`, and are always background (never `executionMode: "delegate"`).
- If a `systemPrompt` field is an empty string, the Prompt Engineer step did not populate it — flag before import. The `AI_PLANNER` (`GENERIC_WORKFLOW_PLANNER`) agent is the only exception, and it should have no `systemPrompt` field at all, not an empty one — see Step 4b.
- Reserve `MCP_INPUT_REQUIRED` for things only a human can decide. If a generated agent uses `MCP_INPUT_REQUIRED` to ask for data a tool could fetch (a URL, a DB record, a file), that's a design smell — point it out to the user; it should likely be a delegate `AI_WORKFLOW` agent instead.
- For the difference between this skill and `generate-speakmanai-workflow`: use this one when the workflow will primarily run inside a coding-agent session with real tool access; use the other when the workflow should run unattended against a hosted background model with humans supplying any external data through pause steps.
